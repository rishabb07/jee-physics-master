import tempfile
from pathlib import Path
import pytest
from pydantic import ValidationError

from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference
from jee_physics.models.enums import AtomType
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.models.source import SourceRegistryRecord
from jee_physics.storage.io import safe_write_json
from jee_physics.validation.provenance_validator import validate_atom_provenance


def test_invalid_page_range_raises_validation_error():
    with pytest.raises(ValidationError) as exc:
        ProvenanceRecord(
            source_id="src-test-01",
            file_name="test.pdf",
            page_start=50,
            page_end=40,  # Invalid: page_start > page_end
        )
    assert "page_start (50) cannot exceed page_end (40)" in str(exc.value)


def test_multi_provenance_supported():
    prov1 = ProvenanceRecord(
        source_id="src-hcv-vol1",
        file_name="hcv_vol1.pdf",
        page_start=12,
        page_end=13,
        source_locator="Example 4",
    )
    prov2 = ProvenanceRecord(
        source_id="src-irodov",
        file_name="irodov.pdf",
        page_start=5,
        page_end=5,
        source_locator="Problem 1.2",
    )

    atom = KnowledgeAtom(
        atom_id="kinematics-theory-multi",
        atom_type=AtomType.THEORY,
        title="Instantaneous Velocity",
        taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="1d-motion"),
        provenance=[prov1, prov2],  # Multiple occurrences preserved!
        confidence=0.99,
        content_hash="1" * 64,
        content="Velocity defined as derivative of position vector with respect to time.",
    )
    assert len(atom.provenance) == 2


def test_provenance_validation_detects_unregistered_source():
    with tempfile.TemporaryDirectory() as tmpdir:
        reg_dir = Path(tmpdir)
        # Register source 'src-real-book'
        real_record = SourceRegistryRecord(
            source_id="src-real-book",
            file_name="real_book.pdf",
            file_size_bytes=1000,
            sha256="a" * 64,
        )
        safe_write_json(reg_dir / "src-real-book.json", real_record)

        # Create atom referencing a bogus un-registered source
        bogus_prov = ProvenanceRecord(
            source_id="src-fake-unregistered",
            file_name="fake.pdf",
            page_start=1,
            page_end=2,
        )
        atom = KnowledgeAtom(
            atom_id="kinematics-theory-check",
            atom_type=AtomType.THEORY,
            title="Acceleration",
            taxonomy=TaxonomyReference(chapter_id="kinematics", topic_id="1d-motion"),
            provenance=[bogus_prov],
            confidence=0.9,
            content_hash="2" * 64,
            content="Acceleration is rate of change of velocity.",
        )

        errors = validate_atom_provenance(atom, registry_dir=reg_dir)
        assert len(errors) == 1
        assert "does not exist in registry" in errors[0]
