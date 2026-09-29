from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from jee_physics.core.hasher import compute_content_hash
from jee_physics.core.ids import generate_review_id
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import AtomStatus, ReviewIssueType, ReviewStatus
from jee_physics.models.review import ReviewQueueItem
from jee_physics.models.source import SourceRegistryRecord
from jee_physics.storage.io import read_json
from jee_physics.validation.latex_linter import lint_latex_syntax


@dataclass
class BatchValidationResult:
    valid_atoms: List[KnowledgeAtom] = field(default_factory=list)
    invalid_atoms: List[Tuple[KnowledgeAtom, List[str]]] = field(default_factory=list)
    review_items: List[ReviewQueueItem] = field(default_factory=list)
    duplicate_ids: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return len(self.invalid_atoms) == 0 and len(self.duplicate_ids) == 0


def _recompute_content_hash(atom: KnowledgeAtom) -> str:
    """Deterministically computes or recomputes the content hash of an atom."""
    if atom.question:
        opt_str = "".join(opt.text for opt in atom.question.options)
        return compute_content_hash(atom.question.statement + opt_str)
    if atom.formula:
        return compute_content_hash(atom.formula.formula_latex)
    if atom.solved_example:
        steps_str = "".join(sm.steps for sm in atom.solved_example.solution_steps)
        return compute_content_hash(atom.solved_example.problem_statement + steps_str)
    if atom.misconception:
        return compute_content_hash(atom.misconception.stated_misconception + atom.misconception.correction)
    if atom.content:
        return compute_content_hash(atom.content)
    return compute_content_hash(atom.title)


def validate_staged_atom_batch(
    atoms: List[KnowledgeAtom],
    registry_dir: Path,
    expected_source_id: Optional[str] = None,
    existing_atom_ids: Optional[Set[str]] = None,
    low_confidence_threshold: float = 0.85,
) -> BatchValidationResult:
    """Performs strict deterministic validation and sanitization on candidate Knowledge Atoms.
    
    Invariants enforced:
    1. AI State Field Sanitization: Verification status is ALWAYS forced to STAGED.
       AI candidate cannot self-promote to VERIFIED or CANONICAL.
    2. Authoritative Provenance Validation: Source ID and file name MUST match registered
       records in sources/registry/. Page numbers must fall within registered source bounds.
    3. LaTeX Delimiter and Syntax Linting: Balance of $, braces, and math commands.
    4. Duplicate ID Detection: Collisions within batch or existing staging are rejected.
    5. Exception-Only Review Queue Routing: Items with confidence < 0.85 route to review/queue/.
    """
    result = BatchValidationResult()
    seen_in_batch: Set[str] = set()
    existing_ids = existing_atom_ids or set()
    registry_dir = Path(registry_dir)

    # Pre-load expected source record if expected_source_id is provided
    expected_reg_record: Optional[SourceRegistryRecord] = None
    if expected_source_id:
        reg_file = registry_dir / f"{expected_source_id}.json"
        if not reg_file.exists():
            for atom in atoms:
                result.invalid_atoms.append(
                    (atom, [f"Expected source '{expected_source_id}' does not exist in registry."])
                )
            return result
        expected_reg_record = SourceRegistryRecord.model_validate(read_json(reg_file))

    for atom in atoms:
        atom_errors: List[str] = []

        # -------------------------------------------------------------
        # 1. State Field Sanitization & Anti-Self-Promotion
        # -------------------------------------------------------------
        if atom.verification_status != AtomStatus.STAGED:
            result.warnings.append(
                f"Atom '{atom.atom_id}' claimed verification_status '{atom.verification_status.value}'; "
                f"overridden to '{AtomStatus.STAGED.value}'."
            )
            atom.verification_status = AtomStatus.STAGED

        # Ensure AI cannot claim canonical deduplication or archive status in staging
        if atom.duplicate_group_id is not None:
            result.warnings.append(
                f"Atom '{atom.atom_id}' claimed duplicate_group_id '{atom.duplicate_group_id}'; reset to None."
            )
            atom.duplicate_group_id = None
        if atom.archive_reason is not None:
            atom.archive_reason = None

        # Recompute/verify content hash
        expected_hash = _recompute_content_hash(atom)
        if not atom.content_hash or atom.content_hash != expected_hash:
            atom.content_hash = expected_hash

        # -------------------------------------------------------------
        # 2. Duplicate ID Check
        # -------------------------------------------------------------
        if atom.atom_id in seen_in_batch:
            atom_errors.append(f"Duplicate atom_id '{atom.atom_id}' detected within current batch.")
            result.duplicate_ids.append(atom.atom_id)
        elif atom.atom_id in existing_ids:
            atom_errors.append(f"Duplicate atom_id '{atom.atom_id}' already exists in staging/kb.")
            result.duplicate_ids.append(atom.atom_id)
        else:
            seen_in_batch.add(atom.atom_id)

        # -------------------------------------------------------------
        # 3. Authoritative Provenance Validation
        # -------------------------------------------------------------
        if not atom.provenance:
            atom_errors.append("Atom has empty provenance list. Every atom must trace to at least one source.")
        else:
            for idx, prov in enumerate(atom.provenance):
                # Verify source_id matches expected_source_id if specified
                if expected_source_id and prov.source_id != expected_source_id:
                    atom_errors.append(
                        f"Provenance #{idx}: source_id '{prov.source_id}' does not match expected batch source_id '{expected_source_id}'."
                    )

                # Look up registry record for this provenance source_id
                prov_reg_file = registry_dir / f"{prov.source_id}.json"
                if not prov_reg_file.exists():
                    atom_errors.append(
                        f"Provenance #{idx}: referenced source_id '{prov.source_id}' does not exist in registry."
                    )
                    continue

                source_rec = expected_reg_record if (expected_reg_record and prov.source_id == expected_source_id) else SourceRegistryRecord.model_validate(read_json(prov_reg_file))

                # Verify file_name matches registered record exactly
                if prov.file_name.strip() != source_rec.file_name.strip():
                    atom_errors.append(
                        f"Provenance #{idx}: file_name '{prov.file_name}' does not match registered source file_name '{source_rec.file_name}'."
                    )

                # Check page bounds against registered source total_pages
                if source_rec.total_pages and source_rec.total_pages > 0:
                    if prov.page_start is not None and (prov.page_start < 1 or prov.page_start > source_rec.total_pages):
                        atom_errors.append(
                            f"Provenance #{idx}: page_start ({prov.page_start}) is outside source page bounds (1..{source_rec.total_pages})."
                        )
                    if prov.page_end is not None and (prov.page_end < 1 or prov.page_end > source_rec.total_pages):
                        atom_errors.append(
                            f"Provenance #{idx}: page_end ({prov.page_end}) is outside source page bounds (1..{source_rec.total_pages})."
                        )

                if prov.page_start is not None and prov.page_end is not None and prov.page_start > prov.page_end:
                    atom_errors.append(
                        f"Provenance #{idx}: page_start ({prov.page_start}) exceeds page_end ({prov.page_end})."
                    )

                # Check source_sha256 if present in extraction_metadata
                if prov.extraction_metadata and "source_sha256" in prov.extraction_metadata:
                    claimed_hash = prov.extraction_metadata["source_sha256"]
                    if claimed_hash != source_rec.sha256:
                        atom_errors.append(
                            f"Provenance #{idx}: claimed source_sha256 does not match authoritative registered hash."
                        )

        # -------------------------------------------------------------
        # 4. LaTeX Syntax & Delimiter Linting
        # -------------------------------------------------------------
        latex_snippets: List[str] = []
        if atom.content:
            latex_snippets.append(atom.content)
        if atom.formula:
            latex_snippets.append(atom.formula.formula_latex)
        if atom.question:
            latex_snippets.append(atom.question.statement)
            for opt in atom.question.options:
                latex_snippets.append(opt.text)
        if atom.solved_example:
            latex_snippets.append(atom.solved_example.problem_statement)
            for sm in atom.solved_example.solution_steps:
                latex_snippets.append(sm.steps)

        for snip in latex_snippets:
            lint_errs = lint_latex_syntax(snip)
            if lint_errs:
                atom_errors.extend([f"LaTeX syntax error: {e}" for e in lint_errs])

        # -------------------------------------------------------------
        # 5. Low Confidence & Exception Routing
        # -------------------------------------------------------------
        if atom.confidence < low_confidence_threshold:
            prov = atom.provenance[0] if atom.provenance else None
            rev_id = generate_review_id("low_conf")
            rev_item = ReviewQueueItem(
                review_id=rev_id,
                issue_type=ReviewIssueType.LOW_CONFIDENCE,
                atom_id=atom.atom_id,
                source_id=prov.source_id if prov else "unknown",
                source_file=prov.file_name if prov else "unknown",
                source_page=prov.page_start if prov else None,
                flagged_text=atom.title,
                problem_description=f"Extraction confidence ({atom.confidence:.2f}) is below threshold ({low_confidence_threshold}).",
                suggested_action="Review visual page source and confirm notation/subscripts.",
                status=ReviewStatus.PENDING,
                created_at=datetime.now(timezone.utc),
            )
            result.review_items.append(rev_item)
            result.warnings.append(
                f"Atom '{atom.atom_id}' has low confidence ({atom.confidence:.2f}); queued for review."
            )

        if atom_errors:
            result.invalid_atoms.append((atom, atom_errors))
        else:
            result.valid_atoms.append(atom)

    return result
