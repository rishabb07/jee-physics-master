from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from jee_physics.dedup.normalizer import compute_normalized_fingerprint
from jee_physics.models.atom import KnowledgeAtom, SolutionMethod
from jee_physics.models.enums import AtomStatus
from jee_physics.models.dedup import (
    CanonicalMapping,
    DedupAction,
    DedupAuditJournalRecord,
    DedupCandidate,
    DedupCluster,
    DedupDecision,
    DedupDecisionClass,
    PreservedProvenance,
    PreservedSolutionMethod,
)
from jee_physics.storage.io import safe_write_json, safe_write_jsonl


PROHIBITED_CANONICAL_MARKERS = [
    "variant",
    "test",
    "fixture",
    "synthetic",
    "ambiguous",
    "conflict",
    "dummy",
    "multimethod",
    "mock-synth",
]


def validate_canonical_kb_storage_integrity(
    kb_atoms_dir: Optional[Path] = None,
    registry_dir: Optional[Path] = None,
) -> List[str]:
    """Formal architecture invariant validator: kb/atoms/ contains canonical source-of-truth knowledge ONLY.
    
    Rejects:
    - Test fixtures, synthetic variants, temporary experiments
    - Unverified or staged atoms
    - Non-JSON files (except .gitkeep)
    - Records missing provenance or source registry grounding
    """
    errors: List[str] = []
    root = Path.cwd()
    if kb_atoms_dir is None:
        kb_atoms_dir = root / "kb" / "atoms"
    if registry_dir is None:
        registry_dir = root / "sources" / "registry"

    kb_atoms_dir = Path(kb_atoms_dir)
    if not kb_atoms_dir.exists():
        return [f"kb/atoms directory '{kb_atoms_dir}' does not exist."]

    for file_path in sorted(kb_atoms_dir.iterdir()):
        if file_path.name == ".gitkeep":
            continue
        if not file_path.name.endswith(".json"):
            errors.append(f"Non-JSON file found in kb/atoms/: {file_path.name}")
            continue

        lower_name = file_path.stem.lower()
        for marker in PROHIBITED_CANONICAL_MARKERS:
            if marker in lower_name:
                errors.append(
                    f"Prohibited synthetic marker '{marker}' found in canonical atom filename: {file_path.name}"
                )

        try:
            raw_text = file_path.read_text(encoding="utf-8")
            raw_data = json.loads(raw_text)
        except Exception as e:
            errors.append(f"Failed to parse JSON in '{file_path.name}': {e}")
            continue

        if raw_data.get("is_test_fixture") or "fixture_category" in raw_data:
            errors.append(f"Test fixture metadata found in canonical atom: {file_path.name}")

        try:
            atom = KnowledgeAtom.model_validate(raw_data)
        except Exception as e:
            errors.append(f"Schema validation failed for '{file_path.name}': {e}")
            continue

        if atom.verification_status != AtomStatus.VERIFIED:
            errors.append(
                f"Atom '{atom.atom_id}' has non-verified status '{atom.verification_status.value}' in canonical storage."
            )

        if registry_dir.exists():
            for p in atom.provenance:
                reg_file = registry_dir / f"{p.source_id}.json"
                if not reg_file.exists():
                    errors.append(
                        f"Atom '{atom.atom_id}' references unregistered source '{p.source_id}'."
                    )

    return errors


def select_canonical_representative(atoms: List[KnowledgeAtom]) -> KnowledgeAtom:
    """Deterministically select the surviving canonical atom for a cluster.
    
    Deterministic scoring criteria:
    1. Verification state (VERIFIED > PROPOSED > STAGED)
    2. Provenance completeness (number of sources, locators)
    3. Content completeness (solution methods, concepts, diagrams)
    4. Historical stability (lower atom_version / earlier created_at)
    5. Deterministic tie-breaker (alphabetical atom_id)
    """
    if not atoms:
        raise ValueError("Cannot select canonical representative from empty list of atoms.")
    if len(atoms) == 1:
        return atoms[0]

    def _score_atom(a: KnowledgeAtom) -> Tuple[int, int, int, int, str]:
        # Test fixture penalty: Genuine canonical atoms always win over synthetic fixtures
        is_fixture = (
            getattr(a, "is_test_fixture", False)
            or any(m in a.atom_id.lower() for m in PROHIBITED_CANONICAL_MARKERS)
        )
        if is_fixture:
            return (-100000, 0, 0, 0, a.atom_id)

        # 1. Verification status
        status_weight = 0
        if a.verification_status == AtomStatus.VERIFIED:
            status_weight = 1000
        elif a.verification_status == AtomStatus.VALIDATED:
            status_weight = 500
        elif a.verification_status == AtomStatus.STAGED:
            status_weight = 100

        # 2. Provenance completeness
        prov_score = len(a.provenance) * 10
        for p in a.provenance:
            if p.source_locator:
                prov_score += 5

        # 3. Content completeness
        content_score = 0
        if a.question:
            content_score += len(a.question.solution_methods) * 15
            content_score += len(a.question.concepts) * 5
            if a.question.verified_answer:
                content_score += 20
        if a.figure_refs:
            content_score += len(a.figure_refs) * 10

        # 4. Stability: invert version so lower version ranks higher, or use timestamp
        # Invert version (version 1 > version 2)
        version_stability = -a.atom_version

        # 5. Tie breaker: invert atom_id so alphabetically smaller wins in max()
        # Alternatively, sort with key directly
        return (status_weight, prov_score, content_score, version_stability, "")

    # Sort descending by score, tie-breaker ascending on atom_id
    sorted_atoms = sorted(
        atoms,
        key=lambda a: (_score_atom(a)[:4], -ord(a.atom_id[0]) if a.atom_id else 0, a.atom_id),
    )
    # The highest scoring atom
    best_atom = max(
        atoms,
        key=lambda a: (
            _score_atom(a)[0],  # status
            _score_atom(a)[1],  # provenance
            _score_atom(a)[2],  # content
            _score_atom(a)[3],  # stability
            # Invert string comparison for max(): lexicographically smaller atom_id wins
            [-ord(c) for c in a.atom_id],
        ),
    )
    return best_atom


def stage_dedup_decisions_file(
    candidate_file: Path,
    staging_dir: Optional[Path] = None,
    review_queue_dir: Optional[Path] = None,
) -> Tuple[bool, Optional[Path], List[str]]:
    """Validate untrusted deduplication decisions submitted by subagents."""
    errors: List[str] = []
    root = Path.cwd()
    if staging_dir is None:
        staging_dir = root / "build" / "staging" / "deduplication"
    if review_queue_dir is None:
        review_queue_dir = root / "review" / "queue" / "deduplication"

    candidate_file = Path(candidate_file)
    if not candidate_file.exists():
        return False, None, [f"Candidate decisions file '{candidate_file}' does not exist."]

    try:
        with open(candidate_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        return False, None, [f"Failed to parse JSON in '{candidate_file}': {e}"]

    items = raw_data if isinstance(raw_data, list) else [raw_data]
    validated_decisions: List[DedupDecision] = []

    for idx, item in enumerate(items):
        try:
            decision = DedupDecision.model_validate(item)
            validated_decisions.append(decision)
        except Exception as e:
            errors.append(f"Decision {idx+1} schema validation failed: {e}")

    if errors:
        return False, None, errors

    staging_dir.mkdir(parents=True, exist_ok=True)
    staged_path = staging_dir / candidate_file.name
    safe_write_json(staged_path, [d.model_dump(mode="json") for d in validated_decisions])
    return True, staged_path, []


class DeduplicationResult:
    def __init__(self):
        self.merged_clusters: List[DedupCluster] = []
        self.mappings: List[CanonicalMapping] = []
        self.kept_separate: List[str] = []
        self.review_items: List[Dict[str, Any]] = []
        self.rejected_items: List[Dict[str, Any]] = []
        self.audit_records: List[DedupAuditJournalRecord] = []


def apply_deduplication(
    decisions: List[DedupDecision],
    candidates_map: Dict[str, DedupCandidate],
    atoms_dir: Optional[Path] = None,
    dedup_dir: Optional[Path] = None,
    review_queue_dir: Optional[Path] = None,
    reports_dir: Optional[Path] = None,
    confidence_threshold: float = 0.85,
) -> DeduplicationResult:
    """Execute deterministic deduplication gate, clustering, provenance preservation, and audit logging."""
    root = Path.cwd()
    if atoms_dir is None:
        atoms_dir = root / "kb" / "atoms"
    if dedup_dir is None:
        dedup_dir = root / "kb" / "dedup"
    if review_queue_dir is None:
        review_queue_dir = root / "review" / "queue" / "deduplication"
    if reports_dir is None:
        reports_dir = root / "build" / "reports"

    clusters_dir = dedup_dir / "clusters"
    mappings_dir = dedup_dir / "mappings"
    audit_journal_path = dedup_dir / "audit_journal.jsonl"

    clusters_dir.mkdir(parents=True, exist_ok=True)
    mappings_dir.mkdir(parents=True, exist_ok=True)
    review_queue_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    result = DeduplicationResult()

    # Cache loaded canonical atoms
    loaded_atoms: Dict[str, KnowledgeAtom] = {}

    def _get_atom(atom_id: str) -> Optional[KnowledgeAtom]:
        if atom_id in loaded_atoms:
            return loaded_atoms[atom_id]
        p = atoms_dir / f"{atom_id}.json"
        if not p.exists():
            return None
        try:
            atom = KnowledgeAtom.model_validate_json(p.read_text(encoding="utf-8"))
            loaded_atoms[atom_id] = atom
            return atom
        except Exception:
            return None

    # Track pairs approved for merge
    # Pair -> decision
    merge_pairs: List[Tuple[str, str, DedupDecision]] = []
    contradiction_tracker: Dict[Tuple[str, str], str] = {}

    for decision in decisions:
        cand = candidates_map.get(decision.candidate_id)
        if not cand:
            review_item = {
                "candidate_id": decision.candidate_id,
                "reason": "UNKNOWN_CANDIDATE_ID",
                "details": f"Candidate ID '{decision.candidate_id}' not found in candidate registry.",
                "decision": decision.model_dump(mode="json"),
            }
            result.review_items.append(review_item)
            safe_write_json(review_queue_dir / f"review_{decision.candidate_id}.json", review_item)
            continue

        atom_a = _get_atom(cand.atom_a_id)
        atom_b = _get_atom(cand.atom_b_id)

        if not atom_a or not atom_b:
            missing = cand.atom_a_id if not atom_a else cand.atom_b_id
            reject_item = {
                "candidate_id": decision.candidate_id,
                "reason": "ATOM_NOT_FOUND",
                "details": f"Atom '{missing}' does not exist in canonical kb/atoms/.",
            }
            result.rejected_items.append(reject_item)
            continue

        # Invariant: Subject isolation - only PHYSICS questions may merge
        sub_a = getattr(atom_a, "subject", None) or cand.candidate_metadata.get("atom_a_subject", "PHYSICS")
        sub_b = getattr(atom_b, "subject", None) or cand.candidate_metadata.get("atom_b_subject", "PHYSICS")
        if str(sub_a).upper() != "PHYSICS" or str(sub_b).upper() != "PHYSICS":
            reject_item = {
                "candidate_id": decision.candidate_id,
                "reason": "SUBJECT_ISOLATION_VIOLATION",
                "details": f"Subject isolation violation: atom_a={sub_a}, atom_b={sub_b}. Cross-subject merges are strictly prohibited.",
            }
            result.rejected_items.append(reject_item)
            continue

        # Invariant: Block synthetic test fixtures from production canonical deduplication
        is_fixture = (
            getattr(atom_a, "is_test_fixture", False)
            or getattr(atom_b, "is_test_fixture", False)
            or any(m in cand.atom_a_id.lower() for m in PROHIBITED_CANONICAL_MARKERS)
            or any(m in cand.atom_b_id.lower() for m in PROHIBITED_CANONICAL_MARKERS)
            or cand.candidate_metadata.get("is_test_fixture", False)
        )
        if is_fixture and dedup_dir == root / "kb" / "dedup":
            reject_item = {
                "candidate_id": decision.candidate_id,
                "reason": "TEST_FIXTURE_BLOCKED_FROM_PRODUCTION_KB",
                "details": f"Synthetic test fixtures ({cand.atom_a_id}, {cand.atom_b_id}) cannot be merged into production canonical storage.",
            }
            result.rejected_items.append(reject_item)
            continue

        # Invariant: Both atoms must be VERIFIED
        if atom_a.verification_status != AtomStatus.VERIFIED or atom_b.verification_status != AtomStatus.VERIFIED:
            reject_item = {
                "candidate_id": decision.candidate_id,
                "reason": "ATOM_NOT_VERIFIED",
                "details": f"Atoms must be VERIFIED. atom_a={atom_a.verification_status}, atom_b={atom_b.verification_status}",
            }
            result.rejected_items.append(reject_item)
            continue

        # Check confidence threshold
        if decision.duplicate_confidence < confidence_threshold and decision.decision_class in (
            DedupDecisionClass.EXACT_DUPLICATE,
            DedupDecisionClass.SEMANTIC_DUPLICATE,
            DedupDecisionClass.MULTI_METHOD_SAME_PROBLEM,
        ):
            review_item = {
                "candidate_id": decision.candidate_id,
                "reason": "CONFIDENCE_BELOW_THRESHOLD",
                "details": f"Confidence {decision.duplicate_confidence} < threshold {confidence_threshold}",
                "decision": decision.model_dump(mode="json"),
            }
            result.review_items.append(review_item)
            safe_write_json(review_queue_dir / f"review_{decision.candidate_id}.json", review_item)
            continue

        # Class: UNCERTAIN
        if decision.decision_class == DedupDecisionClass.UNCERTAIN:
            review_item = {
                "candidate_id": decision.candidate_id,
                "reason": "UNCERTAIN_DECISION",
                "details": decision.rationale,
                "decision": decision.model_dump(mode="json"),
            }
            result.review_items.append(review_item)
            safe_write_json(review_queue_dir / f"review_{decision.candidate_id}.json", review_item)
            continue

        # Class: SAME_CONCEPT_DIFFERENT_PROBLEM or RELATED_BUT_DISTINCT
        if decision.decision_class in (
            DedupDecisionClass.SAME_CONCEPT_DIFFERENT_PROBLEM,
            DedupDecisionClass.RELATED_BUT_DISTINCT,
        ):
            pair_key = (min(cand.atom_a_id, cand.atom_b_id), max(cand.atom_a_id, cand.atom_b_id))
            contradiction_tracker[pair_key] = decision.decision_class.value
            result.kept_separate.append(decision.candidate_id)

            # Record in journal
            journal_rec = DedupAuditJournalRecord(
                entry_id=f"jrn-sep-{decision.candidate_id}",
                action_type="KEPT_SEPARATE",
                candidate_id=decision.candidate_id,
                decision_id=decision.candidate_id,
                details={
                    "atom_a": cand.atom_a_id,
                    "atom_b": cand.atom_b_id,
                    "decision_class": decision.decision_class.value,
                    "rationale": decision.rationale,
                },
            )
            result.audit_records.append(journal_rec)
            continue

        # Potential MERGE class: EXACT_DUPLICATE, SEMANTIC_DUPLICATE, MULTI_METHOD_SAME_PROBLEM
        # INVARIANT: Physics truth check - compare verified answers
        ans_a = atom_a.question.verified_answer if atom_a.question else None
        ans_b = atom_b.question.verified_answer if atom_b.question else None

        if ans_a is not None and ans_b is not None and str(ans_a).strip() != str(ans_b).strip():
            # Discrepancy in physics answers between claimed duplicates!
            review_item = {
                "candidate_id": decision.candidate_id,
                "reason": "PHYSICS_ANSWER_CONFLICT",
                "details": f"Claimed duplicates have conflicting verified answers: atom_a={ans_a} vs atom_b={ans_b}. Refusing silent merge.",
                "decision": decision.model_dump(mode="json"),
            }
            result.review_items.append(review_item)
            safe_write_json(review_queue_dir / f"review_{decision.candidate_id}.json", review_item)
            continue

        # Approved for merge pairing
        merge_pairs.append((cand.atom_a_id, cand.atom_b_id, decision))

    # Build connected clusters using Disjoint Set Union (DSU)
    parent: Dict[str, str] = {}
    cluster_decisions: Dict[str, List[DedupDecision]] = {}

    def find(x: str) -> str:
        if parent.setdefault(x, x) != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for a_id, b_id, dec in merge_pairs:
        union(a_id, b_id)

    # Group atoms by root
    cluster_groups: Dict[str, Set[str]] = {}
    for a_id, b_id, dec in merge_pairs:
        root_id = find(a_id)
        cluster_groups.setdefault(root_id, set()).add(a_id)
        cluster_groups.setdefault(root_id, set()).add(b_id)
        cluster_decisions.setdefault(root_id, []).append(dec)

    # Check for contradictions within clusters
    for root_id, members in list(cluster_groups.items()):
        member_list = sorted(list(members))
        has_contradiction = False
        conflict_desc = ""
        for i in range(len(member_list)):
            for j in range(i + 1, len(member_list)):
                pair_key = (min(member_list[i], member_list[j]), max(member_list[i], member_list[j]))
                if pair_key in contradiction_tracker:
                    has_contradiction = True
                    conflict_desc = f"Cluster members {pair_key[0]} and {pair_key[1]} have contradictory decision: {contradiction_tracker[pair_key]}"
                    break
            if has_contradiction:
                break

        if has_contradiction:
            # Route entire cluster to review queue
            review_item = {
                "cluster_root": root_id,
                "reason": "CLUSTER_CONTRADICTION",
                "details": conflict_desc,
                "member_atoms": member_list,
            }
            result.review_items.append(review_item)
            safe_write_json(review_queue_dir / f"review_cluster_contradiction_{root_id[:16]}.json", review_item)
            del cluster_groups[root_id]
            continue

        # Valid cluster: Deterministically select canonical representative
        member_atoms = [_get_atom(m) for m in member_list if _get_atom(m) is not None]
        canonical_atom = select_canonical_representative(member_atoms)

        # Consolidate preserved provenance
        preserved_prov_list: List[Dict[str, Any]] = []
        seen_prov_signatures: Set[str] = set()

        for m_atom in member_atoms:
            for p in m_atom.provenance:
                sig = f"{p.source_id}|{p.page_start}|{p.page_end}|{p.source_locator}"
                if sig not in seen_prov_signatures:
                    seen_prov_signatures.add(sig)
                    preserved_rec = PreservedProvenance(
                        atom_id=m_atom.atom_id,
                        source_id=p.source_id,
                        file_name=p.file_name,
                        file_path=p.file_path,
                        page_start=p.page_start,
                        page_end=p.page_end,
                        source_locator=p.source_locator,
                        edition=p.edition,
                        source_claimed_answer=m_atom.question.source_claimed_answer if m_atom.question else None,
                        original_statement=m_atom.question.statement if m_atom.question else m_atom.content,
                        extraction_metadata=p.extraction_metadata,
                    )
                    preserved_prov_list.append(preserved_rec.model_dump(mode="json"))

        # Consolidate preserved solution methods
        preserved_methods_list: List[Dict[str, Any]] = []
        seen_method_signatures: Set[str] = set()

        for m_atom in member_atoms:
            if m_atom.question and m_atom.question.solution_methods:
                for idx, sm in enumerate(m_atom.question.solution_methods):
                    msig = hashlib.sha256(sm.steps.encode("utf-8")).hexdigest()[:16]
                    if msig not in seen_method_signatures:
                        seen_method_signatures.add(msig)
                        sm_rec = PreservedSolutionMethod(
                            method_id=f"sm-{m_atom.atom_id[:12]}-{idx+1}",
                            source_atom_id=m_atom.atom_id,
                            source_id=m_atom.provenance[0].source_id if m_atom.provenance else None,
                            method_name=sm.method_name,
                            steps=sm.steps,
                            source_attributed=sm.source_attributed,
                            verified=True,
                        )
                        preserved_methods_list.append(sm_rec.model_dump(mode="json"))

        decs = cluster_decisions.get(root_id, [])
        cluster_conf = min((d.duplicate_confidence for d in decs), default=1.0)
        # Determine dominant cluster type
        cluster_type = DedupDecisionClass.EXACT_DUPLICATE
        if any(d.decision_class == DedupDecisionClass.MULTI_METHOD_SAME_PROBLEM for d in decs):
            cluster_type = DedupDecisionClass.MULTI_METHOD_SAME_PROBLEM
        elif any(d.decision_class == DedupDecisionClass.SEMANTIC_DUPLICATE for d in decs):
            cluster_type = DedupDecisionClass.SEMANTIC_DUPLICATE

        cluster_id = f"cluster-{canonical_atom.atom_id[:20]}-{hashlib.sha256(','.join(member_list).encode('utf-8')).hexdigest()[:8]}"

        cluster_obj = DedupCluster(
            cluster_id=cluster_id,
            canonical_atom_id=canonical_atom.atom_id,
            member_atom_ids=member_list,
            cluster_type=cluster_type,
            cluster_confidence=cluster_conf,
            decision_ids=[d.candidate_id for d in decs],
            preserved_provenance=preserved_prov_list,
            preserved_solution_methods=preserved_methods_list,
        )
        result.merged_clusters.append(cluster_obj)
        safe_write_json(clusters_dir / f"{cluster_id}.json", cluster_obj.model_dump(mode="json"))

        # Create canonical mappings for every member
        for m_atom in member_atoms:
            primary_dec = decs[0] if decs else None
            mapping_obj = CanonicalMapping(
                original_atom_id=m_atom.atom_id,
                canonical_atom_id=canonical_atom.atom_id,
                cluster_id=cluster_id,
                reason=primary_dec.rationale if primary_dec else "Deterministic exact duplicate merge",
                decision_id=primary_dec.candidate_id if primary_dec else "exact-hash",
                classifier_identity=primary_dec.agent_identity if primary_dec else "deterministic-gate",
                conversation_id=primary_dec.agent_conversation_id if primary_dec else "system",
                source_provenance=[p.model_dump(mode="json") for p in m_atom.provenance],
                atom_version=m_atom.atom_version,
                content_hash=m_atom.content_hash,
            )
            result.mappings.append(mapping_obj)
            safe_write_json(mappings_dir / f"{m_atom.atom_id}.json", mapping_obj.model_dump(mode="json"))

            # Log to audit journal
            journal_entry = DedupAuditJournalRecord(
                entry_id=f"jrn-map-{m_atom.atom_id}",
                action_type="MAPPING_REGISTERED",
                cluster_id=cluster_id,
                canonical_atom_id=canonical_atom.atom_id,
                candidate_id=primary_dec.candidate_id if primary_dec else None,
                decision_id=primary_dec.candidate_id if primary_dec else None,
                details={
                    "original_atom_id": m_atom.atom_id,
                    "canonical_atom_id": canonical_atom.atom_id,
                    "cluster_id": cluster_id,
                    "is_canonical": (m_atom.atom_id == canonical_atom.atom_id),
                    "cluster_type": cluster_type.value,
                    "preserved_provenance_count": len(preserved_prov_list),
                    "preserved_solutions_count": len(preserved_methods_list),
                },
            )
            result.audit_records.append(journal_entry)

    # Persist audit journal entries idempotently
    if result.audit_records:
        journal_dicts = [r.model_dump(mode="json") for r in result.audit_records]
        existing_records = []
        existing_entry_ids = set()
        if audit_journal_path.exists():
            try:
                with open(audit_journal_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            rec = json.loads(line)
                            existing_records.append(rec)
                            existing_entry_ids.add(rec.get("entry_id"))
            except Exception:
                pass
        new_records = [r for r in journal_dicts if r.get("entry_id") not in existing_entry_ids]
        if new_records:
            safe_write_jsonl(audit_journal_path, existing_records + new_records)

    # Persist build/reports/deduplication_decision_report.json
    decision_report_data = {
        "report_type": "DEDUPLICATION_DECISION_REPORT",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_decisions_processed": len(decisions),
        "total_clusters_created": len(result.merged_clusters),
        "total_canonical_mappings": len(result.mappings),
        "total_kept_separate": len(result.kept_separate),
        "total_routed_to_review": len(result.review_items),
        "total_rejected": len(result.rejected_items),
        "clusters": [c.model_dump(mode="json") for c in result.merged_clusters],
        "review_items": result.review_items,
        "rejected_items": result.rejected_items,
    }
    safe_write_json(reports_dir / "deduplication_decision_report.json", decision_report_data)

    return result
