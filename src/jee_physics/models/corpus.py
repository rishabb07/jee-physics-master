from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SourceRole(str, Enum):
    """Authoritative project classification for a source document."""
    PRIMARY_JEE = "PRIMARY_JEE"                  # e.g., H.C. Verma Vol 1 & 2
    UNDERGRADUATE_DEPTH = "UNDERGRADUATE_DEPTH"  # e.g., Halliday/Resnick/Walker, University Physics
    CONCEPTUAL_DEPTH = "CONCEPTUAL_DEPTH"        # e.g., Feynman Lectures
    ADVANCED_PROBLEMS = "ADVANCED_PROBLEMS"      # e.g., Irodov Problems in General Physics
    EXAM_ASSESSMENT = "EXAM_ASSESSMENT"          # e.g., Real & mock JEE papers


class SourceContentType(str, Enum):
    """Granular classification of physical content within a source segment."""
    CONCEPT = "CONCEPT"
    DEFINITION = "DEFINITION"
    PRINCIPLE = "PRINCIPLE"
    LAW = "LAW"
    FORMULA = "FORMULA"
    DERIVATION = "DERIVATION"
    EXAMPLE = "EXAMPLE"
    PROBLEM = "PROBLEM"
    SOLUTION = "SOLUTION"
    FIGURE_DIAGRAM = "FIGURE_DIAGRAM"
    MISCONCEPTION_CAUTION = "MISCONCEPTION_CAUTION"
    EXPERIMENT_OBSERVATION = "EXPERIMENT_OBSERVATION"
    EXAM_QUESTION = "EXAM_QUESTION"
    OTHER = "OTHER"


class CoverageStatus(str, Enum):
    """Taxonomy-level source grounding and corroboration classification."""
    MULTI_SOURCE_COVERED = "MULTI_SOURCE_COVERED"      # >= 2 independent sources cover this node
    SINGLE_SOURCE_COVERED = "SINGLE_SOURCE_COVERED"    # Exactly 1 source covers this node
    ASSESSMENT_ONLY = "ASSESSMENT_ONLY"                # Only present in mock/exam questions
    WEAK_SOURCE_COVERAGE = "WEAK_SOURCE_COVERAGE"      # Mentioned only briefly or implicitly
    NO_SOURCE_FOUND = "NO_SOURCE_FOUND"                # Explicitly missing from source corpus
    SOURCE_CONFLICT = "SOURCE_CONFLICT"                # Sources disagree on sign/form/value
    UNCERTAIN_MAPPING = "UNCERTAIN_MAPPING"            # Ambiguous taxonomy alignment


class SourceMetadataRecord(BaseModel):
    """Complete metadata record for a registered source in the corpus."""
    source_id: str = Field(..., description="Unique deterministic source identifier")
    file_name: str = Field(..., description="Original file name")
    relative_path: str = Field(..., description="Path relative to repository root")
    sha256: str = Field(..., min_length=64, max_length=64, description="Cryptographic SHA-256 hash")
    file_size_bytes: int = Field(..., ge=0)
    page_count: int = Field(..., ge=1)
    source_role: SourceRole = Field(..., description="Role assigned in Phase 11")
    has_extractable_text: bool = Field(False)
    is_image_only: bool = Field(False)
    toc_entries_count: int = Field(0, ge=0)
    bibliographic_info: Dict[str, Any] = Field(default_factory=dict)
    ingestion_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EnhancedSourceSegment(BaseModel):
    """Granular semantic and page-bounded segment of a source document."""
    segment_id: str = Field(..., description="Unique segment identifier")
    source_id: str = Field(..., description="Parent source identifier")
    start_page: int = Field(..., ge=1)
    end_page: int = Field(..., ge=1)
    segment_title: str = Field(..., description="Section or chapter title")
    chapter_title: Optional[str] = Field(None)
    section_number: Optional[str] = Field(None)
    subject_type: str = Field("PHYSICS", description="PHYSICS, MIXED, NON_CONTENT, UNCERTAIN")
    content_types: List[SourceContentType] = Field(default_factory=list)
    extracted_text_snippet: Optional[str] = Field(None, description="Diagnostic text snippet")
    word_count: int = Field(0, ge=0)
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    figure_count: int = Field(0, ge=0)
    equation_count: int = Field(0, ge=0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SourceFormulaRecord(BaseModel):
    """Source-grounded formula extraction record."""
    formula_id: str = Field(..., description="Deterministic formula identifier")
    name_or_title: str = Field(..., description="Descriptive name of the formula")
    canonical_latex: str = Field(..., description="Mathematical LaTeX formula")
    source_id: str = Field(..., description="Originating source ID")
    source_title: str = Field(...)
    segment_id: str = Field(...)
    page_start: int = Field(..., ge=1)
    page_end: int = Field(..., ge=1)
    variables: Dict[str, str] = Field(default_factory=dict, description="Variable symbol -> description")
    units: Dict[str, str] = Field(default_factory=dict, description="Variable symbol -> SI units")
    conditions_assumptions: List[str] = Field(default_factory=list, description="Conditions of validity stated in source")
    related_taxonomy_nodes: List[str] = Field(default_factory=list, description="Taxonomy node IDs")
    verification_status: str = Field("SOURCE_VERIFIED")


class SourceDerivationRecord(BaseModel):
    """Source-grounded physical derivation record."""
    derivation_id: str = Field(..., description="Deterministic derivation identifier")
    title: str = Field(..., description="Title of the derivation")
    source_id: str = Field(...)
    source_title: str = Field(...)
    segment_id: str = Field(...)
    page_start: int = Field(..., ge=1)
    page_end: int = Field(..., ge=1)
    starting_assumptions: List[str] = Field(default_factory=list)
    starting_equations: List[str] = Field(default_factory=list)
    derivation_steps: List[str] = Field(default_factory=list)
    final_equation: str = Field(...)
    related_taxonomy_nodes: List[str] = Field(default_factory=list)


class SourceProblemRecord(BaseModel):
    """Source problem record extracted from textbook or exam source."""
    problem_id: str = Field(...)
    source_id: str = Field(...)
    source_title: str = Field(...)
    segment_id: str = Field(...)
    page_number: int = Field(..., ge=1)
    problem_number_or_label: str = Field(...)
    problem_type: str = Field("EXERCISE", description="EXERCISE, WORKED_EXAMPLE, EXAM_MCQ, EXAM_NUMERICAL, OLYMPIAD")
    problem_statement: str = Field(...)
    options: Optional[Dict[str, str]] = Field(None)
    source_answer: Optional[str] = Field(None)
    source_solution: Optional[str] = Field(None)
    figure_references: List[str] = Field(default_factory=list)
    taxonomy_node_id: str = Field(...)
    difficulty_tier: Optional[str] = Field(None)


class SourceDisagreementRecord(BaseModel):
    """Documented disagreement, notation variance, or convention clash between sources."""
    conflict_id: str = Field(...)
    conflict_category: str = Field(..., description="SIGN_CONVENTION, THERMODYNAMICS_WORK, TERMINOLOGY, VALIDITY_REGIME")
    topic_or_concept: str = Field(...)
    source_a: Dict[str, Any] = Field(..., description="First source details (source_id, segment, text/formula)")
    source_b: Dict[str, Any] = Field(..., description="Second source details (source_id, segment, text/formula)")
    nature_of_disagreement: str = Field(...)
    explanation_and_reconciliation: str = Field(...)
    resolution_status: str = Field("SOURCE_DISAGREEMENT_DOCUMENTED")


class TaxonomyCoverageRecord(BaseModel):
    """Coverage matrix entry for a single taxonomy node."""
    taxonomy_node_id: str = Field(...)
    node_name: str = Field(...)
    level: str = Field(...)
    parent_id: Optional[str] = Field(None)
    source_ids: List[str] = Field(default_factory=list)
    segment_ids: List[str] = Field(default_factory=list)
    concept_count: int = Field(0, ge=0)
    formula_count: int = Field(0, ge=0)
    derivation_count: int = Field(0, ge=0)
    example_count: int = Field(0, ge=0)
    problem_count: int = Field(0, ge=0)
    exam_question_count: int = Field(0, ge=0)
    multi_source: bool = Field(False)
    coverage_status: CoverageStatus = Field(...)
    explicit_gaps: List[str] = Field(default_factory=list)
    corroborated_sources: List[str] = Field(default_factory=list)


class SourceCoverageMatrixReport(BaseModel):
    """Complete Source x Taxonomy Coverage Report."""
    report_id: str = Field(...)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_taxonomy_nodes: int = Field(..., ge=0)
    status_counts: Dict[str, int] = Field(default_factory=dict)
    source_coverage_summary: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    multi_source_nodes_count: int = Field(0, ge=0)
    single_source_nodes_count: int = Field(0, ge=0)
    gap_nodes_count: int = Field(0, ge=0)
    nodes: Dict[str, TaxonomyCoverageRecord] = Field(default_factory=dict)


class SourceLibraryIndex(BaseModel):
    """Browsable machine-readable source index for the entire Physics corpus."""
    index_id: str = Field(...)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_sources: int = Field(..., ge=1)
    total_pages: int = Field(..., ge=1)
    total_segments: int = Field(..., ge=1)
    total_formulas: int = Field(0, ge=0)
    total_derivations: int = Field(0, ge=0)
    total_problems: int = Field(0, ge=0)
    sources: List[SourceMetadataRecord] = Field(default_factory=list)
    segments_by_source: Dict[str, List[EnhancedSourceSegment]] = Field(default_factory=dict)
    taxonomy_coverage_summary: Dict[str, Any] = Field(default_factory=dict)
    disagreements: List[SourceDisagreementRecord] = Field(default_factory=list)
