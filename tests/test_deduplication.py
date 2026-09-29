from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
import pytest

from jee_physics.dedup.candidate_generator import (
    BaseSemanticRetriever,
    extract_comparison_features,
    generate_candidate_pairs,
    jaccard_similarity,
    tokenize_physics_words,
)
from jee_physics.dedup.gate import (
    apply_deduplication,
    select_canonical_representative,
    stage_dedup_decisions_file,
    validate_canonical_kb_storage_integrity,
)
from jee_physics.dedup.normalizer import (
    clean_option_text,
    clean_statement_text,
    compute_normalized_fingerprint,
    extract_numerical_values,
    extract_target_quantity,
    normalize_latex,
    normalize_unicode_and_symbols,
)
from jee_physics.models.atom import (
    KnowledgeAtom,
    ProvenanceRecord,
    QuestionOption,
    QuestionPayload,
    SolutionMethod,
    TaxonomyReference,
)
from jee_physics.models.enums import AtomStatus, AtomType, DifficultyLevel
from jee_physics.models.dedup import (
    CanonicalMapping,
    DedupAction,
    DedupCandidate,
    DedupCluster,
    DedupDecision,
    DedupDecisionClass,
    NormalizedAtomFingerprint,
    PreservedProvenance,
    PreservedSolutionMethod,
)


@pytest.fixture
def sample_atom_1() -> KnowledgeAtom:
    return KnowledgeAtom(
        atom_id="sample-atom-physics-001",
        schema_version="1.0.0",
        atom_version=1,
        active=True,
        atom_type=AtomType.QUESTION,
        title="Harmonic oscillation time period",
        taxonomy=TaxonomyReference(
            chapter_id="oscillations",
            topic_id="simple-harmonic-motion",
            subtopic_id="time-period-shm",
        ),
        provenance=[
            ProvenanceRecord(
                source_id="src-mock-01",
                file_name="mock_01.pdf",
                page_start=1,
                page_end=1,
                source_locator="Q1",
            )
        ],
        confidence=0.98,
        verification_status=AtomStatus.VERIFIED,
        content_hash="11112222333344445555666677778888",
        question=QuestionPayload(
            statement=r"A body executes SHM with amplitude $A = 2\text{ m}$. Find its time period.",
            options=[
                QuestionOption(id="A", text=r"$2\text{ s}$"),
                QuestionOption(id="B", text=r"$4\text{ s}$"),
            ],
            source_claimed_answer="A",
            verified_answer="A",
            difficulty=DifficultyLevel.L2,
            solution_methods=[
                SolutionMethod(method_name="Standard", steps="T = 2 pi / omega", source_attributed=True)
            ],
            concepts=["shm", "time-period"],
        ),
    )


@pytest.fixture
def sample_atom_2() -> KnowledgeAtom:
    # Exact duplicate of sample_atom_1 with different formatting and whitespace
    return KnowledgeAtom(
        atom_id="sample-atom-physics-002",
        schema_version="1.0.0",
        atom_version=1,
        active=True,
        atom_type=AtomType.QUESTION,
        title="Harmonic oscillation time period duplicate",
        taxonomy=TaxonomyReference(
            chapter_id="oscillations",
            topic_id="simple-harmonic-motion",
            subtopic_id="time-period-shm",
        ),
        provenance=[
            ProvenanceRecord(
                source_id="src-mock-02",
                file_name="mock_02.pdf",
                page_start=5,
                page_end=5,
                source_locator="Problem 12",
            )
        ],
        confidence=0.99,
        verification_status=AtomStatus.VERIFIED,
        content_hash="99998888777766665555444433332222",
        question=QuestionPayload(
            statement=r"Choose the correct option: A body executes SHM with amplitude \( A=2\text{ m} \). Find its time period.",
            options=[
                QuestionOption(id="A", text=r"(A) \(2\text{ s}\)"),
                QuestionOption(id="B", text=r"(B) \(4\text{ s}\)"),
            ],
            source_claimed_answer="A",
            verified_answer="A",
            difficulty=DifficultyLevel.L2,
            solution_methods=[
                SolutionMethod(method_name="Alternative Energy Method", steps="E = 1/2 k A^2", source_attributed=True)
            ],
            concepts=["shm", "time-period"],
        ),
    )


# 1. Normalization tests
def test_normalization_whitespace_and_unicode():
    raw = "A   block   of   mass\u00A0M \u2013 moving with velocity\u2014v \u2212 5 m/s."
    cleaned = clean_statement_text(raw)
    assert "   " not in cleaned
    assert "\u00A0" not in cleaned
    assert "-" in cleaned


def test_normalization_latex_delimiters():
    raw = r"Find \( x \) when \[ y = 10 \]."
    norm = normalize_latex(raw)
    assert r"\(" not in norm
    assert r"\[" not in norm
    assert "$x$" in norm
    assert "$$y = 10$$" in norm or "$$y=10$$" in norm


def test_normalization_option_prefixes():
    assert clean_option_text("(A) $10\\text{ m/s}$") == "$10\\text{m/s}$"
    assert clean_option_text("A. 25 J") == "25 J"
    assert clean_option_text("[B] \\sqrt{3}") == "\\sqrt{3}"


def test_extract_target_and_numericals():
    stmt = r"A particle moves in a circle. Find the time period if radius is $2\text{ m}$ and speed is $4\text{ m/s}$."
    target = extract_target_quantity(stmt)
    nums = extract_numerical_values(stmt)
    assert target == "time_period"
    assert "2" in nums
    assert "4" in nums


# 2. Exact Deduplication & Fingerprinting Invariance
def test_exact_dedup_hash_invariance(sample_atom_1, sample_atom_2):
    fp1 = compute_normalized_fingerprint(sample_atom_1)
    fp2 = compute_normalized_fingerprint(sample_atom_2)

    # Statements should normalize to the identical text
    assert fp1.statement_normalized == fp2.statement_normalized
    assert fp1.statement_hash == fp2.statement_hash
    assert fp1.problem_hash == fp2.problem_hash


# 3. Candidate Generation
def test_candidate_generation_exact_and_taxonomy(sample_atom_1, sample_atom_2):
    cands, stats = generate_candidate_pairs([sample_atom_1, sample_atom_2])
    assert len(cands) == 1
    assert cands[0].generation_method == "EXACT_HASH_MATCH"
    assert "EXACT_PROBLEM_HASH" in cands[0].blocking_signals
    assert cands[0].comparison_features["same_target"] is True


def test_superficial_similarity_does_not_force_merge():
    # Two questions with identical physics topic but different questions
    a1 = KnowledgeAtom(
        atom_id="atom-pendulum-01",
        schema_version="1.0.0",
        atom_version=1,
        active=True,
        atom_type=AtomType.QUESTION,
        title="Simple pendulum length",
        taxonomy=TaxonomyReference(chapter_id="oscillations", topic_id="pendulum"),
        provenance=[ProvenanceRecord(source_id="s1", file_name="f1.pdf", page_start=1, page_end=1)],
        confidence=0.95,
        verification_status=AtomStatus.VERIFIED,
        content_hash="h1111111111111111",
        question=QuestionPayload(
            statement="A simple pendulum has time period 2 s. What is its length?",
            verified_answer="1 m",
            difficulty=DifficultyLevel.L1,
        ),
    )
    a2 = KnowledgeAtom(
        atom_id="atom-pendulum-02",
        schema_version="1.0.0",
        atom_version=1,
        active=True,
        atom_type=AtomType.QUESTION,
        title="Simple pendulum frequency on moon",
        taxonomy=TaxonomyReference(chapter_id="oscillations", topic_id="pendulum"),
        provenance=[ProvenanceRecord(source_id="s2", file_name="f2.pdf", page_start=2, page_end=2)],
        confidence=0.95,
        verification_status=AtomStatus.VERIFIED,
        content_hash="h2222222222222222",
        question=QuestionPayload(
            statement="A simple pendulum has frequency 0.5 Hz on Earth. What is its frequency on Moon?",
            verified_answer="0.2 Hz",
            difficulty=DifficultyLevel.L2,
        ),
    )

    cands, stats = generate_candidate_pairs([a1, a2])
    assert len(cands) == 1
    # Candidate was generated via taxonomy blocking, but comparison features reveal material difference
    cand = cands[0]
    assert cand.comparison_features["same_target"] is False
    assert cand.comparison_features["material_problem_difference"] is True


# 4. Deterministic Canonical Selection
def test_deterministic_canonical_selection(sample_atom_1, sample_atom_2):
    # sample_atom_1 and sample_atom_2
    rep = select_canonical_representative([sample_atom_1, sample_atom_2])
    # Both are VERIFIED. Let's see: sample_atom_1 has atom_id "sample-atom-physics-001"
    # sample_atom_2 has atom_id "sample-atom-physics-002"
    assert rep.atom_id in ("sample-atom-physics-001", "sample-atom-physics-002")
    # Repeated call must yield the exact same representative (idempotency)
    assert select_canonical_representative([sample_atom_1, sample_atom_2]).atom_id == rep.atom_id
    assert select_canonical_representative([sample_atom_2, sample_atom_1]).atom_id == rep.atom_id


# 5. Staging Gate & Application
def test_dedup_gate_stages_and_applies_exact_duplicate(sample_atom_1, sample_atom_2):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        atoms_dir = tmp_path / "kb" / "atoms"
        dedup_dir = tmp_path / "kb" / "dedup"
        review_dir = tmp_path / "review" / "queue" / "deduplication"
        reports_dir = tmp_path / "build" / "reports"
        staging_dir = tmp_path / "build" / "staging" / "deduplication"

        atoms_dir.mkdir(parents=True)
        (atoms_dir / f"{sample_atom_1.atom_id}.json").write_text(sample_atom_1.model_dump_json(), encoding="utf-8")
        (atoms_dir / f"{sample_atom_2.atom_id}.json").write_text(sample_atom_2.model_dump_json(), encoding="utf-8")

        cand = DedupCandidate(
            candidate_id="cand-001-002",
            atom_a_id=sample_atom_1.atom_id,
            atom_b_id=sample_atom_2.atom_id,
            generation_method="EXACT_HASH_MATCH",
            blocking_signals=["EXACT_PROBLEM_HASH"],
        )

        decision = DedupDecision(
            candidate_id="cand-001-002",
            decision_class=DedupDecisionClass.MULTI_METHOD_SAME_PROBLEM,
            duplicate_confidence=0.99,
            same_underlying_problem=True,
            same_concept_only=False,
            rationale="Identical physical problem with two distinct solution methods.",
            recommended_action=DedupAction.MERGE,
            agent_identity="physics-deduplicator",
            agent_conversation_id="conv-test-123",
        )

        # Stage decision file
        dec_file = tmp_path / "decisions.json"
        dec_file.write_text(json.dumps([decision.model_dump(mode="json")]), encoding="utf-8")
        ok, staged_path, errs = stage_dedup_decisions_file(dec_file, staging_dir=staging_dir)
        assert ok is True
        assert staged_path.exists()
        assert len(errs) == 0

        # Apply deduplication
        result = apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        assert len(result.merged_clusters) == 1
        cluster = result.merged_clusters[0]
        assert cluster.cluster_type == DedupDecisionClass.MULTI_METHOD_SAME_PROBLEM
        assert len(cluster.member_atom_ids) == 2

        # Invariant: Provenance from both sources is preserved
        prov_sources = {p["source_id"] for p in cluster.preserved_provenance}
        assert prov_sources == {"src-mock-01", "src-mock-02"}

        # Invariant: Solution methods from both atoms are preserved
        method_names = {m["method_name"] for m in cluster.preserved_solution_methods}
        assert "Standard" in method_names
        assert "Alternative Energy Method" in method_names

        # Invariant: Mappings exist for both atoms
        assert len(result.mappings) == 2
        for m in result.mappings:
            assert m.canonical_atom_id == cluster.canonical_atom_id

        # Invariant: Audit journal has records
        assert len(result.audit_records) >= 2
        journal_path = dedup_dir / "audit_journal.jsonl"
        assert journal_path.exists()


# 6. Physical Answer Conflict Rejection & Review Routing
def test_answer_conflict_is_routed_to_review(sample_atom_1, sample_atom_2):
    # Alter atom 2 answer to create an explicit physics conflict
    sample_atom_2.question.verified_answer = "B"  # atom 1 has "A"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        atoms_dir = tmp_path / "kb" / "atoms"
        dedup_dir = tmp_path / "kb" / "dedup"
        review_dir = tmp_path / "review" / "queue" / "deduplication"
        reports_dir = tmp_path / "build" / "reports"

        atoms_dir.mkdir(parents=True)
        (atoms_dir / f"{sample_atom_1.atom_id}.json").write_text(sample_atom_1.model_dump_json(), encoding="utf-8")
        (atoms_dir / f"{sample_atom_2.atom_id}.json").write_text(sample_atom_2.model_dump_json(), encoding="utf-8")

        cand = DedupCandidate(
            candidate_id="cand-conflict-01",
            atom_a_id=sample_atom_1.atom_id,
            atom_b_id=sample_atom_2.atom_id,
            generation_method="EXACT_HASH_MATCH",
        )

        decision = DedupDecision(
            candidate_id="cand-conflict-01",
            decision_class=DedupDecisionClass.EXACT_DUPLICATE,
            duplicate_confidence=0.99,
            same_underlying_problem=True,
            same_concept_only=False,
            rationale="Claiming duplicate despite answer discrepancy.",
            recommended_action=DedupAction.MERGE,
            agent_identity="physics-deduplicator",
            agent_conversation_id="conv-conflict-01",
        )

        result = apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        # Gate must refuse silent merge
        assert len(result.merged_clusters) == 0
        assert len(result.review_items) == 1
        assert result.review_items[0]["reason"] == "PHYSICS_ANSWER_CONFLICT"
        assert (review_dir / f"review_{cand.candidate_id}.json").exists()


# 7. Low Confidence & Uncertain Decision Routing
def test_uncertain_and_low_confidence_routing(sample_atom_1, sample_atom_2):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        atoms_dir = tmp_path / "kb" / "atoms"
        dedup_dir = tmp_path / "kb" / "dedup"
        review_dir = tmp_path / "review" / "queue" / "deduplication"
        reports_dir = tmp_path / "build" / "reports"

        atoms_dir.mkdir(parents=True)
        (atoms_dir / f"{sample_atom_1.atom_id}.json").write_text(sample_atom_1.model_dump_json(), encoding="utf-8")
        (atoms_dir / f"{sample_atom_2.atom_id}.json").write_text(sample_atom_2.model_dump_json(), encoding="utf-8")

        cand = DedupCandidate(
            candidate_id="cand-lowconf-01",
            atom_a_id=sample_atom_1.atom_id,
            atom_b_id=sample_atom_2.atom_id,
            generation_method="FEATURE_BLOCKING",
        )

        # Low confidence decision
        decision = DedupDecision(
            candidate_id="cand-lowconf-01",
            decision_class=DedupDecisionClass.SEMANTIC_DUPLICATE,
            duplicate_confidence=0.65,  # Below threshold 0.85
            same_underlying_problem=True,
            same_concept_only=False,
            rationale="Uncertain if notation shift changes physical conditions.",
            recommended_action=DedupAction.REVIEW,
            agent_identity="physics-deduplicator",
            agent_conversation_id="conv-lowconf-01",
        )

        result = apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        assert len(result.merged_clusters) == 0
        assert len(result.review_items) == 1
        assert result.review_items[0]["reason"] == "CONFIDENCE_BELOW_THRESHOLD"


# 8. Same Concept Kept Separate
def test_same_concept_kept_separate(sample_atom_1, sample_atom_2):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        atoms_dir = tmp_path / "kb" / "atoms"
        dedup_dir = tmp_path / "kb" / "dedup"
        review_dir = tmp_path / "review" / "queue" / "deduplication"
        reports_dir = tmp_path / "build" / "reports"

        atoms_dir.mkdir(parents=True)
        (atoms_dir / f"{sample_atom_1.atom_id}.json").write_text(sample_atom_1.model_dump_json(), encoding="utf-8")
        (atoms_dir / f"{sample_atom_2.atom_id}.json").write_text(sample_atom_2.model_dump_json(), encoding="utf-8")

        cand = DedupCandidate(
            candidate_id="cand-sameconcept-01",
            atom_a_id=sample_atom_1.atom_id,
            atom_b_id=sample_atom_2.atom_id,
            generation_method="TAXONOMY_BLOCKING",
        )

        decision = DedupDecision(
            candidate_id="cand-sameconcept-01",
            decision_class=DedupDecisionClass.SAME_CONCEPT_DIFFERENT_PROBLEM,
            duplicate_confidence=0.99,
            same_underlying_problem=False,
            same_concept_only=True,
            rationale="Both test SHM, but conditions and questions are materially distinct.",
            recommended_action=DedupAction.KEEP_SEPARATE,
            agent_identity="physics-deduplicator",
            agent_conversation_id="conv-sc-01",
        )

        result = apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        assert len(result.merged_clusters) == 0
        assert len(result.kept_separate) == 1
        assert result.kept_separate[0] == "cand-sameconcept-01"


# 9. Invariant: Canonical Atom Content Is NOT Modified
def test_canonical_atom_content_invariant_after_merge(sample_atom_1, sample_atom_2):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        atoms_dir = tmp_path / "kb" / "atoms"
        dedup_dir = tmp_path / "kb" / "dedup"
        review_dir = tmp_path / "review" / "queue" / "deduplication"
        reports_dir = tmp_path / "build" / "reports"

        atoms_dir.mkdir(parents=True)
        p1 = atoms_dir / f"{sample_atom_1.atom_id}.json"
        p2 = atoms_dir / f"{sample_atom_2.atom_id}.json"
        p1.write_text(sample_atom_1.model_dump_json(), encoding="utf-8")
        p2.write_text(sample_atom_2.model_dump_json(), encoding="utf-8")

        orig_p1_text = p1.read_text(encoding="utf-8")
        orig_p2_text = p2.read_text(encoding="utf-8")

        cand = DedupCandidate(
            candidate_id="cand-inv-01",
            atom_a_id=sample_atom_1.atom_id,
            atom_b_id=sample_atom_2.atom_id,
            generation_method="EXACT_HASH_MATCH",
        )

        decision = DedupDecision(
            candidate_id="cand-inv-01",
            decision_class=DedupDecisionClass.EXACT_DUPLICATE,
            duplicate_confidence=1.0,
            same_underlying_problem=True,
            same_concept_only=False,
            rationale="Exact duplicate merge.",
            recommended_action=DedupAction.MERGE,
            agent_identity="physics-deduplicator",
            agent_conversation_id="conv-inv-01",
        )

        apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        # Confirm atom files on disk remain completely unmodified
        assert p1.read_text(encoding="utf-8") == orig_p1_text
        assert p2.read_text(encoding="utf-8") == orig_p2_text


# 10. Invariant: Canonical KB Storage Contains Zero Test Fixtures
def test_canonical_kb_contains_no_test_fixtures():
    """Verify that kb/atoms/ contains only verified canonical physics atoms and zero synthetic fixtures."""
    kb_path = Path("kb/atoms")
    assert kb_path.exists(), "kb/atoms/ directory must exist"

    # Run the deterministic storage validator
    errors = validate_canonical_kb_storage_integrity(kb_path)
    assert len(errors) == 0, f"Canonical storage integrity violations found: {errors}"

    # Confirm exactly 35 genuine canonical atoms exist
    canonical_files = list(kb_path.glob("*.json"))
    assert len(canonical_files) == 35, f"Expected exactly 35 canonical atoms, found {len(canonical_files)}"

    for f in canonical_files:
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data.get("verification_status") == "VERIFIED"
        assert not data.get("is_test_fixture"), f"Test fixture found in canonical KB: {f.name}"
        assert "fixture_category" not in data
        # Ensure no synthetic naming markers exist
        lower_name = f.stem.lower()
        for marker in ["variant", "test", "fixture", "synthetic", "ambiguous", "conflict", "multimethod"]:
            assert marker not in lower_name, f"Prohibited marker '{marker}' in canonical atom '{f.name}'"


# 11. Test Fixtures Directory Integrity
def test_test_fixtures_directory_integrity():
    """Verify that test fixtures are segregated in tests/fixtures/dedup/ with explicit metadata."""
    fixtures_dir = Path("tests/fixtures/dedup")
    assert fixtures_dir.exists(), "tests/fixtures/dedup/ must exist"

    fixture_files = list(fixtures_dir.glob("*.json"))
    assert len(fixture_files) >= 4, f"Expected at least 4 test fixtures, found {len(fixture_files)}"

    for f in fixture_files:
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data.get("is_test_fixture") is True, f"Fixture {f.name} missing is_test_fixture=True"
        assert data.get("fixture_category") == "CONTROLLED_PILOT_FIXTURE"


# 12. Invariant: Idempotent Deduplication Application
def test_idempotent_deduplication_application(sample_atom_1, sample_atom_2):
    """Running deduplication gate twice against already-processed input creates zero duplicate clusters or mappings."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        atoms_dir = tmp_path / "kb" / "atoms"
        dedup_dir = tmp_path / "kb" / "dedup"
        review_dir = tmp_path / "review" / "queue" / "deduplication"
        reports_dir = tmp_path / "build" / "reports"

        atoms_dir.mkdir(parents=True)
        (atoms_dir / f"{sample_atom_1.atom_id}.json").write_text(sample_atom_1.model_dump_json(), encoding="utf-8")
        (atoms_dir / f"{sample_atom_2.atom_id}.json").write_text(sample_atom_2.model_dump_json(), encoding="utf-8")

        cand = DedupCandidate(
            candidate_id="cand-idempotent-01",
            atom_a_id=sample_atom_1.atom_id,
            atom_b_id=sample_atom_2.atom_id,
            generation_method="EXACT_HASH_MATCH",
        )

        decision = DedupDecision(
            candidate_id="cand-idempotent-01",
            decision_class=DedupDecisionClass.EXACT_DUPLICATE,
            duplicate_confidence=1.0,
            same_underlying_problem=True,
            same_concept_only=False,
            rationale="Exact duplicate idempotency test.",
            recommended_action=DedupAction.MERGE,
            agent_identity="physics-deduplicator",
            agent_conversation_id="conv-idemp-01",
        )

        # Run 1
        res1 = apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        clusters_1 = list((dedup_dir / "clusters").glob("*.json"))
        mappings_1 = list((dedup_dir / "mappings").glob("*.json"))
        journal_lines_1 = (dedup_dir / "audit_journal.jsonl").read_text(encoding="utf-8").strip().split("\n")

        assert len(clusters_1) == 1
        assert len(mappings_1) == 2

        # Run 2 (identical decisions and candidates)
        res2 = apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        clusters_2 = list((dedup_dir / "clusters").glob("*.json"))
        mappings_2 = list((dedup_dir / "mappings").glob("*.json"))
        journal_lines_2 = (dedup_dir / "audit_journal.jsonl").read_text(encoding="utf-8").strip().split("\n")

        # Counts must NOT double; clusters and mappings must remain unchanged
        assert len(clusters_2) == len(clusters_1)
        assert len(mappings_2) == len(mappings_1)
        assert len(journal_lines_2) == len(journal_lines_1)


# 13. Subject Isolation Invariant
def test_subject_isolation_blocks_cross_domain_merges(sample_atom_1, sample_atom_2):
    """Subject identity is a hard prerequisite: Chemistry/Math questions cannot merge into Physics."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        atoms_dir = tmp_path / "kb" / "atoms"
        dedup_dir = tmp_path / "kb" / "dedup"
        review_dir = tmp_path / "review" / "queue" / "deduplication"
        reports_dir = tmp_path / "build" / "reports"

        atoms_dir.mkdir(parents=True)
        (atoms_dir / f"{sample_atom_1.atom_id}.json").write_text(sample_atom_1.model_dump_json(), encoding="utf-8")
        (atoms_dir / f"{sample_atom_2.atom_id}.json").write_text(sample_atom_2.model_dump_json(), encoding="utf-8")

        # Disguise atom 2 with Chemistry subject in metadata
        cand = DedupCandidate(
            candidate_id="cand-subject-violation-01",
            atom_a_id=sample_atom_1.atom_id,
            atom_b_id=sample_atom_2.atom_id,
            generation_method="TAXONOMY_BLOCKING",
            candidate_metadata={"atom_b_subject": "CHEMISTRY"},
        )

        decision = DedupDecision(
            candidate_id="cand-subject-violation-01",
            decision_class=DedupDecisionClass.EXACT_DUPLICATE,
            duplicate_confidence=0.99,
            same_underlying_problem=True,
            same_concept_only=False,
            rationale="Attempting cross-subject merge.",
            recommended_action=DedupAction.MERGE,
            agent_identity="physics-deduplicator",
            agent_conversation_id="conv-subj-01",
        )

        result = apply_deduplication(
            decisions=[decision],
            candidates_map={cand.candidate_id: cand},
            atoms_dir=atoms_dir,
            dedup_dir=dedup_dir,
            review_queue_dir=review_dir,
            reports_dir=reports_dir,
        )

        # Merge must be strictly rejected
        assert len(result.merged_clusters) == 0
        assert len(result.rejected_items) == 1
        assert result.rejected_items[0]["reason"] == "SUBJECT_ISOLATION_VIOLATION"


# 14. Reproducible Canonical Representative Selection
def test_deterministic_reproducible_canonical_selection(sample_atom_1, sample_atom_2):
    """Canonical representative selection must be independent of list ordering or randomness."""
    rep_forward = select_canonical_representative([sample_atom_1, sample_atom_2])
    rep_reverse = select_canonical_representative([sample_atom_2, sample_atom_1])
    assert rep_forward.atom_id == rep_reverse.atom_id

    # Create a 3rd atom with lower verification status
    atom_3 = sample_atom_1.model_copy(deep=True)
    atom_3.atom_id = "sample-atom-physics-000"  # alphabetically smaller
    atom_3.verification_status = AtomStatus.STAGED

    # Even though atom_3 is alphabetically first, verified status must outrank staged status
    rep_with_staged = select_canonical_representative([atom_3, sample_atom_1, sample_atom_2])
    assert rep_with_staged.verification_status == AtomStatus.VERIFIED
    assert rep_with_staged.atom_id == rep_forward.atom_id


# 15. BaseSemanticRetriever Extension Interface
def test_base_semantic_retriever_extension_interface(sample_atom_1, sample_atom_2):
    """Verify that candidate generation extensible interface supports plugging in future semantic retrievers."""
    from typing import Dict, List, Tuple
    from jee_physics.models.dedup import NormalizedAtomFingerprint

    class MockEmbeddingRetriever(BaseSemanticRetriever):
        def retrieve_candidates(
            self,
            atoms: List[KnowledgeAtom],
            fingerprints: Dict[str, NormalizedAtomFingerprint],
            top_k: int = 5,
            threshold: float = 0.75,
        ) -> List[Tuple[str, str, float]]:
            return [(sample_atom_1.atom_id, sample_atom_2.atom_id, 0.95)]

    retriever = MockEmbeddingRetriever()
    cands, stats = generate_candidate_pairs(
        atoms=[sample_atom_1, sample_atom_2],
        semantic_retriever=retriever,
    )

    assert any(c.generation_method in ("EXACT_HASH_MATCH", "SEMANTIC_RETRIEVAL") for c in cands)
    assert stats["total_candidate_pairs_generated"] >= 1

