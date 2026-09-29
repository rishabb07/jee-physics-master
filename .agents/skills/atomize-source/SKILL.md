---
name: atomize-source
description: Extract structured, verified-ready Knowledge Atoms from multimodal physics source pages without altering source truth.
---

# Multimodal Source Atomization Skill

## 1. Overview & Core Directives

The **Atomization Agent** is an **EXTRACTION worker**, not an author, editor, or physics judge. Its role is to convert raw source pages (PDF text + visual page renderings) into discrete, structured, and auditable candidate **Knowledge Atoms** deposited in `build/staging/incoming/`, and then invoke the deterministic staging gate.

### Prime Directives:
1. **Visual Primacy:** The visual page representation is authoritative whenever extracted PDF text is corrupted, fragmented, or ambiguous (especially for mathematical formulas, superscripts, subscripts, fractions, and diagrams).
2. **Source Fidelity (Zero Pre-Verification):** Never alter, fix, or "improve" a source question, formula, or answer key. If a textbook contains a clear misprint, transcribe what is visually present, lower confidence, and record an explicit ambiguity note. The atomizer never decides whether physics is correct.
3. **No Direct Promotion:** Never write directly to `kb/atoms/`, `verification/`, or `output/`. The agent's output is an untrusted candidate JSONL file written strictly to `build/staging/incoming/`.
4. **Deterministic Gate Enforcement:** Only the Python CLI command `python -m jee_physics stage-batch <source_id> <candidate_jsonl>` validates and promotes candidate atoms into `build/staging/atoms/`.
5. **Permanent Traceability:** Every atom must contain exact provenance (source ID, source file, page range, and section/question locator) matching the authoritative source record in `sources/registry/`.

---

## 2. Operational Workflow

An Antigravity agent or subagent executing source atomization must follow this strict 10-step protocol:

1. **Select Registered Source:** Verify the `source_id` exists in `sources/registry/{source_id}.json`. Note the authoritative `file_name` and `total_pages`.
2. **Select Segment / Pages:** Identify target pages from `sources/segments/{source_id}_inventory.json`.
3. **Load Visual Representation:** Render or view target page visuals using `view_file` on high-resolution page images.
4. **Consult Raw Text as Supporting Evidence:** Check text snippets for keywords, but never trust corrupted OCR or mangled equations.
5. **Apply Visual Primacy:** Transcribe mathematical expressions and diagram references from the visual rendering.
6. **Construct Candidate Atoms:** Build Pydantic-compliant `KnowledgeAtom` dicts with appropriate taxonomy, provenance, and confidence score.
7. **Write Candidate Batch:** Write the candidate JSONL stream to:
   ```text
   build/staging/incoming/atomizer_{source_id}_{descriptor}.jsonl
   ```
8. **FORBIDDEN DESTINATIONS:**
   - NEVER write to `kb/atoms/` (canonical knowledge base).
   - NEVER write to `verification/` (reserved for blind solver and adjudication).
   - NEVER write to `output/` (reserved for publication).
9. **Execute Deterministic Staging Gate:**
   Run the CLI command via `run_command`:
   ```bash
   python -m jee_physics stage-batch <source_id> build/staging/incoming/atomizer_<source_id>_<descriptor>.jsonl
   ```
10. **Inspect Report & Verification Gate:**
    Confirm that `build/reports/atomization_{source_id}_{batch_id}.json` records clean validation, `JobManifest` is generated, and `kb/atoms/` remains empty.

---

## 3. Atomization Granularity Policy

Atoms must be **independently useful conceptual units**. Avoid both monolithic page-dumps and micro-fragmentation:

| Source Element | Target Atom Type | Granularity Rule |
| :--- | :--- | :--- |
| **Problem / Exercise** | `question` | One single problem per atom. Must contain the complete statement, all option choices (A, B, C, D), source-provided answer/solution if present, and references to any associated diagram. |
| **Worked Example** | `solved_example` | Complete problem statement plus the step-by-step solution method as presented in the source. |
| **Physics Definition / Law** | `theory` | A self-contained conceptual unit (e.g. 1–3 paragraphs explaining a physical law, its assumptions, and physical consequences). Do not split related explanatory sentences into separate atoms. |
| **Core Equation** | `formula` | Standalone mathematical identity with definitions of variables, units, and conditions of validity. |
| **Diagram / Schematic** | `figure` | Standalone technical diagram, circuit, ray diagram, or free-body diagram with bounding box metadata and descriptive caption. |
| **Physical Intuition** | `insight` | Dedicated discussion on "What does this mean physically?", limiting cases ($t \to \infty, m \to 0$), or geometric interpretations. |
| **Common Student Trap** | `misconception` | Explicit discussion in source warning against an intuitive but mathematically/physically wrong assumption. |

---

## 4. Mathematical Transcription Standards (LaTeX)

All equations must be transcribed into KaTeX-compatible LaTeX:
- **Fractions:** Use `\frac{numerator}{denominator}`. Never use loose slashes like `4 3` for $\frac{4}{3}$.
- **Trigonometric Functions:** `\sin\theta`, `\cos\alpha`, `\tan^{-1}(x)`.
- **Vectors:** `\vec{v}` or `\mathbf{v}`, and unit vectors `\hat{i}, \hat{j}, \hat{k}`.
- **Subscripts / Superscripts:** Group braces explicitly: `T_{0}`, `v_{0}`, `10^{-3}\text{ J}`, `x^{2n}`.
- **Physical Units:** Wrap in `\text{...}`: `10\text{ ms}^{-2}`, `\mu\text{F}`, `\text{N}`.
- **Square Roots:** `\sqrt{3}`, `\sqrt{2}`.

---

## 5. Confidence & Exception Routing

Confidence must be scored conservatively:
- **HIGH ($\ge 0.95$):** Visually sharp, mathematically unambiguous, text stream and image match perfectly.
- **MEDIUM ($0.85 - 0.94$):** Minor formatting ambiguity or slight visual noise, but mathematical meaning is clear.
- **LOW ($< 0.85$):** Ambiguous subscript (e.g. $v_0$ vs $v_o$), damaged scan, handwritten uncertainty, or missing vital figure label.
  - **Action for LOW confidence:** The atom is still created and staged, but an associated `ReviewQueueItem` is automatically generated in `review/queue/` documenting the uncertainty.
