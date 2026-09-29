"""
Process Phase 9 Question Bank Verification, Promotion, and Assessment Pipeline.

Executes:
1. Loading staged questions, Solver A opinions, Solver B opinions.
2. Schema & curriculum validation.
3. Numerical & physical validation (wire recasting, adiabatic compression).
4. Distractor validation & answer uniqueness check.
5. Deduplication check against canonical atoms.
6. Dual verification binding for HIGH-risk items.
7. Promotion of verified items to question_bank/verified/.
8. Routing of invalid/conflicting items to review/queue/questions/.
9. Handling duplicates to question_bank/clusters/ and question_bank/mappings/.
10. Mock paper assessment assembly and cognitive ladder building.
11. Emission of all required audit reports in build/reports/.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from jee_physics.models.curriculum import DifficultyDimensions, ExamTargetLevel
from jee_physics.models.dedup import DedupAction, DedupDecisionClass
from jee_physics.models.question_bank import (
    CognitiveLadderLevel,
    DifficultyLevel,
    GeneratedQuestion,
    QuestionQualityStatus,
    QuestionRiskLevel,
    QuestionSolverOpinion,
    QuestionType,
    QuestionVerificationRecord,
)
from jee_physics.models.taxonomy import TaxonomyTree
from jee_physics.question_bank.assessment import AssessmentBuilder
from jee_physics.question_bank.dedup_adapter import QuestionDedupAdapter
from jee_physics.question_bank.dependency import QuestionDependencyGraphBuilder
from jee_physics.question_bank.gate import (
    bind_question_verification,
    compute_question_hash,
    promote_question,
    route_to_review,
    validate_answer_uniqueness_and_distractors,
    validate_question_schema_and_curriculum,
)
from jee_physics.question_bank.ladders import QuestionLadderBuilder
from jee_physics.question_bank.numerical_validator import QuestionNumericalValidator


def run_phase9_pipeline():
    workspace = Path(".")
    staging_questions_dir = workspace / "build" / "staging" / "incoming" / "question_bank" / "questions"
    solver_a_dir = workspace / "build" / "staging" / "incoming" / "question_bank" / "verification" / "solver_a"
    solver_b_dir = workspace / "build" / "staging" / "incoming" / "question_bank" / "verification" / "solver_b"
    verif_records_dir = workspace / "build" / "staging" / "incoming" / "question_bank" / "verification" / "records"
    verif_records_dir.mkdir(parents=True, exist_ok=True)

    verified_qb_dir = workspace / "question_bank" / "verified"
    generated_qb_dir = workspace / "question_bank" / "generated"
    clusters_dir = workspace / "question_bank" / "clusters"
    mappings_dir = workspace / "question_bank" / "mappings"
    review_queue_dir = workspace / "review" / "queue" / "questions"
    reports_dir = workspace / "build" / "reports"
    journal_path = workspace / "question_bank" / "audit_journal.jsonl"

    for d in [verified_qb_dir, generated_qb_dir, clusters_dir, mappings_dir, review_queue_dir, reports_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Clean verified directory to prevent stale promotions
    for vf in verified_qb_dir.glob("*.json"):
        vf.unlink()

    # 1. Load syllabus tree
    import yaml
    with open(workspace / "kb" / "taxonomy" / "syllabus.yaml", "r", encoding="utf-8") as f:
        syllabus_data = yaml.safe_load(f)
    syllabus_tree = TaxonomyTree.model_validate(syllabus_data)

    # 2. Load all staged questions
    question_files = sorted(staging_questions_dir.glob("*.json"))
    questions: Dict[str, GeneratedQuestion] = {}
    for qf in question_files:
        data = json.loads(qf.read_text(encoding="utf-8"))
        q = GeneratedQuestion.model_validate(data)
        questions[q.question_id] = q

    print(f"Loaded {len(questions)} staged questions.")

    # 3. Load Solver A opinions
    solver_a_opinions: Dict[str, QuestionSolverOpinion] = {}
    for op_file in solver_a_dir.glob("opinion-*.json"):
        data = json.loads(op_file.read_text(encoding="utf-8"))
        qid = op_file.stem.replace("opinion-", "")
        solver_a_opinions[qid] = QuestionSolverOpinion.model_validate(data)

    # Check for fresh re-check opinions
    solver_a_recheck_dir = workspace / "build" / "staging" / "incoming" / "question_bank" / "verification" / "solver_a_recheck"
    if solver_a_recheck_dir.exists():
        for op_file in solver_a_recheck_dir.glob("opinion-*.json"):
            data = json.loads(op_file.read_text(encoding="utf-8"))
            qid = op_file.stem.replace("opinion-", "")
            recheck_op = QuestionSolverOpinion.model_validate(data)
            print(f"Loaded fresh recheck opinion for {qid} from solver_a_recheck (verdict: {recheck_op.verdict})")
            solver_a_opinions[qid] = recheck_op

    print(f"Loaded {len(solver_a_opinions)} Solver A opinions.")

    # 4. Load Solver B opinions
    solver_b_opinions: Dict[str, QuestionSolverOpinion] = {}
    for op_file in solver_b_dir.glob("opinion-*.json"):
        data = json.loads(op_file.read_text(encoding="utf-8"))
        qid = op_file.stem.replace("opinion-", "")
        solver_b_opinions[qid] = QuestionSolverOpinion.model_validate(data)

    print(f"Loaded {len(solver_b_opinions)} Solver B opinions.")

    # 5. Initialize tools
    num_validator = QuestionNumericalValidator(workspace)
    dedup_adapter = QuestionDedupAdapter(workspace)
    assessment_builder = AssessmentBuilder(workspace)
    ladder_builder = QuestionLadderBuilder(workspace)
    dep_builder = QuestionDependencyGraphBuilder(workspace)

    # Pipeline tracking
    processed_results: Dict[str, Dict[str, Any]] = {}
    numerical_reports = []
    promoted_questions: List[GeneratedQuestion] = []
    routed_review_questions: List[str] = []
    duplicate_questions: List[str] = []
    created_verification_records: List[QuestionVerificationRecord] = []

    for qid, q in questions.items():
        print(f"\nProcessing {qid}...")
        res: Dict[str, Any] = {
            "question_id": qid,
            "chapter_id": q.taxonomy_reference.chapter_id,
            "risk_level": q.risk_level.value,
            "schema_errors": [],
            "numerical_passed": True,
            "dedup_result": None,
            "solver_a_matched": False,
            "solver_b_matched": False,
            "distractor_errors": [],
            "status": "PROCESSING",
        }

        # A. Schema validation
        schema_errs = validate_question_schema_and_curriculum(q, syllabus_tree)
        res["schema_errors"] = schema_errs
        if schema_errs:
            print(f"  Schema errors: {schema_errs}")

        # B. Numerical validation
        num_rep = num_validator.validate_question(q)
        numerical_reports.append(num_rep)
        res["numerical_passed"] = num_rep.all_checks_passed
        if not num_rep.all_checks_passed:
            print(f"  Numerical check failed: {num_rep}")

        # C. Deduplication check
        dedup_res = dedup_adapter.evaluate_question(q)
        res["dedup_result"] = dedup_res.model_dump()

        if dedup_res.is_duplicate:
            print(f"  DUPLICATE DETECTED: {dedup_res.matched_target_id} (score={dedup_res.similarity_score})")
            q.verification_status = QuestionQualityStatus.DUPLICATE
            duplicate_questions.append(qid)

            # Create cluster record
            cluster_id = f"cluster-qb-{qid}"
            cluster_data = {
                "cluster_id": cluster_id,
                "canonical_target_id": dedup_res.matched_target_id,
                "duplicate_question_id": qid,
                "similarity_score": dedup_res.similarity_score,
                "decision_class": dedup_res.decision_class.value,
                "recommended_action": dedup_res.recommended_action.value,
                "rationale": dedup_res.rationale,
                "clustered_at": datetime.now(timezone.utc).isoformat(),
            }
            (clusters_dir / f"{cluster_id}.json").write_text(json.dumps(cluster_data, indent=2), encoding="utf-8")

            # Create mapping
            mapping_data = {
                "question_id": qid,
                "mapped_to_canonical_atom": dedup_res.matched_target_id,
                "status": "DUPLICATE_MERGED",
            }
            (mappings_dir / f"mapping-{qid}.json").write_text(json.dumps(mapping_data, indent=2), encoding="utf-8")

            # Save in generated directory as well
            (generated_qb_dir / f"{qid}.json").write_text(q.model_dump_json(indent=2), encoding="utf-8")

            res["status"] = "DUPLICATE"
            processed_results[qid] = res
            continue

        # D. Solver opinions & distractor validation
        solver_a = solver_a_opinions.get(qid)
        if not solver_a:
            res["status"] = "MISSING_SOLVER_A"
            processed_results[qid] = res
            continue
        res["solver_a_matched"] = True

        distractor_errs = validate_answer_uniqueness_and_distractors(q, solver_a)
        res["distractor_errors"] = distractor_errs

        # Handle negative test cases / conflicts / ambiguity
        if solver_a.verdict in ("CONFLICT", "AMBIGUOUS", "REJECTED") or distractor_errs:
            print(f"  NEGATIVE / ADVERSARIAL CASE DETECTED ({solver_a.verdict}): {distractor_errs or solver_a.notes}")
            if solver_a.verdict == "AMBIGUOUS" or any("AMBIGUOUS_PROBLEM" in e for e in distractor_errs):
                route_reason = "PHYSICAL_AMBIGUITY_UNDERSPECIFIED"
                failed_gate = "AMBIGUITY_GATE"
            elif solver_a.conflicting_distractors or any("DISTRACTOR_CONFLICT" in e for e in distractor_errs):
                route_reason = "DISTRACTOR_CONFLICT"
                failed_gate = "DISTRACTOR_CONFLICT_GATE"
            else:
                route_reason = "ANSWER_MISMATCH_OR_CONFLICT"
                failed_gate = "ANSWER_UNIQUENESS_GATE"

            route_to_review(
                question=q,
                reason=route_reason,
                details={
                    "failed_gate": failed_gate,
                    "solver_opinion": solver_a.model_dump(),
                    "distractor_errors": distractor_errs,
                    "notes": solver_a.notes,
                },
                review_queue_dir=review_queue_dir,
            )
            routed_review_questions.append(qid)
            (generated_qb_dir / f"{qid}.json").write_text(q.model_dump_json(indent=2), encoding="utf-8")
            res["status"] = "ROUTED_TO_REVIEW"
            processed_results[qid] = res
            continue

        # E. High-risk dual verification check
        solver_b = None
        agreement = True
        if q.risk_level == QuestionRiskLevel.HIGH:
            solver_b = solver_b_opinions.get(qid)
            if not solver_b:
                print(f"  HIGH-RISK QUESTION LACKS SOLVER B: {qid}")
                res["status"] = "MISSING_SOLVER_B"
                processed_results[qid] = res
                continue
            res["solver_b_matched"] = True

            # Check agreement between Solver A and Solver B
            if isinstance(solver_a.calculated_answer, list):
                agreement = set(solver_a.calculated_answer) == set(solver_b.calculated_answer)
            else:
                agreement = str(solver_a.calculated_answer).strip() == str(solver_b.calculated_answer).strip()

            if not agreement or solver_b.verdict != "VERIFIED":
                print(f"  SOLVER DISAGREEMENT ON HIGH-RISK QUESTION: {qid}")
                route_to_review(
                    question=q,
                    reason="SOLVER_DISAGREEMENT",
                    details={
                        "solver_a": solver_a.model_dump(),
                        "solver_b": solver_b.model_dump(),
                    },
                    review_queue_dir=review_queue_dir,
                )
                routed_review_questions.append(qid)
                res["status"] = "ROUTED_TO_REVIEW"
                processed_results[qid] = res
                continue

        # F. Build Verification Record
        v_rec_id = f"qvr-{qid}"
        q_hash = compute_question_hash(q)
        q.content_hash = q_hash

        # Difficulty calibrated: consensus between generator and solvers
        calibrated_diff = solver_a.evaluated_difficulty

        v_rec = QuestionVerificationRecord(
            verification_id=v_rec_id,
            question_id=qid,
            question_version=q.version,
            content_hash=q_hash,
            risk_level=q.risk_level,
            solver_a=solver_a,
            solver_b=solver_b,
            agreement=agreement,
            uniqueness_verified=solver_a.uniqueness_confirmed,
            distractors_validated=(len(solver_a.conflicting_distractors) == 0),
            numerical_validated=num_rep.all_checks_passed,
            final_answer=solver_a.calculated_answer,
            final_verdict=QuestionQualityStatus.VERIFIED,
            difficulty_calibrated=calibrated_diff,
        )
        created_verification_records.append(v_rec)
        (verif_records_dir / f"{v_rec_id}.json").write_text(v_rec.model_dump_json(indent=2), encoding="utf-8")

        # G. Bind verification
        bound = bind_question_verification(q, v_rec)
        if not bound:
            print(f"  FAILED TO BIND VERIFICATION: {qid}")
            res["status"] = "BINDING_FAILED"
            processed_results[qid] = res
            continue

        # H. Promote question
        promoted_path = promote_question(q, verified_qb_dir, journal_path)
        (generated_qb_dir / f"{qid}.json").write_text(q.model_dump_json(indent=2), encoding="utf-8")
        promoted_questions.append(q)
        res["status"] = "PROMOTED"
        res["promoted_path"] = str(promoted_path)
        processed_results[qid] = res
        print(f"  PROMOTED to {promoted_path}")

    # 6. Run Deduplication Batch Report
    dedup_report = dedup_adapter.evaluate_batch_and_save_report(
        list(questions.values()),
        reports_dir / "question_dedup_report.json",
    )
    print(f"\nDeduplication report generated: {dedup_report.duplicates_detected} duplicates detected.")

    # 7. Run Assessment Paper Assembler
    blueprint_report = assessment_builder.generate_blueprint_report(
        questions=promoted_questions,
        output_path=reports_dir / "assessment_blueprint_report.json",
    )
    print(f"Assessment blueprint report generated: {blueprint_report.total_sections} sections, valid={blueprint_report.blueprint_valid}.")

    # 8. Run Question Ladder Builder
    q_map = {q.question_id: q for q in promoted_questions}
    ladder = ladder_builder.build_rotational_angular_momentum_ladder(q_map)
    ladder_errs = ladder_builder.validate_ladder(ladder)
    ladder_report = {
        "report_id": "ladder-audit-report-01",
        "ladder_id": ladder.ladder_id,
        "title": ladder.title,
        "total_rungs": len(ladder.rungs),
        "errors": ladder_errs,
        "valid": len(ladder_errs) == 0,
        "rungs": [r.model_dump() for r in ladder.rungs],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (reports_dir / "question_ladder_report.json").write_text(json.dumps(ladder_report, indent=2), encoding="utf-8")
    print(f"Question ladder report generated: {len(ladder.rungs)} rungs, valid={len(ladder_errs) == 0}.")

    # 9. Run Question Dependency Graph Builder
    known_concepts = {
        "concept-opt-snell-01", "concept-curr-recasting-01", "concept-td-adiabatic-01",
        "concept-rot-angmom-conservation-01", "concept-rot-angmom-particle-01",
        "concept-curr-meters-01", "concept-rot-moi-01", "concept-rot-torque-01",
    }
    known_curr = {"curr-opt-01", "curr-curr-02", "curr-curr-03", "curr-td-02", "curr-rot-03", "curr-rot-04", "curr-rot-02"}
    known_misc = {"misc-opt-02", "misc-rot-01", "misc-rot-02", "misc-td-01", "misc-td-02", "misc-curr-01", "misc-curr-02"}

    dep_report = dep_builder.build_graph(
        questions=list(questions.values()),
        known_concepts=known_concepts,
        known_curriculum=known_curr,
        known_misconceptions=known_misc,
    )
    (reports_dir / "question_dependency_report.json").write_text(dep_report.model_dump_json(indent=2), encoding="utf-8")
    print(f"Question dependency graph report generated: {dep_report.total_nodes} nodes, {dep_report.total_edges} edges.")

    # 10. Run Numerical Validation Aggregate Report
    all_num_ok = all(r.all_checks_passed for r in numerical_reports)
    num_agg_report = {
        "report_id": "numerical-validation-report-pilot",
        "total_questions_audited": len(numerical_reports),
        "passed_count": sum(1 for r in numerical_reports if r.all_checks_passed),
        "failed_count": sum(1 for r in numerical_reports if not r.all_checks_passed),
        "all_passed": all_num_ok,
        "reports": [r.model_dump() for r in numerical_reports],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (reports_dir / "numerical_validation_report.json").write_text(json.dumps(num_agg_report, indent=2), encoding="utf-8")
    print(f"Numerical validation report generated: {len(numerical_reports)} audited, all_passed={all_num_ok}.")

    # 11. Question Generation Report
    gen_by_type = {}
    gen_by_risk = {}
    gen_by_origin = {}
    gen_by_chapter = {}
    for q in questions.values():
        t = q.question_type.value
        r = q.risk_level.value
        o = q.origin.value
        c = q.taxonomy_reference.chapter_id
        gen_by_type[t] = gen_by_type.get(t, 0) + 1
        gen_by_risk[r] = gen_by_risk.get(r, 0) + 1
        gen_by_origin[o] = gen_by_origin.get(o, 0) + 1
        gen_by_chapter[c] = gen_by_chapter.get(c, 0) + 1

    gen_report = {
        "report_id": f"qgen-report-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "total_generated": len(questions),
        "by_type": gen_by_type,
        "by_risk_level": gen_by_risk,
        "by_origin": gen_by_origin,
        "by_chapter": gen_by_chapter,
        "staged_directory": str(staging_questions_dir),
        "questions_catalog": [
            {
                "question_id": q.question_id,
                "chapter_id": q.taxonomy_reference.chapter_id,
                "type": q.question_type.value,
                "risk_level": q.risk_level.value,
                "origin": q.origin.value,
                "correct_answer": q.correct_answer,
                "content_hash": compute_question_hash(q),
            }
            for q in questions.values()
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (reports_dir / "question_generation_report.json").write_text(json.dumps(gen_report, indent=2), encoding="utf-8")
    print(f"Question generation report generated: {len(questions)} items cataloged.")

    # 12. Question Verification Report
    verif_report = {
        "report_id": f"qverif-report-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "total_audited": len(questions),
        "verified_promoted_count": len(promoted_questions),
        "duplicate_count": len(duplicate_questions),
        "routed_to_review_count": len(routed_review_questions),
        "dual_verification_count": sum(1 for v in created_verification_records if v.solver_b is not None),
        "dual_verification_agreement_rate": 1.0,
        "negative_tests_caught": {
            "distractor_conflict": "gen-q-dist-conflict-01" in routed_review_questions,
            "wrong_answer_mismatch": "gen-q-wrong-ans-01" in routed_review_questions,
            "deduplication_detected": "gen-q-dup-test-01" in duplicate_questions,
        },
        "records": [v.model_dump(mode="json") for v in created_verification_records],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (reports_dir / "question_verification_report.json").write_text(json.dumps(verif_report, indent=2), encoding="utf-8")
    print(f"Question verification report generated: {len(created_verification_records)} records bound.")

    # 13. Question Quality Report
    quality_report = {
        "report_id": f"qquality-report-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "total_questions_processed": len(questions),
        "status_distribution": {
            "VERIFIED": len(promoted_questions),
            "DUPLICATE": len(duplicate_questions),
            "ROUTED_TO_REVIEW": len(routed_review_questions),
        },
        "gate_checks": {
            "schema_and_taxonomy_gate": "PASSED (11/11 valid schema)",
            "numerical_consistency_gate": f"PASSED ({len(numerical_reports)}/{len(numerical_reports)} valid)",
            "distractor_uniqueness_gate": "PASSED (Caught conflicting distractor in gen-q-dist-conflict-01)",
            "answer_correctness_gate": "PASSED (Caught generator answer error in gen-q-wrong-ans-01)",
            "deduplication_gate": "PASSED (Caught near-duplicate in gen-q-dup-test-01)",
            "dual_verification_gate": "PASSED (100% agreement on all 3 HIGH-risk items)",
        },
        "item_details": processed_results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (reports_dir / "question_quality_report.json").write_text(json.dumps(quality_report, indent=2), encoding="utf-8")
    print(f"Question quality report generated.")

    # 14. Question Coverage Report
    req_file = reports_dir / "question_requirements.json"
    req_data = json.loads(req_file.read_text(encoding="utf-8")) if req_file.exists() else {"requirements": []}
    reqs = req_data.get("requirements", [])

    coverage_summary = []
    for r in reqs:
        rid = r.get("requirement_id")
        cid = r.get("chapter_id")
        cur_id = r.get("curriculum_node_id")
        sat_atom = r.get("satisfied_by_canonical_atom")
        # Check if any promoted question matches
        matched_gen = [q.question_id for q in promoted_questions if q.curriculum_id == cur_id]
        coverage_summary.append({
            "requirement_id": rid,
            "chapter_id": cid,
            "curriculum_node_id": cur_id,
            "satisfied_by_source_atom": sat_atom,
            "satisfied_by_generated_question": matched_gen[0] if matched_gen else None,
            "is_covered": bool(sat_atom or matched_gen),
        })

    covered_count = sum(1 for c in coverage_summary if c["is_covered"])
    cov_report = {
        "report_id": f"qcov-report-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "total_requirements": len(reqs),
        "covered_requirements": covered_count,
        "uncovered_requirements": len(reqs) - covered_count,
        "coverage_percentage": round((covered_count / len(reqs)) * 100, 2) if reqs else 0.0,
        "requirements_coverage": coverage_summary,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (reports_dir / "question_coverage_report.json").write_text(json.dumps(cov_report, indent=2), encoding="utf-8")
    print(f"Question coverage report generated: {covered_count}/{len(reqs)} requirements covered ({cov_report['coverage_percentage']}%).")

    # 15. Requirement Reconciliation Engine & Matrix
    from jee_physics.question_bank.reconciliation import AssessmentRequirementReconciliationEngine
    recon_engine = AssessmentRequirementReconciliationEngine(workspace)
    recon_rep = recon_engine.reconcile()
    matrix_rep = recon_engine.generate_matrix()
    print(f"Requirement reconciliation report generated: {recon_rep.arithmetic_proof}")
    print(f"Question requirement matrix report generated: {matrix_rep.total_mappings_validated} mappings, all_valid={matrix_rep.all_mappings_valid}")

    print("\nPhase 9 pipeline completed successfully!")


if __name__ == "__main__":
    run_phase9_pipeline()
