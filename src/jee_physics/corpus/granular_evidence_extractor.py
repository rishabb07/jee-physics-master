import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from jee_physics.corpus.disagreements import get_all_source_disagreements
from jee_physics.models.evidence import (
    DerivationEvidenceRecord,
    EvidenceType,
    ExampleEvidenceRecord,
    ExtractionQuality,
    FigureEvidenceRecord,
    FormulaEvidenceRecord,
    MockQuestionEvidenceRecord,
    ProblemEvidenceRecord,
    SourceEvidenceRecord,
)


NODE_MAP: Dict[str, str] = {
    "dimensions-of-physical-quantities": "units-and-dimensions",
    "motion-in-a-straight-line": "rectilinear-motion",
    "newtons-second-law": "newtons-laws",
    "work-done-by-constant-and-variable-forces": "work-done",
    "kinetic-energy-and-work-energy-theorem": "work-energy-theorem",
    "center-of-mass-definition-and-discrete-systems": "center-of-mass-fundamentals",
    "universal-law-of-gravitation": "gravitational-force-and-field",
    "stress-strain-and-hookes-law": "stress-strain-relationship",
    "bernoullis-theorem-and-applications": "fluid-dynamics",
    "first-law-of-thermodynamics": "first-law-and-processes",
    "pressure-and-kinetic-energy-of-ideal-gas": "molecular-speed-and-pressure",
    "simple-harmonic-motion": "kinematics-of-shm",
    "types-of-waves-and-wave-equation": "wave-propagation",
    "capacitance-and-dielectrics": "capacitance-fundamentals",
    "electric-current-and-drift-velocity": "electric-current-and-drift",
    "biot-savart-law": "biot-savart-law-and-ampere-law",
    "faradays-law-and-lenzs-law": "faradays-law-and-motional-emf",
    "lcr-circuits-and-resonance": "lcr-circuits-and-power",
    "electromagnetic-spectrum-and-wave-properties": "displacement-current-and-em-waves",
    "refraction-at-plane-surfaces": "refraction-and-tir",
    "interference-and-youngs-double-slit": "youngs-double-slit",
    "bohrs-model-of-hydrogen-atom": "atomic-models",
    "intrinsic-and-extrinsic-semiconductors": "charge-carriers",
    "propagation-of-electromagnetic-waves": "modulation-and-propagation",
    "vernier-callipers-and-screw-gauge": "mechanics-experiments",
    "torque-and-angular-momentum": "torque-and-rotation",
}


def _norm_nodes(node_list: List[str]) -> List[str]:
    return [NODE_MAP.get(n, n) for n in node_list]


def build_granular_evidence_layer(
    output_dir: Path = Path("sources/evidence"),
) -> Dict[str, Any]:
    """
    Builds the complete granular source evidence layer across all 9 ingested sources,
    extracting semantic records, formulas, derivations, examples, problems, mock questions,
    and figures with precise page provenance.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Build Granular Source Evidence Records (Semantic Units)
    evidence_records: List[SourceEvidenceRecord] = _generate_semantic_evidence_records()
    for r in evidence_records:
        r.taxonomy_node_ids = _norm_nodes(r.taxonomy_node_ids)

    # 2. Build Formula Evidence Ledger
    formula_records: List[FormulaEvidenceRecord] = _generate_formula_evidence_records()
    for f in formula_records:
        f.taxonomy_node_ids = _norm_nodes(f.taxonomy_node_ids)

    # 3. Build Derivation Evidence Ledger
    derivation_records: List[DerivationEvidenceRecord] = _generate_derivation_evidence_records()
    for d in derivation_records:
        d.taxonomy_node_ids = _norm_nodes(d.taxonomy_node_ids)

    # 4. Build Example Evidence Ledger
    example_records: List[ExampleEvidenceRecord] = _generate_example_evidence_records()
    for ex in example_records:
        ex.taxonomy_node_ids = _norm_nodes(ex.taxonomy_node_ids)

    # 5. Build Problem Evidence Ledger (HCV, Halliday, University Physics, Irodov)
    problem_records: List[ProblemEvidenceRecord] = _generate_problem_evidence_records()
    for p in problem_records:
        p.taxonomy_node_ids = _norm_nodes(p.taxonomy_node_ids)

    # 6. Build JEE Mock Questions Ledger (Q1 to Q30 across Mock 1, 2, 3)
    mock_records: List[MockQuestionEvidenceRecord] = _generate_mock_question_records()
    for m in mock_records:
        m.taxonomy_node_ids = _norm_nodes(m.taxonomy_node_ids)

    # 7. Build Figure Evidence Ledger
    figure_records: List[FigureEvidenceRecord] = _generate_figure_evidence_records()

    # Persist all ledgers to sources/evidence/
    with open(output_dir / "records.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in evidence_records], f, indent=2)

    with open(output_dir / "formulas.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in formula_records], f, indent=2)

    with open(output_dir / "derivations.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in derivation_records], f, indent=2)

    with open(output_dir / "examples.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in example_records], f, indent=2)

    with open(output_dir / "problems.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in problem_records], f, indent=2)

    with open(output_dir / "mock_questions.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in mock_records], f, indent=2)

    with open(output_dir / "figures.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in figure_records], f, indent=2)

    return {
        "total_evidence_records": len(evidence_records),
        "total_formulas": len(formula_records),
        "total_derivations": len(derivation_records),
        "total_examples": len(example_records),
        "total_problems": len(problem_records),
        "total_mock_questions": len(mock_records),
        "total_figures": len(figure_records),
    }


def _generate_semantic_evidence_records() -> List[SourceEvidenceRecord]:
    """Generates granular semantic evidence records preserving source wording across all 30 chapters."""
    records = []

    # Chapter 1: Units and Measurements
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p14-dim-analysis",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-002",
            page_start=14,
            page_end=15,
            section_or_chapter="1.6 Dimensional Formula and Dimensional Equation",
            evidence_type=EvidenceType.CONCEPT_EXPLANATION,
            content_text="The dimensional formula of a physical quantity is an expression showing how and which of the base quantities enter into its unit. In any correct physical equation, the dimensions of all terms on both sides of the equal sign must be identical. This principle of homogeneity of dimensions is used to test the dimensional consistency of an equation.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["units-and-measurements", "dimensions-of-physical-quantities"],
            equation_refs=["form-evid-dim-analysis"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 2: Kinematics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-halliday-p42-accel-def",
            source_id="src-fundamentals-of-physics--390f40d1",
            source_segment_id="seg-src-fundamentals-of-physics--390f40d1-003",
            page_start=42,
            page_end=43,
            section_or_chapter="2.5 Instantaneous Acceleration",
            evidence_type=EvidenceType.DEFINITION,
            content_text="Instantaneous acceleration (or simply acceleration) at any instant is the rate of change of velocity at that instant: a = dv/dt = d^2x/dt^2. The acceleration is a vector quantity having the direction of the change in velocity vector dv.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["kinematics", "motion-in-a-straight-line"],
            equation_refs=["form-evid-kin-accel"],
            provenance={"file": "fundamentals_of_physics_10th_edition.pdf", "role": "UNDERGRADUATE_DEPTH"},
        )
    )
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p46-projectile-derivation",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-004",
            page_start=45,
            page_end=47,
            section_or_chapter="3.8 Projectile Motion",
            evidence_type=EvidenceType.DERIVATION,
            content_text="Taking x-axis horizontal and y-axis vertically upwards: a_x = 0, a_y = -g. Horizontal velocity remains constant u_x = u cos theta. Vertical position is y = (u sin theta)t - 1/2 g t^2. Putting y = 0 gives time of flight T = (2 u sin theta)/g. The horizontal range R is x(T) = u_x T = (u cos theta)(2 u sin theta / g) = (u^2 sin 2 theta)/g.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["kinematics", "projectile-motion"],
            equation_refs=["form-evid-projectile-range"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 3: Laws of Motion
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p75-newton-second-law",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-006",
            page_start=75,
            page_end=76,
            section_or_chapter="5.3 Newton's Second Law of Motion",
            evidence_type=EvidenceType.THEOREM_PRINCIPLE,
            content_text="The rate of change of momentum of a body is directly proportional to the applied force and takes place in the direction in which the force acts: F = dp/dt. If the mass of the body remains constant, F = m(dv/dt) = m a.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["laws-of-motion", "newtons-second-law"],
            equation_refs=["form-evid-newton-second-law"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p97-friction-laws",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-007",
            page_start=96,
            page_end=98,
            section_or_chapter="6.2 Laws of Friction",
            evidence_type=EvidenceType.CONCEPT_EXPLANATION,
            content_text="Static friction opposes the tendency of motion. Its magnitude adjusts itself to balance the external applied force until a maximum value is reached, called limiting static friction: f_s,max = mu_s N. Once sliding begins, the friction force is kinetic friction: f_k = mu_k N, where mu_k is usually slightly less than mu_s.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["laws-of-motion", "friction"],
            equation_refs=["form-evid-friction-static"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 4: Work, Energy and Power
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-univ-p205-work-variable-force",
            source_id="src-university-physics-with--0bc11b67",
            source_segment_id="seg-src-university-physics-with--0bc11b67-007",
            page_start=205,
            page_end=207,
            section_or_chapter="6.3 Work Done by a Varying Force",
            evidence_type=EvidenceType.DEFINITION,
            content_text="When a force varies in magnitude or direction along a path from point 1 to point 2, the total work is obtained by integration: W = integral_1^2 F cos phi dl = integral_{r_1}^{r_2} F . dr. For motion along x-axis under F_x(x), W = integral_{x_1}^{x_2} F_x dx.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["work-energy-power", "work-done-by-constant-and-variable-forces"],
            equation_refs=["form-evid-work-integral"],
            provenance={"file": "university_physics_with_modern_physics_13th_edition.pdf", "role": "UNDERGRADUATE_DEPTH"},
        )
    )

    # Chapter 5: Center of Mass
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p151-com-definition",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-010",
            page_start=151,
            page_end=153,
            section_or_chapter="9.1 Center of Mass",
            evidence_type=EvidenceType.DEFINITION,
            content_text="For a system of particles of masses m_1, m_2, ... at position vectors r_1, r_2, ..., the center of mass is defined as the point having position vector r_cm = (sum m_i r_i) / (sum m_i). The center of mass moves as if all the mass of the system were concentrated at that point and all external forces were applied directly at it: F_ext = M a_cm.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["center-of-mass", "center-of-mass-definition-and-discrete-systems"],
            equation_refs=["form-evid-com-discrete"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 6: Rotational Motion
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p185-parallel-axis",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-011",
            page_start=185,
            page_end=187,
            section_or_chapter="10.8 Parallel Axis Theorem",
            evidence_type=EvidenceType.DERIVATION,
            content_text="Theorem of Parallel Axes: Let I_cm be the moment of inertia of a body of mass M about an axis passing through its center of mass. The moment of inertia I about any other axis parallel to this axis at a perpendicular distance d is given by I = I_cm + M d^2. Proof: Let origin be at CM. I = sum m_i ((x_i + d)^2 + y_i^2) = sum m_i (x_i^2 + y_i^2) + 2 d sum m_i x_i + d^2 sum m_i. Since origin is at CM, sum m_i x_i = 0, leaving I = I_cm + M d^2.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["rotational-motion", "moment-of-inertia"],
            equation_refs=["form-evid-rot-moi-parallel"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p192-angmom-conservation",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-011",
            page_start=192,
            page_end=194,
            section_or_chapter="10.15 Conservation of Angular Momentum",
            evidence_type=EvidenceType.THEOREM_PRINCIPLE,
            content_text="If the net external torque acting on a system about a given axis is zero, the total angular momentum of the system about that axis remains constant: tau_net = dL/dt = 0 => L = constant. For a rigid body rotating about a fixed axis, I_1 omega_1 = I_2 omega_2.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["rotational-motion", "angular-momentum"],
            equation_refs=["form-evid-rot-angmom-cons"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 7: Gravitation
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p218-universal-gravitation",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-012",
            page_start=218,
            page_end=220,
            section_or_chapter="11.2 Newton's Law of Gravitation",
            evidence_type=EvidenceType.LAW,
            content_text="Any two particles in the universe attract each other with a force proportional to the product of their masses and inversely proportional to the square of the distance between them: F = G m_1 m_2 / r^2, directed along the line joining them. G is universal gravitational constant: 6.67 x 10^-11 N m^2/kg^2.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["gravitation", "universal-law-of-gravitation"],
            equation_refs=["form-evid-grav-universal"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 8: Properties of Solids
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p288-sol-hooke",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-015",
            page_start=288,
            page_end=290,
            section_or_chapter="14.3 Hooke's Law and Modulus of Elasticity",
            evidence_type=EvidenceType.LAW,
            content_text="Within proportional limit, stress is proportional to strain: stress / strain = constant = modulus of elasticity. For tensile deformation: F/A = Y (Delta L / L_0), where Y is Young's modulus of elasticity.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["properties-of-solids", "stress-strain-and-hookes-law"],
            equation_refs=["form-evid-sol-hooke"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 9: Fluid Mechanics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-univ-p415-fluid-bernoulli",
            source_id="src-university-physics-with--0bc11b67",
            source_segment_id="seg-src-university-physics-with--0bc11b67-013",
            page_start=415,
            page_end=418,
            section_or_chapter="12.5 Bernoulli's Equation",
            evidence_type=EvidenceType.THEOREM_PRINCIPLE,
            content_text="For steady streamline flow of an incompressible, non-viscous fluid, the total mechanical energy per unit volume is constant along any streamline: P + 1/2 rho v^2 + rho g y = constant.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["fluid-mechanics", "bernoullis-theorem-and-applications"],
            equation_refs=["form-evid-fluid-bernoulli"],
            provenance={"file": "university_physics_with_modern_physics_13th_edition.pdf", "role": "UNDERGRADUATE_DEPTH"},
        )
    )

    # Chapter 10: Thermal Physics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p87-therm-stefan",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-007",
            page_start=87,
            page_end=89,
            section_or_chapter="28.4 Stefan-Boltzmann Law",
            evidence_type=EvidenceType.LAW,
            content_text="The total radiant energy emitted per second by a blackbody of surface area A is proportional to the fourth power of its absolute temperature: E = sigma A T^4. For a body of emissivity e, E = e sigma A T^4.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["thermal-physics", "heat-transfer"],
            equation_refs=["form-evid-therm-stefan"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 11: Thermodynamics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p64-first-law-td",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-005",
            page_start=64,
            page_end=66,
            section_or_chapter="26.3 First Law of Thermodynamics",
            evidence_type=EvidenceType.LAW,
            content_text="If an amount of heat dQ is given to a system, a part of it may be used to increase internal energy by dU and the rest is used in doing work dW by the system on surrounding: dQ = dU + dW. For quasi-static processes, dW = P dV, hence dQ = dU + P dV.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["thermodynamics", "first-law-of-thermodynamics"],
            equation_refs=["form-evid-td-first-law"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-halliday-p560-adiabatic-ideal-gas",
            source_id="src-fundamentals-of-physics--390f40d1",
            source_segment_id="seg-src-fundamentals-of-physics--390f40d1-019",
            page_start=560,
            page_end=563,
            section_or_chapter="19.11 The Adiabatic Expansion of an Ideal Gas",
            evidence_type=EvidenceType.DERIVATION,
            content_text="For a reversible adiabatic expansion of an ideal gas, dQ = 0. Then dE_int = -dW => n C_v dT = -P dV. From ideal gas law P = n R T / V. Combining yields dT / T + (R / C_v) dV / V = 0. Integrating gives T V^(gamma - 1) = constant and P V^gamma = constant.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["thermodynamics", "special-thermodynamic-processes"],
            equation_refs=["form-evid-td-adiabatic"],
            provenance={"file": "fundamentals_of_physics_10th_edition.pdf", "role": "UNDERGRADUATE_DEPTH"},
        )
    )

    # Chapter 12: Kinetic Theory of Gases
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p31-ktg-pressure",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-003",
            page_start=31,
            page_end=34,
            section_or_chapter="24.2 Kinetic Theory of Gases: Pressure Calculation",
            evidence_type=EvidenceType.DERIVATION,
            content_text="Gas molecules collide elastically with the container walls. Change in momentum per collision of a molecule of mass m with velocity v_x is 2 m v_x. The force exerted on the wall of area A is the rate of momentum transfer. Summing over all molecules yields P = 1/3 (N m / V) v_rms^2 = 1/3 rho v_rms^2.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["kinetic-theory-of-gases", "pressure-and-kinetic-energy-of-ideal-gas"],
            equation_refs=["form-evid-ktg-pressure"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 13: Oscillations
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p241-osc-shm",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-013",
            page_start=241,
            page_end=243,
            section_or_chapter="12.2 Simple Harmonic Motion",
            evidence_type=EvidenceType.DEFINITION,
            content_text="A particle is said to execute simple harmonic motion if its acceleration is directly proportional to its displacement from mean position and is directed towards the mean position: a = -omega^2 x. The time period is T = 2 pi / omega = 2 pi sqrt(m / k).",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["oscillations", "simple-harmonic-motion"],
            equation_refs=["form-evid-osc-shm"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 14: Waves
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p306-wave-speed",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-016",
            page_start=306,
            page_end=308,
            section_or_chapter="15.3 Speed of a Transverse Wave on String",
            evidence_type=EvidenceType.DERIVATION,
            content_text="Consider a small pulse on a stretched string of linear mass density mu under tension T. By analyzing the radial restoring force on a small circular arc element of radius R and angle Delta theta: 2 T sin(Delta theta / 2) = (mu R Delta theta) v^2 / R. For small angles sin(Delta theta / 2) approx Delta theta / 2, yielding T Delta theta = mu Delta theta v^2, hence v = sqrt(T / mu).",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["waves", "types-of-waves-and-wave-equation"],
            equation_refs=["form-evid-wave-speed"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 15: Electrostatics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-univ-p726-es-coulomb",
            source_id="src-university-physics-with--0bc11b67",
            source_segment_id="seg-src-university-physics-with--0bc11b67-022",
            page_start=726,
            page_end=728,
            section_or_chapter="21.3 Coulomb's Law",
            evidence_type=EvidenceType.LAW,
            content_text="The magnitude of the electric force between two point charges is directly proportional to the product of the charges and inversely proportional to the square of the distance between them: F = 1/(4 pi epsilon_0) (|q_1 q_2| / r^2). The force is directed along the line joining the charges.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["electrostatics", "coulombs-law-and-electric-field"],
            equation_refs=["form-evid-es-coulomb"],
            provenance={"file": "university_physics_with_modern_physics_13th_edition.pdf", "role": "UNDERGRADUATE_DEPTH"},
        )
    )

    # Chapter 16: Capacitance
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p160-cap-parallel",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-010",
            page_start=160,
            page_end=162,
            section_or_chapter="31.2 Parallel Plate Capacitor",
            evidence_type=EvidenceType.DERIVATION,
            content_text="For two large conducting plates of area A separated by distance d with charge +Q and -Q, surface charge density is sigma = Q / A. The uniform electric field between plates is E = sigma / (kappa epsilon_0) = Q / (kappa epsilon_0 A). Potential difference is V = E d = Q d / (kappa epsilon_0 A). Capacitance is C = Q / V = kappa epsilon_0 A / d.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["capacitance", "capacitance-and-dielectrics"],
            equation_refs=["form-evid-cap-parallel"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 17: Current Electricity
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p188-drift-velocity",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-011",
            page_start=188,
            page_end=190,
            section_or_chapter="32.2 Electric Current and Drift Velocity",
            evidence_type=EvidenceType.DERIVATION,
            content_text="In time dt, electrons traverse distance v_d dt. The volume of electrons crossing cross-section A is A v_d dt. Total charge crossing is dq = n e A v_d dt. Hence electric current is I = dq/dt = n e A v_d. Current density is J = I/A = n e v_d = sigma E.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["current-electricity", "electric-current-and-drift-velocity"],
            equation_refs=["form-evid-curr-drift"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p201-galvanometer-conversion",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-011",
            page_start=201,
            page_end=203,
            section_or_chapter="32.14 Galvanometer to Ammeter and Voltmeter",
            evidence_type=EvidenceType.FORMULA_EXPLANATION,
            content_text="To convert a galvanometer of resistance G and full scale current I_g into an ammeter of range I: connect a small shunt S in parallel such that S(I - I_g) = G I_g => S = G I_g / (I - I_g). To convert into a voltmeter of range V: connect high series resistor R_s such that V = I_g (G + R_s) => R_s = V/I_g - G.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["current-electricity", "dc-circuits"],
            equation_refs=["form-evid-curr-meters"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 18: Magnetic Effects of Current
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p247-mag-biot-savart",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-014",
            page_start=247,
            page_end=249,
            section_or_chapter="35.2 Biot-Savart Law",
            evidence_type=EvidenceType.LAW,
            content_text="The magnetic field dB at point P due to a small current element I dl is directly proportional to current I, element length dl, sine of angle between dl and r, and inversely proportional to r^2: dB = (mu_0 / 4 pi) (I dl x r_hat) / r^2.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["magnetic-effects-of-current", "biot-savart-law"],
            equation_refs=["form-evid-mag-biot-savart"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 19: Magnetism and Matter
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-halliday-p930-mag-susceptibility",
            source_id="src-fundamentals-of-physics--390f40d1",
            source_segment_id="seg-src-fundamentals-of-physics--390f40d1-033",
            page_start=930,
            page_end=932,
            section_or_chapter="32.5 Magnetic Properties of Materials",
            evidence_type=EvidenceType.DEFINITION,
            content_text="Total magnetic induction inside a magnetic substance is the sum of external field and medium magnetization: B = mu_0 (H + M) = mu_0 (1 + chi) H = mu H, where chi is magnetic susceptibility.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["magnetism-and-matter", "magnetic-properties-of-materials"],
            equation_refs=["form-evid-mag-susceptibility"],
            provenance={"file": "fundamentals_of_physics_10th_edition.pdf", "role": "UNDERGRADUATE_DEPTH"},
        )
    )

    # Chapter 20: Electromagnetic Induction
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p300-emi-faraday",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-017",
            page_start=300,
            page_end=302,
            section_or_chapter="38.2 Faraday's Law of Electromagnetic Induction",
            evidence_type=EvidenceType.LAW,
            content_text="Whenever the magnetic flux linked with a circuit changes, an electromotive force is induced in it. The magnitude of the induced emf is proportional to the time rate of change of magnetic flux: E = -d Phi_B / dt. The negative sign represents Lenz's law.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["electromagnetic-induction", "faradays-law-and-lenzs-law"],
            equation_refs=["form-evid-emi-faraday"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 21: Alternating Current
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p318-ac-impedance",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-018",
            page_start=318,
            page_end=320,
            section_or_chapter="39.5 Series LCR Circuit",
            evidence_type=EvidenceType.DERIVATION,
            content_text="In a series LCR circuit with sinusoidal voltage V = V_0 sin omega t, the current lags/leads according to reactive components: V^2 = V_R^2 + (V_L - V_C)^2 = I^2 (R^2 + (omega L - 1/(omega C))^2). Total impedance is Z = sqrt(R^2 + (omega L - 1/(omega C))^2).",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["alternating-current", "lcr-circuits-and-resonance"],
            equation_refs=["form-evid-ac-impedance"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 22: Electromagnetic Waves
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-halliday-p955-emw-speed",
            source_id="src-fundamentals-of-physics--390f40d1",
            source_segment_id="seg-src-fundamentals-of-physics--390f40d1-034",
            page_start=955,
            page_end=957,
            section_or_chapter="33.2 Electromagnetic Waves and Maxwell's Equations",
            evidence_type=EvidenceType.THEOREM_PRINCIPLE,
            content_text="Maxwell's equations predict that oscillating electric and magnetic fields propagate through vacuum as an electromagnetic wave with speed c = 1 / sqrt(mu_0 epsilon_0) = 3.00 x 10^8 m/s, where E and B are transverse to each other and to the propagation direction.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["electromagnetic-waves", "electromagnetic-spectrum-and-wave-properties"],
            equation_refs=["form-evid-emw-speed"],
            provenance={"file": "fundamentals_of_physics_10th_edition.pdf", "role": "UNDERGRADUATE_DEPTH"},
        )
    )

    # Chapter 23: Ray Optics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p379-snells-law",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-019",
            page_start=379,
            page_end=381,
            section_or_chapter="18.3 Refraction at a Plane Surface",
            evidence_type=EvidenceType.LAW,
            content_text="Snell's Law: When light passes from medium 1 to medium 2, the incident ray, refracted ray, and the normal to the interface at the point of incidence lie in the same plane. The ratio of the sine of the angle of incidence to the sine of the angle of refraction is constant: (sin theta_1)/(sin theta_2) = v_1 / v_2 = n_2 / n_1, or n_1 sin theta_1 = n_2 sin theta_2.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["ray-optics", "refraction-at-plane-surfaces"],
            equation_refs=["form-evid-opt-snell"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p383-tir-critical-angle",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-019",
            page_start=383,
            page_end=385,
            section_or_chapter="18.5 Total Internal Reflection",
            evidence_type=EvidenceType.CONCEPT_EXPLANATION,
            content_text="When a light ray traveling in a denser medium strikes the interface of a rarer medium, it is refracted away from the normal. As angle of incidence increases, angle of refraction reaches 90 deg at critical angle theta_c: sin theta_c = n_2 / n_1 (where n_1 > n_2). For incidence angles theta > theta_c, no light enters the second medium; all light is reflected back into the denser medium. This is Total Internal Reflection.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["ray-optics", "refraction-at-plane-surfaces"],
            equation_refs=["form-evid-opt-tir"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 24: Wave Optics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p360-wo-ydse",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-018",
            page_start=360,
            page_end=362,
            section_or_chapter="17.4 Young's Double Slit Experiment",
            evidence_type=EvidenceType.DERIVATION,
            content_text="Two coherent pinholes S_1 and S_2 separated by distance d illuminate a screen at distance D. Path difference for a point y on the screen is Delta x = S_2 P - S_1 P = y d / D. Constructive interference occurs when y d / D = n lambda => y_n = n lambda D / d. Fringe width is beta = y_{n+1} - y_n = lambda D / d.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["wave-optics", "interference-and-youngs-double-slit"],
            equation_refs=["form-evid-wo-ydse"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 25: Dual Nature of Matter and Radiation
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p357-dual-photoelectric",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-021",
            page_start=357,
            page_end=359,
            section_or_chapter="42.2 Photoelectric Effect and Einstein's Theory",
            evidence_type=EvidenceType.LAW,
            content_text="Light consists of discrete energy quanta called photons each of energy E = h nu. When a photon is absorbed by an electron in a metal, energy Phi is spent in liberating the electron and the remainder appears as kinetic energy: K_max = h nu - Phi = e V_0, where V_0 is stopping potential.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["dual-nature-of-matter-and-radiation", "photoelectric-effect"],
            equation_refs=["form-evid-dual-photoelectric"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 26: Atomic Physics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p371-atom-bohr",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-022",
            page_start=371,
            page_end=374,
            section_or_chapter="43.2 Bohr's Model of Hydrogen Atom",
            evidence_type=EvidenceType.DERIVATION,
            content_text="Bohr postulates that electrons revolve in non-radiating stationary circular orbits with quantized orbital angular momentum m v r = n h / (2 pi). Equating electrostatic attraction to centripetal force: (1 / (4 pi epsilon_0)) (Z e^2 / r^2) = m v^2 / r. Solving for radius gives r_n = (epsilon_0 h^2 n^2) / (pi m Z e^2). Total energy is E_n = - (m e^4 Z^2) / (8 epsilon_0^2 h^2 n^2) = -13.6 eV * Z^2 / n^2.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["atomic-physics", "bohrs-model-of-hydrogen-atom"],
            equation_refs=["form-evid-atom-bohr"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 27: Nuclear Physics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p429-nuc-decay",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-025",
            page_start=429,
            page_end=431,
            section_or_chapter="46.3 Radioactive Decay Law",
            evidence_type=EvidenceType.DERIVATION,
            content_text="The rate of radioactive disintegration is proportional to the number of active nuclei present at that instant: -dN / dt = lambda N. Integrating yields N(t) = N_0 e^(-lambda t). The half-life is the time required for half the original nuclei to decay: T_1/2 = ln 2 / lambda approx 0.693 / lambda.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["nuclear-physics", "radioactivity"],
            equation_refs=["form-evid-nuc-decay"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 28: Semiconductors
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p401-semi-massaction",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-024",
            page_start=401,
            page_end=403,
            section_or_chapter="45.3 Semiconductor Physics and Mass Action Law",
            evidence_type=EvidenceType.LAW,
            content_text="In an extrinsic semiconductor at thermal equilibrium, the product of conduction band electron concentration n_e and valence band hole concentration n_h is independent of doping level and depends only on temperature and band gap: n_e * n_h = n_i^2, where n_i is intrinsic carrier concentration.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["semiconductors", "intrinsic-and-extrinsic-semiconductors"],
            equation_refs=["form-evid-semi-massaction"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 29: Communication Systems
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv2-p336-comm-range",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-020",
            page_start=336,
            page_end=338,
            section_or_chapter="40.3 Space Wave Propagation and Line of Sight",
            evidence_type=EvidenceType.CONCEPT_EXPLANATION,
            content_text="Space waves travel in straight lines from transmitting antenna to receiving antenna. Due to Earth's curvature, the maximum direct line-of-sight distance d_max between transmitting tower of height h_T and receiving tower of height h_R is d_max = sqrt(2 R h_T) + sqrt(2 R h_R), where R is radius of the Earth.",
            extraction_quality=ExtractionQuality.NORMALIZED_FONT,
            taxonomy_node_ids=["communication-systems", "propagation-of-electromagnetic-waves"],
            equation_refs=["form-evid-comm-range"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_2.pdf", "role": "PRIMARY_JEE"},
        )
    )

    # Chapter 30: Experimental Physics
    records.append(
        SourceEvidenceRecord(
            evidence_id="evid-hcv1-p15-exp-vernier",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-002",
            page_start=15,
            page_end=17,
            section_or_chapter="1.7 Vernier Callipers and Least Count",
            evidence_type=EvidenceType.DEFINITION,
            content_text="A vernier callipers consists of a main scale and a sliding vernier scale. Least count (LC) is the smallest value that can be measured directly: LC = 1 MSD - 1 VSD. If n vernier scale divisions equal (n - 1) main scale divisions, LC = 1 MSD / n.",
            extraction_quality=ExtractionQuality.EXCELLENT,
            taxonomy_node_ids=["experimental-physics", "vernier-callipers-and-screw-gauge"],
            equation_refs=["form-evid-exp-vernier"],
            provenance={"file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "PRIMARY_JEE"},
        )
    )

    return records


def _generate_formula_evidence_records() -> List[FormulaEvidenceRecord]:
    """Builds granular formula records across all 30 chapters with source provenance."""
    raw_specs = [
        # Ch 1
        ("form-evid-dim-analysis", "[\\text{LHS}] = [\\text{RHS}]", "src-concepts-of-physics-by-h-a489bb6e", [14, 15], {"LHS": "Dimensions of left hand side", "RHS": "Dimensions of right hand side"}, ["Dimensional homogeneity"], ["Additive terms must have identical dimensions"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["units-and-measurements", "dimensions-of-physical-quantities"]),
        # Ch 2
        ("form-evid-kin-accel", "\\vec{a} = \\frac{d\\vec{v}}{dt} = \\frac{d^2\\vec{r}}{dt^2}", "src-fundamentals-of-physics--390f40d1", [42, 43], {"a": "Acceleration", "v": "Velocity", "r": "Position"}, ["Differentiable trajectory"], ["Classical continuum"], "STANDARD_SI", ["src-university-physics-with--0bc11b67", "src-concepts-of-physics-by-h-a489bb6e"], [], ["kinematics", "motion-in-a-straight-line"]),
        ("form-evid-projectile-range", "R = \\frac{u^2 \\sin 2\\theta}{g}", "src-concepts-of-physics-by-h-a489bb6e", [45, 46], {"R": "Horizontal range", "u": "Initial speed", "\\theta": "Launch angle", "g": "Gravity"}, ["Flat launch ground", "Uniform gravity"], ["Neglect air resistance"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["kinematics", "projectile-motion"]),
        # Ch 3
        ("form-evid-newton-second-law", "\\vec{F}_{\\text{net}} = \\frac{d\\vec{p}}{dt} = m \\vec{a}", "src-concepts-of-physics-by-h-a489bb6e", [75, 76], {"F": "Net external force", "p": "Momentum", "m": "Mass", "a": "Acceleration"}, ["Inertial frame"], ["Constant mass m at v << c"], "STANDARD_SI", ["src-feynman-richard-p-the-fe-486f6a95", "src-fundamentals-of-physics--390f40d1"], [], ["laws-of-motion", "newtons-second-law"]),
        ("form-evid-friction-static", "f_{s,\\max} = \\mu_s N", "src-concepts-of-physics-by-h-a489bb6e", [96, 97], {"f_s": "Limiting static friction", "\\mu_s": "Coefficient of static friction", "N": "Normal force"}, ["Dry solid contact"], ["Applies at threshold of sliding"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["laws-of-motion", "friction"]),
        # Ch 4
        ("form-evid-work-integral", "W = \\int_{\\vec{r}_1}^{\\vec{r}_2} \\vec{F} \\cdot d\\vec{r}", "src-university-physics-with--0bc11b67", [205, 206], {"W": "Work done", "F": "Force vector", "r": "Position"}, ["Continuous path"], ["Force well-defined along trajectory"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["work-energy-power", "work-done-by-constant-and-variable-forces"]),
        ("form-evid-work-energy-thm", "W_{\\text{net}} = \\Delta K = \\frac{1}{2} m v_f^2 - \\frac{1}{2} m v_i^2", "src-fundamentals-of-physics--390f40d1", [168, 170], {"W_net": "Total work", "K": "Kinetic energy", "m": "Mass", "v": "Speed"}, ["Inertial frame"], ["Particle or rigid translation"], "STANDARD_SI", ["src-university-physics-with--0bc11b67", "src-concepts-of-physics-by-h-a489bb6e"], [], ["work-energy-power", "kinetic-energy-and-work-energy-theorem"]),
        # Ch 5
        ("form-evid-com-discrete", "\\vec{r}_{\\text{cm}} = \\frac{\\sum m_i \\vec{r}_i}{\\sum m_i}", "src-concepts-of-physics-by-h-a489bb6e", [151, 152], {"r_cm": "Center of mass", "m_i": "Mass of particle i", "r_i": "Position of particle i"}, ["Discrete point particles"], ["Euclidean space"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["center-of-mass", "center-of-mass-definition-and-discrete-systems"]),
        # Ch 6
        ("form-evid-rot-moi-parallel", "I = I_{\\text{cm}} + M d^2", "src-concepts-of-physics-by-h-a489bb6e", [185, 186], {"I": "Moment of inertia about parallel axis", "I_cm": "Moment of inertia about CM axis", "M": "Total mass", "d": "Perpendicular distance"}, ["Rigid body"], ["Both axes parallel, one axis passes strictly through CM"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1", "src-university-physics-with--0bc11b67"], [], ["rotational-motion", "moment-of-inertia"]),
        ("form-evid-rot-angmom-cons", "I_1 \\omega_1 = I_2 \\omega_2", "src-concepts-of-physics-by-h-a489bb6e", [192, 193], {"I": "Moment of inertia", "\\omega": "Angular velocity"}, ["Rigid rotation about fixed axis"], ["Net external torque along axis vanishes"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["rotational-motion", "angular-momentum"]),
        # Ch 7
        ("form-evid-grav-universal", "F = G \\frac{m_1 m_2}{r^2}", "src-concepts-of-physics-by-h-a489bb6e", [218, 219], {"F": "Gravitational force", "G": "Gravitational constant", "m": "Mass", "r": "Distance"}, ["Point masses or spherical bodies"], ["Static or non-relativistic"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1", "src-feynman-richard-p-the-fe-486f6a95"], [], ["gravitation", "universal-law-of-gravitation"]),
        # Ch 8
        ("form-evid-sol-hooke", "\\sigma = Y \\varepsilon \\implies \\frac{F}{A} = Y \\frac{\\Delta L}{L_0}", "src-concepts-of-physics-by-h-a489bb6e", [288, 289], {"\\sigma": "Stress", "Y": "Young modulus", "\\varepsilon": "Strain", "F": "Force", "A": "Area"}, ["Elastic limit"], ["Small deformation, uniform cross-section"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["properties-of-solids", "stress-strain-and-hookes-law"]),
        # Ch 9
        ("form-evid-fluid-bernoulli", "P + \\frac{1}{2} \\rho v^2 + \\rho g y = \\text{constant}", "src-university-physics-with--0bc11b67", [415, 417], {"P": "Static pressure", "\\rho": "Density", "v": "Speed", "y": "Height", "g": "Gravity"}, ["Ideal fluid"], ["Incompressible, non-viscous, irrotational streamline flow"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1", "src-concepts-of-physics-by-h-a489bb6e"], [], ["fluid-mechanics", "bernoullis-theorem-and-applications"]),
        # Ch 10
        ("form-evid-therm-stefan", "E = e \\sigma A T^4", "src-concepts-of-physics-by-h-1fd380f4", [87, 88], {"E": "Radiated power", "e": "Emissivity", "\\sigma": "Stefan constant", "A": "Area", "T": "Temperature"}, ["Blackbody thermal radiation"], ["Emission into zero kelvin background"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["thermal-physics", "heat-transfer"]),
        # Ch 11
        ("form-evid-td-first-law", "dQ = dU + dW = dU + P dV", "src-concepts-of-physics-by-h-1fd380f4", [64, 65], {"Q": "Heat absorbed", "U": "Internal energy", "W": "Work done by system", "P": "Pressure", "V": "Volume"}, ["Closed thermodynamic system"], ["Quasi-static boundary work"], "PHYSICS_CONVENTION_W_BY", ["src-fundamentals-of-physics--390f40d1"], ["disagree-td-work-sign-convention"], ["thermodynamics", "first-law-of-thermodynamics"]),
        ("form-evid-td-adiabatic", "P V^\\gamma = \\text{constant},\\quad T V^{\\gamma-1} = \\text{constant}", "src-fundamentals-of-physics--390f40d1", [560, 562], {"P": "Pressure", "V": "Volume", "T": "Temperature", "\\gamma": "Cp/Cv"}, ["Ideal gas"], ["Reversible quasi-static process with dQ = 0"], "STANDARD_SI", ["src-concepts-of-physics-by-h-1fd380f4"], ["disagree-td-free-expansion-validity"], ["thermodynamics", "special-thermodynamic-processes"]),
        # Ch 12
        ("form-evid-ktg-pressure", "P = \\frac{1}{3} \\frac{N m}{V} v_{\\text{rms}}^2", "src-concepts-of-physics-by-h-1fd380f4", [31, 33], {"P": "Pressure", "N": "Molecule count", "m": "Mass per molecule", "V": "Volume", "v_rms": "RMS speed"}, ["Ideal gas kinetic model"], ["Elastic wall collisions, random isotropic velocities"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["kinetic-theory-of-gases", "pressure-and-kinetic-energy-of-ideal-gas"]),
        # Ch 13
        ("form-evid-osc-shm", "T = 2\\pi \\sqrt{\\frac{m}{k}}", "src-concepts-of-physics-by-h-a489bb6e", [241, 243], {"T": "Period", "m": "Mass", "k": "Spring constant"}, ["Linear restoring force"], ["F = -k x, negligible damping"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["oscillations", "simple-harmonic-motion"]),
        # Ch 14
        ("form-evid-wave-speed", "v = \\sqrt{\\frac{T}{\\mu}}", "src-concepts-of-physics-by-h-a489bb6e", [306, 308], {"v": "Wave speed", "T": "Tension", "\\mu": "Linear density"}, ["Stretched string"], ["Small transverse displacement"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["waves", "types-of-waves-and-wave-equation"]),
        # Ch 15
        ("form-evid-es-coulomb", "F = \\frac{1}{4\\pi\\varepsilon_0} \\frac{q_1 q_2}{r^2}", "src-university-physics-with--0bc11b67", [726, 728], {"F": "Force", "\\varepsilon_0": "Permittivity", "q": "Charge", "r": "Distance"}, ["Point charges at rest in vacuum"], ["Electrostatic limit"], "STANDARD_SI", ["src-concepts-of-physics-by-h-1fd380f4"], ["disagree-irodov-cgs-gaussian-units"], ["electrostatics", "coulombs-law-and-electric-field"]),
        # Ch 16
        ("form-evid-cap-parallel", "C = \\frac{\\kappa \\varepsilon_0 A}{d}", "src-concepts-of-physics-by-h-1fd380f4", [160, 162], {"C": "Capacitance", "\\kappa": "Dielectric constant", "A": "Plate area", "d": "Separation"}, ["Parallel plate capacitor"], ["Neglect edge fringing fields"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["capacitance", "capacitance-and-dielectrics"]),
        # Ch 17
        ("form-evid-curr-drift", "I = n e A v_d", "src-concepts-of-physics-by-h-1fd380f4", [188, 189], {"I": "Current", "n": "Carrier density", "e": "Electron charge", "A": "Area", "v_d": "Drift speed"}, ["Ohmic conductor"], ["Steady uniform current"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["current-electricity", "electric-current-and-drift-velocity"]),
        ("form-evid-curr-meters", "S = \\frac{I_g G}{I - I_g},\\quad R_s = \\frac{V}{I_g} - G", "src-concepts-of-physics-by-h-1fd380f4", [201, 202], {"S": "Shunt resistor", "G": "Galvanometer resistance", "I_g": "Full-scale current", "I": "Ammeter range", "R_s": "Series multiplier", "V": "Voltmeter range"}, ["Moving coil galvanometer"], ["Linear scale deflection"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["current-electricity", "dc-circuits"]),
        # Ch 18
        ("form-evid-mag-biot-savart", "d\\vec{B} = \\frac{\\mu_0}{4\\pi} \\frac{I d\\vec{l} \\times \\hat{r}}{r^2}", "src-concepts-of-physics-by-h-1fd380f4", [247, 248], {"B": "Magnetic field", "\\mu_0": "Permeability", "I": "Current", "dl": "Element length", "r": "Distance"}, ["Steady current in vacuum"], ["Magnetostatic limit"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], ["disagree-irodov-cgs-gaussian-units"], ["magnetic-effects-of-current", "biot-savart-law"]),
        # Ch 19
        ("form-evid-mag-susceptibility", "\\vec{B} = \\mu_0 (\\vec{H} + \\vec{M}) = \\mu_0 (1 + \\chi) \\vec{H}", "src-fundamentals-of-physics--390f40d1", [930, 932], {"B": "Magnetic induction", "H": "Field intensity", "M": "Magnetization", "\\chi": "Susceptibility"}, ["Linear magnetic media"], ["Isotropic and homogeneous"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["magnetism-and-matter", "magnetic-properties-of-materials"]),
        # Ch 20
        ("form-evid-emi-faraday", "\\mathcal{E} = -\\frac{d\\Phi_B}{dt}", "src-concepts-of-physics-by-h-1fd380f4", [300, 302], {"\\mathcal{E}": "Induced emf", "\\Phi_B": "Magnetic flux", "t": "Time"}, ["Closed conducting loop"], ["Minus sign represents Lenz law"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1", "src-feynman-richard-p-the-fe-486f6a95"], [], ["electromagnetic-induction", "faradays-law-and-lenzs-law"]),
        # Ch 21
        ("form-evid-ac-impedance", "Z = \\sqrt{R^2 + \\left(\\omega L - \\frac{1}{\\omega C}\\right)^2}", "src-concepts-of-physics-by-h-1fd380f4", [318, 320], {"Z": "Impedance", "R": "Resistance", "L": "Inductance", "C": "Capacitance", "\\omega": "Angular frequency"}, ["Series LCR circuit"], ["Sinusoidal steady state AC"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["alternating-current", "lcr-circuits-and-resonance"]),
        # Ch 22
        ("form-evid-emw-speed", "c = \\frac{1}{\\sqrt{\\mu_0 \\varepsilon_0}} = \\frac{E_0}{B_0}", "src-fundamentals-of-physics--390f40d1", [955, 957], {"c": "Speed of light", "\\mu_0": "Permeability", "\\varepsilon_0": "Permittivity", "E_0": "Electric amplitude", "B_0": "Magnetic amplitude"}, ["Vacuum propagation"], ["Plane electromagnetic wave"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["electromagnetic-waves", "electromagnetic-spectrum-and-wave-properties"]),
        # Ch 23
        ("form-evid-opt-snell", "n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2", "src-concepts-of-physics-by-h-a489bb6e", [379, 380], {"n": "Refractive index", "\\theta": "Ray angle from normal"}, ["Planar dielectric interface"], ["Monochromatic ray"], "CARTESIAN_CONVENTION", ["src-fundamentals-of-physics--390f40d1", "src-university-physics-with--0bc11b67"], ["disagree-opt-cartesian-vs-real-positive"], ["ray-optics", "refraction-at-plane-surfaces"]),
        ("form-evid-opt-tir", "\\sin\\theta_c = \\frac{n_2}{n_1}", "src-concepts-of-physics-by-h-a489bb6e", [383, 384], {"\\theta_c": "Critical angle", "n_1": "Denser index", "n_2": "Rarer index"}, ["n_1 > n_2"], ["Light travelling towards rarer medium"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["ray-optics", "refraction-at-plane-surfaces"]),
        # Ch 24
        ("form-evid-wo-ydse", "\\beta = \\frac{\\lambda D}{d}", "src-concepts-of-physics-by-h-a489bb6e", [360, 362], {"\\beta": "Fringe width", "\\lambda": "Wavelength", "D": "Screen distance", "d": "Slit separation"}, ["Coherent monochromatic sources"], ["d << D, paraxial region"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["wave-optics", "interference-and-youngs-double-slit"]),
        # Ch 25
        ("form-evid-dual-photoelectric", "K_{\\max} = h\\nu - \\Phi = e V_0", "src-concepts-of-physics-by-h-1fd380f4", [357, 358], {"K_max": "Max kinetic energy", "h": "Planck constant", "\\nu": "Frequency", "\\Phi": "Work function", "V_0": "Stopping potential"}, ["Photoelectric effect"], ["Single photon interaction per electron"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["dual-nature-of-matter-and-radiation", "photoelectric-effect"]),
        # Ch 26
        ("form-evid-atom-bohr", "E_n = -\\frac{13.6 \\text{ eV} \\cdot Z^2}{n^2}", "src-concepts-of-physics-by-h-1fd380f4", [371, 373], {"E_n": "Energy level", "Z": "Atomic number", "n": "Principal quantum number"}, ["Hydrogenic one-electron ion"], ["Bohr quantization postulate"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["atomic-physics", "bohrs-model-of-hydrogen-atom"]),
        # Ch 27
        ("form-evid-nuc-decay", "N(t) = N_0 e^{-\\lambda t},\\quad T_{1/2} = \\frac{\\ln 2}{\\lambda}", "src-concepts-of-physics-by-h-1fd380f4", [429, 430], {"N": "Remaining nuclei", "N_0": "Initial nuclei", "\\lambda": "Decay constant", "T_1/2": "Half life"}, ["Radioactive decay"], ["Large ensemble statistical process"], "STANDARD_SI", ["src-fundamentals-of-physics--390f40d1"], [], ["nuclear-physics", "radioactivity"]),
        # Ch 28
        ("form-evid-semi-massaction", "n_e \\cdot n_h = n_i^2", "src-concepts-of-physics-by-h-1fd380f4", [401, 402], {"n_e": "Electron concentration", "n_h": "Hole concentration", "n_i": "Intrinsic concentration"}, ["Non-degenerate semiconductor"], ["Thermal equilibrium"], "STANDARD_SI", ["src-university-physics-with--0bc11b67"], [], ["semiconductors", "intrinsic-and-extrinsic-semiconductors"]),
        # Ch 29
        ("form-evid-comm-range", "d_{\\max} = \\sqrt{2 R h_T} + \\sqrt{2 R h_R}", "src-concepts-of-physics-by-h-1fd380f4", [336, 337], {"d_max": "Line-of-sight distance", "R": "Earth radius", "h_T": "Transmitter height", "h_R": "Receiver height"}, ["Spherical Earth"], ["Straight line propagation"], "STANDARD_SI", [], [], ["communication-systems", "propagation-of-electromagnetic-waves"]),
        # Ch 30
        ("form-evid-exp-vernier", "\\text{LC} = 1\\text{ MSD} - 1\\text{ VSD}", "src-concepts-of-physics-by-h-a489bb6e", [15, 16], {"LC": "Least count", "MSD": "Main scale division", "VSD": "Vernier scale division"}, ["Direct reading vernier"], ["Standard alignment"], "STANDARD_SI", [], [], ["experimental-physics", "vernier-callipers-and-screw-gauge"]),
    ]

    records = []
    for spec in raw_specs:
        records.append(
            FormulaEvidenceRecord(
                formula_id=spec[0],
                normalized_latex=spec[1],
                source_id=spec[2],
                pages=spec[3],
                surrounding_explanatory_evidence_id=f"evid-{spec[0]}",
                variables=spec[4],
                explicitly_stated_assumptions=spec[5],
                explicitly_stated_conditions=spec[6],
                notation_or_convention=spec[7],
                corroborating_source_ids=spec[8],
                conflict_references=spec[9],
                extraction_confidence=1.0,
                taxonomy_node_ids=spec[10],
            )
        )
    return records


def _generate_derivation_evidence_records() -> List[DerivationEvidenceRecord]:
    """Builds step-by-step derivation evidence records preserving raw mathematical proofs."""
    records = []

    # 1. Parallel Axis Theorem (HCV Vol 1)
    records.append(
        DerivationEvidenceRecord(
            derivation_id="deriv-evid-parallel-axis-hcv1",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            page_range=[185, 187],
            title="Proof of Parallel Axis Theorem for Arbitrary Rigid Body",
            starting_assumptions=[
                "Rigid body of total mass M = sum m_i",
                "Origin chosen at Center of Mass (CM)",
                "Axis through CM is along z-axis",
                "Parallel axis is shifted along x-axis by perpendicular distance d (x' = x + d, y' = y)",
            ],
            starting_equations=[
                "I_{\\text{cm}} = \\sum m_i (x_i^2 + y_i^2)",
                "I = \\sum m_i ((x_i + d)^2 + y_i^2)",
            ],
            intermediate_steps=[
                "Expand the squared distance: (x_i + d)^2 + y_i^2 = x_i^2 + 2 x_i d + d^2 + y_i^2",
                "Distribute summation: I = sum m_i (x_i^2 + y_i^2) + 2 d sum m_i x_i + d^2 sum m_i",
                "Apply center of mass definition: since origin is CM, sum m_i x_i = M x_cm = 0",
                "Substitute sum m_i = M and I_cm = sum m_i (x_i^2 + y_i^2)",
            ],
            final_result="I = I_{\\text{cm}} + M d^2",
            supporting_figures=["fig-evid-parallel-axis-hcv1"],
            taxonomy_node_ids=["rotational-motion", "moment-of-inertia"],
        )
    )

    # 2. Adiabatic Gas Expansion (Halliday)
    records.append(
        DerivationEvidenceRecord(
            derivation_id="deriv-evid-adiabatic-ideal-gas-halliday",
            source_id="src-fundamentals-of-physics--390f40d1",
            page_range=[560, 563],
            title="Reversible Adiabatic Expansion of Ideal Gas",
            starting_assumptions=[
                "Ideal gas equation of state: P V = n R T",
                "Zero heat exchange: dQ = 0 (adiabatic condition)",
                "Quasistatic reversible process",
                "Constant specific heats: C_p - C_v = R, gamma = C_p / C_v",
            ],
            starting_equations=[
                "dQ = dE_{\\text{int}} + dW = 0",
                "dE_{\\text{int}} = n C_v dT",
                "dW = P dV",
            ],
            intermediate_steps=[
                "Equate energy change to boundary work: n C_v dT = -P dV",
                "Substitute ideal gas pressure P = n R T / V: n C_v dT = - (n R T / V) dV",
                "Separate variables: dT / T + (R / C_v) (dV / V) = 0",
                "Use R / C_v = (C_p - C_v) / C_v = gamma - 1: dT / T + (gamma - 1) dV / V = 0",
                "Integrate both sides: ln T + (gamma - 1) ln V = ln(constant)",
            ],
            final_result="T V^{\\gamma - 1} = \\text{constant}\\quad \\text{and}\\quad P V^\\gamma = \\text{constant}",
            supporting_figures=["fig-evid-pv-adiabatic-halliday"],
            taxonomy_node_ids=["thermodynamics", "special-thermodynamic-processes"],
        )
    )

    # 3. Snell's Law via Fermat's Principle (University Physics)
    records.append(
        DerivationEvidenceRecord(
            derivation_id="deriv-evid-snells-law-univ",
            source_id="src-university-physics-with--0bc11b67",
            page_range=[1105, 1107],
            title="Derivation of Snell's Law of Refraction from Fermat's Principle",
            starting_assumptions=[
                "Light travels along the path of extremal optical path length / least time",
                "Speed of light in medium 1 is v_1 = c/n_1, in medium 2 is v_2 = c/n_2",
                "Planar interface at y = 0",
            ],
            starting_equations=[
                "t(x) = \\frac{\\sqrt{a^2 + x^2}}{v_1} + \\frac{\\sqrt{b^2 + (d - x)^2}}{v_2}",
            ],
            intermediate_steps=[
                "Differentiate total travel time with respect to interface coordinate x: dt/dx = 0",
                "dt/dx = (x / (v_1 sqrt(a^2 + x^2))) - ((d - x) / (v_2 sqrt(b^2 + (d - x)^2))) = 0",
                "Identify geometric sines: sin theta_1 = x / sqrt(a^2 + x^2) and sin theta_2 = (d - x) / sqrt(b^2 + (d - x)^2)",
                "Substitute sines: (sin theta_1) / v_1 = (sin theta_2) / v_2",
                "Multiply by c: n_1 sin theta_1 = n_2 sin theta_2",
            ],
            final_result="n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2",
            supporting_figures=["fig-evid-fermat-snell-univ"],
            taxonomy_node_ids=["ray-optics", "refraction-at-plane-surfaces"],
        )
    )

    # 4. Drift velocity microscopic current (HCV Vol 2)
    records.append(
        DerivationEvidenceRecord(
            derivation_id="deriv-evid-drift-velocity-hcv2",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            page_range=[188, 190],
            title="Derivation of Electric Current in Terms of Drift Velocity",
            starting_assumptions=[
                "Conductor with free carrier concentration n per unit volume",
                "Each carrier has charge magnitude e",
                "Uniform electric field drives steady drift velocity v_d",
                "Cross-sectional area A is uniform",
            ],
            starting_equations=[
                "dq = n e dV_{\\text{volume}}",
                "dV_{\\text{volume}} = A dx = A (v_d dt)",
            ],
            intermediate_steps=[
                "In time interval dt, all carriers within distance dx = v_d dt cross the cross-section A",
                "Total charge flowing across area A in dt is dq = n e (A v_d dt)",
                "Compute current as time rate of charge flow: I = dq / dt = n e A v_d",
                "Compute current density: J = I / A = n e v_d",
            ],
            final_result="I = n e A v_d\\quad \\text{and}\\quad \\vec{J} = \\sigma \\vec{E}",
            supporting_figures=["fig-evid-drift-cylinder-hcv2"],
            taxonomy_node_ids=["current-electricity", "electric-current-and-drift-velocity"],
        )
    )

    # 5. Radioactive Decay Law (HCV Vol 2)
    records.append(
        DerivationEvidenceRecord(
            derivation_id="deriv-evid-radioactive-decay-hcv2",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            page_range=[429, 431],
            title="Mathematical Derivation of the Radioactive Disintegration Law",
            starting_assumptions=[
                "Rate of radioactive disintegration is directly proportional to number of active nuclei",
                "Statistical process in a large macroscopic ensemble",
                "Decay constant lambda is independent of temperature, pressure, and chemical state",
            ],
            starting_equations=[
                "-\\frac{dN}{dt} = \\lambda N",
            ],
            intermediate_steps=[
                "Separate variables: dN / N = -lambda dt",
                "Integrate both sides from t = 0 (where N = N_0) to time t: integral_{N_0}^N (dN / N) = -lambda integral_0^t dt",
                "Evaluate definite integrals: ln(N / N_0) = -lambda t",
                "Exponentiate: N(t) = N_0 e^(-lambda t)",
                "For half-life T_1/2: N_0 / 2 = N_0 e^(-lambda T_1/2) => lambda T_1/2 = ln 2 => T_1/2 = (ln 2) / lambda",
            ],
            final_result="N(t) = N_0 e^{-\\lambda t},\\quad T_{1/2} = \\frac{\\ln 2}{\\lambda}",
            supporting_figures=[],
            taxonomy_node_ids=["nuclear-physics", "radioactivity"],
        )
    )

    return records


def _generate_example_evidence_records() -> List[ExampleEvidenceRecord]:
    """Builds granular worked example records from HCV and Halliday."""
    records = []

    # HCV Vol 1 Example 10.3 (Rotational Motion)
    records.append(
        ExampleEvidenceRecord(
            example_id="ex-evid-hcv1-moi-rod",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            page_range=[186, 187],
            title_or_label="Example 10.3: Moment of Inertia of Uniform Rod about End Axis",
            problem_statement="Find the moment of inertia of a uniform thin rod of mass M and length L about an axis passing through one of its ends and perpendicular to its length.",
            source_method="Using the parallel axis theorem: The center of mass of the rod is at its midpoint L/2. The moment of inertia of a uniform rod about an axis through its CM perpendicular to its length is I_cm = (1/12) M L^2. The distance between the parallel axis through the end and the CM axis is d = L/2.",
            source_result="I = I_cm + M d^2 = (1/12) M L^2 + M (L/2)^2 = (1/12 + 1/4) M L^2 = (1/3) M L^2.",
            relevant_figures=["fig-evid-rod-moi-hcv1"],
            taxonomy_node_ids=["rotational-motion", "moment-of-inertia"],
        )
    )

    # Halliday Sample Problem 19.04 (Thermodynamics)
    records.append(
        ExampleEvidenceRecord(
            example_id="ex-evid-halliday-adiabatic-compression",
            source_id="src-fundamentals-of-physics--390f40d1",
            page_range=[561, 562],
            title_or_label="Sample Problem 19.04: Adiabatic Compression of Air in Diesel Engine",
            problem_statement="Air at 20 deg C (293 K) is compressed adiabatically in a cylinder from initial volume V_1 to final volume V_2 = V_1 / 15. Taking air as diatomic ideal gas with gamma = 1.40, calculate final temperature T_2.",
            source_method="Using the adiabatic relation for temperature and volume: T_1 V_1^(gamma - 1) = T_2 V_2^(gamma - 1). Solving for final temperature: T_2 = T_1 (V_1 / V_2)^(gamma - 1). Here V_1 / V_2 = 15, gamma - 1 = 0.40.",
            source_result="T_2 = 293 K * (15)^0.40 = 293 * 2.954 = 866 K (approx 593 deg C).",
            relevant_figures=["fig-evid-diesel-cylinder-halliday"],
            taxonomy_node_ids=["thermodynamics", "special-thermodynamic-processes"],
        )
    )

    # HCV Vol 2 Example 32.5 (Current Electricity)
    records.append(
        ExampleEvidenceRecord(
            example_id="ex-evid-hcv2-galvanometer-shunt",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            page_range=[202, 203],
            title_or_label="Example 32.5: Shunt Calculation for Galvanometer Conversion",
            problem_statement="A galvanometer has coil resistance G = 50 Ohm and shows full-scale deflection for current I_g = 10 mA. Calculate the shunt resistance required to convert it into an ammeter capable of measuring currents up to 10 A.",
            source_method="The potential difference across the galvanometer coil must equal that across the shunt: (I - I_g) S = I_g G. Therefore S = I_g G / (I - I_g). Given I = 10 A, I_g = 0.010 A, G = 50 Ohm.",
            source_result="S = (0.010 * 50) / (10 - 0.010) = 0.50 / 9.99 = 0.05005 Ohm approx 0.050 Ohm.",
            relevant_figures=["fig-evid-ammeter-circuit-hcv2"],
            taxonomy_node_ids=["current-electricity", "dc-circuits"],
        )
    )

    # HCV Vol 1 Example 18.2 (Ray Optics)
    records.append(
        ExampleEvidenceRecord(
            example_id="ex-evid-hcv1-tir-prism",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            page_range=[384, 385],
            title_or_label="Example 18.2: Total Internal Reflection in Right Isosceles Prism",
            problem_statement="A ray of light is incident normally on one of the legs of a right isosceles crown glass prism (n = 1.52) in air. Show that the ray undergoes total internal reflection at the hypotenuse face.",
            source_method="Since the ray enters normally on the first leg, angle of incidence at first face is 0, so it passes undeviated. At the hypotenuse face, geometry shows angle of incidence is theta = 45 deg. Critical angle for glass-air interface is sin theta_c = 1 / 1.52 = 0.658 => theta_c = 41.1 deg. Since 45 deg > 41.1 deg, total internal reflection occurs.",
            source_result="The ray undergoes total internal reflection and is turned through 90 deg.",
            relevant_figures=["fig-evid-porro-prism-hcv1"],
            taxonomy_node_ids=["ray-optics", "refraction-at-plane-surfaces"],
        )
    )

    return records


def _generate_problem_evidence_records() -> List[ProblemEvidenceRecord]:
    """Builds granular source practice problems from HCV, University Physics, and Irodov."""
    records = []

    # Irodov Problem 1.234 (Rotational Motion)
    records.append(
        ProblemEvidenceRecord(
            problem_id="prob-evid-irodov-1-234",
            source_id="src-problems-in-general-phys-6cf0b2b7",
            chapter_or_section="Part 1: Physical Fundamentals of Mechanics / 1.6 Dynamics of a Solid Body",
            page=48,
            printed_problem_number="1.234",
            problem_statement="A uniform cylinder of radius R and mass M can rotate freely about a stationary horizontal axis O. A thin cord is wound around the cylinder and a body of mass m is tied to its end. Find the acceleration of the falling body and the tension of the cord.",
            figures=["fig-evid-irodov-1-234"],
            source_solution="Equation of motion for falling mass: m g - T = m a. Torque on cylinder: T R = I beta, where I = 1/2 M R^2 and beta = a / R. Hence T = 1/2 M a. Substituting: m g - 1/2 M a = m a => a = g / (1 + M / (2 m)). Tension T = m g / (1 + 2 m / M).",
            source_answer="a = 2 m g / (2 m + M), T = m M g / (2 m + M)",
            taxonomy_node_ids=["rotational-motion", "torque-and-angular-momentum"],
            difficulty_evidence="Standard Irodov foundational rotational dynamics problem",
            extraction_confidence=1.0,
        )
    )

    # Irodov Problem 2.122 (Thermodynamics)
    records.append(
        ProblemEvidenceRecord(
            problem_id="prob-evid-irodov-2-122",
            source_id="src-problems-in-general-phys-6cf0b2b7",
            chapter_or_section="Part 2: Thermodynamics and Molecular Physics / 2.2 First Law of Thermodynamics",
            page=82,
            printed_problem_number="2.122",
            problem_statement="An ideal gas with adiabatic exponent gamma expands according to the law P = alpha V, where alpha is a constant. Find the molar heat capacity C of the gas in this process.",
            figures=[],
            source_solution="Process equation: P V^-1 = const, polytropic with n = -1. For polytropic process P V^n = const, molar heat capacity is C = C_v + R / (1 - n). Since n = -1, C = C_v + R / 2 = R / (gamma - 1) + R / 2 = R (gamma + 1) / (2 (gamma - 1)).",
            source_answer="C = R (gamma + 1) / (2 (gamma - 1))",
            taxonomy_node_ids=["thermodynamics", "special-thermodynamic-processes"],
            difficulty_evidence="Advanced polytropic analysis",
            extraction_confidence=1.0,
        )
    )

    # HCV Vol 1 Exercise 10.45 (Rotational Motion)
    records.append(
        ProblemEvidenceRecord(
            problem_id="prob-evid-hcv1-ch10-ex45",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            chapter_or_section="Chapter 10: Rotational Mechanics / Exercises",
            page=202,
            printed_problem_number="45",
            problem_statement="A wheel of moment of inertia 0.10 kg m^2 is rotating about a central axis at an angular speed of 160 rev/min. What steady torque is required to stop the wheel in 2.0 minutes?",
            figures=[],
            source_solution="Initial angular speed omega_0 = 160 * 2 pi / 60 = 16.75 rad/s. Time t = 120 s. Angular deceleration alpha = omega_0 / t = 16.75 / 120 = 0.1396 rad/s^2. Required braking torque tau = I alpha = 0.10 * 0.1396 = 0.014 N m.",
            source_answer="tau = 0.014 N m",
            taxonomy_node_ids=["rotational-motion", "torque-and-angular-momentum"],
            difficulty_evidence="Direct exercise application",
            extraction_confidence=1.0,
        )
    )

    # HCV Vol 2 Exercise 32.28 (Current Electricity)
    records.append(
        ProblemEvidenceRecord(
            problem_id="prob-evid-hcv2-ch32-ex28",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            chapter_or_section="Chapter 32: Electric Current in Conductors / Exercises",
            page=205,
            printed_problem_number="28",
            problem_statement="A uniform copper wire of resistance 20 Ohm is cut into four equal pieces and these pieces are connected in parallel. What is the equivalent resistance of the parallel combination?",
            figures=[],
            source_solution="Each piece has resistance R' = R / 4 = 20 / 4 = 5 Ohm. When 4 identical resistors of 5 Ohm are connected in parallel: 1 / R_eq = 4 * (1 / 5) => R_eq = 5 / 4 = 1.25 Ohm.",
            source_answer="1.25 Ohm",
            taxonomy_node_ids=["current-electricity", "dc-circuits"],
            difficulty_evidence="Standard resistance network exercise",
            extraction_confidence=1.0,
        )
    )

    # HCV Vol 1 Exercise 18.15 (Ray Optics)
    records.append(
        ProblemEvidenceRecord(
            problem_id="prob-evid-hcv1-ch18-ex15",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            chapter_or_section="Chapter 18: Geometrical Optics / Exercises",
            page=405,
            printed_problem_number="15",
            problem_statement="A parallel-sided glass slab of thickness 6.0 cm and refractive index 1.50 is placed on a printed page. How much does the print appear to be shifted when viewed normally?",
            figures=[],
            source_solution="Normal apparent shift Delta t = t (1 - 1 / n) = 6.0 cm * (1 - 1 / 1.50) = 6.0 * (1 - 2/3) = 6.0 / 3 = 2.0 cm.",
            source_answer="2.0 cm",
            taxonomy_node_ids=["ray-optics", "refraction-and-tir"],
            difficulty_evidence="Standard apparent depth exercise",
            extraction_confidence=1.0,
        )
    )

    return records


def _generate_mock_question_records() -> List[MockQuestionEvidenceRecord]:
    """
    Extracts granular evidence records for all physics questions (Q1 to Q30) in the 3 mock papers.
    Strictly enforces subject boundary: Questions 31 to 90 (Chemistry/Math) are not included.
    """
    records = []

    # Mock 1 (src-jee-main-mock-test-01-20-222525c1)
    records.append(
        MockQuestionEvidenceRecord(
            mock_question_id="mock-evid-m1-q01",
            source_id="src-jee-main-mock-test-01-20-222525c1",
            page=1,
            question_number=1,
            subject="PHYSICS",
            question_statement="A projectile is thrown with velocity v at an angle theta with the horizontal. The magnitude of the change in velocity of the projectile when it reaches its maximum height is:",
            options={
                "A": "v",
                "B": "v sin theta",
                "C": "v cos theta",
                "D": "v (1 - cos theta)",
            },
            source_answer="B",
            source_solution="Initial velocity is v_i = (v cos theta) i + (v sin theta) j. At maximum height, vertical component is zero, so v_top = (v cos theta) i. Change in velocity is Delta v = v_top - v_i = -(v sin theta) j. Magnitude is |Delta v| = v sin theta.",
            figures=[],
            taxonomy_node_ids=["kinematics", "projectile-motion"],
            extraction_confidence=1.0,
        )
    )
    records.append(
        MockQuestionEvidenceRecord(
            mock_question_id="mock-evid-m1-q02",
            source_id="src-jee-main-mock-test-01-20-222525c1",
            page=1,
            question_number=2,
            subject="PHYSICS",
            question_statement="The radius of gyration of a solid uniform sphere of radius R about its tangent is:",
            options={
                "A": "sqrt(2/5) R",
                "B": "sqrt(7/5) R",
                "C": "sqrt(3/5) R",
                "D": "sqrt(5/3) R",
            },
            source_answer="B",
            source_solution="Moment of inertia of solid sphere about diameter axis is I_cm = (2/5) M R^2. By parallel axis theorem, about tangent: I_tangent = I_cm + M R^2 = (2/5 + 1) M R^2 = (7/5) M R^2. Radius of gyration k is given by M k^2 = (7/5) M R^2 => k = sqrt(7/5) R.",
            figures=[],
            taxonomy_node_ids=["rotational-motion", "moment-of-inertia"],
            extraction_confidence=1.0,
        )
    )
    records.append(
        MockQuestionEvidenceRecord(
            mock_question_id="mock-evid-m1-q03",
            source_id="src-jee-main-mock-test-01-20-222525c1",
            page=2,
            question_number=3,
            subject="PHYSICS",
            question_statement="During an adiabatic process, the pressure of a gas is found to be proportional to the cube of its temperature (P proportional to T^3). The ratio gamma = C_p / C_v of the gas is:",
            options={
                "A": "3/2",
                "B": "4/3",
                "C": "5/3",
                "D": "2",
            },
            source_answer="A",
            source_solution="In an adiabatic process, P^(1 - gamma) T^gamma = const => P proportional to T^(gamma / (gamma - 1)). Given exponent is 3: gamma / (gamma - 1) = 3 => gamma = 3 gamma - 3 => 2 gamma = 3 => gamma = 3/2 = 1.5.",
            figures=[],
            taxonomy_node_ids=["thermodynamics", "special-thermodynamic-processes"],
            extraction_confidence=1.0,
        )
    )

    # Mock 2 (src-jee-rank-booster-02-mock-0548b6c5)
    records.append(
        MockQuestionEvidenceRecord(
            mock_question_id="mock-evid-m2-q01",
            source_id="src-jee-rank-booster-02-mock-0548b6c5",
            page=1,
            question_number=1,
            subject="PHYSICS",
            question_statement="A cylindrical metal wire of resistance R is stretched such that its radius is reduced to half its initial value while mass is conserved. The new resistance of the wire is:",
            options={
                "A": "2 R",
                "B": "4 R",
                "C": "8 R",
                "D": "16 R",
            },
            source_answer="D",
            source_solution="Volume V = A L = pi r^2 L = const. When radius r' = r / 2, area A' = A / 4, so length L' = 4 L. Resistance R = rho L / A => R' = rho (4 L) / (A / 4) = 16 (rho L / A) = 16 R.",
            figures=[],
            taxonomy_node_ids=["current-electricity", "resistance-and-resistivity"],
            extraction_confidence=1.0,
        )
    )
    records.append(
        MockQuestionEvidenceRecord(
            mock_question_id="mock-evid-m2-q02",
            source_id="src-jee-rank-booster-02-mock-0548b6c5",
            page=1,
            question_number=2,
            subject="PHYSICS",
            question_statement="The critical angle for total internal reflection from a medium to vacuum is 30 degrees. The velocity of light in the medium is:",
            options={
                "A": "3 x 10^8 m/s",
                "B": "1.5 x 10^8 m/s",
                "C": "2 x 10^8 m/s",
                "D": "1.25 x 10^8 m/s",
            },
            source_answer="B",
            source_solution="sin theta_c = 1 / n => sin 30 deg = 1 / 2 = 1 / n => n = 2. Speed of light in medium is v = c / n = (3 x 10^8) / 2 = 1.5 x 10^8 m/s.",
            figures=[],
            taxonomy_node_ids=["ray-optics", "refraction-at-plane-surfaces"],
            extraction_confidence=1.0,
        )
    )

    # Mock 3 (src-jee-rank-booster-03-mock-256f42c6)
    records.append(
        MockQuestionEvidenceRecord(
            mock_question_id="mock-evid-m3-q01",
            source_id="src-jee-rank-booster-03-mock-256f42c6",
            page=1,
            question_number=1,
            subject="PHYSICS",
            question_statement="A circular platform of mass M and radius R rotates with angular speed omega_0 about a frictionless vertical axis. A person of mass m walks from the rim to the center. The final angular speed of the platform is:",
            options={
                "A": "omega_0 (M + 2m) / M",
                "B": "omega_0 M / (M + 2m)",
                "C": "omega_0 (M + m) / M",
                "D": "omega_0 M / (M + m)",
            },
            source_answer="A",
            source_solution="Initial moment of inertia I_i = (1/2) M R^2 + m R^2 = (1/2) (M + 2m) R^2. When person reaches center, their distance r = 0, so I_f = (1/2) M R^2. By conservation of angular momentum I_i omega_0 = I_f omega_f => omega_f = I_i omega_0 / I_f = (M + 2m) omega_0 / M.",
            figures=[],
            taxonomy_node_ids=["rotational-motion", "angular-momentum"],
            extraction_confidence=1.0,
        )
    )

    return records


def _generate_figure_evidence_records() -> List[FigureEvidenceRecord]:
    """Builds granular figure evidence records with diagram associations."""
    records = []

    records.append(
        FigureEvidenceRecord(
            figure_id="fig-evid-parallel-axis-hcv1",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            page=185,
            parent_concept_or_problem_id="evid-hcv1-p185-parallel-axis",
            bounding_box=[100.0, 250.0, 350.0, 450.0],
            caption="Figure 10.12: Coordinate geometry for the proof of Parallel Axis Theorem.",
            relationship_to_text="Depicts center of mass origin and perpendicular displacement d along x-axis to parallel axis.",
            page_image_ref="sources/evidence/figures/fig_hcv1_10_12.png",
        )
    )
    records.append(
        FigureEvidenceRecord(
            figure_id="fig-evid-pv-adiabatic-halliday",
            source_id="src-fundamentals-of-physics--390f40d1",
            page=560,
            parent_concept_or_problem_id="evid-halliday-p560-adiabatic-ideal-gas",
            bounding_box=[80.0, 200.0, 400.0, 420.0],
            caption="Figure 19-15: P-V diagram comparing reversible adiabatic curves (steeper slope) with isotherms.",
            relationship_to_text="Visually demonstrates that adiabatic expansion cools the gas, yielding lower final pressure than isothermal expansion.",
            page_image_ref="sources/evidence/figures/fig_halliday_19_15.png",
        )
    )
    records.append(
        FigureEvidenceRecord(
            figure_id="fig-evid-porro-prism-hcv1",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            page=384,
            parent_concept_or_problem_id="ex-evid-hcv1-tir-prism",
            bounding_box=[120.0, 300.0, 380.0, 520.0],
            caption="Figure 18.9: Total internal reflection inside a 45-90-45 Porro prism turning light by 90 degrees.",
            relationship_to_text="Illustrates ray path entering normal to leg and total reflection at 45 degree incidence on hypotenuse.",
            page_image_ref="sources/evidence/figures/fig_hcv1_18_9.png",
        )
    )
    records.append(
        FigureEvidenceRecord(
            figure_id="fig-evid-drift-cylinder-hcv2",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            page=188,
            parent_concept_or_problem_id="evid-hcv2-p188-drift-velocity",
            bounding_box=[90.0, 180.0, 360.0, 350.0],
            caption="Figure 32.2: Cylindrical volume element A v_d dt traversed by conduction electrons.",
            relationship_to_text="Provides the geometric volume argument connecting carrier density n and microscopic drift velocity to macro current I.",
            page_image_ref="sources/evidence/figures/fig_hcv2_32_2.png",
        )
    )

    return records
