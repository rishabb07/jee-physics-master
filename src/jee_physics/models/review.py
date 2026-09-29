from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

from jee_physics.models.enums import ReviewIssueType, ReviewStatus


class ReviewQueueItem(BaseModel):
    """An exception item escalated to the review queue for human or senior adjudicator inspection."""
    review_id: str = Field(..., min_length=1, description="Unique exception ID")
    issue_type: ReviewIssueType = Field(..., description="Classification of the issue")
    atom_id: Optional[str] = Field(None, description="Atom identifier if available")
    source_id: str = Field(..., min_length=1, description="Source where issue originated")
    source_file: str = Field(..., min_length=1, description="Filename of source")
    source_page: Optional[int] = Field(None, ge=1, description="Page number")
    crop_image_path: Optional[str] = Field(None, description="Path to visual snippet (for OCR/diagram ambiguities)")
    flagged_text: Optional[str] = Field(None, description="The specific transcribed snippet in question")
    problem_description: str = Field(..., min_length=1, description="Detailed statement of the ambiguity or conflict")
    suggested_action: Optional[str] = Field(None, description="Automated recommendation before escalation")
    status: ReviewStatus = Field(ReviewStatus.PENDING, description="Current resolution status")
    reviewer_decision: Optional[str] = Field(None, description="Decision made upon resolution")
    reviewer_note: Optional[str] = Field(None, description="Rationale or corrective instructions")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = Field(None, description="Timestamp of resolution")
