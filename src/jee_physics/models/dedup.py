from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DedupDecisionClass(str, Enum):
    """Authoritative decision classes for physical and mathematical deduplication."""
    EXACT_DUPLICATE = "EXACT_DUPLICATE"
    SEMANTIC_DUPLICATE = "SEMANTIC_DUPLICATE"
    SAME_CONCEPT_DIFFERENT_PROBLEM = "SAME_CONCEPT_DIFFERENT_PROBLEM"
    MULTI_METHOD_SAME_PROBLEM = "MULTI_METHOD_SAME_PROBLEM"
    RELATED_BUT_DISTINCT = "RELATED_BUT_DISTINCT"
    UNCERTAIN = "UNCERTAIN"


class DedupAction(str, Enum):
    """Deterministic actions resulting from deduplication evaluation."""
    MERGE = "MERGE"
    KEEP_SEPARATE = "KEEP_SEPARATE"
    REVIEW = "REVIEW"


class NormalizedAtomFingerprint(BaseModel):
    """Deterministic auxiliary fingerprint of an atom without mutating source truth."""
    atom_id: str = Field(..., min_length=1, description="Original atom ID")
    statement_normalized: str = Field(..., description="Cleaned, normalized statement")
    statement_hash: str = Field(..., min_length=16, description="SHA-256 of normalized statement")
    options_normalized: Optional[List[str]] = Field(None, description="Normalized option texts if present")
    options_hash: Optional[str] = Field(None, description="SHA-256 of combined normalized options")
    problem_hash: str = Field(..., min_length=16, description="SHA-256 of full problem statement + options")
    taxonomy_node: Optional[str] = Field(None, description="Combined chapter/topic/subtopic slug")
    chapter_id: Optional[str] = Field(None, description="Taxonomy chapter ID")
    topic_id: Optional[str] = Field(None, description="Taxonomy topic ID")
    subtopic_id: Optional[str] = Field(None, description="Taxonomy subtopic ID")
    question_type: Optional[str] = Field(None, description="e.g. MCQ, NUMERICAL")
    target_quantity: Optional[str] = Field(None, description="Physical quantity sought e.g. time_period, acceleration")
    numerical_values: List[str] = Field(default_factory=list, description="Extracted numerical constants/values")
    has_figure: bool = Field(False, description="Whether problem requires or includes a figure")
    physics_skeleton_hash: str = Field(..., description="Abstracted structural hash of variables and target")


class ComparisonFeatures(BaseModel):
    """Explicit physical/mathematical comparison dimensions."""
    same_physical_setup: Optional[bool] = None
    same_given_information: Optional[bool] = None
    same_constraints: Optional[bool] = None
    same_target: Optional[bool] = None
    same_solution_structure: Optional[bool] = None
    same_answer_structure: Optional[bool] = None
    same_diagram_role: Optional[bool] = None
    notation_only_difference: Optional[bool] = None
    wording_only_difference: Optional[bool] = None
    numerical_substitution_only: Optional[bool] = None
    material_problem_difference: Optional[bool] = None


class DedupCandidate(BaseModel):
    """A pair of atoms staged for deduplication comparison."""
    candidate_id: str = Field(..., min_length=1, description="Unique candidate identifier")
    atom_a_id: str = Field(..., min_length=1, description="First atom ID")
    atom_b_id: str = Field(..., min_length=1, description="Second atom ID")
    generation_method: str = Field(..., description="e.g. EXACT_HASH_MATCH, TAXONOMY_BLOCKING, FEATURE_BLOCKING")
    blocking_signals: List[str] = Field(default_factory=list, description="Signals that triggered this candidate pairing")
    atom_a_fingerprint: Optional[NormalizedAtomFingerprint] = None
    atom_b_fingerprint: Optional[NormalizedAtomFingerprint] = None
    comparison_features: Dict[str, Any] = Field(default_factory=dict, description="Structured physical comparison features")
    candidate_metadata: Dict[str, Any] = Field(default_factory=dict, description="Source provenance and context")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DedupDecision(BaseModel):
    """Cognitive decision produced by the physics-deduplicator subagent."""
    candidate_id: str = Field(..., min_length=1, description="Target candidate ID")
    decision_class: DedupDecisionClass = Field(..., description="Decision classification")
    duplicate_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this classification")
    same_underlying_problem: bool = Field(..., description="True if mathematically the identical problem")
    same_concept_only: bool = Field(..., description="True if only shares physics concepts but different questions")
    rationale: str = Field(..., min_length=1, description="Detailed physical/mathematical justification")
    distinguishing_evidence: Optional[str] = Field(None, description="Differences in givens, target, or physics")
    recommended_action: DedupAction = Field(..., description="MERGE, KEEP_SEPARATE, or REVIEW")
    agent_identity: str = Field("physics-deduplicator", description="Agent that performed evaluation")
    agent_conversation_id: str = Field(..., description="Subagent conversation ID for chain-of-custody")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None


class PreservedProvenance(BaseModel):
    """Immutable provenance record preserved across all deduplicated source occurrences."""
    atom_id: str
    source_id: str
    file_name: str
    file_path: Optional[str] = None
    page_start: int
    page_end: int
    source_locator: Optional[str] = None
    edition: Optional[str] = None
    source_claimed_answer: Optional[str] = None
    original_statement: Optional[str] = None
    extraction_metadata: Dict[str, Any] = Field(default_factory=dict)


class PreservedSolutionMethod(BaseModel):
    """A distinct solution method preserved under the canonical problem."""
    method_id: str
    source_atom_id: str
    source_id: Optional[str] = None
    method_name: str
    steps: str
    source_attributed: bool = True
    verified: bool = True


class DedupCluster(BaseModel):
    """An equivalence cluster mapping multiple source occurrences to one canonical representative."""
    cluster_id: str = Field(..., min_length=1, description="Unique cluster identifier")
    canonical_atom_id: str = Field(..., min_length=1, description="Deterministically selected canonical atom ID")
    member_atom_ids: List[str] = Field(..., min_length=1, description="All member atoms in this cluster")
    cluster_type: DedupDecisionClass = Field(..., description="Class of equivalence")
    cluster_confidence: float = Field(..., ge=0.0, le=1.0)
    decision_ids: List[str] = Field(default_factory=list, description="IDs of deduplication decisions")
    preserved_provenance: List[Dict[str, Any]] = Field(default_factory=list, description="All preserved source provenance records")
    preserved_solution_methods: List[Dict[str, Any]] = Field(default_factory=list, description="All preserved solution methods")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CanonicalMapping(BaseModel):
    """Immutable persistent mapping from an original atom to its canonical representative."""
    original_atom_id: str = Field(..., min_length=1)
    canonical_atom_id: str = Field(..., min_length=1)
    cluster_id: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)
    decision_id: str = Field(..., min_length=1)
    classifier_identity: str = Field(...)
    conversation_id: str = Field(...)
    source_provenance: List[Dict[str, Any]] = Field(default_factory=list)
    atom_version: int = Field(1, ge=1)
    content_hash: str = Field(..., min_length=16)
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DedupAuditJournalRecord(BaseModel):
    """Journal entry recorded in kb/dedup/audit_journal.jsonl."""
    entry_id: str
    action_type: str  # CLUSTER_CREATED, MAPPING_REGISTERED, REVIEW_ROUTED, MERGE_REJECTED
    cluster_id: Optional[str] = None
    canonical_atom_id: Optional[str] = None
    candidate_id: Optional[str] = None
    decision_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Legacy compatibility models
class DedupVariant(BaseModel):
    source_id: str = Field(..., description="Source document where this duplicate appeared")
    source_locator: Optional[str] = Field(None, description="Page / Problem number in that source")
    notation_notes: Optional[str] = Field(None, description="Any notation differences (e.g. angle alpha vs theta)")
    solution_difference: Optional[str] = Field(None, description="Summary if the source provided an alternative solution")


class DedupRecord(BaseModel):
    duplicate_group_id: str = Field(..., min_length=1, description="Unique cluster identifier")
    canonical_atom_id: str = Field(..., min_length=1, description="Primary atom representing this equivalence class")
    reason: str = Field(..., description="Explanation of why these atoms are identical physical problems")
    variants: List[DedupVariant] = Field(default_factory=list, description="All known source occurrences")
    keep_both_solutions: bool = Field(True, description="True if distinct solution methods should both be retained")
    merge_action: str = Field("CANONICAL_WITH_MULTI_PROVENANCE")
    status: str = Field("APPROVED", description="PENDING_REVIEW, APPROVED, REJECTED")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
