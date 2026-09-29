import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import yaml

from jee_physics.models.enums import AtomType, DifficultyLevel
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.taxonomy import TaxonomyLevel, TaxonomyTree
from jee_physics.models.curriculum import (
    CurriculumGapItem,
    CurriculumGapReport,
    GapCategory,
)
from jee_physics.curriculum.prerequisites import CurriculumPrerequisiteDAG
from jee_physics.storage.io import safe_write_json


def analyze_curriculum_coverage(
    syllabus_path: Path,
    kb_atoms_dir: Path,
    chapter_specs_dir: Optional[Path] = None,
    review_queue_dir: Optional[Path] = None,
    output_report_path: Optional[Path] = None,
    prerequisite_dag: Optional[CurriculumPrerequisiteDAG] = None,
) -> CurriculumGapReport:
    """Analyzes multi-level curriculum coverage and produces a deterministic CurriculumGapReport.
    
    Distinguishes between mere atom presence and genuine pedagogical coverage (explanations,
    worked examples, basic practice, advanced synthesis, and prerequisite mapping).
    """
    # 1. Load Taxonomy Tree
    with open(syllabus_path, "r", encoding="utf-8") as f:
        syllabus_data = yaml.safe_load(f)
    tree = TaxonomyTree.model_validate(syllabus_data)

    # 2. Index Canonical Atoms in kb/atoms/
    atoms_by_node: Dict[str, List[KnowledgeAtom]] = defaultdict(list)
    atoms_by_chapter: Dict[str, List[KnowledgeAtom]] = defaultdict(list)
    total_canonical_atoms = 0

    if kb_atoms_dir.exists():
        for atom_file in kb_atoms_dir.glob("*.json"):
            if atom_file.name.startswith("."):
                continue
            try:
                with open(atom_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                atom = KnowledgeAtom.model_validate(data)
                total_canonical_atoms += 1

                chap = atom.taxonomy.chapter_id
                top = atom.taxonomy.topic_id
                sub = atom.taxonomy.subtopic_id

                atoms_by_chapter[chap].append(atom)
                atoms_by_node[chap].append(atom)
                if top:
                    atoms_by_node[top].append(atom)
                if sub:
                    atoms_by_node[sub].append(atom)
            except Exception:
                continue

    # 3. Index Review Queue items
    review_blocked_chapters: Set[str] = set()
    review_blocked_nodes: Set[str] = set()
    if review_queue_dir and review_queue_dir.exists():
        for r_file in review_queue_dir.rglob("*.json"):
            try:
                with open(r_file, "r", encoding="utf-8") as f:
                    r_data = json.load(f)
                # Check for chapter or atom references
                candidate_id = r_data.get("candidate_id", "")
                atom_id = r_data.get("atom_id", "")
                for chap_id in tree.nodes:
                    if chap_id in candidate_id or chap_id in atom_id:
                        review_blocked_chapters.add(chap_id)
            except Exception:
                continue

    # 4. Generate Gap Items & Pedagogical Breakdown
    gap_items: List[CurriculumGapItem] = []
    gaps_by_category: Dict[str, int] = defaultdict(int)

    nodes_covered = 0
    nodes_empty = 0
    nodes_light = 0

    content_exists_nodes = 0
    explanation_exists_nodes = 0
    worked_example_nodes = 0
    basic_practice_nodes = 0
    advanced_synthesis_nodes = 0
    prereq_mapped_nodes = 0
    fully_pedagogically_covered_nodes = 0

    excluded_nodes = ["physics"]

    dag_taxonomy_refs: Set[str] = set()
    if prerequisite_dag:
        for cnode in prerequisite_dag.nodes.values():
            dag_taxonomy_refs.add(cnode.curriculum_id)
            if cnode.taxonomy_reference:
                if cnode.taxonomy_reference.chapter_id:
                    dag_taxonomy_refs.add(cnode.taxonomy_reference.chapter_id)
                if cnode.taxonomy_reference.topic_id:
                    dag_taxonomy_refs.add(cnode.taxonomy_reference.topic_id)
                if cnode.taxonomy_reference.subtopic_id:
                    dag_taxonomy_refs.add(cnode.taxonomy_reference.subtopic_id)

    for nid, node in tree.nodes.items():
        if node.level == TaxonomyLevel.SUBJECT:
            continue

        parent_chapter = node.id if node.level == TaxonomyLevel.CHAPTER else node.parent_id
        # Resolve parent chapter slug up to root
        curr_node = node
        while curr_node and curr_node.level not in (TaxonomyLevel.CHAPTER, TaxonomyLevel.SUBJECT):
            if curr_node.parent_id and curr_node.parent_id in tree.nodes:
                curr_node = tree.nodes[curr_node.parent_id]
            else:
                break
        chapter_slug = curr_node.id if curr_node and curr_node.level == TaxonomyLevel.CHAPTER else "physics"

        node_atoms = atoms_by_node.get(nid, [])
        atom_count = len(node_atoms)

        if prerequisite_dag and (nid in prerequisite_dag.nodes or nid in dag_taxonomy_refs):
            prereq_mapped_nodes += 1

        if atom_count == 0:
            nodes_empty += 1
            if node.level in (TaxonomyLevel.TOPIC, TaxonomyLevel.SUBTOPIC):
                gap_items.append(
                    CurriculumGapItem(
                        gap_id=f"gap-empty-{nid}",
                        taxonomy_node_id=nid,
                        chapter_id=chapter_slug,
                        gap_category=GapCategory.NO_CONTENT,
                        description=f"Taxonomy node '{nid}' ({node.name}) has 0 canonical knowledge atoms.",
                        severity="WARNING" if not node.extension_olympiad else "INFO",
                        remediation_action=f"Extract and verify foundational content for '{node.name}'.",
                    )
                )
                gaps_by_category[GapCategory.NO_CONTENT.value] += 1
        else:
            nodes_covered += 1
            content_exists_nodes += 1
            if atom_count == 1:
                nodes_light += 1

            # Pedagogical breakdown
            theories = [a for a in node_atoms if a.atom_type in (AtomType.THEORY, AtomType.INSIGHT)]
            worked_examples = [a for a in node_atoms if a.atom_type == AtomType.SOLVED_EXAMPLE]
            questions = [a for a in node_atoms if a.atom_type == AtomType.QUESTION]
            basic_questions = [
                q for q in questions
                if q.question and q.question.difficulty in (DifficultyLevel.L1, DifficultyLevel.L2)
            ]
            advanced_questions = [
                q for q in questions
                if q.question and q.question.difficulty in (DifficultyLevel.L4, DifficultyLevel.L5)
            ]

            if theories:
                explanation_exists_nodes += 1
            if worked_examples:
                worked_example_nodes += 1
            if basic_questions:
                basic_practice_nodes += 1
            if advanced_questions:
                advanced_synthesis_nodes += 1
            if theories and worked_examples and basic_questions and advanced_questions:
                fully_pedagogically_covered_nodes += 1

            if questions and not theories:
                gap_items.append(
                    CurriculumGapItem(
                        gap_id=f"gap-no-theory-{nid}",
                        taxonomy_node_id=nid,
                        chapter_id=chapter_slug,
                        gap_category=GapCategory.NO_EXPLANATION,
                        description=f"Node '{nid}' contains practice questions but lacks theoretical explanation atoms.",
                        severity="WARNING",
                        remediation_action=f"Synthesize pedagogical core concept explanation for '{node.name}'.",
                    )
                )
                gaps_by_category[GapCategory.NO_EXPLANATION.value] += 1

            if questions and not worked_examples:
                gap_items.append(
                    CurriculumGapItem(
                        gap_id=f"gap-no-example-{nid}",
                        taxonomy_node_id=nid,
                        chapter_id=chapter_slug,
                        gap_category=GapCategory.NO_WORKED_EXAMPLE,
                        description=f"Node '{nid}' lacks step-by-step worked examples.",
                        severity="INFO",
                        remediation_action=f"Construct worked example with strategy and sanity checks for '{node.name}'.",
                    )
                )
                gaps_by_category[GapCategory.NO_WORKED_EXAMPLE.value] += 1

            if questions and not basic_questions:
                gap_items.append(
                    CurriculumGapItem(
                        gap_id=f"gap-no-basic-q-{nid}",
                        taxonomy_node_id=nid,
                        chapter_id=chapter_slug,
                        gap_category=GapCategory.NO_BASIC_QUESTION,
                        description=f"Node '{nid}' lacks foundational L1/L2 questions for recognition/direct application.",
                        severity="WARNING",
                        remediation_action=f"Add direct application scaffolding questions for '{node.name}'.",
                    )
                )
                gaps_by_category[GapCategory.NO_BASIC_QUESTION.value] += 1

            if questions and not advanced_questions:
                gap_items.append(
                    CurriculumGapItem(
                        gap_id=f"gap-no-adv-q-{nid}",
                        taxonomy_node_id=nid,
                        chapter_id=chapter_slug,
                        gap_category=GapCategory.NO_ADVANCED_QUESTION,
                        description=f"Node '{nid}' lacks high-tier L4/L5 synthesis questions for JEE Advanced aspirants.",
                        severity="INFO",
                        remediation_action=f"Develop multi-concept JEE Advanced synthesis problems for '{node.name}'.",
                    )
                )
                gaps_by_category[GapCategory.NO_ADVANCED_QUESTION.value] += 1

        # Check for Olympiad extension justification
        if node.extension_olympiad and not node.syllabus_sources:
            gap_items.append(
                CurriculumGapItem(
                    gap_id=f"gap-unsupported-ext-{nid}",
                    taxonomy_node_id=nid,
                    chapter_id=chapter_slug,
                    gap_category=GapCategory.UNSUPPORTED_EXTENSION,
                    description=f"Extension node '{nid}' has no official Olympiad syllabus source citations.",
                    severity="INFO",
                    remediation_action=f"Attach Olympiad/INPhO syllabus source reference to '{node.name}'.",
                )
            )
            gaps_by_category[GapCategory.UNSUPPORTED_EXTENSION.value] += 1

        # Check for review queue blocking
        if nid in review_blocked_nodes or chapter_slug in review_blocked_chapters:
            gap_items.append(
                CurriculumGapItem(
                    gap_id=f"gap-review-blocked-{nid}",
                    taxonomy_node_id=nid,
                    chapter_id=chapter_slug,
                    gap_category=GapCategory.REVIEW_BLOCKED,
                    description=f"Chapter '{chapter_slug}' or node '{nid}' has unresolved items in review/queue/.",
                    severity="CRITICAL",
                    remediation_action=f"Resolve pending review queue items for '{chapter_slug}'.",
                )
            )
            gaps_by_category[GapCategory.REVIEW_BLOCKED.value] += 1

        # Check for missing prerequisite DAG mapping
        if prerequisite_dag and nid in prerequisite_dag.nodes:
            prereqs = prerequisite_dag.get_direct_prerequisites(nid)
            node_type = prerequisite_dag.nodes[nid].node_type
            # Non-foundation concepts should typically have at least one prerequisite
            if (
                node_type in (CurriculumNodeType.TOPIC, CurriculumNodeType.CONCEPT, CurriculumNodeType.PRINCIPLE)
                and not prereqs
                and node.order > 1
            ):
                gap_items.append(
                    CurriculumGapItem(
                        gap_id=f"gap-missing-prereq-{nid}",
                        taxonomy_node_id=nid,
                        chapter_id=chapter_slug,
                        gap_category=GapCategory.MISSING_PREREQUISITE,
                        description=f"Curriculum unit '{nid}' has no documented prerequisites in DAG.",
                        severity="INFO",
                        remediation_action=f"Map prerequisite dependencies for '{node.name}'.",
                    )
                )
                gaps_by_category[GapCategory.MISSING_PREREQUISITE.value] += 1

    pedagogical_breakdown = {
        "content_exists": content_exists_nodes,
        "explanation_exists": explanation_exists_nodes,
        "worked_example_exists": worked_example_nodes,
        "basic_practice_exists": basic_practice_nodes,
        "advanced_synthesis_exists": advanced_synthesis_nodes,
        "prerequisite_mapped": prereq_mapped_nodes,
        "fully_pedagogically_covered": fully_pedagogically_covered_nodes,
    }

    report = CurriculumGapReport(
        report_id=f"gap-report-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        total_taxonomy_nodes=len(tree.nodes),
        content_bearing_nodes_analyzed=len(tree.nodes) - len(excluded_nodes),
        excluded_nodes=excluded_nodes,
        exclusion_reason="Organizational root node (TaxonomyLevel.SUBJECT) excluded; only chapters, topics, and subtopics are content-bearing.",
        nodes_covered=nodes_covered,
        nodes_empty=nodes_empty,
        nodes_light=nodes_light,
        taxonomy_presence_nodes=nodes_covered,
        pedagogical_coverage_breakdown=pedagogical_breakdown,
        gaps_by_category=dict(gaps_by_category),
        gap_items=gap_items,
        generated_at=datetime.now(timezone.utc),
    )

    if output_report_path:
        output_report_path.parent.mkdir(parents=True, exist_ok=True)
        safe_write_json(output_report_path, report)

    return report
