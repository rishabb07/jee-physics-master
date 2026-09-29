import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from pydantic import ValidationError

from jee_physics.atomization.validator import validate_staged_atom_batch
from jee_physics.core.hasher import compute_file_sha256
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.manifest import FileChecksumRecord, JobManifest
from jee_physics.models.source import SourceRegistryRecord
from jee_physics.storage.io import read_json, safe_write_json, safe_write_jsonl


@dataclass
class AtomizationReport:
    source_id: str
    file_name: str
    batch_id: str
    pages_processed: List[int]
    total_atoms_staged: int
    atoms_by_type: Dict[str, int]
    confidence_distribution: Dict[str, int]
    questions_extracted: int
    figures_detected: int
    validation_failures: int
    review_items_queued: int
    warnings: List[str]
    pages_with_no_atoms: List[int]
    staged_atoms_file: str
    manifest_file: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def stage_atom_batch(
    atoms: List[KnowledgeAtom],
    source_id: str,
    pages_processed: List[int],
    project_root: Path,
    worker_id: str = "physics-atomizer-v1",
) -> AtomizationReport:
    """Safely stages a batch of extracted atoms into build/staging/atoms/.
    
    CRITICAL INVARIANT:
    - Writes ONLY to build/staging/ and review/queue/.
    - kb/atoms/ remains 100% untouched.
    """
    project_root = Path(project_root)
    staging_atoms_dir = project_root / "build" / "staging" / "atoms"
    staging_manifests_dir = project_root / "build" / "staging" / "manifests"
    reports_dir = project_root / "build" / "reports"
    review_queue_dir = project_root / "review" / "queue"
    registry_dir = project_root / "sources" / "registry"

    staging_atoms_dir.mkdir(parents=True, exist_ok=True)
    staging_manifests_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load source registry record
    reg_file = registry_dir / f"{source_id}.json"
    if not reg_file.exists():
        raise FileNotFoundError(f"Source '{source_id}' not found in registry ({registry_dir}).")

    reg_record = SourceRegistryRecord.model_validate(read_json(reg_file))
    batch_ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    batch_id = f"batch_{source_id}_{batch_ts}_{uuid.uuid4().hex[:4]}"

    # 2. Run deterministic validation gate with strict source_id enforcement
    val_result = validate_staged_atom_batch(
        atoms=atoms,
        registry_dir=registry_dir,
        expected_source_id=source_id,
    )

    valid_atoms = val_result.valid_atoms
    invalid_atoms = val_result.invalid_atoms
    review_items = val_result.review_items
    warnings = list(val_result.warnings)

    for item, errs in invalid_atoms:
        warnings.append(f"Rejected atom '{item.atom_id}': {'; '.join(errs)}")

    # 3. Write valid atoms to staging JSONL
    staged_atoms_path = staging_atoms_dir / f"{batch_id}.jsonl"
    safe_write_jsonl(staged_atoms_path, valid_atoms)

    # 4. Write review queue items
    for item in review_items:
        queue_sub = review_queue_dir / item.issue_type.value.lower()
        queue_sub.mkdir(parents=True, exist_ok=True)
        safe_write_json(queue_sub / f"{item.review_id}.json", item)

    # 5. Compute stats
    atoms_by_type: Dict[str, int] = {}
    confidence_dist: Dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    questions_count = 0
    figures_count = 0
    covered_pages: Set[int] = set()

    for a in valid_atoms:
        t = a.atom_type.value
        atoms_by_type[t] = atoms_by_type.get(t, 0) + 1

        if a.confidence >= 0.95:
            confidence_dist["HIGH"] += 1
        elif a.confidence >= 0.85:
            confidence_dist["MEDIUM"] += 1
        else:
            confidence_dist["LOW"] += 1

        if a.atom_type.value == "question":
            questions_count += 1
        if a.figure_refs:
            figures_count += len(a.figure_refs)

        for p in a.provenance:
            if p.page_start:
                covered_pages.add(p.page_start)

    pages_with_no_atoms = [p for p in pages_processed if p not in covered_pages]

    # 6. Generate batch manifest
    manifest_id = f"man-{batch_id}"
    staged_hash = compute_file_sha256(staged_atoms_path) if staged_atoms_path.exists() else "0" * 64
    staged_size = staged_atoms_path.stat().st_size if staged_atoms_path.exists() else 0

    if len(valid_atoms) == 0:
        manifest_status = "FAILED"
    elif len(invalid_atoms) == 0:
        manifest_status = "COMPLETED"
    else:
        manifest_status = "PARTIAL_SUCCESS"

    manifest = JobManifest(
        manifest_id=manifest_id,
        job_type="ATOMIZE",
        stage="EXTRACTION",
        input_files=[
            FileChecksumRecord(
                file_path=f"sources/raw/{reg_record.file_name}",
                sha256=reg_record.sha256,
                size_bytes=reg_record.file_size_bytes,
            )
        ],
        output_files=[
            FileChecksumRecord(
                file_path=str(staged_atoms_path.relative_to(project_root)).replace("\\", "/"),
                sha256=staged_hash,
                size_bytes=staged_size,
            )
        ],
        generated_atom_ids=[a.atom_id for a in valid_atoms],
        status=manifest_status,
        metadata={
            "source_id": source_id,
            "source_version": reg_record.source_version,
            "worker_id": worker_id,
            "pages_processed": pages_processed,
            "validation_failures": len(invalid_atoms),
            "review_items_queued": len(review_items),
        },
    )

    manifest_path = staging_manifests_dir / f"{batch_id}.manifest.json"
    safe_write_json(manifest_path, manifest)

    # 7. Generate atomization report
    report = AtomizationReport(
        source_id=source_id,
        file_name=reg_record.file_name,
        batch_id=batch_id,
        pages_processed=pages_processed,
        total_atoms_staged=len(valid_atoms),
        atoms_by_type=atoms_by_type,
        confidence_distribution=confidence_dist,
        questions_extracted=questions_count,
        figures_detected=figures_count,
        validation_failures=len(invalid_atoms),
        review_items_queued=len(review_items),
        warnings=warnings,
        pages_with_no_atoms=pages_with_no_atoms,
        staged_atoms_file=str(staged_atoms_path.relative_to(project_root)).replace("\\", "/"),
        manifest_file=str(manifest_path.relative_to(project_root)).replace("\\", "/"),
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    report_path = reports_dir / f"atomization_{source_id}_{batch_id}.json"
    safe_write_json(report_path, report.to_dict())

    return report


def stage_candidate_file(
    source_id: str,
    candidate_path: Path,
    project_root: Path,
    worker_id: str = "physics-atomizer",
) -> AtomizationReport:
    """Ingests, parses, validates, and stages an untrusted candidate JSONL file.
    
    This function forms the deterministic verification boundary between the
    Antigravity cognitive worker and the JEE Physics Knowledge System.
    """
    candidate_path = Path(candidate_path)
    if not candidate_path.exists():
        raise FileNotFoundError(f"Candidate file '{candidate_path}' not found.")

    registry_dir = Path(project_root) / "sources" / "registry"
    reg_file = registry_dir / f"{source_id}.json"
    if not reg_file.exists():
        raise FileNotFoundError(f"Source '{source_id}' not found in registry ({registry_dir}).")

    raw_lines = candidate_path.read_text(encoding="utf-8").splitlines()
    atoms: List[KnowledgeAtom] = []
    malformed_errors: List[str] = []

    for line_idx, line in enumerate(raw_lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            raw_dict = json.loads(stripped)
        except json.JSONDecodeError as err:
            raise ValueError(f"Malformed JSON at line {line_idx} in '{candidate_path}': {err}")

        try:
            atom = KnowledgeAtom.model_validate(raw_dict)
            atoms.append(atom)
        except ValidationError as val_err:
            malformed_errors.append(f"Line {line_idx}: {val_err}")

    if malformed_errors:
        raise ValueError(
            f"Schema validation rejected {len(malformed_errors)} candidate record(s) in '{candidate_path}':\n"
            + "\n".join(malformed_errors[:5])
        )

    # Determine pages covered
    pages_processed = sorted(
        list({p.page_start for a in atoms for p in a.provenance if p.page_start is not None})
    )

    return stage_atom_batch(
        atoms=atoms,
        source_id=source_id,
        pages_processed=pages_processed,
        project_root=project_root,
        worker_id=worker_id,
    )
