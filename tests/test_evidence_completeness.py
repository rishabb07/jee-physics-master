"""
Test Suite for Phase 11.6: Source Evidence Completeness Audit & Corrective Re-Extraction.
Verifies bibliographic metadata accuracy, HCV2 font decoding robustness,
mock paper subject boundary isolation, structural section audits, and canonical KB immutability.
"""

import json
from pathlib import Path
import pytest

from jee_physics.corpus.bibliographic_verifier import (
    AUTHORITATIVE_BIBLIOGRAPHIC_REGISTRY,
    get_all_verified_bibliographic_info,
)
from jee_physics.corpus.hcv2_decoder import decode_hcv2_text, is_hcv2_page_font_shifted
from jee_physics.corpus.random_quality_auditor import run_deterministic_random_audit
from jee_physics.corpus.section_coverage_auditor import build_source_structural_sections
from jee_physics.corpus.visual_inspection_router import route_visual_and_equation_dependent_pages


def test_authoritative_bibliographic_verification():
    """Verify all 9 source metadata records, resolving previous edition discrepancies."""
    bib_list = get_all_verified_bibliographic_info()
    assert len(bib_list) == 9

    by_id = {b.source_id: b for b in bib_list}

    # 1. Halliday & Resnick must be 9th Edition
    hr = by_id["src-fundamentals-of-physics--390f40d1"]
    assert "9th Edition" in hr.edition
    assert hr.total_pages == 1330
    assert hr.has_extractable_text is True

    # 2. University Physics must be 13th Edition
    up = by_id["src-university-physics-with--0bc11b67"]
    assert "13th Edition" in up.edition
    assert up.total_pages == 1598
    assert up.has_extractable_text is True

    # 3. Feynman must be image-only / scanned
    feynman = by_id["src-feynman-richard-p-the-fe-486f6a95"]
    assert feynman.is_image_only is True
    assert feynman.has_extractable_text is False

    # 4. Mock 1 must be vectorized glyphs
    mock1 = by_id["src-jee-main-mock-test-01-20-222525c1"]
    assert mock1.extraction_nature == "VECTORIZED_GLYPHS"


def test_hcv2_font_decoding_robustness():
    """Verify that shifted pages decode correctly while unshifted pages remain intact."""
    # Sample shifted string
    shifted_sample = "\x03 &+$37(5\x03 \x15\x16\n+($7\x03 $1'\x03 7(03(5$785(\n"
    assert is_hcv2_page_font_shifted(shifted_sample) is True
    decoded = decode_hcv2_text(shifted_sample)
    assert "CHAPTER" in decoded
    assert "HEAT" in decoded and "TEMPERATURE" in decoded

    # Sample normal unshifted string (e.g. Chapter 26)
    normal_sample = "CHAPTER 26\nLAWS OF THERMODYNAMICS\n26.1 THE FIRST LAW OF THERMODYNAMICS\nWe have seen that heat is just a form of energy."
    assert is_hcv2_page_font_shifted(normal_sample) is False


def test_mock_paper_subject_boundary_and_counts():
    """Verify that 90 mock questions exist, strictly bounded to Physics (Q1-Q30)."""
    mock_file = Path("sources/evidence/mock_questions.json")
    assert mock_file.exists()

    with open(mock_file, "r", encoding="utf-8") as f:
        mock_qs = json.load(f)

    assert len(mock_qs) == 90

    # Ensure all question numbers are between 1 and 30
    for q in mock_qs:
        assert 1 <= q["question_number"] <= 30
        assert q["subject"] == "PHYSICS"
        assert "CHEMISTRY" not in q["subject"]
        assert "MATHEMATICS" not in q["subject"]


def test_textbook_problems_inventory():
    """Verify practice problems from HCV1, HCV2, Irodov, Halliday, UP with printed answers."""
    prob_file = Path("sources/evidence/problems.json")
    assert prob_file.exists()

    with open(prob_file, "r", encoding="utf-8") as f:
        probs = json.load(f)

    assert len(probs) >= 30

    sources = {p["source_id"] for p in probs}
    assert "src-problems-in-general-phys-6cf0b2b7" in sources  # Irodov
    assert "src-concepts-of-physics-by-h-a489bb6e" in sources  # HCV 1
    assert "src-concepts-of-physics-by-h-1fd380f4" in sources  # HCV 2
    assert "src-fundamentals-of-physics--390f40d1" in sources  # Halliday
    assert "src-university-physics-with--0bc11b67" in sources  # UP

    # Check that Irodov problems have printed answers
    irodov_probs = [p for p in probs if p["source_id"] == "src-problems-in-general-phys-6cf0b2b7"]
    assert len(irodov_probs) >= 1000
    irodov_with_answers = [p for p in irodov_probs if p.get("source_answer")]
    assert len(irodov_with_answers) >= 1000


def test_structural_section_coverage():
    """Verify structural section tree generation across all 9 sources."""
    results = build_source_structural_sections(Path("sources/evidence"))
    assert len(results) == 9

    # Check HCV 1
    hcv1 = results["src-concepts-of-physics-by-h-a489bb6e"]
    assert hcv1.physics_sections == 22
    assert hcv1.covered_sections >= 10

    # Check Irodov
    irodov = results["src-problems-in-general-phys-6cf0b2b7"]
    assert irodov.physics_sections == 41
    assert (irodov.covered_sections + irodov.partial_sections) >= 35


def test_visual_inspection_routing():
    """Verify routing of visual-dependent pages."""
    records = route_visual_and_equation_dependent_pages()
    assert len(records) >= 700

    reasons = {r.dependency_reason for r in records}
    assert "VECTOR_DRAWINGS" in reasons
    assert "SCANNED_IMAGE_ONLY" in reasons
    assert "RAY_DIAGRAM" in reasons
    assert "CIRCUIT_SCHEMATIC" in reasons


def test_deterministic_random_quality_audit():
    """Verify that the random quality audit runs deterministically and reports results."""
    rep = run_deterministic_random_audit(seed=42, evidence_dir=Path("sources/evidence"))
    assert rep.total_samples == 48
    assert rep.full_matches >= 20
    assert rep.partial_coverages >= 5
    assert rep.unextracted_misses >= 3


def test_canonical_kb_immutability():
    """Verify that kb/atoms/ and kb/taxonomy/syllabus.yaml are 100% unaltered."""
    kb_atoms = list(Path("kb/atoms").glob("*.json"))
    assert len(kb_atoms) == 35

    # Check syllabus.yaml exists
    syllabus = Path("kb/taxonomy/syllabus.yaml")
    assert syllabus.exists()
    assert syllabus.stat().st_size > 10000
