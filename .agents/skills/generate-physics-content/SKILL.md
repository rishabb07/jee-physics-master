---
name: generate-physics-content
description: Guidelines and protocols for generating atomic physics instructional content (concepts, derivations, worked examples, misconceptions) grounded in verified knowledge and curriculum specs.
---

# Physics Content Generation Skill

## 1. Principles & Grounding Rules
1. **Never Ghost-Write Physics Facts**: Every claim must have an explicit `claim_traces` mapping to canonical KB atoms, official JEE syllabus topics, or authorized source references.
2. **First-Principles Rigor**:
   - For derivations: state physical system, coordinate conventions, sign conventions, fundamental conservation laws or differential equations, explicit substitutions, dimensional checks, and limiting cases.
   - For concepts: provide intuitive physical insight, formal definition, domain of validity, and prerequisite connections.
   - For worked examples: state givens, unknowns, principles used, step-by-step math, sanity checks, and alternative solution methods.
   - For misconceptions: diagnose exact erroneous mental model, provide explicit counterexamples, explain the physical truth, and provide a diagnostic check.
3. **No Direct Writing to Canonical Knowledge Base**: All content must be written to `build/staging/incoming/content/` before verification and gating.
4. **LaTeX Quality**: All math must use standard LaTeX delimiters (`$...$` for inline, `$$...$$` for block math). Avoid broken syntax or undefined macros.
