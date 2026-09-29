from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, model_validator

from jee_physics.models.enums import AtomStatus, DifficultyLevel
from jee_physics.models.atom import TaxonomyReference, SolutionMethod
from jee_physics.models.provenance import ProvenanceRecord


class PedagogicalRole(str, Enum):
    """The learning and narrative role of a curriculum element."""
    FOUNDATION_CONCEPT = "FOUNDATION_CONCEPT"          # Introductory concept / physical intuition
    CORE_PRINCIPLE = "CORE_PRINCIPLE"                  # Fundamental physical law or governing theorem
    DERIVATION = "DERIVATION"                          # Mathematical derivation from first principles
    WORKED_EXAMPLE = "WORKED_EXAMPLE"                  # Fully resolved pedagogical example
    QUESTION_LADDER = "QUESTION_LADDER"                # Progressive scaffolding sequence
    PRACTICE_QUESTION = "PRACTICE_QUESTION"            # Targeted exercise question
    ADVANCED_SYNTHESIS = "ADVANCED_SYNTHESIS"          # Multi-concept Olympiad / JEE Advanced synthesis
    COMMON_MISCONCEPTION = "COMMON_MISCONCEPTION"      # Pitfall analysis and warning callout
    REVISION_SUMMARY = "REVISION_SUMMARY"              # Rapid review checklist and formula link
    HISTORICAL_NOTE = "HISTORICAL_NOTE"                # Historical or physical context
    INTUITION_BUILDER = "INTUITION_BUILDER"            # Physical thought experiment or qualitative reasoning


class CurriculumNodeType(str, Enum):
    """Granular level of an element in the pedagogical curriculum hierarchy."""
    SUBJECT = "SUBJECT"
    CHAPTER = "CHAPTER"
    TOPIC = "TOPIC"
    SUBTOPIC = "SUBTOPIC"
    CONCEPT = "CONCEPT"
    PRINCIPLE = "PRINCIPLE"
    FORMULA = "FORMULA"
    WORKED_EXAMPLE = "WORKED_EXAMPLE"
    QUESTION = "QUESTION"
    COMMON_ERROR = "COMMON_ERROR"


class ExamTargetLevel(str, Enum):
    """Target examination level relevance."""
    JEE_MAIN = "JEE_MAIN"
    JEE_ADVANCED = "JEE_ADVANCED"
    OLYMPIAD_EXTENSION = "OLYMPIAD_EXTENSION"


class PrerequisiteRelationshipType(str, Enum):
    """The pedagogical nature of a prerequisite dependency."""
    STRICT_CONCEPTUAL = "STRICT_CONCEPTUAL"            # Cannot understand B without mastering A
    MATHEMATICAL_TOOL = "MATHEMATICAL_TOOL"            # Mathematical technique required (e.g. integration, vectors)
    INTUITIVE_ANALOG = "INTUITIVE_ANALOG"              # Physical analogy (e.g. linear momentum -> angular momentum)
    PEDAGOGICAL_PREPARATION = "PEDAGOGICAL_PREPARATION"# Helpful preceding context
    EXTENDED_SYNTHESIS = "EXTENDED_SYNTHESIS"          # Coupling of two distinct branches


class PrerequisiteProvenanceType(str, Enum):
    """Provenance and authority classification for a prerequisite edge."""
    DETERMINISTIC_STRUCTURAL = "DETERMINISTIC_STRUCTURAL" # Mathematical or strict definition dependency
    PEDAGOGICAL_JUDGMENT = "PEDAGOGICAL_JUDGMENT"         # Curriculum sequence judgment based on cognitive scaffolding
    SOURCE_DERIVED = "SOURCE_DERIVED"                     # Sequence directly mandated by standard syllabus/textbook presentation
    PROJECT_DESIGNED = "PROJECT_DESIGNED"                 # Project-designed curriculum ladder structure


class ChapterTemplateType(str, Enum):
    """Specialized chapter layout templates based on physics domain."""
    MECHANICS = "MECHANICS"
    THERMODYNAMICS = "THERMODYNAMICS"
    ELECTRODYNAMICS = "ELECTRODYNAMICS"
    OPTICS = "OPTICS"
    WAVES_AND_OSCILLATIONS = "WAVES_AND_OSCILLATIONS"
    MODERN_PHYSICS = "MODERN_PHYSICS"
    GENERAL = "GENERAL"


class DifficultyDimensions(BaseModel):
    """Structured multi-dimensional difficulty model.
    
    Prevents reducing cognitive complexity to an arbitrary single score.
    Ratings for each dimension range from 1 (minimal) to 5 (extreme).
    
    CRITICAL METHODOLOGICAL DISTINCTION:
    - The six individual dimension ratings (1-5) are rubric-derived pedagogical judgments.
    - The composite scoring formula and weighting constants are project-defined policy (PEDAGOGICAL_PROJECT_POLICY),
      not an official NTA/IIT JEE standard.
    - Once the six dimension ratings are provided, the composite score and derived difficulty band
      are deterministically and reproducibly computed by the system.
    """
    conceptual_difficulty: int = Field(..., ge=1, le=5, description="Depth of physical insight required (1-5)")
    mathematical_difficulty: int = Field(..., ge=1, le=5, description="Complexity of algebraic or calculus tools (1-5)")
    multistep_reasoning_difficulty: int = Field(..., ge=1, le=5, description="Number of logical steps and linkages (1-5)")
    abstraction_difficulty: int = Field(..., ge=1, le=5, description="Distance from tangible, intuitive intuition (1-5)")
    computational_burden: int = Field(..., ge=1, le=5, description="Arithmetical density or algebraic length (1-5)")
    trap_misconception_difficulty: int = Field(..., ge=1, le=5, description="Presence of subtle sign/frame/constraint traps (1-5)")
    derived_difficulty_band: Optional[DifficultyLevel] = Field(None, description="Derived standard difficulty rating L1-L5")
    weighting_policy: str = Field(
        "PEDAGOGICAL_PROJECT_POLICY",
        description="Source of weighting constants: 2.0*Conc + 2.0*Multi + 1.5*Math + 1.5*Abs + 1.0*Trap + 0.8*Comp"
    )

    @model_validator(mode="after")
    def compute_derived_band(self) -> "DifficultyDimensions":
        # Deterministic composite score weighted towards conceptual and multi-step reasoning
        weighted_score = (
            2.0 * self.conceptual_difficulty
            + 2.0 * self.multistep_reasoning_difficulty
            + 1.5 * self.mathematical_difficulty
            + 1.5 * self.abstraction_difficulty
            + 1.0 * self.trap_misconception_difficulty
            + 0.8 * self.computational_burden
        ) / 8.8

        if self.derived_difficulty_band is None:
            if weighted_score < 1.8:
                self.derived_difficulty_band = DifficultyLevel.L1
            elif weighted_score < 2.8:
                self.derived_difficulty_band = DifficultyLevel.L2
            elif weighted_score < 3.8:
                self.derived_difficulty_band = DifficultyLevel.L3
            elif weighted_score < 4.6:
                self.derived_difficulty_band = DifficultyLevel.L4
            else:
                self.derived_difficulty_band = DifficultyLevel.L5
        return self


class PrerequisiteEdge(BaseModel):
    """A directed dependency edge in the curriculum prerequisite DAG."""
    from_node_id: str = Field(..., min_length=1, description="Prerequisite node ID")
    to_node_id: str = Field(..., min_length=1, description="Dependent node ID")
    relationship_type: PrerequisiteRelationshipType = Field(..., description="Nature of the dependency")
    provenance_type: PrerequisiteProvenanceType = Field(
        default=PrerequisiteProvenanceType.PROJECT_DESIGNED,
        description="Origin and authority of the prerequisite relationship"
    )
    evidence: str = Field(..., min_length=5, description="Documented syllabus or pedagogical evidence")
    rationale: str = Field(..., min_length=5, description="Physical explanation of why this dependency exists")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence in this prerequisite edge")
    provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Source provenance justifying this edge")


class CurriculumNode(BaseModel):
    """An explicit unit of learning in the curriculum hierarchy."""
    curriculum_id: str = Field(..., min_length=1, description="Unique curriculum identifier, e.g. 'curr-rot-01'")
    taxonomy_reference: TaxonomyReference = Field(..., description="Mapping to authoritative syllabus taxonomy")
    node_type: CurriculumNodeType = Field(..., description="Granular curriculum element type")
    title: str = Field(..., min_length=1, description="Pedagogical title")
    description: Optional[str] = Field(None, description="Scope definition or narrative explanation")
    prerequisite_ids: List[str] = Field(default_factory=list, description="IDs of prerequisite curriculum units")
    dependent_ids: List[str] = Field(default_factory=list, description="IDs of downstream curriculum units")
    mathematical_prerequisites: List[str] = Field(default_factory=list, description="Mathematical tools required (e.g. 'cross-product', 'integration')")
    target_exam_levels: List[ExamTargetLevel] = Field(
        default_factory=lambda: [ExamTargetLevel.JEE_MAIN, ExamTargetLevel.JEE_ADVANCED],
        description="Relevant exam tiers"
    )
    pedagogical_role: PedagogicalRole = Field(PedagogicalRole.FOUNDATION_CONCEPT, description="Pedagogical role")
    recommended_learning_position: int = Field(1, ge=1, description="Topological sequence position in learning order")
    estimated_learning_weight: float = Field(1.0, ge=0.1, le=10.0, description="Relative study effort weight")
    difficulty_band: DifficultyLevel = Field(DifficultyLevel.L2, description="Representative difficulty band")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Curriculum assignment confidence")
    provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Source provenance citations")


class FormulaRecord(BaseModel):
    """Structured physical formula record beyond an isolated LaTeX string."""
    formula_id: str = Field(..., min_length=1, description="Unique formula identifier")
    title: str = Field(..., min_length=1, description="Formula name (e.g. 'Conservation of Angular Momentum')")
    equation_latex: str = Field(..., min_length=1, description="Complete KaTeX-compatible LaTeX equation")
    variables: Dict[str, str] = Field(..., description="Mapping of variable symbol -> physical quantity name")
    units_and_dimensions: Dict[str, str] = Field(..., description="Mapping of variable/constant -> SI unit and dimension")
    assumptions: List[str] = Field(..., min_length=1, description="Explicit physical assumptions (e.g. 'Rigid body', 'Fixed axis')")
    conditions_of_validity: List[str] = Field(..., min_length=1, description="Conditions under which this formula holds")
    derivation_links: List[str] = Field(default_factory=list, description="Referenced derivations or parent principles")
    related_concept_ids: List[str] = Field(default_factory=list, description="Connected curriculum concept IDs")
    common_misuse_cases: List[str] = Field(default_factory=list, description="Common traps where students misapply this formula")
    provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Source provenance records")
    verification_status: AtomStatus = Field(AtomStatus.VERIFIED, description="Verification status")


class WorkedExampleRecord(BaseModel):
    """A fully-structured worked example with physical setup and sanity checks."""
    example_id: str = Field(..., min_length=1, description="Unique example identifier")
    problem_statement: str = Field(..., min_length=5, description="Full problem statement with LaTeX math")
    known_quantities: Dict[str, str] = Field(..., description="Explicitly given physical quantities")
    target_quantity: str = Field(..., min_length=1, description="Quantity to be determined")
    relevant_concepts: List[str] = Field(..., min_length=1, description="Core physical concepts required")
    governing_principles: List[str] = Field(..., min_length=1, description="Laws or theorems used (e.g. 'Work-Energy Theorem')")
    solution_strategy: str = Field(..., min_length=5, description="Teacher-like explanation of the approach")
    step_by_step_derivation: List[str] = Field(..., min_length=1, description="Step-by-step mathematical steps")
    final_answer: str = Field(..., min_length=1, description="Exact verified final result")
    sanity_checks: List[str] = Field(default_factory=list, description="Dimensional checks, limiting cases (e.g. m -> 0)")
    alternate_methods: List[SolutionMethod] = Field(default_factory=list, description="Alternative physical derivations")
    source_atom_id: Optional[str] = Field(None, description="Canonical atom ID if adapted from verified atom")
    provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Source provenance records")
    verification_status: AtomStatus = Field(AtomStatus.VERIFIED, description="Verification status")


class MisconceptionRecord(BaseModel):
    """Explicit physical misconception record with trap mechanisms."""
    misconception_id: str = Field(..., min_length=1, description="Unique misconception identifier")
    category: str = Field(
        ...,
        description="Category: SIGN_MISTAKE, VECTOR_SCALAR_CONFUSION, INVALID_FORMULA_CONDITION, "
                    "WRONG_CONSERVATION_LAW, FRAME_CONFUSION, HIDDEN_CONSTRAINT_OMISSION, DIMENSIONAL_INCONSISTENCY"
    )
    statement: str = Field(..., min_length=5, description="The incorrect intuitive claim or belief")
    explanation: str = Field(..., min_length=5, description="Rigorous physical explanation of why it is incorrect")
    trap_mechanism: str = Field(..., min_length=5, description="How JEE exam questions specifically test and exploit this")
    trigger_conditions: List[str] = Field(default_factory=list, description="Specific problem configurations triggering this error")
    connected_concept_ids: List[str] = Field(default_factory=list, description="Connected curriculum concept IDs")
    connected_atom_ids: List[str] = Field(default_factory=list, description="Verified atom IDs that illustrate this trap")


class QuestionLadderRung(BaseModel):
    """An individual problem rung in a progressive question ladder."""
    level: int = Field(..., ge=0, le=5, description="Ladder level 0 to 5")
    level_name: str = Field(..., description="Level label, e.g. 'Direct application', 'JEE Advanced'")
    atom_id: str = Field(..., min_length=1, description="Canonical verified atom ID")
    physical_delta: str = Field(..., min_length=5, description="Physical change introduced compared to preceding rung")
    reasoning_depth: int = Field(1, ge=1, le=5, description="Cognitive steps required")
    concepts_involved: List[str] = Field(..., min_length=1, description="Physics concepts exercised in this rung")
    mathematical_complexity: str = Field(..., description="Mathematical tools involved")
    transfer_requirement: Optional[str] = Field(None, description="Transfer of knowledge to non-standard geometry/context")


class QuestionLadder(BaseModel):
    """A sequence of problems scaffolding understanding across one physical system."""
    ladder_id: str = Field(..., min_length=1, description="Unique ladder identifier")
    chapter_id: str = Field(..., min_length=1, description="Parent chapter slug")
    topic_id: str = Field(..., min_length=1, description="Parent topic slug")
    title: str = Field(..., min_length=1, description="Title of the ladder")
    physical_system: str = Field(..., min_length=5, description="The shared physical system (e.g. 'Rotating disc with dropping mass')")
    rungs: List[QuestionLadderRung] = Field(..., min_length=2, description="Ordered progressive rungs")
    pedagogical_objective: Optional[str] = Field(None, description="Overall learning takeaway of this ladder")

    @model_validator(mode="after")
    def validate_rungs_order(self) -> "QuestionLadder":
        levels = [r.level for r in self.rungs]
        if levels != sorted(levels):
            raise ValueError(f"Ladder rungs must be strictly non-decreasing in level: {levels}")
        return self


# Backwards compatibility alias for Phase 1 QuestionLadderSpec
class QuestionLadderSpec(QuestionLadder):
    pass


class ConceptPlacement(BaseModel):
    """Placement of a concept in the chapter narrative structure."""
    concept_id: str = Field(..., min_length=1, description="Unique concept identifier")
    curriculum_id: str = Field(..., min_length=1, description="Curriculum unit ID")
    role: PedagogicalRole = Field(PedagogicalRole.FOUNDATION_CONCEPT, description="Pedagogical role")
    prerequisite_relationship: Optional[str] = Field(None, description="Prerequisite note or linkage")
    explanation_priority: int = Field(1, ge=1, description="Order of presentation within section")
    source_atom_ids: List[str] = Field(default_factory=list, description="Backing canonical atom IDs if any")
    source_evidence: str = Field(..., min_length=1, description="Evidence citation justifying concept inclusion")


class QuestionPlacement(BaseModel):
    """Placement of a verified canonical question within a chapter or topic."""
    atom_id: str = Field(..., min_length=1, description="Verified canonical atom ID")
    curriculum_id: str = Field(..., min_length=1, description="Curriculum unit ID")
    chapter_id: str = Field(..., min_length=1, description="Chapter slug")
    topic_id: str = Field(..., min_length=1, description="Topic slug")
    pedagogical_role: PedagogicalRole = Field(PedagogicalRole.PRACTICE_QUESTION, description="Role of this question")
    difficulty_dimensions: DifficultyDimensions = Field(..., description="Multi-dimensional difficulty breakdown")
    prerequisite_concept_ids: List[str] = Field(default_factory=list, description="Concept IDs student must know before solving")
    question_ladder_id: Optional[str] = Field(None, description="ID of parent ladder if part of a ladder")
    question_ladder_position: Optional[int] = Field(None, description="Rung position in ladder if applicable")
    source_provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Original source provenance")


class ChapterSpec(BaseModel):
    """Editorial and pedagogical specification for a book chapter."""
    chapter_id: str = Field(..., min_length=1, description="Canonical chapter slug (e.g. 'rotational-motion')")
    chapter_title: str = Field(..., min_length=1, description="Display title for the chapter")
    template_type: ChapterTemplateType = Field(ChapterTemplateType.GENERAL, description="Domain chapter template")
    order: int = Field(1, ge=1, description="Curriculum presentation order")
    taxonomy_references: List[TaxonomyReference] = Field(default_factory=list, description="Associated taxonomy nodes")
    learning_objectives: List[str] = Field(default_factory=list, description="Concrete pedagogical objectives")
    prerequisite_curriculum_nodes: List[str] = Field(default_factory=list, description="Required prerequisite curriculum node IDs")
    concept_sequence: List[ConceptPlacement] = Field(default_factory=list, description="Ordered concept placements")
    formula_sequence: List[FormulaRecord] = Field(default_factory=list, description="Ordered formula records")
    misconception_sequence: List[MisconceptionRecord] = Field(default_factory=list, description="Ordered misconception records")
    worked_example_sequence: List[WorkedExampleRecord] = Field(default_factory=list, description="Ordered worked examples")
    question_sequence: List[QuestionPlacement] = Field(default_factory=list, description="Ordered question placements")
    question_ladders: List[QuestionLadder] = Field(default_factory=list, description="Structured question ladders")
    revision_checklist: List[str] = Field(default_factory=list, description="Key revision points")
    coverage_requirements: Dict[str, Any] = Field(default_factory=dict, description="Deterministic coverage requirements")
    assessment_requirements: Dict[str, Any] = Field(default_factory=dict, description="Target difficulty counts and problem types")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Compatibility properties for legacy Phase 1 tests/interfaces
    @property
    def title(self) -> str:
        return self.chapter_title

    @property
    def ladders(self) -> List[QuestionLadder]:
        return self.question_ladders

    @property
    def mandatory_atom_ids(self) -> List[str]:
        return [q.atom_id for q in self.question_sequence]


class ChapterSectionPlan(BaseModel):
    """Blueprint for a single section within a chapter."""
    section_id: str = Field(..., min_length=1, description="Section slug, e.g. 'sec-01-torque'")
    section_order: int = Field(..., ge=1, description="Sequence order within chapter")
    title: str = Field(..., min_length=1, description="Section heading")
    pedagogical_purpose: str = Field(..., min_length=5, description="Specific learning goal for this section")
    concepts: List[str] = Field(default_factory=list, description="Concept titles or IDs")
    formula_ids: List[str] = Field(default_factory=list, description="Referenced formula IDs")
    worked_example_ids: List[str] = Field(default_factory=list, description="Referenced worked example IDs")
    question_atom_ids: List[str] = Field(default_factory=list, description="Referenced canonical question atom IDs")
    misconception_ids: List[str] = Field(default_factory=list, description="Referenced misconception IDs")
    prerequisite_refs: List[str] = Field(default_factory=list, description="Section prerequisites")
    source_references: List[str] = Field(default_factory=list, description="Source provenance citations")
    unresolved_gaps: List[str] = Field(default_factory=list, description="Identified pedagogical gaps in this section")


class ChapterPlan(BaseModel):
    """Complete structured blueprint for assembling a chapter."""
    plan_id: str = Field(..., min_length=1, description="Unique plan identifier")
    chapter_id: str = Field(..., min_length=1, description="Target chapter slug")
    title: str = Field(..., min_length=1, description="Full chapter title")
    template_type: ChapterTemplateType = Field(ChapterTemplateType.GENERAL, description="Domain chapter template")
    sections: List[ChapterSectionPlan] = Field(..., min_length=1, description="Ordered section plans")
    pedagogical_synthesis_notes: List[str] = Field(default_factory=list, description="Synthesis strategies across multiple sources")
    unresolved_gaps: List[str] = Field(default_factory=list, description="Gaps identified during assembly planning")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MockTestSpec(BaseModel):
    """Specification for generating an adaptive or milestone chapter mock test."""
    mock_id: str = Field(..., min_length=1, description="Unique mock test ID")
    chapter_id: str = Field(..., min_length=1, description="Chapter or multi-chapter domain slug")
    title: str = Field(..., min_length=1, description="Title of the mock exam")
    target_question_count: int = Field(25, ge=5, le=100, description="Default JEE Physics chapter mock is 25 questions")
    difficulty_distribution: Dict[str, int] = Field(
        default_factory=lambda: {"L1": 3, "L2": 7, "L3": 8, "L4": 5, "L5": 2},
        description="Target distribution across difficulty levels L1 through L5"
    )
    question_types: List[str] = Field(
        default_factory=lambda: ["single_correct", "multiple_correct", "numerical"]
    )
    time_limit_minutes: int = Field(60, ge=15, le=180)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CurriculumAuditRecord(BaseModel):
    """Immutable audit trail for curriculum structural modifications."""
    entry_id: str = Field(..., min_length=1, description="Unique audit journal entry ID")
    curriculum_change: str = Field(..., min_length=1, description="Operation performed, e.g. 'ADD_PREREQUISITE_EDGE'")
    previous_value: Optional[str] = Field(None, description="Previous state or value")
    new_value: str = Field(..., min_length=1, description="New state or value")
    reason: str = Field(..., min_length=5, description="Physical or pedagogical justification")
    agent_identity: str = Field(..., min_length=1, description="Subagent role or deterministic process name")
    conversation_id: str = Field(..., min_length=1, description="Antigravity conversation ID")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall certainty score")
    validation_status: str = Field("VALIDATION_PASSED", description="Deterministic validation status ('VALIDATION_PASSED', 'FAILED', etc.)")
    agent_confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Autonomous subagent self-assessed confidence")
    evidence_strength: str = Field("DETERMINISTIC_GATE_VERIFIED", description="Origin of verification evidence ('DETERMINISTIC_GATE_VERIFIED', 'INDEPENDENT_EVALUATION', etc.)")
    evidence: str = Field(..., min_length=1, description="Supporting evidence")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GapCategory(str, Enum):
    """Classification of pedagogical and content gaps."""
    NO_CONTENT = "NO_CONTENT"                          # Taxonomy node has zero canonical atoms
    NO_EXPLANATION = "NO_EXPLANATION"                  # Node has questions but no theory/explanation
    NO_WORKED_EXAMPLE = "NO_WORKED_EXAMPLE"            # Node lacks a step-by-step worked example
    NO_BASIC_QUESTION = "NO_BASIC_QUESTION"            # Node lacks L1/L2 foundational practice problems
    NO_ADVANCED_QUESTION = "NO_ADVANCED_QUESTION"      # Node lacks L4/L5 synthesis problems
    MISSING_PREREQUISITE = "MISSING_PREREQUISITE"      # Node has no mapped prerequisites in DAG
    UNSUPPORTED_EXTENSION = "UNSUPPORTED_EXTENSION"    # Extension node lacks Olympiad justification
    REVIEW_BLOCKED = "REVIEW_BLOCKED"                  # Topic has unplaced atoms stalled in review queue


class CurriculumGapItem(BaseModel):
    """A specific identified curriculum gap."""
    gap_id: str = Field(..., min_length=1, description="Unique gap identifier")
    taxonomy_node_id: str = Field(..., min_length=1, description="Associated taxonomy node ID")
    chapter_id: str = Field(..., min_length=1, description="Parent chapter slug")
    gap_category: GapCategory = Field(..., description="Gap classification category")
    description: str = Field(..., min_length=5, description="Detailed explanation of what is missing")
    severity: str = Field("WARNING", description="'CRITICAL', 'WARNING', or 'INFO'")
    remediation_action: str = Field(..., min_length=5, description="Recommended remediation instruction for content generation")


class CurriculumGapReport(BaseModel):
    """Comprehensive deterministic curriculum gap report."""
    report_id: str = Field(..., min_length=1, description="Unique report identifier")
    total_taxonomy_nodes: int = Field(460, ge=0, description="Total nodes in syllabus tree including root")
    content_bearing_nodes_analyzed: int = Field(459, ge=0, description="Content-bearing syllabus nodes analyzed")
    excluded_nodes: List[str] = Field(default_factory=lambda: ["physics"], description="List of structural nodes excluded from content analysis")
    exclusion_reason: str = Field(
        "Organizational root node (TaxonomyLevel.SUBJECT) excluded; only chapters, topics, and subtopics are content-bearing.",
        description="Justification for excluded nodes"
    )
    nodes_covered: int = Field(..., ge=0, description="Nodes with at least one verified atom (Taxonomy Presence)")
    nodes_empty: int = Field(..., ge=0, description="Nodes with zero verified atoms")
    nodes_light: int = Field(..., ge=0, description="Nodes with only 1 atom (under-covered)")
    taxonomy_presence_nodes: int = Field(0, ge=0, description="Count of nodes having at least one verified atom")
    pedagogical_coverage_breakdown: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of nodes satisfying each pedagogical criterion"
    )
    gaps_by_category: Dict[str, int] = Field(default_factory=dict, description="Count of gaps per category")
    gap_items: List[CurriculumGapItem] = Field(default_factory=list, description="Granular gap items")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
