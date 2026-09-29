"""Content Requirement Extraction Engine for Phase 8.

Inspects approved ChapterSpecs and ChapterPlans to extract formal, granular
content generation requirements and identify missing source/content gaps.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Dict, List, Optional, Set

from jee_physics.models.curriculum import ChapterPlan, ChapterSpec
from jee_physics.models.content import (
    ContentBlockType,
    ContentRequirement,
    ContentRequirementReport,
    ContentRiskLevel,
)
from jee_physics.storage.io import safe_write_json


def extract_content_requirements(
    chapters_dir: Path,
    kb_atoms_dir: Path,
    output_path: Optional[Path] = None,
) -> ContentRequirementReport:
    """Extracts granular content generation requirements from approved ChapterSpecs and ChapterPlans."""
    requirements: List[ContentRequirement] = []
    gaps_count = 0

    # Index existing canonical atoms
    canonical_atom_ids: Set[str] = set()
    if kb_atoms_dir.exists():
        for af in kb_atoms_dir.glob("*.json"):
            if not af.name.startswith("."):
                canonical_atom_ids.add(af.stem)

    # Process all chapter specs
    spec_files = sorted(list(chapters_dir.glob("*_spec.json")))

    for sfile in spec_files:
        with open(sfile, "r", encoding="utf-8") as f:
            spec_data = json.load(f)
        spec = ChapterSpec.model_validate(spec_data)
        chap_id = spec.chapter_id

        # Load corresponding plan if available
        plan_file = chapters_dir / f"{chap_id}_plan.json"
        plan: Optional[ChapterPlan] = None
        if plan_file.exists():
            with open(plan_file, "r", encoding="utf-8") as f:
                plan_data = json.load(f)
            plan = ChapterPlan.model_validate(plan_data)

        # 1. Concept Explanations Requirements
        for idx, cp in enumerate(spec.concept_sequence):
            can_kb = any(aid in canonical_atom_ids for aid in cp.source_atom_ids)
            req = ContentRequirement(
                requirement_id=f"req-{chap_id}-concept-{cp.concept_id}",
                chapter_id=chap_id,
                section_id=f"sec-{chap_id}-{idx + 1:02d}",
                content_type=ContentBlockType.CONCEPT_EXPLANATION,
                curriculum_node_id=cp.curriculum_id,
                objective=f"Explain concept '{cp.concept_id}' with physical intuition and formal definition",
                required_source_refs=cp.source_atom_ids or [cp.source_evidence],
                required_prerequisites=[cp.prerequisite_relationship] if cp.prerequisite_relationship else [],
                needs_physics_verification=True,
                can_generate_from_kb=can_kb,
                is_unresolved_gap=False,
                risk_level=ContentRiskLevel.MEDIUM,
            )
            requirements.append(req)

        # 2. Formula & Derivation Requirements
        for f_rec in spec.formula_sequence:
            # Formula specification
            req_f = ContentRequirement(
                requirement_id=f"req-{chap_id}-formula-{f_rec.formula_id}",
                chapter_id=chap_id,
                section_id=f"sec-{chap_id}-formula",
                content_type=ContentBlockType.FORMULA,
                curriculum_node_id=f_rec.related_concept_ids[0] if f_rec.related_concept_ids else f"curr-{chap_id}",
                objective=f"Formalize equation and validity conditions for '{f_rec.title}'",
                required_source_refs=[f_rec.formula_id],
                required_prerequisites=f_rec.related_concept_ids,
                needs_physics_verification=True,
                can_generate_from_kb=True,
                is_unresolved_gap=False,
                risk_level=ContentRiskLevel.MEDIUM,
            )
            requirements.append(req_f)

            # High-risk Derivation requirement
            req_d = ContentRequirement(
                requirement_id=f"req-{chap_id}-derivation-{f_rec.formula_id}",
                chapter_id=chap_id,
                section_id=f"sec-{chap_id}-derivation",
                content_type=ContentBlockType.DERIVATION,
                curriculum_node_id=f_rec.related_concept_ids[0] if f_rec.related_concept_ids else f"curr-{chap_id}",
                objective=f"Derive '{f_rec.title}' ({f_rec.equation_latex}) from first principles",
                required_source_refs=f_rec.derivation_links or [f_rec.formula_id],
                required_prerequisites=f_rec.related_concept_ids,
                needs_physics_verification=True,
                can_generate_from_kb=False,
                is_unresolved_gap=False,
                risk_level=ContentRiskLevel.HIGH,
            )
            requirements.append(req_d)

        # 3. Worked Example Requirements
        for ex in spec.worked_example_sequence:
            can_kb = ex.source_atom_id in canonical_atom_ids if ex.source_atom_id else False
            req_ex = ContentRequirement(
                requirement_id=f"req-{chap_id}-example-{ex.example_id}",
                chapter_id=chap_id,
                section_id=f"sec-{chap_id}-examples",
                content_type=ContentBlockType.WORKED_EXAMPLE,
                curriculum_node_id=f"curr-{chap_id}",
                objective=f"Structured worked example for target '{ex.target_quantity}': {ex.solution_strategy[:60]}...",
                required_source_refs=[ex.source_atom_id] if ex.source_atom_id else [],
                required_prerequisites=ex.relevant_concepts,
                needs_physics_verification=True,
                can_generate_from_kb=can_kb,
                is_unresolved_gap=False,
                risk_level=ContentRiskLevel.HIGH if not can_kb else ContentRiskLevel.MEDIUM,
            )
            requirements.append(req_ex)

        # 4. Misconception Inoculation Requirements
        for misc in spec.misconception_sequence:
            req_misc = ContentRequirement(
                requirement_id=f"req-{chap_id}-misc-{misc.misconception_id}",
                chapter_id=chap_id,
                section_id=f"sec-{chap_id}-misconceptions",
                content_type=ContentBlockType.MISCONCEPTION,
                curriculum_node_id=f"curr-{chap_id}",
                objective=f"Misconception inoculation ({misc.category}): {misc.statement[:60]}...",
                required_source_refs=misc.connected_atom_ids,
                required_prerequisites=misc.connected_concept_ids,
                needs_physics_verification=True,
                can_generate_from_kb=len(misc.connected_atom_ids) > 0,
                is_unresolved_gap=False,
                risk_level=ContentRiskLevel.MEDIUM,
            )
            requirements.append(req_misc)

        # 5. Unresolved Gaps from ChapterPlan
        if plan and plan.unresolved_gaps:
            for g_idx, gap_desc in enumerate(plan.unresolved_gaps):
                gaps_count += 1
                req_gap = ContentRequirement(
                    requirement_id=f"req-{chap_id}-gap-{g_idx + 1:02d}",
                    chapter_id=chap_id,
                    section_id=f"sec-{chap_id}-gap",
                    content_type=ContentBlockType.CONCEPT_EXPLANATION,
                    curriculum_node_id=f"curr-{chap_id}",
                    objective=gap_desc,
                    required_source_refs=[],
                    required_prerequisites=[],
                    needs_physics_verification=True,
                    can_generate_from_kb=False,
                    is_unresolved_gap=True,
                    risk_level=ContentRiskLevel.HIGH,
                )
                requirements.append(req_gap)

    report = ContentRequirementReport(
        report_id=f"content-reqs-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        requirements_count=len(requirements),
        gaps_count=gaps_count,
        requirements=requirements,
        generated_at=datetime.now(timezone.utc),
    )

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        safe_write_json(output_path, report)

    return report
