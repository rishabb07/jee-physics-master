# JEE Physics Master Book — Pedagogical Style Guide

## 1. Purpose & Voice
- **Purpose:** Transform verified knowledge atoms into the most conceptually lucid, mathematically rigorous, and teacher-like learning product for JEE Advanced aspirants.
- **Voice:** First-principles, intuitive, conversational, mathematically precise. Build understanding from foundational physical intuition to deep synthesis. Never sound like a robotic transcript.

## 2. Difficulty Scale (L1–L5)
Every problem and example receives exactly one level:
- **L1 (Direct Recall / Direct Substitution):** Single-formula evaluation, standard definitions, dimensional verification.
- **L2 (Standard JEE Main):** Routine conceptual application, standard projectile/incline/circuit setups requiring 2–3 algebraic steps.
- **L3 (JEE Advanced Single-Concept Reasoning):** Non-routine frame of reference, deep conceptual reasoning, or subtle constraint geometry.
- **L4 (JEE Advanced Multi-Concept Synthesis):** Blends mechanics with electrostatics, rotational dynamics with thermodynamics, or requires non-obvious mathematical setups.
- **L5 (Olympiad-Level / Extreme Synthesis):** Generalization beyond standard JEE requirements (Irodov, Krotov, INPhO). Always tagged `OUTSIDE_JEE_SYLLABUS` if outside the official curriculum.

## 3. Question Ladders
A ladder is a structured sequence of 3 to 6 problems sharing a common physical system:
- **Rung 1:** Baseline setup under idealizing assumptions (e.g. frictionless horizontal plane).
- **Rung 2:** Introduce a single physical effect (e.g. friction).
- **Rung 3:** Alter geometry (e.g. incline with angle $\theta$).
- **Rung 4:** Couple bodies (e.g. pulley and secondary hanging mass).
- **Rung 5:** Move to an accelerating frame (pseudo-forces) or variable forces.
Each rung must feature short bridging prose explaining the physical delta.

## 4. "What Does This Mean Physically?" Callouts
- Use these callouts strategically when an equation expresses non-obvious physical behavior (e.g. limiting cases where $m \to 0$ or $t \to \infty$, sign reversals in work, or energy partitioning).
- Do not mechanically attach callouts to every trivial formula.

## 5. Mathematical Notation & LaTeX
- Use standard KaTeX-compatible LaTeX for all inline (`$...$`) and block (`$$...$$`) math.
- Vectors must use explicit vector notation (e.g. $\vec{v}$ or $\mathbf{v}$).
- Distinguish clearly between scalar magnitudes and vector components.
