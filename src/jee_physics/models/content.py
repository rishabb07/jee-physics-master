"""Pydantic models for Phase 8 Content Generation, Verification, Editorial Assembly, and QA.

Separates content specification, content generation, independent physics verification,
editorial assembly, and rendered QA.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from jee_physics.models.atom import TaxonomyReference
from jee_physics.models.provenance import ProvenanceRecord


class ContentBlockType(str, Enum):
    """Pedagogical content block types within a chapter."""
    OBJECTIVE = "OBJECTIVE"
    PREREQUISITE_REFRESH = "PREREQUISITE_REFRESH"
    INTUITION = "INTUITION"
    CONCEPT_EXPLANATION = "CONCEPT_EXPLANATION"
    FORMAL_DEFINITION = "FORMAL_DEFINITION"
    FORMULA = "FORMULA"
    DERIVATION = "DERIVATION"
    WORKED_EXAMPLE = "WORKED_EXAMPLE"
    MISCONCEPTION = "MISCONCEPTION"
    QUESTION_SET = "QUESTION_SET"
    SUMMARY = "SUMMARY"
    REVISION_CHECKLIST = "REVISION_CHECKLIST"
    EDITORIAL_TRANSITION = "EDITORIAL_TRANSITION"


class ContentVerificationStatus(str, Enum):
    """Lifecycle verification states for generated physics content."""
    UNVERIFIED = "UNVERIFIED"
    GENERATED = "GENERATED"
    STAGED = "STAGED"
    VERIFIED = "VERIFIED"
    PROMOTABLE = "PROMOTABLE"
    REJECTED = "REJECTED"
    CONFLICT = "CONFLICT"
    REVIEW = "REVIEW"
    INVALIDATED = "INVALIDATED"


class ContentRiskLevel(str, Enum):
    """Risk classification for physical content requiring calibrated verification rigor."""
    LOW = "LOW"          # Formatting, wording transitions, non-substantive connective prose
    MEDIUM = "MEDIUM"    # Standard explanations, common formula descriptions, standard examples
    HIGH = "HIGH"        # Non-trivial derivations, sign convention subtleties, limiting case proofs


class ClaimTraceClass(str, Enum):
    """Provenance audit class for every substantive physical statement."""
    CANONICAL_KB = "CANONICAL_KB"                      # Grounded directly in verified kb/atoms/
    SOURCE_DERIVED = "SOURCE_DERIVED"                  # Traceable to registered source document text
    GENERATED_AND_VERIFIED = "GENERATED_AND_VERIFIED"  # Subagent-generated and independently verified
    EDITORIAL_TRANSITION = "EDITORIAL_TRANSITION"      # Connective editorial prose without physics claims


class ConceptExplanation(BaseModel):
    """Atomic pedagogical explanation of a physical concept."""
    content_id: str = Field(..., min_length=1, description="Unique content identifier")
    curriculum_id: str = Field(..., min_length=1, description="Mapped curriculum unit ID")
    taxonomy_reference: TaxonomyReference = Field(..., description="Authoritative taxonomy mapping")
    title: str = Field(..., min_length=1, description="Display title of the concept")
    learning_objective: str = Field(..., min_length=5, description="Clear statement of what student will learn")
    explanation: str = Field(..., min_length=10, description="Rigorous physical narrative")
    intuition: str = Field(..., min_length=5, description="Physical intuition, everyday analog, or thought experiment")
    formal_definition: str = Field(..., min_length=5, description="Precise formal physical definition")
    assumptions: List[str] = Field(default_factory=list, description="Explicit boundary assumptions")
    boundary_conditions: List[str] = Field(default_factory=list, description="Limits of validity and edge conditions")
    related_formula_ids: List[str] = Field(default_factory=list, description="Associated formula IDs")
    prerequisite_refs: List[str] = Field(default_factory=list, description="Required prerequisite curriculum IDs")
    source_references: List[str] = Field(default_factory=list, description="Source citations or text references")
    generation_metadata: Dict[str, Any] = Field(default_factory=dict, description="Agent identity, prompt, and parameters")
    verification_status: ContentVerificationStatus = Field(ContentVerificationStatus.GENERATED)
    content_hash: Optional[str] = Field(None, description="SHA-256 hash of normalized content payload")
    verification_record_id: Optional[str] = Field(None, description="Bound verification record ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FormulaRecord(BaseModel):
    """Structured physical formula record beyond an isolated LaTeX string."""
    formula_id: str = Field(..., min_length=1, description="Unique formula identifier")
    chapter_id: str = Field(..., min_length=1, description="Parent chapter slug")
    title: str = Field(..., min_length=1, description="Descriptive title of the formula")
    equation: str = Field(..., min_length=1, description="Complete KaTeX-compatible LaTeX equation")
    equation_latex: Optional[str] = Field(None, description="Alias for equation in KaTeX format")
    variables: Dict[str, str] = Field(..., description="Mapping of variable symbol -> physical quantity name")
    units: Dict[str, str] = Field(..., description="Mapping of variable -> SI unit")
    dimensions: Dict[str, str] = Field(..., description="Mapping of variable -> dimensional formula")
    assumptions: List[str] = Field(..., min_length=1, description="Explicit physical assumptions")
    validity_conditions: List[str] = Field(..., min_length=1, description="Conditions under which this formula holds")
    derivation_reference: Optional[str] = Field(None, description="Referenced derivation record ID")
    related_concepts: List[str] = Field(default_factory=list, description="Connected curriculum concept IDs")
    common_misuse: List[str] = Field(default_factory=list, description="Common traps where students misapply this formula")
    provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Source provenance citations")
    generation_metadata: Dict[str, Any] = Field(default_factory=dict, description="Agent identity, prompt, and parameters")
    verification_status: ContentVerificationStatus = Field(ContentVerificationStatus.GENERATED)
    content_hash: Optional[str] = Field(None, description="SHA-256 hash of normalized formula payload")
    verification_record_id: Optional[str] = Field(None, description="Bound verification record ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def model_post_init(self, __context: Any) -> None:
        if not self.equation_latex and self.equation:
            self.equation_latex = self.equation
        elif not self.equation and self.equation_latex:
            self.equation = self.equation_latex


class DerivationStep(BaseModel):
    """A single sequential step in a mathematical physics derivation."""
    step_number: int = Field(..., ge=1, description="1-indexed step sequence")
    description: str = Field(..., min_length=3, description="Physical/mathematical operation performed")
    starting_equation: str = Field(..., description="Equation prior to transformation")
    operation: str = Field(..., description="Applied law, substitution, or calculus operation")
    result_equation: str = Field(..., description="Resulting equation in LaTeX math")
    assumptions_applied: List[str] = Field(default_factory=list, description="Assumptions invoked in this step")


class DerivationRecord(BaseModel):
    """First-principles mathematical derivation of a target formula."""
    derivation_id: str = Field(..., min_length=1, description="Unique derivation identifier")
    target_formula_id: str = Field(..., min_length=1, description="Formula ID being derived")
    target_equation: str = Field(..., min_length=1, description="Target equation in LaTeX math")
    starting_principles: List[str] = Field(..., min_length=1, description="Starting axioms, laws, or theorems")
    assumptions: List[str] = Field(..., min_length=1, description="Explicit physical assumptions")
    ordered_steps: List[DerivationStep] = Field(..., min_length=1, description="Sequential derivation steps")
    final_equation: str = Field(..., min_length=1, description="Derived final equation")
    applicability_conditions: List[str] = Field(..., min_length=1, description="Conditions under which derivation holds")
    source_references: List[str] = Field(default_factory=list, description="Source textbook references")
    risk_level: ContentRiskLevel = Field(ContentRiskLevel.HIGH, description="High risk by default for derivations")
    verification_status: ContentVerificationStatus = Field(ContentVerificationStatus.GENERATED)
    verification_record_id: Optional[str] = Field(None, description="Bound verification record ID")
    content_hash: Optional[str] = Field(None, description="SHA-256 hash of normalized derivation content")
    generator_identity: str = Field(..., min_length=1, description="Authoring agent name")
    generator_conversation_id: str = Field(..., min_length=1, description="Authoring conversation ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WorkedExampleSolutionStep(BaseModel):
    """An individual step in a worked example solution."""
    step_number: int = Field(..., ge=1, description="1-indexed step sequence")
    principle_applied: str = Field(..., description="Governing physical principle or formula")
    equation: str = Field(..., description="Symbolic algebraic equation")
    substitution: str = Field(..., description="Numerical substitution with units")
    intermediate_result: str = Field(..., description="Step result with units")


class WorkedExampleContentRecord(BaseModel):
    """A fully-structured worked example with physical strategy and sanity checks."""
    example_id: str = Field(..., min_length=1, description="Unique example identifier")
    problem_statement: str = Field(..., min_length=5, description="Problem statement with LaTeX math")
    known_quantities: Dict[str, str] = Field(..., description="Given quantities with symbols and units")
    target_quantity: str = Field(..., min_length=1, description="Target quantity to calculate")
    relevant_concepts: List[str] = Field(..., min_length=1, description="Core physical concepts exercised")
    governing_principles: List[str] = Field(..., min_length=1, description="Governing laws or theorems")
    solution_strategy: str = Field(..., min_length=5, description="High-level solution strategy")
    ordered_steps: List[WorkedExampleSolutionStep] = Field(..., min_length=1, description="Solution steps")
    final_answer: str = Field(..., min_length=1, description="Exact verified final result")
    units: str = Field(..., min_length=1, description="SI units of final result")
    sanity_checks: List[str] = Field(default_factory=list, description="Limiting cases, dimensions, orders of magnitude")
    alternate_methods: List[str] = Field(default_factory=list, description="Alternative solution approaches")
    source_atom_id: Optional[str] = Field(None, description="Canonical atom ID if adapted from verified atom")
    provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Source provenance records")
    risk_level: ContentRiskLevel = Field(ContentRiskLevel.MEDIUM)
    verification_status: ContentVerificationStatus = Field(ContentVerificationStatus.GENERATED)
    verification_record_id: Optional[str] = Field(None, description="Bound verification record ID")
    content_hash: Optional[str] = Field(None, description="SHA-256 hash of normalized example payload")
    generator_identity: str = Field(..., min_length=1, description="Authoring agent name")
    generator_conversation_id: str = Field(..., min_length=1, description="Authoring conversation ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MisconceptionContentRecord(BaseModel):
    """Structured physical misconception record with trap mechanisms and correction."""
    misconception_id: str = Field(..., min_length=1, description="Unique misconception identifier")
    concept_id: str = Field(..., min_length=1, description="Mapped concept ID")
    title: str = Field(..., min_length=1, description="Descriptive title of the misconception")
    category: str = Field(..., description="SIGN_MISTAKE, VECTOR_SCALAR_CONFUSION, INVALID_FORMULA_CONDITION, etc.")
    incorrect_statement: str = Field(..., min_length=5, description="The flawed intuitive belief")
    why_it_fails: str = Field(..., min_length=5, description="Rigorous physical explanation of why it fails")
    diagnostic_symptom: str = Field(..., min_length=5, description="How to spot this error in student thinking")
    corrective_explanation: str = Field(..., min_length=5, description="Correct physical principle to apply")
    supporting_evidence: str = Field(..., min_length=5, description="Textbook or experimental evidence")
    connected_atom_ids: List[str] = Field(default_factory=list, description="Canonical atom IDs illustrating this")
    verification_status: ContentVerificationStatus = Field(ContentVerificationStatus.GENERATED)
    content_hash: Optional[str] = Field(None, description="SHA-256 hash of normalized misconception")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"extra": "allow"}


class ChapterContentBlock(BaseModel):
    """A typed atomic content block ready for editorial sequencing into chapter drafts."""
    block_id: str = Field(..., min_length=1, description="Unique content block ID")
    block_type: ContentBlockType = Field(..., description="Typed content block variant")
    chapter_id: str = Field(..., min_length=1, description="Parent chapter slug")
    section_id: str = Field(..., min_length=1, description="Parent section ID from ChapterPlan")
    order_in_section: int = Field(..., ge=1, description="Sequential order within section")
    payload_id: str = Field(..., min_length=1, description="ID of backing atomic record (concept, formula, derivation, etc.)")
    payload_type: str = Field(..., description="Model type name of backing payload")
    title: Optional[str] = Field(None, description="Block header title if rendered")
    rendered_markdown: str = Field(..., min_length=1, description="Formatted pedagogical markdown")
    trace_class: ClaimTraceClass = Field(ClaimTraceClass.GENERATED_AND_VERIFIED, description="Claim provenance trace")
    source_atom_ids: List[str] = Field(default_factory=list, description="Canonical atom IDs supporting this block")
    verification_status: ContentVerificationStatus = Field(ContentVerificationStatus.VERIFIED)
    content_hash: Optional[str] = Field(None, description="SHA-256 hash of rendered markdown")


class ContentRequirement(BaseModel):
    """A single formal content generation requirement extracted from ChapterSpec / ChapterPlan."""
    requirement_id: str = Field(..., min_length=1, description="Unique requirement identifier")
    chapter_id: str = Field(..., min_length=1, description="Target chapter slug")
    section_id: str = Field(..., min_length=1, description="Target section ID")
    content_type: ContentBlockType = Field(..., description="Target content block type")
    curriculum_node_id: str = Field(..., min_length=1, description="Associated curriculum node ID")
    objective: str = Field(..., min_length=5, description="Objective of this content unit")
    required_source_refs: List[str] = Field(default_factory=list, description="Source references required")
    required_prerequisites: List[str] = Field(default_factory=list, description="Prerequisite concepts")
    needs_physics_verification: bool = Field(True, description="Whether independent physics verification is required")
    can_generate_from_kb: bool = Field(False, description="Whether canonical atoms in kb/atoms/ directly satisfy it")
    is_unresolved_gap: bool = Field(False, description="Flagged as missing source/content gap")
    risk_level: ContentRiskLevel = Field(ContentRiskLevel.MEDIUM, description="Verification risk level")


class ContentRequirementReport(BaseModel):
    """Deterministic catalog of all extracted content generation requirements across chapters."""
    report_id: str = Field(..., min_length=1, description="Unique report identifier")
    requirements_count: int = Field(..., ge=0, description="Total requirements cataloged")
    gaps_count: int = Field(..., ge=0, description="Requirements flagged as unresolved gaps")
    requirements: List[ContentRequirement] = Field(default_factory=list, description="Detailed requirements list")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ContentVerificationRecord(BaseModel):
    """Immutable record of independent physical verification bound to exact content hash."""
    verification_id: str = Field(..., min_length=1, description="Unique verification identifier")
    artifact_id: str = Field(..., min_length=1, description="Target content artifact ID")
    artifact_version: int = Field(1, ge=1, description="Version of the artifact verified")
    content_hash: str = Field(..., min_length=8, description="SHA-256 hash of the exact verified content payload")
    verifier_id: str = Field(..., min_length=1, description="Verifier agent identity")
    verifier_conversation_id: str = Field(..., min_length=1, description="Verifier agent conversation ID")
    risk_level: ContentRiskLevel = Field(..., description="Assessed risk level")
    verdict: str = Field(..., description="'VERIFIED' | 'REJECTED' | 'CONFLICT' | 'REVIEW'")
    assumptions_checked: bool = Field(..., description="Whether assumptions were independently reviewed")
    dimensional_check_passed: bool = Field(..., description="Whether dimensional analysis verified")
    numerical_check_passed: bool = Field(..., description="Whether numerical values recomputed independently")
    limiting_case_check_passed: bool = Field(..., description="Whether physical limits verified")
    independent_derivation_or_calculation: str = Field(..., min_length=5, description="Independent verification work")
    findings: List[str] = Field(default_factory=list, description="Summary of verifier findings")
    discrepancies: List[str] = Field(default_factory=list, description="Any detected physical flaws or caveats")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class VerifierOpinion(BaseModel):
    """An individual verifier's independent evaluation."""
    verifier_id: str = Field(..., min_length=1, description="Verifier agent identity")
    verifier_conversation_id: str = Field(..., min_length=1, description="Verifier agent conversation ID")
    verdict: str = Field(..., description="'VERIFIED' | 'REJECTED' | 'REVIEW'")
    assumptions_checked: bool = Field(True, description="Whether assumptions were audited")
    dimensional_check_passed: bool = Field(True, description="Whether dimensions were checked")
    numerical_check_passed: bool = Field(True, description="Whether calculations were checked")
    limiting_case_check_passed: bool = Field(True, description="Whether limits were checked")
    independent_derivation_or_calculation: str = Field(..., min_length=5, description="Independent verification work")
    findings: List[str] = Field(default_factory=list, description="Verifier findings")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DualVerificationRecord(BaseModel):
    """Immutable record of dual independent verification for HIGH-risk content."""
    verification_id: str = Field(..., min_length=1, description="Unique dual verification identifier (dual-cvr-{artifact_id})")
    artifact_id: str = Field(..., min_length=1, description="Target content artifact ID")
    artifact_version: int = Field(1, ge=1, description="Artifact version")
    content_hash: str = Field(..., min_length=8, description="SHA-256 hash of verified substantive payload")
    risk_level: ContentRiskLevel = Field(ContentRiskLevel.HIGH, description="Risk level (strictly HIGH for dual verification)")
    verifier_a: VerifierOpinion = Field(..., description="First independent verifier's opinion")
    verifier_b: VerifierOpinion = Field(..., description="Second independent verifier's opinion")
    agreement: bool = Field(..., description="Whether Verifier A and Verifier B agree")
    adjudication_reference: Optional[str] = Field(None, description="Adjudication ID if discrepancy required arbitration")
    final_verdict: str = Field(..., description="'VERIFIED' | 'REJECTED' | 'REVIEW'")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChapterQAFinding(BaseModel):
    """An individual issue detected during independent chapter QA audit."""
    category: str = Field(..., description="'PHYSICS' | 'CURRICULUM' | 'EDITORIAL' | 'PEDAGOGY' | 'RENDERING'")
    severity: str = Field("WARNING", description="'CRITICAL' | 'WARNING' | 'INFO'")
    location: str = Field(..., description="Section, block ID, or line reference")
    description: str = Field(..., min_length=5, description="Description of the issue")
    remediation: str = Field(..., min_length=5, description="Suggested fix")


class ChapterQAReport(BaseModel):
    """Audit report produced by the Independent Chapter QA Agent."""
    report_id: str = Field(..., min_length=1, description="Unique QA report identifier")
    chapter_id: str = Field(..., min_length=1, description="Audited chapter slug")
    verdict: str = Field("PASSED", description="'PASSED' | 'FAILED' | 'NEEDS_REVISION'")
    physics_passed: bool = Field(..., description="Physics accuracy check")
    curriculum_passed: bool = Field(..., description="Curriculum specification alignment check")
    editorial_passed: bool = Field(..., description="Editorial and notation consistency check")
    pedagogy_passed: bool = Field(..., description="Pedagogical scaffolding and flow check")
    provenance_passed: bool = Field(True, description="Provenance and claim trace validity check")
    findings: List[ChapterQAFinding] = Field(default_factory=list, description="List of detected findings")
    claim_traces: Dict[str, ClaimTraceClass] = Field(
        default_factory=dict,
        description="Audit trace mapping substantive claims to ClaimTraceClass"
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RenderingQAReport(BaseModel):
    """Deterministic rendering QA report checking LaTeX, references, and layout integrity."""
    report_id: str = Field(..., min_length=1, description="Unique rendering QA report identifier")
    chapter_id: str = Field(..., min_length=1, description="Audited chapter slug")
    latex_errors: List[str] = Field(default_factory=list, description="LaTeX syntax or delimiter balance errors")
    broken_references: List[str] = Field(default_factory=list, description="Unresolved section, formula, or figure references")
    empty_sections: List[str] = Field(default_factory=list, description="Sections with zero content blocks")
    passed: bool = Field(..., description="True if zero critical rendering errors")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
