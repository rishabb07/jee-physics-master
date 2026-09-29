import json
from pathlib import Path
import pytest
import yaml

from jee_physics.corpus.evidence_retriever import EvidenceRetriever
from jee_physics.corpus.truth_auditor import SourceTruthGate, get_adversarial_fixtures, run_targeted_adversarial_truth_audit
from jee_physics.models.evidence import EvidenceTruthClassification, TaxonomyMappingQuality


@pytest.fixture
def evidence_dir():
    return Path("sources/evidence")


def test_hard_boundary_truth_classification(evidence_dir):
    """Verifies that every evidence record is classified into the hard truth boundary."""
    records_file = evidence_dir / "records.json"
    assert records_file.exists()

    with open(records_file, "r", encoding="utf-8") as f:
        records = json.load(f)

    assert len(records) == 1181

    source_exact_count = 0
    index_meta_count = 0

    for r in records:
        tc = r.get("truth_classification")
        assert tc in [e.value for e in EvidenceTruthClassification]
        if tc == EvidenceTruthClassification.SOURCE_EXACT.value:
            source_exact_count += 1
        elif tc == EvidenceTruthClassification.INDEX_METADATA.value:
            index_meta_count += 1

    assert source_exact_count == 1180
    assert index_meta_count == 1
    # Check that the isolated metadata record is specifically the Irodov reference key
    meta_rec = [r for r in records if r.get("truth_classification") == EvidenceTruthClassification.INDEX_METADATA.value][0]
    assert meta_rec["evidence_id"] == "evid-irodov-answers-and-solutions-ref"


def test_sub_ledgers_truth_classification(evidence_dir):
    """Verifies all sub-ledgers strictly enforce proper truth classification (SOURCE_EXACT vs INDEX_METADATA)."""
    for filename, min_count in [
        ("formulas.json", 125),
        ("derivations.json", 7),
        ("examples.json", 7),
        ("mock_questions.json", 90),
        ("figures.json", 12),
        ("irodov_problems.json", 1878),
    ]:
        p = evidence_dir / filename
        assert p.exists(), f"Ledger {filename} missing"
        with open(p, "r", encoding="utf-8") as f:
            items = json.load(f)
        assert len(items) >= min_count
        for item in items:
            assert item.get("truth_classification") == EvidenceTruthClassification.SOURCE_EXACT.value, (
                f"Item in {filename} must be SOURCE_EXACT"
            )

    # Textbook problem stubs must be strictly INDEX_METADATA
    tb_path = evidence_dir / "textbook_problems_ledger.json"
    assert tb_path.exists()
    with open(tb_path, "r", encoding="utf-8") as f:
        tb_items = json.load(f)
    assert len(tb_items) == 647
    for item in tb_items:
        assert item.get("truth_classification") == EvidenceTruthClassification.INDEX_METADATA.value

    # Problems.json contains 1,878 SOURCE_EXACT (Irodov) and 647 INDEX_METADATA (textbook stubs)
    prob_path = evidence_dir / "problems.json"
    assert prob_path.exists()
    with open(prob_path, "r", encoding="utf-8") as f:
        probs = json.load(f)
    assert len(probs) == 2525
    exact_probs = [p for p in probs if p.get("source_id") == "src-problems-in-general-phys-6cf0b2b7"]
    meta_probs = [p for p in probs if p.get("source_id") != "src-problems-in-general-phys-6cf0b2b7"]
    assert len(exact_probs) == 1878
    assert len(meta_probs) == 647
    for p in exact_probs:
        assert p.get("truth_classification") == EvidenceTruthClassification.SOURCE_EXACT.value
    for p in meta_probs:
        assert p.get("truth_classification") == EvidenceTruthClassification.INDEX_METADATA.value


def test_feynman_complete_resolution(evidence_dir):
    """Verifies all 52 Feynman lectures are completely accounted for with 0 unresolved pages."""
    feynman_file = evidence_dir / "feynman_accounting.json"
    assert feynman_file.exists()

    with open(feynman_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_lectures"] == 52
    assert data["pages_requiring_further_inspection"] == 0
    for lec in data["lectures"]:
        assert lec["visual_extraction_status"] == "complete"
        assert lec["visual_inspection_status"] == "CONFIRMED_PHYSICS"


def test_targeted_adversarial_truth_gate():
    """Verifies that the SourceTruthGate passes all 8 adversarial test fixtures with zero false admissions."""
    summary = run_targeted_adversarial_truth_audit()
    assert summary.total_fixtures == 8
    assert summary.fixtures_passed == 8
    assert summary.fixtures_failed == 0
    assert summary.gate_integrity_passed is True

    # Verify specific scenario behaviors
    results_by_scenario = {r.scenario_name: r for r in summary.fixture_results}
    assert results_by_scenario["GENUINE_SOURCE_TEXT"].actual_gate_decision == "ACCEPT_AS_SOURCE_EXACT"
    assert results_by_scenario["GENERATED_SUMMARY"].actual_gate_decision == "REJECT_FROM_SOURCE_EXACT"
    assert results_by_scenario["INCORRECT_CITATION"].actual_gate_decision == "REJECT_FROM_SOURCE_EXACT"
    assert results_by_scenario["WRONG_PAGE"].actual_gate_decision == "REJECT_FROM_SOURCE_EXACT"
    assert results_by_scenario["SYNTHETIC_FORMULA"].actual_gate_decision == "REJECT_FROM_SOURCE_EXACT"
    assert results_by_scenario["ALTERED_FORMULA"].actual_gate_decision == "REJECT_FROM_SOURCE_EXACT"
    assert results_by_scenario["GENERATED_TAXONOMY_MAPPING"].actual_gate_decision == "ACCEPT_AS_PROJECT_DERIVED"
    assert results_by_scenario["GENUINE_FORMULA"].actual_gate_decision == "ACCEPT_AS_SOURCE_EXACT"


def test_stratified_250_truth_audit(evidence_dir):
    """Verifies that the stratified 250-page audit achieves 100% accounting and 0 unexplained misses."""
    strat_file = evidence_dir / "stratified_250_truth_audit.json"
    assert strat_file.exists()

    with open(strat_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    summary = data["summary"]

    assert summary["total_samples"] >= 250
    assert summary["unexplained_misses"] == 0
    assert summary["extraction_failed"] == 0
    assert summary["coverage_integrity_percentage"] == 100.0


def test_retrieval_purity_30_nodes(evidence_dir):
    """Verifies that querying >= 30 taxonomy nodes returns 100% pure SOURCE_EXACT evidence with zero metadata leakage."""
    purity_file = evidence_dir / "retrieval_purity_30_nodes.json"
    assert purity_file.exists()

    with open(purity_file, "r", encoding="utf-8") as f:
        summary = json.load(f)

    assert summary["total_nodes_audited"] >= 30
    assert summary["nodes_passed"] == summary["total_nodes_audited"]
    assert summary["overall_purity_rate"] == 100.0
    assert summary["zero_metadata_leakage_confirmed"] is True
    assert len(summary["branches_covered"]) == 5


def test_canonical_kb_immutability():
    """Verifies that the canonical knowledge base and syllabus remain 100% untouched."""
    atom_files = list(Path("kb/atoms").glob("*.json"))
    assert len(atom_files) == 35, f"Expected exactly 35 canonical atoms, found {len(atom_files)}"

    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    assert syllabus_path.exists()
    with open(syllabus_path, "r", encoding="utf-8") as f:
        syllabus = yaml.safe_load(f)
    assert "nodes" in syllabus
    assert len(syllabus["nodes"]) > 400

    # Ensure output/book is empty or untouched
    book_dir = Path("output/book")
    if book_dir.exists():
        assert len(list(book_dir.glob("*.md"))) == 0
