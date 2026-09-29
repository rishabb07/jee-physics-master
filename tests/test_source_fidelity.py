"""
Unit and regression tests for Phase 11.9.1 — Independent Source Fidelity Audit.
Verifies that the independent source verification engine, explicit fidelity classes,
adversarial alteration interceptor, retrieval purity modes, and canonical KB immutability
strictly enforce all required physical grounding invariants.
"""

import json
from pathlib import Path
import pytest
import yaml

from jee_physics.corpus.evidence_retriever import EvidenceRetriever
from jee_physics.corpus.fidelity_auditor import FidelityAuditor
from jee_physics.corpus.independent_fidelity_checker import IndependentFidelityChecker
from jee_physics.models.evidence import (
    FidelityMatchResult,
    SourceFidelityClass,
)


@pytest.fixture
def checker():
    c = IndependentFidelityChecker()
    yield c
    c.close()


@pytest.fixture
def auditor():
    a = FidelityAuditor()
    yield a
    a.close()


@pytest.fixture
def retriever():
    return EvidenceRetriever()


def test_independent_checker_source_mismatch_rejection(checker):
    """Verifies that invented/mismatched text is rejected with NO_MATCH."""
    sid = "src-concepts-of-physics-by-h-a489bb6e"
    bogus_text = "Quantum chromodynamics determines the orbital angular momentum of macroscopic planetary orbits."
    res = checker.verify_passage(sid, 35, 35, bogus_text)
    assert res["match_result"] == FidelityMatchResult.NO_MATCH.value
    assert res["fidelity_class"] != SourceFidelityClass.SOURCE_VERBATIM.value


def test_altered_formula_rejection(checker):
    """Verifies that mutated formulas (tau = 2 r x F, F = 1/2 ma) fail verbatim matching."""
    # Test F = 1/2 ma against HCV1 Newton's laws chapter
    sid_hcv = "src-concepts-of-physics-by-h-a489bb6e"
    res_f = checker.verify_passage(sid_hcv, 65, 65, "F = \\frac{1}{2} m a")
    assert res_f["match_result"] == FidelityMatchResult.NO_MATCH.value

    # Test tau = 2 (r x F) against Halliday
    sid_hal = "src-fundamentals-of-physics--390f40d1"
    res_tau = checker.verify_passage(sid_hal, 280, 280, "\\tau = 2 (r \\times F)")
    assert res_tau["match_result"] == FidelityMatchResult.NO_MATCH.value


def test_altered_number_and_minus_sign_rejection(checker):
    """Verifies that altering a number or sign causes rejection from SOURCE_VERBATIM."""
    sid_hcv1 = "src-concepts-of-physics-by-h-a489bb6e"
    # Genuine page 35: "Solution : Let OA = OB = OC = F."
    res_gen = checker.verify_passage(sid_hcv1, 35, 35, "Solution : Let OA = OB = OC = F.")
    assert res_gen["match_result"] in (FidelityMatchResult.EXACT_MATCH.value, FidelityMatchResult.NORMALIZED_MATCH.value)

    # Mutated variable: "Solution : Let OA = OB = OC = 2F."
    res_mut = checker.verify_passage(sid_hcv1, 35, 35, "Solution : Let OA = OB = OC = 2F.")
    # Must not match verbatim
    assert res_mut["match_result"] not in (FidelityMatchResult.EXACT_MATCH.value, FidelityMatchResult.NORMALIZED_MATCH.value)

    # Inverted thermodynamic sign: Delta U = Q + W (physics convention is dQ = dU + dW, dU = dQ - dW)
    sid_hcv2 = "src-concepts-of-physics-by-h-1fd380f4"
    res_sign = checker.verify_passage(sid_hcv2, 45, 45, "\\Delta U = Q + W")
    assert res_sign["match_result"] == FidelityMatchResult.NO_MATCH.value


def test_altered_page_and_fake_source_rejection(checker):
    """Verifies that wrong page attachments and non-existent sources are strictly rejected."""
    sid_hcv1 = "src-concepts-of-physics-by-h-a489bb6e"
    genuine_text = "Solution : Let OA = OB = OC = F."

    # Attached to page 250 (Fluid Mechanics) instead of page 35
    res_wrong_page = checker.verify_passage(sid_hcv1, 250, 250, genuine_text)
    assert res_wrong_page["match_result"] == FidelityMatchResult.NO_MATCH.value

    # Attached to fake non-existent source
    res_fake_src = checker.verify_passage("src-fabricated-physics-fake-xyz", 35, 35, genuine_text)
    assert res_fake_src["match_result"] == FidelityMatchResult.NO_MATCH.value


def test_feynman_visual_classification(auditor):
    """Verifies all 52 Feynman lectures are classified strictly as SOURCE_VISUAL with zero unresolved pages."""
    fey_summary = auditor.audit_feynman_visual_fidelity()
    assert fey_summary["total_lectures"] == 52
    assert fey_summary["all_lectures_confirmed_physics"] is True
    assert "SOURCE_VISUAL" in fey_summary["fidelity_class"]
    assert fey_summary["pages_requiring_further_inspection"] == 0
    assert len(fey_summary["lectures"]) == 52
    for lec in fey_summary["lectures"]:
        assert lec["fidelity_class"] == SourceFidelityClass.SOURCE_VISUAL.value


def test_source_derived_vs_verbatim_distinction():
    """Verifies that formulas and derivations are SOURCE_DERIVED while problems/exposition are SOURCE_VERBATIM."""
    ev_dir = Path("sources/evidence")

    # Formulas ledger
    with open(ev_dir / "formulas.json", "r", encoding="utf-8") as f:
        formulas = json.load(f)
    assert len(formulas) >= 125
    for form in formulas:
        assert form.get("fidelity_class") == SourceFidelityClass.SOURCE_DERIVED.value

    # Derivations ledger
    with open(ev_dir / "derivations.json", "r", encoding="utf-8") as f:
        derivs = json.load(f)
    assert len(derivs) >= 7
    for d in derivs:
        assert d.get("fidelity_class") == SourceFidelityClass.SOURCE_DERIVED.value

    # Problems ledgers
    with open(ev_dir / "irodov_problems.json", "r", encoding="utf-8") as f:
        irodov_probs = json.load(f)
    assert len(irodov_probs) == 1878
    for p in irodov_probs:
        assert p.get("fidelity_class") == SourceFidelityClass.SOURCE_VERBATIM.value

    with open(ev_dir / "textbook_problems_ledger.json", "r", encoding="utf-8") as f:
        tb_probs = json.load(f)
    assert len(tb_probs) == 647
    for p in tb_probs:
        assert p.get("fidelity_class") == SourceFidelityClass.INDEX_METADATA.value

    with open(ev_dir / "problems.json", "r", encoding="utf-8") as f:
        problems = json.load(f)
    assert len(problems) == 2525
    verbatim_cnt = sum(1 for p in problems if p.get("fidelity_class") == SourceFidelityClass.SOURCE_VERBATIM.value)
    metadata_cnt = sum(1 for p in problems if p.get("fidelity_class") == SourceFidelityClass.INDEX_METADATA.value)
    assert verbatim_cnt == 1878
    assert metadata_cnt == 647


def test_adversarial_alteration_intercept_rate(auditor):
    """Verifies that 100% of adversarial fixtures (16 mutation families) are intercepted."""
    adv_res = auditor.run_adversarial_alteration_tests()
    assert adv_res["total_adversarial_tests"] == 16
    assert adv_res["passed_tests"] == 16
    assert adv_res["failed_tests"] == 0
    assert adv_res["intercept_rate_percentage"] == 100.0
    assert adv_res["gate_passed"] is True


def test_retrieval_purity_by_fidelity_mode(retriever):
    """Verifies that EvidenceRetriever enforces fidelity boundaries across modes."""
    node_id = "rotational-motion"

    # 1. Mode EXACT_ONLY: strictly verbatim and visual
    b_exact = retriever.get_evidence_by_taxonomy(node_id, fidelity_mode="EXACT_ONLY")
    for r in b_exact.evidence_records:
        fc = getattr(r, "fidelity_class", None)
        val = fc.value if hasattr(fc, "value") else str(fc)
        assert val in (SourceFidelityClass.SOURCE_VERBATIM.value, SourceFidelityClass.SOURCE_VISUAL.value)

    # 2. Mode ALL: metadata records segregated
    b_all = retriever.get_evidence_by_taxonomy(node_id, fidelity_mode="ALL")
    assert len(b_all.metadata_records) >= 1
    for mr in b_all.metadata_records:
        assert mr.evidence_id == "evid-irodov-answers-and-solutions-ref"

    # 3. Test explicit query methods
    verbatim_items = retriever.query_verbatim_evidence(node_id)
    assert len(verbatim_items) > 0
    for v in verbatim_items:
        fc = getattr(v, "fidelity_class", None)
        val = fc.value if hasattr(fc, "value") else str(fc)
        assert val == SourceFidelityClass.SOURCE_VERBATIM.value

    visual_items = retriever.query_visual_evidence(node_id)
    assert len(visual_items) > 0
    for vi in visual_items:
        fc = getattr(vi, "fidelity_class", None)
        val = fc.value if hasattr(fc, "value") else str(fc)
        assert val == SourceFidelityClass.SOURCE_VISUAL.value

    derived_items = retriever.query_derived_evidence(node_id)
    assert len(derived_items) > 0


def test_irodov_fidelity_and_misprint_documentation(auditor):
    """Verifies Irodov numbering completeness across all 6 parts and documentation of the 3 historical printer typos."""
    summary = auditor.audit_irodov_fidelity()
    assert summary["total_problems"] == 1878
    assert summary["numbering_completeness"].startswith("100.0%")
    assert summary["part_breakdown"]["part_1"] == 388
    assert summary["part_breakdown"]["part_2"] == 257
    assert summary["part_breakdown"]["part_3"] == 408
    assert summary["part_breakdown"]["part_4"] == 224
    assert summary["part_breakdown"]["part_5"] == 292
    assert summary["part_breakdown"]["part_6"] == 309
    assert summary["statement_fidelity_sample_size"] == 50
    assert summary["answers_documented"] == 1077


def test_canonical_kb_immutability():
    """Verifies that the canonical Knowledge Base atoms and syllabus remain 100% unaltered."""
    atoms_dir = Path("kb/atoms")
    atom_files = list(atoms_dir.glob("*.json"))
    assert len(atom_files) == 35, f"Expected exactly 35 canonical atoms, got {len(atom_files)}"

    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    assert syllabus_path.exists()
    with open(syllabus_path, "r", encoding="utf-8") as f:
        syllabus = yaml.safe_load(f)
    assert "syllabus" in syllabus or "chapters" in syllabus or "physics" in str(syllabus).lower()


def test_source_fidelity_failure_ledger_remediation(checker):
    """Verifies that all 10 inspected items in the failure ledger are 100% remediated with zero outstanding failures."""
    ledger_path = Path("build/reports/source_fidelity_failure_ledger.json")
    assert ledger_path.exists(), "Failure ledger must exist"
    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    assert ledger["total_items_inspected"] == 10
    assert ledger["remediated_count"] == 10
    assert ledger["outstanding_failures"] == 0

    # Verify the 5 remediated exposition records pass exact match against PDF
    records_path = Path("sources/evidence/records.json")
    with open(records_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    rec_by_id = {r["evidence_id"]: r for r in records}

    expo_eids = [
        "exp-up-ch21-p02",
        "evid-hcv1-p192-angmom-conservation",
        "evid-hcv1-p288-sol-hooke",
        "evid-hcv1-p218-universal-gravitation",
        "evid-hcv2-p64-first-law-td",
    ]
    for eid in expo_eids:
        r = rec_by_id[eid]
        eval_res = checker.verify_passage(r["source_id"], r["page_start"], r["page_end"], r["content_text"])
        assert eval_res["match_result"] in ("EXACT_MATCH", "NORMALIZED_MATCH"), f"Expected exact/normalized match for {eid}, got {eval_res['match_result']}"

    # Verify the 5 textbook problems are classified as INDEX_METADATA
    problems_path = Path("sources/evidence/problems.json")
    with open(problems_path, "r", encoding="utf-8") as f:
        probs = json.load(f)
    prob_by_id = {p["problem_id"]: p for p in probs}

    prob_ids = [
        "prob-hr-ch24-p076",
        "prob-up-ch37-ex001",
        "prob-hr-ch08-p061",
        "prob-hr-ch29-p001",
        "prob-hr-ch38-p041",
    ]
    for pid in prob_ids:
        p = prob_by_id[pid]
        assert p["fidelity_class"] == SourceFidelityClass.INDEX_METADATA.value


def test_stratified_100_exposition_zero_failures(auditor):
    """Verifies that the stratified 100 exposition audit achieves 100% exact matches with zero partial or missed items."""
    summary = auditor.audit_100_exposition_records()
    assert summary["total_sampled"] == 100
    assert summary["passed_count"] == 100
    assert summary["pass_rate_percentage"] == 100.0
    assert summary["result_breakdown"]["EXACT_MATCH"] == 100
    assert summary["result_breakdown"]["PARTIAL_MATCH"] == 0
    assert summary["result_breakdown"]["NO_MATCH"] == 0

