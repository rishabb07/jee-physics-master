import json
from pathlib import Path
from typing import Dict, Type
from pydantic import BaseModel

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.curriculum import (
    ChapterPlan,
    ChapterSpec,
    ConceptPlacement,
    CurriculumAuditRecord,
    CurriculumGapReport,
    CurriculumNode,
    FormulaRecord,
    MisconceptionRecord,
    MockTestSpec,
    QuestionLadder,
    QuestionPlacement,
    WorkedExampleRecord,
)
from jee_physics.models.dedup import (
    CanonicalMapping,
    DedupCandidate,
    DedupCluster,
    DedupDecision,
    DedupRecord,
    NormalizedAtomFingerprint,
)
from jee_physics.models.manifest import JobManifest
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.models.review import ReviewQueueItem
from jee_physics.models.source import (
    PageContentRepresentation,
    SourcePageInventory,
    SourceRegistryRecord,
    SourceSegment,
    SourceSegmentationPlan,
)
from jee_physics.models.verification import VerificationRecord
from jee_physics.models.taxonomy import TaxonomyNode, TaxonomyTree, TaxonomyAssignment
from jee_physics.models.subject import SubjectClassificationRecord, SubjectAuditReport

from jee_physics.models.content import (
    ChapterContentBlock,
    ChapterQAReport,
    ConceptExplanation,
    ContentRequirementReport,
    ContentVerificationRecord,
    DerivationRecord,
    DualVerificationRecord,
    MisconceptionContentRecord,
    RenderingQAReport,
    WorkedExampleContentRecord,
)

SCHEMAS_MAP: Dict[str, Type[BaseModel]] = {
    "source.schema.json": SourceRegistryRecord,
    "source_segment.schema.json": SourceSegment,
    "source_page_inventory.schema.json": SourcePageInventory,
    "source_segmentation_plan.schema.json": SourceSegmentationPlan,
    "page_content_representation.schema.json": PageContentRepresentation,
    "atom.schema.json": KnowledgeAtom,
    "provenance.schema.json": ProvenanceRecord,
    "dedup.schema.json": DedupRecord,
    "dedup_candidate.schema.json": DedupCandidate,
    "dedup_decision.schema.json": DedupDecision,
    "dedup_cluster.schema.json": DedupCluster,
    "canonical_mapping.schema.json": CanonicalMapping,
    "normalized_atom_fingerprint.schema.json": NormalizedAtomFingerprint,
    "verification.schema.json": VerificationRecord,
    "review.schema.json": ReviewQueueItem,
    "chapter_spec.schema.json": ChapterSpec,
    "chapter_plan.schema.json": ChapterPlan,
    "curriculum_node.schema.json": CurriculumNode,
    "concept_placement.schema.json": ConceptPlacement,
    "question_placement.schema.json": QuestionPlacement,
    "question_ladder.schema.json": QuestionLadder,
    "formula_record.schema.json": FormulaRecord,
    "worked_example_record.schema.json": WorkedExampleRecord,
    "misconception_record.schema.json": MisconceptionRecord,
    "curriculum_audit_record.schema.json": CurriculumAuditRecord,
    "curriculum_gap_report.schema.json": CurriculumGapReport,
    "mock_spec.schema.json": MockTestSpec,
    "job_manifest.schema.json": JobManifest,
    "taxonomy_node.schema.json": TaxonomyNode,
    "taxonomy_tree.schema.json": TaxonomyTree,
    "taxonomy_assignment.schema.json": TaxonomyAssignment,
    "subject_classification.schema.json": SubjectClassificationRecord,
    "subject_audit_report.schema.json": SubjectAuditReport,
    "concept_explanation.schema.json": ConceptExplanation,
    "derivation_record.schema.json": DerivationRecord,
    "worked_example_content_record.schema.json": WorkedExampleContentRecord,
    "misconception_content_record.schema.json": MisconceptionContentRecord,
    "chapter_content_block.schema.json": ChapterContentBlock,
    "content_requirement_report.schema.json": ContentRequirementReport,
    "content_verification_record.schema.json": ContentVerificationRecord,
    "dual_verification_record.schema.json": DualVerificationRecord,
    "chapter_qa_report.schema.json": ChapterQAReport,
    "rendering_qa_report.schema.json": RenderingQAReport,
}


def generate_all_schemas(output_dir: Path) -> Dict[str, Path]:
    """Generates JSON Schema files directly from authoritative Pydantic models."""
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files: Dict[str, Path] = {}

    for file_name, model_cls in SCHEMAS_MAP.items():
        schema_dict = model_cls.model_json_schema()
        schema_path = output_dir / file_name
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(schema_dict, f, indent=2)
        generated_files[file_name] = schema_path

    return generated_files


if __name__ == "__main__":
    schemas_dir = Path(__file__).resolve().parent.parent.parent.parent / "schemas"
    results = generate_all_schemas(schemas_dir)
    print(f"Generated {len(results)} JSON schemas in {schemas_dir}")
