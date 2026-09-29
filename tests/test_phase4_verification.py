import math
from pathlib import Path
import pytest

from jee_physics.models.atom import (
    ExamMetadata,
    FigureReference,
    KnowledgeAtom,
    QuestionOption,
    QuestionPayload,
    TaxonomyReference,
)
from jee_physics.models.enums import AtomStatus, AtomType, DifficultyLevel, VerificationVerdict
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.models.verification import (
    AdjudicationRecord,
    SolverRun,
    VerificationRecord,
)
from jee_physics.verification.comparator import compare_solver_runs
from jee_physics.verification.normalizer import (
    clean_latex_math_string,
    compare_answers,
    evaluate_simple_math_expression,
    normalize_option_label,
    parse_numerical_value,
)
from jee_physics.verification.policy import is_high_risk_question
from jee_physics.verification.promoter import (
    promote_atom_to_canonical,
    validate_promotion_eligibility,
)
from jee_physics.verification.runner import execute_verification_protocol
from jee_physics.verification.sanitizer import (
    audit_blind_package_for_leaks,
    create_blind_solver_package,
)


def make_test_question_atom(
    atom_id: str = "rotational-motion-question-1234abcd",
    source_claimed_answer: str | None = "C",
    source_solution: str | None = None,
    difficulty: DifficultyLevel = DifficultyLevel.L2,
) -> KnowledgeAtom:
    statement = "A disc rotates about vertical axis. Insect moves along diameter. Angular speed?"
    options = [
        QuestionOption(id="A", text="continuously decreases"),
        QuestionOption(id="B", text="continuously increases"),
        QuestionOption(id="C", text="first increases and then decreases"),
        QuestionOption(id="D", text="remains unchanged"),
    ]
    prov = ProvenanceRecord(
        source_id="src-mock-test-01-abcdef12",
        file_name="mock_test_01.pdf",
        page_start=4,
        page_end=4,
        source_locator="Q12",
    )
    return KnowledgeAtom(
        atom_id=atom_id,
        schema_version="1.0.0",
        atom_version=1,
        active=True,
        atom_type=AtomType.QUESTION,
        title="Disc and insect angular speed",
        taxonomy=TaxonomyReference(chapter_id="rotational-motion", topic_id="angular-momentum"),
        provenance=[prov],
        confidence=0.99,
        verification_status=AtomStatus.STAGED,
        content_hash="a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90",
        question=QuestionPayload(
            statement=statement,
            options=options,
            source_claimed_answer=source_claimed_answer,
            source_solution=source_solution,
            difficulty=difficulty,
            concepts=["conservation-of-angular-momentum"],
        ),
    )


def test_question_payload_preserves_source_claim_and_solution():
    atom = make_test_question_atom(
        source_claimed_answer="B",
        source_solution="Differentiate L = I * omega with respect to time.",
    )
    assert atom.question.source_claimed_answer == "B"
    assert atom.question.verified_answer is None
    assert atom.question.source_solution == "Differentiate L = I * omega with respect to time."
    assert atom.verification_status == AtomStatus.STAGED


def test_blind_package_sanitizer_excludes_all_answers_and_solutions():
    atom = make_test_question_atom(
        source_claimed_answer="C",
        source_solution="Torque is zero, therefore L is constant.",
    )
    pkg = create_blind_solver_package(atom)

    # Verify presence of problem content
    assert pkg.atom_id == atom.atom_id
    assert pkg.statement == atom.question.statement
    assert len(pkg.options) == 4
    assert pkg.difficulty == DifficultyLevel.L2

    # Verify strict exclusion of answer keys and solutions
    pkg_dict = pkg.model_dump()
    assert "source_claimed_answer" not in pkg_dict
    assert "verified_answer" not in pkg_dict
    assert "source_solution" not in pkg_dict
    assert "answer" not in pkg_dict
    assert "verification_status" not in pkg_dict

    leak_audit = audit_blind_package_for_leaks(pkg)
    assert not leak_audit["has_leak"]
    assert len(leak_audit["leaks"]) == 0


def test_two_independent_solver_records_coexist_and_verify(tmp_path: Path):
    atom = make_test_question_atom()

    run_a = SolverRun(
        solver_run_id="run-solver_a-001",
        atom_id=atom.atom_id,
        solver_id="solver_a",
        independent_answer="C",
        reasoning_steps=["Conservation of angular momentum: I decreases then increases, so omega increases then decreases."],
        assumptions_used=["No external torque"],
    )
    run_b = SolverRun(
        solver_run_id="run-solver_b-002",
        atom_id=atom.atom_id,
        solver_id="solver_b",
        independent_answer="Option (C)",
        reasoning_steps=["I(r) = I_disc + m*r^2. As r: R -> 0 -> R, I decreases then increases. Therefore omega increases then decreases."],
        assumptions_used=["Axis passes through center"],
    )

    verif_record, adj = execute_verification_protocol(
        atom=atom,
        solver_runs=[run_a, run_b],
        verification_base_dir=tmp_path,
    )

    assert verif_record.verdict == VerificationVerdict.VERIFIED
    assert verif_record.consensus_answer == "C"
    assert "run-solver_a-001" in verif_record.solver_run_ids
    assert "run-solver_b-002" in verif_record.solver_run_ids
    assert verif_record.independent_answers["solver_a"] == "C"
    assert verif_record.independent_answers["solver_b"] == "Option (C)"
    assert adj is None


def test_solver_disagreement_triggers_adjudication():
    res = compare_solver_runs(
        source_claimed_answer="C",
        solver_a_answer="B",
        solver_b_answer="C",
    )
    assert not res.solvers_agree
    assert res.requires_adjudication
    assert res.discrepancy_classification == "SOLVER_DISAGREEMENT"


def test_source_error_represented_without_overwriting_provenance(tmp_path: Path):
    """Synthetic test fixture proving SOURCE_ERROR is recorded without corrupting provenance."""
    # Synthetic problem where source incorrectly printed 'A' instead of correct answer 'D'
    atom = make_test_question_atom(
        source_claimed_answer="A",
        source_solution="Erroneous source textbook assumption ignoring buoyant force.",
    )

    run_a = SolverRun(
        solver_run_id="run-a-src-err",
        atom_id=atom.atom_id,
        solver_id="solver_a",
        independent_answer="D",
        reasoning_steps=["Rigorous Archimedes principle proof shows density relation rho1 < rho3 < rho2."],
    )
    run_b = SolverRun(
        solver_run_id="run-b-src-err",
        atom_id=atom.atom_id,
        solver_id="solver_b",
        independent_answer="D",
        reasoning_steps=["Floatation equilibrium gives net upward buoyancy equal to weight."],
    )

    def mock_adjudicator(at, runs, src_ans):
        return AdjudicationRecord(
            adjudication_id="adj-001",
            atom_id=at.atom_id,
            solver_analyses={"solver_a": "Valid derivation", "solver_b": "Valid derivation"},
            source_claim_analysis=f"Source key '{src_ans}' is an erroneous misprint; physical proof confirms 'D'.",
            physical_reasoning="Ball straddles interface, requiring intermediate density.",
            adjudicated_answer="D",
            verdict=VerificationVerdict.SOURCE_ERROR,
            confidence=0.99,
        )

    verif_record, adj = execute_verification_protocol(
        atom=atom,
        solver_runs=[run_a, run_b],
        adjudicator_fn=mock_adjudicator,
        verification_base_dir=tmp_path,
    )

    assert verif_record.verdict == VerificationVerdict.SOURCE_ERROR
    assert verif_record.source_claimed_answer == "A"
    assert verif_record.consensus_answer == "D"
    assert adj is not None

    # Promote to canonical kb/
    kb_dir = tmp_path / "kb" / "atoms"
    manifests_dir = tmp_path / "verification" / "manifests"
    event = promote_atom_to_canonical(
        atom=atom,
        verification_record=verif_record,
        kb_atoms_dir=kb_dir,
        manifests_dir=manifests_dir,
    )

    assert event.verdict == VerificationVerdict.SOURCE_ERROR
    assert event.source_claimed_answer == "A"
    assert event.verified_answer == "D"

    # Verify promoted file on disk
    canonical_file = kb_dir / f"{atom.atom_id}.json"
    assert canonical_file.exists()
    from jee_physics.storage.io import read_json
    canonical_dict = read_json(canonical_file)
    assert canonical_dict["question"]["source_claimed_answer"] == "A"
    assert canonical_dict["question"]["verified_answer"] == "D"
    assert canonical_dict["verification_status"] == "VERIFIED"
    # Ensure source provenance is intact
    assert canonical_dict["provenance"][0]["source_id"] == "src-mock-test-01-abcdef12"


def test_ambiguous_question_cannot_be_promoted(tmp_path: Path):
    atom = make_test_question_atom()

    verif_record = VerificationRecord(
        verification_id="verif-ambig-001",
        atom_id=atom.atom_id,
        source_id="src-mock-test-01-abcdef12",
        atom_version=1,
        content_hash=atom.content_hash,
        solver_run_ids=["run-1", "run-2"],
        verdict=VerificationVerdict.AMBIGUOUS,
        confidence=0.50,
        consensus_answer=None,
    )

    is_eligible, errors = validate_promotion_eligibility(atom, verif_record)
    assert not is_eligible
    assert any("not eligible for canonical promotion" in err for err in errors)

    with pytest.raises(ValueError, match="failed promotion eligibility"):
        promote_atom_to_canonical(atom, verif_record, tmp_path / "kb")


def test_unverified_staged_atom_cannot_be_promoted(tmp_path: Path):
    atom = make_test_question_atom()
    is_eligible, errors = validate_promotion_eligibility(atom, None)
    assert not is_eligible
    assert any("No VerificationRecord provided" in err for err in errors)


def test_mismatched_atom_version_rejected(tmp_path: Path):
    atom = make_test_question_atom()
    verif_record = VerificationRecord(
        verification_id="verif-ver-001",
        atom_id=atom.atom_id,
        source_id="src-mock-test-01-abcdef12",
        atom_version=2,  # Atom is version 1
        content_hash=atom.content_hash,
        solver_run_ids=["run-1", "run-2"],
        consensus_answer="C",
        verdict=VerificationVerdict.VERIFIED,
        confidence=0.99,
    )
    is_eligible, errors = validate_promotion_eligibility(atom, verif_record)
    assert not is_eligible
    assert any("atom_version mismatch" in err for err in errors)


def test_mismatched_content_hash_rejected(tmp_path: Path):
    atom = make_test_question_atom()
    verif_record = VerificationRecord(
        verification_id="verif-hash-001",
        atom_id=atom.atom_id,
        source_id="src-mock-test-01-abcdef12",
        atom_version=1,
        content_hash="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        solver_run_ids=["run-1", "run-2"],
        consensus_answer="C",
        verdict=VerificationVerdict.VERIFIED,
        confidence=0.99,
    )
    is_eligible, errors = validate_promotion_eligibility(atom, verif_record)
    assert not is_eligible
    assert any("content_hash mismatch" in err for err in errors)


def test_normalizer_symbolic_and_numerical_equivalence():
    # Option labels
    assert normalize_option_label("A") == "A"
    assert normalize_option_label("(A)") == "A"
    assert normalize_option_label("Option A") == "A"
    assert normalize_option_label("Option (3)") == "3"
    assert compare_answers("Option (A)", "A")
    assert compare_answers("Option 2", "(2)")

    # Pure numerical values with tolerance
    assert compare_answers("100", "100.0")
    assert compare_answers("3.75 A", "3.75")
    assert compare_answers("1.5 \\times 10^{-2} N", "0.015")
    assert compare_answers("0.025", "0.0250001")

    # Mathematical expressions with square roots
    # 2/sqrt(3) vs 2*sqrt(3)/3
    assert compare_answers("2/\\sqrt{3}", "2\\sqrt{3}/3")
    assert compare_answers("$\\frac{2}{\\sqrt{3}}$", "$2/\\sqrt{3}$")
    assert compare_answers("4 T_0", "4T_0")


def test_model_error_represented_in_record(tmp_path: Path):
    atom = make_test_question_atom()

    run_a = SolverRun(
        solver_run_id="run-err-a",
        atom_id=atom.atom_id,
        solver_id="solver_a",
        independent_answer="A",  # Erroneous
        reasoning_steps=["Erroneous assumption: insect walking inward decreases angular velocity."],
    )
    run_b = SolverRun(
        solver_run_id="run-correct-b",
        atom_id=atom.atom_id,
        solver_id="solver_b",
        independent_answer="C",  # Correct
        reasoning_steps=["I decreases as r -> 0, so omega increases. Then I increases, so omega decreases."],
    )

    def adjudicator_model_error(at, runs, src_ans):
        return AdjudicationRecord(
            adjudication_id="adj-model-err",
            atom_id=at.atom_id,
            solver_analyses={
                "solver_a": "MODEL_ERROR: solver inverted the inverse relationship between moment of inertia and angular speed.",
                "solver_b": "Valid first-principles angular momentum conservation.",
            },
            source_claim_analysis="Source matches physical reality.",
            physical_reasoning="L = I * omega is constant. Since I first decreases then increases, omega first increases then decreases.",
            adjudicated_answer="C",
            verdict=VerificationVerdict.MODEL_ERROR,
            confidence=0.99,
        )

    verif_record, adj = execute_verification_protocol(
        atom=atom,
        solver_runs=[run_a, run_b],
        adjudicator_fn=adjudicator_model_error,
        verification_base_dir=tmp_path,
    )

    assert verif_record.verdict == VerificationVerdict.MODEL_ERROR
    assert "MODEL_ERROR" in adj.solver_analyses["solver_a"]
    assert verif_record.consensus_answer == "C"

    # Per policy, MODEL_ERROR requires resolution before promotion; cannot be promoted directly
    is_eligible, errors = validate_promotion_eligibility(atom, verif_record)
    assert not is_eligible
    assert any("not eligible for canonical promotion" in err for err in errors)


def test_staged_atom_self_promotion_without_verification_record_rejected(tmp_path: Path):
    """An LLM or malicious user setting verification_status=VERIFIED in staging must be rejected."""
    atom = make_test_question_atom()
    atom.verification_status = AtomStatus.VERIFIED
    atom.question.verified_answer = "C"

    # Attempting to promote without a valid VerificationRecord must fail
    is_eligible, errors = validate_promotion_eligibility(atom, None)
    assert not is_eligible
    assert any("No VerificationRecord provided" in err for err in errors)

    with pytest.raises(ValueError):
        promote_atom_to_canonical(atom, None, tmp_path / "kb" / "atoms")


def test_failed_promotion_leaves_kb_clean(tmp_path: Path):
    atom = make_test_question_atom()
    kb_dir = tmp_path / "kb" / "atoms"
    kb_dir.mkdir(parents=True, exist_ok=True)

    # Invalid record with mismatched content hash
    bad_record = VerificationRecord(
        verification_id="verif-bad-hash",
        atom_id=atom.atom_id,
        source_id="src-mock-test-01-abcdef12",
        atom_version=1,
        content_hash="bad_hash" * 4,
        solver_run_ids=["run-1", "run-2"],
        consensus_answer="C",
        verdict=VerificationVerdict.VERIFIED,
        confidence=0.99,
    )

    with pytest.raises(ValueError):
        promote_atom_to_canonical(atom, bad_record, kb_dir)

    # Ensure no file was written to kb_dir
    files_in_kb = list(kb_dir.glob("*.json"))
    assert len(files_in_kb) == 0


def test_forged_solver_runs_cannot_authorize_promotion(tmp_path: Path):
    """Prove that a forged VerificationRecord referencing non-existent or mismatched solver runs is rejected."""
    atom = make_test_question_atom()
    runs_dir = tmp_path / "verification" / "solver_runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    # 1. Non-existent solver_run_ids
    forged_record = VerificationRecord(
        verification_id="verif-forged-runs",
        atom_id=atom.atom_id,
        source_id="src-mock-test-01-abcdef12",
        atom_version=1,
        content_hash=atom.content_hash,
        solver_run_ids=["run-phantom-001", "run-phantom-002"],
        consensus_answer="C",
        verdict=VerificationVerdict.VERIFIED,
        confidence=0.99,
    )

    is_eligible, errors = validate_promotion_eligibility(
        atom, forged_record, solver_runs_dir=runs_dir
    )
    assert not is_eligible
    assert any("Forged or missing solver run record" in err for err in errors)

    with pytest.raises(ValueError, match="failed promotion eligibility"):
        promote_atom_to_canonical(
            atom=atom,
            verification_record=forged_record,
            kb_atoms_dir=tmp_path / "kb" / "atoms",
            solver_runs_dir=runs_dir,
        )

    # 2. Solver run exists but belongs to a different atom (mismatched atom_id)
    from jee_physics.storage.io import safe_write_json
    different_atom_run = SolverRun(
        solver_run_id="run-other-atom",
        atom_id="different-atom-9999",
        solver_id="solver_a",
        independent_answer="C",
        reasoning_steps=["Legitimate run for another atom."],
    )
    safe_write_json(runs_dir / "run-other-atom.json", different_atom_run.model_dump(mode="json"))

    mismatched_record = VerificationRecord(
        verification_id="verif-mismatched-run",
        atom_id=atom.atom_id,
        source_id="src-mock-test-01-abcdef12",
        atom_version=1,
        content_hash=atom.content_hash,
        solver_run_ids=["run-other-atom"],
        consensus_answer="C",
        verdict=VerificationVerdict.VERIFIED,
        confidence=0.99,
    )

    is_eligible, errors = validate_promotion_eligibility(
        atom, mismatched_record, solver_runs_dir=runs_dir
    )
    assert not is_eligible
    assert any("target atom mismatch" in err for err in errors)


def test_custom_agent_configuration():
    """Verify that .agents/agents/physics-verifier.md is configured with valid Antigravity subagent metadata."""
    agent_file = Path(".agents/agents/physics-verifier.md")
    assert agent_file.exists()
    content = agent_file.read_text(encoding="utf-8")
    assert "name: physics-verifier" in content
    assert "subagent: true" in content
    assert "model: pro" in content
    assert "tools:" in content
    assert "write_to_file" in content
    assert "verification/incoming/" in content


def test_stage_solver_run_success_and_invariants(tmp_path: Path):
    """Test deterministic staging of an untrusted solver JSON file."""
    from jee_physics.verification.staging import stage_solver_run_file
    from jee_physics.storage.io import safe_write_jsonl

    atom = make_test_question_atom()
    staging_atoms_dir = tmp_path / "build" / "staging" / "atoms"
    staging_atoms_dir.mkdir(parents=True, exist_ok=True)
    batch_file = staging_atoms_dir / "test_batch.jsonl"
    safe_write_jsonl(batch_file, [atom.model_dump(mode="json")])

    runs_dir = tmp_path / "verification" / "solver_runs"
    manifests_dir = tmp_path / "verification" / "manifests"
    incoming_dir = tmp_path / "verification" / "incoming"
    incoming_dir.mkdir(parents=True, exist_ok=True)

    solver_file = incoming_dir / "solver_test_001.json"
    solver_data = {
        "solver_run_id": "run-test-custody-001",
        "solver_agent_name": "solver_a",
        "atom_id": atom.atom_id,
        "atom_version": 1,
        "content_hash": atom.content_hash,
        "independent_answer": "C",
        "raw_answer": "Option C",
        "reasoning_steps": ["Step 1: Test step."],
        "assumptions_used": ["None"],
    }
    from jee_physics.storage.io import safe_write_json
    safe_write_json(solver_file, solver_data)

    success, dest, manifest, errors = stage_solver_run_file(
        input_file=solver_file,
        staging_dir=staging_atoms_dir,
        solver_runs_dir=runs_dir,
        manifests_dir=manifests_dir,
    )

    assert success
    assert dest is not None and dest.exists()
    assert manifest is not None and manifest.exists()
    assert len(errors) == 0

    # Test duplicate rejection
    success_dup, _, _, errors_dup = stage_solver_run_file(
        input_file=solver_file,
        staging_dir=staging_atoms_dir,
        solver_runs_dir=runs_dir,
        manifests_dir=manifests_dir,
    )
    assert not success_dup
    assert any("Duplicate solver_run_id" in e for e in errors_dup)


def test_stage_solver_run_prohibited_fields_rejected(tmp_path: Path):
    """Test that solver JSON with prohibited fields (source answers, verdicts) is strictly rejected."""
    from jee_physics.verification.staging import stage_solver_run_file

    atom = make_test_question_atom()
    incoming_dir = tmp_path / "verification" / "incoming"
    incoming_dir.mkdir(parents=True, exist_ok=True)
    poisoned_file = incoming_dir / "poisoned_solver.json"

    poisoned_data = {
        "solver_run_id": "run-poisoned-001",
        "solver_agent_name": "solver_a",
        "atom_id": atom.atom_id,
        "source_claimed_answer": "C",  # Prohibited!
        "verdict": "VERIFIED",          # Prohibited!
        "independent_answer": "C",
    }
    from jee_physics.storage.io import safe_write_json
    safe_write_json(poisoned_file, poisoned_data)

    success, dest, manifest, errors = stage_solver_run_file(
        input_file=poisoned_file,
        staging_dir=tmp_path / "staging",
        solver_runs_dir=tmp_path / "runs",
        manifests_dir=tmp_path / "manifests",
    )
    assert not success
    assert any("Prohibited field" in e for e in errors)


def test_stage_adjudication_file(tmp_path: Path):
    """Test deterministic staging of an untrusted adjudication JSON file."""
    from jee_physics.verification.staging import stage_adjudication_file
    from jee_physics.storage.io import safe_write_jsonl, safe_write_json

    atom = make_test_question_atom()
    staging_atoms_dir = tmp_path / "build" / "staging" / "atoms"
    staging_atoms_dir.mkdir(parents=True, exist_ok=True)
    batch_file = staging_atoms_dir / "test_batch.jsonl"
    safe_write_jsonl(batch_file, [atom.model_dump(mode="json")])

    adj_file = tmp_path / "incoming" / "adj_test.json"
    adj_file.parent.mkdir(parents=True, exist_ok=True)

    adj_data = {
        "adjudication_id": "adj-unit-test-001",
        "atom_id": atom.atom_id,
        "atom_version": 1,
        "content_hash": atom.content_hash,
        "adjudicator_id": "physics-adjudicator",
        "solver_analyses": {
            "solver_a": "Correct derivation",
            "solver_b": "Incorrect assumption",
        },
        "source_claim_analysis": "Source was wrong",
        "physical_reasoning": "First principles proof",
        "adjudicated_answer": "C",
        "verdict": "SOURCE_ERROR",
        "confidence": 0.99,
    }
    safe_write_json(adj_file, adj_data)

    success, dest, manifest, errors = stage_adjudication_file(
        input_file=adj_file,
        staging_dir=staging_atoms_dir,
        adjudication_dir=tmp_path / "verification" / "adjudications",
        manifests_dir=tmp_path / "verification" / "manifests",
    )
    assert success
    assert dest is not None and dest.exists()
    assert manifest is not None and manifest.exists()


def test_blind_package_contains_no_answers_or_peer_data():
    """Verify that serialized blind packages contain zero answer keys or peer solver data."""
    blind_file = Path("verification/incoming/pilot_blind_packages.json")
    if not blind_file.exists():
        pytest.skip("pilot_blind_packages.json not generated")

    import json
    packages = json.loads(blind_file.read_text(encoding="utf-8"))
    assert len(packages) == 5

    forbidden_keys = [
        "source_claimed_answer",
        "verified_answer",
        "source_solution",
        "solution_methods",
        "answer",
        "verdict",
        "solver_runs",
        "adjudication_result",
    ]

    for pkg in packages:
        for key in forbidden_keys:
            assert key not in pkg, f"Package {pkg.get('atom_id')} leaked {key}!"
        assert "statement" in pkg
        assert "options" in pkg
        assert "concepts" in pkg

