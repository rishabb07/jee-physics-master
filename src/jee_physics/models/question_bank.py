"""Pydantic models for Phase 9 Question Bank & Assessment Generation.

Defines typed schemas for generated questions, distractor rationales,
diagram references, source grounding, independent verification records,
assessment blueprints, and question ladders.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, model_validator

from jee_physics.models.atom import TaxonomyReference
from jee_physics.models.curriculum import DifficultyDimensions, ExamTargetLevel
from jee_physics.models.enums import DifficultyLevel


class QuestionOrigin(str, Enum):
    """Origin of a question in the knowledge system."""
    GENERATED = "GENERATED"                    # Genuinely novel generated problem
    SOURCE_DERIVATIVE = "SOURCE_DERIVATIVE"    # Systematically transformed from source atom
    CANONICAL_ADAPTATION = "CANONICAL_ADAPTATION" # Direct pedagogical adaptation of canonical atom
    CANONICAL_KB = "CANONICAL_KB"              # Historical source question in kb/atoms/


class QuestionType(str, Enum):
    """Pedagogical format of the question."""
    SINGLE_CORRECT_MCQ = "SINGLE_CORRECT_MCQ"
    MULTIPLE_CORRECT_MCQ = "MULTIPLE_CORRECT_MCQ"
    NUMERICAL = "NUMERICAL"
    ASSERTION_REASONING = "ASSERTION_REASONING"
    CONCEPTUAL_QUALITATIVE = "CONCEPTUAL_QUALITATIVE"
    MULTI_STEP_STRUCTURED = "MULTI_STEP_STRUCTURED"


class QuestionQualityStatus(str, Enum):
    """Lifecycle quality states for questions."""
    GENERATED = "GENERATED"
    STAGED = "STAGED"
    SOLVED_INDEPENDENTLY = "SOLVED_INDEPENDENTLY"
    VERIFIED = "VERIFIED"
    PROMOTABLE = "PROMOTABLE"
    REJECTED = "REJECTED"
    CONFLICT = "CONFLICT"
    AMBIGUOUS = "AMBIGUOUS"
    REVIEW = "REVIEW"
    DUPLICATE = "DUPLICATE"
    INVALIDATED = "INVALIDATED"


class QuestionRiskLevel(str, Enum):
    """Risk classification requiring calibrated verification rigor."""
    LOW = "LOW"          # Simple recall or single-step formula substitution
    MEDIUM = "MEDIUM"    # Standard two-step calculation or direct conceptual question
    HIGH = "HIGH"        # Multi-concept, multiple-correct, subtle signs, novel diagrams


class CognitiveLadderLevel(str, Enum):
    """Cognitive demand level for Question Ladders."""
    RECOGNITION = "RECOGNITION"
    DIRECT_APPLICATION = "DIRECT_APPLICATION"
    MULTI_STEP = "MULTI_STEP"
    CONCEPT_COMBINATION = "CONCEPT_COMBINATION"
    TRANSFER = "TRANSFER"
    ADVANCED_SYNTHESIS = "ADVANCED_SYNTHESIS"


class DistractorRationale(BaseModel):
    """Pedagogical diagnosis of an incorrect multiple-choice option."""
    option_key: str = Field(..., description="Option letter, e.g. 'A', 'B'")
    distractor_value: str = Field(..., description="The option's rendered text or numerical value")
    likely_misconception: str = Field(..., description="Cognitive pitfall leading to this option")
    student_rationale: str = Field(..., description="Why a student might arrive at this option")
    physical_error: str = Field(..., description="Physical or mathematical justification for why it is wrong")
    error_category: str = Field(..., description="Category: SIGN_MISTAKE, WRONG_CONSERVATION_LAW, etc.")


class DiagramReference(BaseModel):
    """Explicit diagram specification with topological and entity bindings."""
    figure_id: str = Field(..., min_length=1, description="Unique figure identifier")
    description: str = Field(..., min_length=5, description="Physical and geometric description")
    referenced_entities: List[str] = Field(default_factory=list, description="Entities shown in diagram")
    labels: Dict[str, str] = Field(default_factory=dict, description="Label-to-meaning mapping")
    geometry_consistent: bool = Field(True, description="Geometric consistency confirmed")
    figure_hash: Optional[str] = Field(None, description="SHA-256 hash of image file if rendered")


class SourceGrounding(BaseModel):
    """Relationship to canonical source questions in kb/atoms/."""
    relationship_type: str = Field(
        ...,
        description="'NEW_PROBLEM' | 'SEMANTIC_VARIANT' | 'SOURCE_DERIVATIVE'"
    )
    source_atom_id: Optional[str] = Field(None, description="Referenced canonical atom ID if derivative")
    transformation_type: Optional[str] = Field(
        None,
        description="e.g. PARAMETER_VARIATION, GEOMETRY_INVERSION, TARGET_SWAP"
    )
    what_changed: Optional[str] = Field(None, description="Exact delta from the source atom")
    why_pedagogically_distinct: Optional[str] = Field(None, description="Educational justification")


class GeneratedQuestion(BaseModel):
    """First-class typed model for generated physics questions."""
    question_id: str = Field(..., min_length=1, description="Unique question identifier")
    version: int = Field(1, ge=1, description="Question version")
    origin: QuestionOrigin = Field(QuestionOrigin.GENERATED, description="Origin classification")
    curriculum_id: str = Field(..., min_length=1, description="Mapped curriculum node ID")
    taxonomy_reference: TaxonomyReference = Field(..., description="Authoritative taxonomy mapping")
    concept_references: List[str] = Field(..., min_length=1, description="Referenced concept IDs")
    prerequisite_references: List[str] = Field(default_factory=list, description="Prerequisite curriculum node IDs")
    target_exam_level: ExamTargetLevel = Field(..., description="JEE_MAIN | JEE_ADVANCED | OLYMPIAD_EXTENSION")
    question_type: QuestionType = Field(..., description="MCQ, Numerical, etc.")
    statement: str = Field(..., min_length=10, description="Complete problem statement in KaTeX LaTeX")
    diagram_references: List[DiagramReference] = Field(default_factory=list, description="Diagram references")
    options: Dict[str, str] = Field(default_factory=dict, description="Options dictionary for MCQs")
    correct_answer: Union[str, List[str]] = Field(..., description="Correct answer option(s) or numerical value")
    solution_strategy: str = Field(..., min_length=5, description="High-level pedagogical strategy")
    solution: str = Field(..., min_length=10, description="Step-by-step rigorous solution")
    assumptions: List[str] = Field(default_factory=list, description="Physical idealizations and assumptions")
    numerical_values: Dict[str, Any] = Field(default_factory=dict, description="Numerical parameter values")
    units: Optional[str] = Field(None, description="SI units of target quantity if numerical")
    tolerance: Optional[float] = Field(None, description="Acceptable numerical relative tolerance, e.g. 0.02")
    intended_learning_objective: str = Field(..., min_length=5, description="Target skill evaluated")
    difficulty_dimensions: DifficultyDimensions = Field(..., description="6D difficulty rating")
    difficulty_band: DifficultyLevel = Field(..., description="Derived L1-L5 band")
    misconception_targeted: Optional[str] = Field(None, description="Mapped misconception ID if applicable")
    distractor_rationales: List[DistractorRationale] = Field(default_factory=list, description="Rationales for all distractors")
    source_grounding: SourceGrounding = Field(..., description="Grounding relationship to canonical atoms")
    risk_level: QuestionRiskLevel = Field(QuestionRiskLevel.MEDIUM, description="Risk level")
    generation_metadata: Dict[str, Any] = Field(default_factory=dict, description="Authoring agent metadata")
    content_hash: Optional[str] = Field(None, description="Substantive SHA-256 hash")
    verification_status: QuestionQualityStatus = Field(QuestionQualityStatus.GENERATED)
    verification_record_id: Optional[str] = Field(None, description="Bound verification record ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def validate_mcq_options(self) -> "GeneratedQuestion":
        if self.question_type in (QuestionType.SINGLE_CORRECT_MCQ, QuestionType.MULTIPLE_CORRECT_MCQ):
            if not self.options:
                raise ValueError(f"MCQ question {self.question_id} must have options dictionary")
            if isinstance(self.correct_answer, str):
                if self.question_type == QuestionType.SINGLE_CORRECT_MCQ and self.correct_answer not in self.options:
                    raise ValueError(f"Correct answer '{self.correct_answer}' not in options keys: {list(self.options.keys())}")
            elif isinstance(self.correct_answer, list):
                for ans in self.correct_answer:
                    if ans not in self.options:
                        raise ValueError(f"Correct answer '{ans}' not in options keys: {list(self.options.keys())}")
        return self


class QuestionSolverOpinion(BaseModel):
    """An independent solver agent's first-principles solution to a question."""
    solver_id: str = Field(..., min_length=1, description="Solver agent name")
    conversation_id: str = Field(..., min_length=1, description="Solver conversation ID")
    independent_interpretation: str = Field(..., min_length=5, description="Independent reading of problem")
    governing_principles: List[str] = Field(..., min_length=1, description="Governing physical laws")
    independent_equations: List[str] = Field(..., min_length=1, description="Equations set up independently")
    independent_solution_steps: List[str] = Field(..., min_length=1, description="Step-by-step derivation")
    calculated_answer: Union[str, List[str]] = Field(..., description="Independent calculated answer")
    dimensional_check_passed: bool = Field(..., description="Whether dimensional homogeneity holds")
    numerical_check_passed: bool = Field(..., description="Whether arithmetic calculations hold")
    uniqueness_confirmed: bool = Field(..., description="Whether answer is unique (no other valid option)")
    conflicting_distractors: List[str] = Field(default_factory=list, description="Any options that are also physically valid")
    evaluated_difficulty: DifficultyDimensions = Field(..., description="Independent difficulty assessment")
    verdict: str = Field(..., description="'VERIFIED' | 'REJECTED' | 'AMBIGUOUS' | 'CONFLICT'")
    notes: Optional[str] = Field(None, description="Verification notes")
    record_status: str = Field("ACTIVE", description="'ACTIVE' | 'SUPERSEDED' | 'CORRECTED_RECORD'")
    superseded_by: Optional[str] = Field(None, description="Replacement solver opinion path or ID if superseded")
    superseded_reason: Optional[str] = Field(None, description="Reason why this record was superseded")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionVerificationRecord(BaseModel):
    """Immutable verification record for a generated question."""
    verification_id: str = Field(..., min_length=1, description="Unique verification record ID")
    question_id: str = Field(..., min_length=1, description="Target question ID")
    question_version: int = Field(1, ge=1, description="Question version")
    content_hash: str = Field(..., min_length=8, description="Substantive SHA-256 hash of question")
    risk_level: QuestionRiskLevel = Field(..., description="Risk level")
    solver_a: QuestionSolverOpinion = Field(..., description="Primary independent solver")
    solver_b: Optional[QuestionSolverOpinion] = Field(None, description="Secondary independent solver for HIGH-risk")
    agreement: bool = Field(True, description="Whether solvers agree on answer and validity")
    uniqueness_verified: bool = Field(True, description="Uniqueness of answer verified")
    distractors_validated: bool = Field(True, description="All distractors verified strictly invalid")
    numerical_validated: bool = Field(True, description="Numerical computation validated")
    final_answer: Union[str, List[str]] = Field(..., description="Consensus verified answer")
    final_verdict: QuestionQualityStatus = Field(QuestionQualityStatus.VERIFIED)
    difficulty_calibrated: DifficultyDimensions = Field(..., description="Consensus difficulty rating")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AssessmentSectionBlueprint(BaseModel):
    """Section structure within an assessment paper blueprint."""
    section_name: str = Field(..., description="e.g. 'Section A - Single Choice'")
    question_type: QuestionType = Field(..., description="Question format")
    question_count: int = Field(..., ge=1, description="Number of questions in section")
    marks_per_question: float = Field(..., gt=0, description="Marks for full correct answer")
    negative_marks: float = Field(0.0, le=0, description="Negative marks for wrong answer (negative or 0)")
    partial_marking: bool = Field(False, description="Whether partial marks apply")
    difficulty_target: Dict[str, int] = Field(default_factory=dict, description="Target counts per difficulty L1-L5")


class AssessmentBlueprint(BaseModel):
    """First-class specification for full exam mock paper generation."""
    assessment_id: str = Field(..., min_length=1, description="Unique blueprint ID")
    title: str = Field(..., min_length=1, description="Title of mock exam")
    target_exam: ExamTargetLevel = Field(..., description="JEE_MAIN | JEE_ADVANCED")
    total_time_minutes: int = Field(..., ge=30, description="Time limit in minutes")
    total_marks: float = Field(..., gt=0, description="Total maximum score")
    sections: List[AssessmentSectionBlueprint] = Field(..., min_length=1, description="Ordered sections")
    chapter_coverage_weights: Dict[str, float] = Field(..., description="Target weight per chapter")
    prerequisite_coverage: List[str] = Field(default_factory=list, description="Required prerequisite syllabus nodes")
    target_skills: List[str] = Field(default_factory=list, description="Target problem-solving skills")
    scoring_rules: Dict[str, Any] = Field(default_factory=dict, description="Detailed scoring rules")
    negative_marking_rules: Dict[str, Any] = Field(default_factory=dict, description="Negative marking rules")
    exclusions: List[str] = Field(default_factory=list, description="Explicit topic exclusions")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionLadderRung(BaseModel):
    """An individual progressive rung in a question ladder."""
    rung_number: int = Field(..., ge=1, description="1-indexed sequence")
    cognitive_level: CognitiveLadderLevel = Field(..., description="Target cognitive level")
    question_id: str = Field(..., min_length=1, description="Question ID mapped to this rung")
    prerequisite_rungs: List[int] = Field(default_factory=list, description="Prerequisite rung numbers")
    cognitive_delta: str = Field(..., min_length=5, description="What additional skill is demanded vs prior rung")
    pedagogical_purpose: str = Field(..., min_length=5, description="Role in student scaffolding")


class QuestionLadder(BaseModel):
    """A progressive cognitive sequence of questions."""
    ladder_id: str = Field(..., min_length=1, description="Unique ladder ID")
    chapter_id: str = Field(..., min_length=1, description="Parent chapter slug")
    topic_id: str = Field(..., min_length=1, description="Parent topic slug")
    title: str = Field(..., min_length=1, description="Title of the ladder")
    rungs: List[QuestionLadderRung] = Field(..., min_length=2, description="Progressive rungs")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
