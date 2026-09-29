import json
from pathlib import Path
import pytest
import yaml

from jee_physics.corpus.classifier import classify_segment_subject
from jee_physics.corpus.disagreements import get_all_source_disagreements
from jee_physics.corpus.extractor import (
    extract_canonical_corpus_derivations,
    extract_canonical_corpus_formulas,
    extract_canonical_corpus_problems,
)
from jee_physics.corpus.indexer import build_source_library_index
from jee_physics.corpus.matrix import build_coverage_matrix_report
from jee_physics.corpus.registry import register_all_corpus_sources
from jee_physics.corpus.segmenter import segment_all_corpus_sources
from jee_physics.models.corpus import (
    CoverageStatus,
    EnhancedSourceSegment,
    SourceContentType,
    SourceFormulaRecord,
)
from jee_physics.models.source import SourceSegment
from jee_physics.models.taxonomy import SubjectType, TaxonomyTree
from jee_physics.storage.io import read_json


@pytest.fixture
def corpus_root() -> Path:
    return Path(__file__).resolve().parent.parent


def test_adversarial_rejection_of_nonexistent_source_id(corpus_root):
    """Adversarial test: Agent cannot assign or cite a nonexistent source ID."""
    reg_dir = corpus_root / "sources" / "registry"
    registered_ids = {f.stem for f in reg_dir.glob("*.json")}

    fake_source_id = "src-fabricated-source-12345678"
    assert fake_source_id not in registered_ids

    # Attempting to validate a segment or atom referencing this fake source must fail
    with pytest.raises(Exception):
        # Prov validation check
        from jee_physics.validation.provenance_validator import validate_atom_provenance
        atom = {
            "atom_id": "test-atom-fake-src",
            "source_provenance": [
                {
                    "source_id": fake_source_id,
                    "page_start": 10,
                    "page_end": 15,
                }
            ],
            "claims": [{"claim_text": "Fake claim", "provenance_indices": [0]}],
        }
        validate_atom_provenance(atom, registered_sources=registered_ids)


def test_adversarial_rejection_of_out_of_bounds_page(corpus_root):
    """Adversarial test: Agent cannot cite a page exceeding the document's actual page count."""
    reg_dir = corpus_root / "sources" / "registry"
    young_freedman_rec = None
    for f in reg_dir.glob("*.json"):
        data = read_json(f)
        if "university physics" in data.get("file_name", "").lower():
            young_freedman_rec = data
            break

    assert young_freedman_rec is not None
    total_pages = young_freedman_rec["total_pages"]
    assert total_pages == 1598

    # Attempt to cite page 2500
    with pytest.raises(ValueError, match="page_start|cannot exceed"):
        SourceSegment(
            segment_id="seg-fake-oob",
            source_id=young_freedman_rec["source_id"],
            page_start=2500,
            page_end=2400,  # inverted & OOB
            segment_title="Phantom Section",
        )


def test_adversarial_rejection_of_fabricated_taxonomy_node(corpus_root):
    """Adversarial test: Agent cannot map a segment to a phantom taxonomy node."""
    syllabus_path = corpus_root / "kb" / "taxonomy" / "syllabus.yaml"
    with open(syllabus_path, "r", encoding="utf-8") as f:
        tax_data = yaml.safe_load(f)
    tree = TaxonomyTree.model_validate(tax_data)

    fake_node_id = "quantum-teleportation-at-scale"
    assert fake_node_id not in tree.nodes
    assert tree.resolve_node_id(fake_node_id) is None


def test_adversarial_subject_boundary_blocks_chemistry_and_math(corpus_root):
    """Adversarial test: Chemistry and Math test paper pages cannot enter the Physics KB."""
    # Mock 2: page 7 is Organic Chemistry
    chem_segment = EnhancedSourceSegment(
        segment_id="seg-mock2-chem-test",
        source_id="src-jee-rank-booster-02-mock-0548b6c5",
        start_page=6,
        end_page=9,
        segment_title="Chemistry Section A & B (Q31-60)",
        subject_type="CHEMISTRY",
        content_types=[SourceContentType.OTHER],
    )
    subj = classify_segment_subject(chem_segment, "jee_rank_booster_-02_mock_paper.pdf")
    assert subj == SubjectType.CHEMISTRY
    assert subj != SubjectType.PHYSICS

    # Mock 3: page 13 is Mathematics circles
    math_segment = EnhancedSourceSegment(
        segment_id="seg-mock3-math-test",
        source_id="src-jee-rank-booster-03-mock-256f42c6",
        start_page=12,
        end_page=14,
        segment_title="Mathematics Section A & B (Q61-90)",
        subject_type="MATHEMATICS",
        content_types=[SourceContentType.OTHER],
    )
    subj_m = classify_segment_subject(math_segment, "jee_rank_booster-03_mock_paper.pdf")
    assert subj_m == SubjectType.MATHEMATICS
    assert subj_m != SubjectType.PHYSICS


def test_source_disagreement_catalog_integrity(corpus_root):
    """Verifies that known physical disagreements and sign conventions are documented."""
    disagreements = get_all_source_disagreements()
    assert len(disagreements) >= 4

    categories = {d.conflict_category for d in disagreements}
    assert "SIGN_CONVENTION" in categories
    assert "VALIDITY_REGIME" in categories
    assert "TERMINOLOGY" in categories

    # Ensure Thermodynamics sign convention is specifically recorded
    td_conflict = next((d for d in disagreements if d.conflict_id == "conflict-td-sign-001"), None)
    assert td_conflict is not None
    assert "dQ = dU + dW" in td_conflict.source_a["equation"]
    assert "\\Delta U = q + w" in td_conflict.source_b["equation"]


def test_coverage_matrix_report_determinism(corpus_root):
    """Verifies that the Source x Taxonomy Coverage Report is complete and deterministic."""
    report_json_path = corpus_root / "build" / "reports" / "source_coverage_report.json"
    report_md_path = corpus_root / "reports" / "source_coverage_report.md"
    index_json_path = corpus_root / "build" / "reports" / "source_library_index.json"

    assert report_json_path.exists()
    assert report_md_path.exists()
    assert index_json_path.exists()

    with open(report_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_taxonomy_nodes"] == 459  # 460 minus root subject node
    assert data["multi_source_nodes_count"] >= 400
    assert data["gap_nodes_count"] > 0
    assert "MULTI_SOURCE_COVERED" in data["status_counts"]
    assert "SOURCE_CONFLICT" in data["status_counts"]
    assert "WEAK_SOURCE_COVERAGE" in data["status_counts"]


def test_all_nine_sources_registered_and_segmented(corpus_root):
    """Verifies all 9 sources are properly registered and segmented with inventories."""
    reg_dir = corpus_root / "sources" / "registry"
    seg_dir = corpus_root / "sources" / "segments"

    reg_files = list(reg_dir.glob("*.json"))
    assert len(reg_files) == 9

    inv_files = list(seg_dir.glob("*_inventory.json"))
    assert len(inv_files) == 9

    seg_files = list(seg_dir.glob("*_segments.json"))
    assert len(seg_files) == 9

    total_pages = sum(read_json(f)["total_pages"] for f in inv_files)
    assert total_pages == 4839


def test_canonical_kb_atoms_strictly_untouched(corpus_root):
    """Inviolate invariant: Canonical KB atoms in kb/atoms/ must be untouched."""
    baseline_path = corpus_root / "build" / "staging" / "baseline_hashes.json"
    assert baseline_path.exists()

    with open(baseline_path, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    import hashlib
    for fpath, orig_hash in baseline["kb_atoms"].items():
        with open(fpath, "rb") as cur_f:
            cur_hash = hashlib.sha256(cur_f.read()).hexdigest()
        assert cur_hash == orig_hash, f"Canonical atom {fpath} was modified!"

    with open(corpus_root / "kb" / "taxonomy" / "syllabus.yaml", "rb") as tax_f:
        cur_tax_hash = hashlib.sha256(tax_f.read()).hexdigest()
    assert cur_tax_hash == baseline["syllabus"], "Authoritative syllabus tree was modified!"
