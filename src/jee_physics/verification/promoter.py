import json
from pathlib import Path
from typing import List, Optional, Tuple
import uuid

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import AtomStatus, VerificationVerdict
from jee_physics.models.verification import PromotionEvent, VerificationRecord
from jee_physics.storage.io import safe_write_json


def validate_promotion_eligibility(
    atom: KnowledgeAtom,
    verification_record: Optional[VerificationRecord],
    solver_runs_dir: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """Strictly validates whether a staged KnowledgeAtom is eligible for canonical promotion.
    
    Safety Invariants:
    1. A valid VerificationRecord must exist.
    2. The record's atom_id, atom_version, and content_hash must match the atom exactly.
    3. The verdict must be either VERIFIED or SOURCE_ERROR.
       (AMBIGUOUS, UNRESOLVED, and MODEL_ERROR are strictly forbidden from promotion).
    4. Anti-self-promotion: A candidate atom in staging cannot grant itself VERIFIED status.
    5. The verified answer is derived authoritatively from the VerificationRecord, not from unverified staging claims.
    6. Forged solver runs: If solver_runs_dir is provided, all solver_run_ids must exist on disk and match the atom_id.
    """
    errors: List[str] = []

    if verification_record is None:
        errors.append("No VerificationRecord provided. Staged atoms cannot be promoted without independent verification.")
        return False, errors

    # Check referential integrity
    if verification_record.atom_id != atom.atom_id:
        errors.append(
            f"VerificationRecord atom_id mismatch: expected '{atom.atom_id}', found '{verification_record.atom_id}'."
        )

    if verification_record.atom_version != atom.atom_version:
        errors.append(
            f"VerificationRecord atom_version mismatch: atom is v{atom.atom_version}, record is v{verification_record.atom_version}."
        )

    if verification_record.content_hash != atom.content_hash:
        errors.append(
            f"VerificationRecord content_hash mismatch: atom hash '{atom.content_hash}' does not match verified hash '{verification_record.content_hash}'."
        )

    # Check promotable verdict
    promotable_verdicts = [VerificationVerdict.VERIFIED, VerificationVerdict.SOURCE_ERROR]
    if verification_record.verdict not in promotable_verdicts:
        errors.append(
            f"Verdict '{verification_record.verdict.value}' is not eligible for canonical promotion. "
            f"Only VERIFIED and SOURCE_ERROR atoms may be promoted."
        )

    # Check solver count
    if not verification_record.solver_run_ids:
        errors.append("VerificationRecord contains no solver_run_ids.")

    # Validate solver run existence and integrity if solver_runs_dir is specified
    if solver_runs_dir is not None:
        runs_dir = Path(solver_runs_dir)
        if not runs_dir.exists():
            errors.append(f"Solver runs directory does not exist: '{runs_dir}'.")
        else:
            for run_id in verification_record.solver_run_ids:
                run_file = runs_dir / f"{run_id}.json"
                if not run_file.exists():
                    errors.append(f"Forged or missing solver run record for solver_run_id '{run_id}'.")
                else:
                    try:
                        run_data = json.loads(run_file.read_text(encoding="utf-8"))
                        if run_data.get("atom_id") != atom.atom_id:
                            errors.append(
                                f"Solver run '{run_id}' target atom mismatch: "
                                f"expected '{atom.atom_id}', found '{run_data.get('atom_id')}'."
                            )
                    except Exception as e:
                        errors.append(f"Failed to read solver run '{run_id}': {e}")

    # Check consensus answer presence for questions
    if atom.question is not None and not verification_record.consensus_answer:
        errors.append("VerificationRecord contains no consensus_answer for question atom.")

    # Check provenance
    if not atom.provenance:
        errors.append("Atom has empty provenance. Canonical atoms must have traceable provenance.")

    return len(errors) == 0, errors


def promote_atom_to_canonical(
    atom: KnowledgeAtom,
    verification_record: VerificationRecord,
    kb_atoms_dir: Path,
    manifests_dir: Optional[Path] = None,
    staged_path: str = "build/staging/atoms/",
    solver_runs_dir: Optional[Path] = None,
) -> PromotionEvent:
    """Atomically promotes a staged KnowledgeAtom into canonical kb/atoms/.
    
    Ensures:
    - Zero promotion of unverified or mismatched atoms.
    - Explicit distinction between source_claimed_answer and verified_answer.
    - Atomic file write to prevent partial corruption.
    - Audit event logging.
    """
    is_eligible, errors = validate_promotion_eligibility(
        atom=atom,
        verification_record=verification_record,
        solver_runs_dir=solver_runs_dir,
    )
    if not is_eligible:
        raise ValueError(
            f"Atom '{atom.atom_id}' failed promotion eligibility checks:\n - " + "\n - ".join(errors)
        )

    kb_atoms_dir = Path(kb_atoms_dir)
    kb_atoms_dir.mkdir(parents=True, exist_ok=True)

    target_path = kb_atoms_dir / f"{atom.atom_id}.json"

    # Construct canonical atom payload with explicit verified vs source claim distinction
    canonical_atom = atom.model_copy(deep=True)
    canonical_atom.verification_status = AtomStatus.VERIFIED

    if canonical_atom.question is not None:
        # Preserve source claim intact
        canonical_atom.question.source_claimed_answer = verification_record.source_claimed_answer
        # Authoritatively assign verified answer from verification record
        canonical_atom.question.verified_answer = verification_record.consensus_answer
        canonical_atom.question.answer = verification_record.consensus_answer

        if verification_record.source_solution:
            canonical_atom.question.source_solution = verification_record.source_solution

    # Atomic write to canonical kb/atoms/
    payload_dict = canonical_atom.model_dump(mode="json")
    safe_write_json(target_path, payload_dict)

    # Create PromotionEvent
    prov = atom.provenance[0] if atom.provenance else None
    event = PromotionEvent(
        promotion_id=f"promo-{atom.atom_id}-{uuid.uuid4().hex[:6]}",
        atom_id=atom.atom_id,
        verification_id=verification_record.verification_id,
        source_id=prov.source_id if prov else verification_record.source_id,
        atom_version=atom.atom_version,
        staged_path=staged_path,
        canonical_path=str(target_path),
        verdict=verification_record.verdict,
        source_claimed_answer=verification_record.source_claimed_answer,
        verified_answer=verification_record.consensus_answer,
    )

    if manifests_dir:
        manifests_dir = Path(manifests_dir)
        manifests_dir.mkdir(parents=True, exist_ok=True)
        event_path = manifests_dir / f"{event.promotion_id}.json"
        safe_write_json(event_path, event.model_dump(mode="json"))

    return event
