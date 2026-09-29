from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator

from jee_physics.models.enums import AtomStatus, AtomType, DifficultyLevel
from jee_physics.models.provenance import ProvenanceRecord


class TaxonomyReference(BaseModel):
    """Hierarchical positioning in the official JEE syllabus."""
    chapter_id: str = Field(..., min_length=1, description="Normalized chapter slug, e.g., 'kinematics'")
    topic_id: str = Field(..., min_length=1, description="Topic slug, e.g., 'projectile-motion'")
    subtopic_id: Optional[str] = Field(None, description="Optional subtopic slug, e.g., 'motion-on-incline'")


class QuestionOption(BaseModel):
    id: str = Field(..., description="Option identifier (A, B, C, D, etc.)")
    text: str = Field(..., description="Option text, preserving LaTeX notation")


class SolutionMethod(BaseModel):
    method_name: str = Field("Standard Method", description="e.g. 'Energy Method', 'Newton's Laws', 'Rotated Axes'")
    steps: str = Field(..., description="Step-by-step derivation or reasoning")
    source_attributed: bool = Field(True, description="True if this method appeared in the source text")


class ExamMetadata(BaseModel):
    exam: Optional[str] = Field(None, description="e.g. 'JEE Advanced', 'JEE Main', 'AIEEE'")
    exam_name: Optional[str] = Field(None, description="Alias for exam name")
    year: Optional[int] = Field(None, ge=1960, le=2050, description="Examination year")
    paper: Optional[Any] = Field(None, description="Paper number (e.g. 1 or 2)")
    question_number: Optional[str] = Field(None, description="Question number in that examination paper")

    @model_validator(mode="before")
    @classmethod
    def handle_metadata_compatibility(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "exam_name" in data and not data.get("exam"):
                data["exam"] = data["exam_name"]
            if "exam" in data and not data.get("exam_name"):
                data["exam_name"] = data["exam"]
            if "paper" in data and isinstance(data["paper"], str):
                import re
                m = re.search(r"\d+", data["paper"])
                if m:
                    data["paper"] = int(m.group(0))
            if "question_number" in data and data["question_number"] is not None:
                data["question_number"] = str(data["question_number"])
        return data


class QuestionPayload(BaseModel):
    statement: str = Field(..., min_length=1, description="Complete problem statement with LaTeX math")
    options: List[QuestionOption] = Field(default_factory=list, description="Multiple choice options if present")
    source_claimed_answer: Optional[str] = Field(None, description="Observed source-claimed answer key (e.g. 'A' or '4.2')")
    verified_answer: Optional[str] = Field(None, description="Independently verified correct answer")
    source_solution: Optional[str] = Field(None, description="Observed source-provided solution or derivation")
    answer: Optional[str] = Field(None, description="Legacy/compatibility answer field")
    solution_methods: List[SolutionMethod] = Field(default_factory=list, description="All preserved solution methods")
    difficulty: DifficultyLevel = Field(..., description="Difficulty rating L1 through L5")
    exam_metadata: Optional[ExamMetadata] = Field(None, description="Exam year/paper info if known")
    concepts: List[str] = Field(default_factory=list, description="Core physical concepts required")

    @model_validator(mode="before")
    @classmethod
    def handle_answer_compatibility(cls, data: Any) -> Any:
        if isinstance(data, dict):
            opts = data.get("options")
            if isinstance(opts, dict):
                data["options"] = [{"id": k, "text": str(v)} for k, v in opts.items()]
            ans = data.get("answer")
            if ans is not None and data.get("source_claimed_answer") is None:
                data["source_claimed_answer"] = ans
            if data.get("answer") is None:
                data["answer"] = data.get("verified_answer") or data.get("source_claimed_answer")
        return data


class FormulaPayload(BaseModel):
    formula_latex: str = Field(..., min_length=1, description="LaTeX representation of formula")
    variables: Dict[str, str] = Field(default_factory=dict, description="Mapping of variable symbol to physical meaning")
    units: Dict[str, str] = Field(default_factory=dict, description="SI units for variables")
    validity_conditions: Optional[str] = Field(None, description="Physical bounds (e.g. constant acceleration)")
    physical_meaning: Optional[str] = Field(None, description="Pedagogical meaning of the equation")


class SolvedExamplePayload(BaseModel):
    problem_statement: str = Field(..., min_length=1)
    solution_steps: List[SolutionMethod] = Field(default_factory=list)
    difficulty: DifficultyLevel = Field(DifficultyLevel.L2)
    concepts: List[str] = Field(default_factory=list)
    key_takeaway: Optional[str] = Field(None)


class MisconceptionPayload(BaseModel):
    flawed_statement: str = Field(..., description="The common erroneous statement or intuition")
    why_tempting: str = Field(..., description="Why students fall into this misconception")
    correct_physical_insight: str = Field(..., description="The scientifically correct physical reasoning")
    counter_example: Optional[str] = Field(None, description="A scenario highlighting the contradiction")


class FigureReference(BaseModel):
    figure_id: str = Field(..., description="Unique figure identifier linking to sources/figures/")
    caption: Optional[str] = Field(None, description="Original or generated caption")
    alt_text: Optional[str] = Field(None, description="Descriptive alt text for diagram accessibility")


class KnowledgeAtom(BaseModel):
    """The canonical atomic unit of physics knowledge."""
    atom_id: str = Field(..., min_length=1, description="Deterministic permanent atom ID")
    schema_version: str = Field("1.0.0", description="Schema version of this record")
    atom_version: int = Field(1, ge=1, description="Sequential version count for updates")
    active: bool = Field(True, description="False if superseded by a newer version or decommissioned")
    atom_type: AtomType = Field(..., description="Classification: theory, formula, question, etc.")
    title: str = Field(..., min_length=1, description="Concise descriptive title of the atom")
    taxonomy: TaxonomyReference = Field(..., description="Placement within the JEE syllabus tree")
    provenance: List[ProvenanceRecord] = Field(..., min_length=1, description="List of source occurrences")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of extraction/adjudication")
    verification_status: AtomStatus = Field(AtomStatus.STAGED, description="Lifecycle status")
    content_hash: str = Field(..., min_length=16, description="SHA-256 fingerprint of the core content")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Type-specific payloads
    content: Optional[str] = Field(None, description="Text body for theory, insight, or general note")
    formula: Optional[FormulaPayload] = Field(None, description="Payload for formula atoms")
    question: Optional[QuestionPayload] = Field(None, description="Payload for question atoms")
    solved_example: Optional[SolvedExamplePayload] = Field(None, description="Payload for solved examples")
    misconception: Optional[MisconceptionPayload] = Field(None, description="Payload for misconceptions")
    figure_refs: List[FigureReference] = Field(default_factory=list, description="Associated figures")
    insight: Optional[str] = Field(None, description="'What does this mean physically?' intuition")
    duplicate_group_id: Optional[str] = Field(None, description="Cluster ID if part of an equivalence group")
    archive_reason: Optional[str] = Field(None, description="Documented reason if routed to kb/archive/")

    @model_validator(mode="after")
    def validate_type_payloads(self) -> "KnowledgeAtom":
        if self.atom_type == AtomType.QUESTION and self.question is None:
            raise ValueError("question payload must be provided when atom_type is 'question'")
        if self.atom_type == AtomType.FORMULA and self.formula is None:
            raise ValueError("formula payload must be provided when atom_type is 'formula'")
        if self.atom_type == AtomType.THEORY and not self.content:
            raise ValueError("content must be provided when atom_type is 'theory'")
        if self.atom_type == AtomType.SOLVED_EXAMPLE and self.solved_example is None:
            raise ValueError("solved_example payload must be provided when atom_type is 'solved_example'")
        if self.atom_type == AtomType.MISCONCEPTION and self.misconception is None:
            raise ValueError("misconception payload must be provided when atom_type is 'misconception'")
        return self
