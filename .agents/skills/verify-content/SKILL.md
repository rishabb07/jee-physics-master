---
name: verify-content
description: Independent physics verification protocols for instructional content, derivations, and worked examples.
---

# Content Verification Skill

## 1. Verification Dimensions
Every generated physics block must undergo rigorous verification according to risk level:
- **Assumptions Audit**: Are all physical idealizations (e.g. rigid body, frictionless surface, ideal gas, paraxial rays, ohmic conductor) explicitly declared?
- **Dimensional Homogeneity**: Do all intermediate and final equations have matching SI units and dimensional formula?
- **Limiting & Boundary Cases**: Do equations reduce correctly under extreme physical limits (e.g. $m \\to 0$, $v \\ll c$, $\\theta \\to 0$, $R \\to \\infty$)?
- **Numerical & Algebraic Consistency**: Are arithmetic evaluations error-free with consistent significant figures?
- **Claim Trace Validity**: Are claims correctly categorized as `CANONICAL_KB`, `SOURCE_DERIVED`, `GENERATED_AND_VERIFIED`, or `EDITORIAL_TRANSITION`?

## 2. Inviolable Invariant
Verification records must be cryptographically bound to the content hash (`content_hash`) of the substantive payload. If content is edited post-verification, verification status is automatically `INVALIDATED`.
