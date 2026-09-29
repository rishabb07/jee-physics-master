from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, model_validator


class SubjectType(str, Enum):
    """Authoritative subject-level domain boundaries."""
    PHYSICS = "PHYSICS"
    CHEMISTRY = "CHEMISTRY"
    MATHEMATICS = "MATHEMATICS"
    NON_CONTENT = "NON_CONTENT"
    OTHER = "OTHER"
    MIXED = "MIXED"
    UNCERTAIN = "UNCERTAIN"


class NodeProvenanceClass(str, Enum):
    """Authority/provenance classification for a taxonomy node."""
    OFFICIAL_EXAM_COVERAGE = "OFFICIAL_EXAM_COVERAGE"      # Explicitly in official JEE syllabus brochure
    PEDAGOGICAL_GROUPING = "PEDAGOGICAL_GROUPING"          # Standard pedagogical grouping from build guide/textbooks
    EXTENSION_OLYMPIAD = "EXTENSION_OLYMPIAD"              # Advanced extension beyond standard JEE syllabus
    INFERRED_ORGANIZATION = "INFERRED_ORGANIZATION"        # Inferred subtopic clustering for atom variants


class SyllabusSourceAuthority(str, Enum):
    """Authoritative institutions or specifications justifying coverage."""
    JEE_ADVANCED = "JEE_ADVANCED"
    JEE_MAIN = "JEE_MAIN"
    PROJECT_BUILD_GUIDE = "PROJECT_BUILD_GUIDE"
    OLYMPIAD = "OLYMPIAD"


class SyllabusSource(BaseModel):
    """Specific official syllabus document or brochure reference."""
    authority: SyllabusSourceAuthority = Field(..., description="Authority justifying syllabus presence")
    edition: Optional[str] = Field(None, description="Syllabus edition or year (e.g. '2026', 'BUILD_GUIDE_V2')")
    document_ref: Optional[str] = Field(None, description="Official syllabus document or brochure section reference")


class TaxonomyLevel(str, Enum):
    """Hierarchy depth levels within the syllabus tree."""
    SUBJECT = "SUBJECT"
    CHAPTER = "CHAPTER"
    TOPIC = "TOPIC"
    SUBTOPIC = "SUBTOPIC"
    EXTENSION = "EXTENSION"


LEVEL_ORDER: Dict[TaxonomyLevel, int] = {
    TaxonomyLevel.SUBJECT: 0,
    TaxonomyLevel.CHAPTER: 1,
    TaxonomyLevel.TOPIC: 2,
    TaxonomyLevel.SUBTOPIC: 3,
    TaxonomyLevel.EXTENSION: 4,
}


class TaxonomyNode(BaseModel):
    """A node in the authoritative syllabus taxonomy hierarchy."""
    id: str = Field(..., min_length=1, description="Stable, permanent slug ID (e.g. 'kinematics')")
    name: str = Field(..., min_length=1, description="Display name / title")
    level: TaxonomyLevel = Field(..., description="Hierarchy level")
    parent_id: Optional[str] = Field(None, description="Parent node ID. None only for the root subject node")
    subject: SubjectType = Field(SubjectType.PHYSICS, description="Parent subject classification")
    aliases: List[str] = Field(default_factory=list, description="Alternative recognized slugs / historical IDs")
    description: Optional[str] = Field(None, description="Scope definition or syllabus boundary")
    prerequisites: List[str] = Field(default_factory=list, description="IDs of prerequisite taxonomy nodes")
    provenance_class: NodeProvenanceClass = Field(NodeProvenanceClass.PEDAGOGICAL_GROUPING, description="Provenance category of this node")
    syllabus_sources: List[SyllabusSource] = Field(default_factory=list, description="Official or authoritative source citations justifying this node")
    extension_olympiad: bool = Field(False, description="True if beyond standard JEE syllabus (Olympiad / Irodov tier)")
    active: bool = Field(True, description="False if deprecated or decommissioned")
    order: int = Field(1, ge=1, description="Curriculum presentation order among siblings")


class TaxonomyTree(BaseModel):
    """Authoritative, fully-validated syllabus taxonomy tree."""
    schema_version: str = Field("1.0.0", description="Schema version of this taxonomy")
    root_id: str = Field("physics", description="ID of the root subject node")
    nodes: Dict[str, TaxonomyNode] = Field(..., description="Dictionary mapping node_id -> TaxonomyNode")

    @model_validator(mode="after")
    def validate_tree_integrity(self) -> "TaxonomyTree":
        nodes = self.nodes

        # 1. Root check
        if self.root_id not in nodes:
            raise ValueError(f"Root node '{self.root_id}' is not present in nodes dictionary.")

        root = nodes[self.root_id]
        if root.level != TaxonomyLevel.SUBJECT:
            raise ValueError(f"Root node '{self.root_id}' must have level SUBJECT, found '{root.level}'.")
        if root.parent_id is not None:
            raise ValueError(f"Root node '{self.root_id}' cannot have a parent_id (found '{root.parent_id}').")

        # 2. Exactly one root node
        root_nodes = [nid for nid, n in nodes.items() if n.parent_id is None]
        if len(root_nodes) != 1 or root_nodes[0] != self.root_id:
            raise ValueError(
                f"Taxonomy tree must have exactly one root with parent_id=None. Found roots: {root_nodes}"
            )

        # 3. Check node IDs match keys
        for nid, n in nodes.items():
            if n.id != nid:
                raise ValueError(f"Node dictionary key '{nid}' does not match node.id '{n.id}'.")

        # 4. Alias collision check
        all_ids: Set[str] = set(nodes.keys())
        all_aliases: Dict[str, str] = {}
        for nid, n in nodes.items():
            for alias in n.aliases:
                if alias in all_ids:
                    raise ValueError(f"Alias '{alias}' on node '{nid}' collides with existing node ID.")
                if alias in all_aliases:
                    raise ValueError(
                        f"Alias '{alias}' on node '{nid}' collides with alias on node '{all_aliases[alias]}'."
                    )
                all_aliases[alias] = nid

        # 5. Parent reference and level hierarchy check
        for nid, n in nodes.items():
            if nid == self.root_id:
                continue

            if not n.parent_id:
                raise ValueError(f"Non-root node '{nid}' is missing parent_id.")
            if n.parent_id not in nodes:
                raise ValueError(f"Node '{nid}' references non-existent parent_id '{n.parent_id}'.")

            parent = nodes[n.parent_id]
            allowed_child_levels = {
                TaxonomyLevel.SUBJECT: {TaxonomyLevel.CHAPTER},
                TaxonomyLevel.CHAPTER: {TaxonomyLevel.TOPIC, TaxonomyLevel.EXTENSION},
                TaxonomyLevel.TOPIC: {TaxonomyLevel.SUBTOPIC, TaxonomyLevel.EXTENSION},
                TaxonomyLevel.SUBTOPIC: set(),
                TaxonomyLevel.EXTENSION: set(),
            }
            if n.level not in allowed_child_levels.get(parent.level, set()):
                raise ValueError(
                    f"Invalid parent-child level hierarchy: Child '{nid}' ({n.level.value}) cannot be a child of "
                    f"'{parent.id}' ({parent.level.value})."
                )

        # 6. Cycle detection
        for nid in nodes:
            visited = set()
            curr = nid
            while curr is not None:
                if curr in visited:
                    raise ValueError(f"Cycle detected in taxonomy tree involving node '{curr}'.")
                visited.add(curr)
                curr_node = nodes.get(curr)
                curr = curr_node.parent_id if curr_node else None

        # 7. Prerequisites reference validation
        for nid, n in nodes.items():
            for prereq in n.prerequisites:
                if prereq not in nodes and prereq not in all_aliases:
                    raise ValueError(f"Node '{nid}' references undefined prerequisite '{prereq}'.")

        return self

    def resolve_node_id(self, identifier: str) -> Optional[str]:
        """Resolves a node ID or alias to the canonical node ID."""
        if identifier in self.nodes:
            return identifier
        for nid, n in self.nodes.items():
            if identifier in n.aliases:
                return nid
        return None

    def get_node(self, identifier: str) -> Optional[TaxonomyNode]:
        """Gets a TaxonomyNode by ID or alias."""
        canonical_id = self.resolve_node_id(identifier)
        return self.nodes.get(canonical_id) if canonical_id else None


class TaxonomyAssignment(BaseModel):
    """Proposed or approved mapping of an atom into the taxonomy."""
    atom_id: str = Field(..., min_length=1, description="Target atom ID")
    chapter_id: str = Field(..., min_length=1, description="Canonical chapter ID in taxonomy")
    topic_id: str = Field(..., min_length=1, description="Canonical topic ID in taxonomy")
    subtopic_id: Optional[str] = Field(None, description="Optional canonical subtopic ID in taxonomy")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this classification")
    rationale: str = Field(..., min_length=1, description="Physical and pedagogical reasoning for this taxonomy placement")
    status: str = Field("PROPOSED", description="PROPOSED, APPROVED, or UNMAPPED")
    notes: Optional[str] = Field(None, description="Caveats, cross-topic overlaps, or audit notes")


class TaxonomyAuditRecord(BaseModel):
    """Immutable persistent audit entry for an applied taxonomy assignment."""
    audit_id: str = Field(..., description="Unique ID for this audit record")
    atom_id: str = Field(..., description="Target atom ID")
    atom_version: int = Field(1, description="Version of the atom at the time of classification")
    content_hash: str = Field(..., description="Content hash of the atom at the time of classification")
    taxonomy_schema_version: str = Field("1.0.0", description="Schema version of the syllabus tree used")
    chapter_id: str = Field(..., description="Assigned canonical chapter ID")
    topic_id: str = Field(..., description="Assigned canonical topic ID")
    subtopic_id: Optional[str] = Field(None, description="Assigned canonical subtopic ID")
    previous_taxonomy: Optional[Dict[str, Optional[str]]] = Field(None, description="Previous taxonomy before update")
    classifier_identity: str = Field(..., description="Agent or subagent name that performed classification")
    classifier_conversation_id: Optional[str] = Field(None, description="Subagent conversation ID")
    rationale: str = Field(..., description="Pedagogical and syllabus justification")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence score")
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of when assignment was applied")
    status: str = Field("APPROVED", description="Status of the audit record")
