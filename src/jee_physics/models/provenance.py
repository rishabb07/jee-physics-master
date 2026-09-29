from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, model_validator


class ProvenanceRecord(BaseModel):
    """Represents a specific occurrence and physical location of knowledge within a source file."""
    source_id: str = Field(..., description="Unique identifier of the registered source document")
    file_name: str = Field(..., description="Original filename of the source document")
    file_path: Optional[str] = Field(None, description="Path or relative URI to source document")
    page_start: Optional[int] = Field(None, ge=1, description="1-based starting page number where available")
    page_end: Optional[int] = Field(None, ge=1, description="1-based ending page number where available")
    source_locator: Optional[str] = Field(None, description="Human-readable location (e.g. Chapter 3, Example 12, Q14)")
    edition: Optional[str] = Field(None, description="Edition or printing identifier of the source")
    extraction_metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata captured during extraction")

    @model_validator(mode="after")
    def validate_page_range(self) -> "ProvenanceRecord":
        if self.page_start is not None and self.page_end is not None:
            if self.page_start > self.page_end:
                raise ValueError(
                    f"page_start ({self.page_start}) cannot exceed page_end ({self.page_end})"
                )
        return self
