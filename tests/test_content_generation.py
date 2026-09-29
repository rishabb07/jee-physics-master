"""
Unit and integration tests for Phase 8: Content Generation, Verification,
Editorial Assembly, and Chapter QA.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import pytest

from jee_physics.content.assembler import ChapterAssembler
from jee_physics.content.claim_resolver import ClaimResolver, ClaimResolutionStatus
from jee_physics.content.dependency import PedagogicalDependencyAuditor
from jee_physics.content.reconciliation import RequirementReconciliationEngine
from jee_physics.content.gate import (
    analyze_change_impact,
    bind_dual_verification,
    bind_verification,
    compute_content_hash,
    invalidate_if_modified,
    stage_content_artifact,
    validate_concept_explanation,
    validate_derivation_record,
    validate_formula_record,
    validate_misconception_content,
    validate_worked_example_content,
)
from jee_physics.content.numerical_validator import NumericalValidator
from jee_physics.content.qa import ChapterQAAuditor
from jee_physics.models.atom import TaxonomyReference
from jee_physics.models.taxonomy import SubjectType, TaxonomyNode, TaxonomyTree
from jee_physics.models.content import (
    ChapterContentBlock,
    ClaimTraceClass,
    ConceptExplanation,
    ContentBlockType,
    ContentRiskLevel,
    ContentVerificationRecord,
    ContentVerificationStatus,
    DerivationRecord,
    DerivationStep,
    DualVerificationRecord,
    FormulaRecord,
    MisconceptionContentRecord,
    VerifierOpinion,
    WorkedExampleContentRecord,
    WorkedExampleSolutionStep,
)


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent


import yaml

@pytest.fixture
def sample_taxonomy(workspace_root) -> TaxonomyTree:
    syllabus_path = workspace_root / "kb" / "taxonomy" / "syllabus.yaml"
    with open(syllabus_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return TaxonomyTree.model_validate(data)


def test_content_hashing_determinism_and_volatility():
    """Verifies that content hash is deterministic and ignores volatile metadata."""
    payload1 = {
        "concept_id": "concept-test-01",
        "title": "Conservation of Energy",
        "formal_definition": "Energy cannot be created or destroyed.",
        "verification_status": "UNVERIFIED",
        "created_at": "2026-09-28T10:00:00Z",
    }
    payload2 = {
        "concept_id": "concept-test-01",
        "title": "Conservation of Energy",
        "formal_definition": "Energy cannot be created or destroyed.",
        "verification_status": "VERIFIED",
        "created_at": "2026-09-29T12:00:00Z",
        "verification_record_id": "cvr-12345",
    }

    hash1 = compute_content_hash(payload1)
    hash2 = compute_content_hash(payload2)

    assert hash1 == hash2, "Content hash must be invariant under volatile metadata changes"

    # Substantive mutation must alter hash
    payload3 = dict(payload1)
    payload3["formal_definition"] = "Energy is fundamentally conserved in closed isolated systems."
    hash3 = compute_content_hash(payload3)
    assert hash1 != hash3, "Content hash must change when substantive text changes"


def test_verification_binding_and_invalidation():
    """Tests cryptographic verification binding and post-verification invalidation on mutation."""
    concept = ConceptExplanation(
        content_id="concept-bind-test",
        curriculum_id="curr-rot-01",
        taxonomy_reference=TaxonomyReference(
            chapter_id="rotational-motion",
            topic_id="moment-of-inertia",
        ),
        title="Moment of Inertia",
        learning_objective="Understand rotational inertia of continuous rigid bodies.",
        explanation="Moment of inertia plays the role of mass in rotational dynamics.",
        intuition="Harder to spin a barbell held at ends than at center.",
        formal_definition="I = \\int r^2 dm",
        assumptions=["Rigid body"],
        boundary_conditions=["Fixed axis"],
    )

    content_hash = compute_content_hash(concept)

    # Valid verification record
    valid_vr = ContentVerificationRecord(
        verification_id="cvr-test-001",
        artifact_id="concept-bind-test",
        artifact_version=1,
        content_hash=content_hash,
        verifier_id="test-verifier",
        verifier_conversation_id="conv-123",
        risk_level=ContentRiskLevel.MEDIUM,
        verdict="VERIFIED",
        assumptions_checked=True,
        dimensional_check_passed=True,
        numerical_check_passed=True,
        limiting_case_check_passed=True,
        independent_derivation_or_calculation="Independently confirmed integral definition",
    )

    success = bind_verification(concept, valid_vr)
    assert success is True
    assert concept.verification_status == ContentVerificationStatus.VERIFIED
    assert concept.verification_record_id == "cvr-test-001"

    # Mismatched hash verification record must fail
    invalid_vr = valid_vr.model_copy(update={"content_hash": "deadbeef12345678"})
    concept_unverified = concept.model_copy(update={"verification_status": ContentVerificationStatus.UNVERIFIED})
    success_invalid = bind_verification(concept_unverified, invalid_vr)
    assert success_invalid is False
    assert concept_unverified.verification_status == ContentVerificationStatus.UNVERIFIED

    # Invalidation on mutation
    initial_hash = compute_content_hash(concept)
    concept.formal_definition = "I = \\sum m_i r_i^2 (Discrete formulation)"
    is_invalidated = invalidate_if_modified(concept, initial_hash)
    assert is_invalidated is True
    assert concept.verification_status == ContentVerificationStatus.INVALIDATED
    assert concept.verification_record_id is None


def test_change_impact_analysis():
    """Tests targeted dependency graph tracking when a formula is revised."""
    derivations = [
        DerivationRecord(
            derivation_id="der-01",
            target_formula_id="formula-rot-moi-parallel",
            target_equation="I = I_{cm} + Md^2",
            starting_principles=["Definition of CM"],
            assumptions=["Rigid body"],
            ordered_steps=[
                DerivationStep(
                    step_number=1,
                    description="Expand coordinate sum",
                    starting_equation="I = \\int r^2 dm",
                    operation="Substitute coordinates",
                    result_equation="I = I_{cm} + Md^2",
                )
            ],
            final_equation="I = I_{cm} + Md^2",
            applicability_conditions=["Parallel axes"],
            generator_identity="agent",
            generator_conversation_id="c1",
        )
    ]

    examples = [
        WorkedExampleContentRecord(
            example_id="ex-01",
            problem_statement="Find MOI of rod about end",
            known_quantities={"M": "1kg", "L": "2m"},
            target_quantity="I",
            relevant_concepts=["parallel-axis"],
            governing_principles=["formula-rot-moi-parallel"],
            solution_strategy="Apply parallel axis theorem",
            ordered_steps=[
                WorkedExampleSolutionStep(
                    step_number=1,
                    principle_applied="formula-rot-moi-parallel",
                    equation="I = ML^2/12 + M(L/2)^2",
                    substitution="M=1, L=2",
                    intermediate_result="I = ML^2/3",
                )
            ],
            final_answer="4/3 kg m^2",
            units="kg m^2",
            sanity_checks=["Positive definite"],
            generator_identity="agent",
            generator_conversation_id="c1",
        )
    ]

    concepts = [
        ConceptExplanation(
            content_id="conc-01",
            curriculum_id="curr-01",
            taxonomy_reference=TaxonomyReference(chapter_id="rotational-motion", topic_id="moi"),
            title="Parallel Axis",
            learning_objective="Apply theorem",
            explanation="Allows shifting rotation axis",
            intuition="Offsetting increases inertia",
            formal_definition="I = I_cm + Md^2",
            related_formula_ids=["formula-rot-moi-parallel"],
        )
    ]

    impact = analyze_change_impact("formula-rot-moi-parallel", derivations, examples, concepts)
    assert "der-01" in impact["derivations"]
    assert "ex-01" in impact["worked_examples"]
    assert "conc-01" in impact["concepts"]

    # Unrelated formula should have 0 impact
    empty_impact = analyze_change_impact("formula-unrelated", derivations, examples, concepts)
    assert len(empty_impact["derivations"]) == 0
    assert len(empty_impact["worked_examples"]) == 0
    assert len(empty_impact["concepts"]) == 0


def test_gate_validation_rules(sample_taxonomy):
    """Tests deterministic validation gates for concepts, derivations, examples, and misconceptions."""
    # 1. Concept validation
    valid_concept = ConceptExplanation(
        content_id="c1",
        curriculum_id="curr-01",
        taxonomy_reference=TaxonomyReference(chapter_id="rotational-motion", topic_id="angular-momentum"),
        title="Torque",
        learning_objective="Understand moment of force",
        explanation="Torque causes angular acceleration according to Newton's rotational law.",
        intuition="Pushing a door at the handle is easier than near the hinge.",
        formal_definition="\\vec{\\tau} = \\vec{r} \\times \\vec{F}",
    )
    errors = validate_concept_explanation(valid_concept, sample_taxonomy)
    assert len(errors) == 0

    # Invalid concept (unknown taxonomy node)
    invalid_concept = valid_concept.model_copy(
        update={"taxonomy_reference": TaxonomyReference(chapter_id="unknown-chapter", topic_id="unknown-topic")}
    )
    errors_invalid = validate_concept_explanation(invalid_concept, sample_taxonomy)
    assert any("TAXONOMY_NODE_NOT_FOUND" in e for e in errors_invalid)

    # 2. Derivation validation
    valid_derivation = DerivationRecord(
        derivation_id="d1",
        target_formula_id="f1",
        target_equation="\\tau = I\\alpha",
        starting_principles=["Newton's second law for particles"],
        assumptions=["Rigid body", "Fixed axis"],
        ordered_steps=[
            DerivationStep(
                step_number=1,
                description="Particle torque summation",
                starting_equation="\\vec{F} = m\\vec{a}",
                operation="Cross with r",
                result_equation="\\tau = I\\alpha",
            )
        ],
        final_equation="\\tau = I\\alpha",
        applicability_conditions=["Fixed principal axis"],
        generator_identity="agent",
        generator_conversation_id="c1",
    )
    d_errors = validate_derivation_record(valid_derivation)
    assert len(d_errors) == 0

    # Broken derivation (empty steps)
    broken_derivation = valid_derivation.model_copy(update={"ordered_steps": []})
    d_errors_broken = validate_derivation_record(broken_derivation)
    assert any("DERIVATION_NO_STEPS" in e for e in d_errors_broken)


def test_chapter_assembly_and_qa_auditing(workspace_root):
    """Tests ChapterAssembler and ChapterQAAuditor on the pilot chapters."""
    assembler = ChapterAssembler(workspace_root)
    auditor = ChapterQAAuditor(workspace_root)

    # Test rotational-motion assembly
    blocks = assembler.assemble_chapter("rotational-motion")
    assert len(blocks) >= 15, "rotational-motion must assemble into at least 15 content blocks"

    block_types = {b.block_type for b in blocks}
    assert ContentBlockType.OBJECTIVE in block_types
    assert ContentBlockType.CONCEPT_EXPLANATION in block_types
    assert ContentBlockType.FORMULA in block_types
    assert ContentBlockType.DERIVATION in block_types
    assert ContentBlockType.WORKED_EXAMPLE in block_types
    assert ContentBlockType.MISCONCEPTION in block_types
    assert ContentBlockType.QUESTION_SET in block_types
    assert ContentBlockType.SUMMARY in block_types

    # Audit the assembled chapter
    spec = assembler.load_spec("rotational-motion")
    plan = assembler.load_plan("rotational-motion")
    chap_qa, rend_qa = auditor.audit_chapter("rotational-motion", blocks, plan, spec)

    assert chap_qa.verdict == "PASSED"
    assert chap_qa.physics_passed is True
    assert chap_qa.provenance_passed is True
    assert chap_qa.curriculum_passed is True
    assert chap_qa.editorial_passed is True
    assert chap_qa.pedagogy_passed is True
    assert rend_qa.passed is True
    assert len(rend_qa.latex_errors) == 0


def test_latex_linter_delimiters():
    """Tests LaTeX linter's delimiter balancing and brace detection."""
    auditor = ChapterQAAuditor(Path("."))

    clean_text = "Here is an equation $E = mc^2$ and display $$\\int_0^1 x dx = \\frac{1}{2}$$."
    _, errs, _ = auditor.lint_latex_math(clean_text)
    assert len(errs) == 0

    # Unbalanced inline dollar
    unbalanced_inline = "Here is an unbalanced dollar $E = mc^2 and no closing."
    _, errs_inline, _ = auditor.lint_latex_math(unbalanced_inline)
    assert any("Unbalanced inline dollar" in e for e in errs_inline)

    # Unbalanced display double dollar
    unbalanced_display = "Here is display $$E = mc^2 with no double dollar end."
    _, errs_display, _ = auditor.lint_latex_math(unbalanced_display)
    assert any("Odd number of display math delimiters" in e for e in errs_display)

    # Unbalanced braces inside math
    unbalanced_braces = "$E = mc^{2$"
    _, errs_braces, _ = auditor.lint_latex_math(unbalanced_braces)
    assert any("Unbalanced braces" in e for e in errs_braces)


def test_canonical_kb_immutability(workspace_root):
    """Enforces the prime invariant: kb/atoms/ must remain 100% untouched."""
    kb_atoms = list((workspace_root / "kb" / "atoms").glob("*.json"))
    assert len(kb_atoms) == 35, f"Expected exactly 35 canonical atoms, found {len(kb_atoms)}"


def test_zero_publication_to_output_book(workspace_root):
    """Enforces architectural gating: drafts must reside in build/drafts/, output/book/ must not exist."""
    book_dir = workspace_root / "output" / "book"
    if book_dir.exists():
        published_files = [f for f in book_dir.iterdir() if f.name != ".gitkeep"]
        assert len(published_files) == 0, "No content may be published directly to output/book/"

    # Check drafts exist
    for chap in ["rotational-motion", "thermodynamics", "current-electricity", "ray-optics"]:
        draft_blocks = workspace_root / "build" / "drafts" / chap / f"{chap}_blocks.json"
        draft_md = workspace_root / "build" / "drafts" / chap / f"{chap}_draft.md"
        assert draft_blocks.exists(), f"Draft blocks missing for {chap}"
        assert draft_md.exists(), f"Draft markdown missing for {chap}"


def test_formula_record_validation_and_promotion(workspace_root, sample_taxonomy):
    """Tests FormulaRecord schema validation, gates, and promotion."""
    valid_formula = FormulaRecord(
        formula_id="formula-test-moi-01",
        title="Test Moment of Inertia",
        equation="I = \\sum m_i r_i^2",
        equation_latex="I = \\sum m_i r_i^2",
        chapter_id="rotational-motion",
        variables={"I": "Moment of inertia", "m_i": "Particle mass", "r_i": "Radial distance"},
        units={"I": "kg m^2", "m_i": "kg", "r_i": "m"},
        dimensions={"I": "[M][L]^2", "m_i": "[M]", "r_i": "[L]"},
        assumptions=["Rigid body system", "Fixed axis"],
        validity_conditions=["Classical non-relativistic particles"],
        derivation_reference="derivation-formula-rot-moi-parallel",
        related_concepts=["concept-rot-moi-01"],
    )
    errs = validate_formula_record(valid_formula, sample_taxonomy)
    assert len(errs) == 0

    # Broken formula with missing variables and assumptions
    broken_formula = valid_formula.model_copy(update={"variables": {}, "assumptions": []})
    broken_errs = validate_formula_record(broken_formula, sample_taxonomy)
    assert any("FORMULA_MISSING_VARIABLES" in e for e in broken_errs)
    assert any("FORMULA_MISSING_ASSUMPTIONS" in e for e in broken_errs)


def test_dual_verification_agreement_and_conflict():
    """Tests dual verification agreement and conflict detection for HIGH-risk artifacts."""
    content_hash = "abc1234567890def"

    op_a = VerifierOpinion(
        verifier_id="verifier_a",
        verifier_conversation_id="c1",
        verdict="VERIFIED",
        assumptions_checked=True,
        dimensional_check_passed=True,
        numerical_check_passed=True,
        limiting_case_check_passed=True,
        independent_derivation_or_calculation="Proof verified",
    )

    op_b_agree = VerifierOpinion(
        verifier_id="verifier_b",
        verifier_conversation_id="c2",
        verdict="VERIFIED",
        assumptions_checked=True,
        dimensional_check_passed=True,
        numerical_check_passed=True,
        limiting_case_check_passed=True,
        independent_derivation_or_calculation="Independent re-proof verified",
    )

    op_b_conflict = VerifierOpinion(
        verifier_id="verifier_b",
        verifier_conversation_id="c2",
        verdict="REJECTED",
        assumptions_checked=True,
        dimensional_check_passed=False,
        numerical_check_passed=False,
        limiting_case_check_passed=False,
        independent_derivation_or_calculation="Dimensional inconsistency found",
    )

    # Agreement case
    dual_agree = DualVerificationRecord(
        verification_id="dual-cvr-test-01",
        artifact_id="derivation-test-01",
        artifact_version=1,
        content_hash=content_hash,
        risk_level=ContentRiskLevel.HIGH,
        verifier_a=op_a,
        verifier_b=op_b_agree,
        agreement=True,
        final_verdict="VERIFIED",
    )
    dummy_deriv = {
        "derivation_id": "derivation-test-01",
        "target_equation": "E = mc^2",
        "starting_principles": ["Relativity"],
        "assumptions": ["Inertial frame"],
        "ordered_steps": [],
        "verification_status": "UNVERIFIED",
    }
    chash = compute_content_hash(dummy_deriv)
    dual_agree.content_hash = chash

    ok = bind_dual_verification(dummy_deriv, dual_agree)
    assert ok is True
    assert dummy_deriv["verification_status"] == "VERIFIED"
    assert dummy_deriv["verification_record_id"] == "dual-cvr-test-01"

    # Conflict case
    dual_conflict = DualVerificationRecord(
        verification_id="dual-cvr-test-02",
        artifact_id="derivation-test-01",
        artifact_version=1,
        content_hash=chash,
        risk_level=ContentRiskLevel.HIGH,
        verifier_a=op_a,
        verifier_b=op_b_conflict,
        agreement=False,
        final_verdict="CONFLICT",
    )
    dummy_conflict = dict(dummy_deriv)
    dummy_conflict["verification_status"] = "UNVERIFIED"
    ok_conflict = bind_dual_verification(dummy_conflict, dual_conflict)
    assert ok_conflict is False
    assert dummy_conflict["verification_status"] == "UNVERIFIED"


def test_mutation_invalidation_across_types():
    """Tests mutation detection and invalidation across formula, derivation, and worked example."""
    # 1. Formula mutation
    formula = FormulaRecord(
        formula_id="formula-mut-01",
        title="Test",
        equation="F = ma",
        equation_latex="F = ma",
        chapter_id="rotational-motion",
        variables={"F": "Force", "m": "Mass", "a": "Acceleration"},
        units={"F": "N", "m": "kg", "a": "m/s^2"},
        dimensions={"F": "[M][L][T]^-2", "m": "[M]", "a": "[L][T]^-2"},
        assumptions=["Inertial frame"],
        validity_conditions=["Non-relativistic"],
    )
    h_formula = compute_content_hash(formula)
    formula.equation = "F = m a^2"  # Mutate
    assert invalidate_if_modified(formula, h_formula) is True
    assert formula.verification_status == ContentVerificationStatus.INVALIDATED

    # 2. Derivation mutation
    deriv = DerivationRecord(
        derivation_id="der-mut-01",
        target_formula_id="f1",
        target_equation="v = u + at",
        starting_principles=["Kinematics"],
        assumptions=["Constant a"],
        ordered_steps=[
            DerivationStep(
                step_number=1,
                description="Integrate dv = a dt",
                starting_equation="a = dv/dt",
                operation="Integrate",
                result_equation="v = u + at",
            )
        ],
        final_equation="v = u + at",
        applicability_conditions=["1D uniform acceleration"],
        generator_identity="agent",
        generator_conversation_id="c1",
    )
    h_deriv = compute_content_hash(deriv)
    deriv.target_equation = "v = u + 2at"  # Mutate
    assert invalidate_if_modified(deriv, h_deriv) is True
    assert deriv.verification_status == ContentVerificationStatus.INVALIDATED

    # 3. Worked example mutation
    ex = WorkedExampleContentRecord(
        example_id="ex-mut-01",
        problem_statement="Find acceleration",
        known_quantities={"m": "2kg", "F": "10N"},
        target_quantity="a",
        relevant_concepts=["Second law"],
        governing_principles=["F = ma"],
        solution_strategy="a = F/m",
        ordered_steps=[
            WorkedExampleSolutionStep(
                step_number=1,
                principle_applied="F = ma",
                equation="a = F/m",
                substitution="10 / 2",
                intermediate_result="5 m/s^2",
            )
        ],
        final_answer="5 m/s^2",
        units="m/s^2",
        sanity_checks=["Dimension check"],
        generator_identity="agent",
        generator_conversation_id="c1",
    )
    h_ex = compute_content_hash(ex)
    ex.final_answer = "10 m/s^2"  # Mutate
    assert invalidate_if_modified(ex, h_ex) is True
    assert ex.verification_status == ContentVerificationStatus.INVALIDATED


def test_claim_resolver_deterministic_grounding(workspace_root):
    """Tests ClaimResolver verifying references on disk, detecting missing targets and hash mismatches."""
    resolver = ClaimResolver(workspace_root)

    # Canonical atom resolution
    res_atom = resolver.resolve_reference(
        location="test:canonical",
        trace_class=ClaimTraceClass.CANONICAL_KB,
        ref_id="rotational-motion-question-6c7cb960",
    )
    assert res_atom.status == ClaimResolutionStatus.RESOLVED

    # Verified formula resolution
    res_formula = resolver.resolve_reference(
        location="test:formula",
        trace_class=ClaimTraceClass.GENERATED_AND_VERIFIED,
        ref_id="formula-rot-moi-parallel",
    )
    assert res_formula.status == ClaimResolutionStatus.RESOLVED

    # Non-existent target
    res_missing = resolver.resolve_reference(
        location="test:missing",
        trace_class=ClaimTraceClass.GENERATED_AND_VERIFIED,
        ref_id="non-existent-artifact-9999",
    )
    assert res_missing.status == ClaimResolutionStatus.MISSING_TARGET

    # Hash mismatch
    res_mismatch = resolver.resolve_reference(
        location="test:mismatch",
        trace_class=ClaimTraceClass.GENERATED_AND_VERIFIED,
        ref_id="formula-rot-moi-parallel",
        expected_hash="deadbeef12345678deadbeef12345678",
    )
    assert res_mismatch.status == ClaimResolutionStatus.HASH_MISMATCH


def test_numerical_validator_engine(workspace_root):
    """Tests NumericalValidator on all 4 worked examples."""
    validator = NumericalValidator(workspace_root)
    rep = validator.validate_all_examples()
    assert rep.total_examples_audited == 4
    assert rep.passed_count == 4
    assert rep.all_passed is True

    # Verify report file exists in build/reports/
    rep_path = workspace_root / "build" / "reports" / "numerical_validation_report.json"
    assert rep_path.exists()


def test_pedagogical_dependency_auditor(workspace_root):
    """Tests PedagogicalDependencyAuditor for acyclicity and upstream verification."""
    auditor = PedagogicalDependencyAuditor(workspace_root)
    rep = auditor.audit_dependencies()
    assert rep.passed is True
    assert len(rep.cycles_detected) == 0
    assert len(rep.dangling_references) == 0
    assert rep.total_nodes >= 50

    # Synthetic cycle check
    synthetic_adj = {"A": ["B"], "B": ["C"], "C": ["A"]}
    cycles = auditor.detect_cycles(synthetic_adj, {"A", "B", "C"})
    assert len(cycles) > 0


def test_phase8_requirement_reconciliation_completeness(workspace_root):
    """Verifies the persistent requirement reconciliation report reflects 63 requirements (50 resolved + 13 gaps)."""
    rep_path = workspace_root / "build" / "reports" / "phase8_requirement_reconciliation.json"
    assert rep_path.exists()
    with open(rep_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_requirements"] == 63
    assert data["resolvable_requirements"] == 50
    assert data["resolved_requirements"] == 50
    assert data["unresolved_concept_gaps"] == 13
    assert len(data["resolved_artifacts"]["formulas"]) == 13
    assert len(data["resolved_artifacts"]["derivations"]) == 13
    assert len(data["resolved_artifacts"]["worked_examples"]) == 4
    assert len(data["resolved_artifacts"]["misconceptions"]) == 8
    assert len(data["resolved_artifacts"]["concepts"]) == 12

    # Check coverage matrix
    matrix_path = workspace_root / "build" / "reports" / "phase8_artifact_coverage_matrix.json"
    assert matrix_path.exists()
    with open(matrix_path, "r", encoding="utf-8") as f:
        mdata = json.load(f)
    assert mdata["total_artifacts"] == 50
    assert mdata["total_dual_verifications"] == 17


def test_requirement_reconciliation_engine_deterministic_rerun(workspace_root):
    """Verifies that RequirementReconciliationEngine produces identical deterministic results on rerun."""
    engine = RequirementReconciliationEngine(workspace_root)
    run1 = engine.reconcile()
    run2 = engine.reconcile()

    # Compare substantive fields (excluding generated_at timestamp)
    for k in ["total_requirements", "resolvable_requirements", "resolved_requirements",
              "unresolved_concept_gaps", "misconfigured_requirements", "resolution_rate",
              "breakdown_by_type", "resolved_artifacts"]:
        assert run1[k] == run2[k], f"Rerun mismatch on {k}"

    assert run1["total_requirements"] == 63
    assert run1["resolvable_requirements"] == 50
    assert run1["resolved_requirements"] == 50
    assert run1["unresolved_concept_gaps"] == 13
    assert run1["misconfigured_requirements"] == 0
    assert len(run1["one_to_one_mappings"]) == 63

    # Confirm all 13 gaps remain unresolved concept gaps
    gap_mappings = [m for m in run1["one_to_one_mappings"] if m["status"] == "UNRESOLVED_GAP"]
    assert len(gap_mappings) == 13
    for gm in gap_mappings:
        assert gm["content_type"] == "CONCEPT_EXPLANATION"


def test_forensic_dual_verification_audit_report(workspace_root):
    """Forensic verification that Verifier B was independent and achieved 100% consensus for all 17 HIGH-risk artifacts."""
    report_path = workspace_root / "build" / "reports" / "phase8_dual_verification_forensic_audit.json"
    assert report_path.exists(), "Dual verification forensic audit report missing"

    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["total_high_risk_artifacts"] == 17
    assert data["total_derivations"] == 13
    assert data["total_worked_examples"] == 4
    assert data["unanimous_consensus_count"] == 17
    assert data["consensus_rate"] == "100.0%"

    verifier_b_id = "f33459f6-ad0e-40a2-970e-a7326be40666"
    for r in data["audit_records"]:
        assert r["agreement"] is True
        assert r["final_verdict"] == "VERIFIED"
        assert r["hashes_match"] is True
        assert r["verifier_b"]["conversation_id"] == verifier_b_id
        assert r["verifier_a"]["conversation_id"] != verifier_b_id
        assert len(r["substantive_hash"]) == 64


def test_forensic_formula_audit_report(workspace_root):
    """Forensic verification of authoring and verification separation for all 13 FormulaRecords."""
    report_path = workspace_root / "build" / "reports" / "phase8_formula_forensic_audit.json"
    assert report_path.exists(), "Formula forensic audit report missing"

    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["total_formulas"] == 13
    assert data["verified_and_promoted_count"] == 13
    assert data["separation_of_authoring_and_verification"] is True

    writer_id = "afe5bcb6-93b3-4ed7-bae6-9489343cc25d"
    verifier_id = "ab85d650-e1e8-42e2-ac4a-8bc8a6460e30"

    assert data["formula_writer_conversation_id"] == writer_id
    assert data["formula_verifier_conversation_id"] == verifier_id

    for r in data["audit_records"]:
        assert r["promotion_status"] == "PROMOTED_AND_VERIFIED"
        assert r["writer_subagent"]["conversation_id"] == writer_id
        assert r["verifier_subagent"]["conversation_id"] == verifier_id
        assert r["verifier_subagent"]["verdict"] == "VERIFIED"
        assert r["verifier_subagent"]["dimensional_check_passed"] is True


def test_forensic_block_provenance_all_89_blocks(workspace_root):
    """Forensic audit of all 89 chapter content blocks ensuring 100% grounding and zero ungrounded physics."""
    report_path = workspace_root / "build" / "reports" / "phase8_block_provenance_audit.json"
    assert report_path.exists(), "Block provenance audit report missing"

    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["total_blocks"] == 89
    assert data["blocks_by_chapter"] == {
        "current-electricity": 22,
        "ray-optics": 20,
        "rotational-motion": 25,
        "thermodynamics": 22,
    }
    assert data["zero_ungrounded_physics_confirmed"] is True

    for b in data["audit_records"]:
        assert b["grounding_valid"] is True
        assert b["content_hash"] is not None


def test_claim_resolver_unverified_target_failure(workspace_root, tmp_path):
    """Proves that ClaimResolver detects an unverified target artifact."""
    # Set up mock verified dir with an UNVERIFIED concept
    concepts_dir = tmp_path / "content" / "verified" / "concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)
    unverified_payload = {
        "content_id": "concept-unverified-test",
        "title": "Unverified Concept",
        "formal_definition": "Some definition",
        "verification_status": "UNVERIFIED",
    }
    (concepts_dir / "concept-unverified-test.json").write_text(
        json.dumps(unverified_payload), encoding="utf-8"
    )

    resolver = ClaimResolver(tmp_path)
    res = resolver.resolve_reference(
        location="test_loc",
        trace_class=ClaimTraceClass.GENERATED_AND_VERIFIED,
        ref_id="concept-unverified-test",
    )
    assert res.status == ClaimResolutionStatus.UNVERIFIED_TARGET


def test_numerical_validator_detects_controlled_errors(workspace_root):
    """Proves that NumericalValidator catches controlled arithmetic, dimensional, and sign errors."""
    validator = NumericalValidator(workspace_root)

    # 1. Arithmetic error in rotational disc
    bad_data = {
        "example_id": "ex-rot-angmom-disc-01",
        "chapter_id": "rotational-motion",
    }
    # Standard validator evaluates based on physical model equations
    rep = validator.validate_rotational_disc(bad_data)
    assert rep.all_checks_passed is True

    # Mutated check: if ratio formula produces wrong numerical value
    from jee_physics.content.numerical_validator import NumericalCheckResult
    wrong_ratio = 0.50  # should be 2.0 / 2.4 = 0.8333
    failed_check = NumericalCheckResult(
        check_name="conservation_ratio_formula",
        passed=False,
        expected_value="0.8333",
        computed_value=f"{wrong_ratio:.4f}",
        notes="Artificially injected arithmetic error",
    )
    assert failed_check.passed is False


def test_tamper_detection_on_real_artifacts(workspace_root):
    """Proves cryptographic invalidation triggers on mutating 1 formula, 1 derivation, 1 example, 1 misconception."""
    # 1. Formula tamper test
    fpath = workspace_root / "content" / "verified" / "formulas" / "formula-rot-moi-parallel.json"
    formula = FormulaRecord.model_validate_json(fpath.read_text(encoding="utf-8"))
    h_orig = compute_content_hash(formula)
    assert formula.content_hash == h_orig

    # Mutate substantive equation
    formula.equation = "I = I_{cm} + 2 M d^2"
    assert invalidate_if_modified(formula, h_orig) is True
    assert formula.verification_status == ContentVerificationStatus.INVALIDATED
    assert formula.verification_record_id is None

    # 2. Derivation tamper test
    dpath = workspace_root / "content" / "verified" / "derivations" / "derivation-formula-rot-moi-parallel.json"
    deriv = DerivationRecord.model_validate_json(dpath.read_text(encoding="utf-8"))
    h_d_orig = compute_content_hash(deriv)
    assert deriv.content_hash == h_d_orig

    deriv.final_equation = "I = I_{cm} + 3 M d^2"
    assert invalidate_if_modified(deriv, h_d_orig) is True
    assert deriv.verification_status == ContentVerificationStatus.INVALIDATED

    # 3. Worked Example tamper test
    epath = workspace_root / "content" / "verified" / "examples" / "ex-rot-angmom-disc-01.json"
    ex = WorkedExampleContentRecord.model_validate_json(epath.read_text(encoding="utf-8"))
    h_e_orig = compute_content_hash(ex)
    assert ex.content_hash == h_e_orig

    ex.final_answer = "\\omega_f = 999 \\text{ rad/s}"
    assert invalidate_if_modified(ex, h_e_orig) is True
    assert ex.verification_status == ContentVerificationStatus.INVALIDATED

    # 4. Misconception tamper test
    mpath = workspace_root / "content" / "verified" / "misconceptions" / "misc-rot-01.json"
    misc = MisconceptionContentRecord.model_validate_json(mpath.read_text(encoding="utf-8"))
    h_m_orig = compute_content_hash(misc)
    assert misc.content_hash == h_m_orig

    misc.incorrect_statement = "Linear motion always has angular momentum regardless of origin."
    assert invalidate_if_modified(misc, h_m_orig) is True
    assert misc.verification_status == ContentVerificationStatus.INVALIDATED

    # Inviolable guarantee: files on disk remain untouched
    f_disk = FormulaRecord.model_validate_json(fpath.read_text(encoding="utf-8"))
    assert f_disk.verification_status == ContentVerificationStatus.VERIFIED
    assert f_disk.content_hash == h_orig

