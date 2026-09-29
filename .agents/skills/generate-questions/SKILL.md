---
name: generate-questions
description: Protocols and requirements for generating rigorous, syllabus-aligned JEE Physics questions with authentic distractor engineering.
---

# Generate Questions Skill

## Overview
This skill governs the generation of typed, structured assessment questions (`GeneratedQuestion`) for the JEE Physics Master Knowledge System.

## Core Protocols
1. Grounding in Approved Curriculum:
   - Every question must declare its target `curriculum_id` and authoritative `taxonomy_reference`.
   - Prerequisites must be explicitly declared and supported.

2. Authentic Distractor Engineering:
   - For every incorrect option in an MCQ:
     * Detail the exact formula mistake, sign error, wrong conservation assumption, or dimensional blunder.
     * Explain why an intelligent but uncareful student would pick it.
     * Demonstrate why it is physically and mathematically false.

3. Question Types Supported:
   - `SINGLE_CORRECT_MCQ`
   - `MULTIPLE_CORRECT_MCQ`
   - `NUMERICAL`
   - `ASSERTION_REASONING`
   - `CONCEPTUAL_QUALITATIVE`
   - `MULTI_STEP_STRUCTURED`

4. Staging Isolation:
   - Output must be written directly to `build/staging/incoming/question_bank/questions/{question_id}.json`.
   - Never write to `kb/atoms/` or `question_bank/verified/`.
