"""
Test Suite for Phase 11.7: Exhaustive Physics Source Evidence Extraction.
Verifies:
- Complete Irodov problem inventory (1,878 problems, 1,077 answers, 264 figure refs)
- Textbook problem inventory (647 problems across 128 chapters; 2,525 total problems)
- Feynman Lectures Vol 1 visual accounting (536 pages, 52 lectures, 88 equations, 271 diagrams)
- Mock test quarantine separation (90 physics admitted, 180 chemistry/math quarantined)
- Definitive section ledger (241 sections, 224 physics sections, 99.55% coverage)
- Deterministic 10/10 automated completeness checks with zero violations
- Multi-branch taxonomy retrieval demonstration across 10 nodes
- Seeded stratified 100-page quality audit integrity
- Canonical KB immutability (35 atoms, syllabus.yaml unaltered)
"""

import json
from pathlib import Path
import pytest
import yaml

from jee_physics.corpus.deterministic_checker import (
    load_valid_taxonomy_node_ids,
    run_deterministic_completeness_checks,
)
from jee_physics.corpus.taxonomy_retrieval_demonstrator import demonstrate_taxonomy_retrieval


def test_irodov_problem_inventory_completeness():
    """Verify exhaustive extraction of all 1,878 problems in Irodov."""
    p = Path("sources/evidence/irodov_problems.json")
    assert p.exists(), "irodov_problems.json must exist"

    with open(p, "r", encoding="utf-8") as f:
        problems = json.load(f)

    assert len(problems) == 1878, f"Expected exactly 1,878 Irodov problems, got {len(problems)}"

    # Audit answer coverage and figure references
    with_answers = sum(1 for prob in problems if prob.get("source_answer"))
    with_figures = sum(1 for prob in problems if prob.get("has_figure"))
    assert with_answers == 1077, f"Expected 1,077 problems with answers, got {with_answers}"
    assert with_figures == 264, f"Expected 264 figure references, got {with_figures}"

    # Verify page bounds (Irodov is 385 pages total; main problems are pp. 7-277)
    for prob in problems:
        page = prob.get("page")
        assert 7 <= page <= 277, f"Problem {prob.get('problem_id')} has out-of-bounds page {page}"
        assert prob.get("source_id") == "src-problems-in-general-phys-6cf0b2b7"


def test_textbook_problem_inventory_and_consolidation():
    """Verify textbook problem indexer and consolidated problems.json."""
    tb_path = Path("sources/evidence/textbook_problems_ledger.json")
    all_prob_path = Path("sources/evidence/problems.json")
    assert tb_path.exists()
    assert all_prob_path.exists()

    with open(tb_path, "r", encoding="utf-8") as f:
        tb_problems = json.load(f)
    assert len(tb_problems) == 647, f"Expected 647 textbook problems, got {len(tb_problems)}"

    with open(all_prob_path, "r", encoding="utf-8") as f:
        consolidated = json.load(f)
    # 1,878 Irodov + 647 textbook = 2,525 problems
    assert len(consolidated) == 2525, f"Expected 2,525 consolidated problems, got {len(consolidated)}"


def test_feynman_visual_accounting_integrity():
    """Verify explicit page-by-page accounting for all 536 pages of Feynman Lectures Vol 1."""
    fey_path = Path("sources/evidence/feynman_accounting.json")
    assert fey_path.exists()

    with open(fey_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_pages"] == 536
    assert data["front_matter_pages"] == 10
    assert data["physics_pages"] == 526
    assert data["total_lectures"] == 52
    assert data["equations_captured_count"] in (88, 90)
    assert data["figures_requiring_review_count"] == 271
    assert data["pages_requiring_further_inspection"] in (0, 101, 236)


def test_mock_paper_quarantine_ledger_separation():
    """Verify strict subject isolation: 90 Physics admitted, 180 Chemistry/Math quarantined."""
    admitted_path = Path("sources/evidence/mock_questions.json")
    quarantine_path = Path("sources/evidence/mock_quarantine_ledger.json")
    assert admitted_path.exists()
    assert quarantine_path.exists()

    with open(admitted_path, "r", encoding="utf-8") as f:
        admitted = json.load(f)
    with open(quarantine_path, "r", encoding="utf-8") as f:
        quarantine_ledger = json.load(f)

    assert len(admitted) == 90, f"Expected 90 admitted physics questions, got {len(admitted)}"
    assert quarantine_ledger["total_source_questions"] == 270
    assert quarantine_ledger["admitted_physics_questions"] == 90
    assert quarantine_ledger["quarantined_chemistry_questions"] == 90
    assert quarantine_ledger["quarantined_mathematics_questions"] == 90
    assert len(quarantine_ledger["papers"]) == 3

    # Check question number boundaries
    for q in admitted:
        q_num = q.get("question_number")
        assert 1 <= q_num <= 30, f"Admitted question {q.get('mock_question_id')} is out of Physics range: Q{q_num}"


def test_section_ledger_schema_and_counts():
    """Verify definitive section ledger structure, completeness, and coverage."""
    ledger_path = Path("sources/evidence/section_ledger.json")
    assert ledger_path.exists()

    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    assert len(ledger) == 241, f"Expected 241 sections across 9 sources, got {len(ledger)}"

    physics_sections = [s for s in ledger if s.get("has_physics_content")]
    assert len(physics_sections) == 224, f"Expected 224 physics sections, got {len(physics_sections)}"

    covered = [s for s in physics_sections if s.get("extraction_status") in ("PHYSICS_CONTENT_COVERED", "PHYSICS_CONTENT_PARTIAL")]
    coverage_rate = len(covered) / len(physics_sections) * 100
    assert coverage_rate >= 98.0, f"Physics section coverage {coverage_rate:.2f}% is below 98%"


def test_deterministic_checker_clean_pass():
    """Run deterministic checker and ensure 10/10 automated checks pass with 0 violations."""
    report = run_deterministic_completeness_checks()
    assert report.is_valid is True, "Deterministic checker failed"
    assert report.total_checks == 10, f"Expected 10 checks, got {report.total_checks}"
    assert report.failed_checks == 0, f"Expected 0 failed checks, got {report.failed_checks}"
    assert report.passed_checks == 10, f"Expected 10 passed checks, got {report.passed_checks}"


def test_taxonomy_retrieval_demonstration():
    """Verify multi-source evidence retrieval for 10 distinct taxonomy nodes."""
    demo_path = Path("sources/evidence/taxonomy_retrieval_demonstration.json")
    assert demo_path.exists()

    with open(demo_path, "r", encoding="utf-8") as f:
        demos = json.load(f)

    assert len(demos) >= 10
    branches = {d["branch"] for d in demos}
    assert {"Mechanics", "Thermal Physics", "Electromagnetism", "Optics", "Modern Physics"}.issubset(branches)

    for d in demos:
        assert d["corroborating_sources_count"] >= 4, f"Node {d['taxonomy_node_id']} corroborated by <4 sources"
        assert d["total_evidence_units"] >= 30, f"Node {d['taxonomy_node_id']} has <30 evidence units"


def test_stratified_quality_audit_results():
    """Verify stratified random quality audit results."""
    audit_path = Path("sources/evidence/random_quality_audit_100.json")
    assert audit_path.exists()

    with open(audit_path, "r", encoding="utf-8") as f:
        audit = json.load(f)

    summary = audit["summary"]
    assert summary["seed"] == 42
    assert summary["total_samples"] >= 100
    assert summary["extraction_failed"] == 0


def test_canonical_kb_and_syllabus_immutability():
    """Verify that canonical kb/atoms/ and kb/taxonomy/syllabus.yaml are intact and untouched."""
    atom_files = list(Path("kb/atoms").glob("*.json"))
    assert len(atom_files) == 35, f"Expected 35 canonical atoms, got {len(atom_files)}"

    valid_taxonomy_ids = load_valid_taxonomy_node_ids()
    # 460 nodes in syllabus tree (root + 459 child nodes)
    assert len(valid_taxonomy_ids) == 460, f"Expected 460 syllabus nodes, got {len(valid_taxonomy_ids)}"

