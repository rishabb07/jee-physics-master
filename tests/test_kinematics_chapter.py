"""
Comprehensive Test Suite for Phase 12: Kinematics Chapter.
Verifies the complete end-to-end chain:
SOURCE EVIDENCE -> TAXONOMY -> CURRICULUM -> CONTENT SYNTHESIS -> INDEPENDENT VERIFICATION -> QA -> WEB PROJECTION.
"""

import json
from pathlib import Path
import pytest

from jee_physics.content.assembler import ChapterAssembler
from jee_physics.content.gate import compute_content_hash
from jee_physics.content.qa import ChapterQAAuditor
from jee_physics.models.curriculum import ChapterPlan, ChapterSpec, QuestionLadder
from jee_physics.models.content import ContentVerificationStatus
from jee_physics.web.builder import WebDataBuilder
from jee_physics.web.compiler import WebCompiler


@pytest.fixture
def project_root():
    return Path.cwd()


def test_kinematics_scope_and_spec_integrity(project_root):
    """Verify Kinematics scope, ChapterSpec, and QuestionLadder conform to schemas and constraints."""
    scope_file = project_root / "curriculum" / "chapters" / "kinematics_scope.json"
    assert scope_file.exists(), "Kinematics scope specification missing"
    scope_data = json.loads(scope_file.read_text(encoding="utf-8"))
    assert scope_data["chapter_id"] == "kinematics"
    assert len(scope_data["topics"]) == 3
    tot_subtopics = sum(len(t.get("subtopics", [])) for t in scope_data["topics"])
    assert tot_subtopics == 16
    assert len(scope_data["source_grounding_summary"]["primary_sources"]) >= 6

    spec_file = project_root / "curriculum" / "chapters" / "kinematics_spec.json"
    assert spec_file.exists(), "Kinematics spec missing"
    spec_data = json.loads(spec_file.read_text(encoding="utf-8"))
    spec = ChapterSpec.model_validate(spec_data)
    assert spec.chapter_id == "kinematics"
    assert spec.template_type.value == "MECHANICS"
    assert len(spec.taxonomy_references) == 16
    assert len(spec.learning_objectives) == 8
    assert len(spec.concept_sequence) == 8
    assert len(spec.formula_sequence) == 12
    assert len(spec.misconception_sequence) == 5
    assert len(spec.worked_example_sequence) == 5
    assert len(spec.question_sequence) == 2


def test_kinematics_question_ladder_integrity(project_root):
    """Verify progressive QuestionLadder for inclined projectile motion."""
    ladder_file = project_root / "curriculum" / "ladders" / "ladder-kin-proj-incline-01.json"
    assert ladder_file.exists(), "Kinematics question ladder missing"
    ladder_data = json.loads(ladder_file.read_text(encoding="utf-8"))
    ladder = QuestionLadder.model_validate(ladder_data)
    assert ladder.ladder_id == "ladder-kin-proj-incline-01"
    assert ladder.chapter_id == "kinematics"
    assert len(ladder.rungs) == 4
    for idx, rung in enumerate(ladder.rungs, start=1):
        assert rung.level == idx
        assert rung.physical_delta
        assert 1 <= rung.reasoning_depth <= 5


def test_kinematics_chapter_plan_integrity(project_root):
    """Verify structured 4-section ChapterPlan for Kinematics."""
    plan_file = project_root / "curriculum" / "chapters" / "kinematics_plan.json"
    assert plan_file.exists(), "Kinematics chapter plan missing"
    plan_data = json.loads(plan_file.read_text(encoding="utf-8"))
    plan = ChapterPlan.model_validate(plan_data)
    assert plan.plan_id == "plan-kinematics-001"
    assert plan.chapter_id == "kinematics"
    assert len(plan.sections) == 4

    sec_ids = [s.section_id for s in plan.sections]
    assert sec_ids == [
        "sec-01-rectilinear-kinematics",
        "sec-02-acceleration-and-gravity",
        "sec-03-projectile-motion",
        "sec-04-relative-motion",
    ]


def test_kinematics_verified_content_inventory_and_hash_binding(project_root):
    """Verify all 36 Kinematics content items in content/verified/ have valid verification bindings."""
    verified_dir = project_root / "content" / "verified"

    # 1. Concepts (8)
    concepts = list((verified_dir / "concepts").glob("concept-kin-*.json"))
    assert len(concepts) == 8, f"Expected 8 verified kinematics concepts, found {len(concepts)}"
    for cp in concepts:
        cdata = json.loads(cp.read_text(encoding="utf-8"))
        assert cdata["verification_status"] == "VERIFIED"
        assert cdata["verification_record_id"].startswith("cvr-")
        # Validate hash immutability
        expected_hash = compute_content_hash(cdata)
        assert cdata["content_hash"] == expected_hash

    # 2. Formulas (12)
    formulas = list((verified_dir / "formulas").glob("formula-kin-*.json"))
    assert len(formulas) == 12, f"Expected 12 verified kinematics formulas, found {len(formulas)}"
    for fp in formulas:
        fdata = json.loads(fp.read_text(encoding="utf-8"))
        assert fdata["verification_status"] == "VERIFIED"
        assert fdata["verification_record_id"].startswith("cvr-")
        assert fdata["content_hash"] == compute_content_hash(fdata)

    # 3. Misconceptions (5)
    misc = list((verified_dir / "misconceptions").glob("misc-kin-*.json"))
    assert len(misc) == 5, f"Expected 5 verified kinematics misconceptions, found {len(misc)}"
    for mp in misc:
        mdata = json.loads(mp.read_text(encoding="utf-8"))
        assert mdata["verification_status"] == "VERIFIED"
        assert mdata["verification_record_id"].startswith("cvr-")
        assert mdata["content_hash"] == compute_content_hash(mdata)

    # 4. Derivations (6 - High Risk / Dual Verified)
    derivs = list((verified_dir / "derivations").glob("derivation-formula-kin-*.json"))
    assert len(derivs) == 6, f"Expected 6 verified kinematics derivations, found {len(derivs)}"
    for dp in derivs:
        ddata = json.loads(dp.read_text(encoding="utf-8"))
        assert ddata["verification_status"] == "VERIFIED"
        assert ddata["verification_record_id"].startswith("dual-cvr-")
        # Check dual record exists
        dual_path = verified_dir / "dual_verifications" / f"{ddata['verification_record_id']}.json"
        assert dual_path.exists(), f"Dual verification record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_verdict"] == "VERIFIED"

    # 5. Worked Examples (5 - High Risk / Dual Verified)
    examples = list((verified_dir / "examples").glob("ex-kin-*.json"))
    assert len(examples) == 5, f"Expected 5 verified kinematics examples, found {len(examples)}"
    for ep in examples:
        edata = json.loads(ep.read_text(encoding="utf-8"))
        assert edata["verification_status"] == "VERIFIED"
        assert edata["verification_record_id"].startswith("dual-cvr-")
        dual_path = verified_dir / "dual_verifications" / f"{edata['verification_record_id']}.json"
        assert dual_path.exists(), f"Dual verification record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_verdict"] == "VERIFIED"


def test_kinematics_chapter_assembly_and_qa(project_root):
    """Verify Kinematics chapter assembly, QA audit report, and LaTeX rendering check."""
    assembler = ChapterAssembler(project_root)
    blocks = assembler.assemble_chapter("kinematics")
    assert len(blocks) == 44, f"Expected 44 assembled blocks, got {len(blocks)}"

    # Check draft files
    drafts_dir = project_root / "build" / "drafts" / "kinematics"
    blocks_file = drafts_dir / "kinematics_blocks.json"
    md_file = drafts_dir / "kinematics_draft.md"
    assert blocks_file.exists()
    assert md_file.exists()
    assert md_file.stat().st_size > 40000

    # Run independent QA Auditor
    auditor = ChapterQAAuditor(project_root)
    plan = assembler.load_plan("kinematics")
    spec = assembler.load_spec("kinematics")
    qa_rep, rend_rep = auditor.audit_chapter("kinematics", blocks, plan, spec)

    assert qa_rep.verdict == "PASSED"
    assert qa_rep.physics_passed is True
    assert qa_rep.curriculum_passed is True
    assert qa_rep.provenance_passed is True
    assert rend_rep.passed is True
    assert len(rend_rep.latex_errors) == 0


def test_kinematics_web_compilation(project_root):
    """Verify Kinematics compiles cleanly into Web Data and Output distribution."""
    compiler = WebCompiler(root_dir=project_root)
    out_dir = compiler.compile(clean=True)

    data_dir = out_dir / "data"
    ch_file = data_dir / "chapter_kinematics.json"
    assert ch_file.exists(), "chapter_kinematics.json missing from web distribution"

    ch_data = json.loads(ch_file.read_text(encoding="utf-8"))
    assert ch_data["chapter_id"] == "kinematics"
    assert ch_data["status"] == "PILOT_ACTIVE"
    assert len(ch_data["sections"]) == 4

    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["pilot_active_chapters"] == 5
    assert manifest["counts"]["concepts"] == 20
    assert manifest["counts"]["formulas"] == 25
    assert manifest["counts"]["derivations"] == 19
    assert manifest["counts"]["worked_examples"] == 9
    assert manifest["counts"]["misconceptions"] == 13
    assert manifest["counts"]["verified_questions"] == 19
    assert manifest["counts"]["question_ladders"] == 2
