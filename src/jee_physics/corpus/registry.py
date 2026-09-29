import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import pymupdf

from jee_physics.core.ids import generate_source_id
from jee_physics.models.corpus import SourceMetadataRecord, SourceRole
from jee_physics.models.enums import FileFormat, SourceStatus, SourceType
from jee_physics.models.source import SourceRegistryRecord
from jee_physics.storage.io import read_json, safe_write_json


# Authoritative bibliographic and role specifications for the 9 sources
CORPUS_CATALOG: Dict[str, Dict] = {
    "concepts_of_physics_by_h.c._verma_volume_1.pdf": {
        "source_role": SourceRole.PRIMARY_JEE,
        "source_type": SourceType.TEXTBOOK,
        "bibliographic_info": {
            "title": "Concepts of Physics (Volume 1)",
            "author": "Dr. Harish Chandra Verma",
            "publisher": "Bharati Bhawan Publishers & Distributors",
            "edition": "Standard Reprint",
            "subject_coverage": "Mechanics, Waves, and Optics for JEE Main & Advanced",
            "chapters_range": "Chapters 1 to 22",
        },
    },
    "concepts_of_physics_by_h.c._verma_volume_2.pdf": {
        "source_role": SourceRole.PRIMARY_JEE,
        "source_type": SourceType.TEXTBOOK,
        "bibliographic_info": {
            "title": "Concepts of Physics (Volume 2)",
            "author": "Dr. Harish Chandra Verma",
            "publisher": "Bharati Bhawan Publishers & Distributors",
            "edition": "Standard Reprint",
            "subject_coverage": "Thermodynamics, Electrodynamics, and Modern Physics for JEE Main & Advanced",
            "chapters_range": "Chapters 23 to 47",
        },
    },
    "Fundamentals of Physics-Halliday,Resnick,Walker.pdf": {
        "source_role": SourceRole.UNDERGRADUATE_DEPTH,
        "source_type": SourceType.TEXTBOOK,
        "bibliographic_info": {
            "title": "Fundamentals of Physics",
            "authors": ["David Halliday", "Robert Resnick", "Jearl Walker"],
            "publisher": "John Wiley & Sons, Inc.",
            "edition": "10th Extended Edition",
            "subject_coverage": "Comprehensive calculus-based foundation and derivations across all classical physics",
            "chapters_range": "Chapters 1 to 44",
        },
    },
    "University Physics with Modern Physics, 13th Edition.pdf": {
        "source_role": SourceRole.UNDERGRADUATE_DEPTH,
        "source_type": SourceType.TEXTBOOK,
        "bibliographic_info": {
            "title": "University Physics with Modern Physics",
            "authors": ["Hugh D. Young", "Roger A. Freedman"],
            "publisher": "Pearson Addison-Wesley",
            "edition": "13th Edition",
            "subject_coverage": "Rigorous university-level mechanics, thermodynamics, electromagnetism, optics, and modern physics",
            "chapters_range": "Chapters 1 to 44",
        },
    },
    "Feynman, Richard P. The Feynman Lectures on Physics.pdf": {
        "source_role": SourceRole.CONCEPTUAL_DEPTH,
        "source_type": SourceType.REFERENCE_BOOK,
        "bibliographic_info": {
            "title": "The Feynman Lectures on Physics (Volume 1)",
            "authors": ["Richard P. Feynman", "Robert B. Leighton", "Matthew Sands"],
            "publisher": "Addison-Wesley Publishing Company",
            "edition": "Definitive Edition",
            "subject_coverage": "Fundamental conceptual foundations, symmetry, conservation laws, relativity, and radiation",
            "chapters_range": "Chapters 1 to 52",
        },
    },
    "problems_in_general_physics_by_i_e_irodov.pdf": {
        "source_role": SourceRole.ADVANCED_PROBLEMS,
        "source_type": SourceType.PROBLEM_BOOK,
        "bibliographic_info": {
            "title": "Problems in General Physics",
            "author": "I. E. Irodov",
            "publisher": "Mir Publishers Moscow",
            "edition": "English Translation",
            "subject_coverage": "Advanced problems and olympiad-tier syntheses for JEE Advanced mastery",
            "parts_range": "Parts 1 to 6 (1,877 problems)",
        },
    },
    "jee_main_mock_test-01-2024-jan.pdf": {
        "source_role": SourceRole.EXAM_ASSESSMENT,
        "source_type": SourceType.TEST_PAPER,
        "bibliographic_info": {
            "title": "JEE Main Mock Test Paper 01 (January 2024 Session)",
            "publisher": "JEE National Test Series",
            "edition": "2024 Session",
            "subject_coverage": "Complete NTA JEE Main pattern test paper with Section A (MCQs) and Section B (Numerical values)",
        },
    },
    "jee_rank_booster_-02_mock_paper.pdf": {
        "source_role": SourceRole.EXAM_ASSESSMENT,
        "source_type": SourceType.TEST_PAPER,
        "bibliographic_info": {
            "title": "JEE Rank Booster Mock Paper 02",
            "publisher": "Rank Booster Test Series",
            "edition": "JEE Advanced/Main Calibration Series",
            "subject_coverage": "Physics (Q1-30), Chemistry (Q31-60), Mathematics (Q61-90)",
        },
    },
    "jee_rank_booster-03_mock_paper.pdf": {
        "source_role": SourceRole.EXAM_ASSESSMENT,
        "source_type": SourceType.TEST_PAPER,
        "bibliographic_info": {
            "title": "JEE Rank Booster Mock Paper 03",
            "publisher": "Rank Booster Test Series",
            "edition": "JEE Advanced/Main Calibration Series",
            "subject_coverage": "Physics (Q1-30), Chemistry (Q31-60), Mathematics (Q61-90)",
        },
    },
}


def register_all_corpus_sources(
    raw_dir: Path,
    registry_dir: Path,
) -> List[SourceMetadataRecord]:
    """Inspects all 9 PDF files in sources/raw/ and generates authoritative registry records."""
    raw_dir = Path(raw_dir)
    registry_dir = Path(registry_dir)
    registry_dir.mkdir(parents=True, exist_ok=True)

    metadata_records: List[SourceMetadataRecord] = []

    for file_path in sorted(raw_dir.glob("*.pdf")):
        fname = file_path.name
        if fname not in CORPUS_CATALOG:
            continue

        catalog_entry = CORPUS_CATALOG[fname]
        source_role: SourceRole = catalog_entry["source_role"]
        source_type: SourceType = catalog_entry["source_type"]
        bib_info = catalog_entry["bibliographic_info"]

        # 1. Deterministic SHA-256
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        sha256 = hashlib.sha256(file_bytes).hexdigest()
        file_size = len(file_bytes)

        # 2. Source ID
        source_id = generate_source_id(fname, sha256)

        # 3. Document inspection via PyMuPDF
        doc = pymupdf.open(str(file_path))
        page_count = len(doc)
        toc = doc.get_toc()
        toc_count = len(toc)

        # Detect extractable text
        sample_pages = min(page_count, 15)
        text_chars = sum(len(doc[i].get_text().strip()) for i in range(sample_pages))
        has_text = text_chars > 100
        is_image_only = not has_text

        # Create corpus SourceMetadataRecord
        meta_rec = SourceMetadataRecord(
            source_id=source_id,
            file_name=fname,
            relative_path=f"sources/raw/{fname}",
            sha256=sha256,
            file_size_bytes=file_size,
            page_count=page_count,
            source_role=source_role,
            has_extractable_text=has_text,
            is_image_only=is_image_only,
            toc_entries_count=toc_count,
            bibliographic_info=bib_info,
            ingestion_timestamp=datetime.now(timezone.utc),
        )
        metadata_records.append(meta_rec)

        # Create standard SourceRegistryRecord for compatibility with scanner/cli
        registry_rec = SourceRegistryRecord(
            source_id=source_id,
            source_version=1,
            file_name=fname,
            file_path=fname,
            file_size_bytes=file_size,
            sha256=sha256,
            extension=".pdf",
            mime_type="application/pdf",
            file_format=FileFormat.PDF,
            source_type=source_type,
            total_pages=page_count,
            has_extractable_text=has_text,
            is_image_only=is_image_only,
            is_encrypted=False,
            status=SourceStatus.SEGMENTED,
            processing_stage=None,
            last_error=None,
            metadata={
                "source_role": source_role.value,
                "toc_entries_count": toc_count,
                "bibliographic_info": bib_info,
            },
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        reg_file = registry_dir / f"{source_id}.json"
        safe_write_json(reg_file, registry_rec)

    return metadata_records
