---
name: verify-questions
description: Protocols for independent first-principles solving, answer uniqueness verification, and distractor audits for generated physics questions.
---

# Verify Questions Skill

## Overview
This skill governs the independent verification of generated physics questions. Verification must be conducted in strict isolation from the generator's claimed answer.

## Core Protocols
1. Independent Derivation:
   - Formulate governing principles, boundary conditions, and equations independently.
   - Solve step-by-step to arrive at the calculated answer.

2. Uniqueness & Distractor Validation:
   - For single-correct MCQ: prove that exactly one option is correct.
   - Test each distractor individually: prove it is false under the problem's physical assumptions.
   - If any distractor is also valid, reject the question (`CONFLICT`).

3. Ambiguity & Feasibility Audit:
   - Check if problem lacks critical givens (e.g., unspecified reference frame, missing surface friction, ill-defined boundary).
   - Flag `AMBIGUOUS` and route to `review/queue/questions/`.

4. Risk-Calibrated Dual Verification:
   - HIGH-risk questions (multi-concept, multi-correct, complex numerical, non-trivial diagrams) require two independent solvers (Solver A + Solver B) to agree on the solution.
