import tempfile
from pathlib import Path
import yaml

from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference
from jee_physics.models.enums import AtomType
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.validation.taxonomy_validator import validate_taxonomy_reference


def make_dummy_atom(chapter: str, topic: str, subtopic: str | None = None) -> KnowledgeAtom:
    return KnowledgeAtom(
        atom_id="test-atom-tax",
        atom_type=AtomType.THEORY,
        title="Test Taxonomy",
        taxonomy=TaxonomyReference(chapter_id=chapter, topic_id=topic, subtopic_id=subtopic),
        provenance=[
            ProvenanceRecord(source_id="src-1", file_name="test.pdf", page_start=1, page_end=1)
        ],
        confidence=1.0,
        content_hash="3" * 64,
        content="Test content.",
    )


def test_taxonomy_validation_against_tree():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".yaml", encoding="utf-8") as f:
        syllabus_data = {
            "chapters": {
                "kinematics": {
                    "title": "Kinematics",
                    "topics": {
                        "1d-motion": {
                            "title": "Motion in One Dimension",
                            "subtopics": ["constant-acceleration", "variable-acceleration"],
                        }
                    },
                }
            }
        }
        yaml.safe_dump(syllabus_data, f)
        tree_path = Path(f.name)

    try:
        # 1. Valid placement
        atom_valid = make_dummy_atom("kinematics", "1d-motion", "constant-acceleration")
        errs = validate_taxonomy_reference(atom_valid, syllabus_tree_path=tree_path)
        assert len(errs) == 0

        # 2. Invalid chapter
        atom_bad_chap = make_dummy_atom("quantum-mechanics", "1d-motion")
        errs = validate_taxonomy_reference(atom_bad_chap, syllabus_tree_path=tree_path)
        assert any("Chapter 'quantum-mechanics' is not defined" in e for e in errs)

        # 3. Invalid topic
        atom_bad_top = make_dummy_atom("kinematics", "photoelectric-effect")
        errs = validate_taxonomy_reference(atom_bad_top, syllabus_tree_path=tree_path)
        assert any("Topic 'photoelectric-effect' is not defined" in e for e in errs)

        # 4. Invalid subtopic
        atom_bad_sub = make_dummy_atom("kinematics", "1d-motion", "string-theory")
        errs = validate_taxonomy_reference(atom_bad_sub, syllabus_tree_path=tree_path)
        assert any("Subtopic 'string-theory' is not defined" in e for e in errs)
    finally:
        tree_path.unlink()
