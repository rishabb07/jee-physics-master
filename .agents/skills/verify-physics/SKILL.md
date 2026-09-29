---
name: verify-physics
description: Independently solve physics questions from first principles in strict isolation from source answers or peer solutions.
---

# Blind Physics Verification Skill

## 1. Prime Directives

1. **Strict Blind Isolation:**
   - You MUST solve the problem purely from first principles.
   - You MUST NOT seek, guess, inspect, or incorporate `source_claimed_answer`, `source_solution`, or any peer solver's answers.
2. **First-Principles Derivation:**
   - Every solution must clearly state physical laws invoked (e.g. Newton's 2nd Law, Gauss's Law, Conservation of Angular Momentum, 1st Law of Thermodynamics).
   - Set up algebraic equations before substituting numerical values.
   - Verify dimensional consistency and limiting cases ($t \to 0, t \to \infty, m \to 0$, etc.).
3. **Structured Response Contract & Direct File Writing:**
   - You MUST write your solver result yourself using your file-writing tool.
   - Target destination:
     ```text
     verification/incoming/solver_{atom_id}_{solver_run_id}.json
     ```
   - Emit an unambiguous answer (e.g. Option ID "A", "B", "C", "D" or exact numerical value).
   - List explicit physical assumptions made (e.g., "assuming ideal gas", "massless string", "frictionless surface").
   - Document any interpretation of diagrams or geometric ambiguities.
   - If the problem statement lacks essential parameters, explicitly declare `uncertainty` or `possible_ambiguities` rather than guessing.

---

## 2. Input Contract

The solver receives ONLY a sanitized `BlindSolverPackage`:
- `package_id`: Unique identifier of the package.
- `atom_id`: Unique identifier of the question.
- `atom_version`: Version of the staged atom.
- `content_hash`: Content hash of the question atom.
- `blind_package_hash`: Hash of the blind package.
- `statement`: Problem statement containing KaTeX LaTeX math.
- `options`: List of multiple-choice options (if applicable).
- `figure_refs`: Diagrams and captions (if applicable).
- `difficulty`: Expected difficulty level.
- `concepts`: Core physical concepts.
- `exam_metadata`: Year/paper info (without answer keys).

---

## 3. Output Contract (JSON file written to `verification/incoming/`)

```json
{
  "solver_run_id": "run-solver_a-<uuid>",
  "solver_agent_name": "solver_a",
  "atom_id": "<atom_id>",
  "atom_version": 1,
  "content_hash": "<content_hash>",
  "verification_protocol_version": "1.0.0",
  "blind_package_hash": "<blind_package_hash>",
  "independent_answer": "C",
  "raw_answer": "Option C: first increases and then decreases",
  "reasoning_steps": [
    "Step 1: System consists of disc + insect rotating about vertical axis with zero external torque.",
    "Step 2: Angular momentum L = I(r)*omega is conserved.",
    "Step 3: As insect walks towards center, I decreases so omega increases. As it walks from center to opposite rim, I increases so omega decreases."
  ],
  "assumptions_used": [
    "No external torque acting on the system",
    "Axis of rotation remains fixed"
  ],
  "uncertainty": null,
  "diagram_interpretation": null,
  "possible_ambiguities": [],
  "created_at": "2026-09-28T01:30:00Z"
}
```

---

## 4. Forbidden Actions & Prohibited Fields

- **DO NOT** ask parent agent to copy your response.
- **DO NOT** write into `verification/records/`, `verification/solver_runs/`, `verification/manifests/`, or `kb/atoms/`.
- **DO NOT** include `source_claimed_answer`, `source_solution`, `verified_answer`, `verdict`, `adjudication_result`, `promoted`, or `promotion_status`.
- **DO NOT** search the web or codebase for answer keys.
- **DO NOT** attempt to read `verification/records/` or `sources/registry/`.
- **DO NOT** assume textbook answers are infallible.
- **DO NOT** invent missing parameters to force an answer if the problem is physically unsolvable.
