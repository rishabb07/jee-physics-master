import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pymupdf
import pypdf

from jee_physics.models.corpus import EnhancedSourceSegment, SourceContentType
from jee_physics.models.enums import FileFormat, SegmentType
from jee_physics.models.source import PageRecord, SourcePageInventory, SourceSegment, SourceSegmentationPlan
from jee_physics.storage.io import safe_write_json


def decode_hcv2_text(text: str) -> str:
    """Decodes font-shifted ASCII in HCV Volume 2 body text."""
    res = []
    for c in text:
        if c in " \n\r\t":
            res.append(c)
        else:
            val = ord(c) + 29
            if 32 <= val <= 126:
                res.append(chr(val))
            else:
                res.append(c)
    return "".join(res)


def generate_source_inventory(
    source_id: str,
    file_path: Path,
    file_hash: str,
) -> SourcePageInventory:
    """Generates a complete deterministic page-by-page inventory using PyMuPDF."""
    file_path = Path(file_path)
    doc = pymupdf.open(str(file_path))
    total_pages = len(doc)

    page_records: List[PageRecord] = []
    pages_with_text = 0
    pages_with_images = 0

    is_hcv2 = "concepts_of_physics_by_h.c._verma_volume_2" in file_path.name.lower()

    for idx in range(total_pages):
        page_num = idx + 1
        page = doc[idx]
        raw_text = page.get_text() or ""
        if is_hcv2 and "&+$37(5" in raw_text:
            raw_text = decode_hcv2_text(raw_text)

        cleaned_text = raw_text.strip()
        has_text = len(cleaned_text) > 0
        text_len = len(cleaned_text)

        if has_text:
            pages_with_text += 1
            page_hash = hashlib.sha256(cleaned_text.encode("utf-8")).hexdigest()
            snippet = cleaned_text[:200].replace("\n", " ").strip()
        else:
            page_hash = hashlib.sha256(f"{source_id}:page:{page_num}".encode("utf-8")).hexdigest()
            snippet = None

        img_list = page.get_images()
        image_count = len(img_list)
        has_images = image_count > 0
        if has_images:
            pages_with_images += 1

        rect = page.rect
        dimensions = [float(rect.width), float(rect.height)]

        page_records.append(
            PageRecord(
                source_id=source_id,
                page_number=page_num,
                page_hash=page_hash,
                has_text=has_text,
                approximate_text_length=text_len,
                has_images=has_images,
                image_count=image_count,
                dimensions_pt=dimensions,
                text_snippet=snippet,
            )
        )

    is_image_only = (pages_with_text == 0 and total_pages > 0)

    return SourcePageInventory(
        source_id=source_id,
        file_name=file_path.name,
        sha256=file_hash,
        total_pages=total_pages,
        pages_with_text=pages_with_text,
        pages_with_images=pages_with_images,
        is_image_only=is_image_only,
        pages=page_records,
        created_at=datetime.now(timezone.utc),
    )


# Authoritative chapter and section definitions for the textbooks
HCV1_SEGMENTS: List[Tuple[str, int, int, str, List[SourceContentType]]] = [
    ("Front Matter & Preface", 1, 10, "NON_CONTENT", [SourceContentType.OTHER]),
    ("Chapter 1: Introduction to Physics", 11, 21, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.DEFINITION, SourceContentType.PROBLEM]),
    ("Chapter 2: Physics and Mathematics", 22, 40, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.PROBLEM]),
    ("Chapter 3: Rest and Motion: Kinematics", 41, 65, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 4: The Forces", 66, 73, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.DEFINITION, SourceContentType.PROBLEM]),
    ("Chapter 5: Newton's Laws of Motion", 74, 94, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 6: Friction", 95, 110, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 7: Circular Motion", 111, 127, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 8: Work and Energy", 128, 149, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.PRINCIPLE, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 9: Centre of Mass, Linear Momentum, Collision", 150, 180, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.PRINCIPLE, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 10: Rotational Mechanics", 181, 216, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 11: Gravitation", 217, 239, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 12: Simple Harmonic Motion", 240, 264, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 13: Fluid Mechanics", 265, 286, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.PRINCIPLE, SourceContentType.LAW, SourceContentType.PROBLEM]),
    ("Chapter 14: Some Mechanical Properties of Matter", 287, 304, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.FORMULA, SourceContentType.PROBLEM]),
    ("Chapter 15: Wave Motion and Waves on a String", 305, 330, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 16: Sound Waves", 331, 357, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 17: Light Waves", 358, 376, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.PRINCIPLE, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 18: Geometrical Optics", 377, 424, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 19: Optical Instruments", 425, 438, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 20: Dispersion and Spectra", 439, 447, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.EXPERIMENT_OBSERVATION, SourceContentType.PROBLEM]),
    ("Chapter 21: Speed of Light", 448, 452, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.EXPERIMENT_OBSERVATION, SourceContentType.PROBLEM]),
    ("Chapter 22: Photometry", 453, 463, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.PROBLEM]),
    ("Appendix & Index", 464, 471, "NON_CONTENT", [SourceContentType.OTHER]),
]

HCV2_SEGMENTS: List[Tuple[str, int, int, str, List[SourceContentType]]] = [
    ("Front Matter & Preface", 1, 15, "NON_CONTENT", [SourceContentType.OTHER]),
    ("Chapter 23: Heat and Temperature", 16, 29, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.PROBLEM]),
    ("Chapter 24: Kinetic Theory of Gases", 30, 53, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 25: Calorimetry", 54, 63, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.PRINCIPLE, SourceContentType.PROBLEM]),
    ("Chapter 26: Laws of Thermodynamics", 64, 79, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 27: Specific Heat Capacities of Gases", 80, 95, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 28: Heat Transfer", 96, 118, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 29: Electric Field and Potential", 119, 141, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 30: Gauss's Law", 142, 158, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 31: Capacitors", 159, 186, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 32: Electric Current in Conductors", 187, 220, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]),
    ("Chapter 33: Thermal and Chemical Effects of Electric Current", 221, 229, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.PROBLEM]),
    ("Chapter 34: Magnetic Field", 230, 245, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 35: Magnetic Field due to a Current", 246, 270, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 36: Permanent Magnets", 271, 281, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.DEFINITION, SourceContentType.PROBLEM]),
    ("Chapter 37: Magnetic Properties of Matter", 282, 298, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.DEFINITION, SourceContentType.PROBLEM]),
    ("Chapter 38: Electromagnetic Induction", 299, 330, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 39: Alternating Current", 331, 346, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 40: Electromagnetic Waves", 347, 355, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.PROBLEM]),
    ("Chapter 41: Electric Current through Gases", 356, 369, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.EXPERIMENT_OBSERVATION, SourceContentType.PROBLEM]),
    ("Chapter 42: Photoelectric Effect and Wave-Particle Duality", 370, 382, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.EXPERIMENT_OBSERVATION, SourceContentType.FORMULA, SourceContentType.PROBLEM]),
    ("Chapter 43: Bohr's Model and Physics of the Atom", 383, 402, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 44: X-rays", 403, 411, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.PROBLEM]),
    ("Chapter 45: Semiconductors and Semiconductor Devices", 412, 436, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.DEFINITION, SourceContentType.PROBLEM]),
    ("Chapter 46: The Nucleus", 437, 460, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.LAW, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Chapter 47: Special Theory of Relativity", 461, 475, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.DERIVATION, SourceContentType.PROBLEM]),
    ("Appendix & Index", 476, 481, "NON_CONTENT", [SourceContentType.OTHER]),
]

IRODOV_SEGMENTS: List[Tuple[str, int, int, str, List[SourceContentType]]] = [
    ("Preface & Notation", 1, 9, "NON_CONTENT", [SourceContentType.OTHER]),
    ("1.1 Kinematics", 10, 18, "PHYSICS", [SourceContentType.PROBLEM]),
    ("1.2 The Fundamental Equation of Dynamics", 19, 27, "PHYSICS", [SourceContentType.PROBLEM]),
    ("1.3 Conservation Laws (Energy, Momentum, Angular Momentum)", 28, 41, "PHYSICS", [SourceContentType.PROBLEM]),
    ("1.4 Universal Gravitation", 42, 44, "PHYSICS", [SourceContentType.PROBLEM]),
    ("1.5 Dynamics of a Solid Body", 45, 58, "PHYSICS", [SourceContentType.PROBLEM]),
    ("1.6 Elastic Deformations of a Solid Body", 59, 61, "PHYSICS", [SourceContentType.PROBLEM]),
    ("1.7 Hydrodynamics", 62, 66, "PHYSICS", [SourceContentType.PROBLEM]),
    ("1.8 Relativistic Mechanics", 67, 70, "PHYSICS", [SourceContentType.PROBLEM]),
    ("2.1 Equation of the Gas State. Processes", 71, 74, "PHYSICS", [SourceContentType.PROBLEM]),
    ("2.2 The First Law of Thermodynamics. Heat Capacity", 75, 80, "PHYSICS", [SourceContentType.PROBLEM]),
    ("2.3 Kinetic Theory of Gases. Boltzmann's Law and Maxwell's Distribution", 81, 86, "PHYSICS", [SourceContentType.PROBLEM]),
    ("2.4 The Second Law of Thermodynamics. Entropy", 87, 92, "PHYSICS", [SourceContentType.PROBLEM]),
    ("2.5 Liquids. Capillary Effects", 93, 95, "PHYSICS", [SourceContentType.PROBLEM]),
    ("2.6 Phase Transformations", 96, 98, "PHYSICS", [SourceContentType.PROBLEM]),
    ("2.7 Transport Phenomena", 99, 100, "PHYSICS", [SourceContentType.PROBLEM]),
    ("3.1 Constant Electric Field in Vacuum", 101, 107, "PHYSICS", [SourceContentType.PROBLEM]),
    ("3.2 Conductors and Dielectrics in an Electric Field", 108, 114, "PHYSICS", [SourceContentType.PROBLEM]),
    ("3.3 Electric Capacitance. Energy of an Electric Field", 115, 121, "PHYSICS", [SourceContentType.PROBLEM]),
    ("3.4 Electric Current", 122, 132, "PHYSICS", [SourceContentType.PROBLEM]),
    ("3.5 Constant Magnetic Field. Magnetics", 133, 143, "PHYSICS", [SourceContentType.PROBLEM]),
    ("3.6 Electromagnetic Induction. Maxwell's Equations", 144, 155, "PHYSICS", [SourceContentType.PROBLEM]),
    ("3.7 Motion of Charged Particles in Electric and Magnetic Fields", 156, 161, "PHYSICS", [SourceContentType.PROBLEM]),
    ("4.1 Mechanical Oscillations", 162, 175, "PHYSICS", [SourceContentType.PROBLEM]),
    ("4.2 Electric Oscillations", 176, 183, "PHYSICS", [SourceContentType.PROBLEM]),
    ("4.3 Elastic Waves. Acoustics", 184, 189, "PHYSICS", [SourceContentType.PROBLEM]),
    ("4.4 Electromagnetic Waves. Radiation", 190, 194, "PHYSICS", [SourceContentType.PROBLEM]),
    ("5.1 Photometry and Geometrical Optics", 195, 205, "PHYSICS", [SourceContentType.PROBLEM]),
    ("5.2 Interference of Light", 206, 211, "PHYSICS", [SourceContentType.PROBLEM]),
    ("5.3 Diffraction of Light", 212, 222, "PHYSICS", [SourceContentType.PROBLEM]),
    ("5.4 Polarization of Light", 223, 229, "PHYSICS", [SourceContentType.PROBLEM]),
    ("5.5 Dispersion and Absorption of Light", 230, 232, "PHYSICS", [SourceContentType.PROBLEM]),
    ("5.6 Optics of Moving Sources", 233, 235, "PHYSICS", [SourceContentType.PROBLEM]),
    ("5.7 Thermal Radiation. Quantum Nature of Light", 236, 240, "PHYSICS", [SourceContentType.PROBLEM]),
    ("6.1 Scattering of Particles. Rutherford-Bohr Atom", 241, 246, "PHYSICS", [SourceContentType.PROBLEM]),
    ("6.2 Wave Properties of Particles. Schrodinger Equation", 247, 252, "PHYSICS", [SourceContentType.PROBLEM]),
    ("6.3 Properties of Atoms. Spectra", 253, 259, "PHYSICS", [SourceContentType.PROBLEM]),
    ("6.4 Molecules and Crystals", 260, 265, "PHYSICS", [SourceContentType.PROBLEM]),
    ("6.5 Radioactivity", 266, 269, "PHYSICS", [SourceContentType.PROBLEM]),
    ("6.6 Nuclear Reactions", 270, 274, "PHYSICS", [SourceContentType.PROBLEM]),
    ("6.7 Elementary Particles", 275, 277, "PHYSICS", [SourceContentType.PROBLEM]),
    ("Answers and Solutions", 278, 362, "PHYSICS", [SourceContentType.SOLUTION]),
    ("Appendices & Tables", 363, 385, "NON_CONTENT", [SourceContentType.OTHER]),
]

MOCK_SEGMENTS: Dict[str, List[Tuple[str, int, int, str, List[SourceContentType]]]] = {
    "jee_main_mock_test-01-2024-jan.pdf": [
        ("Physics Section A & B (Q1-30)", 1, 4, "PHYSICS", [SourceContentType.EXAM_QUESTION, SourceContentType.PROBLEM]),
        ("Chemistry Section A & B (Q31-60)", 5, 8, "CHEMISTRY", [SourceContentType.OTHER]),
        ("Mathematics Section A & B (Q61-90)", 9, 12, "MATHEMATICS", [SourceContentType.OTHER]),
    ],
    "jee_rank_booster_-02_mock_paper.pdf": [
        ("Physics Section A & B (Q1-30)", 1, 5, "PHYSICS", [SourceContentType.EXAM_QUESTION, SourceContentType.PROBLEM]),
        ("Chemistry Section A & B (Q31-60)", 6, 9, "CHEMISTRY", [SourceContentType.OTHER]),
        ("Mathematics Section A & B (Q61-90)", 10, 12, "MATHEMATICS", [SourceContentType.OTHER]),
    ],
    "jee_rank_booster-03_mock_paper.pdf": [
        ("Physics Section A & B (Q1-30)", 1, 7, "PHYSICS", [SourceContentType.EXAM_QUESTION, SourceContentType.PROBLEM]),
        ("Chemistry Section A & B (Q31-60)", 8, 11, "CHEMISTRY", [SourceContentType.OTHER]),
        ("Mathematics Section A & B (Q61-90)", 12, 14, "MATHEMATICS", [SourceContentType.OTHER]),
    ],
}


def build_enhanced_segments(
    source_id: str,
    file_path: Path,
) -> Tuple[SourceSegmentationPlan, List[EnhancedSourceSegment]]:
    """Builds clean semantic segments for a source document using TOC bookmarks and verified layouts."""
    fname = file_path.name
    doc = pymupdf.open(str(file_path))
    total_pages = len(doc)

    raw_segments: List[Tuple[str, int, int, str, List[SourceContentType]]] = []

    if "volume_1" in fname.lower():
        raw_segments = HCV1_SEGMENTS
    elif "volume_2" in fname.lower():
        raw_segments = HCV2_SEGMENTS
    elif "irodov" in fname.lower():
        raw_segments = IRODOV_SEGMENTS
    elif fname in MOCK_SEGMENTS:
        raw_segments = MOCK_SEGMENTS[fname]
    elif "halliday" in fname.lower():
        # Derive from 44 L1 chapter bookmarks
        toc = doc.get_toc()
        l1_chapters = [(t[1].strip().replace("\r", " "), t[2]) for t in toc if t[0] == 1 and any(c.isdigit() for c in t[1])]
        raw_segments.append(("Front Matter", 1, min(l1_chapters[0][1] - 1, 26), "NON_CONTENT", [SourceContentType.OTHER]))
        for i in range(len(l1_chapters)):
            title, start_pg = l1_chapters[i]
            end_pg = l1_chapters[i+1][1] - 1 if i + 1 < len(l1_chapters) else 1300
            raw_segments.append((title, start_pg, end_pg, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]))
        raw_segments.append(("Appendices & Index", 1301, total_pages, "NON_CONTENT", [SourceContentType.OTHER]))
    elif "university physics" in fname.lower():
        # Derive from 44 L2 chapter bookmarks
        toc = doc.get_toc()
        l2_chapters = [(t[1].strip(), t[2]) for t in toc if t[0] == 2 and any(c.isdigit() for c in t[1])]
        # Filter to actual numbered chapters (1 to 44)
        filtered = []
        for title, p in l2_chapters:
            first_word = title.split()[0]
            if first_word.isdigit() and int(first_word) <= 44:
                filtered.append((title, p))
        raw_segments.append(("Front Matter", 1, 26, "NON_CONTENT", [SourceContentType.OTHER]))
        for i in range(len(filtered)):
            title, start_pg = filtered[i]
            end_pg = filtered[i+1][1] - 1 if i + 1 < len(filtered) else total_pages
            raw_segments.append((title, start_pg, end_pg, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.FORMULA, SourceContentType.DERIVATION, SourceContentType.EXAMPLE, SourceContentType.PROBLEM]))
    elif "feynman" in fname.lower():
        # 52 lectures
        # Table of contents is pages 1 to 10. Lectures 1 to 52 span pages 11 to 536 (~10 pages per lecture)
        raw_segments.append(("Front Matter & Contents", 1, 10, "NON_CONTENT", [SourceContentType.OTHER]))
        toc = doc.get_toc()
        lectures = [t[1].strip() for t in toc if t[0] == 2 and any(c.isdigit() for c in t[1][:3])]
        if not lectures:
            lectures = [f"Lecture {i:02d}" for i in range(1, 53)]
        
        # Distribute remaining pages 11 to 536 across lectures
        start = 11
        lecture_pages = (total_pages - 10) // len(lectures)
        for i, lec in enumerate(lectures):
            end = start + lecture_pages if i + 1 < len(lectures) else total_pages
            raw_segments.append((lec, start, end, "PHYSICS", [SourceContentType.CONCEPT, SourceContentType.PRINCIPLE, SourceContentType.MISCONCEPTION_CAUTION]))
            start = end + 1

    # Build typed objects
    enhanced_list: List[EnhancedSourceSegment] = []
    base_segments: List[SourceSegment] = []

    for idx, (title, start_p, end_p, subj, content_types) in enumerate(raw_segments):
        start_p = max(1, min(start_p, total_pages))
        end_p = max(start_p, min(end_p, total_pages))
        seg_id = f"seg-{source_id}-{idx+1:03d}"

        # Extract snippet from start page
        snippet = ""
        word_count = 0
        if doc and start_p <= total_pages:
            try:
                page_text = doc[start_p - 1].get_text() or ""
                if "volume_2" in fname.lower() and "&+$37(5" in page_text:
                    page_text = decode_hcv2_text(page_text)
                snippet = page_text[:200].replace("\n", " ").strip()
                # Compute total word count in segment
                for pno in range(start_p - 1, min(end_p, start_p + 5)):
                    p_text = doc[pno].get_text() or ""
                    if "volume_2" in fname.lower() and "&+$37(5" in p_text:
                        p_text = decode_hcv2_text(p_text)
                    word_count += len(p_text.split())
            except Exception:
                pass

        enhanced = EnhancedSourceSegment(
            segment_id=seg_id,
            source_id=source_id,
            start_page=start_p,
            end_page=end_p,
            segment_title=title,
            chapter_title=title,
            section_number=None,
            subject_type=subj,
            content_types=content_types,
            extracted_text_snippet=snippet,
            word_count=word_count,
            confidence=1.0,
            figure_count=0,
            equation_count=0,
            metadata={"source_file": fname},
        )
        enhanced_list.append(enhanced)

        base_seg = SourceSegment(
            segment_id=seg_id,
            source_id=source_id,
            segment_type=SegmentType.DETERMINISTIC_PAGE_SEGMENT,
            page_start=start_p,
            page_end=end_p,
            segment_title=title,
            segment_summary=f"Pages {start_p}-{end_p} of {fname} ({title})",
            provisional_chapter_id=None,
            provisional_topic_id=None,
            provisional_subtopic_id=None,
            extraction_status="EXTRACTED" if subj == "PHYSICS" else "EXCLUDED",
            confidence=1.0,
            metadata={"subject_type": subj, "content_types": [ct.value for ct in content_types]},
        )
        base_segments.append(base_seg)

    plan = SourceSegmentationPlan(
        source_id=source_id,
        file_name=fname,
        segmentation_type=SegmentType.DETERMINISTIC_PAGE_SEGMENT,
        total_segments=len(base_segments),
        segments=base_segments,
        created_at=datetime.now(timezone.utc),
    )

    return plan, enhanced_list


def segment_all_corpus_sources(
    raw_dir: Path,
    registry_dir: Path,
    segments_dir: Path,
) -> Dict[str, List[EnhancedSourceSegment]]:
    """Generates inventories and semantic segments for all 9 registered sources."""
    raw_dir = Path(raw_dir)
    segments_dir = Path(segments_dir)
    segments_dir.mkdir(parents=True, exist_ok=True)

    all_enhanced_segments: Dict[str, List[EnhancedSourceSegment]] = {}

    for file_path in sorted(raw_dir.glob("*.pdf")):
        with open(file_path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        from jee_physics.core.ids import generate_source_id
        source_id = generate_source_id(file_path.name, h)

        # 1. Page Inventory
        inv = generate_source_inventory(source_id, file_path, h)
        safe_write_json(segments_dir / f"{source_id}_inventory.json", inv)

        # 2. Semantic Segments
        plan, enhanced = build_enhanced_segments(source_id, file_path)
        safe_write_json(segments_dir / f"{source_id}_segments.json", plan)

        all_enhanced_segments[source_id] = enhanced

    return all_enhanced_segments
