import tempfile
from pathlib import Path
from jee_physics.core.hasher import compute_content_hash, compute_file_sha256


def test_hashing_same_file_twice_gives_identical_hash():
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f:
        f.write("A particle moves in a straight line with constant acceleration a.")
        f_path = Path(f.name)

    try:
        hash1 = compute_file_sha256(f_path)
        hash2 = compute_file_sha256(f_path)
        assert hash1 == hash2
        assert len(hash1) == 64
    finally:
        f_path.unlink()


def test_modified_file_detected_with_different_hash():
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f:
        f.write("Initial state: velocity v0 = 10 m/s")
        f_path = Path(f.name)

    try:
        orig_hash = compute_file_sha256(f_path)

        # Modify the file
        with open(f_path, "a", encoding="utf-8") as f:
            f.write("\nModified state: velocity v0 = 20 m/s")

        new_hash = compute_file_sha256(f_path)
        assert orig_hash != new_hash
    finally:
        f_path.unlink()


def test_deterministic_content_hash_invariant_to_key_order():
    dict1 = {"title": "Kinematics", "order": 1, "concepts": ["velocity", "acceleration"]}
    dict2 = {"order": 1, "concepts": ["velocity", "acceleration"], "title": "Kinematics"}

    hash1 = compute_content_hash(dict1)
    hash2 = compute_content_hash(dict2)
    assert hash1 == hash2
