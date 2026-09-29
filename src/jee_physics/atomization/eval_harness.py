from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import AtomType


@dataclass
class ExtractionEvalResult:
    passed: bool
    checks_run: int = 0
    failures: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


def evaluate_staged_extraction(
    atoms: List[KnowledgeAtom],
    page_start: int,
    page_end: int,
    expected_question_range: Optional[Tuple[int, int]] = None,
    require_diagrams_on_pages: Optional[List[int]] = None,
) -> ExtractionEvalResult:
    """Evaluates extraction quality against structural and provenance invariants.
    
    This is an evaluation harness checking invariants, not a physics truth oracle.
    """
    failures: List[str] = []
    checks = 0

    # 1. Page range accounting
    checks += 1
    covered_pages: Set[int] = set()
    for a in atoms:
        for p in a.provenance:
            if p.page_start:
                covered_pages.add(p.page_start)
            if p.page_end:
                covered_pages.add(p.page_end)

    for p in range(page_start, page_end + 1):
        if p not in covered_pages:
            failures.append(f"Page accounting gap: page {p} has no extracted atoms.")

    # 2. Page bounds check
    checks += 1
    for a in atoms:
        for p in a.provenance:
            if p.page_start and (p.page_start < page_start or p.page_start > page_end):
                failures.append(
                    f"Atom '{a.atom_id}' has out-of-bounds page_start {p.page_start} (expected {page_start}..{page_end})."
                )

    # 3. Non-empty mathematical content
    checks += 1
    for a in atoms:
        if a.atom_type == AtomType.QUESTION and a.question:
            if not a.question.statement.strip():
                failures.append(f"Question atom '{a.atom_id}' has empty statement.")
        elif a.atom_type == AtomType.FORMULA and a.formula:
            if not a.formula.formula_latex.strip():
                failures.append(f"Formula atom '{a.atom_id}' has empty formula_latex.")

    # 4. Question count within expected range
    question_count = sum(1 for a in atoms if a.atom_type == AtomType.QUESTION)
    if expected_question_range:
        checks += 1
        min_q, max_q = expected_question_range
        if question_count < min_q or question_count > max_q:
            failures.append(
                f"Question count {question_count} outside expected range [{min_q}, {max_q}]."
            )

    # 5. Diagram presence check
    if require_diagrams_on_pages:
        checks += 1
        diagram_pages: Set[int] = set()
        for a in atoms:
            if a.figure_refs:
                for p in a.provenance:
                    if p.page_start:
                        diagram_pages.add(p.page_start)
        for req_p in require_diagrams_on_pages:
            if req_p not in diagram_pages:
                failures.append(f"Expected diagram reference on page {req_p}, but none was found.")

    passed = len(failures) == 0
    metrics = {
        "total_atoms": len(atoms),
        "questions_count": question_count,
        "covered_pages": sorted(list(covered_pages)),
        "page_range": [page_start, page_end],
    }

    return ExtractionEvalResult(
        passed=passed,
        checks_run=checks,
        failures=failures,
        metrics=metrics,
    )
