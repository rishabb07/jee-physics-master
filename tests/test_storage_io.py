import json
import tempfile
from pathlib import Path
import pytest
from jee_physics.storage.io import read_json, read_jsonl, safe_write_json, safe_write_jsonl


def test_safe_write_json_writes_valid_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "output.json"
        data = {"project": "jee-physics", "atoms_count": 42}

        safe_write_json(target, data)
        assert target.exists()

        loaded = read_json(target)
        assert loaded == data


def test_safe_writes_do_not_leave_corrupt_partial_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "vital_data.json"
        original_data = {"status": "unaltered", "version": 1}
        safe_write_json(target, original_data)

        # Attempt to write an un-serializable object (e.g. set)
        bad_data = {"status": "corrupted", "bad_set": {1, 2, 3}}
        with pytest.raises(TypeError):
            safe_write_json(target, bad_data)

        # Target file must still contain the intact original data, not a partial corrupt file!
        assert target.exists()
        loaded = read_json(target)
        assert loaded == original_data

        # Ensure no dangling temporary files remain
        tmp_files = list(Path(tmpdir).glob(".tmp_*"))
        assert len(tmp_files) == 0


def test_safe_write_jsonl_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "atoms.jsonl"
        records = [
            {"id": "atom-1", "type": "theory"},
            {"id": "atom-2", "type": "question"},
        ]
        safe_write_jsonl(target, records)
        loaded = read_jsonl(target)
        assert loaded == records
