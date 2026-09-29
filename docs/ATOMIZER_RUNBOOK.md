# Multimodal Atomizer Operator Runbook

This document defines the standard operating procedure for human operators, orchestrators, and AI agents executing the **Atomization Stage** of the JEE Physics Master Knowledge System.

---

## Architecture Overview

```
+-------------------------------------------------------------------+
|                   ANTIGRAVITY COGNITIVE AGENT                     |
|                                                                   |
| 1. Read sources/registry/{source_id}.json                         |
| 2. Read sources/segments/{source_id}_inventory.json               |
| 3. Render/view page images (Visual Primacy Rule)                  |
| 4. Extract atoms & transcribe LaTeX                               |
| 5. Write candidate JSONL: build/staging/incoming/{filename}.jsonl |
+---------------------------------+---------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|               DETERMINISTIC PYTHON STAGING BOUNDARY               |
|                                                                   |
| Command:                                                          |
|   python -m jee_physics stage-batch <source_id> <candidate_file>  |
|                                                                   |
| Actions:                                                          |
| - Validates against Pydantic schema                               |
| - Verifies provenance against sources/registry/                   |
| - Enforces page bounds [1..total_pages]                           |
| - Lints LaTeX syntax and delimiters                               |
| - Forces verification_status = STAGED (Anti-Self-Promotion)       |
| - Recomputes deterministic content SHA-256                        |
| - Writes to build/staging/atoms/{batch_id}.jsonl                  |
| - Generates JobManifest in build/staging/manifests/               |
| - Writes report in build/reports/                                 |
| - Routes confidence < 0.85 to review/queue/                       |
+-------------------------------------------------------------------+
```

---

## Step-by-Step Operator Instructions

### Step 1: Identify Registered Source
Confirm that the source is registered and obtain its `source_id`:
```bash
python -m jee_physics status
```
Inspect the registration record in `sources/registry/{source_id}.json`. Note:
- `file_name`
- `total_pages`
- `sha256`

### Step 2: Select Segment / Target Page Range
Consult `sources/segments/{source_id}_inventory.json` or `_segments.json` to select the page range for the current run (e.g. pages 4–5).

### Step 3: Load Visual Page Representation
Ensure target pages are rendered at high resolution for visual inspection:
```bash
python -c "import pymupdf, os; os.makedirs('build/staging/rendered_pages', exist_ok=True); doc = pymupdf.open('sources/raw/<file_name>'); doc[p-1].get_pixmap(dpi=200).save('build/staging/rendered_pages/page_<p>.png')"
```
Open each image using `view_file` to inspect mathematical notation, figures, and options.

### Step 4: Apply Visual Primacy & Transcribe
Follow [`.agents/skills/atomize-source/SKILL.md`](../.agents/skills/atomize-source/SKILL.md):
- Keep whole questions intact with all options.
- Transcribe mathematics into KaTeX LaTeX (`$...$`).
- Record diagram references and captions.
- Retain exact source answers without editing or verification.

### Step 5: Write Untrusted Candidate JSONL
Write candidate atoms line-by-line into:
```text
build/staging/incoming/atomizer_{source_id}_pages_{start}_{end}.jsonl
```

### Step 6: Execute Deterministic Staging Gate
Run the staging validation command:
```bash
python -m jee_physics stage-batch <source_id> build/staging/incoming/atomizer_<source_id>_pages_<start}_{end}.jsonl
```

### Step 7: Inspect Execution Report
Examine the generated report in:
```text
build/reports/atomization_{source_id}_{batch_id}.json
```
Verify:
1. `validation_failures == 0`
2. `total_atoms_staged > 0`
3. `pages_with_no_atoms` is empty (all target pages accounted for)
4. `kb/atoms/` remains untouched (0 canonical atoms written)

### Step 8: Complete
The candidate batch is now securely staged in `build/staging/atoms/` and ready for the Phase 4 Blind Verification Agent.
