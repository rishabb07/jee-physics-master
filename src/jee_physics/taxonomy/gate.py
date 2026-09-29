import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference
from jee_physics.models.subject import SubjectAuditReport, SubjectClassificationRecord
from jee_physics.models.taxonomy import SubjectType, TaxonomyAssignment, TaxonomyAuditRecord, TaxonomyLevel, TaxonomyTree
from jee_physics.storage.io import safe_write_json
from jee_physics.validation.taxonomy_validator import load_canonical_taxonomy_tree, validate_subject_isolation


def stage_subject_classification_file(
    candidate_file: Path,
    staging_dir: Optional[Path] = None,
    review_queue_dir: Optional[Path] = None,
    registry_dir: Optional[Path] = None,
) -> Tuple[bool, Optional[Path], List[str]]:
    """Deterministic validation and staging gate for untrusted subject classification outputs."""
    errors: List[str] = []
    root = Path.cwd()
    if staging_dir is None:
        staging_dir = root / "build" / "staging" / "subject_classifications"
    if review_queue_dir is None:
        review_queue_dir = root / "review" / "queue" / "subject_exceptions"
    if registry_dir is None:
        registry_dir = root / "sources" / "registry"

    candidate_file = Path(candidate_file)
    if not candidate_file.exists():
        return False, None, [f"Candidate file '{candidate_file}' does not exist."]

    try:
        with open(candidate_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        return False, None, [f"Failed to parse JSON in '{candidate_file}': {e}"]

    # Parse single record or list
    records: List[SubjectClassificationRecord] = []
    if isinstance(raw_data, list):
        for idx, item in enumerate(raw_data):
            try:
                records.append(SubjectClassificationRecord.model_validate(item))
            except Exception as e:
                errors.append(f"Record {idx+1} failed schema validation: {e}")
    elif isinstance(raw_data, dict):
        try:
            records.append(SubjectClassificationRecord.model_validate(raw_data))
        except Exception as e:
            errors.append(f"SubjectClassificationRecord schema validation failed: {e}")
    else:
        return False, None, [f"Expected dict or list in '{candidate_file}', found {type(raw_data)}"]

    if errors:
        return False, None, errors

    # Validate each record against registry
    validated_records: List[SubjectClassificationRecord] = []
    for rec in records:
        reg_file = registry_dir / f"{rec.source_id}.json"
        if not reg_file.exists():
            errors.append(f"Source ID '{rec.source_id}' is not registered in sources/registry/.")
            continue

        try:
            reg_data = json.loads(reg_file.read_text(encoding="utf-8"))
            total_pages = reg_data.get("total_pages", 999999)
        except Exception:
            total_pages = 999999

        if rec.page_start < 1 or rec.page_end > total_pages or rec.page_start > rec.page_end:
            errors.append(
                f"Invalid page bounds [{rec.page_start}, {rec.page_end}] for source with {total_pages} pages."
            )
            continue

        # Handle exception path for UNCERTAIN or MIXED
        if rec.subject in (SubjectType.UNCERTAIN, SubjectType.MIXED):
            rec.status = "EXCEPTION_PENDING"
            review_queue_dir.mkdir(parents=True, exist_ok=True)
            ex_path = review_queue_dir / f"subject_ex_{rec.classification_id}.json"
            safe_write_json(ex_path, rec.model_dump(mode="json"))
            errors.append(
                f"Subject '{rec.subject.value}' on pages {rec.page_start}-{rec.page_end} routed to exception queue: {ex_path}"
            )
        else:
            rec.status = "VALIDATED"
            validated_records.append(rec)

    if errors and not validated_records:
        return False, None, errors

    staging_dir.mkdir(parents=True, exist_ok=True)
    if len(records) == 1:
        rec = records[0]
        staged_path = staging_dir / f"{rec.source_id}_pages_{rec.page_start:02d}_{rec.page_end:02d}.json"
        safe_write_json(staged_path, rec.model_dump(mode="json"))
    else:
        source_id = records[0].source_id
        staged_path = staging_dir / f"{source_id}_subject_audit.json"
        report = SubjectAuditReport(
            source_id=source_id,
            file_name=records[0].source_id,
            total_pages=max(r.page_end for r in records),
            records=records,
            physics_pages=[p for r in records if r.subject == SubjectType.PHYSICS for p in range(r.page_start, r.page_end + 1)],
            excluded_pages=[p for r in records if r.subject != SubjectType.PHYSICS for p in range(r.page_start, r.page_end + 1)],
            uncertain_pages=[p for r in records if r.subject in (SubjectType.UNCERTAIN, SubjectType.MIXED) for p in range(r.page_start, r.page_end + 1)],
        )
        safe_write_json(staged_path, report.model_dump(mode="json"))

    return True, staged_path, errors


def stage_taxonomy_assignment_file(
    candidate_file: Path,
    syllabus_path: Optional[Path] = None,
    staging_dir: Optional[Path] = None,
    review_queue_dir: Optional[Path] = None,
    kb_atoms_dir: Optional[Path] = None,
) -> Tuple[bool, Optional[Path], List[str]]:
    """Deterministic validation and staging gate for taxonomy classification proposals."""
    errors: List[str] = []
    root = Path.cwd()
    if syllabus_path is None:
        syllabus_path = root / "kb" / "taxonomy" / "syllabus.yaml"
    if staging_dir is None:
        staging_dir = root / "build" / "staging" / "taxonomy_assignments"
    if review_queue_dir is None:
        review_queue_dir = root / "review" / "queue" / "unmapped_atoms"
    if kb_atoms_dir is None:
        kb_atoms_dir = root / "kb" / "atoms"

    candidate_file = Path(candidate_file)
    if not candidate_file.exists():
        return False, None, [f"Candidate file '{candidate_file}' does not exist."]

    try:
        tree = load_canonical_taxonomy_tree(syllabus_path)
    except Exception as e:
        return False, None, [f"Failed to load canonical syllabus tree: {e}"]

    try:
        with open(candidate_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        return False, None, [f"Failed to parse JSON in '{candidate_file}': {e}"]

    assignments: List[TaxonomyAssignment] = []
    if isinstance(raw_data, list):
        for idx, item in enumerate(raw_data):
            try:
                assignments.append(TaxonomyAssignment.model_validate(item))
            except Exception as e:
                errors.append(f"Assignment {idx+1} failed schema validation: {e}")
    elif isinstance(raw_data, dict):
        try:
            assignments.append(TaxonomyAssignment.model_validate(raw_data))
        except Exception as e:
            errors.append(f"TaxonomyAssignment schema validation failed: {e}")
    else:
        return False, None, [f"Expected dict or list in '{candidate_file}', found {type(raw_data)}"]

    if errors:
        return False, None, errors

    validated_assignments: List[TaxonomyAssignment] = []

    for assign in assignments:
        # Check target atom exists
        atom_file = kb_atoms_dir / f"{assign.atom_id}.json"
        if not atom_file.exists():
            # Check staging atoms
            staged_matches = list((root / "build" / "staging" / "atoms").glob(f"*{assign.atom_id}*"))
            if not staged_matches:
                errors.append(f"Target atom '{assign.atom_id}' does not exist in kb/atoms/ or staging.")
                continue

        # Check if UNMAPPED or low confidence
        if assign.status == "UNMAPPED" or assign.confidence < 0.70:
            assign.status = "UNMAPPED"
            review_queue_dir.mkdir(parents=True, exist_ok=True)
            unmapped_path = review_queue_dir / f"unmapped_{assign.atom_id}.json"
            safe_write_json(unmapped_path, assign.model_dump(mode="json"))
            errors.append(
                f"Atom '{assign.atom_id}' marked UNMAPPED (confidence={assign.confidence:.2f}) -> routed to {unmapped_path}"
            )
            continue

        # Validate against canonical taxonomy tree
        canon_ch = tree.resolve_node_id(assign.chapter_id)
        if not canon_ch:
            errors.append(f"Chapter '{assign.chapter_id}' is not defined in the syllabus tree.")
            continue
        ch_node = tree.nodes.get(canon_ch)
        if not ch_node or ch_node.level != TaxonomyLevel.CHAPTER:
            errors.append(f"Node '{assign.chapter_id}' is not a CHAPTER in the syllabus tree.")
            continue

        canon_top = tree.resolve_node_id(assign.topic_id)
        if not canon_top:
            errors.append(f"Topic '{assign.topic_id}' is not defined in the syllabus tree.")
            continue
        top_node = tree.nodes.get(canon_top)
        if not top_node or top_node.level != TaxonomyLevel.TOPIC:
            errors.append(f"Node '{assign.topic_id}' is not a TOPIC in the syllabus tree.")
            continue
        if top_node.parent_id != canon_ch:
            errors.append(
                f"Topic '{assign.topic_id}' belongs to '{top_node.parent_id}', not chapter '{assign.chapter_id}'."
            )
            continue

        if assign.subtopic_id:
            canon_sub = tree.resolve_node_id(assign.subtopic_id)
            if not canon_sub:
                errors.append(f"Subtopic '{assign.subtopic_id}' is not defined in the syllabus tree.")
                continue
            sub_node = tree.nodes.get(canon_sub)
            if not sub_node or sub_node.level not in (TaxonomyLevel.SUBTOPIC, TaxonomyLevel.EXTENSION):
                errors.append(f"Node '{assign.subtopic_id}' is not a SUBTOPIC/EXTENSION in the syllabus tree.")
                continue
            if sub_node.parent_id != canon_top and sub_node.parent_id != canon_ch:
                errors.append(
                    f"Subtopic '{assign.subtopic_id}' does not belong under topic '{assign.topic_id}'."
                )
                continue

        # Normalize slugs to canonical IDs
        assign.chapter_id = canon_ch
        assign.topic_id = canon_top
        if assign.subtopic_id:
            assign.subtopic_id = tree.resolve_node_id(assign.subtopic_id)
        assign.status = "APPROVED"
        validated_assignments.append(assign)

    if errors and not validated_assignments:
        return False, None, errors

    staging_dir.mkdir(parents=True, exist_ok=True)
    out_path = staging_dir / f"staged_assignments_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    safe_write_json(out_path, [a.model_dump(mode="json") for a in validated_assignments])

    return True, out_path, errors


def apply_taxonomy_assignment_to_canonical_atom(
    atom_id: str,
    assignment: TaxonomyAssignment,
    kb_atoms_dir: Optional[Path] = None,
    journal_path: Optional[Path] = None,
    classifier_identity: str = "physics_taxonomy_classifier",
    classifier_conversation_id: Optional[str] = "53e98d36-5d48-4182-962c-377dc6893e41",
) -> KnowledgeAtom:
    """Updates only the taxonomy metadata of a canonical atom, strictly preserving all physics content,
    and records an immutable audit record in the persistent taxonomy journal.
    """
    root = Path.cwd()
    if kb_atoms_dir is None:
        kb_atoms_dir = root / "kb" / "atoms"
    if journal_path is None:
        journal_path = root / "kb" / "taxonomy" / "assignments_journal.jsonl"

    atom_path = kb_atoms_dir / f"{atom_id}.json"
    if not atom_path.exists():
        raise FileNotFoundError(f"Canonical atom file '{atom_path}' not found.")

    with open(atom_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    atom = KnowledgeAtom.model_validate(data)
    prev_tax = atom.taxonomy.model_dump(mode="json") if atom.taxonomy else None

    # Strictly preserve content, provenance, verified answer, verification status
    atom.taxonomy = TaxonomyReference(
        chapter_id=assignment.chapter_id,
        topic_id=assignment.topic_id,
        subtopic_id=assignment.subtopic_id,
    )
    atom.updated_at = datetime.now(timezone.utc)

    # Save back atomically
    safe_write_json(atom_path, atom.model_dump(mode="json"))

    # Record persistent audit trail
    audit_rec = TaxonomyAuditRecord(
        audit_id=f"tax-audit-{atom_id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        atom_id=atom_id,
        atom_version=atom.atom_version,
        content_hash=atom.content_hash,
        taxonomy_schema_version="1.0.0",
        chapter_id=assignment.chapter_id,
        topic_id=assignment.topic_id,
        subtopic_id=assignment.subtopic_id,
        previous_taxonomy=prev_tax,
        classifier_identity=classifier_identity,
        classifier_conversation_id=classifier_conversation_id,
        rationale=assignment.rationale,
        confidence=assignment.confidence,
        applied_at=datetime.now(timezone.utc),
        status="APPROVED",
    )

    journal_path.parent.mkdir(parents=True, exist_ok=True)
    with open(journal_path, "a", encoding="utf-8") as jf:
        jf.write(audit_rec.model_dump_json() + "\n")

    return atom


def validate_atom_against_subject_audit(
    atom: KnowledgeAtom,
    subject_audit: Union[Path, SubjectAuditReport],
) -> Tuple[bool, Optional[str]]:
    """Enforces strict subject-boundary isolation.
    
    Verifies that the atom's source pages were classified as PHYSICS (or allowed MIXED lines).
    If an atom's provenance references pages classified as CHEMISTRY, MATHEMATICS, NON_CONTENT,
    or UNCERTAIN without explicit clearance, it is strictly REJECTED regardless of any
    physics-like taxonomy labels attached to it.
    """
    if isinstance(subject_audit, Path):
        with open(subject_audit, "r", encoding="utf-8") as f:
            report = SubjectAuditReport.model_validate(json.load(f))
    elif isinstance(subject_audit, SubjectAuditReport):
        report = subject_audit
    else:
        raise TypeError(f"Expected Path or SubjectAuditReport, got {type(subject_audit)}")

    for prov in atom.provenance:
        if prov.source_id != report.source_id:
            continue
        page_range = range(prov.page_start, prov.page_end + 1)
        for page in page_range:
            if page in report.excluded_pages:
                return (
                    False,
                    f"Atom '{atom.atom_id}' originates from excluded non-physics page {page}. "
                    f"Subject isolation gate prevents promotion into Physics KB."
                )
            if page in report.uncertain_pages:
                # If transitional mixed page, requires explicit provenance validation
                pass

    return True, None
