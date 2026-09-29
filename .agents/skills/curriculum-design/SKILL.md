---
name: curriculum-design
description: Design structured pedagogical curriculum models, prerequisite DAGs, question ladders, and chapter specifications from verified physics knowledge.
---

# Physics Curriculum Design Protocol

## 1. Prime Directives & System Invariants

1. **The Canonical Knowledge Base is the Source of Truth:**
   - Never edit, modify, or delete files in `kb/atoms/`.
   - The curriculum layer organizes verified material for learning; it does not author raw physics facts.

2. **Taxonomy $\neq$ Curriculum:**
   - Do NOT modify `kb/taxonomy/syllabus.yaml`.
   - Taxonomy is classification; curriculum is learning organization.
   - A chapter can sequence concepts and topics in an order pedagogically optimal for students, which may differ from numeric syllabus ordering.

3. **Grounding & Physics Invariant:**
   - Every substantive concept, formula, example, and question must trace to canonical verified atoms or authorized syllabus nodes.
   - Never place unverified or ambiguous questions into the curriculum.

4. **Multi-Dimensional Difficulty:**
   - Do NOT reduce difficulty to a single arbitrary number.
   - Assess 6 cognitive dimensions: conceptual, mathematical, multi-step reasoning, abstraction, computational burden, and trap/misconception difficulty.

5. **Chain of Custody:**
   - Write all generated curriculum artifacts directly to:
     `build/staging/incoming/curriculum/{chapter_id}_spec.json`
     and ladders to `build/staging/incoming/curriculum/ladders/{ladder_id}.json`
   - The parent agent must NOT create or edit these files for you.

---

## 2. Question Ladder Methodology

A Question Ladder scaffold understanding across a single physical system:
- **Level 0 (Recognition):** Identify governing laws and physical symmetries under ideal conditions.
- **Level 1 (Direct Application):** Single-formula evaluation, standard definitions, or dimensional verification.
- **Level 2 (Standard Multi-Step):** 2–3 algebraic steps combining basic equations (Standard JEE Main).
- **Level 3 (Advanced Single-Concept):** Non-routine frame of reference, deep conceptual reasoning, or subtle constraint geometry.
- **Level 4 (Advanced Multi-Concept Synthesis):** Blends two distinct domains (e.g. mechanics + electrostatics) or requires non-obvious mathematical setups.
- **Level 5 (Olympiad Extension):** Deep synthesis or continuous distributions (Irodov/Krotov tier).

Each rung must explicitly document its **physical delta** from the preceding rung.
