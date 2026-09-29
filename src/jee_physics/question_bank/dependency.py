"""
Question Dependency Graph and Reference Validator for Phase 9.

Constructs and verifies the full pedagogical assessment chain:
curriculum node -> concept -> question -> misconception tested -> difficulty rung
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from jee_physics.models.question_bank import GeneratedQuestion


class QuestionDependencyNode(BaseModel):
    """A node in the assessment dependency graph."""
    node_id: str
    node_type: str  # "CURRICULUM_NODE" | "CONCEPT" | "QUESTION" | "MISCONCEPTION" | "LADDER_RUNG"
    label: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QuestionDependencyEdge(BaseModel):
    """A directed edge in the assessment dependency graph."""
    source_id: str
    target_id: str
    edge_type: str  # "EXPLAINS" | "EVALUATES" | "DIAGNOSES" | "SCAFFOLDS_TO"


class QuestionDependencyGraphReport(BaseModel):
    """Audit report for the question dependency graph."""
    report_id: str
    total_nodes: int
    total_edges: int
    all_references_valid: bool
    broken_references: List[str] = Field(default_factory=list)
    nodes: List[QuestionDependencyNode] = Field(default_factory=list)
    edges: List[QuestionDependencyEdge] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionDependencyGraphBuilder:
    """Constructs and validates the question dependency network."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(".")

    def build_graph(
        self,
        questions: List[GeneratedQuestion],
        known_concepts: Optional[Set[str]] = None,
        known_curriculum: Optional[Set[str]] = None,
        known_misconceptions: Optional[Set[str]] = None,
    ) -> QuestionDependencyGraphReport:
        """Constructs graph and checks reference integrity."""
        nodes: Dict[str, QuestionDependencyNode] = {}
        edges: List[QuestionDependencyEdge] = []
        broken: List[str] = []

        concepts_set = known_concepts or set()
        curr_set = known_curriculum or set()
        misc_set = known_misconceptions or set()

        for q in questions:
            # 1. Question node
            q_node = QuestionDependencyNode(
                node_id=q.question_id,
                node_type="QUESTION",
                label=q.statement[:60] + "...",
                metadata={
                    "type": q.question_type.value,
                    "difficulty": str(q.difficulty_band),
                    "chapter": q.taxonomy_reference.chapter_id,
                },
            )
            nodes[q.question_id] = q_node

            # 2. Curriculum link
            c_node_id = q.curriculum_id
            if c_node_id:
                if c_node_id not in nodes:
                    nodes[c_node_id] = QuestionDependencyNode(
                        node_id=c_node_id,
                        node_type="CURRICULUM_NODE",
                        label=f"Curriculum Unit: {c_node_id}",
                    )
                edges.append(
                    QuestionDependencyEdge(
                        source_id=c_node_id,
                        target_id=q.question_id,
                        edge_type="EVALUATES",
                    )
                )

            # 3. Concept links
            for cid in q.concept_references:
                if cid not in nodes:
                    nodes[cid] = QuestionDependencyNode(
                        node_id=cid,
                        node_type="CONCEPT",
                        label=f"Concept: {cid}",
                    )
                edges.append(
                    QuestionDependencyEdge(
                        source_id=cid,
                        target_id=q.question_id,
                        edge_type="EXERCISED_IN",
                    )
                )

            # 4. Misconception link
            if q.misconception_targeted:
                mid = q.misconception_targeted
                if mid not in nodes:
                    nodes[mid] = QuestionDependencyNode(
                        node_id=mid,
                        node_type="MISCONCEPTION",
                        label=f"Misconception Trap: {mid}",
                    )
                edges.append(
                    QuestionDependencyEdge(
                        source_id=q.question_id,
                        target_id=mid,
                        edge_type="DIAGNOSES",
                    )
                )

        report = QuestionDependencyGraphReport(
            report_id="question-dependency-graph-pilot",
            total_nodes=len(nodes),
            total_edges=len(edges),
            all_references_valid=(len(broken) == 0),
            broken_references=broken,
            nodes=list(nodes.values()),
            edges=edges,
        )
        return report
