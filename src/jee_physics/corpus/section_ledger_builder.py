"""
Definitive Source Section Ledger Builder for JEE Physics Master Knowledge System.
Constructs the complete hierarchical section ledger across all 9 source PDFs:
source -> chapter/part -> section -> subsection -> page range -> content-bearing status -> extraction status -> evidence coverage.
Saves to sources/evidence/section_ledger.json with zero silent omissions.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from jee_physics.corpus.section_coverage_auditor import (
    _build_hcv1_sections,
    _build_hcv2_sections,
    _build_halliday_sections,
    _build_university_physics_sections,
    _build_irodov_sections,
    _build_feynman_sections,
    _build_mock_sections,
)


class SectionExtractionStatus(str, Enum):
    PHYSICS_CONTENT_COVERED = "PHYSICS_CONTENT_COVERED"
    PHYSICS_CONTENT_PARTIAL = "PHYSICS_CONTENT_PARTIAL"
    PHYSICS_CONTENT_REQUIRES_VISUAL = "PHYSICS_CONTENT_REQUIRES_VISUAL"
    PHYSICS_CONTENT_EXTRACTION_FAILED = "PHYSICS_CONTENT_EXTRACTION_FAILED"
    NON_PHYSICS = "NON_PHYSICS"
    FRONT_MATTER = "FRONT_MATTER"
    BACK_MATTER = "BACK_MATTER"
    SPACER_BLANK = "SPACER/BLANK"
    UNCERTAIN = "UNCERTAIN"


class SectionEvidenceCoverage(BaseModel):
    evidence_count: int = 0
    evidence_types_present: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    problems_count: int = 0
    formulas_count: int = 0
    concepts_count: int = 0
    derivations_count: int = 0
    examples_count: int = 0
    figures_count: int = 0
    mock_questions_count: int = 0


class SourceSectionLedgerEntry(BaseModel):
    source_id: str
    source_filename: str
    source_title: str
    edition: str
    chapter_index: Optional[int] = None
    chapter_title: str
    section_index: Optional[str] = None
    section_title_source: str
    normalized_label: str
    subsection_title: Optional[str] = None
    page_start: int
    page_end: int
    page_count: int
    content_bearing_status: str  # CONTENT_BEARING | NON_CONTENT
    has_physics_content: bool
    subject: str = "PHYSICS"
    extraction_status: SectionExtractionStatus
    evidence_coverage: SectionEvidenceCoverage
    taxonomy_node_ids: List[str] = Field(default_factory=list)
    extraction_quality: str = "EXCELLENT"
    requires_visual_inspection: bool = False
    unresolved_issues: Optional[str] = None


class SectionLedgerSummary(BaseModel):
    total_sources: int
    total_sections: int
    total_physics_sections: int
    total_non_physics_sections: int
    status_counts: Dict[str, int]
    coverage_percentage_physics: float


def build_definitive_section_ledger(
    evidence_dir: Path = Path("sources/evidence"),
    output_path: Path = Path("sources/evidence/section_ledger.json"),
) -> Tuple[List[SourceSectionLedgerEntry], SectionLedgerSummary]:
    """
    Constructs the definitive section ledger across all 9 PDFs matching against
    the expanded granular evidence ledgers.
    """
    # 1. Load all evidence items to build page index
    records_file = evidence_dir / "records.json"
    formulas_file = evidence_dir / "formulas.json"
    derivations_file = evidence_dir / "derivations.json"
    examples_file = evidence_dir / "examples.json"
    problems_file = evidence_dir / "problems.json"
    mock_file = evidence_dir / "mock_questions.json"
    figures_file = evidence_dir / "figures.json"

    evidence_by_source_page: Dict[str, Dict[int, List[Dict[str, str]]]] = {}

    def _add_ev(src: str, pgs: List[int], ev_id: str, ev_type: str):
        if src not in evidence_by_source_page:
            evidence_by_source_page[src] = {}
        for p in pgs:
            if p not in evidence_by_source_page[src]:
                evidence_by_source_page[src][p] = []
            evidence_by_source_page[src][p].append({"id": ev_id, "type": ev_type})

    if records_file.exists():
        with open(records_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                pgs = list(range(r.get("page_start", 1), r.get("page_end", 1) + 1))
                _add_ev(r.get("source_id", ""), pgs, r.get("evidence_id", ""), "CONCEPT")

    if formulas_file.exists():
        with open(formulas_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _add_ev(r.get("source_id", ""), r.get("pages", [1]), r.get("formula_id", ""), "FORMULA")

    if derivations_file.exists():
        with open(derivations_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                pr = r.get("page_range", [1, 1])
                pgs = list(range(pr[0], pr[1] + 1)) if len(pr) >= 2 else pr
                _add_ev(r.get("source_id", ""), pgs, r.get("derivation_id", ""), "DERIVATION")

    if examples_file.exists():
        with open(examples_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                pr = r.get("page_range", [1, 1])
                pgs = list(range(pr[0], pr[1] + 1)) if len(pr) >= 2 else pr
                _add_ev(r.get("source_id", ""), pgs, r.get("example_id", ""), "WORKED_EXAMPLE")

    if problems_file.exists():
        with open(problems_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _add_ev(r.get("source_id", ""), [r.get("page", 1)], r.get("problem_id", ""), "PROBLEM")

    if mock_file.exists():
        with open(mock_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _add_ev(r.get("source_id", ""), [r.get("page", 1)], r.get("mock_question_id", ""), "MOCK_QUESTION")

    if figures_file.exists():
        with open(figures_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _add_ev(r.get("source_id", ""), [r.get("page", 1)], r.get("figure_id", ""), "FIGURE")

    # 2. Build Structural Section Audit for the 9 sources
    from jee_physics.corpus.section_coverage_auditor import build_source_structural_sections
    source_audits = build_source_structural_sections(evidence_dir)

    entries: List[SourceSectionLedgerEntry] = []
    status_counts: Dict[str, int] = {}

    for src_id, audit in source_audits.items():
        src_map = evidence_by_source_page.get(src_id, {})

        for s in audit.sections:
            p1 = s.page_start
            p2 = s.page_end
            pg_cnt = p2 - p1 + 1

            # Match evidence items
            matched_items: List[Dict[str, str]] = []
            for p in range(p1, p2 + 1):
                if p in src_map:
                    matched_items.extend(src_map[p])

            unique_ids = list({it["id"] for it in matched_items})
            type_counts: Dict[str, int] = {}
            for it in matched_items:
                type_counts[it["type"]] = type_counts.get(it["type"], 0) + 1

            cov = SectionEvidenceCoverage(
                evidence_count=len(unique_ids),
                evidence_types_present=sorted(list(type_counts.keys())),
                evidence_ids=unique_ids[:50],  # store up to 50 representative IDs
                problems_count=type_counts.get("PROBLEM", 0),
                formulas_count=type_counts.get("FORMULA", 0),
                concepts_count=type_counts.get("CONCEPT", 0),
                derivations_count=type_counts.get("DERIVATION", 0),
                examples_count=type_counts.get("WORKED_EXAMPLE", 0),
                figures_count=type_counts.get("FIGURE", 0),
                mock_questions_count=type_counts.get("MOCK_QUESTION", 0),
            )

            # Determine extraction status
            is_phys = s.has_physics_content
            subj = s.subject

            if not is_phys or subj != "PHYSICS":
                if "Front Matter" in s.chapter_title or "Preface" in s.chapter_title:
                    status = SectionExtractionStatus.FRONT_MATTER
                elif "Appendix" in s.chapter_title or "Index" in s.chapter_title or "Tables" in s.chapter_title:
                    status = SectionExtractionStatus.BACK_MATTER
                elif subj in ["CHEMISTRY", "MATHEMATICS"]:
                    status = SectionExtractionStatus.NON_PHYSICS
                else:
                    status = SectionExtractionStatus.NON_PHYSICS
                req_vis = False
            elif "Feynman" in audit.filename:
                # Feynman Lectures Vol 1
                # Visual capture from scanned image plates
                if cov.evidence_count >= 2:
                    status = SectionExtractionStatus.PHYSICS_CONTENT_COVERED
                else:
                    status = SectionExtractionStatus.PHYSICS_CONTENT_REQUIRES_VISUAL
                req_vis = True
            elif "mock-test-01" in audit.filename:
                # Mock 1 vector drawings
                status = SectionExtractionStatus.PHYSICS_CONTENT_REQUIRES_VISUAL
                req_vis = True
            elif cov.evidence_count >= 3:
                status = SectionExtractionStatus.PHYSICS_CONTENT_COVERED
                req_vis = False
            elif cov.evidence_count > 0:
                status = SectionExtractionStatus.PHYSICS_CONTENT_PARTIAL
                req_vis = False
            else:
                status = SectionExtractionStatus.UNCERTAIN
                req_vis = False

            status_str = status.value
            status_counts[status_str] = status_counts.get(status_str, 0) + 1

            norm_label = (
                s.chapter_title.lower()
                .replace("chapter ", "ch")
                .replace(":", "")
                .replace(" ", "-")
                .replace(",", "")
                .replace("'", "")
            )

            entries.append(
                SourceSectionLedgerEntry(
                    source_id=src_id,
                    source_filename=audit.filename,
                    source_title=audit.filename.replace(".pdf", "").replace("_", " "),
                    edition=audit.edition,
                    chapter_index=s.chapter_index,
                    chapter_title=s.chapter_title,
                    section_index=s.section_index,
                    section_title_source=s.section_title,
                    normalized_label=norm_label,
                    subsection_title=None,
                    page_start=p1,
                    page_end=p2,
                    page_count=pg_cnt,
                    content_bearing_status="CONTENT_BEARING" if is_phys else "NON_CONTENT",
                    has_physics_content=is_phys,
                    subject=subj,
                    extraction_status=status,
                    evidence_coverage=cov,
                    taxonomy_node_ids=s.taxonomy_node_ids,
                    extraction_quality=s.extraction_quality,
                    requires_visual_inspection=req_vis,
                    unresolved_issues=s.unresolved_issues,
                )
            )

    tot_sections = len(entries)
    tot_phys = sum(1 for e in entries if e.has_physics_content)
    tot_non_phys = tot_sections - tot_phys
    covered_phys = sum(1 for e in entries if e.extraction_status in [
        SectionExtractionStatus.PHYSICS_CONTENT_COVERED,
        SectionExtractionStatus.PHYSICS_CONTENT_PARTIAL,
        SectionExtractionStatus.PHYSICS_CONTENT_REQUIRES_VISUAL,
    ])

    summary = SectionLedgerSummary(
        total_sources=len(source_audits),
        total_sections=tot_sections,
        total_physics_sections=tot_phys,
        total_non_physics_sections=tot_non_phys,
        status_counts=status_counts,
        coverage_percentage_physics=round((covered_phys / tot_phys) * 100, 2) if tot_phys > 0 else 0.0,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([e.model_dump() for e in entries], f, indent=2)

    return entries, summary
