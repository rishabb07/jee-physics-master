import json
from pathlib import Path
import pytest
import yaml

from jee_physics.corpus.evidence_retriever import EvidenceRetriever
from jee_physics.models.evidence import (
    EvidenceType,
    ExtractionQuality,
    PageEvidenceRecord,
    ProblemEvidenceRecord,
    SourceEvidenceRecord,
)
from jee_physics.models.generation_contract import (
    GenerationContractValidator,
    GroundedClaim,
    GroundingMode,
    PhysicsClaimType,
    SourceGroundedContentPayload,
)


@pytest.fixture
def evidence_retriever():
    return EvidenceRetriever(Path("sources/evidence"))


@pytest.fixture
def syllabus_node_ids():
    with open("kb/taxonomy/syllabus.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return set(data.get("nodes", {}).keys())


def test_adversarial_rejection_of_nonexistent_source_id(evidence_retriever):
    """Verifies that queries for a fabricated source ID return zero evidence."""
    fake_source_id = "src-fabricated-physics-textbook-xyz"
    # Provenance lookup must return None
    assert evidence_retriever.get_provenance(fake_source_id) is None

    # Check that no records in ledger claim this fake source
    matching = [r for r in evidence_retriever.records if r.source_id == fake_source_id]
    assert len(matching) == 0


def test_adversarial_rejection_of_nonexistent_evidence_id(evidence_retriever):
    """Verifies that GenerationContractValidator strictly rejects hallucinated evidence IDs."""
    fake_evidence_id = "evid-hallucinated-formula-999"

    payload = SourceGroundedContentPayload(
        payload_id="payload-adversarial-test-01",
        chapter_id="rotational-motion",
        topic_id="moment-of-inertia",
        claims=[
            GroundedClaim(
                claim_id="claim-01",
                claim_statement="The moment of inertia of a sphere is 2/5 M R^2.",
                claim_type=PhysicsClaimType.FORMULA_ASSERTION,
                grounding_mode=GroundingMode.SOURCE_EVIDENCE_BACKED,
                cited_evidence_ids=[fake_evidence_id],
            )
        ],
        cited_evidence_ids=[fake_evidence_id],
    )

    audit_result = GenerationContractValidator.audit_content_block(
        payload, evidence_retriever.valid_evidence_ids
    )

    assert audit_result["passed"] is False
    assert audit_result["hallucinated_citations_count"] >= 1
    assert fake_evidence_id in audit_result["hallucinated_citations"]


def test_adversarial_rejection_of_out_of_bounds_page():
    """Verifies that evidence records cannot have inverted or invalid page bounds."""
    with pytest.raises(ValueError, match="page_start .* cannot exceed page_end"):
        SourceEvidenceRecord(
            evidence_id="evid-invalid-bounds-01",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            page_start=150,
            page_end=140,  # Invalid: start > end
            section_or_chapter="Invalid Section",
            evidence_type=EvidenceType.DEFINITION,
            content_text="Invalid page boundary text.",
            taxonomy_node_ids=["kinematics"],
            provenance={"test": True},
        )


def test_adversarial_rejection_of_fake_taxonomy_nodes(syllabus_node_ids, evidence_retriever):
    """Verifies that every single registered evidence record points strictly to authentic syllabus nodes."""
    for record in evidence_retriever.records:
        for node_id in record.taxonomy_node_ids:
            assert node_id in syllabus_node_ids, f"Evidence record {record.evidence_id} cites non-existent taxonomy node '{node_id}'!"

    for formula in evidence_retriever.formulas:
        for node_id in formula.taxonomy_node_ids:
            assert node_id in syllabus_node_ids, f"Formula {formula.formula_id} cites non-existent taxonomy node '{node_id}'!"


def test_generation_contract_rejects_uncited_claims(evidence_retriever):
    """Verifies that a claim claiming SOURCE_EVIDENCE_BACKED without evidence citations is rejected."""
    with pytest.raises(ValueError, match="marked SOURCE_EVIDENCE_BACKED but provides zero cited_evidence_ids"):
        GroundedClaim(
            claim_id="claim-uncited-01",
            claim_statement="Uncited physics claim.",
            claim_type=PhysicsClaimType.CONCEPTUAL_PROPERTY,
            grounding_mode=GroundingMode.SOURCE_EVIDENCE_BACKED,
            cited_evidence_ids=[],
        )


def test_generation_contract_approves_valid_grounded_payload(evidence_retriever):
    """Verifies that legitimate claims citing verified evidence IDs pass contract validation."""
    valid_id = "evid-hcv1-p185-parallel-axis"
    assert valid_id in evidence_retriever.valid_evidence_ids

    payload = SourceGroundedContentPayload(
        payload_id="payload-valid-test-01",
        chapter_id="rotational-motion",
        topic_id="moment-of-inertia",
        claims=[
            GroundedClaim(
                claim_id="claim-valid-01",
                claim_statement="The moment of inertia about any parallel axis is I = I_cm + M d^2.",
                claim_type=PhysicsClaimType.FORMULA_ASSERTION,
                grounding_mode=GroundingMode.SOURCE_EVIDENCE_BACKED,
                cited_evidence_ids=[valid_id],
            )
        ],
        cited_evidence_ids=[valid_id],
    )

    audit_result = GenerationContractValidator.audit_content_block(
        payload, evidence_retriever.valid_evidence_ids
    )

    assert audit_result["passed"] is True
    assert audit_result["hallucinated_citations_count"] == 0
    assert len(audit_result["violations"]) == 0


def test_retriever_provenance_resolution(evidence_retriever):
    """Verifies that exact page and bibliographic provenance are resolvable for all items."""
    prov = evidence_retriever.get_provenance("form-evid-rot-moi-parallel")
    assert prov is not None
    assert prov["type"] == "FORMULA"
    assert prov["source_id"] == "src-concepts-of-physics-by-h-a489bb6e"
    assert 185 in prov["pages"]


def test_subject_boundary_mock_question_quarantine(evidence_retriever):
    """Verifies that all extracted mock questions are strictly Physics (Q1 to Q30) with zero chemistry/math leakage."""
    for mock_q in evidence_retriever.mock_questions:
        assert mock_q.subject == "PHYSICS"
        assert 1 <= mock_q.question_number <= 30
        assert mock_q.question_number not in range(31, 91)
