from pathlib import Path
from typing import Any, Dict, List, Tuple
from pydantic import ValidationError

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.source import SourceRegistryRecord
from jee_physics.storage.io import read_json


class ValidationResult:
    def __init__(self, is_valid: bool, errors: List[str]):
        self.is_valid = is_valid
        self.errors = errors

    def __bool__(self) -> bool:
        return self.is_valid


def validate_atom_dict(data: Dict[str, Any]) -> Tuple[ValidationResult, KnowledgeAtom | None]:
    """Validates an in-memory dictionary against the KnowledgeAtom schema."""
    try:
        atom = KnowledgeAtom.model_validate(data)
        return ValidationResult(True, []), atom
    except ValidationError as e:
        error_msgs = [f"{err['loc']}: {err['msg']}" for err in e.errors()]
        return ValidationResult(False, error_msgs), None


def validate_atom_file(path: Path) -> Tuple[ValidationResult, KnowledgeAtom | None]:
    """Reads a JSON file and validates it against the KnowledgeAtom schema."""
    try:
        data = read_json(path)
        return validate_atom_dict(data)
    except Exception as e:
        return ValidationResult(False, [f"Failed to read/parse JSON: {str(e)}"]), None


def validate_source_registry_dict(data: Dict[str, Any]) -> Tuple[ValidationResult, SourceRegistryRecord | None]:
    """Validates an in-memory dictionary against the SourceRegistryRecord schema."""
    try:
        record = SourceRegistryRecord.model_validate(data)
        return ValidationResult(True, []), record
    except ValidationError as e:
        error_msgs = [f"{err['loc']}: {err['msg']}" for err in e.errors()]
        return ValidationResult(False, error_msgs), None
