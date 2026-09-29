"""
Deterministic Question Gate and Verification Binding Engine for Phase 9.

Enforces:
1. Deterministic substantive SHA-256 hashing for generated questions.
2. Schema, curriculum alignment, and taxonomy anchor validation.
3. Answer uniqueness and distractor validity audits.
4. Risk-calibrated dual verification binding for HIGH-risk assessment items.
5. Mutation invalidation and cryptographic verification unbinding.
6. Clean promotion from staging to question_bank/verified/.
7. Routing problematic, ambiguous, or conflicting questions to review/queue/questions/.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from jee_physics.models.question_bank import (
    GeneratedQuestion,
    QuestionQualityStatus,
    QuestionRiskLevel,
    QuestionSolverOpinion,
    QuestionType,
    QuestionVerificationRecord,
)
from jee_physics.models.taxonomy import SubjectType, TaxonomyTree


def compute_question_hash(question: Union[GeneratedQuestion, Dict[str, Any]]) -> str:
    """Computes a deterministic SHA-256 hash of a question's substantive physics payload.
    
    Excludes volatile fields such as verification_status, verification_record_id,
    content_hash, and created_at.
    """
    if hasattr(question, "model_dump"):
        data = question.model_dump(mode="json")
    elif isinstance(question, dict):
        data = dict(question)
    else:
        raise TypeError(f"Cannot compute question hash for {type(question)}")

    # Strip volatile fields
    for field in ["verification_status", "verification_record_id", "content_hash", "created_at", "timestamp"]:
        data.pop(field, None)

    serialized = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def validate_question_schema_and_curriculum(
    question: GeneratedQuestion,
    syllabus_tree: TaxonomyTree,
    known_curriculum_nodes: Optional[Set[str]] = None,
) -> List[str]:
    """Validates structural completeness and syllabus/curriculum grounding."""
    errors: List[str] = []

    # 1. Statement check
    if not question.statement.strip() or len(question.statement.strip()) < 10:
        errors.append(f"EMPTY_STATEMENT: Question '{question.question_id}' has insufficient problem statement")

    # 2. Taxonomy anchor check
    tax_chap = question.taxonomy_reference.chapter_id
    if tax_chap not in syllabus_tree.nodes:
        errors.append(f"TAXONOMY_NODE_NOT_FOUND: Chapter '{tax_chap}' not in syllabus tree")
    else:
        node = syllabus_tree.nodes[tax_chap]
        if node.subject != SubjectType.PHYSICS:
            errors.append(f"SUBJECT_ISOLATION_VIOLATION: Question '{question.question_id}' assigned to non-physics domain '{node.subject}'")

    # 3. Curriculum reference check
    if known_curriculum_nodes and question.curriculum_id not in known_curriculum_nodes:
        errors.append(f"UNKNOWN_CURRICULUM_ID: Node '{question.curriculum_id}' not found in approved curriculum DAG")

    # 4. MCQ Options and Distractor Rationales check
    if question.question_type in (QuestionType.SINGLE_CORRECT_MCQ, QuestionType.MULTIPLE_CORRECT_MCQ):
        if len(question.options) < 2:
            errors.append(f"INSUFFICIENT_OPTIONS: MCQ '{question.question_id}' has fewer than 2 options")

        # Check correct answer validity
        if isinstance(question.correct_answer, str):
            if question.correct_answer not in question.options:
                errors.append(f"ANSWER_NOT_IN_OPTIONS: Correct answer '{question.correct_answer}' missing from options keys")
        elif isinstance(question.correct_answer, list):
            for ans in question.correct_answer:
                if ans not in question.options:
                    errors.append(f"ANSWER_NOT_IN_OPTIONS: Correct answer '{ans}' missing from options keys")

        # Distractor rationales check
        if question.question_type == QuestionType.SINGLE_CORRECT_MCQ:
            distractor_keys = [k for k in question.options if k != question.correct_answer]
            provided_keys = {dr.option_key for dr in question.distractor_rationales}
            for dk in distractor_keys:
                if dk not in provided_keys:
                    errors.append(f"MISSING_DISTRACTOR_RATIONALE: Distractor option '{dk}' has no cognitive rationale")

    # 5. Numerical Question units check
    if question.question_type == QuestionType.NUMERICAL:
        if not question.units and not question.statement.lower().count("dimensionless"):
            errors.append(f"MISSING_NUMERICAL_UNITS: Numerical question '{question.question_id}' lacks explicit SI units")

    # 6. Source Grounding check
    if not question.source_grounding or not question.source_grounding.relationship_type:
        errors.append(f"MISSING_SOURCE_GROUNDING: Question '{question.question_id}' lacks origin grounding relationship")

    return errors


def validate_answer_uniqueness_and_distractors(
    question: GeneratedQuestion,
    solver_opinion: QuestionSolverOpinion,
) -> List[str]:
    """Validates that solver derivation matches intended answer and proves distractors invalid."""
    errors: List[str] = []

    # Check calculated answer match
    if isinstance(question.correct_answer, list):
        intended_set = set(question.correct_answer)
        calculated_set = set(solver_opinion.calculated_answer) if isinstance(solver_opinion.calculated_answer, list) else {solver_opinion.calculated_answer}
        if intended_set != calculated_set:
            errors.append(
                f"ANSWER_MISMATCH: Generator answer {intended_set} does not match solver calculated answer {calculated_set}"
            )
    else:
        # String comparison (with numerical tolerance if both are float strings)
        intended_str = str(question.correct_answer).strip()
        calculated_str = str(solver_opinion.calculated_answer).strip()
        matched = False
        try:
            val_int = float(intended_str)
            val_calc = float(calculated_str)
            tol = question.tolerance or 0.02
            matched = abs(val_int - val_calc) <= max(tol * abs(val_int), 1e-4)
        except ValueError:
            matched = (intended_str == calculated_str)

        if not matched:
            errors.append(
                f"ANSWER_MISMATCH: Generator answer '{intended_str}' does not match solver calculated answer '{calculated_str}'"
            )

    # Check solver verdict
    if solver_opinion.verdict == "AMBIGUOUS":
        errors.append(f"AMBIGUOUS_PROBLEM: Solver flagged question '{question.question_id}' as physically ambiguous or underspecified")
    elif solver_opinion.verdict in ("CONFLICT", "REJECTED"):
        errors.append(f"SOLVER_VERDICT_{solver_opinion.verdict}: Solver returned '{solver_opinion.verdict}' for '{question.question_id}'")

    # Check uniqueness
    if not solver_opinion.uniqueness_confirmed:
        errors.append(f"NON_UNIQUE_ANSWER: Solver reported non-unique solution for '{question.question_id}'")

    # Check distractor conflicts
    if solver_opinion.conflicting_distractors:
        errors.append(
            f"DISTRACTOR_CONFLICT: Distractor(s) {solver_opinion.conflicting_distractors} are also physically/mathematically valid"
        )

    # Check dimensional balance
    if not solver_opinion.dimensional_check_passed:
        errors.append(f"DIMENSIONAL_CHECK_FAILED: Solver reported dimensional inconsistency in '{question.question_id}'")

    # Check numerical calculations
    if not solver_opinion.numerical_check_passed:
        errors.append(f"NUMERICAL_CHECK_FAILED: Solver reported arithmetic calculation error in '{question.question_id}'")

    return errors


def bind_question_verification(
    question: GeneratedQuestion,
    verif_record: QuestionVerificationRecord,
) -> bool:
    """Binds an independent QuestionVerificationRecord to a question.
    
    For HIGH-risk questions, strictly requires dual independent verification
    with agreement between Solver A and Solver B.
    """
    current_hash = compute_question_hash(question)
    if verif_record.content_hash != current_hash:
        return False

    if verif_record.final_verdict != QuestionQualityStatus.VERIFIED:
        return False

    # High-risk dual verification enforcement
    if question.risk_level == QuestionRiskLevel.HIGH:
        if verif_record.solver_b is None:
            return False
        if not verif_record.agreement:
            return False

    question.content_hash = current_hash
    question.verification_record_id = verif_record.verification_id
    question.verification_status = QuestionQualityStatus.VERIFIED
    return True


def invalidate_question_if_modified(
    question: GeneratedQuestion,
    previous_hash: str,
) -> bool:
    """Detects substantive mutation after verification and invalidates verification status."""
    current_hash = compute_question_hash(question)
    if current_hash != previous_hash:
        question.verification_status = QuestionQualityStatus.INVALIDATED
        question.verification_record_id = None
        return True
    return False


def route_to_review(
    question: GeneratedQuestion,
    reason: str,
    details: Dict[str, Any],
    review_queue_dir: Path,
) -> Path:
    """Routes an ambiguous, conflicting, or defective question to review/queue/questions/."""
    review_queue_dir.mkdir(parents=True, exist_ok=True)
    target = review_queue_dir / f"{question.question_id}_review.json"

    review_item = {
        "question_id": question.question_id,
        "chapter_id": question.taxonomy_reference.chapter_id,
        "question_type": question.question_type.value,
        "risk_level": question.risk_level.value,
        "review_reason": reason,
        "failed_gate": details.get("failed_gate", reason),
        "relevant_verification_opinions": details.get("solver_opinion"),
        "provenance": {
            "origin": question.origin.value,
            "curriculum_id": question.curriculum_id,
            "taxonomy": question.taxonomy_reference.model_dump(),
        },
        "current_status": "REVIEW",
        "review_details": details,
        "question_payload": question.model_dump(mode="json"),
        "routed_at": datetime.now(timezone.utc).isoformat(),
    }
    target.write_text(json.dumps(review_item, indent=2, default=str), encoding="utf-8")
    question.verification_status = QuestionQualityStatus.REVIEW
    return target


def stage_question_artifact(question: GeneratedQuestion, staging_dir: Path) -> Path:
    """Stages a generated question JSON into staging directory."""
    staging_dir.mkdir(parents=True, exist_ok=True)
    question.content_hash = compute_question_hash(question)
    target = staging_dir / f"{question.question_id}.json"
    target.write_text(question.model_dump_json(indent=2), encoding="utf-8")
    return target


def promote_question(
    question: GeneratedQuestion,
    target_verified_dir: Path,
    audit_journal_path: Path,
) -> Path:
    """Promotes a verified question to question_bank/verified/ and records journal event."""
    if question.verification_status != QuestionQualityStatus.VERIFIED or not question.verification_record_id:
        raise ValueError(f"Cannot promote unverified question '{question.question_id}' (status={question.verification_status})")

    target_verified_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_verified_dir / f"{question.question_id}.json"
    target_path.write_text(question.model_dump_json(indent=2), encoding="utf-8")

    # Record journal entry
    journal_entry = {
        "event_type": "PROMOTION",
        "question_id": question.question_id,
        "version": question.version,
        "content_hash": question.content_hash,
        "verification_record_id": question.verification_record_id,
        "promoted_path": str(target_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(audit_journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(journal_entry) + "\n")

    return target_path
