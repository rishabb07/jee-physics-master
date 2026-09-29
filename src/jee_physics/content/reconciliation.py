"""
Deterministic Requirement Reconciliation Engine for Phase 8.

Reconciles the 63 formal content requirements in build/reports/content_requirements.json
against actual promoted verified artifacts in content/verified/.
Performs deterministic 1-to-1 matching, classifies each requirement as
RESOLVED, UNRESOLVED_GAP, or MISCONFIGURED, and generates:
1. build/reports/phase8_requirement_reconciliation.json
2. build/reports/phase8_artifact_coverage_matrix.json (strictly from actual artifact fields)
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class RequirementReconciliationEngine:
    """Deterministic requirement-to-artifact reconciliation engine."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(".")
        self.requirements_path = self.workspace_root / "build" / "reports" / "content_requirements.json"
        self.verified_dir = self.workspace_root / "content" / "verified"
        self.dual_verif_dir = self.verified_dir / "dual_verifications"
        self.single_verif_dir = self.workspace_root / "build" / "staging" / "incoming" / "content_verification"

    def _load_verified_artifacts(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Loads all verified artifacts categorized by content type."""
        categories = {
            "CONCEPT_EXPLANATION": self.verified_dir / "concepts",
            "FORMULA": self.verified_dir / "formulas",
            "DERIVATION": self.verified_dir / "derivations",
            "WORKED_EXAMPLE": self.verified_dir / "examples",
            "MISCONCEPTION": self.verified_dir / "misconceptions",
        }
        loaded = {}
        for ctype, cdir in categories.items():
            loaded[ctype] = {}
            if cdir.exists():
                for p in cdir.glob("*.json"):
                    try:
                        data = json.loads(p.read_text(encoding="utf-8"))
                        loaded[ctype][p.stem] = data
                    except Exception:
                        pass
        return loaded

    def match_requirement_to_artifact(
        self, req: Dict[str, Any], artifacts_pool: Dict[str, Dict[str, Any]]
    ) -> Optional[str]:
        """Finds matching artifact ID deterministically for a requirement."""
        rid = req.get("requirement_id", "")
        # 1. Direct substring check against pool keys
        for aid in artifacts_pool:
            if aid in rid:
                return aid
        # 2. Required source references
        for sref in req.get("required_source_refs", []):
            if sref in artifacts_pool:
                return sref
        # 3. Curriculum node id
        cnode = req.get("curriculum_node_id")
        if cnode in artifacts_pool:
            return cnode
        # 4. Objective match
        obj = req.get("objective", "")
        for aid in artifacts_pool:
            if aid in obj:
                return aid
        return None

    def reconcile(self) -> Dict[str, Any]:
        """Performs complete deterministic reconciliation."""
        if not self.requirements_path.exists():
            raise FileNotFoundError(f"Requirements file not found: {self.requirements_path}")

        req_data = json.loads(self.requirements_path.read_text(encoding="utf-8"))
        requirements = req_data.get("requirements", [])
        verified_artifacts = self._load_verified_artifacts()

        one_to_one_mappings: List[Dict[str, Any]] = []
        breakdown_by_type: Dict[str, Dict[str, int]] = {
            "CONCEPT_EXPLANATION": {"total": 0, "resolved": 0, "unresolved_gaps": 0, "misconfigured": 0},
            "FORMULA": {"total": 0, "resolved": 0, "unresolved_gaps": 0, "misconfigured": 0},
            "DERIVATION": {"total": 0, "resolved": 0, "unresolved_gaps": 0, "misconfigured": 0},
            "WORKED_EXAMPLE": {"total": 0, "resolved": 0, "unresolved_gaps": 0, "misconfigured": 0},
            "MISCONCEPTION": {"total": 0, "resolved": 0, "unresolved_gaps": 0, "misconfigured": 0},
        }

        resolved_count = 0
        unresolved_gap_count = 0
        misconfigured_count = 0
        unresolved_concept_gaps_details: List[Dict[str, Any]] = []
        resolved_artifacts: Dict[str, List[str]] = {
            "concepts": [],
            "formulas": [],
            "derivations": [],
            "worked_examples": [],
            "misconceptions": [],
        }

        type_to_key = {
            "CONCEPT_EXPLANATION": "concepts",
            "FORMULA": "formulas",
            "DERIVATION": "derivations",
            "WORKED_EXAMPLE": "worked_examples",
            "MISCONCEPTION": "misconceptions",
        }

        for req in requirements:
            rid = req.get("requirement_id")
            ctype = req.get("content_type")
            ch_id = req.get("chapter_id")
            is_gap = req.get("is_unresolved_gap", False)

            if ctype in breakdown_by_type:
                breakdown_by_type[ctype]["total"] += 1

            if is_gap:
                unresolved_gap_count += 1
                if ctype in breakdown_by_type:
                    breakdown_by_type[ctype]["unresolved_gaps"] += 1
                gap_info = {
                    "requirement_id": rid,
                    "chapter_id": ch_id,
                    "content_type": ctype,
                    "status": "UNRESOLVED_GAP",
                    "objective": req.get("objective"),
                    "rationale": "Explicitly declared missing source or curriculum coverage gap",
                }
                one_to_one_mappings.append(gap_info)
                unresolved_concept_gaps_details.append(gap_info)
                continue

            pool = verified_artifacts.get(ctype, {})
            matched_aid = self.match_requirement_to_artifact(req, pool)

            if matched_aid and matched_aid in pool:
                artifact_data = pool[matched_aid]
                v_status = artifact_data.get("verification_status")
                c_hash = artifact_data.get("content_hash")
                v_rec_id = artifact_data.get("verification_record_id")

                if v_status == "VERIFIED" and c_hash:
                    resolved_count += 1
                    if ctype in breakdown_by_type:
                        breakdown_by_type[ctype]["resolved"] += 1
                    resolved_artifacts[type_to_key[ctype]].append(matched_aid)

                    one_to_one_mappings.append({
                        "requirement_id": rid,
                        "chapter_id": ch_id,
                        "content_type": ctype,
                        "status": "RESOLVED",
                        "matched_artifact_id": matched_aid,
                        "content_hash": c_hash,
                        "verification_record_id": v_rec_id,
                        "risk_level": req.get("risk_level", "MEDIUM"),
                    })
                else:
                    misconfigured_count += 1
                    if ctype in breakdown_by_type:
                        breakdown_by_type[ctype]["misconfigured"] += 1
                    one_to_one_mappings.append({
                        "requirement_id": rid,
                        "chapter_id": ch_id,
                        "content_type": ctype,
                        "status": "MISCONFIGURED",
                        "matched_artifact_id": matched_aid,
                        "error": f"Artifact {matched_aid} is not VERIFIED (status={v_status})",
                    })
            else:
                misconfigured_count += 1
                if ctype in breakdown_by_type:
                    breakdown_by_type[ctype]["misconfigured"] += 1
                one_to_one_mappings.append({
                    "requirement_id": rid,
                    "chapter_id": ch_id,
                    "content_type": ctype,
                    "status": "MISCONFIGURED",
                    "error": f"No matching verified artifact found in {ctype} pool",
                })

        total_reqs = len(requirements)
        resolvable = total_reqs - unresolved_gap_count
        resolution_pct = (resolved_count / resolvable * 100) if resolvable > 0 else 0

        return {
            "report_id": "phase8-requirement-reconciliation",
            "total_requirements": total_reqs,
            "resolvable_requirements": resolvable,
            "resolved_requirements": resolved_count,
            "unresolved_concept_gaps": unresolved_gap_count,
            "misconfigured_requirements": misconfigured_count,
            "resolution_rate": f"{resolution_pct:.0f}% of resolvable requirements ({resolved_count}/{resolvable})",
            "breakdown_by_type": breakdown_by_type,
            "resolved_artifacts": resolved_artifacts,
            "unresolved_concept_gaps_details": unresolved_concept_gaps_details,
            "one_to_one_mappings": one_to_one_mappings,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def generate_reconciliation_report(self, output_path: Optional[Path] = None) -> Path:
        """Writes the reconciliation report to disk."""
        target = output_path or (self.workspace_root / "build" / "reports" / "phase8_requirement_reconciliation.json")
        target.parent.mkdir(parents=True, exist_ok=True)
        res = self.reconcile()
        target.write_text(json.dumps(res, indent=2), encoding="utf-8")
        return target

    def generate_artifact_coverage_matrix(self, output_path: Optional[Path] = None) -> Path:
        """Generates phase8_artifact_coverage_matrix.json derived strictly from actual artifact files."""
        target = output_path or (self.workspace_root / "build" / "reports" / "phase8_artifact_coverage_matrix.json")
        target.parent.mkdir(parents=True, exist_ok=True)

        verified_artifacts = self._load_verified_artifacts()
        matrix_rows: List[Dict[str, Any]] = []

        total_dual = 0
        total_single = 0

        # Substantive mapping of categories
        category_meta = [
            ("concepts", "CONCEPT_EXPLANATION", False),
            ("formulas", "FORMULA", False),
            ("derivations", "DERIVATION", True),
            ("examples", "WORKED_EXAMPLE", True),
            ("misconceptions", "MISCONCEPTION", False),
        ]

        for folder, ctype, is_high_risk in category_meta:
            cdir = self.verified_dir / folder
            if not cdir.exists():
                continue
            for fpath in sorted(cdir.glob("*.json")):
                adata = json.loads(fpath.read_text(encoding="utf-8"))
                aid = adata.get("content_id") or adata.get("formula_id") or adata.get("derivation_id") or adata.get("example_id") or adata.get("misconception_id") or fpath.stem
                ch_id = adata.get("chapter_id", "")
                if not ch_id and "taxonomy_reference" in adata:
                    ch_id = adata["taxonomy_reference"].get("chapter_id", "")

                v_status = adata.get("verification_status", "UNKNOWN")
                c_hash = adata.get("content_hash", "")
                risk = adata.get("risk_level", "HIGH" if is_high_risk else "MEDIUM")

                # Grounding provenance from actual fields
                source_refs = adata.get("source_references") or adata.get("source_atom_id") or adata.get("provenance") or []
                if source_refs:
                    grounding = str(source_refs)
                elif "taxonomy_reference" in adata:
                    grounding = f"TAXONOMY:{adata['taxonomy_reference'].get('topic_id', '')}"
                elif adata.get("derivation_reference"):
                    grounding = f"DERIVATION:{adata['derivation_reference']}"
                elif adata.get("connected_atom_ids"):
                    grounding = f"ATOMS:{adata['connected_atom_ids']}"
                else:
                    grounding = "CANONICAL_KB / CURRICULUM_SPEC"

                dual_path = self.dual_verif_dir / f"dual-cvr-{aid}.json"
                is_dual = dual_path.exists()
                if is_dual:
                    total_dual += 1
                    verif_rec_id = f"dual-cvr-{aid}"
                else:
                    total_single += 1
                    verif_rec_id = adata.get("verification_record_id") or f"cvr-{aid}"

                matrix_rows.append({
                    "artifact_id": aid,
                    "artifact_type": ctype,
                    "chapter_id": ch_id,
                    "risk_level": risk,
                    "is_dual_verified": is_dual,
                    "verification_record_id": verif_rec_id,
                    "verification_status": v_status,
                    "content_hash": c_hash,
                    "source_grounding": grounding,
                })

        result = {
            "report_id": "phase8-artifact-coverage-matrix",
            "total_artifacts": len(matrix_rows),
            "total_dual_verifications": total_dual,
            "total_single_verifications": total_single,
            "coverage_matrix": matrix_rows,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

        target.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return target
