from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from jee_physics.dedup.normalizer import compute_normalized_fingerprint
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.dedup import (
    ComparisonFeatures,
    DedupCandidate,
    NormalizedAtomFingerprint,
)
from jee_physics.storage.io import safe_write_json


def tokenize_physics_words(text: str) -> Set[str]:
    """Extract physics-relevant lowercase word tokens, ignoring common stops."""
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "of", "in", "on", "at", "to",
        "for", "with", "by", "from", "and", "or", "as", "if", "that", "this", "then",
        "be", "will", "has", "have", "had", "its", "each", "other", "when", "where"
    }
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    return {w for w in words if w not in stopwords}


def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Compute Jaccard similarity index between two sets of tokens."""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return float(intersection) / float(union) if union > 0 else 0.0


def extract_comparison_features(
    atom_a: KnowledgeAtom,
    atom_b: KnowledgeAtom,
    fp_a: NormalizedAtomFingerprint,
    fp_b: NormalizedAtomFingerprint,
) -> Dict[str, Any]:
    """Compute structured comparison signals across physical and mathematical dimensions."""
    features: Dict[str, Any] = {}

    # Exact statement hash match
    exact_stmt_match = fp_a.statement_hash == fp_b.statement_hash
    exact_prob_match = fp_a.problem_hash == fp_b.problem_hash

    # Target quantity comparison
    same_target = (fp_a.target_quantity is not None and fp_a.target_quantity == fp_b.target_quantity)
    features["same_target"] = same_target

    # Numerical values comparison
    nums_a = set(fp_a.numerical_values)
    nums_b = set(fp_b.numerical_values)
    same_numbers = (nums_a == nums_b and len(nums_a) > 0)
    features["same_numbers"] = same_numbers

    # Diagram role comparison
    same_diagram_role = fp_a.has_figure == fp_b.has_figure
    features["same_diagram_role"] = same_diagram_role

    # Answer / Option structure
    opts_a_len = len(atom_a.question.options) if atom_a.question and atom_a.question.options else 0
    opts_b_len = len(atom_b.question.options) if atom_b.question and atom_b.question.options else 0
    same_answer_structure = (opts_a_len == opts_b_len and fp_a.question_type == fp_b.question_type)
    features["same_answer_structure"] = same_answer_structure

    # Vocabulary overlap
    tokens_a = tokenize_physics_words(fp_a.statement_normalized)
    tokens_b = tokenize_physics_words(fp_b.statement_normalized)
    jaccard = jaccard_similarity(tokens_a, tokens_b)
    features["lexical_jaccard_similarity"] = round(jaccard, 4)

    # Notation / Wording vs Material Problem Difference
    if exact_prob_match or exact_stmt_match:
        features["same_physical_setup"] = True
        features["same_given_information"] = True
        features["same_constraints"] = True
        features["same_solution_structure"] = True
        features["wording_only_difference"] = False
        features["notation_only_difference"] = False
        features["numerical_substitution_only"] = False
        features["material_problem_difference"] = False
    else:
        # If very high token overlap and same numbers and same target, likely semantic duplicate
        if jaccard >= 0.70 and same_numbers and same_target:
            features["same_physical_setup"] = True
            features["same_given_information"] = True
            features["same_constraints"] = True
            features["same_solution_structure"] = True
            features["wording_only_difference"] = True
            features["notation_only_difference"] = False
            features["numerical_substitution_only"] = False
            features["material_problem_difference"] = False
        elif jaccard >= 0.65 and not same_numbers and same_target and len(nums_a) == len(nums_b):
            # Same problem structure with numerical substitution
            features["same_physical_setup"] = True
            features["same_given_information"] = False
            features["same_constraints"] = True
            features["same_solution_structure"] = True
            features["wording_only_difference"] = False
            features["notation_only_difference"] = False
            features["numerical_substitution_only"] = True
            features["material_problem_difference"] = True
        else:
            # Different problems or same concept
            features["same_physical_setup"] = (jaccard > 0.50)
            features["same_given_information"] = same_numbers
            features["same_constraints"] = None
            features["same_solution_structure"] = None
            features["wording_only_difference"] = False
            features["notation_only_difference"] = None
            features["numerical_substitution_only"] = False
            features["material_problem_difference"] = (jaccard < 0.85 or not same_numbers or not same_target)

    return features


def generate_candidate_pairs(
    atoms: List[KnowledgeAtom],
    additional_candidates: Optional[List[Tuple[KnowledgeAtom, KnowledgeAtom, str, List[str]]]] = None,
    semantic_retriever: Optional["BaseSemanticRetriever"] = None,
) -> Tuple[List[DedupCandidate], Dict[str, Any]]:
    """Multi-stage candidate generation: Exact Hash -> Taxonomy Blocking -> Feature Blocking."""
    candidates: List[DedupCandidate] = []
    seen_pairs: Set[Tuple[str, str]] = set()

    atom_map: Dict[str, KnowledgeAtom] = {a.atom_id: a for a in atoms}
    fingerprints: Dict[str, NormalizedAtomFingerprint] = {
        a.atom_id: compute_normalized_fingerprint(a) for a in atoms
    }

    def _add_candidate(
        id_a: str,
        id_b: str,
        method: str,
        signals: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        if id_a == id_b:
            return
        pair_key = (min(id_a, id_b), max(id_a, id_b))
        if pair_key in seen_pairs:
            return
        seen_pairs.add(pair_key)

        cand_id = f"cand-{id_a[:12]}-{id_b[:12]}"
        fp_a = fingerprints[id_a]
        fp_b = fingerprints[id_b]
        atom_a = atom_map[id_a]
        atom_b = atom_map[id_b]

        comp_features = extract_comparison_features(atom_a, atom_b, fp_a, fp_b)

        cand = DedupCandidate(
            candidate_id=cand_id,
            atom_a_id=id_a,
            atom_b_id=id_b,
            generation_method=method,
            blocking_signals=signals,
            atom_a_fingerprint=fp_a,
            atom_b_fingerprint=fp_b,
            comparison_features=comp_features,
            candidate_metadata=metadata or {},
        )
        candidates.append(cand)

    # Stage 1: Exact Normalized Hash Matching (Problem hash & Statement hash)
    exact_prob_buckets: Dict[str, List[str]] = defaultdict(list)
    exact_stmt_buckets: Dict[str, List[str]] = defaultdict(list)

    for atom_id, fp in fingerprints.items():
        exact_prob_buckets[fp.problem_hash].append(atom_id)
        exact_stmt_buckets[fp.statement_hash].append(atom_id)

    for prob_hash, ids in exact_prob_buckets.items():
        if len(ids) > 1:
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    _add_candidate(
                        ids[i],
                        ids[j],
                        method="EXACT_HASH_MATCH",
                        signals=["EXACT_PROBLEM_HASH"],
                        metadata={"hash": prob_hash},
                    )

    for stmt_hash, ids in exact_stmt_buckets.items():
        if len(ids) > 1:
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    _add_candidate(
                        ids[i],
                        ids[j],
                        method="EXACT_HASH_MATCH",
                        signals=["EXACT_STATEMENT_HASH"],
                        metadata={"hash": stmt_hash},
                    )

    # Stage 2: Taxonomy Blocking (within same chapter / topic)
    tax_topic_buckets: Dict[str, List[str]] = defaultdict(list)
    for atom in atoms:
        if atom.taxonomy:
            key = f"{atom.taxonomy.chapter_id}/{atom.taxonomy.topic_id}"
            tax_topic_buckets[key].append(atom.atom_id)

    for topic_key, ids in tax_topic_buckets.items():
        if len(ids) > 1:
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    id_a, id_b = ids[i], ids[j]
                    fp_a, fp_b = fingerprints[id_a], fingerprints[id_b]
                    signals = [f"TAXONOMY:{topic_key}"]

                    # Check secondary affinity signals within taxonomy bucket
                    tokens_a = tokenize_physics_words(fp_a.statement_normalized)
                    tokens_b = tokenize_physics_words(fp_b.statement_normalized)
                    sim = jaccard_similarity(tokens_a, tokens_b)

                    if fp_a.subtopic_id and fp_a.subtopic_id == fp_b.subtopic_id:
                        signals.append(f"SUBTOPIC:{fp_a.subtopic_id}")
                    if fp_a.target_quantity and fp_a.target_quantity == fp_b.target_quantity:
                        signals.append(f"TARGET_QUANTITY:{fp_a.target_quantity}")
                    if fp_a.physics_skeleton_hash == fp_b.physics_skeleton_hash:
                        signals.append("PHYSICS_SKELETON_HASH_MATCH")
                    if sim >= 0.35:
                        signals.append(f"TOKEN_SIMILARITY_{int(sim*100)}")

                    # If in same topic bucket, generate candidate
                    if len(signals) >= 1:
                        _add_candidate(
                            id_a,
                            id_b,
                            method="TAXONOMY_BLOCKING",
                            signals=signals,
                            metadata={"topic": topic_key, "token_sim": round(sim, 3)},
                        )

    # Stage 3: Feature / Cross-Taxonomy Blocking (e.g. skeleton match across topic boundaries)
    skeleton_buckets: Dict[str, List[str]] = defaultdict(list)
    for atom_id, fp in fingerprints.items():
        skeleton_buckets[fp.physics_skeleton_hash].append(atom_id)

    for sk_hash, ids in skeleton_buckets.items():
        if len(ids) > 1:
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    _add_candidate(
                        ids[i],
                        ids[j],
                        method="FEATURE_BLOCKING",
                        signals=["CROSS_TAXONOMY_SKELETON_MATCH"],
                        metadata={"skeleton_hash": sk_hash},
                    )

    # Stage 4: Semantic Retriever (Future extension point for ANN / embedding vector indices)
    if semantic_retriever:
        semantic_pairs = semantic_retriever.retrieve_candidates(atoms, fingerprints)
        for id_a, id_b, score in semantic_pairs:
            _add_candidate(
                id_a,
                id_b,
                method="SEMANTIC_RETRIEVAL",
                signals=[f"EMBEDDING_SIMILARITY_{int(score*100)}"],
                metadata={"similarity_score": score},
            )

    # Stage 5: Process explicitly injected controlled candidate pairs (e.g. for test benchmarking)
    if additional_candidates:
        for atom_a, atom_b, method, signals in additional_candidates:
            if atom_a.atom_id not in atom_map:
                atom_map[atom_a.atom_id] = atom_a
                fingerprints[atom_a.atom_id] = compute_normalized_fingerprint(atom_a)
            if atom_b.atom_id not in atom_map:
                atom_map[atom_b.atom_id] = atom_b
                fingerprints[atom_b.atom_id] = compute_normalized_fingerprint(atom_b)
            _add_candidate(atom_a.atom_id, atom_b.atom_id, method=method, signals=signals)

    stats = {
        "total_atoms_evaluated": len(atoms),
        "total_candidate_pairs_generated": len(candidates),
        "exact_hash_candidates": sum(1 for c in candidates if c.generation_method == "EXACT_HASH_MATCH"),
        "taxonomy_blocking_candidates": sum(1 for c in candidates if c.generation_method == "TAXONOMY_BLOCKING"),
        "feature_blocking_candidates": sum(1 for c in candidates if c.generation_method == "FEATURE_BLOCKING"),
        "semantic_retrieval_candidates": sum(1 for c in candidates if c.generation_method == "SEMANTIC_RETRIEVAL"),
        "controlled_pilot_candidates": sum(1 for c in candidates if c.generation_method == "CONTROLLED_PILOT"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    return candidates, stats


class BaseSemanticRetriever:
    """Extension interface for future embedding/vector or ANN semantic candidate retrieval.
    
    Production scaling path:
    At 10,000+ questions, taxonomy blocking may generate too many pairs in large topics
    or miss cross-topic physical analogies. Concrete subclasses can implement:
    - Dense vector indexing (e.g., text-embedding-004 + FAISS / HNSW)
    - Sparse BM25 / SPLADE lexical retrieval
    - Physics-specific multimodal formula embeddings
    """
    def retrieve_candidates(
        self,
        atoms: List[KnowledgeAtom],
        fingerprints: Dict[str, NormalizedAtomFingerprint],
        top_k: int = 5,
        threshold: float = 0.75,
    ) -> List[Tuple[str, str, float]]:
        """Retrieve candidate pairs based on dense/sparse semantic embeddings.
        
        Returns:
            List of (atom_a_id, atom_b_id, similarity_score)
        """
        raise NotImplementedError("Subclasses must implement retrieve_candidates")


def write_candidate_report(
    candidates: List[DedupCandidate],
    stats: Dict[str, Any],
    report_path: Optional[Path] = None,
) -> Path:
    """Persist build/reports/deduplication_candidate_report.json."""
    if report_path is None:
        report_path = Path("build/reports/deduplication_candidate_report.json")
    report_data = {
        "report_type": "DEDUPLICATION_CANDIDATE_REPORT",
        "statistics": stats,
        "candidates": [c.model_dump(mode="json") for c in candidates],
    }
    safe_write_json(report_path, report_data)
    return report_path
