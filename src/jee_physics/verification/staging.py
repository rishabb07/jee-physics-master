import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone
import uuid

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import VerificationVerdict
from jee_physics.models.verification import (
    AdjudicationRecord,
    SolverRun,
)
from jee_physics.storage.io import read_jsonl, safe_write_json
from jee_physics.verification.sanitizer import create_blind_solver_package

ALLOWED_SOLVER_AGENTS = {
    "solver_a",
    "solver_b",
    "physics-verifier",
    "physics-verifier-a",
    "physics-verifier-b",
}


def find_staged_atom(
    atom_id: str,
    staging_dir: Path = Path("build/staging/atoms"),
) -> Optional[KnowledgeAtom]:
    """Finds a KnowledgeAtom by atom_id across all staging batch files."""
    staging_dir = Path(staging_dir)
    if not staging_dir.exists():
        return None

    for batch_file in staging_dir.glob("*.jsonl"):
        try:
            for line in read_jsonl(batch_file):
                if line.get("atom_id") == atom_id:
                    return KnowledgeAtom.model_validate(line)
        except Exception:
            continue
    return None


def stage_solver_run_file(
    input_file: Path,
    staging_dir: Path = Path("build/staging/atoms"),
    solver_runs_dir: Path = Path("verification/solver_runs"),
    manifests_dir: Path = Path("verification/manifests"),
) -> Tuple[bool, Optional[Path], Optional[Path], List[str]]:
    """Deterministically validates an untrusted solver JSON and stages it into verification/solver_runs/.
    
    Invariants:
    1. Parse and validate against SolverRun Pydantic model (rejecting prohibited fields).
    2. Target atom_id must exist in build/staging/atoms/.
    3. atom_version must match the staged atom.
    4. content_hash must match the staged atom.
    5. solver_run_id must be unique across verification/solver_runs/.
    6. solver_agent_name must be an authorized solver agent.
    7. blind_package_hash must match the actual package hash if provided.
    8. Write strictly to verification/solver_runs/{solver_run_id}.json.
    9. Write deterministic manifest to verification/manifests/stage_run_{solver_run_id}.json.
    """
    input_path = Path(input_file)
    errors: List[str] = []

    if not input_path.exists():
        return False, None, None, [f"Solver result file not found: {input_path}"]

    try:
        raw_data = json.loads(input_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, None, None, [f"Invalid JSON in solver result file '{input_path}': {e}"]

    # Validate against Pydantic model
    try:
        solver_run = SolverRun.model_validate(raw_data)
    except Exception as e:
        return False, None, None, [f"SolverRun schema validation failed: {e}"]

    # 1. Check target atom existence in staging
    staged_atom = find_staged_atom(solver_run.atom_id, staging_dir=staging_dir)
    if staged_atom is None:
        errors.append(f"Target atom '{solver_run.atom_id}' not found in staged batches at '{staging_dir}'.")
        return False, None, None, errors

    # 2. Check atom_version
    if solver_run.atom_version != staged_atom.atom_version:
        errors.append(
            f"atom_version mismatch: staged atom is v{staged_atom.atom_version}, "
            f"solver claimed v{solver_run.atom_version}."
        )

    # 3. Check content_hash
    if solver_run.content_hash and solver_run.content_hash != staged_atom.content_hash:
        errors.append(
            f"content_hash mismatch: staged atom hash is '{staged_atom.content_hash}', "
            f"solver provided '{solver_run.content_hash}'."
        )

    # 4. Check solver_run_id uniqueness
    solver_runs_dir = Path(solver_runs_dir)
    dest_path = solver_runs_dir / f"{solver_run.solver_run_id}.json"
    if dest_path.exists():
        errors.append(
            f"Duplicate solver_run_id '{solver_run.solver_run_id}': run file already exists at '{dest_path}'."
        )

    # 5. Check solver_agent_name
    agent_name = solver_run.solver_agent_name or solver_run.solver_id
    if agent_name not in ALLOWED_SOLVER_AGENTS and not agent_name.startswith(("solver_", "physics-verifier")):
        errors.append(
            f"Unauthorized solver_agent_name '{agent_name}'. Must be one of {sorted(ALLOWED_SOLVER_AGENTS)} "
            f"or prefixed with 'solver_' / 'physics-verifier'."
        )

    # 6. Check blind_package_hash if provided
    if solver_run.blind_package_hash:
        expected_pkg = create_blind_solver_package(staged_atom)
        if expected_pkg.blind_package_hash and solver_run.blind_package_hash != expected_pkg.blind_package_hash:
            errors.append(
                f"blind_package_hash mismatch: expected '{expected_pkg.blind_package_hash}', "
                f"got '{solver_run.blind_package_hash}'."
            )

    if errors:
        return False, None, None, errors

    # Ensure staged atom content_hash and version are populated if omitted by solver
    staged_payload = solver_run.model_copy()
    if not staged_payload.content_hash:
        staged_payload.content_hash = staged_atom.content_hash

    # Write validated SolverRun to verification/solver_runs/
    solver_runs_dir.mkdir(parents=True, exist_ok=True)
    safe_write_json(dest_path, staged_payload.model_dump(mode="json"))

    # Write manifest audit trail
    manifests_dir = Path(manifests_dir)
    manifests_dir.mkdir(parents=True, exist_ok=True)
    manifest_id = f"stage_run_{solver_run.solver_run_id}"
    manifest_path = manifests_dir / f"{manifest_id}.json"

    manifest_data = {
        "manifest_id": manifest_id,
        "solver_run_id": solver_run.solver_run_id,
        "solver_agent_name": agent_name,
        "atom_id": solver_run.atom_id,
        "atom_version": solver_run.atom_version,
        "content_hash": staged_payload.content_hash,
        "input_source_file": str(input_path),
        "staged_destination_file": str(dest_path),
        "independent_answer": solver_run.independent_answer,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "STAGED",
    }
    safe_write_json(manifest_path, manifest_data)

    return True, dest_path, manifest_path, []


def stage_adjudication_file(
    input_file: Path,
    staging_dir: Path = Path("build/staging/atoms"),
    adjudication_dir: Path = Path("verification/adjudications"),
    manifests_dir: Path = Path("verification/manifests"),
) -> Tuple[bool, Optional[Path], Optional[Path], List[str]]:
    """Deterministically validates an untrusted adjudication JSON and stages it into verification/adjudications/.
    
    Invariants:
    1. Parse and validate against AdjudicationRecord Pydantic model.
    2. Target atom_id must exist in build/staging/atoms/.
    3. atom_version must match the staged atom.
    4. content_hash must match the staged atom if provided.
    5. solver_analyses must evaluate at least two distinct solver runs.
    6. verdict must be an authorized verification verdict.
    7. Write validated record and audit manifest.
    """
    input_path = Path(input_file)
    errors: List[str] = []

    if not input_path.exists():
        return False, None, None, [f"Adjudication result file not found: {input_path}"]

    try:
        raw_data = json.loads(input_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, None, None, [f"Invalid JSON in adjudication file '{input_path}': {e}"]

    try:
        adj_record = AdjudicationRecord.model_validate(raw_data)
    except Exception as e:
        return False, None, None, [f"AdjudicationRecord schema validation failed: {e}"]

    # 1. Target atom existence
    staged_atom = find_staged_atom(adj_record.atom_id, staging_dir=staging_dir)
    if staged_atom is None:
        errors.append(f"Target atom '{adj_record.atom_id}' not found in staged batches at '{staging_dir}'.")
        return False, None, None, errors

    # 2. atom_version check
    if adj_record.atom_version != staged_atom.atom_version:
        errors.append(
            f"atom_version mismatch: staged atom is v{staged_atom.atom_version}, "
            f"adjudication claimed v{adj_record.atom_version}."
        )

    # 3. content_hash check
    if adj_record.content_hash and adj_record.content_hash != staged_atom.content_hash:
        errors.append(
            f"content_hash mismatch: staged atom hash is '{staged_atom.content_hash}', "
            f"adjudication provided '{adj_record.content_hash}'."
        )

    # 4. Solvers checked
    if len(adj_record.solver_analyses) < 2:
        errors.append(
            f"Adjudication must evaluate at least 2 solver runs, got {len(adj_record.solver_analyses)}."
        )

    # 5. Verdict validity
    valid_verdicts = {v.value for v in VerificationVerdict}
    if adj_record.verdict.value not in valid_verdicts:
        errors.append(f"Invalid verdict '{adj_record.verdict.value}'.")

    if errors:
        return False, None, None, errors

    adjudication_dir = Path(adjudication_dir)
    adjudication_dir.mkdir(parents=True, exist_ok=True)
    dest_path = adjudication_dir / f"{adj_record.adjudication_id}.json"

    # Save adjudication record
    safe_write_json(dest_path, adj_record.model_dump(mode="json"))

    # Save manifest
    manifests_dir = Path(manifests_dir)
    manifests_dir.mkdir(parents=True, exist_ok=True)
    manifest_id = f"stage_adj_{adj_record.adjudication_id}"
    manifest_path = manifests_dir / f"{manifest_id}.json"

    manifest_data = {
        "manifest_id": manifest_id,
        "adjudication_id": adj_record.adjudication_id,
        "atom_id": adj_record.atom_id,
        "verdict": adj_record.verdict.value,
        "adjudicated_answer": adj_record.adjudicated_answer,
        "input_source_file": str(input_path),
        "staged_destination_file": str(dest_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "STAGED",
    }
    safe_write_json(manifest_path, manifest_data)

    return True, dest_path, manifest_path, []
