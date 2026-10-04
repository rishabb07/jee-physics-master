"""
Comprehensive Test Suite for Phase 13: Newton's Laws / Dynamics Chapter.
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


def test_dynamics_scope_and_spec_integrity(project_root):
    """Verify Dynamics scope, ChapterSpec conform to schemas and constraints."""
    scope_file = project_root / "curriculum" / "chapters" / "dynamics_scope.json"
    assert scope_file.exists(), "Dynamics scope specification missing"
    scope_data = json.loads(scope_file.read_text(encoding="utf-8"))
    assert scope_data["chapter_id"] == "laws-of-motion"
    assert len(scope_data["topics"]) == 3
    tot_subtopics = sum(len(t.get("subtopics", [])) for t in scope_data["topics"])
    assert tot_subtopics == 17
    assert len(scope_data["source_grounding_summary"]["primary_sources"]) >= 6

    # Verify spec in both curriculum/chapters and build/staging/incoming/curriculum
    for spec_path in [
        project_root / "curriculum" / "chapters" / "laws-of-motion_spec.json",
        project_root / "curriculum" / "chapters" / "dynamics_spec.json",
    ]:
        assert spec_path.exists(), f"Spec missing at {spec_path}"
        spec_data = json.loads(spec_path.read_text(encoding="utf-8"))
        spec = ChapterSpec.model_validate(spec_data)
        assert spec.chapter_id == "laws-of-motion"
        assert spec.template_type.value == "MECHANICS"
        assert len(spec.taxonomy_references) == 17
        assert len(spec.learning_objectives) == 8
        assert len(spec.concept_sequence) == 16
        assert len(spec.formula_sequence) == 14
        assert len(spec.misconception_sequence) == 6
        assert len(spec.worked_example_sequence) == 6
        assert len(spec.question_sequence) == 2


def test_dynamics_evidence_manifest_integrity(project_root):
    """Verify the comprehensive source evidence manifest compiled for dynamics."""
    manifest_file = project_root / "build" / "reports" / "dynamics_source_evidence_manifest.json"
    assert manifest_file.exists(), "Dynamics source evidence manifest missing"
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert manifest_data["chapter_id"] == "laws-of-motion"
    assert manifest_data["total_evidence_records"] >= 100
    assert len(manifest_data["records"]) == manifest_data["total_evidence_records"]
    sources = {r["source_title"] for r in manifest_data["records"]}
    assert len(sources) >= 5, f"Expected at least 5 distinct sources, found {len(sources)}"


def test_dynamics_question_ladder_integrity(project_root):
    """Verify progressive QuestionLadder for dry friction and multi-body stacks."""
    ladder_file = project_root / "curriculum" / "ladders" / "ladder-dyn-friction-two-block-01.json"
    assert ladder_file.exists(), "Dynamics question ladder missing"
    ladder_data = json.loads(ladder_file.read_text(encoding="utf-8"))
    ladder = QuestionLadder.model_validate(ladder_data)
    assert ladder.ladder_id == "ladder-dyn-friction-two-block-01"
    assert ladder.chapter_id == "laws-of-motion"
    assert len(ladder.rungs) == 4
    for idx, rung in enumerate(ladder.rungs, start=1):
        assert rung.level == idx
        assert rung.physical_delta
        assert 1 <= rung.reasoning_depth <= 5


def test_dynamics_chapter_plan_integrity(project_root):
    """Verify structured 4-section ChapterPlan for Laws of Motion & Dynamics."""
    plan_file = project_root / "curriculum" / "chapters" / "laws-of-motion_plan.json"
    assert plan_file.exists(), "Laws of Motion chapter plan missing"
    plan_data = json.loads(plan_file.read_text(encoding="utf-8"))
    plan = ChapterPlan.model_validate(plan_data)
    assert plan.plan_id == "plan-dynamics-001"
    assert plan.chapter_id == "laws-of-motion"
    assert len(plan.sections) == 4

    sec_ids = [s.section_id for s in plan.sections]
    assert sec_ids == [
        "sec-01-newtons-laws-and-equilibrium",
        "sec-02-constraints-and-accelerating-frames",
        "sec-03-frictional-dynamics",
        "sec-04-circular-dynamics",
    ]


def test_dynamics_verified_content_inventory_and_hash_binding(project_root):
    """Verify all 49 Dynamics content items in content/verified/ have valid verification bindings."""
    verified_dir = project_root / "content" / "verified"

    # 1. Concepts (16)
    concepts = list((verified_dir / "concepts").glob("concept-dyn-*.json"))
    assert len(concepts) == 16, f"Expected 16 verified dynamics concepts, found {len(concepts)}"
    for cp in concepts:
        cdata = json.loads(cp.read_text(encoding="utf-8"))
        assert cdata["verification_status"] == "VERIFIED"
        assert cdata["verification_record_id"].startswith("cvr-")
        # Validate hash immutability
        expected_hash = compute_content_hash(cdata)
        assert cdata["content_hash"] == expected_hash

    # 2. Formulas (14)
    formulas = list((verified_dir / "formulas").glob("formula-dyn-*.json"))
    assert len(formulas) == 14, f"Expected 14 verified dynamics formulas, found {len(formulas)}"
    for fp in formulas:
        fdata = json.loads(fp.read_text(encoding="utf-8"))
        assert fdata["verification_status"] == "VERIFIED"
        assert fdata["verification_record_id"].startswith("cvr-")
        assert fdata["content_hash"] == compute_content_hash(fdata)

    # 3. Misconceptions (6)
    misc = list((verified_dir / "misconceptions").glob("misc-dyn-*.json"))
    assert len(misc) == 6, f"Expected 6 verified dynamics misconceptions, found {len(misc)}"
    for mp in misc:
        mdata = json.loads(mp.read_text(encoding="utf-8"))
        assert mdata["verification_status"] == "VERIFIED"
        assert mdata["verification_record_id"].startswith("cvr-")
        assert mdata["content_hash"] == compute_content_hash(mdata)

    # 4. Derivations (7 - High Risk / Dual Verified)
    derivs = list((verified_dir / "derivations").glob("derivation-formula-dyn-*.json"))
    assert len(derivs) == 7, f"Expected 7 verified dynamics derivations, found {len(derivs)}"
    for dp in derivs:
        ddata = json.loads(dp.read_text(encoding="utf-8"))
        assert ddata["verification_status"] == "VERIFIED"
        assert ddata["verification_record_id"].startswith("dual-cvr-")
        assert ddata["content_hash"] == compute_content_hash(ddata)
        dual_path = verified_dir / "dual_verifications" / f"{ddata['verification_record_id']}.json"
        assert dual_path.exists(), f"Dual record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_verdict"] == "VERIFIED"

    # 5. Worked Examples (6 - High Risk / Dual Verified)
    examples = list((verified_dir / "examples").glob("ex-dyn-*.json"))
    assert len(examples) == 6, f"Expected 6 verified dynamics examples, found {len(examples)}"
    for ep in examples:
        edata = json.loads(ep.read_text(encoding="utf-8"))
        assert edata["verification_status"] == "VERIFIED"
        assert edata["verification_record_id"].startswith("dual-cvr-")
        assert edata["content_hash"] == compute_content_hash(edata)
        dual_path = verified_dir / "dual_verifications" / f"{edata['verification_record_id']}.json"
        assert dual_path.exists(), f"Dual record missing: {dual_path}"
        dual_data = json.loads(dual_path.read_text(encoding="utf-8"))
        assert dual_data["agreement"] is True
        assert dual_data["final_verdict"] == "VERIFIED"


def test_dynamics_chapter_assembly_and_qa(project_root):
    """Verify Dynamics chapter assembly, QA audit report, and LaTeX rendering check."""
    assembler = ChapterAssembler(project_root)
    blocks = assembler.assemble_chapter("laws-of-motion")
    assert len(blocks) == 56, f"Expected 56 assembled blocks, got {len(blocks)}"

    # Check draft files
    drafts_dir = project_root / "build" / "drafts" / "laws-of-motion"
    blocks_file = drafts_dir / "laws-of-motion_blocks.json"
    md_file = drafts_dir / "laws-of-motion_draft.md"
    assert blocks_file.exists()
    assert md_file.exists()
    assert md_file.stat().st_size > 40000

    # Run independent QA Auditor
    auditor = ChapterQAAuditor(project_root)
    plan = assembler.load_plan("laws-of-motion")
    spec = assembler.load_spec("laws-of-motion")
    qa_rep, rend_rep = auditor.audit_chapter("laws-of-motion", blocks, plan, spec)

    assert qa_rep.verdict == "PASSED"
    assert qa_rep.physics_passed is True
    assert qa_rep.curriculum_passed is True
    assert qa_rep.provenance_passed is True
    assert rend_rep.passed is True
    assert len(rend_rep.latex_errors) == 0


def test_dynamics_web_compilation_and_dual_alias(project_root):
    """Verify Dynamics compiles cleanly into Web Data with dual alias chapter_dynamics.json."""
    compiler = WebCompiler(root_dir=project_root)
    out_dir = compiler.compile(clean=True)

    data_dir = out_dir / "data"
    ch_file = data_dir / "chapter_laws-of-motion.json"
    dyn_file = data_dir / "chapter_dynamics.json"
    assert ch_file.exists(), "chapter_laws-of-motion.json missing from web distribution"
    assert dyn_file.exists(), "chapter_dynamics.json dual alias missing from web distribution"

    ch_data = json.loads(ch_file.read_text(encoding="utf-8"))
    assert ch_data["chapter_id"] == "laws-of-motion"
    assert ch_data["status"] == "PILOT_ACTIVE"
    assert len(ch_data["sections"]) == 4

    dyn_data = json.loads(dyn_file.read_text(encoding="utf-8"))
    assert dyn_data["chapter_id"] == "laws-of-motion"
    assert len(dyn_data["sections"]) == 4

    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"]["pilot_active_chapters"] >= 6
    assert manifest["counts"]["concepts"] >= 36
    assert manifest["counts"]["formulas"] >= 39
    assert manifest["counts"]["derivations"] >= 26
    assert manifest["counts"]["worked_examples"] >= 15
    assert manifest["counts"]["misconceptions"] >= 19
    assert manifest["counts"]["verified_questions"] >= 21
    assert manifest["counts"]["question_ladders"] >= 3


def test_canonical_knowledge_base_immutability(project_root):
    """Prime Directive: Ensure canonical kb/atoms/ and kb/taxonomy/syllabus.yaml are 100% untouched."""
    atoms = list((project_root / "kb" / "atoms").glob("*.json"))
    assert len(atoms) == 35, f"Canonical atom count must remain exactly 35, got {len(atoms)}"

    # Check laws of motion atoms are canonical questions
    lom_atoms = list((project_root / "kb" / "atoms").glob("*laws-of-motion*"))
    assert len(lom_atoms) == 2
    for a in lom_atoms:
        adata = json.loads(a.read_text(encoding="utf-8"))
        assert adata["atom_type"] == "question"
        assert adata["verification_status"] == "VERIFIED"
