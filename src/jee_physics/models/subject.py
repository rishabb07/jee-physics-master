from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

from jee_physics.models.taxonomy import SubjectType


class SubjectClassificationRecord(BaseModel):
    """Authoritative subject-boundary classification for a source document or page range."""
    classification_id: str = Field(..., description="Unique ID for this classification record")
    source_id: str = Field(..., description="Target source ID")
    page_start: int = Field(..., ge=1, description="Start page number (1-indexed)")
    page_end: int = Field(..., ge=1, description="End page number (1-indexed)")
    subject: SubjectType = Field(..., description="Classified subject (PHYSICS, CHEMISTRY, MATHEMATICS, etc.)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence score")
    reason: str = Field(..., min_length=1, description="Reasoning and visual/textual evidence for classification")
    detected_markers: List[str] = Field(default_factory=list, description="Section headers, subject titles, or formulas observed")
    status: str = Field("PROPOSED", description="'PROPOSED', 'VALIDATED', 'EXCEPTION_PENDING', or 'REJECTED'")
    classified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = Field(None, description="Boundary nuances, e.g. transitional page")


class SubjectAuditReport(BaseModel):
    """Summary report of subject classifications across an entire source document."""
    source_id: str = Field(..., description="Target source ID")
    file_name: str = Field(..., description="Source file name")
    total_pages: int = Field(..., ge=1, description="Total pages in the source")
    records: List[SubjectClassificationRecord] = Field(default_factory=list, description="List of page classifications")
    physics_pages: List[int] = Field(default_factory=list, description="List of pages classified as PHYSICS")
    excluded_pages: List[int] = Field(default_factory=list, description="List of pages excluded from Physics KB")
    uncertain_pages: List[int] = Field(default_factory=list, description="Pages with UNCERTAIN or MIXED classification")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
