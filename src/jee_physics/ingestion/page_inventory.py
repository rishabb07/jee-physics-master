import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
import pypdf
from PIL import Image

from jee_physics.models.enums import FileFormat
from jee_physics.models.source import PageRecord, SourcePageInventory


def generate_pdf_page_inventory(source_id: str, file_path: Path, file_hash: str) -> SourcePageInventory:
    """Generates a complete deterministic page-by-page inventory of a PDF document."""
    file_path = Path(file_path)
    reader = pypdf.PdfReader(str(file_path))

    page_records: List[PageRecord] = []
    pages_with_text = 0
    pages_with_images = 0

    total_pages = len(reader.pages)

    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        raw_text = ""
        try:
            raw_text = page.extract_text() or ""
        except Exception:
            raw_text = ""

        cleaned_text = raw_text.strip()
        has_text = len(cleaned_text) > 0
        text_len = len(cleaned_text)

        if has_text:
            pages_with_text += 1
            page_hash = hashlib.sha256(cleaned_text.encode("utf-8")).hexdigest()
            snippet = cleaned_text[:200].replace("\n", " ").strip()
        else:
            page_hash = hashlib.sha256(f"{source_id}:page:{page_num}".encode("utf-8")).hexdigest()
            snippet = None

        image_count = 0
        try:
            image_count = len(page.images)
        except Exception:
            image_count = 0

        has_images = image_count > 0
        if has_images:
            pages_with_images += 1

        dimensions: Optional[List[float]] = None
        try:
            box = page.mediabox
            dimensions = [float(box.width), float(box.height)]
        except Exception:
            dimensions = None

        page_records.append(
            PageRecord(
                source_id=source_id,
                page_number=page_num,
                page_hash=page_hash,
                has_text=has_text,
                approximate_text_length=text_len,
                has_images=has_images,
                image_count=image_count,
                dimensions_pt=dimensions,
                text_snippet=snippet,
            )
        )

    is_image_only = (pages_with_text == 0 and total_pages > 0)

    return SourcePageInventory(
        source_id=source_id,
        file_name=file_path.name,
        sha256=file_hash,
        total_pages=total_pages,
        pages_with_text=pages_with_text,
        pages_with_images=pages_with_images,
        is_image_only=is_image_only,
        pages=page_records,
        created_at=datetime.now(timezone.utc),
    )


def generate_image_page_inventory(source_id: str, file_path: Path, file_hash: str) -> SourcePageInventory:
    """Generates a 1-page inventory for standalone image files (scans, photos, handwritten notes)."""
    file_path = Path(file_path)
    dimensions: Optional[List[float]] = None
    try:
        with Image.open(file_path) as img:
            dimensions = [float(img.width), float(img.height)]
    except Exception:
        dimensions = None

    page_rec = PageRecord(
        source_id=source_id,
        page_number=1,
        page_hash=file_hash,
        has_text=False,
        approximate_text_length=0,
        has_images=True,
        image_count=1,
        dimensions_pt=dimensions,
        text_snippet=None,
    )

    return SourcePageInventory(
        source_id=source_id,
        file_name=file_path.name,
        sha256=file_hash,
        total_pages=1,
        pages_with_text=0,
        pages_with_images=1,
        is_image_only=True,
        pages=[page_rec],
        created_at=datetime.now(timezone.utc),
    )


def generate_page_inventory(source_id: str, file_path: Path, file_format: FileFormat, file_hash: str) -> SourcePageInventory:
    """Dispatches inventory creation based on detected file format."""
    if file_format == FileFormat.PDF:
        return generate_pdf_page_inventory(source_id, file_path, file_hash)
    elif file_format == FileFormat.IMAGE:
        return generate_image_page_inventory(source_id, file_path, file_hash)
    else:
        raise ValueError(f"Cannot generate page inventory for format: {file_format}")
