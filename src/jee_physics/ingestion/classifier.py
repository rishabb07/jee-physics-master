import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple
import pypdf
from PIL import Image

from jee_physics.models.enums import FileFormat, SourceType

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tiff", ".tif", ".bmp"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}


class FileClassificationResult:
    def __init__(
        self,
        file_format: FileFormat,
        mime_type: str,
        extension: str,
        file_size_bytes: int,
        page_count: Optional[int] = None,
        has_extractable_text: bool = False,
        is_image_only: bool = False,
        is_encrypted: bool = False,
        file_created_at: Optional[datetime] = None,
        file_modified_at: Optional[datetime] = None,
        error: Optional[str] = None,
    ):
        self.file_format = file_format
        self.mime_type = mime_type
        self.extension = extension
        self.file_size_bytes = file_size_bytes
        self.page_count = page_count
        self.has_extractable_text = has_extractable_text
        self.is_image_only = is_image_only
        self.is_encrypted = is_encrypted
        self.file_created_at = file_created_at
        self.file_modified_at = file_modified_at
        self.error = error


def get_file_timestamps(path: Path) -> Tuple[datetime, datetime]:
    """Retrieves filesystem creation and modification timestamps in UTC."""
    stat = path.stat()
    # On Windows st_ctime is creation time; on Unix it is metadata change time
    created = datetime.fromtimestamp(stat.st_ctime, timezone.utc)
    modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc)
    return created, modified


def classify_file(path: Path) -> FileClassificationResult:
    """Deterministically inspects and classifies a raw source file without modifying it."""
    path = Path(path)
    extension = path.suffix.lower()
    file_size = path.stat().st_size if path.exists() else 0
    created_at, modified_at = get_file_timestamps(path) if path.exists() else (None, None)

    mime, _ = mimetypes.guess_type(path.name)
    if not mime:
        mime = "application/pdf" if extension == ".pdf" else "application/octet-stream"

    # 1. Handle PDF documents
    if extension in SUPPORTED_PDF_EXTENSIONS:
        try:
            reader = pypdf.PdfReader(str(path))
            if reader.is_encrypted:
                return FileClassificationResult(
                    file_format=FileFormat.PDF,
                    mime_type="application/pdf",
                    extension=extension,
                    file_size_bytes=file_size,
                    page_count=0,
                    is_encrypted=True,
                    file_created_at=created_at,
                    file_modified_at=modified_at,
                    error="PDF is password-protected or encrypted",
                )

            page_count = len(reader.pages)
            if page_count == 0:
                return FileClassificationResult(
                    file_format=FileFormat.PDF,
                    mime_type="application/pdf",
                    extension=extension,
                    file_size_bytes=file_size,
                    page_count=0,
                    file_created_at=created_at,
                    file_modified_at=modified_at,
                    error="PDF contains zero pages",
                )

            # Sample pages to detect text streams and image characteristics
            sample_size = min(page_count, 10)
            pages_with_text = 0
            for i in range(sample_size):
                try:
                    text = reader.pages[i].extract_text()
                    if text and len(text.strip()) > 30:
                        pages_with_text += 1
                except Exception:
                    pass

            has_extractable_text = pages_with_text > 0
            is_image_only = pages_with_text == 0

            return FileClassificationResult(
                file_format=FileFormat.PDF,
                mime_type="application/pdf",
                extension=extension,
                file_size_bytes=file_size,
                page_count=page_count,
                has_extractable_text=has_extractable_text,
                is_image_only=is_image_only,
                is_encrypted=False,
                file_created_at=created_at,
                file_modified_at=modified_at,
            )

        except Exception as e:
            return FileClassificationResult(
                file_format=FileFormat.PDF,
                mime_type="application/pdf",
                extension=extension,
                file_size_bytes=file_size,
                file_created_at=created_at,
                file_modified_at=modified_at,
                error=f"Corrupted or invalid PDF: {str(e)}",
            )

    # 2. Handle Image files
    elif extension in SUPPORTED_IMAGE_EXTENSIONS:
        try:
            with Image.open(path) as img:
                img.verify()  # Check for integrity
            return FileClassificationResult(
                file_format=FileFormat.IMAGE,
                mime_type=mime,
                extension=extension,
                file_size_bytes=file_size,
                page_count=1,
                has_extractable_text=False,
                is_image_only=True,
                file_created_at=created_at,
                file_modified_at=modified_at,
            )
        except Exception as e:
            return FileClassificationResult(
                file_format=FileFormat.IMAGE,
                mime_type=mime,
                extension=extension,
                file_size_bytes=file_size,
                file_created_at=created_at,
                file_modified_at=modified_at,
                error=f"Corrupted image file: {str(e)}",
            )

    # 3. Unsupported format
    return FileClassificationResult(
        file_format=FileFormat.UNSUPPORTED,
        mime_type=mime,
        extension=extension,
        file_size_bytes=file_size,
        file_created_at=created_at,
        file_modified_at=modified_at,
        error=f"Unsupported file format '{extension}'",
    )
