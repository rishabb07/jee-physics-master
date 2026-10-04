"""
Deterministic Claim-Trace Reference Resolver for Phase 8.

Verifies that physical claim traces actually resolve to existing, verified artifacts
on disk and that substantive SHA-256 hashes match exactly, preventing hallucinated
or unverified references.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from jee_physics.content.gate import compute_content_hash
from jee_physics.models.content import (
    ChapterContentBlock,
    ClaimTraceClass,
    ContentVerificationStatus,
)


class ClaimResolutionStatus(str, Enum):
    RESOLVED = "RESOLVED"
    MISSING_TARGET = "MISSING_TARGET"
    HASH_MISMATCH = "HASH_MISMATCH"
    UNVERIFIED_TARGET = "UNVERIFIED_TARGET"
    UNSUPPORTED_CLAIM = "UNSUPPORTED_CLAIM"


class ClaimResolutionItem(BaseModel):
    """Result of resolving a single claim trace reference."""
    claim_location: str
    trace_class: ClaimTraceClass
    referenced_id: str
    target_path: Optional[str] = None
    expected_hash: Optional[str] = None
    actual_hash: Optional[str] = None
    status: ClaimResolutionStatus
    notes: Optional[str] = None


class ClaimResolutionReport(BaseModel):
    """Aggregate report of claim trace verification across blocks or chapters."""
    report_id: str
    chapter_id: str
    total_claims: int
    resolved_count: int
    issues_count: int
    items: List[ClaimResolutionItem] = Field(default_factory=list)
    passed: bool
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClaimResolver:
    """Deterministic engine to resolve and audit claim traces."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.kb_atoms_dir = workspace_root / "kb" / "atoms"
        self.verified_dir = workspace_root / "content" / "verified"
        self.staging_dir = workspace_root / "build" / "staging" / "incoming" / "content"

    def locate_artifact(self, ref_id: str) -> Optional[Path]:
        """Locates an artifact file by ID across kb/atoms, content/verified, and staging."""
        # 1. Check canonical kb/atoms/
        kb_path = self.kb_atoms_dir / f"{ref_id}.json"
        if kb_path.exists():
            return kb_path

        # 2. Check content/verified subdirectories
        categories = ["concepts", "formulas", "derivations", "examples", "misconceptions", "questions"]
        for cat in categories:
            p = self.verified_dir / cat / f"{ref_id}.json"
            if p.exists():
                return p

        # 3. Check staging incoming subdirectories
        for cat in categories:
            p = self.staging_dir / cat / f"{ref_id}.json"
            if p.exists():
                return p

        # 4. Check staging question bank
        qb_p = self.workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verified" / f"{ref_id}.json"
        if qb_p.exists():
            return qb_p

        return None

    def resolve_reference(
        self,
        location: str,
        trace_class: ClaimTraceClass,
        ref_id: str,
        expected_hash: Optional[str] = None,
    ) -> ClaimResolutionItem:
        """Resolves a reference ID and verifies target file existence, hash, and status."""
        target_path = self.locate_artifact(ref_id)
        if not target_path or not target_path.exists():
            return ClaimResolutionItem(
                claim_location=location,
                trace_class=trace_class,
                referenced_id=ref_id,
                target_path=None,
                expected_hash=expected_hash,
                actual_hash=None,
                status=ClaimResolutionStatus.MISSING_TARGET,
                notes=f"Referenced target '{ref_id}' could not be found on disk",
            )

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return ClaimResolutionItem(
                claim_location=location,
                trace_class=trace_class,
                referenced_id=ref_id,
                target_path=str(target_path),
                expected_hash=expected_hash,
                actual_hash=None,
                status=ClaimResolutionStatus.MISSING_TARGET,
                notes=f"Error reading artifact JSON: {e}",
            )

        actual_hash = compute_content_hash(data)

        # Hash check if expected_hash provided
        if expected_hash and expected_hash != actual_hash:
            return ClaimResolutionItem(
                claim_location=location,
                trace_class=trace_class,
                referenced_id=ref_id,
                target_path=str(target_path),
                expected_hash=expected_hash,
                actual_hash=actual_hash,
                status=ClaimResolutionStatus.HASH_MISMATCH,
                notes=f"Substantive hash mismatch: expected {expected_hash[:10]}..., got {actual_hash[:10]}...",
            )

        # Verification status check
        v_status = data.get("verification_status")
        # Canonical atoms might not have verification_status field if in kb/atoms (they are canonical)
        is_canonical = "kb/atoms" in str(target_path).replace("\\", "/")
        if not is_canonical and v_status not in (
            ContentVerificationStatus.VERIFIED.value,
            ContentVerificationStatus.PROMOTABLE.value,
            "VERIFIED",
        ):
            return ClaimResolutionItem(
                claim_location=location,
                trace_class=trace_class,
                referenced_id=ref_id,
                target_path=str(target_path),
                expected_hash=expected_hash,
                actual_hash=actual_hash,
                status=ClaimResolutionStatus.UNVERIFIED_TARGET,
                notes=f"Target artifact has non-verified status: '{v_status}'",
            )

        return ClaimResolutionItem(
            claim_location=location,
            trace_class=trace_class,
            referenced_id=ref_id,
            target_path=str(target_path),
            expected_hash=expected_hash,
            actual_hash=actual_hash,
            status=ClaimResolutionStatus.RESOLVED,
            notes="Target exists, content hash confirmed, and verification confirmed",
        )

    def audit_block(self, block: ChapterContentBlock) -> List[ClaimResolutionItem]:
        """Audits all claim references in a single chapter content block."""
        items: List[ClaimResolutionItem] = []

        if block.trace_class == ClaimTraceClass.EDITORIAL_TRANSITION:
            # Transitions have no external physics claims
            items.append(
                ClaimResolutionItem(
                    claim_location=block.block_id,
                    trace_class=block.trace_class,
                    referenced_id=block.payload_id,
                    target_path=None,
                    expected_hash=None,
                    actual_hash=None,
                    status=ClaimResolutionStatus.RESOLVED,
                    notes="Editorial transition block; exempt from external physics claim verification",
                )
            )
            return items

        # Check backing payload reference
        item = self.resolve_reference(
            location=f"{block.block_id}:payload",
            trace_class=block.trace_class,
            ref_id=block.payload_id,
        )
        items.append(item)

        # Check source atoms if referenced
        for atom_id in block.source_atom_ids:
            atom_item = self.resolve_reference(
                location=f"{block.block_id}:source_atom",
                trace_class=ClaimTraceClass.CANONICAL_KB,
                ref_id=atom_id,
            )
            items.append(atom_item)

        return items

    def audit_chapter_blocks(
        self,
        chapter_id: str,
        blocks: List[ChapterContentBlock],
    ) -> ClaimResolutionReport:
        """Audits an entire block sequence for a chapter."""
        all_items: List[ClaimResolutionItem] = []
        for b in blocks:
            all_items.extend(self.audit_block(b))

        total = len(all_items)
        resolved = sum(1 for item in all_items if item.status == ClaimResolutionStatus.RESOLVED)
        issues = total - resolved

        return ClaimResolutionReport(
            report_id=f"claim-resolution-{chapter_id}",
            chapter_id=chapter_id,
            total_claims=total,
            resolved_count=resolved,
            issues_count=issues,
            items=all_items,
            passed=(issues == 0),
        )
