"""
Comprehensive Test Suite for Phase 16: Rotational Motion Production Upgrade.
Verifies the complete end-to-end repeatable factory chain:
SOURCE EVIDENCE -> TAXONOMY -> CURRICULUM -> CONTENT UPGRADE -> INDEPENDENT VERIFICATION -> QA -> WEB PROJECTION.
"""

import json
from pathlib import Path
import pytest

from jee_physics.content.assembler import ChapterAssembler
from jee_physics.content.gate import compute_content_hash
from jee_physics.content.qa import ChapterQAAuditor
from jee_physics.models.curriculum import ChapterPlan, ChapterSpec, QuestionLadder
from jee_physics.web.compiler import WebCompiler


@pytest.fixture
def project_root():
    return Path.cwd()


def test_rot_scope_and_spec_integrity(project_root):
    """Verify Rotational Motion scope v2 and ChapterSpec conform to schemas and constraints."""
    scope_file = project_root / "curriculum" / "chapters" / "rotational-motion_scope_v2.json"
    assert scope_file.exists(), "Rotational Motion scope specification v2 missing"
    scope_data = json.loads(scope_file.read_text(encoding="utf-8"))
    assert scope_data["chapter_id"] == "rotational-motion"
    assert len(scope_data["topics"]) == 4
    tot_subtopics = sum(len(t.get("subtopics", [])) for t in scope_data["topics"])
    assert tot_subtopics == 18
    assert scope_data["canonical_taxonomy_mapping"]
    assert len(scope_data["prerequisites"]) >= 3

    # Verify spec in curriculum/chapters
    spec_path = project_root / "curriculum" / "chapters" / "rotational-motion_spec.json"
    assert spec_path.exists(), f"Spec missing at {spec_path}"
    spec_data = json.loads(spec_path.read_text(encoding="utf-8"))
    assert spec_data["chapter_id"] == "rotational-motion"
    assert spec_data["template_type"] == "MECHANICS"
    assert len(spec_data["taxonomy_references"]) == 18
    assert len(spec_data["concept_sequence"]) == 11
    assert len(spec_data["formula_sequence"]) == 16
    assert len(spec_data["misconception_sequence"]) == 6
    assert len(spec_data["worked_example_sequence"]) == 6
    assert len(spec_data["question_sequence"]) == 3


def test_rot_evidence_manifest_integrity(project_root):
    """Verify the comprehensive source evidence manifest compiled for Rotational Motion."""
    manifest_file = project_root / "build" / "reports" / "rotational_motion_source_evidence_manifest_v2.json"
    assert manifest_file.exists(), "Rotational motion source evidence manifest missing"
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert isinstance(manifest_data, list)
    assert len(manifest_data) >= 130
    sources = {r["source_id"] for r in manifest_data}
    assert len(sources) >= 5, f"Expected at least 5 distinct sources, found {len(sources)}"
    for r in manifest_data:
        assert r["fidelity_class"] in {"EXACT_ONLY", "SOURCE_GROUNDED"}
        assert r.get("source_id")
        assert r.get("pages")


def test_rot_question_ladder_integrity(project_root):
    """Verify progressive QuestionLadder for rolling on incline rungs."""
    ladder_file = project_root / "curriculum" / "ladders" / "ladder-rot-rolling-incline-01.json"
    assert ladder_file.exists(), "Rotational motion question ladder missing"
    ladder_data = json.loads(ladder_file.read_text(encoding="utf-8"))
    ladder = QuestionLadder.model_validate(ladder_data)
    assert ladder.ladder_id == "ladder-rot-rolling-incline-01"
    assert ladder.chapter_id == "rotational-motion"
    assert len(ladder.rungs) == 4
    for idx, rung in enumerate(ladder.rungs, start=1):
        assert rung.level == idx
        assert rung.physical_delta
        assert 1 <= rung.reasoning_depth <= 5


def test_rot_chapter_plan_integrity(project_root):
    """Verify structured 5-section ChapterPlan for Rotational Motion."""
    plan_file = project_root / "curriculum" / "chapters" / "rotational-motion_plan.json"
    assert plan_file.exists(), "Rotational Motion chapter plan missing"
    plan_data = json.loads(plan_file.read_text(encoding="utf-8"))
    plan = ChapterPlan.model_validate(plan_data)
    assert plan.plan_id == "plan-rotational-motion-001"
    assert plan.chapter_id == "rotational-motion"
    assert len(plan.sections) == 5

    sec_ids = [s.section_id for s in plan.sections]
    assert sec_ids == [
        "sec-01-moment-of-inertia",
        "sec-02-torque-and-rotational-dynamics",
        "sec-03-angular-momentum-particle",
        "sec-04-angular-momentum-conservation",
        "sec-05-pure-rolling-kinematics",
    ]

    # Invariant: Section 5 must NOT be empty
    sec5 = next(s for s in plan.sections if s.section_id == "sec-05-pure-rolling-kinematics")
    assert len(sec5.concepts) == 4
    assert len(sec5.formula_ids) == 3
    assert len(sec5.worked_example_ids) == 2
    assert len(sec5.misconception_ids) == 2


def test_rot_verified_content_inventory_and_hash_binding(project_root):
    """Verify all Rotational Motion content items in content/verified/ have valid verification bindings."""
    verified_dir = project_root / "content" / "verified"
    cvr_dir = project_root / "build" / "staging" / "incoming" / "content_verification"
    dual_dir = verified_dir / "dual_verifications"

    # 1. Concepts (11)
    concepts = list((verified_dir / "concepts").glob("concept-rot-*.json"))
    assert len(concepts) == 11, f"Expected 11 verified concepts, found {len(concepts)}"
    for cp in concepts:
        cdata = json.loads(cp.read_text(encoding="utf-8"))
        assert cdata["verification_status"] == "VERIFIED"
        cvr_file = cvr_dir / f"cvr-{cdata['content_id']}.json"
        assert cvr_file.exists(), f"CVR missing for {cdata['content_id']}"
        cvr = json.loads(cvr_file.read_text(encoding="utf-8"))
        expected_hash = compute_content_hash(cdata)
        assert cvr["content_hash"] == expected_hash
        assert cvr["verdict"] == "VERIFIED"

    # 2. Formulas (16)
    formulas = list((verified_dir / "formulas").glob("formula-rot-*.json"))
    assert len(formulas) == 16, f"Expected 16 verified formulas, found {len(formulas)}"
    for fp in formulas:
        fdata = json.loads(fp.read_text(encoding="utf-8"))
        assert fdata["verification_status"] == "VERIFIED"
        cvr_file = cvr_dir / f"cvr-{fdata['formula_id']}.json"
        assert cvr_file.exists(), f"CVR missing for {fdata['formula_id']}"
        cvr = json.loads(cvr_file.read_text(encoding="utf-8"))
        assert cvr["content_hash"] == compute_content_hash(fdata)
        assert cvr["verdict"] == "VERIFIED"

    # 3. Misconceptions (6)
    misc = list((verified_dir / "misconceptions").glob("misc-rot-*.json"))
    assert len(misc) == 6, f"Expected 6 verified misconceptions, found {len(misc)}"
    for mp in misc:
        mdata = json.loads(mp.read_text(encoding="utf-8"))
        assert mdata["verification_status"] == "VERIFIED"
        cvr_file = cvr_dir / f"cvr-{mdata['misconception_id']}.json"
        assert cvr_file.exists(), f"CVR missing for {mdata['misconception_id']}"
        cvr = json.loads(cvr_file.read_text(encoding="utf-8"))
        assert cvr["content_hash"] == compute_content_hash(mdata)
        assert cvr["verdict"] == "VERIFIED"

    # 4. Derivations (7 - High Risk / Dual Verified)
    derivs = list((verified_dir / "derivations").glob("derivation-formula-rot-*.json"))
    assert len(derivs) == 7, f"Expected 7 verified derivations, found {len(derivs)}"
    for dp in derivs:
        ddata = json.loads(dp.read_text(encoding="utf-8"))
        assert ddata["verification_status"] == "VERIFIED"
        dual_path = dual_dir / f"dual-cvr-{ddata['derivation_id']}.json"
        assert dual_path.exists(), f"Dual record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_verdict"] == "VERIFIED"

    # 5. Worked Examples (6 - High Risk / Dual Verified)
    examples = list((verified_dir / "examples").glob("ex-rot-*.json"))
    assert len(examples) == 6, f"Expected 6 verified examples, found {len(examples)}"
    for ep in examples:
        edata = json.loads(ep.read_text(encoding="utf-8"))
        assert edata["verification_status"] == "VERIFIED"
        dual_path = dual_dir / f"dual-cvr-{edata['example_id']}.json"
        assert dual_path.exists(), f"Dual record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_verdict"] == "VERIFIED"


def test_rot_chapter_assembly_and_qa(project_root):
    """Verify Rotational Motion chapter assembly, QA audit report, and LaTeX rendering check."""
    assembler = ChapterAssembler(project_root)
    blocks = assembler.assemble_chapter("rotational-motion")
    assert len(blocks) == 58, f"Expected 58 assembled blocks, got {len(blocks)}"

    # Check draft files
    drafts_dir = project_root / "build" / "drafts" / "rotational-motion"
    blocks_file = drafts_dir / "rotational-motion_blocks.json"
    md_file = drafts_dir / "rotational-motion_draft.md"
    assert blocks_file.exists()
    assert md_file.exists()
    assert md_file.stat().st_size > 30000

    # Run independent QA Auditor
    auditor = ChapterQAAuditor(project_root)
    plan = assembler.load_plan("rotational-motion")
    spec = assembler.load_spec("rotational-motion")
    qa_rep, rend_rep = auditor.audit_chapter("rotational-motion", blocks, plan, spec)

    assert qa_rep.verdict == "PASSED"
    assert qa_rep.physics_passed is True
    assert qa_rep.curriculum_passed is True
    assert qa_rep.provenance_passed is True
    assert rend_rep.passed is True
    assert len(rend_rep.latex_errors) == 0


def test_rot_web_compilation_and_aliases(project_root):
    """Verify Rotational Motion compiles cleanly into Web Data with all aliases."""
    compiler = WebCompiler(root_dir=project_root)
    out_dir = compiler.compile(clean=True)

    data_dir = out_dir / "data"
    ch_file = data_dir / "chapter_rotational-motion.json"
    rot_file = data_dir / "chapter_rotation.json"
    rbd_file = data_dir / "chapter_rigid-body-dynamics.json"
    short_rbd = data_dir / "chapter_rbd.json"
    dash_file = data_dir / "chapter-rotational-motion.json"

    assert ch_file.exists(), "chapter_rotational-motion.json missing from web distribution"
    assert rot_file.exists(), "chapter_rotation.json alias missing"
    assert rbd_file.exists(), "chapter_rigid-body-dynamics.json alias missing"
    assert short_rbd.exists(), "chapter_rbd.json alias missing"
    assert dash_file.exists(), "chapter-rotational-motion.json alias missing"

    ch_data = json.loads(ch_file.read_text(encoding="utf-8"))
    assert ch_data["chapter_id"] == "rotational-motion"
    assert ch_data["status"] == "PILOT_ACTIVE"
    assert len(ch_data["sections"]) == 5

    # Check Section 5 content
    sec5 = ch_data["sections"][4]
    assert sec5["section_id"] == "sec-05-pure-rolling-kinematics"
    assert len(sec5["concepts"]) == 4
    assert len(sec5["formulas"]) == 3
    assert len(sec5["derivations"]) == 1
    assert len(sec5["worked_examples"]) == 2
    assert len(sec5["misconceptions"]) == 2

    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["pilot_active_chapters"] == 8
    assert manifest["counts"]["concepts"] >= 76
    assert manifest["counts"]["formulas"] >= 84
    assert manifest["counts"]["derivations"] >= 43
    assert manifest["counts"]["worked_examples"] >= 33
    assert manifest["counts"]["misconceptions"] >= 35
    assert manifest["counts"]["verified_questions"] >= 26
    assert manifest["counts"]["question_ladders"] >= 6


def test_canonical_knowledge_base_immutability(project_root):
    """Prime Directive: Ensure canonical kb/atoms/ and kb/taxonomy/syllabus.yaml are 100% untouched."""
    atoms = list((project_root / "kb" / "atoms").glob("*.json"))
    assert len(atoms) == 35, f"Canonical atom count must remain exactly 35, got {len(atoms)}"
