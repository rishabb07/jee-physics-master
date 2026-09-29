import tempfile
from pathlib import Path
import pypdf
from jee_physics.ingestion.scanner import register_new_sources, scan_directory
from jee_physics.models.enums import SourceStatus
from jee_physics.storage.io import read_json


def make_mini_pdf(dest: Path, pages: int = 1) -> None:
    writer = pypdf.PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=100, height=100)
    with open(dest, "wb") as f:
        writer.write(f)


def test_scanner_lifecycle_detection():
    with tempfile.TemporaryDirectory() as tmp_root:
        sources_dir = Path(tmp_root) / "sources" / "raw"
        registry_dir = Path(tmp_root) / "sources" / "registry"
        sources_dir.mkdir(parents=True)
        registry_dir.mkdir(parents=True)

        # 1. Place a new source PDF
        file1 = sources_dir / "irodov_problems.pdf"
        make_mini_pdf(file1, pages=2)

        # Scan should detect 1 new file
        res1 = scan_directory(sources_dir, registry_dir)
        assert len(res1.new_files) == 1
        assert len(res1.modified_files) == 0
        assert len(res1.unchanged_files) == 0

        # Register the source
        registered = register_new_sources(sources_dir, registry_dir)
        assert len(registered) == 1
        assert registered[0].status == SourceStatus.SEGMENTED
        reg_file = registry_dir / f"{registered[0].source_id}.json"
        assert reg_file.exists()

        # 2. Second scan without changes: should be unchanged
        res2 = scan_directory(sources_dir, registry_dir)
        assert len(res2.new_files) == 0
        assert len(res2.modified_files) == 0
        assert len(res2.unchanged_files) == 1

        # 3. Modify the source file
        make_mini_pdf(file1, pages=4)
        res3 = scan_directory(sources_dir, registry_dir)
        assert len(res3.new_files) == 0
        assert len(res3.modified_files) == 1
        assert len(res3.unchanged_files) == 0

