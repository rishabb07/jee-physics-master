import inspect
import json
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from jee_physics.atomization.eval_harness import evaluate_staged_extraction
from jee_physics.atomization.extractor import (
    build_staged_question_atom,
    build_staged_theory_atom,
)
from jee_physics.atomization.runner import stage_atom_batch, stage_candidate_file
from jee_physics.atomization.validator import validate_staged_atom_batch
from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference
from jee_physics.models.enums import AtomStatus, AtomType, DifficultyLevel, ReviewIssueType
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.models.source import SourceRegistryRecord
from jee_physics.storage.io import read_json, safe_write_json, safe_write_jsonl


def test_staged_atom_validates_successfully():
    atom = build_staged_question_atom(
        chapter_id="mechanics",
        topic_id="kinematics",
        statement="A ball is thrown vertically upward with speed $u$. Find max height.",
        options=[
            {"id": "A", "text": "$\\frac{u^2}{2g}$"},
            {"id": "B", "text": "$\\frac{u^2}{g}$"},
        ],
        answer="A",
        difficulty=DifficultyLevel.L1,
        source_id="src-test-01",
        file_name="test_book.pdf",
        page_number=10,
        source_locator="Chapter 2, Q1",
        confidence=0.98,
    )
    assert atom.atom_id.startswith("mechanics-question-")
    assert atom.verification_status == AtomStatus.STAGED
    assert atom.question is not None
    assert atom.question.options[0].text == "$\\frac{u^2}{2g}$"


def test_missing_provenance_rejected():
    with pytest.raises(ValidationError):
        KnowledgeAtom(
            atom_id="test-atom-no-prov",
            atom_type=AtomType.THEORY,
            title="Orphan Atom",
            taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="1d-motion"),
            provenance=[],  # Min length 1 required
            confidence=1.0,
            content_hash="a" * 64,
            content="Some theory.",
        )


def test_impossible_page_range_rejected():
    with pytest.raises(ValidationError):
        ProvenanceRecord(
            source_id="src-01",
            file_name="test.pdf",
            page_start=15,
            page_end=10,  # page_start > page_end
        )


def test_question_missing_required_content_rejected():
    with pytest.raises(ValidationError):
        KnowledgeAtom(
            atom_id="test-q-empty",
            atom_type=AtomType.QUESTION,
            title="Empty Question",
            taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="1d-motion"),
            provenance=[
                ProvenanceRecord(source_id="src-01", file_name="test.pdf", page_start=1, page_end=1)
            ],
            confidence=1.0,
            content_hash="b" * 64,
            # Missing question payload
        )


def test_batch_validation_detects_duplicates_and_latex_errors():
    atom1 = build_staged_question_atom(
        chapter_id="mechanics",
        topic_id="kinematics",
        statement="A stone is dropped from tower of height $h$. Find speed $v = \\sqrt{2gh}$.",
        options=[{"id": "A", "text": "$v$"}],
        answer="A",
        difficulty=DifficultyLevel.L1,
        source_id="src-dummy",
        file_name="dummy.pdf",
        page_number=1,
        source_locator="Q1",
    )
    # atom2 has malformed LaTeX with unbalanced curly brace
    atom2 = build_staged_question_atom(
        chapter_id="mechanics",
        topic_id="kinematics",
        statement="Acceleration is $\\frac{v^2{r}$ in circular motion.",
        options=[{"id": "A", "text": "$a$"}],
        answer="A",
        difficulty=DifficultyLevel.L1,
        source_id="src-dummy",
        file_name="dummy.pdf",
        page_number=2,
        source_locator="Q2",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        reg_dir = Path(tmpdir) / "sources" / "registry"
        reg_dir.mkdir(parents=True)
        rec = SourceRegistryRecord(
            source_id="src-dummy",
            file_name="dummy.pdf",
            file_size_bytes=100,
            sha256="c" * 64,
        )
        safe_write_json(reg_dir / "src-dummy.json", rec)

        val_res = validate_staged_atom_batch([atom1, atom2], registry_dir=reg_dir)
        assert len(val_res.valid_atoms) == 1
        assert len(val_res.invalid_atoms) == 1
        assert "unbalanced curly braces" in val_res.invalid_atoms[0][1][0]


def test_low_confidence_produces_review_queue_item():
    atom_low = build_staged_question_atom(
        chapter_id="mechanics",
        topic_id="kinematics",
        statement="Ambiguous handwritten question: Find speed $v$.",
        options=[{"id": "A", "text": "$10\\text{ m/s}$"}],
        answer="A",
        difficulty=DifficultyLevel.L2,
        source_id="src-handwritten",
        file_name="notes.pdf",
        page_number=5,
        source_locator="Page 5 Note",
        confidence=0.72,  # Low confidence (< 0.85)
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        reg_dir = Path(tmpdir) / "sources" / "registry"
        reg_dir.mkdir(parents=True)
        rec = SourceRegistryRecord(
            source_id="src-handwritten",
            file_name="notes.pdf",
            file_size_bytes=100,
            sha256="d" * 64,
        )
        safe_write_json(reg_dir / "src-handwritten.json", rec)

        val_res = validate_staged_atom_batch([atom_low], registry_dir=reg_dir)
        assert len(val_res.valid_atoms) == 1
        assert len(val_res.review_items) == 1
        assert val_res.review_items[0].issue_type == ReviewIssueType.LOW_CONFIDENCE
        assert val_res.review_items[0].atom_id == atom_low.atom_id


def test_stage_atom_batch_runner_leaves_kb_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        reg_dir = root / "sources" / "registry"
        kb_atoms = root / "kb" / "atoms"
        reg_dir.mkdir(parents=True)
        kb_atoms.mkdir(parents=True)

        rec = SourceRegistryRecord(
            source_id="src-mock",
            file_name="mock.pdf",
            file_size_bytes=500,
            sha256="e" * 64,
        )
        safe_write_json(reg_dir / "src-mock.json", rec)

        atom = build_staged_theory_atom(
            chapter_id="optics",
            topic_id="reflection",
            title="Law of Reflection",
            content="Angle of incidence equals angle of reflection ($i = r$).",
            source_id="src-mock",
            file_name="mock.pdf",
            page_number=1,
            source_locator="Section A",
        )

        rep = stage_atom_batch([atom], "src-mock", pages_processed=[1], project_root=root)

        # 1. Output exists in build/staging/atoms/
        staged_file = root / rep.staged_atoms_file
        assert staged_file.exists()

        # 2. Manifest exists in build/staging/manifests/
        manifest_file = root / rep.manifest_file
        assert manifest_file.exists()
        manifest_data = read_json(manifest_file)
        assert manifest_data["generated_atom_ids"] == [atom.atom_id]

        # 3. CRITICAL INVARIANT: kb/atoms/ is 100% empty!
        kb_files = list(kb_atoms.rglob("*.jsonl"))
        assert len(kb_files) == 0


def test_eval_harness():
    atom = build_staged_question_atom(
        chapter_id="optics",
        topic_id="refraction",
        statement="Snell's Law: $n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2$.",
        options=[{"id": "A", "text": "$\\theta_1$"}],
        answer="A",
        difficulty=DifficultyLevel.L1,
        source_id="src-01",
        file_name="book.pdf",
        page_number=1,
        source_locator="Q1",
    )

    # Eval covering page 1 passes
    res = evaluate_staged_extraction([atom], page_start=1, page_end=1, expected_question_range=(1, 2))
    assert res.passed is True

    # Eval expecting pages 1 to 3 detects gap on page 2 and 3
    res_gap = evaluate_staged_extraction([atom], page_start=1, page_end=3)
    assert res_gap.passed is False
    assert any("page 2 has no extracted atoms" in f for f in res_gap.failures)


# =========================================================================
# Phase 3 Real Operational Boundary Tests
# =========================================================================

def test_stage_candidate_file_arbitrary_source():
    """Proves stage_candidate_file works on any arbitrary registered source."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        reg_dir = root / "sources" / "registry"
        incoming_dir = root / "build" / "staging" / "incoming"
        reg_dir.mkdir(parents=True)
        incoming_dir.mkdir(parents=True)

        source_id = "src-arbitrary-hcv-mechanics-1234"
        file_name = "concepts_of_physics_vol1.pdf"

        # Register arbitrary source
        rec = SourceRegistryRecord(
            source_id=source_id,
            file_name=file_name,
            total_pages=50,
            file_size_bytes=10240,
            sha256="f" * 64,
        )
        safe_write_json(reg_dir / f"{source_id}.json", rec)

        # Build candidate atom
        atom = build_staged_question_atom(
            chapter_id="mechanics",
            topic_id="newtons-laws",
            statement="A block of mass $m$ rests on a smooth horizontal table. A horizontal force $F$ is applied. Find acceleration $a = \\frac{F}{m}$.",
            options=[{"id": "A", "text": "$\\frac{F}{m}$"}],
            answer="A",
            difficulty=DifficultyLevel.L1,
            source_id=source_id,
            file_name=file_name,
            page_number=24,
            source_locator="Exercise 1, Problem 5",
        )

        candidate_file = incoming_dir / "candidate_test.jsonl"
        candidate_file.write_text(json.dumps(atom.model_dump(mode="json")) + "\n", encoding="utf-8")

        # Stage via stage_candidate_file
        report = stage_candidate_file(source_id, candidate_file, project_root=root)
        assert report.total_atoms_staged == 1
        assert report.validation_failures == 0
        assert report.pages_processed == [24]
        assert Path(root / report.staged_atoms_file).exists()


def test_stage_candidate_unknown_source_rejected():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        incoming_dir = root / "build" / "staging" / "incoming"
        incoming_dir.mkdir(parents=True)

        candidate_file = incoming_dir / "candidate.jsonl"
        candidate_file.write_text('{"atom_id": "test"}\n', encoding="utf-8")

        with pytest.raises(FileNotFoundError, match="not found in registry"):
            stage_candidate_file("src-nonexistent-9999", candidate_file, project_root=root)


def test_stage_candidate_mismatched_filename_rejected():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        reg_dir = root / "sources" / "registry"
        incoming_dir = root / "build" / "staging" / "incoming"
        reg_dir.mkdir(parents=True)
        incoming_dir.mkdir(parents=True)

        source_id = "src-source-a"
        rec = SourceRegistryRecord(
            source_id=source_id,
            file_name="real_book.pdf",
            total_pages=10,
            file_size_bytes=1000,
            sha256="1" * 64,
        )
        safe_write_json(reg_dir / f"{source_id}.json", rec)

        # Candidate claims file_name "different_book.pdf"
        atom = build_staged_theory_atom(
            chapter_id="optics",
            topic_id="reflection",
            title="Reflection",
            content="Reflection theory.",
            source_id=source_id,
            file_name="different_book.pdf",  # Mismatched file_name
            page_number=1,
            source_locator="p1",
        )

        candidate_file = incoming_dir / "candidate.jsonl"
        candidate_file.write_text(json.dumps(atom.model_dump(mode="json")) + "\n", encoding="utf-8")

        report = stage_candidate_file(source_id, candidate_file, project_root=root)
        assert report.total_atoms_staged == 0
        assert report.validation_failures == 1
        assert any("does not match registered source file_name" in w for w in report.warnings)


def test_stage_candidate_out_of_range_page_rejected():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        reg_dir = root / "sources" / "registry"
        incoming_dir = root / "build" / "staging" / "incoming"
        reg_dir.mkdir(parents=True)
        incoming_dir.mkdir(parents=True)

        source_id = "src-short-paper"
        rec = SourceRegistryRecord(
            source_id=source_id,
            file_name="short_paper.pdf",
            total_pages=5,  # Only 5 pages
            file_size_bytes=1000,
            sha256="2" * 64,
        )
        safe_write_json(reg_dir / f"{source_id}.json", rec)

        # Candidate references page 20
        atom = build_staged_theory_atom(
            chapter_id="optics",
            topic_id="reflection",
            title="Reflection",
            content="Reflection theory.",
            source_id=source_id,
            file_name="short_paper.pdf",
            page_number=20,  # Out of bounds (> 5)
            source_locator="p20",
        )

        candidate_file = incoming_dir / "candidate.jsonl"
        candidate_file.write_text(json.dumps(atom.model_dump(mode="json")) + "\n", encoding="utf-8")

        report = stage_candidate_file(source_id, candidate_file, project_root=root)
        assert report.total_atoms_staged == 0
        assert report.validation_failures == 1
        assert any("outside source page bounds" in w for w in report.warnings)


def test_candidate_claiming_verified_is_forced_to_staged():
    """Anti-Self-Promotion: Candidate claiming VERIFIED is forced back to STAGED."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        reg_dir = root / "sources" / "registry"
        incoming_dir = root / "build" / "staging" / "incoming"
        reg_dir.mkdir(parents=True)
        incoming_dir.mkdir(parents=True)

        source_id = "src-test-source"
        rec = SourceRegistryRecord(
            source_id=source_id,
            file_name="test.pdf",
            total_pages=10,
            file_size_bytes=1000,
            sha256="3" * 64,
        )
        safe_write_json(reg_dir / f"{source_id}.json", rec)

        atom = build_staged_theory_atom(
            chapter_id="optics",
            topic_id="reflection",
            title="Reflection",
            content="Reflection theory.",
            source_id=source_id,
            file_name="test.pdf",
            page_number=1,
            source_locator="p1",
        )
        atom_dict = atom.model_dump(mode="json")
        atom_dict["verification_status"] = "VERIFIED"  # Malicious/mistaken self-promotion

        candidate_file = incoming_dir / "candidate.jsonl"
        candidate_file.write_text(json.dumps(atom_dict) + "\n", encoding="utf-8")

        report = stage_candidate_file(source_id, candidate_file, project_root=root)
        assert report.total_atoms_staged == 1
        assert report.validation_failures == 0
        assert any("claimed verification_status 'VERIFIED'; overridden to 'STAGED'" in w for w in report.warnings)

        # Inspect the staged atom on disk: must be STAGED
        staged_atoms = Path(root / report.staged_atoms_file).read_text(encoding="utf-8").splitlines()
        staged_dict = json.loads(staged_atoms[0])
        assert staged_dict["verification_status"] == "STAGED"


def test_stage_candidate_invalid_json_rejected_cleanly():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        reg_dir = root / "sources" / "registry"
        incoming_dir = root / "build" / "staging" / "incoming"
        reg_dir.mkdir(parents=True)
        incoming_dir.mkdir(parents=True)

        rec = SourceRegistryRecord(
            source_id="src-any",
            file_name="any.pdf",
            total_pages=5,
            file_size_bytes=100,
            sha256="0" * 64,
        )
        safe_write_json(reg_dir / "src-any.json", rec)

        candidate_file = incoming_dir / "candidate.jsonl"
        candidate_file.write_text("NOT_VALID_JSON\n", encoding="utf-8")

        with pytest.raises(ValueError, match="Malformed JSON at line 1"):
            stage_candidate_file("src-any", candidate_file, project_root=root)


def test_production_code_has_no_source_specific_branches():
    """Verifies that production code contains zero hard-coded source branches like 'booster-03'."""
    import jee_physics.cli as cli_mod
    cli_source = inspect.getsource(cli_mod)
    assert "booster-03" not in cli_source
    assert "booster_-03" not in cli_source


def test_extract_pilot_not_imported_by_production_code():
    """Verifies extract_pilot is not imported anywhere by jee_physics."""
    import jee_physics
    import jee_physics.atomization
    import jee_physics.cli
    import sys
    for mod_name in sys.modules:
        if mod_name.startswith("jee_physics."):
            assert "extract_pilot" not in mod_name


def test_security_filename_spoofing_prevented():
    """Security / Integrity Test (Requirement 13):
    Take a different source file, give it a filename containing 'booster-03',
    and attempt to stage candidate atoms derived from the mock test paper.
    The system MUST reject them because provenance does not match the registered source.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        reg_dir = root / "sources" / "registry"
        incoming_dir = root / "build" / "staging" / "incoming"
        reg_dir.mkdir(parents=True)
        incoming_dir.mkdir(parents=True)

        # Attacker registers unrelated notes with 'booster-03' in the filename
        spoofed_source_id = "src-unrelated-notes-booster-03-9999"
        spoofed_file_name = "unrelated_notes_booster-03.pdf"
        rec = SourceRegistryRecord(
            source_id=spoofed_source_id,
            file_name=spoofed_file_name,
            total_pages=2,  # Only 2 pages
            file_size_bytes=5000,
            sha256="9" * 64,
        )
        safe_write_json(reg_dir / f"{spoofed_source_id}.json", rec)

        # Attacker attempts to stage atoms that claim the real mock test file name and page 4
        spoofed_atom = build_staged_question_atom(
            chapter_id="optics",
            topic_id="ray-optics",
            statement="Prism TIR question from another paper.",
            options=[{"id": "1", "text": "$\\sin\\theta \\ge 8/9$"}],
            answer="1",
            difficulty=DifficultyLevel.L2,
            source_id=spoofed_source_id,
            file_name="jee_rank_booster-03_mock_paper.pdf",  # Mismatched file_name
            page_number=4,  # Out of bounds for the 2-page source
            source_locator="Section A, Q1",
        )

        candidate_file = incoming_dir / "spoofed_candidate.jsonl"
        candidate_file.write_text(json.dumps(spoofed_atom.model_dump(mode="json")) + "\n", encoding="utf-8")

        # Attempt to stage: must be rejected!
        report = stage_candidate_file(spoofed_source_id, candidate_file, project_root=root)
        assert report.total_atoms_staged == 0
        assert report.validation_failures == 1
        # Provenance errors captured:
        assert any("does not match registered source file_name" in w for w in report.warnings)
        assert any("outside source page bounds" in w for w in report.warnings)
