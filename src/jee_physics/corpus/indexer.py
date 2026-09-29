from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from jee_physics.corpus.disagreements import get_all_source_disagreements
from jee_physics.corpus.extractor import (
    extract_canonical_corpus_derivations,
    extract_canonical_corpus_formulas,
    extract_canonical_corpus_problems,
)
from jee_physics.corpus.matrix import build_coverage_matrix_report, generate_markdown_coverage_report
from jee_physics.corpus.registry import register_all_corpus_sources
from jee_physics.corpus.segmenter import segment_all_corpus_sources
from jee_physics.models.corpus import EnhancedSourceSegment, SourceLibraryIndex, SourceMetadataRecord
from jee_physics.storage.io import safe_write_json


def build_source_library_index(
    sources: List[SourceMetadataRecord],
    segments_by_source: Dict[str, List[EnhancedSourceSegment]],
    coverage_report: Any,
) -> SourceLibraryIndex:
    """Assembles the complete browsable machine-readable source index."""
    formulas = extract_canonical_corpus_formulas()
    derivations = extract_canonical_corpus_derivations()
    problems = extract_canonical_corpus_problems()
    disagreements = get_all_source_disagreements()

    total_pages = sum(s.page_count for s in sources)
    total_segments = sum(len(segs) for segs in segments_by_source.values())

    coverage_summary = {
        "total_taxonomy_nodes": coverage_report.total_taxonomy_nodes,
        "multi_source_nodes_count": coverage_report.multi_source_nodes_count,
        "single_source_nodes_count": coverage_report.single_source_nodes_count,
        "gap_nodes_count": coverage_report.gap_nodes_count,
        "status_counts": coverage_report.status_counts,
    }

    index = SourceLibraryIndex(
        index_id=f"idx-corpus-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        generated_at=datetime.now(timezone.utc),
        total_sources=len(sources),
        total_pages=total_pages,
        total_segments=total_segments,
        total_formulas=len(formulas),
        total_derivations=len(derivations),
        total_problems=len(problems),
        sources=sources,
        segments_by_source=segments_by_source,
        taxonomy_coverage_summary=coverage_summary,
        disagreements=disagreements,
    )
    return index


def run_full_corpus_pipeline(
    root_dir: Path,
) -> Dict[str, Any]:
    """Orchestrates complete deterministic ingestion, segmentation, mapping, and report generation."""
    root = Path(root_dir)
    raw_dir = root / "sources" / "raw"
    reg_dir = root / "sources" / "registry"
    seg_dir = root / "sources" / "segments"
    reports_build_dir = root / "build" / "reports"
    reports_md_dir = root / "reports"
    syllabus_path = root / "kb" / "taxonomy" / "syllabus.yaml"

    reports_build_dir.mkdir(parents=True, exist_ok=True)
    reports_md_dir.mkdir(parents=True, exist_ok=True)

    # 1. Register sources
    sources = register_all_corpus_sources(raw_dir, reg_dir)

    # 2. Page inventories & semantic segments
    segments_by_source = segment_all_corpus_sources(raw_dir, reg_dir, seg_dir)

    # 3. Coverage matrix
    coverage_report = build_coverage_matrix_report(syllabus_path, segments_by_source)

    # Save build/reports/source_coverage_report.json
    safe_write_json(reports_build_dir / "source_coverage_report.json", coverage_report)

    # Save reports/source_coverage_report.md
    generate_markdown_coverage_report(coverage_report, reports_md_dir / "source_coverage_report.md")

    # 4. Source Library Index
    index = build_source_library_index(sources, segments_by_source, coverage_report)
    safe_write_json(reports_build_dir / "source_library_index.json", index)

    return {
        "sources_count": len(sources),
        "total_pages": index.total_pages,
        "total_segments": index.total_segments,
        "total_formulas": index.total_formulas,
        "total_derivations": index.total_derivations,
        "total_problems": index.total_problems,
        "multi_source_nodes": coverage_report.multi_source_nodes_count,
        "status_counts": coverage_report.status_counts,
        "coverage_report_json": str(reports_build_dir / "source_coverage_report.json"),
        "coverage_report_md": str(reports_md_dir / "source_coverage_report.md"),
        "library_index_json": str(reports_build_dir / "source_library_index.json"),
    }
