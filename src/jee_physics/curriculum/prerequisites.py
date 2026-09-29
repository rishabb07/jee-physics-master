import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from jee_physics.models.curriculum import (
    CurriculumNode,
    CurriculumNodeType,
    ExamTargetLevel,
    PedagogicalRole,
    PrerequisiteEdge,
    PrerequisiteRelationshipType,
)


class CurriculumPrerequisiteDAG:
    """Directed Acyclic Graph (DAG) modeling pedagogical prerequisites across curriculum units.
    
    Ensures that learning paths respect strict conceptual, mathematical, and intuitive dependencies
    without cycles, self-loops, or impossible progression directions.
    """

    def __init__(
        self,
        graph_id: str = "jee-physics-pilot-curriculum-dag",
        scope: str = "PILOT",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.graph_id = graph_id
        self.scope = scope
        self.metadata = metadata or {
            "pilot_scope": True,
            "description": (
                "Phase 7 Pilot Core Curriculum Graph covering foundational mechanics trunk and the 4 pilot "
                "chapters (rotational-motion, thermodynamics, current-electricity, ray-optics). "
                "Downstream systems must NOT treat this as the full 30-chapter global graph."
            ),
            "covered_pilot_chapters": [
                "rotational-motion",
                "thermodynamics",
                "current-electricity",
                "ray-optics",
            ],
            "covered_curriculum_units": 22,
            "total_syllabus_chapters": 30,
            "omitted_syllabus_chapters_count": 26,
            "omission_classification": "PILOT_SCOPE_LIMITATION",
            "authorship": "PROJECT_ENGINEERING_DESIGN",
            "author_notes": (
                "Constructed by project curriculum engineers based on standard IIT-JEE pedagogical "
                "progressions to serve as an architectural constraint for subagent chapter planning."
            ),
        }
        self.nodes: Dict[str, CurriculumNode] = {}
        self.edges: List[PrerequisiteEdge] = []
        self._adj_forward: Dict[str, List[PrerequisiteEdge]] = defaultdict(list)   # prereq -> dependents
        self._adj_backward: Dict[str, List[PrerequisiteEdge]] = defaultdict(list)  # dependent -> prereqs

    def add_node(self, node: CurriculumNode) -> None:
        """Adds a curriculum node to the graph."""
        self.nodes[node.curriculum_id] = node

    def add_edge(self, edge: PrerequisiteEdge) -> None:
        """Adds a directed prerequisite edge: from_node_id (prerequisite) -> to_node_id (dependent)."""
        self.edges.append(edge)
        self._adj_forward[edge.from_node_id].append(edge)
        self._adj_backward[edge.to_node_id].append(edge)

    def validate_graph(self) -> List[str]:
        """Performs rigorous structural validation on the graph.
        
        Returns a list of error strings. Empty list indicates graph is completely valid.
        """
        errors: List[str] = []

        # 1. Missing node references in edges
        for idx, edge in enumerate(self.edges):
            if edge.from_node_id not in self.nodes:
                errors.append(
                    f"MISSING_NODE_REFERENCE: Edge {idx} references non-existent prerequisite from_node_id='{edge.from_node_id}'"
                )
            if edge.to_node_id not in self.nodes:
                errors.append(
                    f"MISSING_NODE_REFERENCE: Edge {idx} references non-existent dependent to_node_id='{edge.to_node_id}'"
                )

        # 2. Self-loop detection
        for idx, edge in enumerate(self.edges):
            if edge.from_node_id == edge.to_node_id:
                errors.append(
                    f"SELF_PREREQUISITE_LOOP: Node '{edge.from_node_id}' cannot be a prerequisite of itself"
                )

        # 3. Impossible pedagogical direction checks
        # e.g. An Olympiad extension or Advanced Synthesis node cannot be a prerequisite for a Foundation Concept
        for edge in self.edges:
            if edge.from_node_id in self.nodes and edge.to_node_id in self.nodes:
                prereq_node = self.nodes[edge.from_node_id]
                dep_node = self.nodes[edge.to_node_id]

                if (
                    prereq_node.pedagogical_role == PedagogicalRole.ADVANCED_SYNTHESIS
                    and dep_node.pedagogical_role == PedagogicalRole.FOUNDATION_CONCEPT
                ):
                    errors.append(
                        f"IMPOSSIBLE_PREREQUISITE_DIRECTION: Advanced synthesis node '{prereq_node.curriculum_id}' "
                        f"cannot be a prerequisite for foundation concept '{dep_node.curriculum_id}'"
                    )

                if (
                    ExamTargetLevel.OLYMPIAD_EXTENSION in prereq_node.target_exam_levels
                    and ExamTargetLevel.JEE_MAIN in dep_node.target_exam_levels
                    and ExamTargetLevel.OLYMPIAD_EXTENSION not in dep_node.target_exam_levels
                    and edge.relationship_type == PrerequisiteRelationshipType.STRICT_CONCEPTUAL
                ):
                    errors.append(
                        f"IMPOSSIBLE_PREREQUISITE_DIRECTION: Olympiad extension '{prereq_node.curriculum_id}' "
                        f"cannot be a strict conceptual prerequisite for JEE Main foundation '{dep_node.curriculum_id}'"
                    )

        # 4. Cycle detection using Kahn's algorithm
        in_degrees: Dict[str, int] = {nid: 0 for nid in self.nodes}
        for edge in self.edges:
            if edge.to_node_id in in_degrees:
                in_degrees[edge.to_node_id] += 1

        queue = deque([nid for nid, deg in in_degrees.items() if deg == 0])
        visited_count = 0

        while queue:
            curr = queue.popleft()
            visited_count += 1
            for edge in self._adj_forward.get(curr, []):
                dep = edge.to_node_id
                if dep in in_degrees:
                    in_degrees[dep] -= 1
                    if in_degrees[dep] == 0:
                        queue.append(dep)

        if visited_count < len(self.nodes):
            # Identify the cycle components
            cycle_nodes = [nid for nid, deg in in_degrees.items() if deg > 0]
            errors.append(
                f"PREREQUISITE_CYCLE: Detected cycle among {len(cycle_nodes)} nodes: {cycle_nodes[:5]}"
            )

        return errors

    def topological_sort(self) -> List[str]:
        """Returns node IDs in deterministic topological order (prerequisites before dependents).
        
        Raises ValueError if a cycle exists.
        Uses (recommended_learning_position, curriculum_id) as stable tie-breaker.
        """
        errors = self.validate_graph()
        cycle_errors = [e for e in errors if "PREREQUISITE_CYCLE" in e or "SELF_PREREQUISITE_LOOP" in e]
        if cycle_errors:
            raise ValueError(f"Cannot sort DAG with cycles: {cycle_errors}")

        in_degrees: Dict[str, int] = {nid: 0 for nid in self.nodes}
        for edge in self.edges:
            if edge.to_node_id in in_degrees:
                in_degrees[edge.to_node_id] += 1

        # Priority queue / sorted list for deterministic tie breaking
        available = [nid for nid, deg in in_degrees.items() if deg == 0]
        # Sort key: recommended_learning_position ascending, then curriculum_id alphabetically
        available.sort(key=lambda nid: (self.nodes[nid].recommended_learning_position, nid))

        result: List[str] = []
        while available:
            curr = available.pop(0)
            result.append(curr)

            newly_ready = []
            for edge in self._adj_forward.get(curr, []):
                dep = edge.to_node_id
                if dep in in_degrees:
                    in_degrees[dep] -= 1
                    if in_degrees[dep] == 0:
                        newly_ready.append(dep)

            # Insert newly ready maintaining sort order
            available.extend(newly_ready)
            available.sort(key=lambda nid: (self.nodes[nid].recommended_learning_position, nid))

        return result

    def get_direct_prerequisites(self, node_id: str) -> List[str]:
        """Returns direct prerequisite node IDs for the given node."""
        return [edge.from_node_id for edge in self._adj_backward.get(node_id, [])]

    def get_direct_dependents(self, node_id: str) -> List[str]:
        """Returns direct dependent node IDs for the given node."""
        return [edge.to_node_id for edge in self._adj_forward.get(node_id, [])]

    def get_all_prerequisites_transitive(self, node_id: str) -> Set[str]:
        """Returns all transitive prerequisite node IDs via BFS."""
        visited: Set[str] = set()
        queue = deque([node_id])
        while queue:
            curr = queue.popleft()
            for edge in self._adj_backward.get(curr, []):
                p = edge.from_node_id
                if p not in visited:
                    visited.add(p)
                    queue.append(p)
        return visited

    def get_all_dependents_transitive(self, node_id: str) -> Set[str]:
        """Returns all transitive dependent node IDs via BFS."""
        visited: Set[str] = set()
        queue = deque([node_id])
        while queue:
            curr = queue.popleft()
            for edge in self._adj_forward.get(curr, []):
                d = edge.to_node_id
                if d not in visited:
                    visited.add(d)
                    queue.append(d)
        return visited

    def to_dict(self) -> Dict[str, Any]:
        """Serializes DAG to a dictionary."""
        return {
            "graph_id": self.graph_id,
            "scope": self.scope,
            "metadata": self.metadata,
            "nodes": {nid: node.model_dump(mode="json") for nid, node in self.nodes.items()},
            "edges": [edge.model_dump(mode="json") for edge in self.edges],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CurriculumPrerequisiteDAG":
        """Deserializes DAG from a dictionary."""
        dag = cls(
            graph_id=data.get("graph_id", "jee-physics-pilot-curriculum-dag"),
            scope=data.get("scope", "PILOT"),
            metadata=data.get("metadata", None),
        )
        for nid, node_data in data.get("nodes", {}).items():
            dag.add_node(CurriculumNode.model_validate(node_data))
        for edge_data in data.get("edges", []):
            dag.add_edge(PrerequisiteEdge.model_validate(edge_data))
        return dag

    def save_json(self, path: Path) -> None:
        """Saves DAG to a JSON file safely."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)

    @classmethod
    def load_json(cls, path: Path) -> "CurriculumPrerequisiteDAG":
        """Loads DAG from a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
