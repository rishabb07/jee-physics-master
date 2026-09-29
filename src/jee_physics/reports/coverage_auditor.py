from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.storage.io import read_json, read_jsonl


@dataclass
class CoverageReport:
    chapter_id: str
    total_eligible_atoms: int = 0
    placed_atoms_count: int = 0
    book_atoms_count: int = 0
    mock_atoms_count: int = 0
    ladder_atoms_count: int = 0
    archive_atoms_count: int = 0
    unplaced_atom_ids: List[str] = field(default_factory=list)
    coverage_percent: float = 0.0
    is_complete: bool = False

    def to_dict(self) -> Dict[str, object]:
        return {
            "chapter_id": self.chapter_id,
            "total_eligible_atoms": self.total_eligible_atoms,
            "placed_atoms_count": self.placed_atoms_count,
            "book_atoms_count": self.book_atoms_count,
            "mock_atoms_count": self.mock_atoms_count,
            "ladder_atoms_count": self.ladder_atoms_count,
            "archive_atoms_count": self.archive_atoms_count,
            "unplaced_atom_ids": self.unplaced_atom_ids,
            "coverage_percent": round(self.coverage_percent, 2),
            "is_complete": self.is_complete,
        }


def audit_chapter_coverage(
    chapter_id: str,
    kb_atoms_dir: Path,
    output_dir: Path,
    archive_dir: Path,
) -> CoverageReport:
    """Calculates coverage of knowledge atoms for a given chapter.
    
    Invariant: Every valid atom in kb/atoms/ must be placed in either:
    - the chapter body (output/book/{chapter_id}/)
    - the question bank / ladders (output/question_ladders/{chapter_id}/)
    - mock exams (output/mock_tests/{chapter_id}/)
    - or explicitly archived (kb/archive/{chapter_id}_archive.jsonl)
    """
    kb_atoms_dir = Path(kb_atoms_dir)
    output_dir = Path(output_dir)
    archive_dir = Path(archive_dir)

    report = CoverageReport(chapter_id=chapter_id)

    # 1. Discover all eligible canonical atoms for this chapter
    eligible_atom_ids: Set[str] = set()
    if kb_atoms_dir.exists():
        for jsonl_file in kb_atoms_dir.rglob("*.jsonl"):
            for record in read_jsonl(jsonl_file):
                tax = record.get("taxonomy", {})
                if tax.get("chapter_id") == chapter_id and record.get("active", True):
                    eligible_atom_ids.add(record["atom_id"])

    report.total_eligible_atoms = len(eligible_atom_ids)
    if report.total_eligible_atoms == 0:
        report.coverage_percent = 100.0
        report.is_complete = True
        return report

    # 2. Check placed in published book
    book_placed_ids: Set[str] = set()
    book_chapter_dir = output_dir / "book" / chapter_id
    if book_chapter_dir.exists():
        for ch_file in book_chapter_dir.glob("*.json"):
            try:
                data = read_json(ch_file)
                for aid in data.get("atom_ids", []):
                    if aid in eligible_atom_ids:
                        book_placed_ids.add(aid)
            except Exception:
                pass
    report.book_atoms_count = len(book_placed_ids)

    # 3. Check placed in mock exams
    mock_placed_ids: Set[str] = set()
    mocks_dir = output_dir / "mock_tests" / chapter_id
    if mocks_dir.exists():
        for m_file in mocks_dir.glob("*.json"):
            try:
                data = read_json(m_file)
                for q in data.get("questions", []):
                    aid = q.get("atom_id")
                    if aid and aid in eligible_atom_ids:
                        mock_placed_ids.add(aid)
            except Exception:
                pass
    report.mock_atoms_count = len(mock_placed_ids)

    # 4. Check placed in question ladders
    ladder_placed_ids: Set[str] = set()
    ladders_dir = output_dir / "question_ladders" / chapter_id
    if ladders_dir.exists():
        for l_file in ladders_dir.glob("*.json"):
            try:
                data = read_json(l_file)
                for rung in data.get("rungs", []):
                    aid = rung.get("atom_id")
                    if aid and aid in eligible_atom_ids:
                        ladder_placed_ids.add(aid)
            except Exception:
                pass
    report.ladder_atoms_count = len(ladder_placed_ids)

    # 5. Check explicitly archived atoms
    archive_placed_ids: Set[str] = set()
    archive_file = archive_dir / f"{chapter_id}_archive.jsonl"
    if archive_file.exists():
        for record in read_jsonl(archive_file):
            aid = record.get("atom_id")
            if aid and aid in eligible_atom_ids:
                archive_placed_ids.add(aid)
    report.archive_atoms_count = len(archive_placed_ids)

    # Total placed union
    all_placed = book_placed_ids | mock_placed_ids | ladder_placed_ids | archive_placed_ids
    report.placed_atoms_count = len(all_placed)

    unplaced = eligible_atom_ids - all_placed
    report.unplaced_atom_ids = sorted(list(unplaced))
    report.coverage_percent = (report.placed_atoms_count / report.total_eligible_atoms) * 100.0
    report.is_complete = (len(unplaced) == 0)

    return report
