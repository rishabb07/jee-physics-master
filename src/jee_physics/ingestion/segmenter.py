from datetime import datetime, timezone
from typing import List

from jee_physics.models.enums import SegmentType
from jee_physics.models.source import SourceSegment, SourceSegmentationPlan


def create_deterministic_segments(
    source_id: str,
    file_name: str,
    total_pages: int,
    max_pages_per_segment: int = 25,
) -> SourceSegmentationPlan:
    """Generates deterministic contiguous page range segments for a source document.
    
    Distinction:
    - DETERMINISTIC_PAGE_SEGMENT: Fixed-size mechanical page chunks (e.g. 1-25, 26-50)
      guaranteeing exhaustive coverage with zero missing pages.
    - LLM_PROPOSED_SEMANTIC_SEGMENT: Proposed later by an extraction agent based on
      detected chapter, topic, or section boundaries.
    """
    if total_pages <= 0:
        return SourceSegmentationPlan(
            source_id=source_id,
            file_name=file_name,
            segmentation_type=SegmentType.DETERMINISTIC_PAGE_SEGMENT,
            total_segments=0,
            segments=[],
            created_at=datetime.now(timezone.utc),
        )

    segments: List[SourceSegment] = []
    start_page = 1

    while start_page <= total_pages:
        end_page = min(start_page + max_pages_per_segment - 1, total_pages)
        seg_id = f"{source_id}-seg-{start_page:04d}-{end_page:04d}"
        title = f"{file_name} (Pages {start_page}–{end_page})"

        segment = SourceSegment(
            segment_id=seg_id,
            source_id=source_id,
            segment_type=SegmentType.DETERMINISTIC_PAGE_SEGMENT,
            page_start=start_page,
            page_end=end_page,
            segment_title=title,
            segment_summary=f"Deterministic chunk covering pages {start_page} through {end_page}.",
            extraction_status="PENDING",
            confidence=1.0,
        )
        segments.append(segment)
        start_page = end_page + 1

    return SourceSegmentationPlan(
        source_id=source_id,
        file_name=file_name,
        segmentation_type=SegmentType.DETERMINISTIC_PAGE_SEGMENT,
        total_segments=len(segments),
        segments=segments,
        created_at=datetime.now(timezone.utc),
    )
