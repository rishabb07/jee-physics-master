import hashlib
import json
import uuid
from typing import Any, Dict

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import AtomType
from jee_physics.models.verification import BlindSolverPackage


def compute_blind_package_hash(statement: str, options_data: Any, figure_refs_data: Any) -> str:
    """Computes a deterministic SHA256 hash of the problem's blind physical content."""
    payload = {
        "statement": statement,
        "options": options_data,
        "figure_refs": figure_refs_data,
    }
    canonical_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def create_blind_solver_package(atom: KnowledgeAtom) -> BlindSolverPackage:
    """Deterministically extracts a sanitized, solver-visible package from a KnowledgeAtom.
    
    CRITICAL GROUNDING & BLIND SOLVER INVARIANTS:
    - Must NEVER expose `source_claimed_answer`, `verified_answer`, or `answer`.
    - Must NEVER expose `source_solution` or `solution_methods`.
    - Must NEVER expose `verification_status`, `confidence`, or review metadata.
    - Must NEVER expose historical provenance answer keys or solver conclusions.
    """
    if atom.atom_type != AtomType.QUESTION or atom.question is None:
        raise ValueError(
            f"Cannot create BlindSolverPackage for non-question atom '{atom.atom_id}' "
            f"(atom_type={atom.atom_type})."
        )

    q = atom.question
    options_dump = [o.model_dump(mode="json") for o in q.options]
    fig_dump = [f.model_dump(mode="json") for f in atom.figure_refs]
    pkg_hash = compute_blind_package_hash(q.statement, options_dump, fig_dump)

    package = BlindSolverPackage(
        package_id=f"pkg-{atom.atom_id}-{uuid.uuid4().hex[:8]}",
        atom_id=atom.atom_id,
        atom_version=atom.atom_version,
        content_hash=atom.content_hash,
        blind_package_hash=pkg_hash,
        statement=q.statement,
        options=list(q.options),
        figure_refs=list(atom.figure_refs),
        difficulty=q.difficulty,
        concepts=list(q.concepts),
        exam_metadata=q.exam_metadata,
        context_notes=None,
    )

    return package


def audit_blind_package_for_leaks(package: BlindSolverPackage) -> Dict[str, Any]:
    """Audits a BlindSolverPackage for any accidental leakage of answer keys or solutions.
    
    Returns a dict with 'has_leak': bool and 'leaks': List[str].
    """
    leaks = []
    pkg_dict = package.model_dump()

    # Forbidden field keys that should never exist at the root
    forbidden_keys = [
        "source_claimed_answer",
        "verified_answer",
        "source_solution",
        "solution_methods",
        "answer",
        "verification_status",
        "verdict",
        "confidence",
        "adjudication",
        "solver_runs",
    ]

    for key in forbidden_keys:
        if key in pkg_dict and pkg_dict[key] is not None:
            leaks.append(f"Forbidden field '{key}' found in root of BlindSolverPackage.")

    return {
        "has_leak": len(leaks) > 0,
        "leaks": leaks,
    }
