---
name: chapter-planning
description: Transform approved ChapterSpec specifications into structured section-by-section pedagogical chapter blueprints.
---

# Physics Chapter Planning Protocol

## 1. Prime Directives & Invariants

1. **Grounded Blueprints:**
   - Every section in the `ChapterPlan` must explicitly cite its approved concepts, formula IDs, worked example IDs, question atom IDs, and misconception IDs from the parent `ChapterSpec`.
   - Do NOT invent unapproved questions or formulas.

2. **No Final Prose:**
   - Do NOT write final narrative textbook paragraphs.
   - Stop at the structured section-by-section plan detailing pedagogical purpose, concept flow, formula placements, and question anchors.

3. **Honest Gap Identification:**
   - When a required explanation or worked example does not exist in the canonical knowledge base, log it explicitly in `unresolved_gaps`.
   - Never synthesize fake facts to disguise missing content.

4. **Chain of Custody:**
   - Write your structured `ChapterPlan` directly to:
     `build/staging/incoming/curriculum/{chapter_id}_plan.json`
   - The parent agent must NOT create or edit these files for you.
