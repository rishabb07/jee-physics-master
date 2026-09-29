import io
import tempfile
from pathlib import Path
import pypdf
import pytest
from PIL import Image

from jee_physics.ingestion.classifier import classify_file
from jee_physics.ingestion.page_inventory import generate_page_inventory
from jee_physics.ingestion.page_representation import get_page_content_representation
from jee_physics.ingestion.scanner import register_sources, scan_sources_raw
from jee_physics.ingestion.segmenter import create_deterministic_segments
from jee_physics.models.enums import FileFormat, SegmentType, SourceStatus
from jee_physics.models.source import SourcePageInventory, SourceRegistryRecord, SourceSegmentationPlan
from jee_physics.storage.io import read_json


def create_test_pdf(dest_path: Path, num_pages: int = 3, add_text: bool = True) -> Path:
    """Creates a minimal valid PDF for deterministic testing."""
    writer = pypdf.PdfWriter()
    for i in range(num_pages):
        page = writer.add_blank_page(width=612, height=792)  # Standard US Letter
        # We can add annotation or leave as blank page
    
    with open(dest_path, "wb") as f:
        writer.write(f)
    return dest_path


def create_test_image(dest_path: Path, width: int = 200, height: int = 200) -> Path:
    """Creates a minimal valid PNG image for testing."""
    img = Image.new("RGB", (width, height), color=(73, 109, 137))
    img.save(dest_path)
    return dest_path


def test_classify_and_inventory_pdf():
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = Path(tmpdir) / "sample_mechanics.pdf"
        create_test_pdf(pdf_path, num_pages=4)

        classification = classify_file(pdf_path)
        assert classification.file_format == FileFormat.PDF
        assert classification.page_count == 4
        assert classification.is_encrypted is False
        assert classification.error is None

        inventory = generate_page_inventory("src-sample-01", pdf_path, classification.file_format, "a" * 64)
        assert isinstance(inventory, SourcePageInventory)
        assert inventory.total_pages == 4
        assert len(inventory.pages) == 4
        assert inventory.pages[0].page_number == 1
        assert inventory.pages[0].dimensions_pt == [612.0, 792.0]


def test_classify_and_inventory_image():
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = Path(tmpdir) / "photo_circuit.png"
        create_test_image(img_path, width=300, height=400)

        classification = classify_file(img_path)
        assert classification.file_format == FileFormat.IMAGE
        assert classification.page_count == 1
        assert classification.is_image_only is True

        inventory = generate_page_inventory("src-img-01", img_path, classification.file_format, "b" * 64)
        assert inventory.total_pages == 1
        assert inventory.is_image_only is True
        assert inventory.pages[0].dimensions_pt == [300.0, 400.0]


def test_classify_corrupted_pdf():
    with tempfile.TemporaryDirectory() as tmpdir:
        bad_pdf = Path(tmpdir) / "broken.pdf"
        bad_pdf.write_bytes(b"%PDF-1.4\nJUNK CORRUPTED BYTES")

        classification = classify_file(bad_pdf)
        assert classification.file_format == FileFormat.PDF
        assert classification.error is not None
        assert "Corrupted or invalid PDF" in classification.error


def test_classify_unsupported_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        unsupported = Path(tmpdir) / "notes.docx"
        unsupported.write_text("Hello world", encoding="utf-8")

        classification = classify_file(unsupported)
        assert classification.file_format == FileFormat.UNSUPPORTED
        assert "Unsupported file format" in classification.error


def test_deterministic_segmentation_plan():
    plan = create_deterministic_segments("src-test-book", "Irodov.pdf", total_pages=55, max_pages_per_segment=25)
    assert isinstance(plan, SourceSegmentationPlan)
    assert plan.segmentation_type == SegmentType.DETERMINISTIC_PAGE_SEGMENT
    assert plan.total_segments == 3
    # Segments: 1-25, 26-50, 51-55
    assert plan.segments[0].page_start == 1
    assert plan.segments[0].page_end == 25
    assert plan.segments[1].page_start == 26
    assert plan.segments[1].page_end == 50
    assert plan.segments[2].page_start == 51
    assert plan.segments[2].page_end == 55


def test_scanner_strictly_ignores_files_outside_sources_raw():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        raw_dir = root / "sources" / "raw"
        outside_dir = root / "docs"
        reg_dir = root / "sources" / "registry"
        seg_dir = root / "sources" / "segments"

        raw_dir.mkdir(parents=True)
        outside_dir.mkdir(parents=True)

        # Place legitimate source in sources/raw/
        legit_file = raw_dir / "physics_legit.pdf"
        create_test_pdf(legit_file, num_pages=2)

        # Place unrelated doc PDF outside sources/raw/
        build_guide = outside_dir / "Build_Guide.pdf"
        create_test_pdf(build_guide, num_pages=5)

        # Run registration
        summary = register_sources(raw_dir, reg_dir, seg_dir)

        assert summary.registered_new == 1
        assert len(list(reg_dir.glob("*.json"))) == 1

        reg_data = read_json(list(reg_dir.glob("*.json"))[0])
        assert reg_data["file_name"] == "physics_legit.pdf"
        # Confirm build guide was completely ignored!
        for f in reg_dir.glob("*.json"):
            assert "Build_Guide" not in f.name


def test_scanner_preserves_history_when_hash_changes():
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_dir = Path(tmpdir) / "sources" / "raw"
        reg_dir = Path(tmpdir) / "sources" / "registry"
        seg_dir = Path(tmpdir) / "sources" / "segments"
        raw_dir.mkdir(parents=True)

        target_file = raw_dir / "verma_kinematics.pdf"
        create_test_pdf(target_file, num_pages=3)

        # 1. First registration
        sum1 = register_sources(raw_dir, reg_dir, seg_dir)
        assert sum1.registered_new == 1

        reg_path = list(reg_dir.glob("*.json"))[0]
        rec1 = SourceRegistryRecord.model_validate(read_json(reg_path))
        orig_hash = rec1.sha256
        orig_id = rec1.source_id
        assert rec1.source_version == 1
        assert len(rec1.history) == 0

        # 2. Modify the file on disk (add pages)
        create_test_pdf(target_file, num_pages=6)

        sum2 = register_sources(raw_dir, reg_dir, seg_dir)
        assert sum2.updated_modified == 1
        assert sum2.registered_new == 0

        rec2 = SourceRegistryRecord.model_validate(read_json(reg_path))
        # Stable source ID is preserved!
        assert rec2.source_id == orig_id
        assert rec2.source_version == 2
        assert rec2.sha256 != orig_hash
        assert rec2.total_pages == 6
        assert rec2.status == SourceStatus.EXTRACTION_PENDING

        # Historical record is preserved!
        assert len(rec2.history) == 1
        assert rec2.history[0].source_version == 1
        assert rec2.history[0].sha256 == orig_hash
        assert rec2.history[0].total_pages == 3


def test_corrupted_pdf_does_not_crash_scan_batch():
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_dir = Path(tmpdir) / "sources" / "raw"
        reg_dir = Path(tmpdir) / "sources" / "registry"
        seg_dir = Path(tmpdir) / "sources" / "segments"
        raw_dir.mkdir(parents=True)

        # One valid PDF and one corrupted PDF
        valid_file = raw_dir / "valid_exam.pdf"
        create_test_pdf(valid_file, num_pages=2)

        bad_file = raw_dir / "corrupted_file.pdf"
        bad_file.write_bytes(b"%PDF-junk")

        summary = register_sources(raw_dir, reg_dir, seg_dir)
        assert summary.registered_new == 1
        assert summary.failed_sources == 1

        # Both records should be safely registered
        records = [SourceRegistryRecord.model_validate(read_json(f)) for f in reg_dir.glob("*.json")]
        assert len(records) == 2

        statuses = {r.file_name: r.status for r in records}
        assert statuses["valid_exam.pdf"] == SourceStatus.SEGMENTED
        assert statuses["corrupted_file.pdf"] == SourceStatus.FAILED


def test_page_content_representation():
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_dir = Path(tmpdir) / "sources" / "raw"
        reg_dir = Path(tmpdir) / "sources" / "registry"
        seg_dir = Path(tmpdir) / "sources" / "segments"
        raw_dir.mkdir(parents=True)

        pdf_path = raw_dir / "lecture_notes.pdf"
        create_test_pdf(pdf_path, num_pages=2)

        summary = register_sources(raw_dir, reg_dir, seg_dir)
        source_id = summary.records[0].source_id

        # Retrieve standardized page bundle
        page_bundle = get_page_content_representation(source_id, page_number=1, sources_raw_dir=raw_dir, registry_dir=reg_dir)
        assert page_bundle.source_id == source_id
        assert page_bundle.page_number == 1
        assert page_bundle.dimensions_pt == [612.0, 792.0]
