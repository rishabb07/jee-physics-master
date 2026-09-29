import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pymupdf

from jee_physics.corpus.segmenter import decode_hcv2_text
from jee_physics.models.evidence import ExtractionQuality, PageEvidenceRecord


MATH_PATTERNS = [
    r"[=\+\-\*/\^><\(\)]",
    r"\b(sin|cos|tan|log|ln|exp|lim|sqrt)\b",
    r"[αβγδεζηθικλμνξπρστυφχψωΔΣΩ]",
    r"\b(dx|dy|dt|dr|dV|dQ|dU|dW)\b",
    r"\d+\s*[\^/]\s*\d+",
]
MATH_REGEX = re.compile("|".join(MATH_PATTERNS), re.IGNORECASE)

FIGURE_PATTERNS = re.compile(r"\b(fig\.|figure|diagram|schematic)\b", re.IGNORECASE)
TABLE_PATTERNS = re.compile(r"\b(table\s+\d+|table\s+[ivx]+)\b", re.IGNORECASE)
EXAMPLE_PATTERNS = re.compile(r"\b(example\s+\d+|sample\s+problem\s+\d+|illustration\s+\d+)\b", re.IGNORECASE)
PROBLEM_PATTERNS = re.compile(
    r"\b(exercises?|problems?|questions?\s+for\s+short\s+answer|objective\s+i|objective\s+ii|practice\s+set|multiple\s+choice)\b",
    re.IGNORECASE,
)


def extract_page_text_robust(page: pymupdf.Page, source_id: str) -> Tuple[str, ExtractionQuality, bool]:
    """
    Extracts text from a PyMuPDF page, applying Caesar decode for HCV2 and identifying vectorized glyphs.
    Returns (cleaned_text, extraction_quality, is_corrupted).
    """
    raw_text = page.get_text() or ""
    is_corrupted = False

    if "concepts-of-physics-by-h-1fd380f4" in source_id:
        from jee_physics.corpus.hcv2_decoder import extract_hcv2_page
        text, is_shifted, quality = extract_hcv2_page(raw_text)
        return text.strip(), quality, False

    if "jee-main-mock-test-01-20-222525c1" in source_id:
        # Vectorized glyph mock paper
        drawings_count = len(page.get_drawings())
        if drawings_count > 50:
            return f"[Vectorized Mock Exam Page: {drawings_count} drawing paths]", ExtractionQuality.VECTORIZED_GLYPHS, False
        return "", ExtractionQuality.EMPTY, False

    cleaned = raw_text.strip()
    if not cleaned:
        drawings = len(page.get_drawings())
        if drawings > 50:
            return f"[Vector Graphics Page: {drawings} paths]", ExtractionQuality.VECTORIZED_GLYPHS, False
        return "", ExtractionQuality.EMPTY, False

    # Check for excessive unprintable or garbled control characters
    non_printable = sum(1 for c in cleaned if ord(c) < 32 and c not in "\n\r\t")
    if non_printable > len(cleaned) * 0.1:
        is_corrupted = True
        return cleaned, ExtractionQuality.DEGRADED, is_corrupted

    quality = ExtractionQuality.EXCELLENT if len(cleaned) > 200 else ExtractionQuality.GOOD
    return cleaned, quality, is_corrupted


def detect_printed_page_number(text: str) -> Optional[str]:
    """Tries to extract the printed page number from header or footer lines."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return None

    # Check first 2 lines
    for line in lines[:2]:
        m = re.match(r"^(\d{1,4})$", line)
        if m:
            return m.group(1)

    # Check last 2 lines
    for line in lines[-2:]:
        m = re.match(r"^(\d{1,4})$", line)
        if m:
            return m.group(1)

    return None


def detect_page_heading(text: str, coarse_segments: List[Dict]) -> Optional[str]:
    """Identifies the section or chapter heading on the page."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:3]:
        if re.match(r"^(chapter\s+\d+|section\s+\d+|\d+\.\d+)", line, re.IGNORECASE):
            return line[:60]
    return None


def generate_source_page_evidence_inventory(
    source_id: str,
    pdf_path: Path,
    coarse_segments: List[Dict],
) -> List[PageEvidenceRecord]:
    """
    Builds the complete deterministic page-level evidence inventory for a single PDF.
    """
    doc = pymupdf.open(str(pdf_path))
    records: List[PageEvidenceRecord] = []

    # Map page number to coarse segment heading
    page_to_heading: Dict[int, str] = {}
    for seg in coarse_segments:
        start_p = seg.get("start_page", 1)
        end_p = seg.get("end_page", 1)
        title = seg.get("segment_title", "")
        for p in range(start_p, end_p + 1):
            if p not in page_to_heading:
                page_to_heading[p] = title

    for idx, page in enumerate(doc):
        pdf_page = idx + 1
        text, quality, is_corrupted = extract_page_text_robust(page, source_id)
        text_len = len(text)

        printed_page = detect_printed_page_number(text)
        detected_heading = detect_page_heading(text, coarse_segments) or page_to_heading.get(pdf_page)

        has_eq = bool(MATH_REGEX.search(text)) if text_len > 0 else False
        has_fig = bool(FIGURE_PATTERNS.search(text)) or len(page.get_images()) > 0 or len(page.get_drawings()) > 15
        has_tbl = bool(TABLE_PATTERNS.search(text))
        has_ex = bool(EXAMPLE_PATTERNS.search(text))
        has_prob = bool(PROBLEM_PATTERNS.search(text))

        snippet = text[:150].replace("\n", " ").strip() if text else None

        records.append(
            PageEvidenceRecord(
                source_id=source_id,
                pdf_page_number=pdf_page,
                printed_page_number=printed_page,
                extraction_quality=quality,
                text_length=text_len,
                is_corrupted=is_corrupted,
                has_equations=has_eq,
                has_figures=has_fig,
                has_tables=has_tbl,
                has_examples=has_ex,
                has_exercises_problems=has_prob,
                section_or_chapter_heading=detected_heading,
                text_snippet=snippet,
            )
        )

    doc.close()
    return records


def build_all_page_inventories(
    sources_registry_dir: Path,
    sources_segments_dir: Path,
    sources_raw_dir: Path,
    output_dir: Path,
) -> Dict[str, List[PageEvidenceRecord]]:
    """
    Builds page inventories for all registered sources and persists them to sources/evidence/pages/.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    all_inventories: Dict[str, List[PageEvidenceRecord]] = {}

    for reg_file in sorted(sources_registry_dir.glob("*.json")):
        with open(reg_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        source_id = meta["source_id"]
        file_name = meta["file_name"]
        pdf_path = sources_raw_dir / file_name

        if not pdf_path.exists():
            continue

        # Load coarse segments if available
        seg_file = sources_segments_dir / f"{source_id}_segments.json"
        coarse_segments = []
        if seg_file.exists():
            with open(seg_file, "r", encoding="utf-8") as f:
                seg_data = json.load(f)
                coarse_segments = seg_data.get("segments", [])

        page_cnt = meta.get("total_pages") or meta.get("page_count", 0)
        print(f"Building page evidence inventory for {source_id} ({page_cnt} pages)...")
        records = generate_source_page_evidence_inventory(source_id, pdf_path, coarse_segments)
        all_inventories[source_id] = records

        # Save to output file
        out_file = output_dir / f"{source_id}_pages.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump([r.model_dump() for r in records], f, indent=2)

    return all_inventories
