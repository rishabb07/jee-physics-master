import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List


def safe_write_json(path: Path, data: Any, indent: int = 2) -> None:
    """Safely writes JSON data using an atomic replace to prevent corrupt partial files.
    
    1. Writes serialized JSON to an adjacent temporary file.
    2. Flushes buffers and executes os.fsync.
    3. Atomically replaces target file with the temporary file.
    4. Automatically cleans up temporary file on failure.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.parent / f".tmp_{path.name}_{uuid.uuid4().hex[:6]}"

    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            if hasattr(data, "model_dump"):
                # Handle Pydantic model directly
                json.dump(data.model_dump(mode="json"), f, indent=indent, ensure_ascii=False)
            else:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        raise


def safe_write_jsonl(path: Path, records: Iterable[Any]) -> None:
    """Safely writes a stream of JSON records to a JSONL file atomically."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.parent / f".tmp_{path.name}_{uuid.uuid4().hex[:6]}"

    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            for record in records:
                if hasattr(record, "model_dump"):
                    line_data = record.model_dump(mode="json")
                else:
                    line_data = record
                f.write(json.dumps(line_data, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        raise


def read_json(path: Path) -> Any:
    """Reads and parses a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Reads a JSON Lines (JSONL) file into a list of dictionaries."""
    records: List[Dict[str, Any]] = []
    if not Path(path).exists():
        return records
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records
