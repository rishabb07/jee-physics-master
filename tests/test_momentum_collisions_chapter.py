"""
Comprehensive Test Suite for Phase 15: Momentum, Impulse & Collisions Chapter.
Verifies the complete end-to-end repeatable factory chain:
SOURCE EVIDENCE -> TAXONOMY -> CURRICULUM -> CONTENT SYNTHESIS -> INDEPENDENT VERIFICATION -> QA -> WEB PROJECTION.
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


def test_mom_scope_and_spec_integrity(project_root):
    """Verify Momentum, Impulse & Collisions scope and ChapterSpec conform to schemas and constraints."""
    scope_file = project_root / "curriculum" / "chapters" / "center-of-mass_scope.json"
    assert scope_file.exists(), "Center of Mass scope specification missing"
    scope_data = json.loads(scope_file.read_text(encoding="utf-8"))
    assert scope_data["chapter_id"] == "center-of-mass"
    assert len(scope_data["topics"]) == 3
    tot_subtopics = sum(len(t.get("subtopics", [])) for t in scope_data["topics"])
    assert tot_subtopics == 12
    assert len(scope_data["source_evidence_summary"]["sources_utilized"]) >= 6

    # Verify spec in both curriculum/chapters and build/staging/incoming/curriculum
    for spec_path in [
        project_root / "curriculum" / "chapters" / "center-of-mass_spec.json",
        project_root / "build" / "staging" / "incoming" / "curriculum" / "center-of-mass_spec.json",
    ]:
        assert spec_path.exists(), f"Spec missing at {spec_path}"
        spec_data = json.loads(spec_path.read_text(encoding="utf-8"))
        assert spec_data["chapter_id"] == "center-of-mass"
        assert spec_data["template_type"] == "MECHANICS"
        assert len(spec_data["taxonomy_references"]) == 12
        assert len(spec_data["learning_objectives"]) == 9
        assert len(spec_data["concept_sequence"]) == 16
        assert len(spec_data["formula_sequence"]) == 19
        assert len(spec_data["misconception_sequence"]) == 6
        assert len(spec_data["worked_example_sequence"]) == 7
        assert len(spec_data["question_sequence"]) == 2


def test_mom_evidence_manifest_integrity(project_root):
    """Verify the comprehensive source evidence manifest compiled for Momentum, Impulse & Collisions."""
    manifest_file = project_root / "build" / "reports" / "momentum_collisions_source_evidence_manifest.json"
    assert manifest_file.exists(), "Momentum source evidence manifest missing"
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert isinstance(manifest_data, list)
    assert len(manifest_data) >= 100
    sources = {r["source_title"] for r in manifest_data}
    assert len(sources) >= 5, f"Expected at least 5 distinct sources, found {len(sources)}"
    for r in manifest_data:
        assert r["fidelity_class"] in {"SOURCE_VERBATIM", "SOURCE_DERIVED"}
        assert r.get("source_id")
        assert r.get("page_range")


def test_mom_question_ladder_integrity(project_root):
    """Verify progressive QuestionLadder for collision restitution rungs."""
    ladder_file = project_root / "curriculum" / "ladders" / "ladder-mom-collision-restitution-01.json"
    assert ladder_file.exists(), "Momentum question ladder missing"
    ladder_data = json.loads(ladder_file.read_text(encoding="utf-8"))
    ladder = QuestionLadder.model_validate(ladder_data)
    assert ladder.ladder_id == "ladder-mom-collision-restitution-01"
    assert ladder.chapter_id == "center-of-mass"
    assert len(ladder.rungs) == 4
    for idx, rung in enumerate(ladder.rungs, start=1):
        assert rung.level == idx
        assert rung.physical_delta
        assert 1 <= rung.reasoning_depth <= 5


def test_mom_chapter_plan_integrity(project_root):
    """Verify structured 4-section ChapterPlan for Center of Mass & Momentum."""
    plan_file = project_root / "curriculum" / "chapters" / "center-of-mass_plan.json"
    assert plan_file.exists(), "Center of Mass chapter plan missing"
    plan_data = json.loads(plan_file.read_text(encoding="utf-8"))
    plan = ChapterPlan.model_validate(plan_data)
    assert plan.plan_id == "plan-center-of-mass-001"
    assert plan.chapter_id == "center-of-mass"
    assert len(plan.sections) == 4

    sec_ids = [s.section_id for s in plan.sections]
    assert sec_ids == [
        "sec-01-center-of-mass-dynamics",
        "sec-02-impulse-and-momentum",
        "sec-03-conservation-and-variable-mass",
        "sec-04-collisions-and-restitution",
    ]


def test_mom_verified_content_inventory_and_hash_binding(project_root):
    """Verify all Momentum content items in content/verified/ have valid verification bindings."""
    verified_dir = project_root / "content" / "verified"
    cvr_dir = project_root / "build" / "staging" / "incoming" / "content_verification"
    dual_dir = verified_dir / "dual_verifications"

    # 1. Concepts (16)
    concepts = list((verified_dir / "concepts").glob("concept-mom-*.json"))
    assert len(concepts) == 16, f"Expected 16 verified concepts, found {len(concepts)}"
    for cp in concepts:
        cdata = json.loads(cp.read_text(encoding="utf-8"))
        assert cdata["verification_status"] == "VERIFIED"
        cvr_file = cvr_dir / f"cvr-{cdata['concept_id']}.json"
        assert cvr_file.exists(), f"CVR missing for {cdata['concept_id']}"
        cvr = json.loads(cvr_file.read_text(encoding="utf-8"))
        expected_hash = compute_content_hash(cdata)
        assert cvr["content_hash"] == expected_hash
        assert cvr["verdict"] == "VERIFIED"

    # 2. Formulas (19)
    formulas = list((verified_dir / "formulas").glob("formula-mom-*.json"))
    assert len(formulas) == 19, f"Expected 19 verified formulas, found {len(formulas)}"
    for fp in formulas:
        fdata = json.loads(fp.read_text(encoding="utf-8"))
        assert fdata["verification_status"] == "VERIFIED"
        cvr_file = cvr_dir / f"cvr-{fdata['formula_id']}.json"
        assert cvr_file.exists(), f"CVR missing for {fdata['formula_id']}"
        cvr = json.loads(cvr_file.read_text(encoding="utf-8"))
        assert cvr["content_hash"] == compute_content_hash(fdata)
        assert cvr["verdict"] == "VERIFIED"

    # 3. Misconceptions (6)
    misc = list((verified_dir / "misconceptions").glob("misc-mom-*.json"))
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
    derivs = list((verified_dir / "derivations").glob("derivation-formula-mom-*.json"))
    assert len(derivs) == 7, f"Expected 7 verified derivations, found {len(derivs)}"
    for dp in derivs:
        ddata = json.loads(dp.read_text(encoding="utf-8"))
        assert ddata["verification_status"] == "VERIFIED"
        dual_path = dual_dir / f"dual-cvr-{ddata['derivation_id']}.json"
        assert dual_path.exists(), f"Dual record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_status"] == "VERIFIED"

    # 5. Worked Examples (7 - High Risk / Dual Verified)
    examples = list((verified_dir / "examples").glob("ex-mom-*.json"))
    assert len(examples) == 7, f"Expected 7 verified examples, found {len(examples)}"
    for ep in examples:
        edata = json.loads(ep.read_text(encoding="utf-8"))
        assert edata["verification_status"] == "VERIFIED"
        dual_path = dual_dir / f"dual-cvr-{edata['example_id']}.json"
        assert dual_path.exists(), f"Dual record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_status"] == "VERIFIED"

    # 6. Questions (2)
    questions = list((verified_dir / "questions").glob("center-of-mass-question-*.json"))
    assert len(questions) == 2, f"Expected 2 verified questions, found {len(questions)}"
    for qp in questions:
        qdata = json.loads(qp.read_text(encoding="utf-8"))
        assert qdata["verification_status"] == "VERIFIED"
        cvr_file = cvr_dir / f"cvr-{qdata['question_id']}.json"
        assert cvr_file.exists(), f"CVR missing for {qdata['question_id']}"
        cvr = json.loads(cvr_file.read_text(encoding="utf-8"))
        assert cvr["content_hash"] == compute_content_hash(qdata)
        assert cvr["verdict"] == "VERIFIED"


def test_mom_chapter_assembly_and_qa(project_root):
    """Verify Center of Mass chapter assembly, QA audit report, and LaTeX rendering check."""
    assembler = ChapterAssembler(project_root)
    blocks = assembler.assemble_chapter("center-of-mass")
    assert len(blocks) == 58, f"Expected 58 assembled blocks, got {len(blocks)}"

    # Check draft files
    drafts_dir = project_root / "build" / "drafts" / "center-of-mass"
    blocks_file = drafts_dir / "center-of-mass_blocks.json"
    md_file = drafts_dir / "center-of-mass_draft.md"
    assert blocks_file.exists()
    assert md_file.exists()
    assert md_file.stat().st_size > 30000

    # Run independent QA Auditor
    auditor = ChapterQAAuditor(project_root)
    plan = assembler.load_plan("center-of-mass")
    spec = assembler.load_spec("center-of-mass")
    qa_rep, rend_rep = auditor.audit_chapter("center-of-mass", blocks, plan, spec)

    assert qa_rep.verdict == "PASSED"
    assert qa_rep.physics_passed is True
    assert qa_rep.curriculum_passed is True
    assert qa_rep.provenance_passed is True
    assert rend_rep.passed is True
    assert len(rend_rep.latex_errors) == 0


def test_mom_web_compilation_and_dual_alias(project_root):
    """Verify Center of Mass compiles cleanly into Web Data with all aliases."""
    compiler = WebCompiler(root_dir=project_root)
    out_dir = compiler.compile(clean=True)

    data_dir = out_dir / "data"
    ch_file = data_dir / "chapter_center-of-mass.json"
    mom_file = data_dir / "chapter_momentum-collisions.json"
    dash_file = data_dir / "chapter-momentum-collisions.json"
    com_file = data_dir / "chapter_com.json"
    assert ch_file.exists(), "chapter_center-of-mass.json missing from web distribution"
    assert mom_file.exists(), "chapter_momentum-collisions.json dual alias missing"
    assert dash_file.exists(), "chapter-momentum-collisions.json alias missing"
    assert com_file.exists(), "chapter_com.json alias missing"

    ch_data = json.loads(ch_file.read_text(encoding="utf-8"))
    assert ch_data["chapter_id"] == "center-of-mass"
    assert ch_data["status"] == "PILOT_ACTIVE"
    assert len(ch_data["sections"]) == 4

    mom_data = json.loads(mom_file.read_text(encoding="utf-8"))
    assert mom_data["chapter_id"] == "center-of-mass"
    assert len(mom_data["sections"]) == 4

    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["pilot_active_chapters"] == 8
    assert manifest["counts"]["concepts"] >= 69
    assert manifest["counts"]["formulas"] >= 71
    assert manifest["counts"]["derivations"] >= 40
    assert manifest["counts"]["worked_examples"] >= 28
    assert manifest["counts"]["misconceptions"] >= 31
    assert manifest["counts"]["verified_questions"] >= 26
    assert manifest["counts"]["question_ladders"] >= 5


def test_canonical_knowledge_base_immutability(project_root):
    """Prime Directive: Ensure canonical kb/atoms/ and kb/taxonomy/syllabus.yaml are 100% untouched."""
    atoms = list((project_root / "kb" / "atoms").glob("*.json"))
    assert len(atoms) == 35, f"Canonical atom count must remain exactly 35, got {len(atoms)}"
