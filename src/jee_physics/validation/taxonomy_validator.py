from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import yaml

from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference
from jee_physics.models.taxonomy import (
    LEVEL_ORDER,
    SubjectType,
    TaxonomyLevel,
    TaxonomyNode,
    TaxonomyTree,
)


def load_syllabus_tree(tree_path: Path) -> Dict[str, Any]:
    """Loads raw syllabus taxonomy YAML file."""
    if not tree_path.exists():
        return {}
    with open(tree_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_canonical_taxonomy_tree(tree_path: Optional[Path] = None) -> TaxonomyTree:
    """Loads and returns a fully validated Pydantic TaxonomyTree from syllabus.yaml."""
    if tree_path is None:
        tree_path = Path("kb/taxonomy/syllabus.yaml")

    data = load_syllabus_tree(tree_path)
    if "nodes" in data:
        # Structured TaxonomyTree format
        return TaxonomyTree.model_validate(data)
    elif "chapters" in data:
        # Legacy/nested format adapter
        nodes: Dict[str, TaxonomyNode] = {
            "physics": TaxonomyNode(
                id="physics",
                name="Physics",
                level=TaxonomyLevel.SUBJECT,
                parent_id=None,
                subject=SubjectType.PHYSICS,
            )
        }
        for ch_id, ch_data in data["chapters"].items():
            nodes[ch_id] = TaxonomyNode(
                id=ch_id,
                name=ch_data.get("title", ch_id),
                level=TaxonomyLevel.CHAPTER,
                parent_id="physics",
                aliases=ch_data.get("aliases", []),
            )
            for top_id, top_data in ch_data.get("topics", {}).items():
                nodes[top_id] = TaxonomyNode(
                    id=top_id,
                    name=top_data.get("title", top_id),
                    level=TaxonomyLevel.TOPIC,
                    parent_id=ch_id,
                )
                for sub_id in top_data.get("subtopics", []):
                    nodes[sub_id] = TaxonomyNode(
                        id=sub_id,
                        name=sub_id.replace("-", " ").title(),
                        level=TaxonomyLevel.SUBTOPIC,
                        parent_id=top_id,
                    )
        return TaxonomyTree(root_id="physics", nodes=nodes)
    else:
        raise ValueError(f"Unrecognized taxonomy data format in '{tree_path}'.")


def validate_taxonomy_tree_structure(tree_data: Dict[str, Any]) -> List[str]:
    """Deterministic structural validation for a taxonomy tree dictionary.
    
    Verifies:
    - Root presence and uniqueness
    - No orphan nodes (missing parent references)
    - Valid hierarchy level transitions
    - No cycles in parent links
    - Unique node IDs and no alias collisions
    - Valid prerequisite references
    """
    errors: List[str] = []

    try:
        if "nodes" in tree_data:
            # Let Pydantic perform full model validation
            TaxonomyTree.model_validate(tree_data)
        else:
            # Check nested chapters format
            chapters = tree_data.get("chapters", {})
            if not chapters:
                errors.append("Taxonomy contains no chapters.")
            seen_topics: Set[str] = set()
            for ch_id, ch_info in chapters.items():
                topics = ch_info.get("topics", {})
                for top_id in topics:
                    if top_id in seen_topics:
                        errors.append(f"Duplicate topic ID '{top_id}' across chapters.")
                    seen_topics.add(top_id)
    except Exception as e:
        errors.append(f"Taxonomy tree validation failed: {str(e)}")

    return errors


def validate_taxonomy_reference(
    atom_or_ref: Any,
    syllabus_tree_path: Optional[Path] = None,
    tree: Optional[TaxonomyTree] = None,
) -> List[str]:
    """Validates an atom's taxonomy reference against the canonical syllabus tree.
    
    Accepts either a KnowledgeAtom or a TaxonomyReference object.
    Supports alias resolution (e.g. 'rotation' -> 'rotational-motion').
    """
    errors: List[str] = []

    if isinstance(atom_or_ref, KnowledgeAtom):
        tax = atom_or_ref.taxonomy
    elif isinstance(atom_or_ref, TaxonomyReference):
        tax = atom_or_ref
    elif isinstance(atom_or_ref, dict):
        tax = TaxonomyReference.model_validate(atom_or_ref)
    else:
        errors.append(f"Unsupported object type for taxonomy reference validation: {type(atom_or_ref)}")
        return errors

    if not tax.chapter_id or not tax.chapter_id.strip():
        errors.append("Taxonomy chapter_id cannot be blank.")
    if not tax.topic_id or not tax.topic_id.strip():
        errors.append("Taxonomy topic_id cannot be blank.")

    # If no path and no tree, but default canonical syllabus exists, use it
    if tree is None and syllabus_tree_path is None:
        default_path = Path("kb/taxonomy/syllabus.yaml")
        if default_path.exists():
            syllabus_tree_path = default_path

    # If tree not loaded, load it
    if tree is None and syllabus_tree_path and Path(syllabus_tree_path).exists():
        try:
            tree = load_canonical_taxonomy_tree(Path(syllabus_tree_path))
        except Exception:
            # Fallback to raw dict parsing for legacy mock tests
            raw_tree = load_syllabus_tree(Path(syllabus_tree_path))
            chapters = raw_tree.get("chapters", {})
            if tax.chapter_id not in chapters:
                errors.append(f"Chapter '{tax.chapter_id}' is not defined in the canonical syllabus tree.")
                return errors
            topics = chapters[tax.chapter_id].get("topics", {})
            if tax.topic_id not in topics:
                errors.append(
                    f"Topic '{tax.topic_id}' is not defined under chapter '{tax.chapter_id}' in the syllabus tree."
                )
                return errors
            if tax.subtopic_id:
                subtopics = topics[tax.topic_id].get("subtopics", [])
                if tax.subtopic_id not in subtopics:
                    errors.append(
                        f"Subtopic '{tax.subtopic_id}' is not defined under topic '{tax.topic_id}' in the syllabus tree."
                    )
            return errors

    if tree:
        # 1. Resolve chapter
        canonical_chapter_id = tree.resolve_node_id(tax.chapter_id)
        if not canonical_chapter_id:
            errors.append(f"Chapter '{tax.chapter_id}' is not defined in the canonical syllabus tree.")
            return errors

        ch_node = tree.nodes.get(canonical_chapter_id)
        if not ch_node or ch_node.level != TaxonomyLevel.CHAPTER:
            errors.append(f"Node '{tax.chapter_id}' is not a CHAPTER in the syllabus tree.")
            return errors

        # 2. Resolve topic
        canonical_topic_id = tree.resolve_node_id(tax.topic_id)
        if not canonical_topic_id:
            errors.append(
                f"Topic '{tax.topic_id}' is not defined in the syllabus tree."
            )
            return errors

        top_node = tree.nodes.get(canonical_topic_id)
        if not top_node or top_node.level != TaxonomyLevel.TOPIC:
            errors.append(f"Node '{tax.topic_id}' is not a TOPIC in the syllabus tree.")
            return errors

        # Check topic parentage
        if top_node.parent_id != canonical_chapter_id:
            errors.append(
                f"Topic '{tax.topic_id}' is not defined under chapter '{tax.chapter_id}' in the syllabus tree."
            )
            return errors

        # 3. Resolve subtopic if present
        if tax.subtopic_id:
            canonical_sub_id = tree.resolve_node_id(tax.subtopic_id)
            if not canonical_sub_id:
                errors.append(
                    f"Subtopic '{tax.subtopic_id}' is not defined in the syllabus tree."
                )
                return errors

            sub_node = tree.nodes.get(canonical_sub_id)
            if not sub_node or sub_node.level not in (TaxonomyLevel.SUBTOPIC, TaxonomyLevel.EXTENSION):
                errors.append(f"Node '{tax.subtopic_id}' is not a SUBTOPIC/EXTENSION in the syllabus tree.")
                return errors

            if sub_node.parent_id != canonical_topic_id and sub_node.parent_id != canonical_chapter_id:
                errors.append(
                    f"Subtopic '{tax.subtopic_id}' is not defined under topic '{tax.topic_id}' in the syllabus tree."
                )

    return errors


def validate_subject_isolation(
    subject: SubjectType,
    target_kb: SubjectType = SubjectType.PHYSICS,
) -> bool:
    """Enforces strict subject isolation.
    
    Returns True if the subject is permitted into target_kb, False otherwise.
    Chemistry, Mathematics, and Non-content cannot enter the Physics canonical KB.
    """
    if target_kb == SubjectType.PHYSICS:
        return subject == SubjectType.PHYSICS
    return subject == target_kb
