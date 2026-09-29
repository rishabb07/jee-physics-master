"""
Tests for Production Release Gates.
Verifies that blocking release conditions strictly raise AssertionError and prevent distribution.
"""

import json
import pytest
from pathlib import Path
import shutil

from jee_physics.web.compiler import WebCompiler


@pytest.fixture
def compiler():
    return WebCompiler()


def test_clean_distribution_passes_validation(compiler):
    out_dir = compiler.compile(clean=True)
    assert (out_dir / "data" / "manifest.json").exists()


import hashlib

def _update_manifest_hash(dist_dir: Path, fname: str):
    manifest_file = dist_dir / "data" / "manifest.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    fpath = dist_dir / "data" / fname
    manifest["content_hashes"][fname] = hashlib.sha256(fpath.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def test_unverified_question_blocks_distribution(compiler, tmp_path):
    dist_dir = compiler.compile(clean=True)
    q_file = dist_dir / "data" / "questions.json"
    questions = json.loads(q_file.read_text(encoding="utf-8"))

    # Tamper with verification status of first question
    questions[0]["verification_status"] = "UNVERIFIED"
    q_file.write_text(json.dumps(questions, indent=2), encoding="utf-8")
    _update_manifest_hash(dist_dir, "questions.json")

    with pytest.raises(AssertionError, match="Unverified question"):
        compiler._validate_distribution(dist_dir)


def test_review_queue_item_blocks_distribution(compiler):
    dist_dir = compiler.compile(clean=True)
    q_file = dist_dir / "data" / "questions.json"
    questions = json.loads(q_file.read_text(encoding="utf-8"))

    # Tamper by injecting review queue ID
    questions[0]["question_id"] = "gen-q-ambig-test-01"
    q_file.write_text(json.dumps(questions, indent=2), encoding="utf-8")
    _update_manifest_hash(dist_dir, "questions.json")

    with pytest.raises(AssertionError, match="Unverified review item"):
        compiler._validate_distribution(dist_dir)


def test_duplicate_question_id_blocks_distribution(compiler):
    dist_dir = compiler.compile(clean=True)
    q_file = dist_dir / "data" / "questions.json"
    questions = json.loads(q_file.read_text(encoding="utf-8"))

    # Inject duplicate question
    dup = dict(questions[0])
    questions.append(dup)
    q_file.write_text(json.dumps(questions, indent=2), encoding="utf-8")
    _update_manifest_hash(dist_dir, "questions.json")

    with pytest.raises(AssertionError, match="Duplicate question ID"):
        compiler._validate_distribution(dist_dir)


def test_dangling_formula_reference_blocks_distribution(compiler):
    dist_dir = compiler.compile(clean=True)
    ch_file = dist_dir / "data" / "chapter_rotational-motion.json"
    ch_data = json.loads(ch_file.read_text(encoding="utf-8"))

    # Tamper section formula reference
    ch_data["sections"][0]["formulas"][0]["formula_id"] = "formula-nonexistent-ghost-01"
    ch_file.write_text(json.dumps(ch_data, indent=2), encoding="utf-8")
    _update_manifest_hash(dist_dir, "chapter_rotational-motion.json")

    with pytest.raises(AssertionError, match="Dangling formula reference"):
        compiler._validate_distribution(dist_dir)


def test_tampered_manifest_hash_blocks_distribution(compiler):
    dist_dir = compiler.compile(clean=True)
    formulas_file = dist_dir / "data" / "formulas.json"

    # Modify formulas.json without updating manifest
    formulas_file.write_text(formulas_file.read_text(encoding="utf-8") + " ", encoding="utf-8")

    with pytest.raises(AssertionError, match="Hash mismatch"):
        compiler._validate_distribution(dist_dir)
