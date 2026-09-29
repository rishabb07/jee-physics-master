import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from jee_physics.models.enums import AtomStatus
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.taxonomy import TaxonomyLevel, TaxonomyTree, SubjectType
from jee_physics.models.curriculum import (
    ChapterPlan,
    ChapterSpec,
    CurriculumAuditRecord,
    QuestionLadder,
)
from jee_physics.storage.io import safe_write_json


VALID_MISCONCEPTION_CATEGORIES: Set[str] = {
    "SIGN_MISTAKE",
    "VECTOR_SCALAR_CONFUSION",
    "INVALID_FORMULA_CONDITION",
    "WRONG_CONSERVATION_LAW",
    "FRAME_CONFUSION",
    "HIDDEN_CONSTRAINT_OMISSION",
    "DIMENSIONAL_INCONSISTENCY",
    "BOUNDARY_VALUE_CONFUSION",
    "EQUILIBRIUM_CONDITION_MISAPPLICATION",
}


def validate_chapter_spec(
    spec: ChapterSpec,
    syllabus_tree: TaxonomyTree,
    kb_atoms_dir: Path,
) -> List[str]:
    """Validates a ChapterSpec against authoritative syllabus taxonomy and verified canonical KB.
    
    Returns a list of error strings. An empty list signifies complete validity.
    """
    errors: List[str] = []

    # 1. Validate taxonomy references against syllabus tree
    for idx, tax_ref in enumerate(spec.taxonomy_references):
        chap_id = tax_ref.chapter_id
        if chap_id not in syllabus_tree.nodes:
            errors.append(f"TAXONOMY_NODE_NOT_FOUND: Reference {idx} chapter_id '{chap_id}' does not exist in syllabus tree")
            continue

        chap_node = syllabus_tree.nodes[chap_id]
        if chap_node.level != TaxonomyLevel.CHAPTER:
            errors.append(f"INVALID_TAXONOMY_LEVEL: Node '{chap_id}' is of level '{chap_node.level}', expected CHAPTER")

        topic_id = tax_ref.topic_id
        if topic_id not in syllabus_tree.nodes:
            errors.append(f"TAXONOMY_NODE_NOT_FOUND: Reference {idx} topic_id '{topic_id}' does not exist in syllabus tree")
            continue

        topic_node = syllabus_tree.nodes[topic_id]
        if topic_node.level != TaxonomyLevel.TOPIC:
            errors.append(f"INVALID_TAXONOMY_LEVEL: Node '{topic_id}' is of level '{topic_node.level}', expected TOPIC")
        if topic_node.parent_id != chap_id:
            errors.append(
                f"TAXONOMY_PARENTAGE_MISMATCH: Topic '{topic_id}' has parent '{topic_node.parent_id}', expected '{chap_id}'"
            )

        if tax_ref.subtopic_id:
            sub_id = tax_ref.subtopic_id
            if sub_id not in syllabus_tree.nodes:
                errors.append(f"TAXONOMY_NODE_NOT_FOUND: Reference {idx} subtopic_id '{sub_id}' does not exist in syllabus tree")
                continue
            sub_node = syllabus_tree.nodes[sub_id]
            if sub_node.level not in (TaxonomyLevel.SUBTOPIC, TaxonomyLevel.EXTENSION):
                errors.append(f"INVALID_TAXONOMY_LEVEL: Subtopic '{sub_id}' is level '{sub_node.level}', expected SUBTOPIC/EXTENSION")
            if sub_node.parent_id != topic_id:
                errors.append(
                    f"TAXONOMY_PARENTAGE_MISMATCH: Subtopic '{sub_id}' has parent '{sub_node.parent_id}', expected '{topic_id}'"
                )

    # 2. Validate Question Placements
    placed_atom_ids: Set[str] = set()
    for qp in spec.question_sequence:
        atom_id = qp.atom_id
        placed_atom_ids.add(atom_id)
        atom_file = kb_atoms_dir / f"{atom_id}.json"

        if not atom_file.exists():
            errors.append(f"QUESTION_ATOM_NOT_FOUND: Question atom '{atom_id}' not found in canonical kb/atoms/")
            continue

        try:
            with open(atom_file, "r", encoding="utf-8") as f:
                atom_data = json.load(f)
            atom = KnowledgeAtom.model_validate(atom_data)
        except Exception as e:
            errors.append(f"CANONICAL_ATOM_CORRUPT: Failed to load '{atom_id}': {e}")
            continue

        # Invariant: Question must be strictly VERIFIED
        if atom.verification_status != AtomStatus.VERIFIED:
            errors.append(
                f"UNVERIFIED_QUESTION_REJECTED: Atom '{atom_id}' has verification status '{atom.verification_status}', expected VERIFIED"
            )

        # Invariant: Must belong to Physics domain
        if atom.taxonomy.chapter_id in syllabus_tree.nodes:
            atom_chap = syllabus_tree.nodes[atom.taxonomy.chapter_id]
            if atom_chap.subject != SubjectType.PHYSICS:
                errors.append(
                    f"SUBJECT_ISOLATION_VIOLATION: Atom '{atom_id}' belongs to non-physics domain '{atom_chap.subject}'"
                )

    # 3. Validate Question Ladders
    for ladder in spec.question_ladders:
        if ladder.chapter_id != spec.chapter_id:
            errors.append(
                f"LADDER_CHAPTER_MISMATCH: Ladder '{ladder.ladder_id}' specifies chapter '{ladder.chapter_id}', expected '{spec.chapter_id}'"
            )
        for rung in ladder.rungs:
            rung_atom_id = rung.atom_id
            rung_atom_file = kb_atoms_dir / f"{rung_atom_id}.json"
            if not rung_atom_file.exists():
                errors.append(
                    f"LADDER_ATOM_NOT_FOUND: Ladder '{ladder.ladder_id}' rung {rung.level} atom '{rung_atom_id}' not found in kb/atoms/"
                )
            else:
                try:
                    with open(rung_atom_file, "r", encoding="utf-8") as f:
                        rung_data = json.load(f)
                    rung_atom = KnowledgeAtom.model_validate(rung_data)
                    if rung_atom.verification_status != AtomStatus.VERIFIED:
                        errors.append(
                            f"LADDER_UNVERIFIED_ATOM: Ladder '{ladder.ladder_id}' rung {rung.level} atom '{rung_atom_id}' is not VERIFIED"
                        )
                except Exception as e:
                    errors.append(f"LADDER_ATOM_CORRUPT: Failed to load rung atom '{rung_atom_id}': {e}")

    # 4. Validate Formula Records
    for formula in spec.formula_sequence:
        if not formula.equation_latex.strip():
            errors.append(f"FORMULA_MISSING_EQUATION: Formula '{formula.formula_id}' has empty equation_latex")
        if not formula.variables:
            errors.append(f"FORMULA_MISSING_VARIABLES: Formula '{formula.formula_id}' has no variables mapped")
        if not formula.assumptions:
            errors.append(f"FORMULA_MISSING_ASSUMPTIONS: Formula '{formula.formula_id}' lacks explicit assumptions")
        if not formula.conditions_of_validity:
            errors.append(f"FORMULA_MISSING_CONDITIONS: Formula '{formula.formula_id}' lacks conditions of validity")

    # 5. Validate Misconception Records
    for misc in spec.misconception_sequence:
        if misc.category not in VALID_MISCONCEPTION_CATEGORIES:
            errors.append(
                f"INVALID_MISCONCEPTION_CATEGORY: Misconception '{misc.misconception_id}' has invalid category '{misc.category}'"
            )

    # 6. Validate Worked Examples
    for ex in spec.worked_example_sequence:
        if not ex.solution_strategy.strip():
            errors.append(f"WORKED_EXAMPLE_MISSING_STRATEGY: Example '{ex.example_id}' lacks solution strategy")
        if not ex.step_by_step_derivation:
            errors.append(f"WORKED_EXAMPLE_MISSING_STEPS: Example '{ex.example_id}' lacks step-by-step derivation")
        if not ex.final_answer.strip():
            errors.append(f"WORKED_EXAMPLE_MISSING_ANSWER: Example '{ex.example_id}' lacks final answer")

    return errors


def validate_chapter_plan(plan: ChapterPlan, spec: ChapterSpec) -> List[str]:
    """Validates a ChapterPlan against its parent ChapterSpec.
    
    Returns a list of error strings.
    """
    errors: List[str] = []

    if plan.chapter_id != spec.chapter_id:
        errors.append(
            f"PLAN_CHAPTER_MISMATCH: ChapterPlan chapter_id '{plan.chapter_id}' does not match spec '{spec.chapter_id}'"
        )

    # Check section ordering
    seen_orders: Set[int] = set()
    for s in plan.sections:
        if s.section_order in seen_orders:
            errors.append(f"DUPLICATE_SECTION_ORDER: Duplicate section_order {s.section_order} in plan '{plan.plan_id}'")
        seen_orders.add(s.section_order)

    # Verify that question atom IDs in plan belong to spec question sequence or ladders
    spec_atom_ids: Set[str] = {qp.atom_id for qp in spec.question_sequence}
    for ladder in spec.question_ladders:
        for rung in ladder.rungs:
            spec_atom_ids.add(rung.atom_id)

    for s in plan.sections:
        for atom_id in s.question_atom_ids:
            if atom_id not in spec_atom_ids:
                errors.append(
                    f"PLAN_UNSPECIFIED_QUESTION: Section '{s.section_id}' places question '{atom_id}' not approved in ChapterSpec"
                )

    # Verify formula IDs in plan belong to spec formula sequence
    spec_formula_ids: Set[str] = {f.formula_id for f in spec.formula_sequence}
    for s in plan.sections:
        for fid in s.formula_ids:
            if fid not in spec_formula_ids:
                errors.append(
                    f"PLAN_UNSPECIFIED_FORMULA: Section '{s.section_id}' references formula '{fid}' not present in ChapterSpec"
                )

    return errors


def stage_curriculum_artifact(
    incoming_path: Path,
    target_dir: Path,
    expected_type: str = "chapter_spec",
) -> Path:
    """Safely validates and promotes a staged curriculum artifact from incoming staging to canonical curriculum directory.
    
    expected_type: 'chapter_spec' | 'chapter_plan' | 'question_ladder'
    """
    if not incoming_path.exists():
        raise FileNotFoundError(f"Incoming artifact '{incoming_path}' does not exist")

    with open(incoming_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    target_dir.mkdir(parents=True, exist_ok=True)

    if expected_type == "chapter_spec":
        spec = ChapterSpec.model_validate(data)
        out_path = target_dir / f"{spec.chapter_id}_spec.json"
        safe_write_json(out_path, spec)
        return out_path
    elif expected_type == "chapter_plan":
        plan = ChapterPlan.model_validate(data)
        out_path = target_dir / f"{plan.chapter_id}_plan.json"
        safe_write_json(out_path, plan)
        return out_path
    elif expected_type == "question_ladder":
        ladder = QuestionLadder.model_validate(data)
        out_path = target_dir / f"{ladder.ladder_id}.json"
        safe_write_json(out_path, ladder)
        return out_path
    else:
        raise ValueError(f"Unknown curriculum artifact type: '{expected_type}'")


def record_curriculum_audit_entry(journal_path: Path, entry: CurriculumAuditRecord) -> None:
    """Appends an immutable audit entry to the curriculum journal idempotently."""
    journal_path.parent.mkdir(parents=True, exist_ok=True)

    existing_entry_ids: Set[str] = set()
    if journal_path.exists():
        with open(journal_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if "entry_id" in obj:
                        existing_entry_ids.add(obj["entry_id"])
                except Exception:
                    continue

    if entry.entry_id in existing_entry_ids:
        return  # Already recorded idempotently

    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry.model_dump(mode="json"), ensure_ascii=False) + "\n")
