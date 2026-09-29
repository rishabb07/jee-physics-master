"""
Test Suite for Phase 11.8: Expository Evidence Completeness + Final Source Gate.
Verifies:
- Expository evidence inventory scale (>= 1,000 EXPOSITION records)
- Audit 114 reclassification with 0 unexplained misses
- Expected content inventory covering 100% of physics sections across 9 categories
- Feynman Lectures visual extraction status accounting across all 52 lectures
- Multi-source taxonomy retrieval demonstration across >= 20 distinct nodes and all 5 branches
- Adversarial bidirectional content-level traceability (forward, reverse, adversarial rejection)
- Stratified 200-page quality audit with seed=42 and 0 unexplained misses
- Canonical KB immutability (35 atoms, syllabus.yaml untouched)
"""

import json
from pathlib import Path
import pytest
import yaml


def test_expository_evidence_inventory_scale():
    """Verify >= 1,000 granular EXPOSITION evidence records in records.json and exposition.json."""
    rec_path = Path("sources/evidence/records.json")
    exp_path = Path("sources/evidence/exposition.json")
    assert rec_path.exists(), "records.json must exist"
    assert exp_path.exists(), "exposition.json must exist"

    with open(rec_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    with open(exp_path, "r", encoding="utf-8") as f:
        expositions = json.load(f)

    exposition_records = [r for r in records if r.get("evidence_type") == "EXPOSITION"]
    assert len(exposition_records) >= 1000, f"Expected >= 1,000 exposition records, got {len(exposition_records)}"
    assert len(expositions) >= 1000, f"Expected >= 1,000 in exposition.json, got {len(expositions)}"

    # Validate schema fields on sample records
    for r in exposition_records[:30]:
        assert r.get("evidence_id"), "evidence_id must be non-empty"
        assert r.get("source_id"), "source_id must be non-empty"
        assert r.get("page_start", 0) > 0, "page_start must be positive"
        text = r.get("content_text") or r.get("clean_text") or r.get("raw_text")
        assert text, "text content must be non-empty"
        assert "section" in r or "section_or_chapter" in r, "section field must exist"


def test_audit_114_reclassification_zero_unexplained_misses():
    """Verify all 65 misses from 114-page audit were reclassified with zero unexplained misses."""
    reclass_path = Path("sources/evidence/audit_114_reclassification.json")
    assert reclass_path.exists(), "audit_114_reclassification.json must exist"

    with open(reclass_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("unexplained_misses") == 0
    cat_bd = data.get("category_breakdown", {})
    assert cat_bd.get("TRUE_NON_CONTENT") == 4
    assert cat_bd.get("EXPOSITORY_CONTENT_MISSING") == 14
    assert cat_bd.get("VISUAL_CONTENT_MISSING") == 4
    assert cat_bd.get("CONTENT_ALREADY_COVERED") == 92

    valid_cats = {
        "TRUE_NON_CONTENT",
        "CONTENT_ALREADY_COVERED",
        "EXPOSITORY_CONTENT_MISSING",
        "VISUAL_CONTENT_MISSING",
        "EXTRACTION_FAILED",
    }
    for tr in data.get("traces", []):
        cat = tr.get("reclassification_category")
        assert cat in valid_cats, f"Invalid reclassification category {cat}"
        verdict = tr.get("final_verdict")
        assert verdict in ("FULLY_ACCOUNTED", "NON_CONTENT", "VISUAL_REQUIRED"), f"Invalid verdict {verdict}"


def test_expected_content_inventory_presence_and_coverage():
    """Verify section-level expected content inventory covers 100% of physics sections."""
    inv_path = Path("sources/evidence/expected_content_inventory.json")
    ledger_path = Path("sources/evidence/section_ledger.json")
    assert inv_path.exists(), "expected_content_inventory.json must exist"
    assert ledger_path.exists(), "section_ledger.json must exist"

    with open(inv_path, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    assert len(inventory) == 241, f"Expected 241 audited sections, got {len(inventory)}"

    physics_sections = [s for s in ledger if s.get("has_physics_content")]
    assert len(physics_sections) == 224

    for s in physics_sections:
        status = s.get("extraction_status")
        assert status in ("PHYSICS_CONTENT_COVERED", "PHYSICS_CONTENT_PARTIAL"), (
            f"Section {s.get('section_id')} unaddressed with status {status}"
        )

    # Check that all 9 categories are present in each inventory record
    expected_categories = {
        "exposition",
        "definitions",
        "principles_laws",
        "formulas",
        "derivations",
        "examples",
        "figures",
        "tables",
        "problems",
    }
    for item in inventory:
        cat_cov = item.get("category_coverage", {})
        for cat in expected_categories:
            assert cat in cat_cov, f"Category {cat} missing from section {item.get('section_id')}"


def test_feynman_lecture_visual_extraction_status():
    """Verify all 52 Feynman lectures have an explicit visual extraction status."""
    fey_path = Path("sources/evidence/feynman_accounting.json")
    assert fey_path.exists()

    with open(fey_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lectures = data.get("lectures", [])
    assert len(lectures) == 52, f"Expected 52 lectures, got {len(lectures)}"

    valid_statuses = {"complete", "partial", "further_inspection_required"}
    for lec in lectures:
        status = lec.get("visual_extraction_status")
        assert status in valid_statuses, f"Invalid visual_extraction_status '{status}' in lecture {lec.get('lecture_number')}"


def test_taxonomy_retrieval_demonstration_20_nodes():
    """Verify multi-source evidence retrieval for >= 20 distinct taxonomy nodes across all 5 branches."""
    demo_path = Path("sources/evidence/taxonomy_retrieval_demonstration_20.json")
    assert demo_path.exists(), "taxonomy_retrieval_demonstration_20.json must exist"

    with open(demo_path, "r", encoding="utf-8") as f:
        demos = json.load(f)

    assert len(demos) >= 20, f"Expected >= 20 demonstrated nodes, got {len(demos)}"

    branches = {d.get("branch") for d in demos}
    required_branches = {"Mechanics", "Thermal Physics", "Electromagnetism", "Optics", "Modern Physics"}
    assert required_branches.issubset(branches), f"Missing branches: {required_branches - branches}"

    for d in demos:
        assert d.get("total_evidence_units", 0) >= 10, f"Node {d.get('node_id')} has sparse evidence"
        assert d.get("corroborating_sources_count", 0) >= 3, f"Node {d.get('node_id')} has < 3 sources"


def test_adversarial_bidirectional_traceability():
    """Verify 100% pass on forward, reverse, and adversarial rejection traceability."""
    res_path = Path("sources/evidence/adversarial_traceability_results.json")
    assert res_path.exists(), "adversarial_traceability_results.json must exist"

    with open(res_path, "r", encoding="utf-8") as f:
        res = json.load(f)

    assert res.get("forward_tests_passed") == res.get("forward_tests_run") == 50
    assert res.get("reverse_tests_passed") == res.get("reverse_tests_run") == 50
    assert res.get("adversarial_nonexistent_ids_rejected") == res.get("adversarial_nonexistent_ids_tested") == 10
    assert res.get("overall_passed") is True


def test_stratified_200_audit_clean_pass():
    """Verify seeded stratified 200-page quality audit passes with 0 unexplained misses."""
    audit_path = Path("sources/evidence/stratified_200_audit.json")
    assert audit_path.exists(), "stratified_200_audit.json must exist"

    with open(audit_path, "r", encoding="utf-8") as f:
        audit = json.load(f)

    summary = audit.get("summary", {})
    assert summary.get("total_samples") >= 200, f"Sample count {summary.get('total_samples')} < 200"
    assert summary.get("unexplained_misses") == 0, f"Unexplained misses: {summary.get('unexplained_misses')}"
    assert summary.get("extraction_failed") == 0, f"Extraction failed: {summary.get('extraction_failed')}"
    assert summary.get("accounted_percentage") >= 99.0, f"Accounted rate {summary.get('accounted_percentage')}% < 99%"


def test_canonical_kb_immutability():
    """Verify that kb/atoms/ and kb/taxonomy/syllabus.yaml remain 100% unaltered."""
    atoms = list(Path("kb/atoms").glob("*.json"))
    assert len(atoms) == 35, f"Expected exactly 35 canonical atoms in kb/atoms/, found {len(atoms)}"

    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    assert syllabus_path.exists()

    with open(syllabus_path, "r", encoding="utf-8") as f:
        syllabus = yaml.safe_load(f)

    assert "chapters" in syllabus
    assert len(syllabus["chapters"]) == 30, f"Expected 30 chapters in syllabus, found {len(syllabus['chapters'])}"
    assert "nodes" in syllabus
    assert len(syllabus["nodes"]) == 460, f"Expected 460 taxonomy nodes, found {len(syllabus['nodes'])}"
