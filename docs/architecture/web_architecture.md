# Architecture Specification: Interactive Auto-Updating JEE Physics Web Application

## 1. System Vision & Core Principles

The **JEE Physics Master Book Web Application** is an interactive, auto-updating digital learning platform. It serves as a continuously synchronized projection of the canonical verified physics knowledge base.

### 1.1 Inviolable Principles
1. **Canonical KB is the Source of Truth:**
   - Canonical atoms (`kb/atoms/`), verified content (`build/drafts/`, `build/staging/incoming/content/`), curriculum specifications (`curriculum/`, `build/staging/incoming/curriculum/`), and verified question bank items (`question_bank/verified/`) are strictly authoritative.
   - The web application artifacts (`output/web/`, `build/web/`) are disposable projections that can be deleted and deterministically recompiled at any moment.
2. **Strict Verification Boundary:**
   - Absolutely NO unverified content, rejected items, or review queue items (`review/queue/questions/`) may enter the production web bundle.
   - Every question shown to students must possess a certified verification record (`question_bank/verified/`).
3. **Deterministic Auto-Updating:**
   - Changes in upstream knowledge artifacts (e.g. modified concept explanation, new formula, newly promoted question) trigger an automated, deterministic compilation (`python -m jee_physics build-web`) that yields an updated web bundle with matching content hashes and manifest.
4. **Self-Contained & Offline-First:**
   - The application requires zero Node.js/npm dependencies on the host machine.
   - All assets, fonts, styles, KaTeX math rendering engines, and client-side search engines are bundled locally.
5. **No Document-First Legacy:**
   - No PDFs, EPUBs, or printed layouts. The primary format is a modern, responsive, single-page application (SPA) with KaTeX math rendering, interactive question practice, search, and student progress tracking.

---

## 2. System Architecture

```text
CANONICAL KNOWLEDGE & VERIFIED REPOSITORIES
├── kb/taxonomy/syllabus.yaml               (30-chapter syllabus tree)
├── curriculum/prerequisite_graph.json       (Prerequisite DAG)
├── build/staging/incoming/curriculum/       (Chapter specs, plans, ladders)
├── build/staging/incoming/content/          (Concepts, formulas, derivations, examples, misconceptions)
└── question_bank/verified/                  (Promoted, verified questions)
                  ↓
       [ WebDataBuilder Engine ]
   (src/jee_physics/web/builder.py)
                  ↓
        build/web/data/                      (Deterministic JSON Datasets)
        ├── manifest.json
        ├── taxonomy.json
        ├── chapters.json
        ├── chapter_{id}.json
        ├── concepts.json
        ├── formulas.json
        ├── questions.json
        ├── ladders.json
        ├── prerequisites.json
        └── search_index.json
                  ↓
       [ WebCompiler Pipeline ]
  (src/jee_physics/web/compiler.py)
                  ↓
        output/web/                          (Production Web Application Bundle)
        ├── index.html                       (Semantic HTML shell)
        ├── css/app.css                      (Modern responsive typography & theme)
        ├── js/                              (Modular ES6 SPA: router, state, views, math, search)
        ├── vendor/katex/                    (Self-contained KaTeX JS, CSS, and fonts)
        └── data/                            (Compiled JSON data bundle)
```

---

## 3. Data Contract Specification

All datasets are generated deterministically in `build/web/data/` and mirrored to `output/web/data/`.

### 3.1 `manifest.json`
Contains build metadata, timestamps, generator hashes, chapter count, and content counts:
- `build_id`: UUIDv4
- `build_timestamp`: ISO 8601 string
- `version`: Semantic version (e.g. `1.0.0-pilot`)
- `git_commit`: Short hash or HEAD identifier
- `scope`: `PILOT` (4 chapters)
- `chapters`: List of chapter summary objects
- `counts`: Dictionary of total chapters, pilot chapters, concepts, formulas, derivations, examples, misconceptions, verified questions, and ladders.
- `content_hashes`: SHA-256 digests of all constituent data files.

### 3.2 `taxonomy.json`
The authoritative syllabus hierarchy reflecting all 30 chapters across 6 branches (Mechanics, Thermodynamics & Thermal Physics, Oscillations & Waves, Electrodynamics, Optics, Modern Physics).
Each chapter records:
- `chapter_id`: Canonical slug
- `title`: Display title
- `branch`: Subject branch
- `order`: Integer sequence
- `status`: `\"PILOT_ACTIVE\"` for the 4 pilot chapters, `\"PENDING\"` for the remaining 26 chapters.
- `topics`: List of topics with subtopics.

### 3.3 `chapters.json` and `chapter_{id}.json`
- `chapters.json`: Index list of all chapters with metadata, status, topic count, and content block counts.
- `chapter_{id}.json`: Deep chapter document containing:
  - Header & learning objectives
  - Prerequisites and forward links
  - Section-by-section pedagogical content blocks:
    - `CONCEPT`: Statement, intuition, boundary conditions, related formulas
    - `FORMULA`: LaTeX equation, variables with units and dimensions, conditions of validity, common pitfalls
    - `DERIVATION`: Step-by-step physical derivation with mathematical justifications
    - `WORKED_EXAMPLE`: Pedagogical problem, solution strategy, step-by-step solving, sanity checks, trap alerts
    - `MISCONCEPTION`: Erroneous thinking, physical explanation, diagnostic counterexample
    - `QUESTION`: Practice items mapped to the section
  - Question ladder references
  - Revision checklist

### 3.4 `formulas.json`
Complete formula sheet and reference handbook across all active chapters, searchable and filterable by chapter, topic, and physical dimensions.

### 3.5 `questions.json`
All verified questions approved for practice:
- `question_id`, `chapter_id`, `topic_id`, `type` (MCQ, Multi-Correct, Numerical)
- `problem_statement` (LaTeX formatted)
- `options` (for MCQs)
- `correct_answer` (hidden by default in practice mode, revealed upon submission)
- `solution_explanation` (step-by-step verified derivation)
- `difficulty` (6-dimensional metrics: conceptual, mathematical, multi-step, abstraction, computation, trap)
- `distractor_rationales` (explaining why incorrect options are seductive)
- `provenance` (source origin or derivation reference)

### 3.6 `ladders.json`
Scaffolded learning ladders (e.g., `ladder-rot-ang-mom-01`) connecting progressive problem rungs with explicit physical deltas and reasoning depth.

### 3.7 `search_index.json`
Pre-built inverted search index mapping tokenized keywords and physics terms to target entities (chapters, topics, concepts, formulas, questions, misconceptions) with direct deep links.

---

## 4. Frontend Client Architecture

The frontend is implemented as a lightweight, zero-dependency modern ES6 SPA:
- **Routing:** Hash-based client router (`#/curriculum`, `#/chapter/:id`, `#/concept/:id`, `#/formulas`, `#/practice`, `#/ladders`, `#/search`, `#/progress`).
- **Typography & Math:** Auto-rendered KaTeX using local vendor bundle for formulas and inline expressions.
- **State Management:** Reactive local state with persistent browser storage (`localStorage`) for student practice tracking (attempts, score, bookmarks, completed topics).
- **Search Engine:** Client-side token search with term weighting and instant results navigation.
- **UI Components:** Clean sidebar navigation, breadcrumbs, content cards, interactive quiz runner, KaTeX-rendered formula blocks, collapsible derivation steps, and misconception callout alerts.
