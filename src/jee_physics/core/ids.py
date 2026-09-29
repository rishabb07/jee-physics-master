import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from jee_physics.core.hasher import compute_content_hash
from jee_physics.models.enums import AtomType


def slugify(text: str) -> str:
    """Converts raw text into a clean kebab-case slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def generate_atom_id(chapter_id: str, atom_type: AtomType, semantic_label: str) -> str:
    """Generates a stable identifier for a Knowledge Atom.
    
    Identity Rules:
    - Atom IDs must remain stable across minor editorial revisions.
    - Format: `{chapter_slug}-{atom_type}-{semantic_slug}`
    - If semantic_label is long (e.g. question text), the normalized core is hashed
      to produce an 8-character invariant suffix.
    - Content revisions increment `atom_version` and update `content_hash`,
      preserving the permanent `atom_id` so references in ladders and mocks don't break.
    """
    clean_chapter = slugify(chapter_id)
    normalized_label = re.sub(r"\s+", " ", semantic_label).strip().lower()
    fingerprint = compute_content_hash(normalized_label)[:8]
    return f"{clean_chapter}-{atom_type.value}-{fingerprint}"


def generate_source_id(file_name: str, file_hash: str) -> str:
    """Generates a deterministic source identifier: src-{clean_name}-{hash[:8]}."""
    base_name = file_name.rsplit(".", 1)[0]
    clean_name = slugify(base_name)[:24]
    return f"src-{clean_name}-{file_hash[:8]}"


def generate_manifest_id(job_type: str) -> str:
    """Generates a unique timestamped manifest ID."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    return f"man-{slugify(job_type)}-{ts}-{rand_suffix}"


def generate_review_id(issue_type: str) -> str:
    """Generates a unique review queue item ID."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    return f"rev-{slugify(issue_type)}-{ts}-{rand_suffix}"
