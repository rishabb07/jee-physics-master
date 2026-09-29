"""
Comprehensive test suite for Phase 9: Question Bank & Assessment Generation.

Tests cover:
1. Typed Question Models & Validation.
2. Substantive Question Hashing & Invalidation on Mutation.
3. Question Gate & Taxonomy/Curriculum Alignment.
4. Answer Uniqueness & Distractor Conflict Detection.
5. Numerical & Physical Consistency Validation (Wire Recasting, Adiabatic Compression).
6. Deduplication Integration (Duplicate Detection & Clustering).
7. Risk-Calibrated Dual Verification for HIGH-risk Questions.
8. Promotion, Staging, and Review Queue Routing.
9. Assessment Blueprint & Mock Paper Assembly.
10. Cognitive Question Ladders & Dependency Network.
11. Strict Canonical KB Immutability (kb/atoms/ = 35) & Zero Direct Publication (output/book/ empty).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import pytest
import yaml

from jee_physics.models.curriculum import DifficultyDimensions, ExamTargetLevel
from jee_physics.models.dedup import DedupAction, DedupDecisionClass
from jee_physics.models.enums import DifficultyLevel
from jee_physics.models.question_bank import (
    CognitiveLadderLevel,
    DistractorRationale,
    GeneratedQuestion,
    QuestionLadder,
    QuestionLadderRung,
    QuestionOrigin,
    QuestionQualityStatus,
    QuestionRiskLevel,
    QuestionSolverOpinion,
    QuestionType,
    QuestionVerificationRecord,
    SourceGrounding,
    TaxonomyReference,
)
from jee_physics.models.taxonomy import SubjectType, TaxonomyTree
from jee_physics.question_bank.assessment import AssessmentBuilder
from jee_physics.question_bank.dedup_adapter import QuestionDedupAdapter
from jee_physics.question_bank.dependency import QuestionDependencyGraphBuilder
from jee_physics.question_bank.gate import (
    bind_question_verification,
    compute_question_hash,
    invalidate_question_if_modified,
    promote_question,
    route_to_review,
    validate_answer_uniqueness_and_distractors,
    validate_question_schema_and_curriculum,
)
from jee_physics.question_bank.ladders import QuestionLadderBuilder
from jee_physics.question_bank.numerical_validator import QuestionNumericalValidator


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def syllabus_tree(workspace_root: Path) -> TaxonomyTree:
    with open(workspace_root / "kb" / "taxonomy" / "syllabus.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return TaxonomyTree.model_validate(data)


@pytest.fixture
def sample_question() -> GeneratedQuestion:
    return GeneratedQuestion(
        question_id="sample-q-opt-01",
        version=1,
        origin=QuestionOrigin.GENERATED,
        curriculum_id="curr-opt-01",
        taxonomy_reference=TaxonomyReference(
            chapter_id="ray-optics",
            topic_id="refraction-at-plane-surfaces",
            subtopic_id="snells-law",
        ),
        concept_references=["concept-opt-snell-01"],
        prerequisite_references=["curr-opt-01"],
        target_exam_level=ExamTargetLevel.JEE_MAIN,
        question_type=QuestionType.SINGLE_CORRECT_MCQ,
        statement="A ray of light enters a medium of refractive index $n$ from vacuum. What is its speed?",
        options={
            "A": "$c/n$",
            "B": "$c$",
            "C": "$n c$",
            "D": "$c/n^2$",
        },
        correct_answer="A",
        solution_strategy="Use definition of refractive index $n = c/v$.",
        solution="By definition of absolute refractive index, $v = c/n$. Thus Option A is correct.",
        assumptions=["Isotropic dielectric medium"],
        intended_learning_objective="Understand phase velocity reduction in dielectric media",
        difficulty_dimensions=DifficultyDimensions(
            conceptual_difficulty=2,
            mathematical_difficulty=1,
            multistep_reasoning_difficulty=1,
            abstraction_difficulty=1,
            computational_burden=1,
            trap_misconception_difficulty=1,
        ),
        difficulty_band=DifficultyLevel.L1,
        distractor_rationales=[
            DistractorRationale(
                option_key="B",
                distractor_value="$c$",
                likely_misconception="Light speed invariance",
                student_rationale="Thinks c is invariant in all media",
                physical_error="Only c in vacuum is invariant",
                error_category="BOUNDARY_ERROR",
            ),
            DistractorRationale(
                option_key="C",
                distractor_value="$n c$",
                likely_misconception="Inverse ratio",
                student_rationale="Inverts relation",
                physical_error="Medium cannot accelerate light beyond c",
                error_category="FORMULA_INVERSION",
            ),
            DistractorRationale(
                option_key="D",
                distractor_value="$c/n^2$",
                likely_misconception="Squared index",
                student_rationale="Confuses permittivity with refractive index",
                physical_error="Speed scales as 1/n, not 1/n^2",
                error_category="DIMENSIONAL_CONFUSION",
            ),
        ],
        source_grounding=SourceGrounding(relationship_type="NEW_PROBLEM"),
        risk_level=QuestionRiskLevel.LOW,
    )


# ==============================================================================
# 1. Typed Model & Schema Validation Tests
# ==============================================================================

def test_generated_question_model_valid(sample_question: GeneratedQuestion):
    """GeneratedQuestion must instantiate with all validated fields."""
    assert sample_question.question_id == "sample-q-opt-01"
    assert sample_question.question_type == QuestionType.SINGLE_CORRECT_MCQ
    assert sample_question.correct_answer == "A"
    assert len(sample_question.options) == 4
    assert sample_question.verification_status == QuestionQualityStatus.GENERATED


def test_generated_question_invalid_mcq_missing_answer():
    """MCQ with correct_answer not in options must fail validation."""
    with pytest.raises(ValueError, match="Correct answer 'Z' not in options keys"):
        GeneratedQuestion(
            question_id="invalid-mcq-01",
            curriculum_id="curr-opt-01",
            taxonomy_reference=TaxonomyReference(chapter_id="ray-optics", topic_id="refraction"),
            concept_references=["concept-opt-snell-01"],
            target_exam_level=ExamTargetLevel.JEE_MAIN,
            question_type=QuestionType.SINGLE_CORRECT_MCQ,
            statement="Test question statement long enough",
            options={"A": "opt 1", "B": "opt 2"},
            correct_answer="Z",
            solution_strategy="strategy",
            solution="solution text long enough",
            intended_learning_objective="learning objective",
            difficulty_dimensions=DifficultyDimensions(
                conceptual_difficulty=1,
                mathematical_difficulty=1,
                multistep_reasoning_difficulty=1,
                abstraction_difficulty=1,
                computational_burden=1,
                trap_misconception_difficulty=1,
            ),
            difficulty_band=DifficultyLevel.L1,
            source_grounding=SourceGrounding(relationship_type="NEW_PROBLEM"),
        )


def test_validate_question_schema_and_curriculum(sample_question: GeneratedQuestion, syllabus_tree: TaxonomyTree):
    """Schema validator passes for compliant question."""
    errors = validate_question_schema_and_curriculum(sample_question, syllabus_tree)
    assert errors == []


def test_validate_question_schema_rejects_missing_distractor_rationale(sample_question: GeneratedQuestion, syllabus_tree: TaxonomyTree):
    """Single-choice MCQ missing distractor rationales must be flagged."""
    sample_question.distractor_rationales = []
    errors = validate_question_schema_and_curriculum(sample_question, syllabus_tree)
    assert any("MISSING_DISTRACTOR_RATIONALE" in e for e in errors)


# ==============================================================================
# 2. Substantive Hashing & Mutation Invalidation Tests
# ==============================================================================

def test_compute_question_hash_deterministic(sample_question: GeneratedQuestion):
    """Hashing is deterministic and ignores volatile verification fields."""
    h1 = compute_question_hash(sample_question)
    sample_question.verification_status = QuestionQualityStatus.VERIFIED
    sample_question.verification_record_id = "qvr-test-01"
    h2 = compute_question_hash(sample_question)
    assert h1 == h2


def test_compute_question_hash_sensitive_to_statement(sample_question: GeneratedQuestion):
    """Substantive modification of statement alters hash."""
    h1 = compute_question_hash(sample_question)
    sample_question.statement += " Modified wording."
    h2 = compute_question_hash(sample_question)
    assert h1 != h2


def test_invalidate_question_if_modified(sample_question: GeneratedQuestion):
    """Mutating verified question triggers invalidation of verification status."""
    orig_hash = compute_question_hash(sample_question)
    sample_question.verification_status = QuestionQualityStatus.VERIFIED
    sample_question.verification_record_id = "qvr-sample-01"

    # Modify statement
    sample_question.statement = "Completely altered statement."
    invalidated = invalidate_question_if_modified(sample_question, orig_hash)

    assert invalidated is True
    assert sample_question.verification_status == QuestionQualityStatus.INVALIDATED
    assert sample_question.verification_record_id is None


# ==============================================================================
# 3. Answer Uniqueness & Distractor Conflict Gate Tests
# ==============================================================================

def test_distractor_conflict_detection(sample_question: GeneratedQuestion):
    """Gate flags DISTRACTOR_CONFLICT when a distractor is also physically valid."""
    opinion = QuestionSolverOpinion(
        solver_id="solver_a",
        conversation_id="conv-solver-a",
        independent_interpretation="Ray optics refraction",
        governing_principles=["Snell's Law"],
        independent_equations=["v = c/n"],
        independent_solution_steps=["v = c/n matches A"],
        calculated_answer="A",
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=False,
        conflicting_distractors=["B"],
        evaluated_difficulty=sample_question.difficulty_dimensions,
        verdict="CONFLICT",
    )
    errors = validate_answer_uniqueness_and_distractors(sample_question, opinion)
    assert any("DISTRACTOR_CONFLICT" in e for e in errors)
    assert any("NON_UNIQUE_ANSWER" in e for e in errors)


def test_answer_mismatch_detection(sample_question: GeneratedQuestion):
    """Gate flags ANSWER_MISMATCH when solver calculates different answer."""
    opinion = QuestionSolverOpinion(
        solver_id="solver_a",
        conversation_id="conv-solver-a",
        independent_interpretation="Ray optics refraction",
        governing_principles=["Snell's Law"],
        independent_equations=["v = c/n"],
        independent_solution_steps=["Derivation yields C"],
        calculated_answer="C",
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=True,
        conflicting_distractors=[],
        evaluated_difficulty=sample_question.difficulty_dimensions,
        verdict="CONFLICT",
    )
    errors = validate_answer_uniqueness_and_distractors(sample_question, opinion)
    assert any("ANSWER_MISMATCH" in e for e in errors)


def test_multi_correct_answer_validation():
    """Multi-correct MCQ validates sets of correct answers."""
    q = GeneratedQuestion(
        question_id="mcq-multi-01",
        curriculum_id="curr-td-02",
        taxonomy_reference=TaxonomyReference(chapter_id="thermodynamics", topic_id="adiabatic"),
        concept_references=["concept-td-adiabatic-01"],
        target_exam_level=ExamTargetLevel.JEE_ADVANCED,
        question_type=QuestionType.MULTIPLE_CORRECT_MCQ,
        statement="Which statements are correct for reversible adiabatic process?",
        options={"A": "TV^(gamma-1) const", "B": "W = -Delta U", "C": "Delta S = 0", "D": "PV^gamma const"},
        correct_answer=["A", "B", "C", "D"],
        solution_strategy="Check all 4 equations",
        solution="All four statements are fundamental properties of reversible adiabatic processes.",
        intended_learning_objective="Thermodynamic relations",
        difficulty_dimensions=DifficultyDimensions(
            conceptual_difficulty=3,
            mathematical_difficulty=2,
            multistep_reasoning_difficulty=2,
            abstraction_difficulty=2,
            computational_burden=1,
            trap_misconception_difficulty=2,
        ),
        difficulty_band=DifficultyLevel.L3,
        source_grounding=SourceGrounding(relationship_type="NEW_PROBLEM"),
    )
    opinion = QuestionSolverOpinion(
        solver_id="solver_a",
        conversation_id="conv-solver-a",
        independent_interpretation="Adiabatic relations",
        governing_principles=["First Law", "Adiabatic invariants"],
        independent_equations=["TV^(g-1)=const", "PV^g=const"],
        independent_solution_steps=["Verified all 4 options"],
        calculated_answer=["A", "B", "C", "D"],
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=True,
        conflicting_distractors=[],
        evaluated_difficulty=q.difficulty_dimensions,
        verdict="VERIFIED",
    )
    errors = validate_answer_uniqueness_and_distractors(q, opinion)
    assert errors == []


# ==============================================================================
# 4. Numerical & Physical Validator Tests
# ==============================================================================

def test_numerical_validator_wire_recasting(workspace_root: Path):
    """Wire recasting validator proves R scales as (r_0/r_f)^4 = 16."""
    validator = QuestionNumericalValidator(workspace_root)
    q = GeneratedQuestion(
        question_id="gen-q-curr-num-01",
        curriculum_id="curr-curr-02",
        taxonomy_reference=TaxonomyReference(chapter_id="current-electricity", topic_id="resistance"),
        concept_references=["concept-curr-recasting-01"],
        target_exam_level=ExamTargetLevel.JEE_MAIN,
        question_type=QuestionType.NUMERICAL,
        statement="A copper wire of initial resistance R = 10 Ohm has its radius halved. Final resistance:",
        correct_answer="160.0",
        units="Ohm",
        tolerance=0.02,
        numerical_values={"initial_resistance": 10.0, "radius_ratio": 0.5},
        solution_strategy="Volume conservation",
        solution="R scales as 1/r^4, so 10 * 16 = 160 Ohm.",
        intended_learning_objective="Conductor volume conservation",
        difficulty_dimensions=DifficultyDimensions(
            conceptual_difficulty=2,
            mathematical_difficulty=2,
            multistep_reasoning_difficulty=2,
            abstraction_difficulty=1,
            computational_burden=2,
            trap_misconception_difficulty=3,
        ),
        difficulty_band=DifficultyLevel.L2,
        source_grounding=SourceGrounding(relationship_type="NEW_PROBLEM"),
    )
    rep = validator.validate_question(q)
    assert rep.all_checks_passed is True
    assert rep.verified_answer == "160.0"
    assert rep.units_valid is True


def test_numerical_validator_adiabatic_compression(workspace_root: Path):
    """Adiabatic compression validator proves T2 = T1 * 32^0.4 = 300 * 4 = 1200 K."""
    validator = QuestionNumericalValidator(workspace_root)
    q = GeneratedQuestion(
        question_id="gen-q-td-multi-01",
        curriculum_id="curr-td-02",
        taxonomy_reference=TaxonomyReference(chapter_id="thermodynamics", topic_id="adiabatic"),
        concept_references=["concept-td-adiabatic-01"],
        target_exam_level=ExamTargetLevel.JEE_ADVANCED,
        question_type=QuestionType.NUMERICAL,
        statement="Diatomic gas compressed by volume factor 32. Final temperature:",
        correct_answer="1200.0",
        units="K",
        tolerance=0.02,
        numerical_values={"gamma": 1.4, "volume_ratio": 32.0, "initial_temperature": 300.0},
        solution_strategy="TV^(gamma-1) = const",
        solution="T2 = 300 * 32^0.4 = 300 * 4 = 1200 K.",
        intended_learning_objective="Adiabatic temperature scaling",
        difficulty_dimensions=DifficultyDimensions(
            conceptual_difficulty=3,
            mathematical_difficulty=3,
            multistep_reasoning_difficulty=3,
            abstraction_difficulty=2,
            computational_burden=2,
            trap_misconception_difficulty=2,
        ),
        difficulty_band=DifficultyLevel.L3,
        source_grounding=SourceGrounding(relationship_type="NEW_PROBLEM"),
    )
    rep = validator.validate_question(q)
    assert rep.all_checks_passed is True
    assert rep.verified_answer == "1200.0"
    assert rep.units_valid is True


# ==============================================================================
# 5. Deduplication Integration Tests
# ==============================================================================

def test_dedup_adapter_catches_near_duplicate(workspace_root: Path):
    """Deduplication adapter detects duplicate question against canonical atoms."""
    adapter = QuestionDedupAdapter(workspace_root)
    dup_q = GeneratedQuestion(
        question_id="gen-q-dup-test-01",
        curriculum_id="curr-curr-02",
        taxonomy_reference=TaxonomyReference(chapter_id="current-electricity", topic_id="resistance"),
        concept_references=["concept-curr-recasting-01"],
        target_exam_level=ExamTargetLevel.JEE_MAIN,
        question_type=QuestionType.SINGLE_CORRECT_MCQ,
        statement="A wire of resistance R is stretched uniformly so that its length is doubled while volume remains constant. Its new resistance will be:",
        options={"A": "2R", "B": "4R", "C": "R/2", "D": "R/4"},
        correct_answer="B",
        solution_strategy="Volume conservation",
        solution="L doubles, A halves, so R quadruples to 4R.",
        intended_learning_objective="Stretching wire",
        difficulty_dimensions=DifficultyDimensions(
            conceptual_difficulty=2,
            mathematical_difficulty=1,
            multistep_reasoning_difficulty=2,
            abstraction_difficulty=1,
            computational_burden=1,
            trap_misconception_difficulty=3,
        ),
        difficulty_band=DifficultyLevel.L2,
        source_grounding=SourceGrounding(relationship_type="NEW_PROBLEM"),
    )
    res = adapter.evaluate_question(dup_q)
    assert res.is_duplicate is True
    assert res.decision_class == DedupDecisionClass.SEMANTIC_DUPLICATE
    assert res.recommended_action == DedupAction.MERGE


def test_dedup_adapter_approves_source_derivative(workspace_root: Path):
    """Deduplication adapter approves authorized source derivative with distinct parameters."""
    adapter = QuestionDedupAdapter(workspace_root)
    deriv_q = GeneratedQuestion(
        question_id="gen-q-curr-src-deriv-01",
        curriculum_id="curr-curr-03",
        taxonomy_reference=TaxonomyReference(chapter_id="current-electricity", topic_id="meters"),
        concept_references=["concept-curr-meters-01"],
        target_exam_level=ExamTargetLevel.JEE_MAIN,
        question_type=QuestionType.SINGLE_CORRECT_MCQ,
        statement="A moving coil galvanometer has coil resistance G = 50 Ohm and full-scale current Ig = 2 mA. Required shunt for 5 A range:",
        options={"A": "0.020 Ohm", "B": "0.050 Ohm", "C": "0.100 Ohm", "D": "1.000 Ohm"},
        correct_answer="A",
        solution_strategy="Shunt equation",
        solution="S = Ig G / (I - Ig) approx 0.020 Ohm.",
        intended_learning_objective="Ammeter shunting",
        difficulty_dimensions=DifficultyDimensions(
            conceptual_difficulty=2,
            mathematical_difficulty=2,
            multistep_reasoning_difficulty=2,
            abstraction_difficulty=1,
            computational_burden=2,
            trap_misconception_difficulty=2,
        ),
        difficulty_band=DifficultyLevel.L2,
        source_grounding=SourceGrounding(
            relationship_type="SOURCE_DERIVATIVE",
            source_atom_id="current-electricity-question-3a1b8c4d",
            transformation_type="PARAMETER_VARIATION",
            what_changed="Changed coil resistance from 100 to 50 Ohm and current to 5A",
            why_pedagogically_distinct="Exercises multi-decade scale difference",
        ),
    )
    res = adapter.evaluate_question(deriv_q)
    assert res.is_duplicate is False
    assert res.recommended_action == DedupAction.KEEP_SEPARATE


# ==============================================================================
# 6. High-Risk Dual Verification Tests
# ==============================================================================

def test_high_risk_dual_verification_enforcement(sample_question: GeneratedQuestion):
    """HIGH-risk question strictly requires Solver B and solver agreement."""
    sample_question.risk_level = QuestionRiskLevel.HIGH
    q_hash = compute_question_hash(sample_question)
    sample_question.content_hash = q_hash

    solver_a = QuestionSolverOpinion(
        solver_id="solver_a",
        conversation_id="conv-a",
        independent_interpretation="Interpretation",
        governing_principles=["Law 1"],
        independent_equations=["Eq 1"],
        independent_solution_steps=["Step 1"],
        calculated_answer="A",
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=True,
        conflicting_distractors=[],
        evaluated_difficulty=sample_question.difficulty_dimensions,
        verdict="VERIFIED",
    )

    # 1. Verification record with NO solver_b must fail binding for high-risk
    v_rec_single = QuestionVerificationRecord(
        verification_id="qvr-test-single",
        question_id=sample_question.question_id,
        content_hash=q_hash,
        risk_level=QuestionRiskLevel.HIGH,
        solver_a=solver_a,
        solver_b=None,
        agreement=False,
        uniqueness_verified=True,
        distractors_validated=True,
        numerical_validated=True,
        final_answer="A",
        final_verdict=QuestionQualityStatus.VERIFIED,
        difficulty_calibrated=sample_question.difficulty_dimensions,
    )
    assert bind_question_verification(sample_question, v_rec_single) is False

    # 2. Verification record with agreeing solver_b succeeds binding
    solver_b = QuestionSolverOpinion(
        solver_id="solver_b",
        conversation_id="conv-b",
        independent_interpretation="Independent blind interpretation",
        governing_principles=["Law 1"],
        independent_equations=["Eq 1"],
        independent_solution_steps=["Step 1"],
        calculated_answer="A",
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=True,
        conflicting_distractors=[],
        evaluated_difficulty=sample_question.difficulty_dimensions,
        verdict="VERIFIED",
    )
    v_rec_dual = QuestionVerificationRecord(
        verification_id="qvr-test-dual",
        question_id=sample_question.question_id,
        content_hash=q_hash,
        risk_level=QuestionRiskLevel.HIGH,
        solver_a=solver_a,
        solver_b=solver_b,
        agreement=True,
        uniqueness_verified=True,
        distractors_validated=True,
        numerical_validated=True,
        final_answer="A",
        final_verdict=QuestionQualityStatus.VERIFIED,
        difficulty_calibrated=sample_question.difficulty_dimensions,
    )
    assert bind_question_verification(sample_question, v_rec_dual) is True
    assert sample_question.verification_status == QuestionQualityStatus.VERIFIED
    assert sample_question.verification_record_id == "qvr-test-dual"


# ==============================================================================
# 7. Promotion & Review Queue Isolation Tests
# ==============================================================================

def test_promote_unverified_question_raises(sample_question: GeneratedQuestion, tmp_path: Path):
    """Attempting to promote an unverified question raises an exception."""
    sample_question.verification_status = QuestionQualityStatus.GENERATED
    with pytest.raises(ValueError, match="Cannot promote unverified question"):
        promote_question(sample_question, tmp_path / "verified", tmp_path / "audit.jsonl")


def test_route_to_review(sample_question: GeneratedQuestion, tmp_path: Path):
    """route_to_review writes structured review item and sets status to REVIEW."""
    rev_dir = tmp_path / "review"
    path = route_to_review(
        question=sample_question,
        reason="FATAL_DISTRACTOR_CONFLICT",
        details={"conflicting_options": ["B", "C"]},
        review_queue_dir=rev_dir,
    )
    assert path.exists()
    assert sample_question.verification_status == QuestionQualityStatus.REVIEW
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["review_reason"] == "FATAL_DISTRACTOR_CONFLICT"
    assert data["question_id"] == sample_question.question_id


# ==============================================================================
# 8. Assessment Blueprint & Mock Paper Assembly Tests
# ==============================================================================

def test_assessment_paper_assembly(workspace_root: Path):
    """AssessmentBuilder validates blueprints and assembles mock test papers."""
    builder = AssessmentBuilder(workspace_root)
    bp = builder.create_pilot_jee_advanced_blueprint()
    assert bp.target_exam == ExamTargetLevel.JEE_ADVANCED
    assert bp.total_marks == 18.0

    # Load promoted verified questions
    verified_dir = workspace_root / "question_bank" / "verified"
    questions = []
    for f in verified_dir.glob("*.json"):
        questions.append(GeneratedQuestion.model_validate(json.loads(f.read_text(encoding="utf-8"))))

    paper = builder.assemble_paper(bp, questions)
    assert paper.total_questions > 0
    assert len(paper.sections) == len(bp.sections)


# ==============================================================================
# 9. Question Ladder & Dependency Graph Tests
# ==============================================================================

def test_question_ladder_integrity(workspace_root: Path):
    """QuestionLadderBuilder constructs acyclic progressive cognitive rungs."""
    builder = QuestionLadderBuilder(workspace_root)
    ladder = builder.build_rotational_angular_momentum_ladder({})
    errors = builder.validate_ladder(ladder)
    assert errors == []
    assert len(ladder.rungs) == 4
    # Check progressive cognitive levels
    assert ladder.rungs[0].cognitive_level == CognitiveLadderLevel.DIRECT_APPLICATION
    assert ladder.rungs[1].cognitive_level == CognitiveLadderLevel.RECOGNITION
    assert ladder.rungs[2].cognitive_level == CognitiveLadderLevel.CONCEPT_COMBINATION
    assert ladder.rungs[3].cognitive_level == CognitiveLadderLevel.ADVANCED_SYNTHESIS


def test_question_dependency_graph(workspace_root: Path):
    """QuestionDependencyGraphBuilder creates connected assessment dependency network."""
    builder = QuestionDependencyGraphBuilder(workspace_root)
    verified_dir = workspace_root / "question_bank" / "verified"
    questions = [
        GeneratedQuestion.model_validate(json.loads(f.read_text(encoding="utf-8")))
        for f in verified_dir.glob("*.json")
    ]
    report = builder.build_graph(questions)
    assert report.total_nodes > 0
    assert report.total_edges > 0
    assert report.all_references_valid is True


# ==============================================================================
# 10. Invariant Enforcement: Strict Canonical KB & Output Book Protection
# ==============================================================================

def test_canonical_kb_strictly_untouched(workspace_root: Path):
    """Phase 9 question generation must NEVER alter kb/atoms/ (35 canonical atoms)."""
    kb_atoms = list((workspace_root / "kb" / "atoms").glob("*.json"))
    assert len(kb_atoms) == 35, f"Expected 35 canonical atoms, found {len(kb_atoms)}"
    for atom_path in kb_atoms:
        data = json.loads(atom_path.read_text(encoding="utf-8"))
        assert "atom_id" in data, f"Atom at {atom_path} lacks atom_id"
        assert not atom_path.name.startswith("gen-q-"), f"Generated question leaked into kb/atoms/: {atom_path.name}"


def test_output_book_strictly_empty(workspace_root: Path):
    """Phase 9 assessment system must NEVER publish directly to output/book/."""
    book_files = [p.name for p in (workspace_root / "output" / "book").iterdir() if p.name != ".gitkeep"]
    assert len(book_files) == 0, f"Premature publishing detected in output/book/: {book_files}"


# ==============================================================================
# 11. Deterministic Ambiguity Gate Tests (4 Ambiguity Classes + Well-Posed)
# ==============================================================================

def test_ambiguity_gate_missing_info_routes_to_review(workspace_root: Path, tmp_path: Path):
    """Missing information fixture results in AMBIGUOUS verdict and routes to review queue."""
    fixture_path = workspace_root / "tests" / "fixtures" / "question_bank" / "ambig_missing_info.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    q = GeneratedQuestion.model_validate(data)

    opinion = QuestionSolverOpinion(
        solver_id="solver_test",
        conversation_id="conv-ambig-1",
        independent_interpretation="Process path and heat exchange Q are missing; temperature cannot be determined.",
        governing_principles=["First Law of Thermodynamics"],
        independent_equations=["Delta U = Q - W"],
        independent_solution_steps=["Identified missing parameter Q"],
        calculated_answer="UNKNOWN",
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=False,
        conflicting_distractors=[],
        evaluated_difficulty=q.difficulty_dimensions,
        verdict="AMBIGUOUS",
        notes="Missing essential parameter Q and thermodynamic process type.",
    )

    errors = validate_answer_uniqueness_and_distractors(q, opinion)
    assert any("AMBIGUOUS_PROBLEM" in e for e in errors)

    rev_dir = tmp_path / "review"
    rev_path = route_to_review(q, "PHYSICAL_AMBIGUITY_UNDERSPECIFIED", {"errors": errors}, rev_dir)
    assert rev_path.exists()
    assert q.verification_status == QuestionQualityStatus.REVIEW


def test_ambiguity_gate_multiple_interpretations_routes_to_review(workspace_root: Path, tmp_path: Path):
    """Multiple valid interpretations fixture routes to review queue."""
    fixture_path = workspace_root / "tests" / "fixtures" / "question_bank" / "ambig_multiple_interpretations.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    q = GeneratedQuestion.model_validate(data)

    opinion = QuestionSolverOpinion(
        solver_id="solver_test",
        conversation_id="conv-ambig-2",
        independent_interpretation="Collision restitution e is unstated; elastic gives v2, inelastic gives (v1+v2)/2.",
        governing_principles=["Linear Momentum Conservation"],
        independent_equations=["m v1 + m v2 = m v1' + m v2'"],
        independent_solution_steps=["Calculated elastic and inelastic outcomes"],
        calculated_answer=["v2", "(v1+v2)/2"],
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=False,
        conflicting_distractors=["B"],
        evaluated_difficulty=q.difficulty_dimensions,
        verdict="AMBIGUOUS",
        notes="Materially conflicting physical interpretations due to unstated coefficient of restitution.",
    )

    errors = validate_answer_uniqueness_and_distractors(q, opinion)
    assert any("AMBIGUOUS_PROBLEM" in e for e in errors)
    assert any("DISTRACTOR_CONFLICT" in e for e in errors)

    rev_dir = tmp_path / "review"
    rev_path = route_to_review(q, "MULTIPLE_VALID_INTERPRETATIONS", {"errors": errors}, rev_dir)
    assert rev_path.exists()
    assert q.verification_status == QuestionQualityStatus.REVIEW


def test_ambiguity_gate_multiple_numerical_answers_routes_to_review(workspace_root: Path, tmp_path: Path):
    """Multiple valid numerical answers fixture routes to review queue."""
    fixture_path = workspace_root / "tests" / "fixtures" / "question_bank" / "ambig_multiple_numerical_answers.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    q = GeneratedQuestion.model_validate(data)

    opinion = QuestionSolverOpinion(
        solver_id="solver_test",
        conversation_id="conv-ambig-3",
        independent_interpretation="Quadratic kinematics gives t = 2.0 s and t = 6.0 s without direction qualifier.",
        governing_principles=["Constant Acceleration Kinematics"],
        independent_equations=["y = u t - 1/2 g t^2"],
        independent_solution_steps=["Solved quadratic roots t1=2.0s, t2=6.0s"],
        calculated_answer=["2.0", "6.0"],
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=False,
        conflicting_distractors=[],
        evaluated_difficulty=q.difficulty_dimensions,
        verdict="AMBIGUOUS",
        notes="Two valid positive time values satisfy height target without ascending/descending constraint.",
    )

    errors = validate_answer_uniqueness_and_distractors(q, opinion)
    assert any("AMBIGUOUS_PROBLEM" in e for e in errors)

    rev_dir = tmp_path / "review"
    rev_path = route_to_review(q, "MULTIPLE_VALID_NUMERICAL_ANSWERS", {"errors": errors}, rev_dir)
    assert rev_path.exists()
    assert q.verification_status == QuestionQualityStatus.REVIEW


def test_ambiguity_gate_ambiguous_figure_routes_to_review(workspace_root: Path, tmp_path: Path):
    """Ambiguous diagram fixture routes to review queue."""
    fixture_path = workspace_root / "tests" / "fixtures" / "question_bank" / "ambig_figure.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    q = GeneratedQuestion.model_validate(data)

    opinion = QuestionSolverOpinion(
        solver_id="solver_test",
        conversation_id="conv-ambig-4",
        independent_interpretation="Crossing wires lack junction dot; planar schematic is ambiguous between node vs bridge.",
        governing_principles=["Kirchhoff's Current Law"],
        independent_equations=["Node topology indeterminate"],
        independent_solution_steps=["Identified unlabelled crossing"],
        calculated_answer=["2.0", "4.0"],
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=False,
        conflicting_distractors=["B"],
        evaluated_difficulty=q.difficulty_dimensions,
        verdict="AMBIGUOUS",
        notes="Diagram lacks clear schematic node convention at wire crossing.",
    )

    errors = validate_answer_uniqueness_and_distractors(q, opinion)
    assert any("AMBIGUOUS_PROBLEM" in e for e in errors)

    rev_dir = tmp_path / "review"
    rev_path = route_to_review(q, "AMBIGUOUS_FIGURE_SCHEMATIC", {"errors": errors}, rev_dir)
    assert rev_path.exists()
    assert q.verification_status == QuestionQualityStatus.REVIEW


def test_ambiguity_gate_well_posed_promotable(workspace_root: Path, tmp_path: Path):
    """Well-posed question passes ambiguity check and is promotable."""
    fixture_path = workspace_root / "tests" / "fixtures" / "question_bank" / "well_posed_fixture.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    q = GeneratedQuestion.model_validate(data)

    opinion = QuestionSolverOpinion(
        solver_id="solver_test",
        conversation_id="conv-well-posed",
        independent_interpretation="Direct refraction at flat glass boundary using Snell's Law.",
        governing_principles=["Snell's Law of Refraction"],
        independent_equations=["n1 sin(theta1) = n2 sin(theta2)"],
        independent_solution_steps=["sin(theta2) = (1.0 * sin 30) / 1.5 = 0.5 / 1.5 = 1/3"],
        calculated_answer="A",
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=True,
        conflicting_distractors=[],
        evaluated_difficulty=q.difficulty_dimensions,
        verdict="VERIFIED",
        notes="Unambiguous problem with unique correct answer and strictly invalid distractors.",
    )

    errors = validate_answer_uniqueness_and_distractors(q, opinion)
    assert errors == []

    v_rec = QuestionVerificationRecord(
        verification_id="qvr-well-posed-test",
        question_id=q.question_id,
        content_hash=compute_question_hash(q),
        risk_level=QuestionRiskLevel.LOW,
        solver_a=opinion,
        solver_b=None,
        agreement=True,
        uniqueness_verified=True,
        distractors_validated=True,
        numerical_validated=True,
        final_answer="A",
        final_verdict=QuestionQualityStatus.VERIFIED,
        difficulty_calibrated=q.difficulty_dimensions,
    )
    assert bind_question_verification(q, v_rec) is True

    verif_dir = tmp_path / "verified"
    journal = tmp_path / "journal.jsonl"
    promoted = promote_question(q, verif_dir, journal)
    assert promoted.exists()


def test_ambiguous_question_cannot_be_promoted(sample_question: GeneratedQuestion, tmp_path: Path):
    """Deterministic gate rejects promotion of any question in AMBIGUOUS or REVIEW status."""
    sample_question.verification_status = QuestionQualityStatus.REVIEW
    with pytest.raises(ValueError, match="Cannot promote unverified question"):
        promote_question(sample_question, tmp_path / "verified", tmp_path / "journal.jsonl")


# ==============================================================================
# 12. Assessment Requirement Reconciliation & Matrix Tests
# ==============================================================================

def test_phase9_requirement_reconciliation_arithmetic(workspace_root: Path):
    """AssessmentRequirementReconciliationEngine proves exact arithmetic: 12 = 6 + 4 + 1 + 1."""
    from jee_physics.question_bank.reconciliation import (
        AssessmentRequirementReconciliationEngine,
        AssessmentRequirementStatus,
    )
    engine = AssessmentRequirementReconciliationEngine(workspace_root)
    report = engine.reconcile()

    assert report.total_assessment_requirements == 12
    assert report.satisfied_by_existing_count == 6
    assert report.satisfied_by_generated_count == 4
    assert report.unresolved_pilot_gap_count == 1
    assert report.not_in_pilot_scope_count == 1

    # Exact arithmetic proof
    total_sum = (
        report.satisfied_by_existing_count
        + report.satisfied_by_generated_count
        + report.unresolved_pilot_gap_count
        + report.not_in_pilot_scope_count
    )
    assert total_sum == report.total_assessment_requirements == 12

    # Check that individual statuses match
    existing_items = [r for r in report.requirements if r.status == AssessmentRequirementStatus.SATISFIED_BY_EXISTING]
    assert len(existing_items) == 6
    generated_items = [r for r in report.requirements if r.status == AssessmentRequirementStatus.SATISFIED_BY_GENERATED]
    assert len(generated_items) == 4
    unresolved_gap_items = [r for r in report.requirements if r.status == AssessmentRequirementStatus.UNRESOLVED_PILOT_GAP]
    assert len(unresolved_gap_items) == 1
    assert unresolved_gap_items[0].pilot_scope_classification == "IN_PILOT_SCOPE"
    assert unresolved_gap_items[0].unresolved_reason is not None

    scope_items = [r for r in report.requirements if r.status == AssessmentRequirementStatus.NOT_IN_PILOT_SCOPE]
    assert len(scope_items) == 1
    assert scope_items[0].pilot_scope_classification == "NOT_IN_PILOT_SCOPE"
    assert scope_items[0].unresolved_reason is not None


def test_phase9_question_requirement_matrix_all_valid(workspace_root: Path):
    """Question requirement matrix validates all mappings across taxonomy, curriculum, and provenance."""
    from jee_physics.question_bank.reconciliation import AssessmentRequirementReconciliationEngine
    engine = AssessmentRequirementReconciliationEngine(workspace_root)
    matrix = engine.generate_matrix()

    assert matrix.total_mappings_validated == 10
    assert matrix.all_mappings_valid is True
    for entry in matrix.entries:
        assert entry.question_exists is True
        assert entry.curriculum_id_valid is True
        assert entry.taxonomy_valid is True
        assert entry.verification_valid is True
        assert entry.provenance_exists is True
        assert entry.all_checks_passed is True


# ==============================================================================
# 13. Production Artifact vs Test Fixture Provenance Separation Tests
# ==============================================================================

def test_production_vs_fixture_provenance_separation(workspace_root: Path):
    """Controlled test fixtures carry explicit metadata and never leak into verified question bank."""
    fixtures_dir = workspace_root / "tests" / "fixtures" / "question_bank"
    verified_dir = workspace_root / "question_bank" / "verified"

    fixture_files = list(fixtures_dir.glob("*.json"))
    assert len(fixture_files) >= 5

    verified_qids = {p.stem for p in verified_dir.glob("*.json")}

    for ff in fixture_files:
        data = json.loads(ff.read_text(encoding="utf-8"))
        assert data.get("provenance_class") == "CONTROLLED_TEST_FIXTURE"
        qid = data.get("question_id")
        assert qid not in verified_qids, f"Test fixture leaked into verified question bank: {qid}"


# ==============================================================================
# 14. Post-Verification Mutation Invalidation Tests
# ==============================================================================

def test_post_verification_mutation_invalidates_binding(sample_question: GeneratedQuestion, tmp_path: Path):
    """Editing any parameter of a verified question invalidates its verification status."""
    orig_hash = compute_question_hash(sample_question)
    sample_question.verification_status = QuestionQualityStatus.VERIFIED
    sample_question.verification_record_id = "qvr-test-edit-01"

    # Mutate options
    sample_question.options["A"] = "$2 c / n$"
    mutated = invalidate_question_if_modified(sample_question, orig_hash)
    assert mutated is True
    assert sample_question.verification_status == QuestionQualityStatus.INVALIDATED
    assert sample_question.verification_record_id is None

    # Cannot promote
    with pytest.raises(ValueError, match="Cannot promote unverified question"):
        promote_question(sample_question, tmp_path / "verified", tmp_path / "journal.jsonl")


# ==============================================================================
# 15. Deduplication Cluster Persistence Tests
# ==============================================================================

def test_deduplication_cluster_persistence(workspace_root: Path):
    """gen-q-dup-test-01 is recorded in clusters/ and mappings/ and NOT in verified/."""
    clusters_dir = workspace_root / "question_bank" / "clusters"
    verified_dir = workspace_root / "question_bank" / "verified"

    cluster_files = list(clusters_dir.glob("*gen-q-dup-test-01*.json"))
    assert len(cluster_files) > 0, "Duplicate cluster was not persisted"

    # Must NOT be in verified
    assert not (verified_dir / "gen-q-dup-test-01.json").exists()


# ==============================================================================
# 16. Difficulty Calibration Discrepancy Auditing Tests
# ==============================================================================

def test_difficulty_calibration_audit(workspace_root: Path):
    """Verifies that difficulty ratings are preserved and calibrated."""
    staging_dir = workspace_root / "build" / "staging" / "incoming" / "question_bank" / "questions"
    solver_dir = workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verification" / "solver_a"

    calibrations = []
    for qf in staging_dir.glob("*.json"):
        q_data = json.loads(qf.read_text(encoding="utf-8"))
        op_file = solver_dir / f"opinion-{qf.name}"
        if op_file.exists():
            op_data = json.loads(op_file.read_text(encoding="utf-8"))
            gen_diff = q_data["difficulty_dimensions"]["conceptual_difficulty"]
            solv_diff = op_data["evaluated_difficulty"]["conceptual_difficulty"]
            calibrations.append({
                "question_id": qf.stem,
                "gen_diff": gen_diff,
                "solv_diff": solv_diff,
                "discrepancy": abs(gen_diff - solv_diff),
            })

    assert len(calibrations) > 0
    # All discrepancies must be reasonable (<= 2 levels)
    assert all(c["discrepancy"] <= 2 for c in calibrations)


# ==============================================================================
# 17. High-Risk Risk Classification Auditing Tests
# ==============================================================================

def test_high_risk_classification_auditing(workspace_root: Path):
    """Proves that all HIGH-risk questions received dual independent verification."""
    verif_records_dir = workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verification" / "records"
    records = []
    for rf in verif_records_dir.glob("*.json"):
        data = json.loads(rf.read_text(encoding="utf-8"))
        records.append(data)

    high_risk_records = [r for r in records if r.get("risk_level") == "HIGH"]
    assert len(high_risk_records) == 3, f"Expected 3 high-risk records, found {len(high_risk_records)}"

    for hr in high_risk_records:
        assert hr.get("solver_a") is not None
        assert hr.get("solver_b") is not None
        assert hr.get("agreement") is True
        assert hr.get("final_verdict") == "VERIFIED"


# ==============================================================================
# 18. Immutable Verifier Evidence Invariant Tests
# ==============================================================================

def test_immutable_verifier_evidence_invariant(workspace_root: Path):
    """Proves original opinion is preserved, modified record is SUPERSEDED, and fresh recheck governs."""
    import hashlib
    orig_path = workspace_root / "question_bank" / "audit" / "original_solver_opinions" / "opinion-gen-q-ambig-test-01_original.json"
    prov_path = workspace_root / "question_bank" / "audit" / "original_solver_opinions" / "opinion-gen-q-ambig-test-01_provenance.json"
    superseded_path = workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verification" / "solver_a" / "opinion-gen-q-ambig-test-01.json"
    recheck_path = workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verification" / "solver_a_recheck" / "opinion-gen-q-ambig-test-01.json"

    # 1. Original opinion preserved bit-for-bit
    assert orig_path.exists(), "Original Solver A opinion was not preserved in audit archive"
    orig_bytes = orig_path.read_bytes()
    orig_sha256 = hashlib.sha256(orig_bytes).hexdigest()
    assert orig_sha256 == "5bc58f69e6250bca50e9586d3cf255afc82db00c0a5a3550f76fb87e77237876"

    orig_data = json.loads(orig_bytes.decode("utf-8"))
    assert orig_data["verdict"] == "VERIFIED"
    assert orig_data["solver_id"] == "solver_a"
    assert orig_data["conversation_id"] == "c4b2f200-9d09-4009-8419-85baf0f75544"

    # 2. Provenance metadata valid
    assert prov_path.exists()
    prov_data = json.loads(prov_path.read_text(encoding="utf-8"))
    assert prov_data["original_file_sha256"] == orig_sha256
    assert prov_data["status"] == "PRESERVED_HISTORICAL_RECORD"

    # 3. Modified staging record is explicitly marked SUPERSEDED
    assert superseded_path.exists()
    sup_data = json.loads(superseded_path.read_text(encoding="utf-8"))
    assert sup_data.get("record_status") == "SUPERSEDED"
    assert "solver_a_recheck" in sup_data.get("superseded_by", "")

    # 4. Fresh recheck opinion was written by independent subagent
    assert recheck_path.exists()
    recheck_data = json.loads(recheck_path.read_text(encoding="utf-8"))
    assert recheck_data["solver_id"] == "solver_a_recheck"
    assert recheck_data["conversation_id"] == "9081bbf9-cc51-4fdd-aa86-9d98ec9b8f52"
    assert recheck_data["verdict"] == "AMBIGUOUS"
    assert recheck_data["uniqueness_confirmed"] is False


# ==============================================================================
# 19. Assessment Blueprint Integrity Tests
# ==============================================================================

def test_assessment_blueprint_integrity_audit(workspace_root: Path):
    """Proves mock exam paper references ONLY verified questions and zero review/duplicate items."""
    bp_path = workspace_root / "build" / "reports" / "assessment_blueprint_report.json"
    assert bp_path.exists()
    bp_report = json.loads(bp_path.read_text(encoding="utf-8"))

    assert bp_report.get("blueprint_valid") is True
    items = bp_report["assembled_paper"]["items"]
    assert len(items) == 5

    verified_dir = workspace_root / "question_bank" / "verified"
    review_dir = workspace_root / "review" / "queue" / "questions"
    clusters_dir = workspace_root / "question_bank" / "clusters"

    # Gather duplicate cluster members
    duplicate_qids = set()
    for cf in clusters_dir.glob("*.json"):
        c_data = json.loads(cf.read_text(encoding="utf-8"))
        for m in c_data.get("members", []):
            duplicate_qids.add(m.get("question_id"))

    for item in items:
        qid = item["question_id"]
        # Must exist in verified question bank
        assert (verified_dir / f"{qid}.json").exists(), f"Blueprint references unverified question: {qid}"
        # Must NOT exist in review queue
        assert not (review_dir / f"{qid}_review.json").exists(), f"Blueprint references question under review: {qid}"
        # Must NOT be duplicate cluster member
        assert qid not in duplicate_qids, f"Blueprint references duplicate cluster question: {qid}"
        # Marks and difficulty
        assert item["marks"] > 0
        assert item["difficulty_band"] in ("L1", "L2", "L3", "L4", "L5")


# ==============================================================================
# 20. Question Ladder Integrity Tests
# ==============================================================================

def test_question_ladder_integrity_audit(workspace_root: Path):
    """Proves question ladder rungs point ONLY to approved items and zero review/duplicate items."""
    ladder_path = workspace_root / "build" / "reports" / "question_ladder_report.json"
    assert ladder_path.exists()
    report = json.loads(ladder_path.read_text(encoding="utf-8"))

    assert report.get("valid") is True
    assert report.get("total_rungs") == 4

    kb_atoms_dir = workspace_root / "kb" / "atoms"
    verified_dir = workspace_root / "question_bank" / "verified"
    review_dir = workspace_root / "review" / "queue" / "questions"

    for rung in report["rungs"]:
        qid = rung["question_id"]
        # Question must exist in canonical atoms or verified question bank
        in_canonical = (kb_atoms_dir / f"{qid}.json").exists()
        in_verified = (verified_dir / f"{qid}.json").exists()
        assert in_canonical or in_verified, f"Ladder rung references non-existent question: {qid}"

        # Must not be under review
        assert not (review_dir / f"{qid}_review.json").exists(), f"Ladder rung references review question: {qid}"

        # Pedagogical progression metadata
        assert len(rung["cognitive_delta"]) > 10
        assert len(rung["pedagogical_purpose"]) > 10
        assert rung["cognitive_level"] in ("RECOGNITION", "DIRECT_APPLICATION", "MULTI_STEP", "CONCEPT_COMBINATION", "TRANSFER", "ADVANCED_SYNTHESIS")


# ==============================================================================
# 21. Review Queue and Verified Inventory Mutual Consistency Tests
# ==============================================================================

def test_review_queue_and_verified_inventory_integrity(workspace_root: Path):
    """Proves review queue contains all failed items with typed gate reasons and zero verified overlap."""
    review_dir = workspace_root / "review" / "queue" / "questions"
    verified_dir = workspace_root / "question_bank" / "verified"

    review_files = list(review_dir.glob("*_review.json"))
    assert len(review_files) == 3, f"Expected 3 review queue files, found {len(review_files)}"

    verified_qids = {p.stem for p in verified_dir.glob("*.json")}
    expected_review_qids = {"gen-q-ambig-test-01", "gen-q-dist-conflict-01", "gen-q-wrong-ans-01"}
    actual_review_qids = set()

    for rf in review_files:
        data = json.loads(rf.read_text(encoding="utf-8"))
        qid = data["question_id"]
        actual_review_qids.add(qid)

        # Schema fields required by Section 14
        assert "question_id" in data
        assert "review_reason" in data
        assert "failed_gate" in data
        assert "relevant_verification_opinions" in data
        assert "provenance" in data
        assert data["current_status"] == "REVIEW"

        # Mutually exclusive: cannot be verified
        assert qid not in verified_qids, f"Reviewed question {qid} also found in verified question bank!"

    assert actual_review_qids == expected_review_qids


# ==============================================================================
# 22. End-to-End Ambiguity Gate Fixture Processing Tests
# ==============================================================================

def test_end_to_end_ambiguity_gate_fixture_execution(workspace_root: Path, tmp_path: Path):
    """Processes a controlled ambiguity fixture end-to-end through solver opinion to review routing."""
    fixture_path = workspace_root / "tests" / "fixtures" / "question_bank" / "ambig_missing_info.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    q = GeneratedQuestion.model_validate(data)

    # Simulate independent solver deriving AMBIGUOUS from first principles
    solver_opinion = QuestionSolverOpinion(
        solver_id="fresh_test_solver",
        conversation_id="conv-e2e-ambig-test",
        independent_interpretation="First law dU = dQ - dW requires heat exchange dQ and thermodynamic process equation, both omitted.",
        governing_principles=["First Law of Thermodynamics: dU = dQ - dW"],
        independent_equations=["dU = dQ - P dV (indeterminate without dQ and path)"],
        independent_solution_steps=["Identified unstated thermodynamic process path"],
        calculated_answer="INDETERMINATE",
        dimensional_check_passed=True,
        numerical_check_passed=True,
        uniqueness_confirmed=False,
        conflicting_distractors=[],
        evaluated_difficulty=q.difficulty_dimensions,
        verdict="AMBIGUOUS",
        notes="Physical problem lacks necessary thermodynamic path and heat exchange data.",
    )

    # 1. Gate validates uniqueness and distractors
    errors = validate_answer_uniqueness_and_distractors(q, solver_opinion)
    assert any("AMBIGUOUS_PROBLEM" in e for e in errors)

    # 2. Gate routes to review
    rev_dir = tmp_path / "review"
    rev_path = route_to_review(
        question=q,
        reason="PHYSICAL_AMBIGUITY_UNDERSPECIFIED",
        details={
            "failed_gate": "AMBIGUITY_GATE",
            "solver_opinion": solver_opinion.model_dump(),
            "distractor_errors": errors,
        },
        review_queue_dir=rev_dir,
    )
    assert rev_path.exists()
    assert q.verification_status == QuestionQualityStatus.REVIEW

    rev_data = json.loads(rev_path.read_text(encoding="utf-8"))
    assert rev_data["failed_gate"] == "AMBIGUITY_GATE"
    assert rev_data["current_status"] == "REVIEW"

    # 3. Deterministic gate blocks promotion
    with pytest.raises(ValueError, match="Cannot promote unverified question"):
        promote_question(q, tmp_path / "verified", tmp_path / "journal.jsonl")

