import hashlib
import json
from pathlib import Path
from typing import Any


def compute_file_sha256(path: Path, chunk_size: int = 65536) -> str:
    """Computes SHA-256 fingerprint for a file by streaming chunks.
    
    Safe for very large files (e.g. 500MB+ textbook scans) without loading
    the full contents into memory.
    """
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_content_hash(data: Any) -> str:
    """Computes deterministic SHA-256 hash for Python dicts or strings.
    
    Ensures key-ordering invariance by sorting keys in JSON serialization.
    """
    if isinstance(data, (dict, list)):
        serialized = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    else:
        serialized = str(data).strip()
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
