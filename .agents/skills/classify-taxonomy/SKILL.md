---
name: classify-taxonomy
description: Classify verified knowledge atoms into authoritative taxonomy nodes in the JEE Physics syllabus hierarchy without altering physics content.
---

# Taxonomy Classification Protocol

## 1. Purpose
Map verified knowledge atoms to canonical nodes in `kb/taxonomy/syllabus.yaml`:
`SUBJECT` (physics) $\to$ `CHAPTER` $\to$ `TOPIC` $\to$ `SUBTOPIC` (or `EXTENSION`)

**Core Invariant:** Taxonomy classification is organizational metadata. It does NOT alter:
- Question statement
- Multiple-choice options
- Source provenance
- Source claimed answer
- Verified answer
- Verification records

---

## 2. Classification Rules
1. Inspect the atom's statement, options, diagrams, and physical concepts.
2. Search `kb/taxonomy/syllabus.yaml` for the exact matching canonical chapter, topic, and subtopic IDs.
3. If the atom matches a recognized alias (e.g. `rotation`), resolve it to the canonical ID (`rotational-motion`).
4. If an atom cannot be confidently placed ($\text{confidence} < 0.70$) or spans multiple disparate topics:
   - Assign `status = "UNMAPPED"`
   - Provide explicit explanation in `rationale`
   - DO NOT invent new taxonomy nodes.
5. If the atom involves higher-tier Olympiad physics (e.g. gyroscopic precession, relativistic mechanics), map to the appropriate `EXTENSION` node with `extension_olympiad = true`.

---

## 3. Output Schema (`TaxonomyAssignment`)
Write classification outputs to:
```text
build/staging/incoming/taxonomy_assignments/{atom_id}_taxonomy.json
```
or batch file:
```json
{
  "atom_id": "ray-optics-question-e04c1df3",
  "chapter_id": "ray-optics",
  "topic_id": "refraction-and-tir",
  "subtopic_id": "total-internal-reflection",
  "confidence": 0.99,
  "rationale": "Light ray incident normally on prism face experiencing total internal reflection at glass-water boundary.",
  "status": "PROPOSED",
  "notes": null
}
```
