from typing import Any, Dict
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import DifficultyLevel


def is_high_risk_question(atom: KnowledgeAtom, config: Dict[str, Any] | None = None) -> bool:
    """Determines whether a question atom requires enhanced verification according to risk policy.
    
    High Risk Triggers:
    - Difficulty L4 or L5 (Advanced multi-concept / Olympiad)
    - Presence of complex diagrams or multiple figures
    - Mock test questions (exam_metadata present)
    - Low or medium extraction confidence (< 0.95)
    - Explicit ambiguity notes in provenance
    """
    if atom.question is None:
        return False

    q = atom.question

    # 1. Difficulty Level
    if q.difficulty in [DifficultyLevel.L4, DifficultyLevel.L5]:
        return True

    # 2. Complex figures
    if len(atom.figure_refs) > 1:
        return True

    # 3. Extraction confidence
    if atom.confidence < 0.95:
        return True

    # 4. Mock test selection
    if q.exam_metadata and q.exam_metadata.exam:
        return True

    # 5. Provenance extraction flags
    for prov in atom.provenance:
        meta = prov.extraction_metadata or {}
        if "source_misprint" in meta or "diagram_note" in meta:
            return True

    return False


def get_required_solver_count(atom: KnowledgeAtom, verify_all_pilot: bool = True) -> int:
    """Returns the required number of independent solvers for an atom.
    
    In current Phase 4 pilot, every verified question requires at least 2 independent solvers.
    """
    if verify_all_pilot:
        return 2

    if is_high_risk_question(atom):
        return 2

    return 1
