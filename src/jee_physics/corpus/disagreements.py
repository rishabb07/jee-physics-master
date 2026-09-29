from typing import List
from jee_physics.models.corpus import SourceDisagreementRecord


DISAGREEMENTS_CATALOG: List[SourceDisagreementRecord] = [
    SourceDisagreementRecord(
        conflict_id="conflict-td-sign-001",
        conflict_category="SIGN_CONVENTION",
        topic_or_concept="First Law of Thermodynamics and Work Done",
        source_a={
            "source_id": "src-concepts-of-physics-by-h-1fd380f4",
            "source_title": "Concepts of Physics Vol. 2 (H.C. Verma)",
            "page_start": 64,
            "page_end": 66,
            "equation": "dQ = dU + dW",
            "work_definition": "W = \\int P dV (work done by the system)",
        },
        source_b={
            "source_id": "chemistry-standard-iupac",
            "source_title": "IUPAC / Chemical Thermodynamics Convention",
            "equation": "\\Delta U = q + w",
            "work_definition": "w = -\\int P_{ext} dV (work done on the system)",
        },
        nature_of_disagreement=(
            "Opposite sign conventions for mechanical work between Physics textbooks (work done by system is positive) "
            "and Chemistry / IUPAC convention (work done on system is positive)."
        ),
        explanation_and_reconciliation=(
            "In JEE Physics, the physics convention dQ = dU + dW with dW = P dV is canonical and standard across "
            "H.C. Verma, Halliday-Resnick, and University Physics. For an expansion (dV > 0), work done by gas is positive, "
            "resulting in a decrease in internal energy under adiabatic conditions (dU = -dW < 0)."
        ),
        resolution_status="RESOLVED_PHYSICS_CANONICAL_ENFORCED",
    ),
    SourceDisagreementRecord(
        conflict_id="conflict-td-free-expansion-002",
        conflict_category="VALIDITY_REGIME",
        topic_or_concept="Adiabatic Free Expansion vs Reversible Adiabatic Expansion",
        source_a={
            "source_id": "src-fundamentals-of-physics--390f40d1",
            "source_title": "Fundamentals of Physics (Halliday, Resnick, Walker)",
            "page_start": 528,
            "page_end": 532,
            "rule": "P V^\\gamma = \\text{constant} requires quasi-static reversibility",
        },
        source_b={
            "source_id": "naive-problem-banks",
            "source_title": "Unverified / Careless Question Banks",
            "rule": "Blindly applying P V^\\gamma = const to all adiabatic processes including free expansion",
        },
        nature_of_disagreement=(
            "Erroneous assumption that P V^\\gamma = const holds for any process with dQ = 0."
        ),
        explanation_and_reconciliation=(
            "Free expansion into a vacuum has dQ = 0 and dW = 0, so dU = 0 and temperature remains invariant for an ideal gas "
            "(T_f = T_i). However, the process is highly irreversible and turbulent; intermediate states have undefined pressure. "
            "Therefore P V^\\gamma = const does NOT apply to adiabatic free expansion."
        ),
        resolution_status="RESOLVED_PHYSICAL_PROOF_DOCUMENTED",
    ),
    SourceDisagreementRecord(
        conflict_id="conflict-opt-sign-003",
        conflict_category="SIGN_CONVENTION",
        topic_or_concept="Cartesian vs Real-Is-Positive Sign Convention in Geometric Optics",
        source_a={
            "source_id": "src-concepts-of-physics-by-h-a489bb6e",
            "source_title": "Concepts of Physics Vol. 1 (H.C. Verma)",
            "page_start": 378,
            "page_end": 382,
            "convention": "New Cartesian Sign Convention (pole as origin, incident light direction positive)",
        },
        source_b={
            "source_id": "src-problems-in-general-phys-6cf0b2b7",
            "source_title": "Problems in General Physics (I.E. Irodov)",
            "page_start": 195,
            "page_end": 197,
            "convention": "Real-is-positive or Gaussian coordinate convention",
        },
        nature_of_disagreement=(
            "Different coordinate orientation and sign assignments for object distances, image distances, and radii of curvature."
        ),
        explanation_and_reconciliation=(
            "JEE Main and Advanced examinations exclusively utilize the Cartesian coordinate sign convention with 1/v + 1/u = 1/f "
            "for mirrors and 1/v - 1/u = 1/f for lenses. All canonical atoms and assessments in this knowledge system enforce the "
            "Cartesian convention."
        ),
        resolution_status="RESOLVED_PHYSICS_CANONICAL_ENFORCED",
    ),
    SourceDisagreementRecord(
        conflict_id="conflict-em-units-004",
        conflict_category="TERMINOLOGY",
        topic_or_concept="SI vs Gaussian/CGS Electrodynamic Units and Field Relations",
        source_a={
            "source_id": "src-university-physics-with--0bc11b67",
            "source_title": "University Physics with Modern Physics",
            "page_start": 724,
            "page_end": 730,
            "units": "SI (MKS): D = \\varepsilon_0 E + P, B = \\mu_0 (H + M)",
        },
        source_b={
            "source_id": "src-problems-in-general-phys-6cf0b2b7",
            "source_title": "Problems in General Physics (I.E. Irodov)",
            "page_start": 373,
            "page_end": 375,
            "units": "Gaussian / CGS: D = E + 4\\pi P, B = H + 4\\pi M",
        },
        nature_of_disagreement=(
            "Presence of 4\\pi factors and fundamental permittivity/permeability constants between SI and Gaussian formulations."
        ),
        explanation_and_reconciliation=(
            "Irodov contains problems written originally in the Gaussian system and provides an explicit conversion appendix. "
            "For modern JEE Physics, SI units are strictly required. All equations and problem statements mapped into the KB "
            "are verified in SI units."
        ),
        resolution_status="RESOLVED_UNITS_NORMALIZED_TO_SI",
    ),
]


def get_all_source_disagreements() -> List[SourceDisagreementRecord]:
    """Returns the verified catalog of known source disagreements and convention variances."""
    return list(DISAGREEMENTS_CATALOG)
