"""
Pedagogical Dependency Graph and Prerequisite Verifier for Phase 8.

Validates the full pedagogical chain:
concept -> formula -> derivation -> worked_example -> misconception -> question

Enforces:
1. Absence of circular dependencies.
2. Zero dangling references across the chain.
3. Upstream verification invariant: a downstream artifact is only valid if all its
   prerequisites and backing concepts are verified.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from jee_physics.models.content import ContentVerificationStatus


class DependencyEdge(BaseModel):
    """A directed edge in the pedagogical content dependency graph."""
    source_id: str
    source_type: str
    target_id: str
    target_type: str
    relationship: str  # "defines", "derives", "applies", "addresses_pitfall_in", "tests"


class DependencyIssue(BaseModel):
    """An issue detected during dependency graph auditing."""
    issue_type: str  # "CYCLE", "DANGLING_REFERENCE", "UNVERIFIED_UPSTREAM"
    severity: str  # "CRITICAL", "WARNING"
    affected_node: str
    details: str


class DependencyAuditReport(BaseModel):
    """Audit report for content dependency graph."""
    report_id: str
    total_nodes: int
    total_edges: int
    cycles_detected: List[List[str]] = Field(default_factory=list)
    dangling_references: List[str] = Field(default_factory=list)
    unverified_upstream_issues: List[str] = Field(default_factory=list)
    passed: bool
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PedagogicalDependencyAuditor:
    """Audits pedagogical dependencies across all chapters and artifacts."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.verified_dir = workspace_root / "content" / "verified"
        self.staging_dir = workspace_root / "build" / "staging" / "incoming" / "content"
        self.kb_atoms_dir = workspace_root / "kb" / "atoms"
        self.curriculum_dir = workspace_root / "build" / "staging" / "incoming" / "curriculum"

    def _load_json(self, path: Path) -> Optional[Dict[str, Any]]:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def collect_all_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Collects all content items from verified, staging, and kb/atoms."""
        nodes: Dict[str, Dict[str, Any]] = {}

        # 1. KB Atoms
        if self.kb_atoms_dir.exists():
            for p in self.kb_atoms_dir.glob("*.json"):
                data = self._load_json(p)
                if data:
                    nodes[data.get("atom_id", p.stem)] = {
                        "type": "CANONICAL_QUESTION",
                        "status": "VERIFIED",
                        "data": data,
                    }

        # 2. Concepts
        for base in [self.staging_dir, self.verified_dir]:
            cdir = base / "concepts"
            if cdir.exists():
                for p in cdir.glob("*.json"):
                    data = self._load_json(p)
                    if data:
                        cid = data.get("content_id", p.stem)
                        st = data.get("verification_status", "UNVERIFIED")
                        if cid in nodes and nodes[cid]["status"] == "VERIFIED" and st != "VERIFIED":
                            continue
                        nodes[cid] = {
                            "type": "CONCEPT",
                            "status": st,
                            "data": data,
                        }

        # 3. Formulas
        for base in [self.staging_dir, self.verified_dir]:
            fdir = base / "formulas"
            if fdir.exists():
                for p in fdir.glob("*.json"):
                    data = self._load_json(p)
                    if data:
                        fid = data.get("formula_id", p.stem)
                        st = data.get("verification_status", "UNVERIFIED")
                        if fid in nodes and nodes[fid]["status"] == "VERIFIED" and st != "VERIFIED":
                            continue
                        nodes[fid] = {
                            "type": "FORMULA",
                            "status": st,
                            "data": data,
                        }

        # 4. Derivations
        for base in [self.staging_dir, self.verified_dir]:
            ddir = base / "derivations"
            if ddir.exists():
                for p in ddir.glob("*.json"):
                    data = self._load_json(p)
                    if data:
                        did = data.get("derivation_id", p.stem)
                        st = data.get("verification_status", "UNVERIFIED")
                        if did in nodes and nodes[did]["status"] == "VERIFIED" and st != "VERIFIED":
                            continue
                        nodes[did] = {
                            "type": "DERIVATION",
                            "status": st,
                            "data": data,
                        }

        # 5. Worked Examples
        for base in [self.staging_dir, self.verified_dir]:
            edir = base / "examples"
            if edir.exists():
                for p in edir.glob("*.json"):
                    data = self._load_json(p)
                    if data:
                        eid = data.get("example_id", p.stem)
                        st = data.get("verification_status", "UNVERIFIED")
                        if eid in nodes and nodes[eid]["status"] == "VERIFIED" and st != "VERIFIED":
                            continue
                        nodes[eid] = {
                            "type": "WORKED_EXAMPLE",
                            "status": st,
                            "data": data,
                        }

        # 6. Misconceptions
        for base in [self.staging_dir, self.verified_dir]:
            mdir = base / "misconceptions"
            if mdir.exists():
                for p in mdir.glob("*.json"):
                    data = self._load_json(p)
                    if data:
                        mid = data.get("misconception_id", p.stem)
                        st = data.get("verification_status", "UNVERIFIED")
                        if mid in nodes and nodes[mid]["status"] == "VERIFIED" and st != "VERIFIED":
                            continue
                        nodes[mid] = {
                            "type": "MISCONCEPTION",
                            "status": st,
                            "data": data,
                        }

        return nodes

    def build_dependency_graph(self, nodes: Dict[str, Dict[str, Any]]) -> Tuple[List[DependencyEdge], Dict[str, List[str]]]:
        """Constructs edges: concept -> formula -> derivation -> example -> question."""
        edges: List[DependencyEdge] = []
        adj: Dict[str, List[str]] = defaultdict(list)

        for node_id, info in nodes.items():
            ntype = info["type"]
            data = info["data"]

            if ntype == "FORMULA":
                # Formula depends on related concepts
                for c_id in data.get("related_concepts", []):
                    edges.append(DependencyEdge(source_id=c_id, source_type="CONCEPT", target_id=node_id, target_type="FORMULA", relationship="defines"))
                    adj[c_id].append(node_id)

            elif ntype == "DERIVATION":
                # Derivation depends on target formula
                f_id = data.get("target_formula_id")
                if f_id:
                    edges.append(DependencyEdge(source_id=f_id, source_type="FORMULA", target_id=node_id, target_type="DERIVATION", relationship="derives"))
                    adj[f_id].append(node_id)
                # Derivation depends on concepts in starting principles
                for p in data.get("starting_principles", []):
                    for possible_c_id in nodes:
                        if nodes[possible_c_id]["type"] == "CONCEPT" and possible_c_id in p:
                            edges.append(DependencyEdge(source_id=possible_c_id, source_type="CONCEPT", target_id=node_id, target_type="DERIVATION", relationship="grounds"))
                            adj[possible_c_id].append(node_id)

            elif ntype == "WORKED_EXAMPLE":
                # Example depends on governing principles / concepts / formulas
                for principle in data.get("governing_principles", []):
                    for possible_id in nodes:
                        if possible_id in principle:
                            edges.append(DependencyEdge(source_id=possible_id, source_type=nodes[possible_id]["type"], target_id=node_id, target_type="WORKED_EXAMPLE", relationship="applies"))
                            adj[possible_id].append(node_id)

            elif ntype == "MISCONCEPTION":
                c_id = data.get("concept_id")
                if c_id:
                    edges.append(DependencyEdge(source_id=c_id, source_type="CONCEPT", target_id=node_id, target_type="MISCONCEPTION", relationship="addresses_pitfall_in"))
                    adj[c_id].append(node_id)

        return edges, adj

    def detect_cycles(self, adj: Dict[str, List[str]], all_node_ids: Set[str]) -> List[List[str]]:
        """Detects any cycles in the dependency graph using Tarjan's or DFS."""
        visited: Dict[str, int] = {n: 0 for n in all_node_ids}  # 0=unvisited, 1=visiting, 2=visited
        cycles: List[List[str]] = []
        path: List[str] = []

        def dfs(u: str):
            visited[u] = 1
            path.append(u)
            for v in adj.get(u, []):
                if v not in visited:
                    continue
                if visited[v] == 1:
                    idx = path.index(v)
                    cycles.append(list(path[idx:]))
                elif visited[v] == 0:
                    dfs(v)
            path.pop()
            visited[u] = 2

        for n in all_node_ids:
            if visited.get(n) == 0:
                dfs(n)

        return cycles

    def audit_dependencies(self) -> DependencyAuditReport:
        """Executes full dependency audit and returns structured report."""
        nodes = self.collect_all_nodes()
        edges, adj = self.build_dependency_graph(nodes)

        all_node_ids = set(nodes.keys())
        cycles = self.detect_cycles(adj, all_node_ids)

        dangling_refs: List[str] = []
        for edge in edges:
            if edge.source_id not in all_node_ids:
                dangling_refs.append(f"Dangling source '{edge.source_id}' referenced by target '{edge.target_id}'")
            if edge.target_id not in all_node_ids:
                dangling_refs.append(f"Dangling target '{edge.target_id}' referenced by source '{edge.source_id}'")

        unverified_issues: List[str] = []
        for edge in edges:
            if edge.source_id in nodes:
                src_status = nodes[edge.source_id]["status"]
                tgt_status = nodes[edge.target_id]["status"] if edge.target_id in nodes else None
                if tgt_status in ("VERIFIED", ContentVerificationStatus.VERIFIED.value) and src_status not in ("VERIFIED", ContentVerificationStatus.VERIFIED.value):
                    unverified_issues.append(
                        f"Downstream node '{edge.target_id}' marked VERIFIED but upstream prerequisite '{edge.source_id}' is '{src_status}'"
                    )

        passed = (len(cycles) == 0 and len(dangling_refs) == 0 and len(unverified_issues) == 0)

        rep = DependencyAuditReport(
            report_id="pedagogical-dependency-audit-phase8",
            total_nodes=len(nodes),
            total_edges=len(edges),
            cycles_detected=cycles,
            dangling_references=dangling_refs,
            unverified_upstream_issues=unverified_issues,
            passed=passed,
        )

        # Write report to build/reports/
        rep_dir = self.workspace_root / "build" / "reports"
        rep_dir.mkdir(parents=True, exist_ok=True)
        with open(rep_dir / "pedagogical_dependency_report.json", "w", encoding="utf-8") as f:
            json.dump(rep.model_dump(mode="json"), f, indent=2)

        return rep
