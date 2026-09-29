"""Deterministic Content Gate and Verification Binding Engine for Phase 8.

Enforces physical correctness, dimensional balance, explicit assumptions,
immutable hash-to-verification binding, change invalidation, and impact analysis.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from jee_physics.models.content import (
    ConceptExplanation,
    ContentBlockType,
    ContentRiskLevel,
    ContentVerificationRecord,
    ContentVerificationStatus,
    DerivationRecord,
    DualVerificationRecord,
    MisconceptionContentRecord,
    WorkedExampleContentRecord,
)
from jee_physics.models.content import FormulaRecord
from jee_physics.models.taxonomy import SubjectType, TaxonomyTree
from jee_physics.storage.io import safe_write_json


def compute_content_hash(artifact: Any) -> str:
    """Computes a deterministic SHA-256 hash of a content artifact's substantive payload.
    
    Excludes volatile fields such as verification_status, verification_record_id,
    and timestamps so that hash reflects immutable physics content.
    """
    if hasattr(artifact, "model_dump"):
        data = artifact.model_dump(mode="json")
    elif isinstance(artifact, dict):
        data = dict(artifact)
    else:
        raise TypeError(f"Cannot compute content hash for {type(artifact)}")

    # Strip volatile fields
    for field in ["verification_status", "verification_record_id", "content_hash", "created_at", "timestamp"]:
        data.pop(field, None)

    serialized = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def bind_verification(
    artifact: Any,
    verification: ContentVerificationRecord,
) -> bool:
    """Binds an independent ContentVerificationRecord to a content artifact.
    
    Validates that the content_hash in the verification record strictly matches
    the artifact's substantive content hash. If valid, marks verification_status as VERIFIED.
    """
    current_hash = compute_content_hash(artifact)
    if verification.content_hash != current_hash:
        return False

    if verification.verdict != "VERIFIED":
        return False

    if isinstance(artifact, dict):
        artifact["content_hash"] = current_hash
        artifact["verification_record_id"] = verification.verification_id
        artifact["verification_status"] = ContentVerificationStatus.VERIFIED.value
    else:
        artifact.content_hash = current_hash
        artifact.verification_record_id = verification.verification_id
        artifact.verification_status = ContentVerificationStatus.VERIFIED
    return True


def bind_dual_verification(
    artifact: Any,
    dual_verification: DualVerificationRecord,
) -> bool:
    """Binds a DualVerificationRecord to a HIGH-risk content artifact.
    
    Requires both independent verifiers to agree on VERIFIED and the substantive
    content_hash to match.
    """
    current_hash = compute_content_hash(artifact)
    if dual_verification.content_hash != current_hash:
        return False

    if not dual_verification.agreement or dual_verification.final_verdict != "VERIFIED":
        return False

    if isinstance(artifact, dict):
        artifact["content_hash"] = current_hash
        artifact["verification_record_id"] = dual_verification.verification_id
        artifact["verification_status"] = ContentVerificationStatus.VERIFIED.value
    else:
        artifact.content_hash = current_hash
        artifact.verification_record_id = dual_verification.verification_id
        artifact.verification_status = ContentVerificationStatus.VERIFIED
    return True


def invalidate_if_modified(
    artifact: Any,
    previous_hash: str,
) -> bool:
    """Detects content mutation after verification and invalidates verification status.
    
    Returns True if invalidated, False if untouched.
    """
    current_hash = compute_content_hash(artifact)
    if current_hash != previous_hash:
        artifact.verification_status = ContentVerificationStatus.INVALIDATED
        artifact.verification_record_id = None
        return True
    return False


def validate_concept_explanation(
    concept: ConceptExplanation,
    syllabus_tree: TaxonomyTree,
) -> List[str]:
    """Validates physical and curriculum integrity of a ConceptExplanation."""
    errors: List[str] = []

    if not concept.title.strip():
        errors.append(f"CONCEPT_EMPTY_TITLE: Concept '{concept.content_id}' has empty title")
    if not concept.formal_definition.strip():
        errors.append(f"CONCEPT_EMPTY_DEFINITION: Concept '{concept.content_id}' lacks formal definition")
    if not concept.intuition.strip():
        errors.append(f"CONCEPT_EMPTY_INTUITION: Concept '{concept.content_id}' lacks intuition/analog")
    if len(concept.explanation.strip()) < 10:
        errors.append(f"CONCEPT_SHORT_EXPLANATION: Concept '{concept.content_id}' explanation too brief")

    # Validate taxonomy anchor
    chap_id = concept.taxonomy_reference.chapter_id
    if chap_id not in syllabus_tree.nodes:
        errors.append(f"TAXONOMY_NODE_NOT_FOUND: Concept '{concept.content_id}' references unknown chapter '{chap_id}'")
    else:
        chap_node = syllabus_tree.nodes[chap_id]
        if chap_node.subject != SubjectType.PHYSICS:
            errors.append(f"SUBJECT_ISOLATION_VIOLATION: Concept '{concept.content_id}' belongs to non-physics domain '{chap_node.subject}'")

    return errors


def validate_formula_record(
    formula: FormulaRecord,
    syllabus_tree: TaxonomyTree,
) -> List[str]:
    """Validates physical correctness, dimensions, units, and assumptions of a FormulaRecord."""
    errors: List[str] = []

    if not formula.title.strip():
        errors.append(f"FORMULA_EMPTY_TITLE: Formula '{formula.formula_id}' has empty title")
    eq = getattr(formula, "equation", None) or getattr(formula, "equation_latex", None) or ""
    if not eq.strip():
        errors.append(f"FORMULA_EMPTY_EQUATION: Formula '{formula.formula_id}' lacks equation")
    if not formula.variables:
        errors.append(f"FORMULA_MISSING_VARIABLES: Formula '{formula.formula_id}' lacks variable definitions")
    if not getattr(formula, "units", None) and not getattr(formula, "units_and_dimensions", None):
        errors.append(f"FORMULA_MISSING_UNITS: Formula '{formula.formula_id}' lacks SI units")
    if not formula.assumptions:
        errors.append(f"FORMULA_MISSING_ASSUMPTIONS: Formula '{formula.formula_id}' lacks explicit physical assumptions")
    conds = getattr(formula, "validity_conditions", None) or getattr(formula, "conditions_of_validity", None) or []
    if not conds:
        errors.append(f"FORMULA_MISSING_VALIDITY: Formula '{formula.formula_id}' lacks validity conditions")

    # Validate chapter taxonomy anchor if present
    chap_id = getattr(formula, "chapter_id", None)
    if chap_id:
        if chap_id not in syllabus_tree.nodes:
            errors.append(f"TAXONOMY_NODE_NOT_FOUND: Formula '{formula.formula_id}' references unknown chapter '{chap_id}'")
        else:
            chap_node = syllabus_tree.nodes[chap_id]
            if chap_node.subject != SubjectType.PHYSICS:
                errors.append(f"SUBJECT_ISOLATION_VIOLATION: Formula '{formula.formula_id}' belongs to non-physics domain '{chap_node.subject}'")

    return errors


def validate_derivation_record(
    derivation: DerivationRecord,
) -> List[str]:
    """Validates mathematical and physical continuity of a DerivationRecord."""
    errors: List[str] = []

    if not derivation.target_equation.strip():
        errors.append(f"DERIVATION_EMPTY_TARGET: Derivation '{derivation.derivation_id}' lacks target equation")
    if not derivation.starting_principles:
        errors.append(f"DERIVATION_MISSING_PRINCIPLES: Derivation '{derivation.derivation_id}' lacks starting principles")
    if not derivation.assumptions:
        errors.append(f"DERIVATION_MISSING_ASSUMPTIONS: Derivation '{derivation.derivation_id}' lacks explicit assumptions")
    if not derivation.ordered_steps:
        errors.append(f"DERIVATION_NO_STEPS: Derivation '{derivation.derivation_id}' has 0 ordered steps")

    # Validate step numbering continuity
    for idx, step in enumerate(derivation.ordered_steps):
        expected_step = idx + 1
        if step.step_number != expected_step:
            errors.append(
                f"DERIVATION_STEP_DISCONTINUITY: Step at index {idx} has step_number {step.step_number}, expected {expected_step}"
            )
        if not step.result_equation.strip():
            errors.append(f"DERIVATION_EMPTY_EQUATION: Step {step.step_number} in '{derivation.derivation_id}' has empty equation")

    # Final step must match target equation conceptually
    if derivation.ordered_steps:
        final_step = derivation.ordered_steps[-1]
        if not final_step.result_equation.strip():
            errors.append(f"DERIVATION_MISSING_FINAL_RESULT: Last step lacks final derived equation")

    return errors


def validate_worked_example_content(
    example: WorkedExampleContentRecord,
) -> List[str]:
    """Validates completeness, units, and sanity checks of a WorkedExampleContentRecord."""
    errors: List[str] = []

    if not example.problem_statement.strip():
        errors.append(f"EXAMPLE_EMPTY_STATEMENT: Example '{example.example_id}' has empty problem statement")
    if not example.final_answer.strip():
        errors.append(f"EXAMPLE_EMPTY_ANSWER: Example '{example.example_id}' lacks final answer")
    if not example.units.strip():
        errors.append(f"EXAMPLE_MISSING_UNITS: Example '{example.example_id}' lacks SI units")
    if not example.governing_principles:
        errors.append(f"EXAMPLE_MISSING_PRINCIPLES: Example '{example.example_id}' lacks governing principles")
    if not example.solution_strategy.strip():
        errors.append(f"EXAMPLE_MISSING_STRATEGY: Example '{example.example_id}' lacks solution strategy")
    if not example.ordered_steps:
        errors.append(f"EXAMPLE_NO_STEPS: Example '{example.example_id}' has 0 solution steps")
    if not example.sanity_checks:
        errors.append(f"EXAMPLE_MISSING_SANITY_CHECKS: Example '{example.example_id}' lacks sanity checks (limits/dimensions)")

    return errors


def validate_misconception_content(
    misc: MisconceptionContentRecord,
) -> List[str]:
    """Validates evidence grounding and corrective explanation of a MisconceptionContentRecord."""
    errors: List[str] = []

    if not misc.incorrect_statement.strip():
        errors.append(f"MISCONCEPTION_EMPTY_STATEMENT: Misconception '{misc.misconception_id}' has empty statement")
    if not misc.why_it_fails.strip():
        errors.append(f"MISCONCEPTION_MISSING_WHY: Misconception '{misc.misconception_id}' lacks explanation of failure")
    if not misc.corrective_explanation.strip():
        errors.append(f"MISCONCEPTION_MISSING_CORRECTION: Misconception '{misc.misconception_id}' lacks corrective explanation")

    return errors


def analyze_change_impact(
    changed_formula_id: str,
    derivations: List[DerivationRecord],
    examples: List[WorkedExampleContentRecord],
    concepts: List[ConceptExplanation],
) -> Dict[str, List[str]]:
    """Determines which downstream content artifacts must be reverified if a formula changes.
    
    Returns a mapping of dependent_type -> list of dependent IDs.
    """
    impacted: Dict[str, List[str]] = {
        "derivations": [],
        "worked_examples": [],
        "concepts": [],
    }

    # 1. Check derivations deriving this formula
    for d in derivations:
        if d.target_formula_id == changed_formula_id:
            impacted["derivations"].append(d.derivation_id)

    # 2. Check worked examples using concepts or equations associated with this formula
    for ex in examples:
        for p in ex.governing_principles:
            if changed_formula_id in p or any(changed_formula_id in s.principle_applied for s in ex.ordered_steps):
                impacted["worked_examples"].append(ex.example_id)

    # 3. Check concepts referencing this formula
    for c in concepts:
        if changed_formula_id in c.related_formula_ids:
            impacted["concepts"].append(c.content_id)

    return impacted


def stage_content_artifact(
    artifact: Any,
    target_dir: Path,
) -> Path:
    """Safely stages or promotes a content artifact to the target directory."""
    target_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(artifact, dict):
        fid = (
            artifact.get("misconception_id")
            or artifact.get("example_id")
            or artifact.get("derivation_id")
            or artifact.get("formula_id")
            or artifact.get("content_id")
            or artifact.get("concept_id")
            or artifact.get("block_id")
            or artifact.get("verification_id")
        )
        if not fid:
            raise ValueError("Dictionary artifact lacks identifiable ID key")
        filename = f"{fid}.json"
    elif isinstance(artifact, FormulaRecord):
        filename = f"{artifact.formula_id}.json"
    elif isinstance(artifact, ConceptExplanation):
        filename = f"{artifact.content_id}.json"
    elif isinstance(artifact, DerivationRecord):
        filename = f"{artifact.derivation_id}.json"
    elif isinstance(artifact, WorkedExampleContentRecord):
        filename = f"{artifact.example_id}.json"
    elif isinstance(artifact, MisconceptionContentRecord):
        filename = f"{artifact.misconception_id}.json"
    elif hasattr(artifact, "content_id"):
        filename = f"{artifact.content_id}.json"
    elif hasattr(artifact, "block_id"):
        filename = f"{artifact.block_id}.json"
    elif hasattr(artifact, "verification_id"):
        filename = f"{artifact.verification_id}.json"
    else:
        raise ValueError(f"Unsupported content artifact type: {type(artifact)}")

    out_path = target_dir / filename
    safe_write_json(out_path, artifact)
    return out_path
