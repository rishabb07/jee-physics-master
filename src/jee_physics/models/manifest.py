from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FileChecksumRecord(BaseModel):
    file_path: str = Field(..., description="Relative path of file")
    sha256: str = Field(..., min_length=64, max_length=64, description="SHA-256 fingerprint")
    size_bytes: int = Field(..., ge=0)


class JobManifest(BaseModel):
    """Manifest accompanying every batch execution for complete provenance and idempotency."""
    manifest_id: str = Field(..., min_length=1, description="Unique job execution identifier")
    job_type: str = Field(..., min_length=1, description="e.g. INGEST, SEGMENT, ATOMIZE, VERIFY, ASSEMBLE")
    stage: str = Field(..., description="Pipeline stage where job ran")
    input_files: List[FileChecksumRecord] = Field(default_factory=list, description="Fingerprints of inputs consumed")
    output_files: List[FileChecksumRecord] = Field(default_factory=list, description="Fingerprints of outputs produced")
    generated_atom_ids: List[str] = Field(default_factory=list, description="All atom IDs emitted during this run")
    status: str = Field("COMPLETED", description="QUEUED, RUNNING, COMPLETED, FAILED")
    error_message: Optional[str] = Field(None, description="Error trace if execution failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution parameters, model, timestamps")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(None)
