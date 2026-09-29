"""Question Bank module for JEE Physics Master Knowledge System."""

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
from jee_physics.question_bank.reconciliation import (
    AssessmentRequirementReconciliationEngine,
    AssessmentRequirementStatus,
    QuestionRequirementMatrixReport,
    RequirementReconciliationReport,
)
from jee_physics.question_bank.requirements import QuestionRequirementsEngine

__all__ = [
    "AssessmentBuilder",
    "QuestionDedupAdapter",
    "QuestionDependencyGraphBuilder",
    "QuestionLadderBuilder",
    "QuestionNumericalValidator",
    "QuestionRequirementsEngine",
    "AssessmentRequirementReconciliationEngine",
    "AssessmentRequirementStatus",
    "RequirementReconciliationReport",
    "QuestionRequirementMatrixReport",
    "compute_question_hash",
    "validate_question_schema_and_curriculum",
    "validate_answer_uniqueness_and_distractors",
    "bind_question_verification",
    "invalidate_question_if_modified",
    "route_to_review",
    "promote_question",
]
