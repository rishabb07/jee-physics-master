# JEE Physics Knowledge & Learning System
## Authoritative Foundational System Architecture

---

### Executive Overview

This system is an AI-powered physics knowledge and learning refinery designed for JEE Physics (Main, Advanced) and higher-tier extensions (Olympiads). It ingests a continuously growing collection of raw physics documents (textbooks, problem books, coaching modules, past exam papers, handwritten notes, diagrams) and converts them into an auditable, verified, deduplicated knowledge graph of **Knowledge Atoms**.

From this canonical knowledge base, downstream learning products (graded books, conceptual ladders, fill-in workbooks, adaptive mock tests, and personalized remediation paths) are produced as **reproducible, disposable projections**.

The core governing principle is:
> **"The Knowledge Base is the sole source of truth. The generated book is never canonical. All critical information is persisted to disk in transparent, version-controlled formats. Nothing is silently lost, and no unsupported generated content may be promoted into the canonical knowledge base or published output."**

---

## 1. Core Architectural Corrections & System Invariants

### 1.1 Staged Knowledge Lifecycle (Extraction Is Not Canonical)
Raw model extractions must never be committed directly to the canonical knowledge base. Unverified material must stay completely outside `kb/atoms/`.

The strict lifecycle is:
```text
RAW SOURCE 
  → SOURCE REGISTRY 
  → SEGMENTATION 
  → LLM EXTRACTION 
  → build/staging/ 
  → Deterministic Schema / Syntax / Provenance Validation 
  → Verification / Adjudication (Risk-based & Random) 
  → kb/atoms/ (Canonical VERIFIED Knowledge)
```
- `kb/atoms/` contains **strictly approved, verified knowledge**.
- In-flight or unadjudicated extractions remain in `build/staging/atoms/`.

### 1.2 Pydantic as the Single Source of Truth for Data Models
To avoid dual-maintenance synchronization issues and drifting contracts:
- Python **Pydantic models** (`src/jee_physics/models/`) are the authoritative definitions of all system entities.
- JSON Schemas in `schemas/` are **deterministically generated** from these Pydantic models via code generation scripts.
- Runtime validators, CLI commands, and automated test suites all bind against these Pydantic definitions.

### 1.3 The Grounding Invariant (Replacing "Zero Hallucination")
Rather than asserting unverifiable absolute claims like "AI will never hallucinate", the system enforces an operational, testable boundary:
> **"No unsupported generated content may be promoted into the canonical knowledge base or published output."**

Every claim, theorem, formula, question, and solution in the canonical knowledge base and published book must possess a verifiable, traceable basis in:
1. Canonical verified atoms (`kb/atoms/`).
2. Explicitly flagged first-principles mathematical derivations whose assumptions and steps are inspectable.
3. Explicitly authorized source classes recorded in the registry (`sources/registry/`).

### 1.4 Automated Exception Escalation (Review as an Exception System)
Ordinary high-confidence extractions must flow through automated validation without human bottlenecks. Human intervention is strictly an exception system for irreconcilable edge cases.

The escalation ladder is:
```text
Extraction Agent 
  → Second Agent / Independent Verifier (Dual-Pass Solver) 
  → Automated Adjudicator 
  → Unresolved Exception Queue (review/queue/) 
  → Human Reviewer
```
Routine extractions that meet schema, syntax, and verification criteria are auto-promoted. Only items where dual solvers disagree, or where handwriting/diagrams remain ambiguous after automated adjudication, enter `review/queue/`.

### 1.5 Explicit Knowledge Archive & Quarantine (`kb/archive/`)
To uphold the rule that **no source material is silently discarded**, usable physics material that does not cleanly fit the curated narrative flow of a standard chapter (e.g. niche historical contexts, non-standard problem variants, alternative redundant proofs, or tangential olympiad lemmas) is routed to `kb/archive/`.
- Every extracted atom is either placed in a primary product (book section, question bank, ladder, mock) or explicitly preserved in `kb/archive/` with a machine-readable reason code.
- Malformed, unparseable, or corrupt records are quarantined in `review/queue/quarantine/` with full provenance logs.

### 1.6 Risk-Based and Random Verification
To optimize compute budget and focus scrutiny where physics errors are most likely to occur, verification employs a hybrid strategy:
1. **Targeted High-Risk Verification:** $100\%$ mandatory independent solving for:
   - Ambiguous or low-confidence extractions ($confidence < 0.85$).
   - High-difficulty questions (Levels L4 and L5 / JEE Advanced multi-concept / Olympiad).
   - Complex multi-body diagram or constraint problems.
   - Questions where source answers have conflicting keys across editions or books.
   - Handwritten notes or unverified coaching solution keys.
   - Problems selected for high-stakes Mock Tests.
2. **Random Sampling Verification:** A configurable pseudo-random sample (e.g. $10\%–20\%$) of standard L1–L3 questions and routine theory extractions is independently re-solved to detect systemic model or transcription drift.

---

## 2. System Directory Tree

The directory layout enforces a strict separation between immutable inputs, the verified knowledge base, ephemeral build staging, exception queues, and deterministic software code.

```text
jee-physics-master/
├── .git/                                 # Git version control
├── .gitignore
├── README.md                             # Project overview and operational guide
├── AGENTS.md                             # Multi-agent system guidelines & protocols
├── pyproject.toml                        # Project dependencies and configuration
│
├── config/                               # System configuration (version-controlled)
│   ├── system_config.yaml                # Global thresholds, model routing, worker limits
│   └── style_guide.md                    # Authoritative pedagogical style guide
│
├── schemas/                              # Auto-generated JSON Schemas from Pydantic models
│   ├── source.schema.json
│   ├── source_segment.schema.json
│   ├── atom.schema.json
│   ├── provenance.schema.json
│   ├── dedup.schema.json
│   ├── verification.schema.json
│   ├── review.schema.json
│   ├── chapter_spec.schema.json
│   ├── mock_spec.schema.json
│   └── job_manifest.schema.json
│
├── sources/                              # Source storage & ingestion tracking
│   ├── raw/                              # Immutable raw inputs (PDFs, images, scans)
│   │   ├── books/
│   │   ├── coaching/
│   │   ├── test_papers/
│   │   └── notes/
│   ├── registry/                         # One JSON per registered source file ({source_id}.json)
│   ├── segments/                         # Page ranges and provisional chapter routing
│   └── figures/                          # Extracted source figures (crops + metadata)
│
├── kb/                                   # CANONICAL KNOWLEDGE BASE (Sole Source of Truth)
│   ├── taxonomy/                         # Syllabus hierarchy (tree + concept dependencies)
│   │   ├── syllabus_tree.yaml
│   │   └── prerequisites.yaml
│   ├── atoms/                            # Verified atomic knowledge units (CANONICAL)
│   │   ├── mechanics/
│   │   │   ├── kinematics/
│   │   │   │   └── atoms.jsonl           # Partitioned by topic for git friendliness
│   │   │   └── ...
│   │   └── electrodynamics/
│   │       └── ...
│   ├── dedup/                            # Deduplication clusters & multi-source provenance links
│   │   └── clusters.jsonl
│   └── archive/                          # Off-narrative but valid source atoms (Nothing lost)
│       └── {chapter_id}_archive.jsonl
│
├── verification/                         # Mathematical & Physics Verification Records
│   └── records/                          # One record per verified atom ({atom_id}_verification.json)
│
├── review/                               # Human-in-the-Loop Exception Queues
│   ├── queue/                            # Active unresolved exceptions (ocr, physics_conflict)
│   └── resolved/                         # Audit trail of human decisions & corrections
│
├── curriculum/                           # Editorial & Pedagogical Blueprints
│   ├── chapters/                         # Per-chapter composition specs (outlines, mandatory atoms)
│   └── ladders/                          # Scaffolding blueprints for progressive problem ladders
│
├── build/                                # Ephemeral & Staged Generation Workspace
│   ├── staging/                          # Unverified extractions awaiting validation
│   │   ├── atoms/                        # Staged raw atoms ({batch_id}.jsonl)
│   │   └── manifests/                    # Manifests detailing extraction run batches
│   ├── drafts/                           # Isolated staging directory for unverified chapter builds
│   └── reports/                          # Pre-promotion audits (coverage checks, LaTeX linting)
│
├── output/                               # Published / Rendered Learning Product (Disposable projections)
│   ├── book/                             # Validated production chapters (JSON + readable Markdown)
│   ├── question_bank/                    # Graded, searchable question pool (L1-L5)
│   ├── question_ladders/                 # Assembled progressive ladders
│   └── mock_tests/                       # Assembled mock papers with solutions & answer keys
│
├── student/                              # Student interaction & remediation layer
│   ├── progress/                         # Session history & completed units
│   ├── mistakes/                         # Mistake log with concept tags
│   └── remediation_plans/                # Targeted revision sets
│
├── src/                                  # Deterministic Software Pipeline (Python 3.12+)
│   └── jee_physics/
│       ├── __init__.py
│       ├── models/                       # Authoritative Pydantic models
│       ├── core/                         # Hasher, ID generators, file locks, state machine
│       ├── ingestion/                    # File scanner, PDF page boundary segmenter
│       ├── validation/                   # Schema validator, LaTeX linter, coverage auditor
│       ├── storage/                      # Safe transactional atomic writes, indexers
│       ├── reports/                      # Structured status and coverage reporting
│       └── cli.py                        # Unified CLI interface
│
├── prompts/                              # Version-controlled LLM Agent Prompts & System Instructions
│   ├── atomization/
│   ├── verification/
│   ├── dedup/
│   └── chapter_assembly/
│
└── tests/                                # Automated unit, property, and integration tests
```

---

## 3. Task Allocation: Deterministic Code vs. LLM Tasks

| Pipeline Stage | Deterministic Software (Python) | LLM Cognitive Agent |
| :--- | :--- | :--- |
| **Ingestion** | SHA-256 fingerprinting, change detection, file size, page bounds | Document classification (book vs notes vs mock), TOC parsing |
| **Extraction** | Schema validation, deterministic ID assignment, LaTeX syntax linting | Multimodal OCR, mathematical transcription, atomization |
| **Taxonomy** | Validating parent/child node existence in syllabus tree | Mapping source topic terminology to official JEE syllabus nodes |
| **Deduplication** | Exact text/formula hashing, initial text indexing | Semantic equivalence detection, multi-solution clustering |
| **Verification** | Option comparison, numerical evaluation within tolerance ($\delta \le 10^{-3}$) | Blind first-principles problem solving (source answer stripped) |
| **Adjudication** | Automated matching logic, routing to archive or review queue | Secondary dispute arbitration between conflicting solvers |
| **Assembly** | Atom reference checks, coverage arithmetic ($Coverage = \frac{Placed}{Eligible}$) | Pedagogical synthesis, intuitive prose, ladder progression |
| **Deployment** | Transactional directory swaps, git commit management | Generation of targeted remediation sets from student error logs |

---

## 4. Core Data Structures & Schema Specifications

Pydantic models in `src/jee_physics/models/` serve as the canonical source of truth for:
1. `SourceRegistryRecord` (source file tracking, SHA-256, page counts, lifecycle status).
2. `SourceSegment` (page bounds, provisional chapter/topic mapping).
3. `KnowledgeAtom` (the core unit: `theory`, `formula`, `solved_example`, `question`, `figure`, `insight`, `misconception`).
4. `ProvenanceRecord` (source file, start/end pages, locator, extraction metadata; supports multiple source occurrences).
5. `DedupRecord` (canonical atom mapping, duplicate group ID, method variations).
6. `VerificationRecord` (source answer vs independent solver answer, verdict, discrepancy classification).
7. `ReviewQueueItem` (unresolved exceptions, issue type, image crop paths, reviewer decisions).
8. `ChapterSpec` (narrative blueprint, target atom references, ladder rules).
9. `MockTestSpec` (question count, difficulty distribution, remediation blueprint).
10. `JobManifest` (input file hashes, generated atom IDs, run logs).

---

## 5. File-Based Agent Communication & Staging Protocol

```text
[sources/raw/] 
      │ (deterministic scanner)
      ▼
sources/registry/{source_id}.json [State: REGISTERED]
      │ (segmenter)
      ▼
sources/segments/{source_id}_segments.json [State: SEGMENTED]
      │ (atomization agent writes batch payload + manifest)
      ▼
build/staging/atoms/{batch_id}.jsonl [State: STAGED]
      │ (deterministic schema & syntax gate)
      ├─► FAIL: review/queue/quarantine/{review_id}.json
      └─► PASS: build/staging/atoms/{batch_id}.validated.jsonl [State: VALIDATED]
            │
            ▼ (risk-based & random verification)
      verification/records/{atom_id}.json
            ├─► MISMATCH / AMBIGUOUS: review/queue/physics_conflict/
            └─► VERIFIED: kb/atoms/{chapter}/{topic}/atoms.jsonl [State: CANONICAL]
                  │
                  ▼ (curriculum assembly agent)
            build/drafts/{chapter_id}/
                  ├── sections/
                  └── draft_manifest.json
                        │ (deterministic coverage & QA audit)
                        ├─► Coverage < 1.0 or Syntax Error: HALT (build/drafts/ retained)
                        └─► PASS: Atomic promotion to output/book/{chapter_id}/
```

- **Manifests Before Movement:** Every batch processing step outputs a `{batch_id}.manifest.json` detailing input file hashes, output paths, and generated atom IDs.
- **Atomic Promotion via Directory Swap:** Completed chapters are written to `build/drafts/{chapter_id}/`. Only after passing the coverage and integrity auditors are they atomically promoted to `output/book/{chapter_id}/`.
- **Append-Only Event Stream:** Build executions append structured events to `build/reports/build_runs.jsonl`.

---

## 6. Verification Pipeline & Exception Handling System

### 6.1 The Blind Solver Protocol
The verification agent receives only the problem statement and diagram crop—never the textbook's answer key or solution. This prevents confirmation bias.

### 6.2 Discrepancy Triaging
- `SOURCE_ERROR`: Erratum in textbook. Original answer preserved in provenance; verified derivation is published with an explicit editorial disclaimer.
- `MODEL_ERROR`: The model made an algebra or arithmetic error. Automatically re-evaluated by a high-compute reasoning model.
- `AMBIGUOUS`: Insufficient physical constraints specified in the original source statement.
- `UNRESOLVED`: Disagreement persists after automated adjudication $\to$ routed to `review/queue/physics_conflict/`.

### 6.3 Safe Failure Isolation
A failure on a single question or page isolates only that item into `review/queue/` or `kb/archive/`. It does not contaminate the canonical knowledge base or stall the processing of the remaining library.
