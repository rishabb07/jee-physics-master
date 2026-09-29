"""
Comprehensive Test Suite for Phase 10 Web Application.
Tests cover:
1. WebDataBuilder schema and count verification
2. Strict verification boundary (zero leakage of review queue/unverified items)
3. Referential integrity across chapters, formulas, and questions
4. KaTeX offline assets completeness (all woff2 fonts bundled)
5. Search index tokenization and query retrieval
6. Syllabus and prerequisite graph modeling
7. Mandatory End-to-End Mutation Test proving reactive auto-updating
"""

import json
import pytest
import shutil
from pathlib import Path

from jee_physics.web.builder import WebDataBuilder
from jee_physics.web.compiler import WebCompiler
from jee_physics.web.models import WebBuildManifest


@pytest.fixture
def project_root():
    return Path.cwd()


@pytest.fixture
def compiler(project_root):
    return WebCompiler(root_dir=project_root)


@pytest.fixture
def builder(project_root):
    return WebDataBuilder(root_dir=project_root)


def test_web_builder_manifest_and_counts(builder, project_root):
    """Verify WebDataBuilder produces a valid manifest with exact pilot counts."""
    target_dir = project_root / "build" / "web" / "data"
    manifest = builder.build_all(target_dir=target_dir)

    assert isinstance(manifest, WebBuildManifest)
    assert manifest.scope == "PILOT"
    assert manifest.counts["total_chapters"] == 30
    assert manifest.counts["total_chapters"] == 30
    assert manifest.counts["pilot_active_chapters"] == 5
    assert manifest.counts["concepts"] == 20
    assert manifest.counts["formulas"] == 25
    assert manifest.counts["derivations"] == 19
    assert manifest.counts["worked_examples"] == 9
    assert manifest.counts["misconceptions"] == 13
    assert manifest.counts["verified_questions"] == 19
    assert manifest.counts["question_ladders"] == 2
    assert manifest.counts["search_index_entries"] > 80

    # Verify manifest file on disk
    manifest_file = target_dir / "manifest.json"
    assert manifest_file.exists()
    disk_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert disk_data["scope"] == "PILOT"
    assert len(disk_data["chapters"]) == 30


def test_verification_boundary_zero_leakage(builder, project_root):
    """Assert with zero tolerance that review queue items or unverified questions never enter questions.json."""
    target_dir = project_root / "build" / "web" / "data"
    builder.build_all(target_dir=target_dir)

    questions_file = target_dir / "questions.json"
    assert questions_file.exists()
    questions = json.loads(questions_file.read_text(encoding="utf-8"))

    qids = [q["question_id"] for q in questions]

    # Explicitly check forbidden review queue IDs
    forbidden = {
        "gen-q-ambig-test-01",
        "gen-q-dist-conflict-01",
        "gen-q-wrong-ans-01",
    }
    leaks = [fid for fid in forbidden if fid in qids]
    assert len(leaks) == 0, f"CRITICAL LEAK DETECTED: Review queue items in production questions: {leaks}"

    # Verify 100% of questions are certified VERIFIED
    for q in questions:
        assert q["verification_status"] == "VERIFIED", f"Unverified question in production: {q['question_id']}"
        assert len(q["problem_statement"]) > 10, f"Malformed statement in question {q['question_id']}"
        assert q["correct_answer"], f"Missing correct answer in question {q['question_id']}"


def test_referential_integrity(builder, project_root):
    """Verify that all formulas, questions, and concepts referenced in chapters exist."""
    target_dir = project_root / "build" / "web" / "data"
    builder.build_all(target_dir=target_dir)

    formulas = {f["formula_id"] for f in json.loads((target_dir / "formulas.json").read_text(encoding="utf-8"))}
    questions = {q["question_id"] for q in json.loads((target_dir / "questions.json").read_text(encoding="utf-8"))}

    pilot_chapters = ["rotational-motion", "thermodynamics", "current-electricity", "ray-optics", "kinematics"]
    for ch_id in pilot_chapters:
        ch_file = target_dir / f"chapter_{ch_id}.json"
        assert ch_file.exists(), f"Chapter detail missing: {ch_id}"
        ch_data = json.loads(ch_file.read_text(encoding="utf-8"))

        for sec in ch_data["sections"]:
            for f in sec["formulas"]:
                assert f["formula_id"] in formulas, f"Referenced formula {f['formula_id']} not in formulas.json"
            for q in sec["questions"]:
                assert q["question_id"] in questions, f"Referenced question {q['question_id']} not in questions.json"


def test_katex_offline_assets(compiler, project_root):
    """Verify KaTeX vendor assets and offline fonts exist locally."""
    out_dir = compiler.compile(clean=True)

    vendor_katex = out_dir / "vendor" / "katex"
    assert (vendor_katex / "katex.min.js").exists(), "KaTeX JS missing"
    assert (vendor_katex / "katex.min.css").exists(), "KaTeX CSS missing"
    assert (vendor_katex / "auto-render.min.js").exists(), "Auto-render JS missing"

    fonts_dir = vendor_katex / "fonts"
    assert fonts_dir.exists(), "Fonts directory missing"
    woff2_fonts = list(fonts_dir.glob("*.woff2"))
    assert len(woff2_fonts) >= 15, f"Expected KaTeX woff2 fonts, found {len(woff2_fonts)}"


def test_search_index_retrieval(builder, project_root):
    """Verify search index contains entries across all entity types and supports token matching."""
    target_dir = project_root / "build" / "web" / "data"
    builder.build_all(target_dir=target_dir)

    index_file = target_dir / "search_index.json"
    assert index_file.exists()
    items = json.loads(index_file.read_text(encoding="utf-8"))

    entity_types = {item["entity_type"] for item in items}
    expected_types = {"chapter", "concept", "formula", "example", "misconception", "question"}
    assert expected_types.issubset(entity_types), f"Missing entity types in search index: {expected_types - entity_types}"

    # Test token search logic
    torque_items = [item for item in items if "torque" in item["keywords"] or "torque" in item["title"].lower()]
    assert len(torque_items) > 0, "Failed to find search entries for 'torque'"


def test_taxonomy_30_chapters_and_prerequisites(builder, project_root):
    """Verify taxonomy covers all 30 chapters and prerequisites graph is structured."""
    target_dir = project_root / "build" / "web" / "data"
    builder.build_all(target_dir=target_dir)

    taxonomy = json.loads((target_dir / "taxonomy.json").read_text(encoding="utf-8"))
    assert len(taxonomy["chapters"]) == 30
    assert len(taxonomy["branches"]) >= 5

    pilot_active = [ch for ch in taxonomy["chapters"] if ch["status"] == "PILOT_ACTIVE"]
    pending = [ch for ch in taxonomy["chapters"] if ch["status"] == "PENDING"]
    assert len(pilot_active) == 5
    assert len(pending) == 25

    prereqs = json.loads((target_dir / "prerequisites.json").read_text(encoding="utf-8"))
    assert "edges" in prereqs
    assert len(prereqs["edges"]) > 0


def test_end_to_end_mutation_updates_web_output(compiler, project_root):
    """
    Mandatory End-to-End Mutation Test:
    Proves that adding/modifying an upstream knowledge element propagates deterministically
    to the web distribution upon recompilation, and deleting it purges it completely.
    """
    # 1. Base compile
    out_dir = compiler.compile(clean=True)
    formulas_file = out_dir / "data" / "formulas.json"
    base_formulas = json.loads(formulas_file.read_text(encoding="utf-8"))
    base_count = len(base_formulas)

    # 2. Introduce a temporary upstream formula in incoming staging
    test_formula_id = "formula-mutation-test-omega-01"
    temp_formula_path = project_root / "build" / "staging" / "incoming" / "content" / "formulas" / f"{test_formula_id}.json"
    temp_formula_data = {
        "formula_id": test_formula_id,
        "chapter_id": "rotational-motion",
        "title": "Mutation Test Angular Frequency",
        "equation_latex": "\\omega = 2\\pi f",
        "variables": {"\\omega": "Angular frequency", "f": "Frequency"},
        "units": {"\\omega": "rad/s", "f": "Hz"},
        "dimensions": {"\\omega": "[T]^-1", "f": "[T]^-1"},
        "assumptions": ["Periodic motion"],
        "validity_conditions": ["Universal kinematic definition"],
        "common_misuse": ["Confusing frequency with angular frequency"],
        "derivation_reference": None,
        "related_concepts": [],
        "verification_status": "VERIFIED",
    }

    try:
        temp_formula_path.write_text(json.dumps(temp_formula_data, indent=2), encoding="utf-8")

        # 3. Recompile
        compiler.compile()

        # Verify mutation was picked up in distribution
        mutated_formulas = json.loads(formulas_file.read_text(encoding="utf-8"))
        mutated_ids = [f["formula_id"] for f in mutated_formulas]
        assert test_formula_id in mutated_ids, "Mutation test formula not found in compiled output/web/data/formulas.json"
        assert len(mutated_formulas) == base_count + 1

    finally:
        # 4. Clean up temporary test formula
        if temp_formula_path.exists():
            temp_formula_path.unlink()

        # 5. Recompile to verify zero stale retention
        compiler.compile()
        restored_formulas = json.loads(formulas_file.read_text(encoding="utf-8"))
        restored_ids = [f["formula_id"] for f in restored_formulas]
        assert test_formula_id not in restored_ids, "Deleted mutation formula was retained in output/web/data/formulas.json"
        assert len(restored_formulas) == base_count
