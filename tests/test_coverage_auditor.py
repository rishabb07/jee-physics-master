import tempfile
from pathlib import Path

from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference
from jee_physics.models.enums import AtomStatus, AtomType
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.reports.coverage_auditor import audit_chapter_coverage
from jee_physics.storage.io import safe_write_json, safe_write_jsonl


def make_test_atom(atom_id: str, chapter_id: str) -> KnowledgeAtom:
    return KnowledgeAtom(
        atom_id=atom_id,
        atom_type=AtomType.THEORY,
        title=f"Test Theory {atom_id}",
        taxonomy=TaxonomyReference(chapter_id=chapter_id, topic_id="1d-motion"),
        provenance=[
            ProvenanceRecord(source_id="src-1", file_name="book.pdf", page_start=1, page_end=2)
        ],
        confidence=1.0,
        verification_status=AtomStatus.VERIFIED,
        content_hash="4" * 64,
        content="Physics concept text.",
    )


def test_coverage_auditor_flags_unplaced_and_counts_archive():
    with tempfile.TemporaryDirectory() as tmp_root:
        root = Path(tmp_root)
        kb_atoms_dir = root / "kb" / "atoms" / "mechanics" / "kinematics"
        output_dir = root / "output"
        archive_dir = root / "kb" / "archive"

        kb_atoms_dir.mkdir(parents=True)
        archive_dir.mkdir(parents=True)

        # 3 canonical atoms for chapter 'kinematics'
        atom1 = make_test_atom("kin-01", "kinematics")
        atom2 = make_test_atom("kin-02", "kinematics")
        atom3 = make_test_atom("kin-03", "kinematics")
        safe_write_jsonl(kb_atoms_dir / "atoms.jsonl", [atom1, atom2, atom3])

        # Atom 1 is placed in the book
        book_dir = output_dir / "book" / "kinematics"
        book_dir.mkdir(parents=True)
        safe_write_json(book_dir / "section_01.json", {"atom_ids": ["kin-01"]})

        # Atom 2 is preserved in archive
        safe_write_jsonl(archive_dir / "kinematics_archive.jsonl", [{"atom_id": "kin-02"}])

        # Atom 3 is currently unplaced!
        report = audit_chapter_coverage("kinematics", kb_atoms_dir, output_dir, archive_dir)

        assert report.total_eligible_atoms == 3
        assert report.book_atoms_count == 1
        assert report.archive_atoms_count == 1
        assert report.placed_atoms_count == 2
        assert "kin-03" in report.unplaced_atom_ids
        assert report.is_complete is False
        assert round(report.coverage_percent, 1) == 66.7

        # Now place atom 3 into archive as well (nothing silently lost)
        safe_write_jsonl(
            archive_dir / "kinematics_archive.jsonl",
            [{"atom_id": "kin-02"}, {"atom_id": "kin-03"}],
        )
        report2 = audit_chapter_coverage("kinematics", kb_atoms_dir, output_dir, archive_dir)
        assert report2.is_complete is True
        assert report2.coverage_percent == 100.0
        assert len(report2.unplaced_atom_ids) == 0
