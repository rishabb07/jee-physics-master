---
name: dedup-physics
description: Evaluate candidate physics problem pairs to classify mathematical and physical equivalence without altering canonical physics truth.
---

# Physics Semantic Deduplication Protocol

## 1. Prime Directives & System Invariants

1. **The Canonical Knowledge Base is the Source of Truth:**
   - You MUST NOT directly edit, modify, or delete files in `kb/atoms/`.
   - Your role is classification and relationship determination, not editing canonical atoms.

2. **Grounding & Physical Truth Invariant:**
   - Never alter the question statement, multiple-choice options, verified answer, or first-principles derivation.
   - If two candidate questions appear to be duplicates but have conflicting answers or physical contradictions, DO NOT "fix" or reconcile them. Classify them as `UNCERTAIN` or recommend `REVIEW`.

3. **Same Concept $\neq$ Same Problem:**
   - Two questions that both test "Conservation of Angular Momentum" or "Cutting a Bar Magnet" are NOT duplicates if their givens, geometric setup, or target quantities differ.
   - Merging different questions simply because they test the same topic is a severe pedagogical and scientific failure.

4. **Multi-Method Preservation:**
   - When the same underlying problem has multiple genuinely valid solution methods (e.g., Work-Energy vs Newton's Second Law vs Impulse-Momentum), preserve all valid methods. Do not discard alternative methods.

5. **Chain of Custody:**
   - You MUST write your deduplication decision records directly using your file-writing tool to:
     `build/staging/incoming/deduplication/{candidate_or_batch_id}.json`
   - The parent agent must NOT create or edit these records for you.

---

## 2. Physical & Mathematical Equivalence Framework

To determine if two questions are duplicates, evaluate across all fundamental dimensions:

| Dimension | Exact Duplicate | Semantic Duplicate | Same Concept / Different Problem |
| :--- | :--- | :--- | :--- |
| **Physical Setup** | Identical | Identical system & geometry | Different setup or geometry |
| **Givens / Variables** | Identical | Renamed variables ($m \to M$) or equivalent units | Different given values or conditions |
| **Governing Constraints** | Identical | Identical (e.g. frictionless, adiabatic) | Different constraints |
| **Target Quantity** | Identical | Identical physical target | Different unknown asked |
| **Answer / Solution** | Identical | Mathematically isomorphic | Different result or expression |

---

## 3. Decision Classes

- `EXACT_DUPLICATE`:
  Identical problem statement and options, modulo minor whitespace, punctuation, LaTeX delimiter differences (`\(...\)` vs `$..$`), or option prefixes (`(A)` vs `A`).

- `SEMANTIC_DUPLICATE`:
  Different wording, sentence structure, or notation, but mathematically and physically identical. For example:
  - Variable renaming ($r$ replaced by $R$, $\theta$ replaced by $\alpha$)
  - Unit re-expression ($10\text{ m/s}$ vs $1000\text{ cm/s}$)
  - Sentence order rearranged without changing conditions or target.

- `SAME_CONCEPT_DIFFERENT_PROBLEM`:
  Both problems test the same physics concept/formula, but have different givens, different geometric configurations, or seek different target quantities. These MUST remain separate.

- `MULTI_METHOD_SAME_PROBLEM`:
  The exact same underlying problem, but accompanied by distinct, valid solution derivations (e.g. energy balance vs kinematic equations). Both solution methods must be preserved.

- `RELATED_BUT_DISTINCT`:
  Strong lexical or conceptual overlap, but materially distinct physics problems. Must remain separate.

- `UNCERTAIN`:
  Ambiguous evidence, conflicting answers, or confidence $< 0.85$. Routes immediately to `review/queue/deduplication/`.

---

## 4. Output Schema (`DedupDecision`)

Write each decision directly to `build/staging/incoming/deduplication/`:

```json
{
  "candidate_id": "cand-current-elec-current-elec",
  "decision_class": "EXACT_DUPLICATE",
  "duplicate_confidence": 1.0,
  "same_underlying_problem": true,
  "same_concept_only": false,
  "rationale": "Exact match of circuit problem with identical resistances and battery voltage, differing only in whitespace and LaTeX formatting.",
  "distinguishing_evidence": null,
  "recommended_action": "MERGE",
  "agent_identity": "physics-deduplicator",
  "agent_conversation_id": "<your_conversation_id>",
  "created_at": "2026-09-28T05:00:00Z",
  "notes": null
}
```
