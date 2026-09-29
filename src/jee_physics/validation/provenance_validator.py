from pathlib import Path
from typing import List, Set
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.storage.io import read_json


def validate_atom_provenance(atom: KnowledgeAtom, registry_dir: Path | None = None) -> List[str]:
    """Validates the referential and numerical integrity of an atom's provenance entries."""
    errors: List[str] = []

    if not atom.provenance:
        errors.append("Atom has empty provenance list. Every atom must trace to at least one source.")
        return errors

    valid_source_ids: Set[str] = set()
    if registry_dir and Path(registry_dir).exists():
        for reg_file in Path(registry_dir).glob("*.json"):
            try:
                data = read_json(reg_file)
                if "source_id" in data:
                    valid_source_ids.add(data["source_id"])
            except Exception:
                pass

    for idx, prov in enumerate(atom.provenance):
        # Check source_id exists in registry if registry is provided
        if registry_dir and valid_source_ids and prov.source_id not in valid_source_ids:
            errors.append(
                f"Provenance #{idx}: referenced source_id '{prov.source_id}' does not exist in registry."
            )

        # Check page bounds
        if prov.page_start is not None and prov.page_end is not None:
            if prov.page_start > prov.page_end:
                errors.append(
                    f"Provenance #{idx}: page_start ({prov.page_start}) exceeds page_end ({prov.page_end})."
                )

        if not prov.file_name.strip():
            errors.append(f"Provenance #{idx}: file_name cannot be empty.")

    return errors
