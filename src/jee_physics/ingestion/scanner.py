import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from jee_physics.core.hasher import compute_file_sha256
from jee_physics.core.ids import generate_source_id
from jee_physics.ingestion.classifier import classify_file
from jee_physics.ingestion.page_inventory import generate_page_inventory
from jee_physics.ingestion.segmenter import create_deterministic_segments
from jee_physics.models.enums import FileFormat, SourceStatus
from jee_physics.models.source import SourceHistoryEntry, SourceRegistryRecord
from jee_physics.storage.io import read_json, safe_write_json


@dataclass
class ScanReport:
    new_files: List[Path] = field(default_factory=list)
    modified_files: List[Path] = field(default_factory=list)
    unchanged_files: List[Path] = field(default_factory=list)
    missing_source_ids: List[str] = field(default_factory=list)
    total_physical_files: int = 0


@dataclass
class RegistrationSummary:
    registered_new: int = 0
    updated_modified: int = 0
    skipped_unchanged: int = 0
    marked_missing: int = 0
    failed_sources: int = 0
    records: List[SourceRegistryRecord] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, idx: int) -> SourceRegistryRecord:
        return self.records[idx]

    def __iter__(self):
        return iter(self.records)



def scan_sources_raw(sources_raw_dir: Path, registry_dir: Path) -> ScanReport:
    """Scans ONLY sources/raw/ and compares against registry records.
    
    CRITICAL INVARIANT: The pipeline never scans arbitrary repository paths.
    Only files inside sources_raw_dir are eligible for registration.
    """
    sources_raw_dir = Path(sources_raw_dir)
    registry_dir = Path(registry_dir)
    report = ScanReport()

    # 1. Load existing registry records indexed by relative file path and file_name
    registered_records: Dict[str, SourceRegistryRecord] = {}
    if registry_dir.exists():
        for reg_file in registry_dir.glob("*.json"):
            try:
                data = read_json(reg_file)
                rec = SourceRegistryRecord.model_validate(data)
                key = rec.file_path or rec.file_name
                registered_records[key] = rec
            except Exception:
                continue

    if not sources_raw_dir.exists():
        return report

    seen_relative_paths = set()

    # 2. Walk strictly within sources_raw_dir
    for root, _, files in os.walk(sources_raw_dir):
        for fname in files:
            if fname.startswith(".") or fname.endswith(".tmp") or fname == ".gitkeep":
                continue

            file_path = Path(root) / fname
            rel_path = str(file_path.relative_to(sources_raw_dir)).replace("\\", "/")
            seen_relative_paths.add(rel_path)
            report.total_physical_files += 1

            file_hash = compute_file_sha256(file_path)

            if rel_path not in registered_records:
                # Also check by bare filename as fallback
                matched_record = None
                for rec in registered_records.values():
                    if rec.file_name == fname:
                        matched_record = rec
                        break

                if not matched_record:
                    report.new_files.append(file_path)
                else:
                    if matched_record.sha256 == file_hash:
                        report.unchanged_files.append(file_path)
                    else:
                        report.modified_files.append(file_path)
            else:
                existing = registered_records[rel_path]
                if existing.sha256 == file_hash:
                    report.unchanged_files.append(file_path)
                else:
                    report.modified_files.append(file_path)

    # 3. Detect previously registered files that disappeared from sources_raw_dir
    for rel_path, rec in registered_records.items():
        if rec.status != SourceStatus.MISSING:
            phys_path = sources_raw_dir / rel_path
            if not phys_path.exists():
                report.missing_source_ids.append(rec.source_id)

    return report


def register_sources(
    sources_raw_dir: Path,
    registry_dir: Path,
    segments_dir: Optional[Path] = None,
    max_pages_per_segment: int = 25,
) -> RegistrationSummary:
    """Registers and updates source documents strictly under sources/raw/.
    
    - Computes deterministic SHA-256 fingerprints.
    - Increments versions and preserves history when files are modified.
    - Generates page inventories and deterministic segments.
    - Handles corrupted/encrypted files gracefully without failing other files.
    """
    sources_raw_dir = Path(sources_raw_dir)
    registry_dir = Path(registry_dir)
    if segments_dir is None:
        segments_dir = sources_raw_dir.parent / "segments"
    else:
        segments_dir = Path(segments_dir)


    registry_dir.mkdir(parents=True, exist_ok=True)
    segments_dir.mkdir(parents=True, exist_ok=True)

    scan_rep = scan_sources_raw(sources_raw_dir, registry_dir)
    summary = RegistrationSummary()
    summary.skipped_unchanged = len(scan_rep.unchanged_files)

    # Load existing records for lookups
    existing_by_relpath: Dict[str, SourceRegistryRecord] = {}
    if registry_dir.exists():
        for reg_file in registry_dir.glob("*.json"):
            try:
                data = read_json(reg_file)
                rec = SourceRegistryRecord.model_validate(data)
                key = rec.file_path or rec.file_name
                existing_by_relpath[key] = rec
            except Exception:
                pass

    # 1. Process NEW files
    for file_path in scan_rep.new_files:
        rel_path = str(file_path.relative_to(sources_raw_dir)).replace("\\", "/")
        file_hash = compute_file_sha256(file_path)
        source_id = generate_source_id(file_path.name, file_hash)
        classification = classify_file(file_path)

        if classification.error:
            # Source failed inspection (corrupted, encrypted, unsupported)
            record = SourceRegistryRecord(
                source_id=source_id,
                source_version=1,
                file_name=file_path.name,
                file_path=rel_path,
                file_size_bytes=classification.file_size_bytes,
                sha256=file_hash,
                extension=classification.extension,
                mime_type=classification.mime_type,
                file_format=classification.file_format,
                total_pages=classification.page_count,
                is_encrypted=classification.is_encrypted,
                status=SourceStatus.FAILED,
                last_error=classification.error,
                file_created_at=classification.file_created_at,
                file_modified_at=classification.file_modified_at,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            safe_write_json(registry_dir / f"{source_id}.json", record)
            summary.failed_sources += 1
            summary.records.append(record)
            continue

        # Valid source file: generate page inventory & deterministic segments
        total_pages = classification.page_count or 1
        inventory = generate_page_inventory(source_id, file_path, classification.file_format, file_hash)
        safe_write_json(segments_dir / f"{source_id}_inventory.json", inventory)

        seg_plan = create_deterministic_segments(source_id, file_path.name, total_pages, max_pages_per_segment)
        safe_write_json(segments_dir / f"{source_id}_segments.json", seg_plan)

        record = SourceRegistryRecord(
            source_id=source_id,
            source_version=1,
            file_name=file_path.name,
            file_path=rel_path,
            file_size_bytes=classification.file_size_bytes,
            sha256=file_hash,
            extension=classification.extension,
            mime_type=classification.mime_type,
            file_format=classification.file_format,
            total_pages=total_pages,
            has_extractable_text=classification.has_extractable_text,
            is_image_only=classification.is_image_only,
            is_encrypted=classification.is_encrypted,
            status=SourceStatus.SEGMENTED,
            file_created_at=classification.file_created_at,
            file_modified_at=classification.file_modified_at,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        safe_write_json(registry_dir / f"{source_id}.json", record)
        summary.registered_new += 1
        summary.records.append(record)

    # 2. Process MODIFIED files
    for file_path in scan_rep.modified_files:
        rel_path = str(file_path.relative_to(sources_raw_dir)).replace("\\", "/")
        existing = existing_by_relpath.get(rel_path)
        if not existing:
            # Fallback by filename
            for r in existing_by_relpath.values():
                if r.file_name == file_path.name:
                    existing = r
                    break

        if not existing:
            continue

        new_hash = compute_file_sha256(file_path)
        classification = classify_file(file_path)

        # Archive historical snapshot
        history_entry = SourceHistoryEntry(
            source_version=existing.source_version,
            sha256=existing.sha256,
            file_size_bytes=existing.file_size_bytes,
            total_pages=existing.total_pages,
            recorded_at=existing.updated_at,
            change_reason="Source file modified on disk",
        )
        existing.history.append(history_entry)
        existing.source_version += 1
        existing.sha256 = new_hash
        existing.file_size_bytes = classification.file_size_bytes
        existing.total_pages = classification.page_count
        existing.file_modified_at = classification.file_modified_at
        existing.updated_at = datetime.now(timezone.utc)

        if classification.error:
            existing.status = SourceStatus.FAILED
            existing.last_error = classification.error
            summary.failed_sources += 1
        else:
            existing.has_extractable_text = classification.has_extractable_text
            existing.is_image_only = classification.is_image_only
            existing.is_encrypted = classification.is_encrypted
            existing.status = SourceStatus.EXTRACTION_PENDING  # Mark for re-extraction
            existing.last_error = None

            # Regenerate inventory and segments
            total_pages = classification.page_count or 1
            inventory = generate_page_inventory(existing.source_id, file_path, classification.file_format, new_hash)
            safe_write_json(segments_dir / f"{existing.source_id}_inventory.json", inventory)

            seg_plan = create_deterministic_segments(existing.source_id, file_path.name, total_pages, max_pages_per_segment)
            safe_write_json(segments_dir / f"{existing.source_id}_segments.json", seg_plan)

        safe_write_json(registry_dir / f"{existing.source_id}.json", existing)
        summary.updated_modified += 1
        summary.records.append(existing)

    # 3. Process MISSING files
    for source_id in scan_rep.missing_source_ids:
        reg_file = registry_dir / f"{source_id}.json"
        if reg_file.exists():
            data = read_json(reg_file)
            rec = SourceRegistryRecord.model_validate(data)
            rec.status = SourceStatus.MISSING
            rec.updated_at = datetime.now(timezone.utc)
            safe_write_json(reg_file, rec)
            summary.marked_missing += 1
            summary.records.append(rec)

    return summary


# Backward-compatible aliases
register_new_sources = register_sources
scan_directory = scan_sources_raw

