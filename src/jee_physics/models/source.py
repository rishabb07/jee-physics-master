from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


from jee_physics.models.enums import FileFormat, SegmentType, SourceStatus, SourceType


class SourceHistoryEntry(BaseModel):
    """Historical snapshot of a source file before a modification."""
    source_version: int = Field(..., ge=1)
    sha256: str = Field(..., min_length=64, max_length=64)
    file_size_bytes: int = Field(..., ge=0)
    total_pages: Optional[int] = Field(None, ge=1)
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    change_reason: Optional[str] = Field(None, description="Reason or context of file change")


class SourceRegistryRecord(BaseModel):
    """Tracks raw physics source files deposited into the warehouse."""
    source_id: str = Field(..., min_length=1, description="Deterministic unique source identifier")
    source_version: int = Field(1, ge=1, description="Increments on file replacement/hash change")
    file_name: str = Field(..., min_length=1, description="Source file name")
    file_path: Optional[str] = Field(None, description="Relative path within sources/raw/")
    file_size_bytes: int = Field(..., ge=0, description="Size in bytes")
    sha256: str = Field(..., min_length=64, max_length=64, description="Cryptographic SHA-256 fingerprint")
    extension: str = Field("", description="File extension with leading dot (e.g. '.pdf')")
    mime_type: str = Field("application/octet-stream", description="MIME type")

    @model_validator(mode="before")
    @classmethod
    def populate_defaults(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("extension") and data.get("file_name"):
                data["extension"] = Path(data["file_name"]).suffix.lower() or ".unknown"
        return data

    file_format: FileFormat = Field(FileFormat.UNSUPPORTED, description="Classified format (pdf, image, unsupported)")
    source_type: SourceType = Field(SourceType.OTHER, description="Provisional source category")
    total_pages: Optional[int] = Field(None, ge=0, description="Total document page count")
    has_extractable_text: bool = Field(False, description="True if PDF contains digital text streams")
    is_image_only: bool = Field(False, description="True if document appears to be scanned images only")
    is_encrypted: bool = Field(False, description="True if document is password protected")
    status: SourceStatus = Field(SourceStatus.REGISTERED, description="Ingestion lifecycle status")
    processing_stage: Optional[str] = Field(None, description="Current sub-stage or cursor")
    last_error: Optional[str] = Field(None, description="Error trace if status is FAILED")
    history: List[SourceHistoryEntry] = Field(default_factory=list, description="Historical versions prior to changes")
    affected_chapters: List[str] = Field(default_factory=list, description="Target chapters present in document")
    file_created_at: Optional[datetime] = Field(None, description="Filesystem creation timestamp")
    file_modified_at: Optional[datetime] = Field(None, description="Filesystem modification timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary scanner/extraction metadata")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PageRecord(BaseModel):
    """Deterministic inventory entry for a single page in a document."""
    source_id: str = Field(..., min_length=1)
    page_number: int = Field(..., ge=1, description="1-based page index")
    page_hash: str = Field(..., description="SHA-256 of text/content on this page")
    has_text: bool = Field(False)
    approximate_text_length: int = Field(0, ge=0)
    has_images: bool = Field(False)
    image_count: int = Field(0, ge=0)
    dimensions_pt: Optional[List[float]] = Field(None, description="[width, height] in PDF points")
    text_snippet: Optional[str] = Field(None, description="First ~200 characters for diagnostic preview")


class SourcePageInventory(BaseModel):
    """Complete page-by-page inventory of a source document stored under sources/segments/."""
    source_id: str = Field(..., min_length=1)
    file_name: str = Field(..., min_length=1)
    sha256: str = Field(..., min_length=64, max_length=64)
    total_pages: int = Field(..., ge=0)
    pages_with_text: int = Field(0, ge=0)
    pages_with_images: int = Field(0, ge=0)
    is_image_only: bool = Field(False)
    pages: List[PageRecord] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SourceSegment(BaseModel):
    """A bounded contiguous page range of a source file allocated for batch extraction."""
    segment_id: str = Field(..., min_length=1, description="Unique segment identifier")
    source_id: str = Field(..., min_length=1, description="Parent source ID")
    segment_type: SegmentType = Field(
        SegmentType.DETERMINISTIC_PAGE_SEGMENT,
        description="DETERMINISTIC_PAGE_SEGMENT vs LLM_PROPOSED_SEMANTIC_SEGMENT"
    )
    page_start: int = Field(..., ge=1, description="1-based starting page")
    page_end: int = Field(..., ge=1, description="1-based ending page")
    segment_title: str = Field(..., description="Section title or provisional topic name")
    segment_summary: Optional[str] = Field(None, description="Brief overview of contents in chunk")
    provisional_chapter_id: Optional[str] = Field(None, description="Suggested target chapter")
    provisional_topic_id: Optional[str] = Field(None, description="Suggested target topic")
    provisional_subtopic_id: Optional[str] = Field(None, description="Suggested target subtopic")
    extraction_status: str = Field("PENDING", description="PENDING, IN_PROGRESS, EXTRACTED, FAILED")
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_segment_bounds(self) -> "SourceSegment":
        if self.page_start > self.page_end:
            raise ValueError(f"page_start ({self.page_start}) cannot exceed page_end ({self.page_end})")
        return self


class SourceSegmentationPlan(BaseModel):
    """Full segmentation plan for a source document containing ordered segments."""
    source_id: str = Field(..., min_length=1)
    file_name: str = Field(..., min_length=1)
    segmentation_type: SegmentType = Field(SegmentType.DETERMINISTIC_PAGE_SEGMENT)
    total_segments: int = Field(..., ge=0)
    segments: List[SourceSegment] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PageContentRepresentation(BaseModel):
    """Standardized representation of a single page prepared for a downstream multimodal agent."""
    source_id: str = Field(..., min_length=1)
    page_number: int = Field(..., ge=1)
    extracted_text: Optional[str] = Field(None, description="Raw text extracted from PDF stream")
    page_image_path: Optional[str] = Field(None, description="Path to rendered page image if available")
    has_images: bool = Field(False)
    image_count: int = Field(0, ge=0)
    dimensions_pt: Optional[List[float]] = Field(None)
    metadata: Dict[str, Any] = Field(default_factory=dict)
