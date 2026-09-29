---
name: assemble-chapter
description: Protocols for editorial assembly of typed chapter content blocks and markdown drafts from verified content artifacts.
---

# Chapter Assembly Skill

## 1. Assembly Structure
A chapter is composed of ordered `ChapterContentBlock` structures:
- `HERO_INTRODUCTION`: Unit orientation, learning objectives, prerequisite checklist.
- `CONCEPT`: Grounded conceptual foundation and physical intuition.
- `FORMULA`: Formal mathematical statement with domain of validity and variable inventory.
- `DERIVATION`: Step-by-step rigorous proof with limiting cases.
- `WORKED_EXAMPLE`: Scaffolded pedagogical application with trap alerts and sanity checks.
- `MISCONCEPTION`: Inoculation against common cognitive traps.
- `QUESTION_LADDER`: Sequenced canonical problems progressing in difficulty.
- `CHAPTER_SUMMARY`: Formula recap and core synthesis.

## 2. Invariants
1. Only verified content (`content/verified/` or `VERIFIED` status) may be promoted into the primary draft.
2. The chapter must provide dual representations:
   - A deterministic JSON block sequence (`{chapter_id}_blocks.json`).
   - A projected readable Markdown document (`{chapter_id}_draft.md`).
3. Zero direct publication to `output/book/`. All drafts reside in `build/drafts/{chapter_id}/`.
