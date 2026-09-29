from pathlib import Path
from typing import Optional
import pypdf
from PIL import Image

from jee_physics.models.enums import FileFormat
from jee_physics.models.source import PageContentRepresentation, SourceRegistryRecord
from jee_physics.storage.io import read_json


def get_page_content_representation(
    source_id: str,
    page_number: int,
    sources_raw_dir: Path,
    registry_dir: Path,
    figures_raw_dir: Optional[Path] = None,
    extract_embedded_images: bool = False,
) -> PageContentRepresentation:
    """Provides a standardized page bundle (Text, Image path, Metadata) for downstream agents.
    
    Ensures future agents do not directly manipulate or scan raw filesystem paths.
    """
    sources_raw_dir = Path(sources_raw_dir)
    registry_dir = Path(registry_dir)

    reg_file = registry_dir / f"{source_id}.json"
    if not reg_file.exists():
        raise FileNotFoundError(f"Source registry record not found for source_id: '{source_id}'")

    reg_data = read_json(reg_file)
    record = SourceRegistryRecord.model_validate(reg_data)

    source_path = sources_raw_dir / (record.file_path or record.file_name)
    if not source_path.exists():
        raise FileNotFoundError(f"Physical source file not found at: '{source_path}'")

    if record.file_format == FileFormat.IMAGE:
        # Standalone image source (e.g. scan / photo)
        dims = None
        try:
            with Image.open(source_path) as img:
                dims = [float(img.width), float(img.height)]
        except Exception:
            pass

        return PageContentRepresentation(
            source_id=source_id,
            page_number=1,
            extracted_text=None,
            page_image_path=str(source_path),
            has_images=True,
            image_count=1,
            dimensions_pt=dims,
            metadata={"source_file": record.file_name, "format": "image"},
        )

    elif record.file_format == FileFormat.PDF:
        reader = pypdf.PdfReader(str(source_path))
        if page_number < 1 or page_number > len(reader.pages):
            raise IndexError(
                f"Requested page {page_number} is out of bounds (1..{len(reader.pages)}) for '{record.file_name}'"
            )

        page = reader.pages[page_number - 1]
        text = page.extract_text() or ""
        cleaned_text = text.strip() if text else None

        image_count = 0
        try:
            image_count = len(page.images)
        except Exception:
            image_count = 0

        dimensions = None
        try:
            box = page.mediabox
            dimensions = [float(box.width), float(box.height)]
        except Exception:
            dimensions = None

        extracted_img_path = None
        if extract_embedded_images and image_count > 0 and figures_raw_dir:
            figures_raw_dir = Path(figures_raw_dir)
            figures_raw_dir.mkdir(parents=True, exist_ok=True)
            # Extract first image from page if present
            try:
                for img_idx, img_file in enumerate(page.images):
                    img_dest = figures_raw_dir / f"{source_id}_p{page_number:04d}_img{img_idx+1}.png"
                    with open(img_dest, "wb") as f:
                        f.write(img_file.data)
                    extracted_img_path = str(img_dest)
                    break
            except Exception:
                extracted_img_path = None

        return PageContentRepresentation(
            source_id=source_id,
            page_number=page_number,
            extracted_text=cleaned_text,
            page_image_path=extracted_img_path,
            has_images=(image_count > 0),
            image_count=image_count,
            dimensions_pt=dimensions,
            metadata={"source_file": record.file_name, "format": "pdf"},
        )

    else:
        raise ValueError(f"Unsupported format for page representation: {record.file_format}")
