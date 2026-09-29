from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from jee_physics.core.hasher import compute_content_hash
from jee_physics.core.ids import generate_atom_id
from jee_physics.models.atom import (
    ExamMetadata,
    FigureReference,
    FormulaPayload,
    KnowledgeAtom,
    MisconceptionPayload,
    QuestionOption,
    QuestionPayload,
    SolutionMethod,
    SolvedExamplePayload,
    TaxonomyReference,
)
from jee_physics.models.enums import AtomStatus, AtomType, DifficultyLevel
from jee_physics.models.provenance import ProvenanceRecord


def build_staged_question_atom(
    chapter_id: str,
    topic_id: str,
    statement: str,
    options: List[Dict[str, str]],
    answer: Optional[str],
    difficulty: DifficultyLevel,
    source_id: str,
    file_name: str,
    page_number: int,
    source_locator: str,
    confidence: float = 1.0,
    exam_metadata: Optional[Dict[str, Any]] = None,
    solution_methods: Optional[List[Dict[str, Any]]] = None,
    concepts: Optional[List[str]] = None,
    figure_refs: Optional[List[Dict[str, Any]]] = None,
    insight: Optional[str] = None,
    subtopic_id: Optional[str] = None,
    title: Optional[str] = None,
) -> KnowledgeAtom:
    """Helper to build a strictly validated question KnowledgeAtom for staging."""
    opts = [QuestionOption(id=opt["id"], text=opt["text"]) for opt in options]
    sol_methods = []
    if solution_methods:
        for sm in solution_methods:
            sol_methods.append(
                SolutionMethod(
                    method_name=sm.get("method_name", "Standard Solution"),
                    steps=sm["steps"],
                    source_attributed=sm.get("source_attributed", True),
                )
            )

    exam_meta = None
    if exam_metadata:
        exam_meta = ExamMetadata(
            exam=exam_metadata.get("exam"),
            year=exam_metadata.get("year"),
            paper=exam_metadata.get("paper"),
            question_number=exam_metadata.get("question_number"),
        )

    q_payload = QuestionPayload(
        statement=statement,
        options=opts,
        answer=answer,
        solution_methods=sol_methods,
        difficulty=difficulty,
        exam_metadata=exam_meta,
        concepts=concepts or [],
    )

    prov = ProvenanceRecord(
        source_id=source_id,
        file_name=file_name,
        page_start=page_number,
        page_end=page_number,
        source_locator=source_locator,
    )

    atom_title = title or f"Question on {topic_id.replace('-', ' ').title()}"
    atom_id = generate_atom_id(chapter_id, AtomType.QUESTION, statement)
    content_hash = compute_content_hash(statement + "".join(opt["text"] for opt in options))

    figs = [FigureReference(**f) for f in (figure_refs or [])]

    return KnowledgeAtom(
        atom_id=atom_id,
        schema_version="1.0.0",
        atom_version=1,
        active=True,
        atom_type=AtomType.QUESTION,
        title=atom_title,
        taxonomy=TaxonomyReference(chapter_id=chapter_id, topic_id=topic_id, subtopic_id=subtopic_id),
        provenance=[prov],
        confidence=confidence,
        verification_status=AtomStatus.STAGED,
        content_hash=content_hash,
        question=q_payload,
        figure_refs=figs,
        insight=insight,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def build_staged_theory_atom(
    chapter_id: str,
    topic_id: str,
    title: str,
    content: str,
    source_id: str,
    file_name: str,
    page_number: int,
    source_locator: str,
    confidence: float = 1.0,
    insight: Optional[str] = None,
    subtopic_id: Optional[str] = None,
) -> KnowledgeAtom:
    """Helper to build a strictly validated theory KnowledgeAtom for staging."""
    prov = ProvenanceRecord(
        source_id=source_id,
        file_name=file_name,
        page_start=page_number,
        page_end=page_number,
        source_locator=source_locator,
    )

    atom_id = generate_atom_id(chapter_id, AtomType.THEORY, title + " " + content[:60])
    content_hash = compute_content_hash(content)

    return KnowledgeAtom(
        atom_id=atom_id,
        schema_version="1.0.0",
        atom_version=1,
        active=True,
        atom_type=AtomType.THEORY,
        title=title,
        taxonomy=TaxonomyReference(chapter_id=chapter_id, topic_id=topic_id, subtopic_id=subtopic_id),
        provenance=[prov],
        confidence=confidence,
        verification_status=AtomStatus.STAGED,
        content_hash=content_hash,
        content=content,
        insight=insight,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
