from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional, Tuple
import uuid

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import VerificationVerdict
from jee_physics.models.verification import (
    AdjudicationRecord,
    SolverRun,
    VerificationRecord,
)
from jee_physics.storage.io import safe_write_json
from jee_physics.verification.comparator import compare_solver_runs


def save_solver_run(run: SolverRun, runs_dir: Path) -> Path:
    """Persists an individual SolverRun record to disk."""
    runs_dir = Path(runs_dir)
    runs_dir.mkdir(parents=True, exist_ok=True)
    out_path = runs_dir / f"{run.solver_run_id}.json"
    safe_write_json(out_path, run.model_dump(mode="json"))
    return out_path


def save_adjudication_record(record: AdjudicationRecord, adj_dir: Path) -> Path:
    """Persists an AdjudicationRecord to disk."""
    adj_dir = Path(adj_dir)
    adj_dir.mkdir(parents=True, exist_ok=True)
    out_path = adj_dir / f"{record.adjudication_id}.json"
    safe_write_json(out_path, record.model_dump(mode="json"))
    return out_path


def save_verification_record(record: VerificationRecord, records_dir: Path) -> Path:
    """Persists a canonical VerificationRecord to disk."""
    records_dir = Path(records_dir)
    records_dir.mkdir(parents=True, exist_ok=True)
    out_path = records_dir / f"{record.verification_id}.json"
    safe_write_json(out_path, record.model_dump(mode="json"))
    return out_path


def execute_verification_protocol(
    atom: KnowledgeAtom,
    solver_runs: List[SolverRun],
    adjudicator_fn: Optional[Callable[[KnowledgeAtom, List[SolverRun], Optional[str]], AdjudicationRecord]] = None,
    verification_base_dir: Path = Path("verification"),
) -> Tuple[VerificationRecord, Optional[AdjudicationRecord]]:
    """Runs the deterministic Phase 4 verification and reconciliation protocol on an atom.
    
    Workflow:
    1. Extract source claim (from question payload).
    2. Check solver runs (at least 2 required for independent consensus).
    3. Compare Solver A vs Solver B vs Source Claim.
    4. If disagreement or source contradiction occurs:
       - If adjudicator_fn provided, execute adjudication.
       - Otherwise record as UNRESOLVED / AMBIGUOUS / SOURCE_ERROR per comparator.
    5. Construct VerificationRecord.
    6. Persist solver runs, adjudication records, and verification record to disk.
    """
    if len(solver_runs) < 2:
        raise ValueError(
            f"Verification protocol requires at least 2 independent solver runs. "
            f"Found {len(solver_runs)} for atom '{atom.atom_id}'."
        )

    solver_a = solver_runs[0]
    solver_b = solver_runs[1]

    source_claim = atom.question.source_claimed_answer if atom.question else None
    source_solution = atom.question.source_solution if atom.question else None
    source_id = atom.provenance[0].source_id if atom.provenance else "unknown"

    comparison = compare_solver_runs(
        source_claimed_answer=source_claim,
        solver_a_answer=solver_a.independent_answer,
        solver_b_answer=solver_b.independent_answer,
    )

    adjudication_record: Optional[AdjudicationRecord] = None

    if comparison.requires_adjudication and adjudicator_fn:
        # Run adjudication
        adjudication_record = adjudicator_fn(atom, solver_runs, source_claim)
        final_verdict = adjudication_record.verdict
        final_answer = adjudication_record.adjudicated_answer
        final_confidence = adjudication_record.confidence
        discrepancy_class = comparison.discrepancy_classification
    elif comparison.requires_adjudication and not adjudicator_fn:
        # No adjudicator provided; retain preliminary verdict
        final_verdict = comparison.preliminary_verdict
        final_answer = comparison.preliminary_consensus
        final_confidence = 0.80
        discrepancy_class = comparison.discrepancy_classification
    else:
        # Solvers agreed and matched source (or source answer was absent)
        final_verdict = comparison.preliminary_verdict
        final_answer = comparison.preliminary_consensus
        final_confidence = 0.99
        discrepancy_class = comparison.discrepancy_classification

    # Build answers and solutions maps
    answers_map = {run.solver_id: run.independent_answer for run in solver_runs}
    solutions_map = {
        run.solver_id: "\n".join(run.reasoning_steps[:3]) if run.reasoning_steps else "No derivation logged"
        for run in solver_runs
    }

    verification_id = f"verif-{atom.atom_id}-{uuid.uuid4().hex[:6]}"
    v_record = VerificationRecord(
        verification_id=verification_id,
        atom_id=atom.atom_id,
        source_id=source_id,
        atom_version=atom.atom_version,
        content_hash=atom.content_hash,
        verification_protocol_version="1.0.0",
        solver_run_ids=[run.solver_run_id for run in solver_runs],
        source_claimed_answer=source_claim,
        source_solution=source_solution,
        independent_answers=answers_map,
        independent_solutions=solutions_map,
        consensus_answer=final_answer,
        verdict=final_verdict,
        confidence=final_confidence,
        discrepancy_classification=discrepancy_class,
        adjudication_result=adjudication_record,
        created_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
    )

    # Persist all verification artifacts
    runs_dir = verification_base_dir / "solver_runs"
    records_dir = verification_base_dir / "records"
    adj_dir = verification_base_dir / "adjudications"

    for run in solver_runs:
        save_solver_run(run, runs_dir)

    if adjudication_record:
        save_adjudication_record(adjudication_record, adj_dir)

    save_verification_record(v_record, records_dir)

    return v_record, adjudication_record
