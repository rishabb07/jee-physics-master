---
name: classify-subject
description: Classify source pages or segments by subject domain (Physics, Chemistry, Mathematics, Non-Content, Mixed) to enforce strict subject boundaries.
---

# Subject Classification Protocol

## 1. Purpose
Classify source pages or document segments into authoritative subject domains before knowledge atomization or canonical ingestion:
- `PHYSICS`
- `CHEMISTRY`
- `MATHEMATICS`
- `NON_CONTENT`
- `OTHER`
- `MIXED`
- `UNCERTAIN`

**Core Invariant:** Non-physics material (Chemistry, Mathematics, General instructions) must NEVER enter the canonical JEE Physics Knowledge Base.

---

## 2. Subject Detection Criteria

### PHYSICS
- **Vocabulary:** Force, acceleration, mass, velocity, torque, momentum, electric field, magnetic field, potential difference, capacitance, resistance, ray, wavelength, frequency, entropy, adiabatic, temperature, half-life.
- **Visual Markers:** Free-body diagrams, pulleys, inclined planes, circuit schematics, ray diagrams, prisms, waveforms, $P$-$V$ curves.
- **Mathematical Form:** Equations involving physical units ($\text{m/s}$, $\text{N}$, $\text{J}$, $\text{kg}$, $\text{V}$, $\text{A}$, $\mu\text{F}$, $\Omega$, $\text{T}$).

### CHEMISTRY
- **Vocabulary:** Moles, molarity, reaction rate, equilibrium constant, enthalpy, orbitals, electronegativity, hybridization, organic reactions, IUPAC names, oxidation states.
- **Visual Markers:** Molecular structures, chemical equations ($A + B \to C$), benzene rings, coordination complex formulas.

### MATHEMATICS
- **Vocabulary:** Limit, derivative, integral, matrix, determinant, vector space, ellipse, hyperbola, parabola, permutation, combination, probability, trigonometric relations without physical units.
- **Visual Markers:** Geometric coordinate plots ($x$-$y$ axes), function curves, graphs without physical units.

### MIXED
- Transitional pages where one subject finishes and another begins (e.g. Page 7 of `jee_rank_booster-03_mock_paper.pdf` where Physics Q29–Q30 finish and "PART - II CHEMISTRY" begins).

### NON_CONTENT / OTHER
- Examination instructions, cover pages, OMR sheets, syllabus tables, advertisement pages.

---

## 3. Execution Protocol
1. Inspect the page visual renderings (e.g. `build/staging/rendered_pages/page_XX.png`) or extracted page text.
2. Identify subject markers, headers, and question types.
3. Compute confidence score ($0.0$ to $1.0$).
4. If a page contains a transitional boundary, classify as `MIXED` and document the boundary in `reason`.
5. Output structured JSON record adhering strictly to `SubjectClassificationRecord`.
6. Write the candidate JSON file directly to `build/staging/incoming/subject_classifications/`.
