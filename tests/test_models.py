import pytest
from pydantic import ValidationError

from jee_physics.models.atom import (
    FormulaPayload,
    KnowledgeAtom,
    MisconceptionPayload,
    QuestionOption,
    QuestionPayload,
    TaxonomyReference,
)
from jee_physics.models.enums import AtomStatus, AtomType, DifficultyLevel
from jee_physics.models.provenance import ProvenanceRecord


def make_valid_provenance() -> ProvenanceRecord:
    return ProvenanceRecord(
        source_id="src-hcv-vol1-test",
        file_name="concepts_of_physics_by_h.c._verma_volume_1.pdf",
        page_start=45,
        page_end=46,
        source_locator="Chapter 3, Q14",
    )


def test_valid_theory_atom():
    atom = KnowledgeAtom(
        atom_id="kinematics-theory-001",
        atom_type=AtomType.THEORY,
        title="Definition of Average Velocity",
        taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="1d-motion"),
        provenance=[make_valid_provenance()],
        confidence=0.98,
        verification_status=AtomStatus.STAGED,
        content_hash="a" * 64,
        content="Average velocity is defined as the total displacement divided by total time elapsed.",
    )
    assert atom.atom_id == "kinematics-theory-001"
    assert atom.content is not None


def test_valid_question_atom():
    atom = KnowledgeAtom(
        atom_id="kinematics-question-002",
        atom_type=AtomType.QUESTION,
        title="Relative velocity between two cars",
        taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="relative-motion"),
        provenance=[make_valid_provenance()],
        confidence=0.95,
        verification_status=AtomStatus.STAGED,
        content_hash="b" * 64,
        question=QuestionPayload(
            statement="Car A travels at 20 m/s and Car B at 30 m/s in the same direction. Find relative speed.",
            options=[
                QuestionOption(id="A", text="10 m/s"),
                QuestionOption(id="B", text="50 m/s"),
            ],
            answer="A",
            difficulty=DifficultyLevel.L2,
            concepts=["relative-velocity", "1d-motion"],
        ),
    )
    assert atom.question is not None
    assert atom.question.difficulty == DifficultyLevel.L2
    assert atom.question.answer == "A"


def test_question_atom_missing_question_payload_rejected():
    with pytest.raises(ValidationError) as exc:
        KnowledgeAtom(
            atom_id="kinematics-question-003",
            atom_type=AtomType.QUESTION,
            title="Question without payload",
            taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="relative-motion"),
            provenance=[make_valid_provenance()],
            confidence=0.95,
            content_hash="c" * 64,
            # Missing question=...
        )
    assert "question payload must be provided" in str(exc.value)


def test_formula_atom_missing_formula_payload_rejected():
    with pytest.raises(ValidationError) as exc:
        KnowledgeAtom(
            atom_id="kinematics-formula-004",
            atom_type=AtomType.FORMULA,
            title="Formula without payload",
            taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="equations-of-motion"),
            provenance=[make_valid_provenance()],
            confidence=0.95,
            content_hash="d" * 64,
        )
    assert "formula payload must be provided" in str(exc.value)


def test_empty_provenance_rejected():
    with pytest.raises(ValidationError) as exc:
        KnowledgeAtom(
            atom_id="kinematics-theory-005",
            atom_type=AtomType.THEORY,
            title="Orphan Atom",
            taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="1d-motion"),
            provenance=[],  # Empty provenance violates min_length=1
            confidence=0.95,
            content_hash="e" * 64,
            content="Some theory.",
        )
    assert "provenance" in str(exc.value)


def test_invalid_confidence_range_rejected():
    with pytest.raises(ValidationError):
        KnowledgeAtom(
            atom_id="kinematics-theory-006",
            atom_type=AtomType.THEORY,
            title="Confidence Error",
            taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="1d-motion"),
            provenance=[make_valid_provenance()],
            confidence=1.5,  # Out of range [0.0, 1.0]
            content_hash="f" * 64,
            content="Some theory.",
        )
