import pytest
import yaml
from pathlib import Path
import tempfile

from jee_physics.models.enums import AtomType, AtomStatus
from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.models.taxonomy import (
    TaxonomyLevel,
    TaxonomyNode,
    TaxonomyTree,
    TaxonomyAssignment,
    SubjectType,
)
from jee_physics.models.subject import (
    SubjectClassificationRecord,
    SubjectAuditReport,
)
from jee_physics.taxonomy.gate import (
    stage_subject_classification_file,
    stage_taxonomy_assignment_file,
    apply_taxonomy_assignment_to_canonical_atom,
)


def test_authoritative_syllabus_tree_validity():
    """Verify that kb/taxonomy/syllabus.yaml is well-formed, acyclic, and strictly structured."""
    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    assert syllabus_path.exists(), "kb/taxonomy/syllabus.yaml must exist"

    with open(syllabus_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    tree = TaxonomyTree.model_validate(data)
    assert tree.root_id == "physics"
    root = tree.nodes[tree.root_id]
    assert root.level == TaxonomyLevel.SUBJECT
    assert root.subject == SubjectType.PHYSICS

    # Count chapters, topics, subtopics
    chapters = [n for n in tree.nodes.values() if n.level == TaxonomyLevel.CHAPTER]
    topics = [n for n in tree.nodes.values() if n.level == TaxonomyLevel.TOPIC]
    subtopics = [n for n in tree.nodes.values() if n.level in (TaxonomyLevel.SUBTOPIC, TaxonomyLevel.EXTENSION)]

    assert len(chapters) == 30, f"Expected exactly 30 chapters, found {len(chapters)}"
    assert len(topics) >= 70, f"Expected at least 70 topics, found {len(topics)}"
    assert len(subtopics) >= 300, f"Expected at least 300 subtopics, found {len(subtopics)}"

    # Check extension nodes
    extensions = [n for n in tree.nodes.values() if n.extension_olympiad]
    assert len(extensions) >= 3
    assert "advanced-rigid-body-dynamics" in [n.id for n in extensions]


def test_taxonomy_tree_validation_errors():
    """Test validation errors for duplicate IDs, cycles, missing parents, and level transition violations."""
    # 1. Duplicate alias / node ID collision
    with pytest.raises(ValueError, match="collides with existing node ID"):
        TaxonomyTree(
            schema_version="1.0.0",
            root_id="physics",
            nodes={
                "physics": TaxonomyNode(id="physics", name="Physics", level=TaxonomyLevel.SUBJECT, parent_id=None),
                "kinematics": TaxonomyNode(id="kinematics", name="Kinematics", level=TaxonomyLevel.CHAPTER, parent_id="physics", aliases=["physics"]),
            },
        )

    # 2. Missing parent
    with pytest.raises(ValueError, match="references non-existent parent"):
        TaxonomyTree(
            schema_version="1.0.0",
            root_id="physics",
            nodes={
                "physics": TaxonomyNode(id="physics", name="Physics", level=TaxonomyLevel.SUBJECT, parent_id=None),
                "kinematics": TaxonomyNode(id="kinematics", name="Kinematics", level=TaxonomyLevel.CHAPTER, parent_id="non-existent-parent"),
            },
        )

    # 3. Invalid level transition: SUBTOPIC directly under SUBJECT
    with pytest.raises(ValueError, match="Invalid parent-child level hierarchy"):
        TaxonomyTree(
            schema_version="1.0.0",
            root_id="physics",
            nodes={
                "physics": TaxonomyNode(id="physics", name="Physics", level=TaxonomyLevel.SUBJECT, parent_id=None),
                "sub": TaxonomyNode(id="sub", name="Subtopic", level=TaxonomyLevel.SUBTOPIC, parent_id="physics"),
            },
        )


def test_alias_resolution():
    """Verify alias lookup in TaxonomyTree."""
    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    with open(syllabus_path, "r", encoding="utf-8") as f:
        tree = TaxonomyTree.model_validate(yaml.safe_load(f))

    # Standard direct ID
    assert tree.resolve_node_id("rotational-motion") == "rotational-motion"
    # Alias resolution
    assert tree.resolve_node_id("rotation") == "rotational-motion"
    assert tree.resolve_node_id("center-of-mass") == "center-of-mass"
    # Non-existent
    assert tree.resolve_node_id("quantum-gravity-warp-drive") is None


def test_subject_classification_models():
    """Test SubjectClassificationRecord and SubjectAuditReport invariants."""
    rec1 = SubjectClassificationRecord(
        classification_id="sub-01",
        source_id="src-mock",
        page_start=1,
        page_end=6,
        subject=SubjectType.PHYSICS,
        confidence=1.0,
        reason="Physics section",
        detected_markers=["SECTION A", "PHYSICS"],
    )
    assert rec1.subject == SubjectType.PHYSICS

    rec2 = SubjectClassificationRecord(
        classification_id="sub-02",
        source_id="src-mock",
        page_start=8,
        page_end=10,
        subject=SubjectType.CHEMISTRY,
        confidence=0.99,
        reason="Chemistry questions",
        detected_markers=["CHEMISTRY"],
    )
    assert rec2.subject == SubjectType.CHEMISTRY

    report = SubjectAuditReport(
        audit_id="audit-mock",
        source_id="src-mock",
        file_name="jee_rank_booster-03_mock_paper.pdf",
        total_pages=10,
        records=[rec1, rec2],
        physics_pages=[1, 2, 3, 4, 5, 6],
        excluded_pages=[8, 9, 10],
        uncertain_pages=[],
        status="AUDITED",
    )
    assert len(report.physics_pages) == 6
    assert len(report.excluded_pages) == 3


def test_stage_subject_classification_file(tmp_path):
    """Test staging subject classification records via gate."""
    import json
    in_file = tmp_path / "subject_test.json"
    in_file.write_text(json.dumps([
        {
            "classification_id": "sub-test-01",
            "source_id": "src-jee-rank-booster-03-mock-256f42c6",
            "page_start": 1,
            "page_end": 5,
            "subject": "PHYSICS",
            "confidence": 0.98,
            "reason": "Clear physics section",
            "detected_markers": ["PHYSICS"],
            "status": "PROPOSED",
        },
        {
            "classification_id": "sub-test-02",
            "source_id": "src-jee-rank-booster-03-mock-256f42c6",
            "page_start": 6,
            "page_end": 10,
            "subject": "CHEMISTRY",
            "confidence": 0.99,
            "reason": "Clear chemistry section",
            "detected_markers": ["CHEMISTRY"],
            "status": "PROPOSED",
        }
    ]), encoding="utf-8")

    success, staged_file, errs = stage_subject_classification_file(in_file, staging_dir=tmp_path / "staged")
    assert success is True, f"Staging failed: {errs}"
    assert len(errs) == 0
    assert staged_file.exists()

    # Rejection of unregistered source
    bad_file = tmp_path / "bad_subject.json"
    bad_file.write_text(json.dumps([
        {
            "classification_id": "sub-test-03",
            "source_id": "src-unregistered-9999",
            "page_start": 1,
            "page_end": 5,
            "subject": "PHYSICS",
            "confidence": 0.98,
            "reason": "Unknown source",
            "status": "PROPOSED",
        }
    ]), encoding="utf-8")
    success_bad, _, errs_bad = stage_subject_classification_file(bad_file, staging_dir=tmp_path / "staged")
    assert success_bad is False
    assert any("not registered" in e for e in errs_bad)


def test_stage_taxonomy_assignment_file(tmp_path):
    """Test staging taxonomy assignments against authoritative syllabus tree."""
    import json
    syllabus_path = Path("kb/taxonomy/syllabus.yaml")

    # Find an existing canonical atom ID
    canonical_atoms = list(Path("kb/atoms").glob("*.json"))
    assert canonical_atoms, "Expected canonical atoms to exist"
    with open(canonical_atoms[0], "r", encoding="utf-8") as f:
        existing_atom_id = json.load(f)["atom_id"]

    in_file = tmp_path / "assign_test.json"
    # Valid assignment
    in_file.write_text(json.dumps([
        {
            "assignment_id": "assign-01",
            "atom_id": existing_atom_id,
            "chapter_id": "electrostatics",
            "topic_id": "coulombs-law-and-electric-field",
            "subtopic_id": "coulombs-law-vector-form",
            "confidence": 0.95,
            "rationale": "Direct Coulomb law application",
            "status": "PROPOSED",
        }
    ]), encoding="utf-8")

    success, staged_file, errs = stage_taxonomy_assignment_file(in_file, syllabus_path=syllabus_path, staging_dir=tmp_path / "staged")
    assert success is True, f"Failed staging valid assignment: {errs}"
    assert len(errs) == 0
    assert staged_file.exists()

    # Invalid node assignment
    bad_file = tmp_path / "bad_assign.json"
    bad_file.write_text(json.dumps([
        {
            "assignment_id": "assign-bad",
            "atom_id": existing_atom_id,
            "chapter_id": "fake-chapter",
            "topic_id": "coulombs-law-and-electric-field",
            "confidence": 0.95,
            "rationale": "Testing bad chapter",
            "status": "PROPOSED",
        }
    ]), encoding="utf-8")

    success_bad, _, errs_bad = stage_taxonomy_assignment_file(bad_file, syllabus_path=syllabus_path, staging_dir=tmp_path / "staged")
    assert success_bad is False
    assert any("not defined in the syllabus tree" in e for e in errs_bad)


def test_apply_taxonomy_assignment_preserves_content(tmp_path):
    """Verify that applying a taxonomy assignment strictly preserves physics content, questions, answers, and provenance."""
    import json
    canonical_atoms = list(Path("kb/atoms").glob("*.json"))
    assert canonical_atoms, "Expected canonical atoms to exist"
    with open(canonical_atoms[0], "r", encoding="utf-8") as f:
        atom = KnowledgeAtom.model_validate(json.load(f))

    # Save to a temporary test directory so we don't mutate real kb/atoms
    test_kb_dir = tmp_path / "atoms"
    test_kb_dir.mkdir(parents=True, exist_ok=True)
    with open(test_kb_dir / f"{atom.atom_id}.json", "w", encoding="utf-8") as f:
        json.dump(atom.model_dump(mode="json"), f)

    assignment = TaxonomyAssignment(
        assignment_id="tax-assign-01",
        atom_id=atom.atom_id,
        chapter_id="units-and-measurements",
        topic_id="units-and-dimensions",
        subtopic_id="si-units-and-derived-units",
        confidence=0.99,
        rationale="SI units test",
    )

    updated_atom = apply_taxonomy_assignment_to_canonical_atom(
        atom_id=atom.atom_id,
        assignment=assignment,
        kb_atoms_dir=test_kb_dir,
    )

    # Invariants check
    assert updated_atom.taxonomy.chapter_id == "units-and-measurements"
    assert updated_atom.taxonomy.topic_id == "units-and-dimensions"
    assert updated_atom.taxonomy.subtopic_id == "si-units-and-derived-units"

    # Physics content MUST be identical
    assert updated_atom.atom_id == atom.atom_id
    assert updated_atom.question.statement == atom.question.statement
    assert updated_atom.question.verified_answer == atom.question.verified_answer
    assert updated_atom.question.source_claimed_answer == atom.question.source_claimed_answer
    assert updated_atom.content_hash == atom.content_hash
    assert updated_atom.verification_status == atom.verification_status
    assert updated_atom.confidence == atom.confidence
    assert len(updated_atom.provenance) == len(atom.provenance)
    assert updated_atom.provenance[0].source_locator == atom.provenance[0].source_locator


def test_taxonomy_drift_protection(tmp_path):
    """Verify that changing taxonomy metadata does NOT invalidate verification records or alter physics truth."""
    import json
    from jee_physics.models.verification import VerificationRecord, VerificationVerdict

    canonical_atoms = list(Path("kb/atoms").glob("*.json"))
    assert canonical_atoms, "Expected canonical atoms"
    with open(canonical_atoms[0], "r", encoding="utf-8") as f:
        atom = KnowledgeAtom.model_validate(json.load(f))

    # Mock verification record linked to atom content_hash
    v_rec = VerificationRecord(
        verification_id="rec-test-drift-01",
        source_id=atom.provenance[0].source_id,
        atom_id=atom.atom_id,
        atom_version=atom.atom_version,
        content_hash=atom.content_hash,
        solver_run_ids=[],
        consensus_answer=atom.question.verified_answer,
        verdict=VerificationVerdict.VERIFIED,
        confidence=1.0,
    )

    # Temporary directory for safe mutation
    test_kb_dir = tmp_path / "atoms"
    test_kb_dir.mkdir(parents=True, exist_ok=True)
    with open(test_kb_dir / f"{atom.atom_id}.json", "w", encoding="utf-8") as f:
        json.dump(atom.model_dump(mode="json"), f)

    test_journal = tmp_path / "journal.jsonl"

    # Reclassify atom to another valid node
    new_assignment = TaxonomyAssignment(
        assignment_id="tax-reassign-01",
        atom_id=atom.atom_id,
        chapter_id="kinematics",
        topic_id="rectilinear-motion",
        subtopic_id="motion-graphs",
        confidence=0.98,
        rationale="Re-indexing under kinematics for curriculum laddering",
    )

    updated_atom = apply_taxonomy_assignment_to_canonical_atom(
        atom_id=atom.atom_id,
        assignment=new_assignment,
        kb_atoms_dir=test_kb_dir,
        journal_path=test_journal,
    )

    # 1. Verification record remains valid because content_hash is intact
    assert updated_atom.content_hash == v_rec.content_hash
    assert updated_atom.question.verified_answer == v_rec.consensus_answer
    assert updated_atom.atom_version == v_rec.atom_version

    # 2. Physics content & answers unchanged
    assert updated_atom.question.statement == atom.question.statement
    assert updated_atom.question.options == atom.question.options

    # 3. Journal records persistent audit entry
    assert test_journal.exists()
    lines = test_journal.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1
    audit_data = json.loads(lines[0])
    assert audit_data["atom_id"] == atom.atom_id
    assert audit_data["chapter_id"] == "kinematics"
    assert audit_data["status"] == "APPROVED"


def test_subject_isolation_blocks_chemistry_and_math():
    """Verify that non-physics questions cannot enter Physics KB even with valid physics taxonomy."""
    from jee_physics.models.atom import TaxonomyReference
    from jee_physics.taxonomy.gate import validate_atom_against_subject_audit

    # Create mock SubjectAuditReport where pages 8-10 are Chemistry
    audit_report = SubjectAuditReport(
        source_id="src-mock-01",
        file_name="mock.pdf",
        total_pages=14,
        physics_pages=[1, 2, 3, 4, 5, 6],
        excluded_pages=[8, 9, 10, 12, 13, 14],
        uncertain_pages=[7, 11],
    )

    # A Chemistry question from page 8 disguised with Physics taxonomy
    chem_atom = KnowledgeAtom(
        atom_id="chem-atom-p08",
        atom_type=AtomType.QUESTION,
        title="Ammonia Gas Reaction",
        taxonomy=TaxonomyReference(
            chapter_id="thermodynamics",
            topic_id="first-law-and-processes",
            subtopic_id="isothermal-process",
        ),
        provenance=[
            ProvenanceRecord(
                source_id="src-mock-01",
                file_name="mock.pdf",
                page_start=8,
                page_end=8,
                source_locator="Section A, Q35",
            )
        ],
        confidence=1.0,
        content_hash="chem1234chem1234",
        content="Mole calculation of ammonia gas.",
        question={
            "statement": "1 mole of ammonia gas at pressure P...",
            "question_type": "MULTIPLE_CHOICE_SINGLE",
            "options": [{"id": "A", "text": "2 atm"}],
            "verified_answer": "A",
            "difficulty": "L2",
        },
    )

    allowed, err = validate_atom_against_subject_audit(chem_atom, audit_report)
    assert allowed is False
    assert "excluded non-physics page 8" in err
    assert "Subject isolation gate prevents promotion into Physics KB" in err

    # A Physics question from page 3 passes cleanly
    phys_atom = chem_atom.model_copy(deep=True)
    phys_atom.provenance[0].page_start = 3
    phys_atom.provenance[0].page_end = 3
    allowed_phys, err_phys = validate_atom_against_subject_audit(phys_atom, audit_report)
    assert allowed_phys is True
    assert err_phys is None


def test_unknown_taxonomy_and_invalid_parentage_rejected(tmp_path):
    """Verify that non-existent chapters and mismatched topic-chapter parentages are rejected."""
    import json
    from jee_physics.validation.taxonomy_validator import validate_taxonomy_reference
    syllabus_path = Path("kb/taxonomy/syllabus.yaml")

    # 1. Non-existent chapter
    bad_chap_ref = TaxonomyReference(
        chapter_id="quantum-multiverse-mechanics",
        topic_id="rectilinear-motion",
    )
    errs = validate_taxonomy_reference(bad_chap_ref, syllabus_tree_path=syllabus_path)
    assert any("is not defined in the canonical syllabus tree" in e for e in errs)

    # 2. Valid topic under WRONG chapter
    mismatched_ref = TaxonomyReference(
        chapter_id="electrostatics",
        topic_id="angular-momentum",  # angular-momentum belongs to rotational-motion
    )
    errs = validate_taxonomy_reference(mismatched_ref, syllabus_tree_path=syllabus_path)
    assert any("is not defined under chapter 'electrostatics'" in e for e in errs)

    # 3. Valid chapter & topic, but invalid subtopic
    bad_sub_ref = TaxonomyReference(
        chapter_id="rotational-motion",
        topic_id="angular-momentum",
        subtopic_id="fake-subtopic-id-999",
    )
    errs = validate_taxonomy_reference(bad_sub_ref, syllabus_tree_path=syllabus_path)
    assert any("Subtopic 'fake-subtopic-id-999' is not defined" in e for e in errs)


def test_taxonomy_provenance_classes_and_syllabus_sources():
    """Verify that syllabus.yaml nodes carry explicit provenance classes and authority citations."""
    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    with open(syllabus_path, "r", encoding="utf-8") as f:
        tree = TaxonomyTree.model_validate(yaml.safe_load(f))

    from jee_physics.models.taxonomy import NodeProvenanceClass, SyllabusSourceAuthority

    # Verify chapters have OFFICIAL_EXAM_COVERAGE and JEE sources
    chapters = [n for n in tree.nodes.values() if n.level == TaxonomyLevel.CHAPTER]
    for ch in chapters:
        assert ch.provenance_class == NodeProvenanceClass.OFFICIAL_EXAM_COVERAGE
        auths = [s.authority for s in ch.syllabus_sources]
        assert SyllabusSourceAuthority.JEE_ADVANCED in auths
        assert SyllabusSourceAuthority.JEE_MAIN in auths
        editions = [s.edition for s in ch.syllabus_sources]
        assert "2026" in editions

    # Verify extension nodes have EXTENSION_OLYMPIAD and Olympiad sources
    ext_nodes = [n for n in tree.nodes.values() if n.extension_olympiad]
    assert len(ext_nodes) >= 3
    for ext in ext_nodes:
        assert ext.provenance_class == NodeProvenanceClass.EXTENSION_OLYMPIAD
        auths = [s.authority for s in ext.syllabus_sources]
        assert SyllabusSourceAuthority.OLYMPIAD in auths

    # Verify subtopics have PEDAGOGICAL_GROUPING
    subtopics = [n for n in tree.nodes.values() if n.level == TaxonomyLevel.SUBTOPIC]
    for sub in subtopics[:20]:
        assert sub.provenance_class == NodeProvenanceClass.PEDAGOGICAL_GROUPING
