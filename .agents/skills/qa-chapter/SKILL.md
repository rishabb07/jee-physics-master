---
name: qa-chapter
description: Protocols for independent chapter QA, claim verification, syllabus alignment, and LaTeX rendering checks.
---

# Chapter QA Skill

## 1. Multi-Dimensional Quality Audits
1. **Physics Audit**: Check that derivations, equations, and solutions are physically sound, dimensional, and valid.
2. **Curriculum Alignment**: Verify that all learning objectives in `ChapterSpec` are met and no unverified concepts are introduced without flagging.
3. **Editorial & Pedagogy**: Evaluate pacing, clarity, progression, and absence of jargon jumps.
4. **Rendering & LaTeX**: Validate that every LaTeX math delimiter is balanced and all math syntax is clean for KaTeX/MathJax.
5. **Traceability**: Audit claim traces to ensure 100% of claims are mapped to `CANONICAL_KB`, `SOURCE_DERIVED`, `GENERATED_AND_VERIFIED`, or `EDITORIAL_TRANSITION`.
