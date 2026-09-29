# Multi-Agent Operating Protocols & Guidelines

This document governs the operational rules for all AI subagents, developer agents, and automated workers interacting with the **JEE Physics Master Knowledge System**.

---

## 1. Prime Directives

1. **The Knowledge Base (`kb/`) is the Source of Truth:**
   - Never treat `output/book/` or web artifacts as the source of truth.
   - Never write unverified extractions directly into `kb/atoms/`. All extractions must pass through `build/staging/` and undergo verification first.
2. **Grounding Invariant:**
   - No unsupported generated content may be promoted into the canonical knowledge base or published output.
   - Every physics statement, formula, question, or solution must have a traceable basis in canonical verified atoms, explicitly declared first-principles derivations, or authorized sources.
3. **Preserve Provenance Permanently:**
   - Never fabricate, alter, or discard source provenance (file name, page numbers, edition, exam paper year/number).
   - If a textbook answer is wrong, do not silently fix it in the source record. Flag a `SOURCE_ERROR` and document both the historical source key and the independently verified correct physics proof.
4. **Zero Silent Loss:**
   - If material cannot be placed into the main narrative of a chapter, it must be placed in `kb/archive/` with an explicit reason code.
5. **Deterministic Code Handles Deterministic Logic:**
   - File hashing, schema validation, LaTeX delimiter balancing, coverage accounting, and directory transactions are handled strictly by Python code in `src/jee_physics/`.
6. **Exception-Only Human Escalation:**
   - Resolve disputes automatically via secondary verifiers and adjudicators. Route to `review/queue/` only when disagreement remains unresolved.

---

## 2. Agent Responsibilities

| Agent Role | Boundary | Output Destination |
| :--- | :--- | :--- |
| **Ingestion Agent** | Reads raw documents, extracts table of contents, splits page segments | `sources/segments/{source_id}_segments.json` |
| **Atomization Agent** | Extracts theory, formulas, examples, questions from segments | `build/staging/atoms/{batch_id}.jsonl` |
| **Verification Agent (Blind)** | Independently solves physics problems without viewing answer keys | `verification/records/{atom_id}.json` |
| **Deduplication Agent** | Clusters duplicate questions and preserves multiple solution methods | `kb/dedup/clusters.jsonl` |
| **Chapter Assembly Agent**| Generates pedagogical narrative and ladders grounded in verified atoms | `build/drafts/{chapter_id}/` |
| **Coverage QA Agent** | Audits draft chapters for 100% atom placement | `build/reports/coverage_{chapter_id}.json` |
