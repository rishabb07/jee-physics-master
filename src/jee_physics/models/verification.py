from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator

from jee_physics.models.atom import ExamMetadata, FigureReference, QuestionOption
from jee_physics.models.enums import DifficultyLevel, VerificationVerdict

PROHIBITED_SOLVER_FIELDS = {
    "source_claimed_answer",
    "source_solution",
    "verified_answer",
    "verdict",
    "adjudication_result",
    "promoted",
    "promotion_status",
    "consensus_answer",
}


class SolverRun(BaseModel):
    """Structured output representing an independent physics solver run."""
    solver_run_id: str = Field(..., description="Unique ID for this solver execution run")
    atom_id: str = Field(..., description="Target atom ID")
    solver_id: str = Field("solver_a", description="Identifier of the solver agent (e.g. 'solver_a', 'solver_b')")
    solver_agent_name: str = Field("solver_a", description="Canonical name of the solver agent")
    atom_version: int = Field(1, ge=1, description="Version of the staged atom")
    content_hash: Optional[str] = Field(None, description="Content hash of the staged atom")
    verification_protocol_version: str = Field("1.0.0", description="Version of the verification protocol")
    blind_package_hash: Optional[str] = Field(None, description="Deterministic hash of the blind problem package")
    model_name: Optional[str] = Field(None, description="Name/version of the AI model used")
    independent_answer: Optional[str] = Field(None, description="Independent answer extracted (option ID or numerical string)")
    raw_answer: Optional[str] = Field(None, description="Unnormalized raw answer emitted by the solver")
    reasoning_steps: List[str] = Field(default_factory=list, description="Step-by-step physical and mathematical derivation")
    assumptions_used: List[str] = Field(default_factory=list, description="Physical assumptions made during derivation")
    uncertainty: Optional[str] = Field(None, description="Declared uncertainty or confidence qualification")
    diagram_interpretation: Optional[str] = Field(None, description="How the solver understood any included diagrams")
    possible_ambiguities: List[str] = Field(default_factory=list, description="Ambiguities or underspecified parts identified")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_response: Optional[str] = Field(None, description="Full raw response text from the solver")

    @model_validator(mode="before")
    @classmethod
    def validate_solver_contract(cls, values: Any) -> Any:
        if isinstance(values, dict):
            # Check for prohibited fields
            for forbidden in PROHIBITED_SOLVER_FIELDS:
                if forbidden in values and values[forbidden] is not None:
                    raise ValueError(
                        f"Prohibited field '{forbidden}' found in solver output. "
                        f"Solvers must never emit source claims, verified answers, or verdicts."
                    )
            # Synchronize solver_id and solver_agent_name
            if "solver_agent_name" in values and "solver_id" not in values:
                values["solver_id"] = values["solver_agent_name"]
            elif "solver_id" in values and "solver_agent_name" not in values:
                values["solver_agent_name"] = values["solver_id"]
        return values


class AdjudicationRecord(BaseModel):
    """Structured decision by the adjudication agent reconciling solver runs and source claims."""
    adjudication_id: str = Field(..., description="Unique ID for this adjudication decision")
    atom_id: str = Field(..., description="Target atom ID")
    atom_version: int = Field(1, ge=1, description="Version of the target atom")
    content_hash: Optional[str] = Field(None, description="Content hash of the target atom")
    adjudicator_id: str = Field("physics-adjudicator", description="Identity of the adjudicator")
    solver_analyses: Dict[str, str] = Field(default_factory=dict, description="Critique of each solver run's validity")
    source_claim_analysis: str = Field(..., description="Evaluation of source-claimed answer correctness")
    physical_reasoning: str = Field(..., description="Rigorous physical justification for the final verdict")
    adjudicated_answer: Optional[str] = Field(None, description="Final adjudicated correct answer")
    verdict: VerificationVerdict = Field(..., description="Adjudicated verdict")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the adjudication decision")
    notes: Optional[str] = Field(None, description="Additional context or caveats")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class VerificationRecord(BaseModel):
    """Authoritative auditable verification record for a Knowledge Atom."""
    verification_id: str = Field(..., description="Unique verification record ID")
    atom_id: str = Field(..., description="Target atom ID")
    source_id: str = Field(..., description="Original registered source ID")
    atom_version: int = Field(1, ge=1, description="Version of the atom that was verified")
    content_hash: str = Field(..., min_length=16, description="Content hash of the atom at time of verification")
    verification_protocol_version: str = Field("1.0.0", description="Version of the verification protocol applied")
    solver_run_ids: List[str] = Field(default_factory=list, description="List of solver_run_id instances used")
    source_claimed_answer: Optional[str] = Field(None, description="Observed answer key in source, if present")
    source_solution: Optional[str] = Field(None, description="Observed source-provided solution, if present")
    independent_answers: Dict[str, Optional[str]] = Field(default_factory=dict, description="Map of solver_id -> answer")
    independent_solutions: Dict[str, str] = Field(default_factory=dict, description="Map of solver_id -> solution summary")
    consensus_answer: Optional[str] = Field(None, description="Consensus answer if solvers agreed or adjudicated")
    verdict: VerificationVerdict = Field(..., description="Final verification verdict")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall verification confidence score")
    discrepancy_classification: Optional[str] = Field(None, description="Classification of disagreement if any")
    adjudication_result: Optional[AdjudicationRecord] = Field(None, description="Adjudication record if adjudication occurred")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(None, description="When verification concluded")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional runtime or agent metadata")


class BlindSolverPackage(BaseModel):
    """Sanitized, solver-visible package that strictly isolates problem data from source answers."""
    package_id: str = Field(..., description="Unique package ID")
    atom_id: str = Field(..., description="Target atom ID")
    atom_version: int = Field(1, ge=1, description="Version of the staged atom")
    content_hash: Optional[str] = Field(None, description="Content hash of the question atom")
    blind_package_hash: Optional[str] = Field(None, description="Deterministic hash of the package contents")
    statement: str = Field(..., min_length=1, description="Problem statement with LaTeX math")
    options: List[QuestionOption] = Field(default_factory=list, description="List of multiple-choice options")
    figure_refs: List[FigureReference] = Field(default_factory=list, description="Diagram references and captions")
    difficulty: DifficultyLevel = Field(DifficultyLevel.L2, description="Difficulty level")
    concepts: List[str] = Field(default_factory=list, description="Associated concepts")
    exam_metadata: Optional[ExamMetadata] = Field(None, description="Sanitized exam year/paper info")
    context_notes: Optional[str] = Field(None, description="Physical units or context explicitly permitted")


class PromotionEvent(BaseModel):
    """Audit log record for canonical promotion from staging to kb/atoms/."""
    promotion_id: str = Field(..., description="Unique promotion event identifier")
    atom_id: str = Field(..., description="Canonical atom ID promoted")
    verification_id: str = Field(..., description="Associated verification record ID")
    source_id: str = Field(..., description="Source ID of the atom")
    atom_version: int = Field(..., ge=1, description="Version of the promoted atom")
    staged_path: str = Field(..., description="Source path in build/staging/atoms/")
    canonical_path: str = Field(..., description="Destination path in kb/atoms/")
    verdict: VerificationVerdict = Field(..., description="Verdict under which atom was promoted")
    source_claimed_answer: Optional[str] = Field(None, description="Preserved source claim")
    verified_answer: Optional[str] = Field(None, description="Verified answer written to canonical atom")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    promoted_by: str = Field("promotion_gate", description="Component or agent that authorized promotion")
