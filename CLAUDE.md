# JEE Physics Master Project Guidelines

## Core Invariants
- **Source of Truth:** Canonical truth resides exclusively in `kb/`. Output in `output/` is a disposable, reproducible projection.
- **Grounding Invariant:** No unsupported generated content may be promoted into the canonical knowledge base or published output.
- **Staging Lifecycle:** Unverified extractions live in `build/staging/atoms/`. Only verified atoms enter `kb/atoms/`.
- **Archive Path:** Non-core but valid material routes to `kb/archive/`—nothing is silently lost.
- **Verification:** Risk-based (100% on high-risk/L4-L5/conflicts) + random sampling on routine extractions.
- **Exception Review:** Escalation is: Agent -> Independent Verifier -> Automated Adjudicator -> `review/queue/`. Only unresolved exceptions surface to humans.

## Commands
```bash
# System status
python -m jee_physics status

# Source registration
python -m jee_physics register-sources

# Validation
python -m jee_physics validate

# Coverage report
python -m jee_physics report --chapter <chapter_id>

# Generate JSON schemas
python -m jee_physics generate-schemas

# Run test suite
pytest
```
