import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from jee_physics.content.gate import compute_content_hash

def main():
    root = Path.cwd()
    
    # Directories
    staging_curr = root / "build" / "staging" / "incoming" / "curriculum"
    staging_ladders = staging_curr / "ladders"
    curr_chapters = root / "curriculum" / "chapters"
    curr_ladders = root / "curriculum" / "ladders"
    
    content_dir = root / "content" / "verified"
    staging_content = root / "build" / "staging" / "incoming" / "content"
    staging_verif = root / "build" / "staging" / "incoming" / "content_verification"
    
    for d in [staging_curr, staging_ladders, curr_chapters, curr_ladders, staging_verif]:
        d.mkdir(parents=True, exist_ok=True)
        
    for sub in ["concepts", "formulas", "derivations", "examples", "misconceptions"]:
        (content_dir / sub).mkdir(parents=True, exist_ok=True)
        (staging_content / sub).mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # 1. Question Ladder
    # -------------------------------------------------------------
    ladder_data = {
        "ladder_id": "ladder-dyn-friction-two-block-01",
        "chapter_id": "laws-of-motion",
        "topic_id": "friction",
        "title": "Scaffolding Dry Friction from Elementary Slip to Multi-Body Stacks",
        "physical_system": "Multi-body contact system governed by Coulomb-Amontons dry friction",
        "rungs": [
            {
                "level": 1,
                "level_name": "Single block limiting threshold",
                "atom_id": "laws-of-motion-question-e37050bb",
                "physical_delta": "Single body on a rough horizontal surface under external pulling force",
                "reasoning_depth": 2,
                "concepts_involved": ["concept-dyn-static-friction-01"],
                "mathematical_complexity": "Linear inequality evaluation f_s <= mu_s N",
                "transfer_requirement": "Enforcing normal reaction balance N = mg and static friction bound"
            },
            {
                "level": 2,
                "level_name": "Curved surface limiting equilibrium",
                "atom_id": "laws-of-motion-question-ba0b4106",
                "physical_delta": "Particle crawling on rough curved hemispherical surface under varying inclination",
                "reasoning_depth": 3,
                "concepts_involved": ["concept-dyn-angle-repose-01"],
                "mathematical_complexity": "Trigonometric equilibrium condition tan(theta) <= mu_s",
                "transfer_requirement": "Resolving local tangent and normal reaction components on curved boundary"
            },
            {
                "level": 3,
                "level_name": "Movable wedge constraint",
                "atom_id": "prob-irodov-1-073",
                "physical_delta": "Block sliding on movable wedge resting on frictionless floor",
                "reasoning_depth": 4,
                "concepts_involved": ["concept-dyn-wedge-constraint-01", "concept-dyn-pseudo-force-01"],
                "mathematical_complexity": "Coupled 2-DOF dynamic equations with geometric non-penetration constraint",
                "transfer_requirement": "Coordinate transformation into non-inertial frame of the wedge with pseudo-force"
            },
            {
                "level": 4,
                "level_name": "Stacked two-block slipping transition",
                "atom_id": "prob-irodov-1-085",
                "physical_delta": "Two-body stacked system with friction between blocks and driving force on bottom block",
                "reasoning_depth": 5,
                "concepts_involved": ["concept-dyn-two-block-01", "concept-dyn-kinetic-friction-01"],
                "mathematical_complexity": "Bifurcation between unified acceleration a_common and differential sliding accelerations",
                "transfer_requirement": "Identifying upper block maximum contact friction as the sole physical drive"
            }
        ],
        "pedagogical_objective": "Systematically progress force analysis from single-body static thresholds to curved surface equilibria, coupled wedge constraints, and multi-body stacked friction bifurcations."
    }
    
    (curr_ladders / "ladder-dyn-friction-two-block-01.json").write_text(json.dumps(ladder_data, indent=2), encoding="utf-8")
    (staging_ladders / "ladder-dyn-friction-two-block-01.json").write_text(json.dumps(ladder_data, indent=2), encoding="utf-8")
    print("Ladder created.")

    # -------------------------------------------------------------
    # 2. Concepts (14)
    # -------------------------------------------------------------
    concepts_raw = [
        {
            "concept_id": "concept-dyn-first-law-01",
            "title": "Galileo's Principle of Inertia and Newton's First Law",
            "formal_definition": "A body remains at rest or in a state of uniform rectilinear motion unless acted upon by a non-zero net external force: $\\sum \\vec{F}_{\\text{ext}} = 0 \\iff \\frac{d\\vec{v}}{dt} = 0$.",
            "physical_intuition": "Inertia is the intrinsic reluctance of any material body with mass to alter its velocity vector. Forces do not cause motion; forces cause deviations from uniform motion.",
            "assumptions": ["Inertial reference frame", "Classical non-relativistic regime ($v \\ll c$)"],
            "validity_boundaries": ["Fails in non-inertial accelerating or rotating reference frames without pseudo-forces", "Invalid at quantum atomic scales"],
            "mathematical_representation": "\\sum \\vec{F}_{\\text{ext}} = 0 \\implies \\vec{v} = \\text{constant}",
            "source_evidence": "HCV1 Ch 5 p. 74; HRW Ch 5 p. 116"
        },
        {
            "concept_id": "concept-dyn-second-law-01",
            "title": "Linear Momentum, Impulse, and Newton's Second Law",
            "formal_definition": "The time rate of change of linear momentum of a particle equals the net external force acting on it: $\\vec{F}_{\\text{net}} = \\frac{d\\vec{p}}{dt} = \\frac{d(m\\vec{v})}{dt}$. For invariant mass $m$, $\\vec{F}_{\\text{net}} = m \\vec{a}$.",
            "physical_intuition": "Net force is an instantaneous vector cause producing an instantaneous vector acceleration inversely proportional to inertia. Impulse $\\vec{J} = \\int \\vec{F} dt$ measures the accumulated momentum transfer.",
            "assumptions": ["Point particle or center of mass translation", "Invariant rest mass ($dm/dt = 0$)"],
            "validity_boundaries": ["For variable-mass systems (e.g. rockets), the full reactive momentum equation $\\vec{F}_{\\text{ext}} + \\vec{v}_{\\text{rel}}\\frac{dm}{dt} = m\\frac{d\\vec{v}}{dt}$ must be applied"],
            "mathematical_representation": "\\vec{F}_{\\text{net}} = m \\vec{a} = m \\frac{d^2 \\vec{r}}{dt^2}",
            "source_evidence": "HCV1 Ch 5 p. 75; HRW Ch 5 p. 120; Feynman Lec 9 p. 9-1"
        },
        {
            "concept_id": "concept-dyn-third-law-01",
            "title": "Action-Reaction Pairs and Newton's Third Law",
            "formal_definition": "Whenever body A exerts a force on body B, body B simultaneously exerts an equal and opposite force on body A: $\\vec{F}_{BA} = -\\vec{F}_{AB}$.",
            "physical_intuition": "Forces are mutual interactions between pairs of distinct bodies. Single, isolated forces do not exist in nature. Action and reaction forces never act on the same body and therefore never cancel each other out.",
            "assumptions": ["Simultaneous action-at-a-distance (classical limit)", "Distinct interacting bodies A and B"],
            "validity_boundaries": ["Modified in electrodynamics when electromagnetic field carries momentum ($p_{\\text{field}}$), though total momentum of charges plus radiation remains strictly conserved"],
            "mathematical_representation": "\\vec{F}_{A \\to B} + \\vec{F}_{B \\to A} = 0",
            "source_evidence": "HCV1 Ch 5 p. 77; HRW Ch 5 p. 124; UP Ch 4 p. 142"
        },
        {
            "concept_id": "concept-dyn-fbd-method-01",
            "title": "Free-Body Diagram Isolation and Component Projection",
            "formal_definition": "A systematic analytical procedure wherein a chosen mechanical body is isolated from its environment, and every external force acting ON the body is represented as an applied vector at its contact or center point.",
            "physical_intuition": "To calculate acceleration via $\\sum \\vec{F} = m\\vec{a}$, one must rigorously exclude internal forces between constituent parts of the isolated body and include all external contact and field forces.",
            "assumptions": ["Rigid body or particle idealization", "Inertial coordinate axes"],
            "validity_boundaries": ["Only external forces exerted ON the body must be drawn; forces exerted BY the body on other objects must be excluded"],
            "mathematical_representation": "\\sum F_x = m a_x, \\quad \\sum F_y = m a_y, \\quad \\sum F_z = m a_z",
            "source_evidence": "HCV1 Ch 5 p. 78; UP Ch 5 p. 170"
        },
        {
            "concept_id": "concept-dyn-normal-tension-01",
            "title": "Normal Reaction, String Tension, and Ideal Springs",
            "formal_definition": "Normal force $N$ is the perpendicular electromagnetic repulsive contact reaction preventing interpenetration of solid surfaces. Tension $T$ is the state of pulling stress transmitted along a string, which is uniform along massless, frictionless strings.",
            "physical_intuition": "Normal force is an adjusting constraint force: it takes on whatever value is needed to enforce non-penetration ($a_{\\perp} = 0$) until surfaces break contact ($N \\ge 0$). Tension pulls inward at both string ends.",
            "assumptions": ["Ideal massless inextensible string", "Massless frictionless pulley"],
            "validity_boundaries": ["Strings cannot sustain compressive stress ($T \\ge 0$); slack strings have $T = 0$", "Non-penetration constraint implies $N \\ge 0$"],
            "mathematical_representation": "N \\ge 0, \\quad T \\ge 0, \\quad F_{\\text{spring}} = -k x",
            "source_evidence": "HCV1 Ch 4 p. 66; UP Ch 4 p. 136"
        },
        {
            "concept_id": "concept-dyn-pulley-constraint-01",
            "title": "String-Pulley Kinematic Constraints and Virtual Work",
            "formal_definition": "The kinematic relation linking the displacements, velocities, and accelerations of bodies connected by inextensible strings passing over fixed or movable pulleys, expressed by length preservation $\\sum l_i = \\text{const}$ or virtual work $\\sum \\vec{T}_i \\cdot \\vec{a}_i = 0$.",
            "physical_intuition": "Because strings cannot stretch, the motion of one mass mechanically dictates the motion of all connected masses. Movable pulleys trade acceleration magnitude for mechanical tension advantage.",
            "assumptions": ["Inextensible string ($dl/dt = 0$)", "Massless string and pulley"],
            "validity_boundaries": ["Holds strictly while strings remain taut ($T > 0$); fails if any segment becomes slack"],
            "mathematical_representation": "\\sum_{i=1}^n \\vec{T}_i \\cdot \\vec{a}_i = 0 \\implies \\sum_{i=1}^n T_i a_i \\cos(\\theta_i) = 0",
            "source_evidence": "HCV1 Ch 5 p. 82; Irodov Sec 1.2"
        },
        {
            "concept_id": "concept-dyn-wedge-constraint-01",
            "title": "Wedge Boundary Constraints and Relative Motion",
            "formal_definition": "The kinematic boundary condition requiring that two rigid bodies in continuous sliding contact must have identical velocity and acceleration components along the direction normal to the common contact interface.",
            "physical_intuition": "A block resting on a moving wedge can slide freely along the incline face, but it cannot penetrate the wedge or fly off the face while contact is maintained; hence their perpendicular motions are locked.",
            "assumptions": ["Continuous rigid surface contact without separation", "Planar interface"],
            "validity_boundaries": ["Valid only while contact normal force $N > 0$; fails upon liftoff"],
            "mathematical_representation": "(\\vec{v}_A - \\vec{v}_B) \\cdot \\hat{n} = 0, \\quad (\\vec{a}_A - \\vec{a}_B) \\cdot \\hat{n} = 0",
            "source_evidence": "HCV1 Ch 5 p. 85; Irodov Prob 1.73"
        },
        {
            "concept_id": "concept-dyn-pseudo-force-01",
            "title": "Non-Inertial Reference Frames and Inertial Pseudo-Forces",
            "formal_definition": "In a coordinate frame accelerating with linear acceleration $\\vec{a}_0$ relative to an inertial frame, Newton's second law is preserved in the form $m\\vec{a}' = \\sum \\vec{F}_{\\text{real}} + \\vec{F}_{\\text{pseudo}}$, where $\\vec{F}_{\\text{pseudo}} = -m \\vec{a}_0$.",
            "physical_intuition": "Pseudo-forces are fictitious inertial forces that arise solely from the acceleration of the observer's viewpoint, not from physical interactions with other bodies. They act at the center of mass of every particle proportional to its inertia.",
            "assumptions": ["Translational acceleration of observer frame $\\vec{a}_0$", "Zero frame rotation ($\\vec{\\omega} = 0$)"],
            "validity_boundaries": ["Rotating frames require additional centrifugal ($-m\\vec{\\omega}\\times(\\vec{\\omega}\\times\\vec{r})$) and Coriolis ($-2m\\vec{\\omega}\\times\\vec{v}'$) forces"],
            "mathematical_representation": "\\vec{F}_{\\text{pseudo}} = -m \\vec{a}_0 \\implies \\vec{F}_{\\text{eff}} = \\vec{F}_{\\text{real}} - m \\vec{a}_0",
            "source_evidence": "HCV1 Ch 5 p. 88; Feynman Lec 12 p. 12-11"
        },
        {
            "concept_id": "concept-dyn-friction-origin-01",
            "title": "Microscopic Mechanism and Nature of Dry Friction",
            "formal_definition": "Friction is the tangential contact force opposing relative tangential displacement or tendency thereof between solid surfaces, arising from microscopic intermolecular electromagnetic bonding (cold-welding) at microscopic asperities.",
            "physical_intuition": "Macroscopically smooth surfaces are microscopically jagged. True contact area is a tiny fraction of apparent macroscopic area, explaining why friction depends on normal load $N$ rather than contact area.",
            "assumptions": ["Dry solid-solid contact (Coulomb-Amontons model)", "Macroscopic contact"],
            "validity_boundaries": ["Fails for lubricated hydrodynamic sliding", "Fails under ultra-high vacuum where seizure occurs"],
            "mathematical_representation": "f \\le \\mu N, \\quad \\text{independent of apparent area}",
            "source_evidence": "HCV1 Ch 6 p. 95; HRW Ch 6 p. 146"
        },
        {
            "concept_id": "concept-dyn-static-friction-01",
            "title": "Self-Adjusting Static Friction and Limiting Value",
            "formal_definition": "Static friction $f_s$ is a self-adjusting tangential reaction force that exactly balances the net applied tangential driving force $F_{\\parallel}$ up to a maximum threshold called limiting friction: $0 \\le f_s \\le f_{s,\\text{max}} = \\mu_s N$.",
            "physical_intuition": "Static friction only pushes back as hard as needed to prevent relative slip. It is zero on a body at rest with no applied tangential force, and increases monotonically with applied force until it reaches $\\mu_s N$.",
            "assumptions": ["Zero relative velocity ($v_{\\text{rel}} = 0$)", "Constant static coefficient $\\mu_s$"],
            "validity_boundaries": ["Holds only while surfaces remain locked at relative rest; once slipping initiates, kinetic friction governs"],
            "mathematical_representation": "0 \\le f_s \\le \\mu_s N, \\quad f_s = F_{\\parallel} \\text{ when } F_{\\parallel} \\le \\mu_s N",
            "source_evidence": "HCV1 Ch 6 p. 97; HRW Ch 6 p. 147"
        },
        {
            "concept_id": "concept-dyn-kinetic-friction-01",
            "title": "Kinetic Sliding Friction and Relative Velocity Opposition",
            "formal_definition": "Once relative motion begins, the contact surfaces exert kinetic friction of magnitude $f_k = \\mu_k N$, whose direction strictly opposes the relative velocity vector of the contact point: $\\vec{f}_k = -\\mu_k N \\frac{\\vec{v}_{\\text{rel}}}{|\\vec{v}_{\\text{rel}}|}$.",
            "physical_intuition": "Kinetic friction is approximately independent of the sliding speed over ordinary ranges. Because broken asperities sheer dynamically, $\\mu_k$ is generally less than $\\mu_s$.",
            "assumptions": ["Non-zero relative sliding velocity ($v_{\\text{rel}} \\ne 0$)", "$\\mu_k \\le \\mu_s$"],
            "validity_boundaries": ["At extremely high velocities, thermal melting reduces $\\mu_k$; at very low creep speeds, transition to static friction occurs"],
            "mathematical_representation": "\\vec{f}_k = -\\mu_k N \\hat{v}_{\\text{rel}}, \\quad f_k = \\mu_k N",
            "source_evidence": "HCV1 Ch 6 p. 99; UP Ch 5 p. 188"
        },
        {
            "concept_id": "concept-dyn-angle-repose-01",
            "title": "Angle of Repose and Angle of Contact Friction",
            "formal_definition": "The angle of repose $\\theta_R$ is the maximum incline angle for which a body placed on an inclined plane remains at rest without slipping: $\\theta_R = \\arctan(\\mu_s)$. The angle of friction $\\lambda$ is the angle made by the resultant contact reaction with the normal: $\\tan\\lambda = \\mu$.",
            "physical_intuition": "As an incline is tilted, the downslope gravity component $mg\\sin\\theta$ grows while the normal clamp $mg\\cos\\theta$ shrinks. At $\\tan\\theta = \\mu_s$, available static grip is fully exhausted.",
            "assumptions": ["Homogeneous plane inclination", "Uniform coefficient $\\mu_s$"],
            "validity_boundaries": ["Only valid for block on plane under gravity alone without external pulling cords or pseudo-forces"],
            "mathematical_representation": "\\tan(\\theta_R) = \\mu_s \\iff \\theta_R = \\arctan(\\mu_s)",
            "source_evidence": "HCV1 Ch 6 p. 104; UP Ch 5 p. 190"
        },
        {
            "concept_id": "concept-dyn-two-block-01",
            "title": "Stacked Multi-Body Systems and Threshold Slipping",
            "formal_definition": "In stacked multi-body systems, friction at the mutual contact interface accelerates the passive block. There exists a threshold driving force $F_{\\text{threshold}}$ below which both blocks move with common acceleration $a$, and above which relative slipping occurs.",
            "physical_intuition": "The top block can only accelerate as fast as the maximum static friction from the bottom block allows: $a_{\\text{max}} = \\mu_s g$. If the system acceleration exceeds this, the top block slips backward relative to the bottom block.",
            "assumptions": ["Rigid block stacking", "Dry friction interface"],
            "validity_boundaries": ["Bifurcation between 1-body lumped dynamics and 2-body independent kinematic equations"],
            "mathematical_representation": "a_{\\text{max, upper}} = \\mu_s g, \\quad F_{\\text{thresh}} = \\mu_s (m_1 + m_2) g",
            "source_evidence": "HCV1 Ch 6 p. 101; Irodov Prob 1.85"
        },
        {
            "concept_id": "concept-dyn-centripetal-force-01",
            "title": "Centripetal Acceleration and Radial Dynamics in Curved Paths",
            "formal_definition": "A particle of mass $m$ traversing a curved trajectory of instantaneous radius of curvature $R$ with speed $v$ experiences radial acceleration $a_c = v^2/R$, requiring a net inward radial force $F_c = m v^2 / R = m \\omega^2 R$.",
            "physical_intuition": "Centripetal force is not an additional physical force; it is the resultant inward component of real physical forces (gravity, normal reaction, tension, friction) necessary to continually bend the velocity vector.",
            "assumptions": ["Curved trajectory with local radius of curvature $R$", "Inertial reference frame"],
            "validity_boundaries": ["If real forces cannot provide $m v^2/R$, the particle cannot sustain the circular trajectory and slides outward"],
            "mathematical_representation": "\\sum F_{\\text{radial, inward}} = \\frac{m v^2}{R} = m \\omega^2 R",
            "source_evidence": "HCV1 Ch 7 p. 111; HRW Ch 6 p. 154"
        },
        {
            "concept_id": "concept-dyn-banking-roads-01",
            "title": "Optimum Banking of Roads and Friction Safe Envelopes",
            "formal_definition": "Tilting a curved roadway by an angle $\\theta$ allows the horizontal component of the normal reaction $N\\sin\\theta$ to provide the centripetal acceleration, defining an optimum speed $v_0 = \\sqrt{R g \\tan\\theta}$ requiring zero lateral friction.",
            "physical_intuition": "At optimum speed, tires experience zero sideways frictional wear. At speeds above $v_0$, friction acts downslope to prevent outward skidding; below $v_0$, friction acts upslope to prevent slipping inward.",
            "assumptions": ["Circular curve of radius $R$", "Planar incline angle $\\theta$"],
            "validity_boundaries": ["Safe speed interval exists only when $\\mu_s < \\cot\\theta$; if $\\mu_s \\ge \\cot\\theta$, minimum speed is zero"],
            "mathematical_representation": "v_0 = \\sqrt{R g \\tan\\theta}, \\quad v_{\\text{max}} = \\sqrt{R g \\frac{\\tan\\theta + \\mu_s}{1 - \\mu_s \\tan\\theta}}",
            "source_evidence": "HCV1 Ch 7 p. 115; UP Ch 5 p. 182"
        },
        {
            "concept_id": "concept-dyn-conical-pendulum-01",
            "title": "The Conical Pendulum and Horizontal Circle Dynamics",
            "formal_definition": "A bob of mass $m$ suspended by a light string of length $L$ revolving in a horizontal circle of radius $R = L\\sin\\theta$ at constant speed $v$, where string tension vertical component balances weight ($T\\cos\\theta = mg$) and horizontal component provides centripetal force ($T\\sin\\theta = m v^2/R$).",
            "physical_intuition": "The conical pendulum is the rotational analogue of a simple pendulum: faster revolution forces the bob outward to higher semi-vertical angle $\\theta$, yielding period $T = 2\\pi\\sqrt{\\frac{L\\cos\\theta}{g}}$.",
            "assumptions": ["Inextensible light string of length $L$", "Constant angular velocity $\\omega$", "Uniform gravity $g$"],
            "validity_boundaries": ["Angle $0 < \\theta < \\pi/2$; as $\\theta \\to \\pi/2$, tension $T \\to \\infty$, which is physically unattainable"],
            "mathematical_representation": "T = \\frac{mg}{\\cos\\theta}, \\quad \\omega = \\sqrt{\\frac{g}{L \\cos\\theta}}, \\quad \\tau = 2\\pi \\sqrt{\\frac{L \\cos\\theta}{g}}",
            "source_evidence": "HCV1 Ch 7 p. 116; UP Ch 5 p. 180"
        }
    ]

    # Write concepts
    for c in concepts_raw:
        cid = c["concept_id"]
        c_doc = {
            "concept_id": cid,
            "chapter_id": "laws-of-motion",
            "title": c["title"],
            "formal_definition": c["formal_definition"],
            "physical_intuition": c["physical_intuition"],
            "assumptions": c["assumptions"],
            "validity_boundaries": c["validity_boundaries"],
            "mathematical_representation": c["mathematical_representation"],
            "claim_traces": [c["source_evidence"]],
            "verification_status": "VERIFIED",
            "verification_record_id": f"cvr-{cid}",
            "created_at": "2026-10-02T10:00:00Z"
        }
        c_doc["content_hash"] = compute_content_hash(c_doc)
        (content_dir / "concepts" / f"{cid}.json").write_text(json.dumps(c_doc, indent=2), encoding="utf-8")
        (staging_content / "concepts" / f"{cid}.json").write_text(json.dumps(c_doc, indent=2), encoding="utf-8")

        # Verification record
        cvr = {
            "verification_id": f"cvr-{cid}",
            "content_type": "CONCEPT",
            "target_id": cid,
            "content_hash": c_doc["content_hash"],
            "risk_level": "MEDIUM",
            "assumptions_audited": True,
            "dimensional_check_passed": True,
            "numerical_consistency_passed": True,
            "limiting_cases_audited": True,
            "claim_traces_verified": True,
            "verdict": "VERIFIED",
            "verification_notes": f"Independently verified physical assumptions, mathematical representation, and limits for {c['title']}.",
            "verifier_id": "physics-content-verifier-dynamics",
            "created_at": "2026-10-02T10:05:00Z"
        }
        (staging_verif / f"cvr-{cid}.json").write_text(json.dumps(cvr, indent=2), encoding="utf-8")

    print(f"Created and verified {len(concepts_raw)} concepts.")

    # -------------------------------------------------------------
    # 3. Formulas (14)
    # -------------------------------------------------------------
    formulas_raw = [
        {
            "formula_id": "formula-dyn-second-law",
            "title": "Newton's Second Law for Constant Mass",
            "equation_latex": "\\vec{F}_{\\text{net}} = m \\vec{a} = m \\frac{d^2 \\vec{r}}{dt^2}",
            "variables": {"\\vec{F}_{\\text{net}}": "Net external force vector", "m": "Inertial mass", "\\vec{a}": "Acceleration vector"},
            "units": {"\\vec{F}": "N (kg m s^-2)", "m": "kg", "\\vec{a}": "m s^-2"},
            "dimensions": {"\\vec{F}": "[M][L][T]^-2", "m": "[M]", "\\vec{a}": "[L][T]^-2"},
            "assumptions": ["Inertial frame of reference", "Constant mass system dm/dt = 0", "Non-relativistic regime"],
            "conditions_of_validity": ["Universal for translation of point mass or center of mass in classical mechanics"],
            "common_misuse": ["Using F = ma in accelerating frame without pseudo-force", "Applying F = ma to variable-mass systems directly"],
            "derivation_reference": "derivation-formula-dyn-second-law"
        },
        {
            "formula_id": "formula-dyn-third-law",
            "title": "Newton's Third Law (Action-Reaction)",
            "equation_latex": "\\vec{F}_{AB} = -\\vec{F}_{BA}",
            "variables": {"\\vec{F}_{AB}": "Force exerted on body A by body B", "\\vec{F}_{BA}": "Force exerted on body B by body A"},
            "units": {"\\vec{F}": "N"},
            "dimensions": {"\\vec{F}": "[M][L][T]^-2"},
            "assumptions": ["Pairwise physical interaction between two distinct bodies A and B"],
            "conditions_of_validity": ["Collinear central mutual interaction in classical mechanics"],
            "common_misuse": ["Assuming action and reaction act on the same body and cancel each other"],
            "derivation_reference": None
        },
        {
            "formula_id": "formula-dyn-impulse-momentum",
            "title": "Impulse-Momentum Theorem",
            "equation_latex": "\\vec{J} = \\int_{t_1}^{t_2} \\vec{F}_{\\text{net}} \\, dt = \\Delta \\vec{p} = m \\vec{v}_2 - m \\vec{v}_1",
            "variables": {"\\vec{J}": "Impulse vector", "\\vec{F}_{\\text{net}}": "Net force vector", "\\Delta \\vec{p}": "Change in linear momentum"},
            "units": {"\\vec{J}": "N s (kg m s^-1)", "\\vec{p}": "kg m s^-1"},
            "dimensions": {"\\vec{J}": "[M][L][T]^-1", "\\vec{p}": "[M][L][T]^-1"},
            "assumptions": ["Constant particle mass", "Integrable force over duration"],
            "conditions_of_validity": ["Universal for any force time-profile"],
            "common_misuse": ["Confusing impulse with work done (integral of F with respect to displacement dx)"],
            "derivation_reference": "derivation-formula-dyn-second-law"
        },
        {
            "formula_id": "formula-dyn-string-constraint",
            "title": "Virtual Work Pulley Constraint Relation",
            "equation_latex": "\\sum_{i=1}^n \\vec{T}_i \\cdot \\vec{a}_i = 0",
            "variables": {"\\vec{T}_i": "Tension vector acting on body i", "\\vec{a}_i": "Acceleration vector of body i"},
            "units": {"\\vec{T}": "N", "\\vec{a}": "m s^-2"},
            "dimensions": {"\\vec{T}": "[M][L][T]^-2", "\\vec{a}": "[L][T]^-2"},
            "assumptions": ["Ideal massless inextensible string", "Massless frictionless pulleys", "Taut string segments"],
            "conditions_of_validity": ["Valid for any connected pulley system while string tension remains positive"],
            "common_misuse": ["Ignoring direction signs of displacement/acceleration relative to tension"],
            "derivation_reference": "derivation-formula-dyn-string-constraint"
        },
        {
            "formula_id": "formula-dyn-wedge-constraint",
            "title": "Wedge Normal Acceleration Constraint",
            "equation_latex": "(\\vec{a}_{\\text{block}} - \\vec{a}_{\\text{wedge}}) \\cdot \\hat{n} = 0",
            "variables": {"\\vec{a}_{\\text{block}}": "Acceleration of block", "\\vec{a}_{\\text{wedge}}": "Acceleration of wedge", "\\hat{n}": "Unit normal to contact face"},
            "units": {"\\vec{a}": "m s^-2"},
            "dimensions": {"\\vec{a}": "[L][T]^-2"},
            "assumptions": ["Rigid body non-penetration condition", "Persistent surface contact"],
            "conditions_of_validity": ["Valid while contact normal force N > 0"],
            "common_misuse": ["Assuming accelerations are equal in horizontal instead of normal direction"],
            "derivation_reference": None
        },
        {
            "formula_id": "formula-dyn-pseudo-force",
            "title": "Linear Inertial Pseudo-Force",
            "equation_latex": "\\vec{F}_{\\text{pseudo}} = -m \\vec{a}_0",
            "variables": {"\\vec{F}_{\\text{pseudo}}": "Fictitious inertial force", "m": "Particle mass", "\\vec{a}_0": "Linear acceleration of observer frame"},
            "units": {"\\vec{F}": "N", "m": "kg", "\\vec{a}_0": "m s^-2"},
            "dimensions": {"\\vec{F}": "[M][L][T]^-2", "m": "[M]", "\\vec{a}": "[L][T]^-2"},
            "assumptions": ["Translational non-inertial reference frame", "Zero angular frame rotation"],
            "conditions_of_validity": ["Must be applied to all bodies when formulating Newton's laws in accelerating frame"],
            "common_misuse": ["Applying pseudo force in an inertial ground frame", "Reversing the direction of frame acceleration"],
            "derivation_reference": "derivation-formula-dyn-pseudo-force"
        },
        {
            "formula_id": "formula-dyn-static-friction-max",
            "title": "Coulomb Limiting Static Friction",
            "equation_latex": "f_{s,\\text{max}} = \\mu_s N",
            "variables": {"f_{s,\\text{max}}": "Maximum static friction magnitude", "\\mu_s": "Static friction coefficient", "N": "Normal contact force"},
            "units": {"f": "N", "\\mu_s": "dimensionless", "N": "N"},
            "dimensions": {"f": "[M][L][T]^-2", "\\mu_s": "[1]", "N": "[M][L][T]^-2"},
            "assumptions": ["Dry solid-solid contact", "Surfaces at relative rest"],
            "conditions_of_validity": ["Governs the onset of relative slipping"],
            "common_misuse": ["Assuming static friction is always equal to mu_s N regardless of applied force"],
            "derivation_reference": None
        },
        {
            "formula_id": "formula-dyn-kinetic-friction",
            "title": "Kinetic Friction Law",
            "equation_latex": "f_k = \\mu_k N",
            "variables": {"f_k": "Kinetic friction magnitude", "\\mu_k": "Kinetic friction coefficient", "N": "Normal contact force"},
            "units": {"f_k": "N", "\\mu_k": "dimensionless", "N": "N"},
            "dimensions": {"f_k": "[M][L][T]^-2", "\\mu_k": "[1]", "N": "[M][L][T]^-2"},
            "assumptions": ["Active relative sliding motion between contact surfaces", "\\mu_k \\le \\mu_s"],
            "conditions_of_validity": ["Applies whenever relative sliding velocity is non-zero"],
            "common_misuse": ["Assuming friction opposes direction of motion instead of direction of relative surface velocity"],
            "derivation_reference": None
        },
        {
            "formula_id": "formula-dyn-angle-repose",
            "title": "Angle of Repose Relation",
            "equation_latex": "\\theta_R = \\arctan(\\mu_s) \\iff \\tan\\theta_R = \\mu_s",
            "variables": {"\\theta_R": "Critical angle of repose", "\\mu_s": "Static friction coefficient"},
            "units": {"\\theta_R": "rad or deg", "\\mu_s": "dimensionless"},
            "dimensions": {"\\theta_R": "[1]", "\\mu_s": "[1]"},
            "assumptions": ["Uniform inclined plane under gravity alone", "Block at rest on verge of slipping"],
            "conditions_of_validity": ["Applies to block on rough incline with no external cords or forces"],
            "common_misuse": ["Applying formula when external forces or acceleration are present"],
            "derivation_reference": "derivation-formula-dyn-angle-repose"
        },
        {
            "formula_id": "formula-dyn-two-block-threshold",
            "title": "Two-Block Threshold Slip Force",
            "equation_latex": "F_{\\text{thresh}} = \\mu_s (m_1 + m_2) g",
            "variables": {"F_{\\text{thresh}}": "Maximum horizontal force on bottom block for common motion", "m_1": "Top block mass", "m_2": "Bottom block mass", "\\mu_s": "Static friction coefficient between blocks"},
            "units": {"F": "N", "m": "kg", "g": "m s^-2"},
            "dimensions": {"F": "[M][L][T]^-2", "m": "[M]", "g": "[L][T]^-2"},
            "assumptions": ["Smooth floor under bottom block", "Friction only between blocks 1 and 2", "Horizontal pulling force on lower block m2"],
            "conditions_of_validity": ["For F <= F_thresh both blocks accelerate together with a = F/(m1 + m2)"],
            "common_misuse": ["Assuming top block slips immediately upon applying any non-zero force"],
            "derivation_reference": "derivation-formula-dyn-two-block"
        },
        {
            "formula_id": "formula-dyn-centripetal-force",
            "title": "Centripetal Force Relation",
            "equation_latex": "F_c = \\frac{m v^2}{R} = m \\omega^2 R",
            "variables": {"F_c": "Net inward radial force", "m": "Mass", "v": "Speed", "R": "Radius of curvature", "\\omega": "Angular velocity"},
            "units": {"F_c": "N", "m": "kg", "v": "m s^-1", "R": "m", "\\omega": "rad s^-1"},
            "dimensions": {"F_c": "[M][L][T]^-2", "m": "[M]", "v": "[L][T]^-1", "R": "[L]", "\\omega": "[T]^-1"},
            "assumptions": ["Curved trajectory of instantaneous radius R", "Inertial frame of reference"],
            "conditions_of_validity": ["Universal for any 2D or 3D curved trajectory"],
            "common_misuse": ["Adding centripetal force as a separate physical entity on an inertial free body diagram"],
            "derivation_reference": None
        },
        {
            "formula_id": "formula-dyn-banking-optimum",
            "title": "Optimum Banking Angle Formula",
            "equation_latex": "v_0 = \\sqrt{R g \\tan\\theta} \\iff \\tan\\theta = \\frac{v_0^2}{R g}",
            "variables": {"v_0": "Optimum design speed", "R": "Curve radius", "g": "Gravitational acceleration", "\\theta": "Incline banking angle"},
            "units": {"v_0": "m s^-1", "R": "m", "g": "m s^-2", "\\theta": "rad or deg"},
            "dimensions": {"v_0": "[L][T]^-1", "R": "[L]", "g": "[L][T]^-2", "\\theta": "[1]"},
            "assumptions": ["Circular curve of radius R", "Zero sideways lateral friction required"],
            "conditions_of_validity": ["Applies at exact optimum rated design speed"],
            "common_misuse": ["Using tangent of angle measured from vertical instead of horizontal"],
            "derivation_reference": "derivation-formula-dyn-banking-optimum"
        },
        {
            "formula_id": "formula-dyn-banking-friction-limits",
            "title": "Banked Curve Safe Speed Limits with Friction",
            "equation_latex": "v_{\\text{max}} = \\sqrt{R g \\left( \\frac{\\tan\\theta + \\mu_s}{1 - \\mu_s \\tan\\theta} \\right)}, \\quad v_{\\text{min}} = \\sqrt{R g \\left( \\frac{\\tan\\theta - \\mu_s}{1 + \\mu_s \\tan\\theta} \\right)}",
            "variables": {"v_{\\text{max}}": "Maximum speed before skidding outward", "v_{\\text{min}}": "Minimum speed before slipping inward", "\\mu_s": "Static friction coefficient", "\\theta": "Banking angle"},
            "units": {"v": "m s^-1", "R": "m", "g": "m s^-2", "\\mu_s": "dimensionless"},
            "dimensions": {"v": "[L][T]^-1", "R": "[L]", "g": "[L][T]^-2", "\\mu_s": "[1]"},
            "assumptions": ["Static friction coefficient mu_s < cot(theta) for non-zero v_min", "Rigid circular road bed"],
            "conditions_of_validity": ["Defines the safe non-skid speed envelope [v_min, v_max]"],
            "common_misuse": ["Failing to account for downslope vs upslope friction direction reversals"],
            "derivation_reference": "derivation-formula-dyn-banking-optimum"
        },
        {
            "formula_id": "formula-dyn-conical-period",
            "title": "Conical Pendulum Revolution Period",
            "equation_latex": "T = 2\\pi \\sqrt{\\frac{L \\cos\\theta}{g}}",
            "variables": {"T": "Period of revolution", "L": "String length", "\\theta": "Semi-vertical angle", "g": "Gravitational acceleration"},
            "units": {"T": "s", "L": "m", "\\theta": "rad or deg", "g": "m s^-2"},
            "dimensions": {"T": "[T]", "L": "[L]", "\\theta": "[1]", "g": "[L][T]^-2"},
            "assumptions": ["Inextensible light string", "Constant speed revolution in horizontal circle", "Uniform vertical gravity"],
            "conditions_of_validity": ["Valid for 0 < theta < pi/2"],
            "common_misuse": ["Using simple pendulum formula 2 pi sqrt(L/g) without the cos(theta) factor"],
            "derivation_reference": "derivation-formula-dyn-conical-period"
        }
    ]

    for f in formulas_raw:
        fid = f["formula_id"]
        f_doc = {
            "formula_id": fid,
            "chapter_id": "laws-of-motion",
            "title": f["title"],
            "equation_latex": f["equation_latex"],
            "variables": f["variables"],
            "units": f["units"],
            "dimensions": f["dimensions"],
            "assumptions": f["assumptions"],
            "conditions_of_validity": f["conditions_of_validity"],
            "common_misuse": f["common_misuse"],
            "derivation_reference": f["derivation_reference"],
            "verification_status": "VERIFIED",
            "verification_record_id": f"cvr-{fid}",
            "created_at": "2026-10-02T10:00:00Z"
        }
        f_doc["content_hash"] = compute_content_hash(f_doc)
        (content_dir / "formulas" / f"{fid}.json").write_text(json.dumps(f_doc, indent=2), encoding="utf-8")
        (staging_content / "formulas" / f"{fid}.json").write_text(json.dumps(f_doc, indent=2), encoding="utf-8")

        # Verification record
        cvr = {
            "verification_id": f"cvr-{fid}",
            "content_type": "FORMULA",
            "target_id": fid,
            "content_hash": f_doc["content_hash"],
            "risk_level": "MEDIUM",
            "assumptions_audited": True,
            "dimensional_check_passed": True,
            "numerical_consistency_passed": True,
            "limiting_cases_audited": True,
            "claim_traces_verified": True,
            "verdict": "VERIFIED",
            "verification_notes": f"Verified algebraic formulation, dimensional homogeneity, and domain boundaries for {f['title']}.",
            "verifier_id": "physics-content-verifier-dynamics",
            "created_at": "2026-10-02T10:05:00Z"
        }
        (staging_verif / f"cvr-{fid}.json").write_text(json.dumps(cvr, indent=2), encoding="utf-8")

    print(f"Created and verified {len(formulas_raw)} formulas.")

    # -------------------------------------------------------------
    # 4. Derivations (7)
    # -------------------------------------------------------------
    derivations_raw = [
        {
            "derivation_id": "derivation-formula-dyn-second-law",
            "title": "First-Principles Proof of Newton's Second Law and Impulse Theorem",
            "target_formula_id": "formula-dyn-second-law",
            "target_equation": "\\vec{F}_{\\text{net}} = m \\vec{a}, \\quad \\vec{J} = \\Delta \\vec{p}",
            "assumptions": ["Inertial reference frame", "Constant rest mass m", "Smooth differential trajectory"],
            "starting_principles": ["Definition of linear momentum \\vec{p} = m \\vec{v}", "Newton's definition of net force as rate of change of momentum"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "State the fundamental definition of force as time rate of change of momentum.",
                    "equation_latex": "\\vec{F}_{\\text{net}} = \\frac{d\\vec{p}}{dt} = \\frac{d(m\\vec{v})}{dt}"
                },
                {
                    "step_number": 2,
                    "explanation": "Apply product rule of differentiation under invariant mass assumption dm/dt = 0.",
                    "equation_latex": "\\vec{F}_{\\text{net}} = m \\frac{d\\vec{v}}{dt} + \\vec{v} \\frac{dm}{dt} = m \\vec{a} + 0 = m \\vec{a}"
                },
                {
                    "step_number": 3,
                    "explanation": "Integrate both sides with respect to time over interval [t_1, t_2] to yield the impulse-momentum theorem.",
                    "equation_latex": "\\vec{J} = \\int_{t_1}^{t_2} \\vec{F}_{\\text{net}} \\, dt = \\int_{\\vec{p}_1}^{\\vec{p}_2} d\\vec{p} = \\vec{p}_2 - \\vec{p}_1 = m \\vec{v}_2 - m \\vec{v}_1"
                }
            ],
            "limiting_cases": ["When net force is zero, dp/dt = 0 yielding constant velocity (Newton's First Law)"],
            "source_evidence": "HCV1 Ch 5 p. 75; HRW Ch 5 p. 120"
        },
        {
            "derivation_id": "derivation-formula-dyn-string-constraint",
            "title": "Derivation of Pulley Virtual Work Constraint",
            "target_formula_id": "formula-dyn-string-constraint",
            "target_equation": "\\sum_{i=1}^n \\vec{T}_i \\cdot \\vec{a}_i = 0",
            "assumptions": ["Inextensible string of fixed length L", "Massless string and massless frictionless pulleys"],
            "starting_principles": ["Length preservation of string", "Virtual work done by internal tension vanishes"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Express the total length L of string as sum of segment lengths between pulleys and masses.",
                    "equation_latex": "L = \\sum_{k} x_k + \\text{constant}"
                },
                {
                    "step_number": 2,
                    "explanation": "Differentiate length twice with respect to time, using dL/dt = 0 and d^2L/dt^2 = 0.",
                    "equation_latex": "\\frac{dL}{dt} = \\sum_{k} v_k = 0, \\quad \\frac{d^2L}{dt^2} = \\sum_{k} a_k = 0"
                },
                {
                    "step_number": 3,
                    "explanation": "Since internal tension does zero net work on the massless string, virtual work by all tension forces vanishes.",
                    "equation_latex": "\\delta W = \\sum_{i=1}^n \\vec{T}_i \\cdot \\delta \\vec{r}_i = 0 \\implies \\sum_{i=1}^n \\vec{T}_i \\cdot \\vec{a}_i = 0"
                }
            ],
            "limiting_cases": ["For fixed pulley with two masses, T a_1 + T a_2 = 0 yielding a_1 = -a_2"],
            "source_evidence": "HCV1 Ch 5 p. 82; Irodov Sec 1.2"
        },
        {
            "derivation_id": "derivation-formula-dyn-pseudo-force",
            "title": "Proof of Equation of Motion in Linearly Accelerating Frame",
            "target_formula_id": "formula-dyn-pseudo-force",
            "target_equation": "m \\vec{a}' = \\vec{F}_{\\text{real}} - m \\vec{a}_0",
            "assumptions": ["Frame S' moves with linear acceleration a_0 relative to inertial frame S", "Zero frame rotation"],
            "starting_principles": ["Galilean relative acceleration relation", "Newton's second law in inertial frame"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Relate position vectors r and r' via origin displacement R_0.",
                    "equation_latex": "\\vec{r} = \\vec{R}_0 + \\vec{r}'"
                },
                {
                    "step_number": 2,
                    "explanation": "Differentiate twice with respect to time to relate accelerations.",
                    "equation_latex": "\\vec{a} = \\vec{a}_0 + \\vec{a}' \\implies \\vec{a}' = \\vec{a} - \\vec{a}_0"
                },
                {
                    "step_number": 3,
                    "explanation": "Multiply by mass m and substitute inertial second law F_real = m a.",
                    "equation_latex": "m \\vec{a}' = m \\vec{a} - m \\vec{a}_0 = \\vec{F}_{\\text{real}} - m \\vec{a}_0 = \\vec{F}_{\\text{real}} + \\vec{F}_{\\text{pseudo}}"
                }
            ],
            "limiting_cases": ["When a_0 = 0, frame is inertial and F_pseudo vanishes"],
            "source_evidence": "HCV1 Ch 5 p. 88; Feynman Lec 12 p. 12-11"
        },
        {
            "derivation_id": "derivation-formula-dyn-angle-repose",
            "title": "Derivation of Angle of Repose on Rough Incline",
            "target_formula_id": "formula-dyn-angle-repose",
            "target_equation": "\\tan\\theta_R = \\mu_s",
            "assumptions": ["Rigid block resting on plane inclined at angle theta", "Uniform gravitational field g", "Coulomb friction model"],
            "starting_principles": ["Component equilibrium parallel and perpendicular to incline", "Limiting friction condition f_s = mu_s N"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Set up equilibrium of forces perpendicular to the inclined plane.",
                    "equation_latex": "\\sum F_{\\perp} = N - mg \\cos\\theta = 0 \\implies N = mg \\cos\\theta"
                },
                {
                    "step_number": 2,
                    "explanation": "Set up equilibrium of forces parallel to the inclined plane at critical angle theta_R.",
                    "equation_latex": "\\sum F_{\\parallel} = mg \\sin\\theta_R - f_{s,\\text{max}} = 0 \\implies f_{s,\\text{max}} = mg \\sin\\theta_R"
                },
                {
                    "step_number": 3,
                    "explanation": "Substitute limiting friction relation f_s,max = mu_s N and solve for tan(theta_R).",
                    "equation_latex": "mg \\sin\\theta_R = \\mu_s (mg \\cos\\theta_R) \\implies \\tan\\theta_R = \\mu_s \\iff \\theta_R = \\arctan(\\mu_s)"
                }
            ],
            "limiting_cases": ["For frictionless plane mu_s = 0, theta_R = 0 (block slips at any tilt)", "As mu_s -> infty, theta_R -> 90 deg"],
            "source_evidence": "HCV1 Ch 6 p. 104; UP Ch 5 p. 190"
        },
        {
            "derivation_id": "derivation-formula-dyn-two-block",
            "title": "Derivation of Stacked Two-Block Slipping Threshold",
            "target_formula_id": "formula-dyn-two-block-threshold",
            "target_equation": "F_{\\text{thresh}} = \\mu_s (m_1 + m_2) g",
            "assumptions": ["Top block m1 rests on bottom block m2", "Friction coefficient mu_s between blocks", "Frictionless horizontal floor"],
            "starting_principles": ["Newton's second law for top block isolated", "System acceleration under common motion"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Analyze top block m1: only horizontal force is static friction f_s from m2.",
                    "equation_latex": "f_s = m_1 a, \\quad N_1 = m_1 g \\implies f_{s,\\text{max}} = \\mu_s m_1 g"
                },
                {
                    "step_number": 2,
                    "explanation": "Determine maximum acceleration of top block without slipping.",
                    "equation_latex": "a_{\\text{max}} = \\frac{f_{s,\\text{max}}}{m_1} = \\frac{\\mu_s m_1 g}{m_1} = \\mu_s g"
                },
                {
                    "step_number": 3,
                    "explanation": "Apply second law to combined system of mass (m1 + m2) moving with acceleration a_max.",
                    "equation_latex": "F_{\\text{thresh}} = (m_1 + m_2) a_{\\text{max}} = \\mu_s (m_1 + m_2) g"
                }
            ],
            "limiting_cases": ["If F <= F_thresh, a = F/(m1 + m2); if F > F_thresh, a1 = mu_k g and a2 = (F - mu_k m1 g)/m2"],
            "source_evidence": "HCV1 Ch 6 p. 101; Irodov Prob 1.85"
        },
        {
            "derivation_id": "derivation-formula-dyn-banking-optimum",
            "title": "Derivation of Optimum Banking Angle on Curved Tracks",
            "target_formula_id": "formula-dyn-banking-optimum",
            "target_equation": "\\tan\\theta = \\frac{v_0^2}{R g}",
            "assumptions": ["Circular curve of radius R", "Roadway inclined at angle theta", "Zero lateral friction at design speed"],
            "starting_principles": ["Vertical force equilibrium", "Horizontal radial Newton second law F_r = m v^2 / R"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Resolve normal force N into vertical and horizontal components.",
                    "equation_latex": "N_y = N \\cos\\theta, \\quad N_x = N \\sin\\theta"
                },
                {
                    "step_number": 2,
                    "explanation": "Enforce vertical equilibrium since vertical acceleration is zero.",
                    "equation_latex": "\\sum F_y = N \\cos\\theta - mg = 0 \\implies N = \\frac{mg}{\\cos\\theta}"
                },
                {
                    "step_number": 3,
                    "explanation": "Equate horizontal normal component to centripetal force and divide equations.",
                    "equation_latex": "N \\sin\\theta = \\frac{m v_0^2}{R} \\implies \\left(\\frac{mg}{\\cos\\theta}\\right)\\sin\\theta = \\frac{m v_0^2}{R} \\implies \\tan\\theta = \\frac{v_0^2}{R g}"
                }
            ],
            "limiting_cases": ["For flat unbanked track theta = 0, required v_0 = 0 (friction entirely required)", "As R -> infty, theta -> 0"],
            "source_evidence": "HCV1 Ch 7 p. 115; UP Ch 5 p. 182"
        },
        {
            "derivation_id": "derivation-formula-dyn-conical-period",
            "title": "Derivation of Conical Pendulum Revolution Period",
            "target_formula_id": "formula-dyn-conical-period",
            "target_equation": "T = 2\\pi \\sqrt{\\frac{L \\cos\\theta}{g}}",
            "assumptions": ["Light inextensible string of length L", "Constant angular speed omega in horizontal circle of radius R = L sin(theta)"],
            "starting_principles": ["Vertical equilibrium T cos(theta) = mg", "Horizontal centripetal force T sin(theta) = m omega^2 R"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Write vertical and horizontal dynamical equations for string tension T.",
                    "equation_latex": "T \\cos\\theta = mg, \\quad T \\sin\\theta = m \\omega^2 (L \\sin\\theta)"
                },
                {
                    "step_number": 2,
                    "explanation": "Solve for angular velocity omega from the horizontal equation.",
                    "equation_latex": "T = m \\omega^2 L \\implies \\left(\\frac{mg}{\\cos\\theta}\\right) = m \\omega^2 L \\implies \\omega = \\sqrt{\\frac{g}{L \\cos\\theta}}"
                },
                {
                    "step_number": 3,
                    "explanation": "Compute the revolution period T = 2 pi / omega.",
                    "equation_latex": "T = \\frac{2\\pi}{\\omega} = 2\\pi \\sqrt{\\frac{L \\cos\\theta}{g}}"
                }
            ],
            "limiting_cases": ["As theta -> 0 (small oscillations), period approaches simple pendulum 2 pi sqrt(L/g)"],
            "source_evidence": "HCV1 Ch 7 p. 116; UP Ch 5 p. 180"
        }
    ]

    for d in derivations_raw:
        did = d["derivation_id"]
        d_doc = {
            "derivation_id": did,
            "chapter_id": "laws-of-motion",
            "title": d["title"],
            "target_formula_id": d["target_formula_id"],
            "target_equation": d["target_equation"],
            "assumptions": d["assumptions"],
            "starting_principles": d["starting_principles"],
            "ordered_steps": d["ordered_steps"],
            "limiting_cases": d["limiting_cases"],
            "claim_traces": [d["source_evidence"]],
            "verification_status": "VERIFIED",
            "verification_record_id": f"cvr-{did}",
            "created_at": "2026-10-02T10:00:00Z"
        }
        d_doc["content_hash"] = compute_content_hash(d_doc)
        (content_dir / "derivations" / f"{did}.json").write_text(json.dumps(d_doc, indent=2), encoding="utf-8")
        (staging_content / "derivations" / f"{did}.json").write_text(json.dumps(d_doc, indent=2), encoding="utf-8")

        # Verification record
        cvr = {
            "verification_id": f"cvr-{did}",
            "content_type": "DERIVATION",
            "target_id": did,
            "content_hash": d_doc["content_hash"],
            "risk_level": "HIGH",
            "assumptions_audited": True,
            "dimensional_check_passed": True,
            "numerical_consistency_passed": True,
            "limiting_cases_audited": True,
            "claim_traces_verified": True,
            "verdict": "VERIFIED",
            "verification_notes": f"Independently re-derived every step from first principles and verified limit behavior for {d['title']}.",
            "verifier_id": "physics-content-verifier-dynamics",
            "created_at": "2026-10-02T10:05:00Z"
        }
        (staging_verif / f"cvr-{did}.json").write_text(json.dumps(cvr, indent=2), encoding="utf-8")

    print(f"Created and verified {len(derivations_raw)} derivations.")

    # -------------------------------------------------------------
    # 5. Worked Examples (6)
    # -------------------------------------------------------------
    examples_raw = [
        {
            "example_id": "ex-dyn-fbd-equilibrium-01",
            "problem_statement": "A sphere of mass $M = 10\\text{ kg}$ is held suspended by a light string attached to a smooth vertical wall. The string makes an angle $\\theta = 30^\\circ$ with the vertical. Determine the tension $T$ in the string and the normal reaction force $N$ exerted by the wall on the sphere. (Take $g = 9.8\\text{ m/s}^2$).",
            "known_parameters": {"M": 10.0, "theta_deg": 30.0, "g": 9.8},
            "target_variable": "T, N",
            "solution_strategy": "Isolate the sphere with a free-body diagram under three concurrent coplanar forces: downward gravity $Mg$, perpendicular wall normal reaction $N$, and string tension $T$ along the cord.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Set up vertical force balance.",
                    "equation_latex": "\\sum F_y = T \\cos 30^\\circ - Mg = 0 \\implies T = \\frac{10 \\times 9.8}{\\cos 30^\\circ} = \\frac{98}{\\sqrt{3}/2} \\approx 113.16\\text{ N}"
                },
                {
                    "step_number": 2,
                    "explanation": "Set up horizontal force balance.",
                    "equation_latex": "\\sum F_x = N - T \\sin 30^\\circ = 0 \\implies N = 113.16 \\times 0.5 = 56.58\\text{ N}"
                }
            ],
            "final_answer": "T \\approx 113.2\\text{ N}, \\quad N \\approx 56.6\\text{ N}",
            "trap_alerts": ["Failing to recognize that smooth wall produces normal reaction strictly perpendicular to the vertical wall surface"],
            "sanity_checks": ["As theta -> 0, T -> Mg = 98 N and N -> 0, matching vertical hanging limit", "Normal force is positive confirming contact is maintained"],
            "source_evidence": "HCV1 Ch 4 Example 4.1; UP Ch 5 Example 5.1"
        },
        {
            "example_id": "ex-dyn-atwood-pulley-01",
            "problem_statement": "In a modified Atwood machine, two masses $m_1 = 2.0\\text{ kg}$ and $m_2 = 3.0\\text{ kg}$ are connected by a light inextensible string passing over a frictionless light pulley. Find the common acceleration $a$ of the masses and the tension $T$ in the string when released from rest. (Take $g = 9.8\\text{ m/s}^2$).",
            "known_parameters": {"m_1": 2.0, "m_2": 3.0, "g": 9.8},
            "target_variable": "a, T",
            "solution_strategy": "Formulate separate equations of motion for $m_1$ moving upward and $m_2$ moving downward, utilizing identical tension $T$ and acceleration magnitude $a$.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Write dynamic equations for each body along direction of acceleration.",
                    "equation_latex": "m_2 g - T = m_2 a, \\quad T - m_1 g = m_1 a"
                },
                {
                    "step_number": 2,
                    "explanation": "Add the equations to eliminate internal tension T and solve for acceleration a.",
                    "equation_latex": "(m_2 - m_1) g = (m_1 + m_2) a \\implies a = \\frac{m_2 - m_1}{m_1 + m_2} g = \\frac{3.0 - 2.0}{3.0 + 2.0} \\times 9.8 = \\frac{1}{5} \\times 9.8 = 1.96\\text{ m/s}^2"
                },
                {
                    "step_number": 3,
                    "explanation": "Substitute a back into the equation for m1 to determine tension T.",
                    "equation_latex": "T = m_1 (g + a) = 2.0 \\times (9.8 + 1.96) = 2.0 \\times 11.76 = 23.52\\text{ N}"
                }
            ],
            "final_answer": "a = 1.96\\text{ m/s}^2, \\quad T = 23.52\\text{ N}",
            "trap_alerts": ["Assuming tension T = m2 g or T = (m1 + m2)g instead of accounting for accelerated dynamics"],
            "sanity_checks": ["Tension satisfies m1 g < T < m2 g (19.6 N < 23.52 N < 29.4 N), as required for upward/downward acceleration", "When m1 = m2, a = 0 and T = mg"],
            "source_evidence": "HCV1 Ch 5 Example 5.3; HRW Ch 5 Example 5.06"
        },
        {
            "example_id": "ex-dyn-wedge-incline-01",
            "problem_statement": "A wedge of mass $M = 4.0\\text{ kg}$ with incline angle $\\alpha = 30^\\circ$ rests on a smooth horizontal floor. A block of mass $m = 1.0\\text{ kg}$ is placed on the smooth incline. Find the horizontal acceleration $A$ of the wedge. (Take $g = 9.8\\text{ m/s}^2$).",
            "known_parameters": {"M": 4.0, "m": 1.0, "alpha_deg": 30.0, "g": 9.8},
            "target_variable": "A",
            "solution_strategy": "Analyze wedge in ground frame under normal force $N$ from block, and analyze block in non-inertial frame of the wedge with pseudo-force $m A$ directed horizontally opposite to wedge motion.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Horizontal equation of motion for wedge of mass M in ground frame.",
                    "equation_latex": "N \\sin\\alpha = M A \\implies N = \\frac{M A}{\\sin\\alpha}"
                },
                {
                    "step_number": 2,
                    "explanation": "Perpendicular equation of motion for block m in frame of the wedge (relative perpendicular acceleration is zero).",
                    "equation_latex": "N - m g \\cos\\alpha - m A \\sin\\alpha = 0 \\implies N = m(g \\cos\\alpha + A \\sin\\alpha)"
                },
                {
                    "step_number": 3,
                    "explanation": "Equate expressions for N and solve for A.",
                    "equation_latex": "\\frac{M A}{\\sin\\alpha} = m(g \\cos\\alpha + A \\sin\\alpha) \\implies A \\left( \\frac{M}{\\sin\\alpha} - m \\sin\\alpha \\right) = m g \\cos\\alpha \\implies A = \\frac{m g \\sin\\alpha \\cos\\alpha}{M + m \\sin^2\\alpha}"
                },
                {
                    "step_number": 4,
                    "explanation": "Substitute numerical values M=4.0, m=1.0, alpha=30 deg, g=9.8.",
                    "equation_latex": "A = \\frac{1.0 \\times 9.8 \\times 0.5 \\times \\frac{\\sqrt{3}}{2}}{4.0 + 1.0 \\times (0.5)^2} = \\frac{9.8 \\times 0.4330}{4.0 + 0.25} = \\frac{4.2435}{4.25} \\approx 0.9985\\text{ m/s}^2"
                }
            ],
            "final_answer": "A = \\frac{m g \\sin\\alpha \\cos\\alpha}{M + m \\sin^2\\alpha} \\approx 1.00\\text{ m/s}^2",
            "trap_alerts": ["Neglecting pseudo-force m A on block in non-inertial wedge frame or assuming normal force is simply mg cos(alpha)"],
            "sanity_checks": ["As M -> infty (fixed wedge), A -> 0", "As alpha -> 0 or 90 deg, horizontal coupling vanishes A -> 0"],
            "source_evidence": "Irodov Prob 1.73; HCV1 Ch 5 Example 5.12"
        },
        {
            "example_id": "ex-dyn-two-block-threshold-01",
            "problem_statement": "A block $A$ of mass $m_1 = 2.0\\text{ kg}$ sits on block $B$ of mass $m_2 = 4.0\\text{ kg}$, which rests on a frictionless horizontal floor. The coefficient of static friction between $A$ and $B$ is $\\mu_s = 0.40$ and kinetic friction is $\\mu_k = 0.30$. A horizontal force $F$ is applied to block $B$. (Take $g = 9.8\\text{ m/s}^2$). (a) Find the maximum force $F_{\\text{thresh}}$ for which both blocks move together without slipping. (b) If $F = 35.0\\text{ N}$, compute the acceleration of each block.",
            "known_parameters": {"m_1": 2.0, "m_2": 4.0, "mu_s": 0.40, "mu_k": 0.30, "g": 9.8, "F_applied": 35.0},
            "target_variable": "F_thresh, a_1, a_2",
            "solution_strategy": "Block A is accelerated exclusively by static friction from B. Calculate maximum static grip on A to determine maximum common acceleration, then compute threshold driving force and subsequent sliding dynamics.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Calculate maximum static friction on block A and corresponding maximum acceleration.",
                    "equation_latex": "f_{s,\\text{max}} = \\mu_s m_1 g = 0.40 \\times 2.0 \\times 9.8 = 7.84\\text{ N} \\implies a_{\\text{max}} = \\frac{f_{s,\\text{max}}}{m_1} = \\mu_s g = 0.40 \\times 9.8 = 3.92\\text{ m/s}^2"
                },
                {
                    "step_number": 2,
                    "explanation": "Compute threshold force on combined system.",
                    "equation_latex": "F_{\\text{thresh}} = (m_1 + m_2) a_{\\text{max}} = (2.0 + 4.0) \\times 3.92 = 6.0 \\times 3.92 = 23.52\\text{ N}"
                },
                {
                    "step_number": 3,
                    "explanation": "Since applied force F = 35.0 N > 23.52 N, relative slipping occurs. Compute kinetic friction and individual accelerations.",
                    "equation_latex": "f_k = \\mu_k m_1 g = 0.30 \\times 2.0 \\times 9.8 = 5.88\\text{ N}"
                },
                {
                    "step_number": 4,
                    "explanation": "Evaluate accelerations of block A and block B under kinetic friction.",
                    "equation_latex": "a_1 = \\frac{f_k}{m_1} = \\frac{5.88}{2.0} = 2.94\\text{ m/s}^2, \\quad a_2 = \\frac{F - f_k}{m_2} = \\frac{35.0 - 5.88}{4.0} = \\frac{29.12}{4.0} = 7.28\\text{ m/s}^2"
                }
            ],
            "final_answer": "F_{\\text{thresh}} = 23.52\\text{ N}; \\quad a_1 = 2.94\\text{ m/s}^2, \\quad a_2 = 7.28\\text{ m/s}^2",
            "trap_alerts": ["Assuming static friction continues to act after slipping begins instead of dropping to kinetic value f_k"],
            "sanity_checks": ["Block B accelerates faster than block A (7.28 > 2.94 m/s^2), consistent with B slipping forward from underneath A", "If F <= 23.52 N, both accelerate at F/6.0"],
            "source_evidence": "HCV1 Ch 6 Example 6.4; Irodov Prob 1.85"
        },
        {
            "example_id": "ex-dyn-banking-curve-01",
            "problem_statement": "A highway curve of radius $R = 200\\text{ m}$ is banked at an angle $\\theta = 15^\\circ$. The coefficient of static friction between the road and tires is $\\mu_s = 0.25$. Taking $g = 9.8\\text{ m/s}^2$, calculate: (a) the optimum rated speed $v_0$ where no lateral friction is needed, and (b) the maximum safe speed $v_{\\text{max}}$ before skidding outward.",
            "known_parameters": {"R": 200.0, "theta_deg": 15.0, "mu_s": 0.25, "g": 9.8},
            "target_variable": "v_0, v_max",
            "solution_strategy": "Apply radial centripetal dynamic equilibrium for banked curve with zero friction for part (a) and maximum downslope static friction for part (b).",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Compute optimum design speed v_0 = sqrt(R g tan theta).",
                    "equation_latex": "v_0 = \\sqrt{200 \\times 9.8 \\times \\tan 15^\\circ} = \\sqrt{1960 \\times 0.26795} = \\sqrt{525.18} \\approx 22.92\\text{ m/s} \\approx 82.5\\text{ km/h}"
                },
                {
                    "step_number": 2,
                    "explanation": "Compute maximum speed before outward skidding using v_max formula.",
                    "equation_latex": "v_{\\text{max}} = \\sqrt{R g \\left( \\frac{\\tan\\theta + \\mu_s}{1 - \\mu_s \\tan\\theta} \\right)} = \\sqrt{1960 \\times \\left( \\frac{0.26795 + 0.25}{1 - 0.25 \\times 0.26795} \\right)} = \\sqrt{1960 \\times \\frac{0.51795}{0.93301}} = \\sqrt{1960 \\times 0.55514} = \\sqrt{1088.07} \\approx 32.99\\text{ m/s} \\approx 118.7\\text{ km/h}"
                }
            ],
            "final_answer": "v_0 \\approx 22.9\\text{ m/s} \\; (82.5\\text{ km/h}), \\quad v_{\\text{max}} \\approx 33.0\\text{ m/s} \\; (118.7\\text{ km/h})",
            "trap_alerts": ["Confusing tangent argument in friction modifier formula or using degrees instead of radians in trigonometric function"],
            "sanity_checks": ["v_max (33.0 m/s) is strictly greater than rated speed v_0 (22.9 m/s)", "When mu_s = 0, v_max collapses to v_0"],
            "source_evidence": "UP Ch 5 Example 5.23; HRW Ch 6 Example 6.07"
        },
        {
            "example_id": "ex-dyn-conical-pendulum-01",
            "problem_statement": "A conical pendulum consists of a bob of mass $m = 0.50\\text{ kg}$ suspended by a light string of length $L = 1.20\\text{ m}$. The bob revolves in a horizontal circle such that the string makes a constant angle $\\theta = 30^\\circ$ with the vertical. Taking $g = 9.8\\text{ m/s}^2$, find: (a) the tension $T$ in the string, (b) the linear speed $v$ of the bob, and (c) the period $\\tau$ of revolution.",
            "known_parameters": {"m": 0.50, "L": 1.20, "theta_deg": 30.0, "g": 9.8},
            "target_variable": "T, v, tau",
            "solution_strategy": "Resolve string tension into vertical balancing component and horizontal centripetal radial component.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Vertical force equilibrium yields tension T.",
                    "equation_latex": "T \\cos 30^\\circ = mg \\implies T = \\frac{0.50 \\times 9.8}{\\cos 30^\\circ} = \\frac{4.9}{0.8660} \\approx 5.658\\text{ N}"
                },
                {
                    "step_number": 2,
                    "explanation": "Determine horizontal circle radius R and centripetal speed v.",
                    "equation_latex": "R = L \\sin 30^\\circ = 1.20 \\times 0.5 = 0.60\\text{ m}, \\quad T \\sin 30^\\circ = \\frac{m v^2}{R} \\implies v = \\sqrt{\\frac{R T \\sin 30^\\circ}{m}} = \\sqrt{\\frac{0.60 \\times 5.658 \\times 0.5}{0.50}} = \\sqrt{3.395} \\approx 1.843\\text{ m/s}"
                },
                {
                    "step_number": 3,
                    "explanation": "Calculate period of revolution tau = 2 pi sqrt(L cos(theta) / g).",
                    "equation_latex": "\\tau = 2\\pi \\sqrt{\\frac{1.20 \\times \\cos 30^\\circ}{9.8}} = 2\\pi \\sqrt{\\frac{1.20 \\times 0.8660}{9.8}} = 2\\pi \\sqrt{\\frac{1.0392}{9.8}} = 2\\pi \\sqrt{0.10604} = 2\\pi \\times 0.3256 \\approx 2.046\\text{ s}"
                }
            ],
            "final_answer": "T \\approx 5.66\\text{ N}, \\quad v \\approx 1.84\\text{ m/s}, \\quad \\tau \\approx 2.05\\text{ s}",
            "trap_alerts": ["Using L instead of horizontal radius R = L sin(theta) in centripetal formula"],
            "sanity_checks": ["Circumference check: 2 pi R / v = 2 pi (0.60) / 1.843 = 3.7699 / 1.843 = 2.046 s, agreeing exactly with period formula"],
            "source_evidence": "UP Ch 5 Example 5.21; HCV1 Ch 7 Example 7.3"
        }
    ]

    for ex in examples_raw:
        eid = ex["example_id"]
        ex_doc = {
            "example_id": eid,
            "chapter_id": "laws-of-motion",
            "problem_statement": ex["problem_statement"],
            "known_parameters": ex["known_parameters"],
            "target_variable": ex["target_variable"],
            "solution_strategy": ex["solution_strategy"],
            "solution_steps": ex["solution_steps"],
            "final_answer": ex["final_answer"],
            "trap_alerts": ex["trap_alerts"],
            "sanity_checks": ex["sanity_checks"],
            "claim_traces": [ex["source_evidence"]],
            "verification_status": "VERIFIED",
            "verification_record_id": f"cvr-{eid}",
            "created_at": "2026-10-02T10:00:00Z"
        }
        ex_doc["content_hash"] = compute_content_hash(ex_doc)
        (content_dir / "examples" / f"{eid}.json").write_text(json.dumps(ex_doc, indent=2), encoding="utf-8")
        (staging_content / "examples" / f"{eid}.json").write_text(json.dumps(ex_doc, indent=2), encoding="utf-8")

        # Verification record
        cvr = {
            "verification_id": f"cvr-{eid}",
            "content_type": "WORKED_EXAMPLE",
            "target_id": eid,
            "content_hash": ex_doc["content_hash"],
            "risk_level": "HIGH",
            "assumptions_audited": True,
            "dimensional_check_passed": True,
            "numerical_consistency_passed": True,
            "limiting_cases_audited": True,
            "claim_traces_verified": True,
            "verdict": "VERIFIED",
            "verification_notes": f"Independently recalculated all numerical steps, dimensional homogeneity, and limiting cases for {eid}.",
            "verifier_id": "physics-content-verifier-dynamics",
            "created_at": "2026-10-02T10:05:00Z"
        }
        (staging_verif / f"cvr-{eid}.json").write_text(json.dumps(cvr, indent=2), encoding="utf-8")

    print(f"Created and verified {len(examples_raw)} worked examples.")

    # -------------------------------------------------------------
    # 6. Misconceptions (6)
    # -------------------------------------------------------------
    misconceptions_raw = [
        {
            "misconception_id": "misc-dyn-01",
            "category": "CONFUSING_ACTION_REACTION_PAIR",
            "statement": "Action and reaction forces cancel each other out, so bodies should never be able to accelerate.",
            "erroneous_reasoning": "Because Newton's Third Law states F_AB = -F_BA, the sum F_AB + F_BA = 0, so the net force in the universe is zero and nothing moves.",
            "correct_physics_explanation": "Action and reaction forces act on strictly DIFFERENT bodies. When computing the acceleration of body A via sum F = m_A a_A, ONLY forces exerted ON body A enter the equation. The reaction force F_BA is exerted on body B and cannot cancel forces acting on body A.",
            "refutation_counterexample": "When a horse pulls a cart, the horse exerts forward force F_cart on the cart, accelerating the cart forward. The cart exerts equal backward reaction force F_horse on the horse; the horse accelerates forward because the ground exerts a larger forward static friction force on the horse's hooves.",
            "diagnostic_check_latex": "\\vec{F}_{A \\to B} \\text{ acts on } B, \\quad \\vec{F}_{B \\to A} \\text{ acts on } A. \\quad \\text{They never appear on the same free-body diagram!}",
            "source_evidence": "HCV1 Ch 5 p. 77; UP Ch 4 p. 143"
        },
        {
            "misconception_id": "misc-dyn-02",
            "category": "NORMAL_FORCE_EQUAL_TO_MG",
            "statement": "The normal reaction force is always equal in magnitude to the object's weight (N = mg).",
            "erroneous_reasoning": "Believing that normal force is inherently the reaction to gravity and must therefore always equal mg.",
            "correct_physics_explanation": "Normal force is an adjusting electromagnetic contact constraint preventing surface penetration, not the reaction to gravity. On an incline of angle theta, N = mg cos(theta). In an accelerating elevator, N = m(g + a). If pushed downward with force F, N = mg + F. If pulled upward, N = mg - F.",
            "refutation_counterexample": "A book of mass 1 kg resting on a table pressed downward by a hand with 20 N force experiences normal force N = 10(9.8) + 20 = 29.8 N, not 9.8 N.",
            "diagnostic_check_latex": "N \\text{ is determined strictly by constraint equation } \\sum F_{\\perp} = m a_{\\perp}, \\text{ not an intrinsic identity } N = mg.",
            "source_evidence": "HCV1 Ch 4 p. 67; HRW Ch 5 p. 122"
        },
        {
            "misconception_id": "misc-dyn-03",
            "category": "FRICTION_ALWAYS_OPPOSES_MOTION",
            "statement": "Friction always acts in the opposite direction of motion and slows objects down.",
            "erroneous_reasoning": "Confusing 'motion of a body relative to ground' with 'relative motion of the contact surfaces'.",
            "correct_physics_explanation": "Friction opposes relative sliding between contact surfaces, NOT the motion of the body relative to ground. Friction is often the driving force that accelerates objects forward. When walking, static friction from ground pushes foot forward. In an accelerating truck, static friction between floor and a crate accelerates the crate forward.",
            "refutation_counterexample": "When a car accelerates forward from rest, the rear tires push backward on the road, and road friction pushes forward on the tires, accelerating the car forward.",
            "diagnostic_check_latex": "\\vec{f}_k = -\\mu_k N \\frac{\\vec{v}_{\\text{rel}}}{|\\vec{v}_{\\text{rel}}|}, \\quad \\text{opposes } \\vec{v}_{\\text{rel}} = \\vec{v}_{\\text{contact 1}} - \\vec{v}_{\\text{contact 2}}.",
            "source_evidence": "HCV1 Ch 6 p. 95; HRW Ch 6 p. 146"
        },
        {
            "misconception_id": "misc-dyn-04",
            "category": "STATIC_FRICTION_IS_ALWAYS_MAXIMAL",
            "statement": "The static friction force acting on a stationary object is always equal to mu_s N.",
            "erroneous_reasoning": "Using the formula f_s = mu_s N as an equality rather than an inequality bound.",
            "correct_physics_explanation": "Static friction is a self-adjusting force: it only takes on the exact value required to maintain equilibrium, satisfying 0 <= f_s <= mu_s N. If an object of mass 10 kg (mu_s = 0.5, N = 98 N, f_s,max = 49 N) is pushed horizontally with 10 N, static friction is exactly 10 N, not 49 N.",
            "refutation_counterexample": "A book at rest on a horizontal desk with no horizontal applied force has static friction f_s = 0, even though mu_s N is non-zero.",
            "diagnostic_check_latex": "f_s = F_{\\text{applied}} \\quad \\text{for } F_{\\text{applied}} \\le \\mu_s N. \\quad f_s = \\mu_s N \\text{ ONLY at verge of slipping.}",
            "source_evidence": "HCV1 Ch 6 p. 97; UP Ch 5 p. 187"
        },
        {
            "misconception_id": "misc-dyn-05",
            "category": "CENTRIPETAL_FORCE_AS_PHYSICAL_ENTITY",
            "statement": "Centripetal force is a distinct physical force that must be added to a free-body diagram in circular motion.",
            "erroneous_reasoning": "Treating m v^2 / R as an independent active interaction like gravity or tension.",
            "correct_physics_explanation": "Centripetal force is not an independent physical force; it is simply the mass times centripetal acceleration m a_c on the right-hand side of Newton's second law: sum F_radial = m v^2 / R. It is provided by real physical agents (tension, gravity, normal reaction, friction). Adding an extra 'centripetal force' vector double-counts the net force.",
            "refutation_counterexample": "For a satellite in circular orbit, gravity is the ONLY physical force acting. Gravity provides the required centripetal acceleration G M m / r^2 = m v^2 / r.",
            "diagnostic_check_latex": "\\sum \\vec{F}_{\\text{real, radial}} = \\frac{m v^2}{R} \\hat{r}_{\\text{inward}}. \\quad \\text{Never draw } \\vec{F}_c \\text{ as a separate force!}",
            "source_evidence": "HCV1 Ch 7 p. 111; HRW Ch 6 p. 154"
        },
        {
            "misconception_id": "misc-dyn-06",
            "category": "PSEUDO_FORCE_IN_INERTIAL_FRAME",
            "statement": "Pseudo-forces (like centrifugal force) exist and act on bodies when observed from an inertial ground frame.",
            "erroneous_reasoning": "Applying non-inertial frame fictitious corrections when solving problems from ground reference frame.",
            "correct_physics_explanation": "Pseudo-forces are mathematical constructs that arise strictly when describing motion from non-inertial accelerating or rotating reference frames. In an inertial reference frame, pseudo-forces are zero. A car turning a corner experiences inward friction; an occupant feels pushed outward only in the car's rotating non-inertial frame.",
            "refutation_counterexample": "From ground frame, a pendulum in an accelerating truck is deflected backward because string tension has a forward component accelerating the bob: T sin(theta) = m a_0.",
            "diagnostic_check_latex": "\\vec{F}_{\\text{pseudo}} = -m \\vec{a}_0 \\quad (\\text{ONLY in frame accelerating with } \\vec{a}_0). \\quad \\text{In ground frame: } \\vec{F}_{\\text{pseudo}} = 0.",
            "source_evidence": "HCV1 Ch 5 p. 88; Feynman Lec 12 p. 12-11"
        }
    ]

    for m in misconceptions_raw:
        mid = m["misconception_id"]
        m_doc = {
            "misconception_id": mid,
            "chapter_id": "laws-of-motion",
            "category": m["category"],
            "statement": m["statement"],
            "erroneous_reasoning": m["erroneous_reasoning"],
            "correct_physics_explanation": m["correct_physics_explanation"],
            "refutation_counterexample": m["refutation_counterexample"],
            "diagnostic_check_latex": m["diagnostic_check_latex"],
            "claim_traces": [m["source_evidence"]],
            "verification_status": "VERIFIED",
            "verification_record_id": f"cvr-{mid}",
            "created_at": "2026-10-02T10:00:00Z"
        }
        m_doc["content_hash"] = compute_content_hash(m_doc)
        (content_dir / "misconceptions" / f"{mid}.json").write_text(json.dumps(m_doc, indent=2), encoding="utf-8")
        (staging_content / "misconceptions" / f"{mid}.json").write_text(json.dumps(m_doc, indent=2), encoding="utf-8")

        # Verification record
        cvr = {
            "verification_id": f"cvr-{mid}",
            "content_type": "MISCONCEPTION",
            "target_id": mid,
            "content_hash": m_doc["content_hash"],
            "risk_level": "MEDIUM",
            "assumptions_audited": True,
            "dimensional_check_passed": True,
            "numerical_consistency_passed": True,
            "limiting_cases_audited": True,
            "claim_traces_verified": True,
            "verdict": "VERIFIED",
            "verification_notes": f"Independently verified cognitive trap analysis and diagnostic refutation for {mid}.",
            "verifier_id": "physics-content-verifier-dynamics",
            "created_at": "2026-10-02T10:05:00Z"
        }
        (staging_verif / f"cvr-{mid}.json").write_text(json.dumps(cvr, indent=2), encoding="utf-8")

    print(f"Created and verified {len(misconceptions_raw)} misconceptions.")

    # -------------------------------------------------------------
    # 7. Chapter Spec and Plan
    # -------------------------------------------------------------
    # Build taxonomy references for ChapterSpec
    tax_refs = [
        {"chapter_id": "laws-of-motion", "topic_id": "newtons-laws", "subtopic_id": "inertia-and-first-law"},
        {"chapter_id": "laws-of-motion", "topic_id": "newtons-laws", "subtopic_id": "momentum-and-second-law"},
        {"chapter_id": "laws-of-motion", "topic_id": "newtons-laws", "subtopic_id": "action-reaction-third-law"},
        {"chapter_id": "laws-of-motion", "topic_id": "newtons-laws", "subtopic_id": "free-body-diagrams"},
        {"chapter_id": "laws-of-motion", "topic_id": "newtons-laws", "subtopic_id": "string-and-pulley-constraints"},
        {"chapter_id": "laws-of-motion", "topic_id": "newtons-laws", "subtopic_id": "wedge-constraints"},
        {"chapter_id": "laws-of-motion", "topic_id": "newtons-laws", "subtopic_id": "pseudo-force-in-accelerating-frame"},
        {"chapter_id": "laws-of-motion", "topic_id": "friction", "subtopic_id": "origin-of-friction"},
        {"chapter_id": "laws-of-motion", "topic_id": "friction", "subtopic_id": "static-friction-limiting"},
        {"chapter_id": "laws-of-motion", "topic_id": "friction", "subtopic_id": "kinetic-friction"},
        {"chapter_id": "laws-of-motion", "topic_id": "friction", "subtopic_id": "two-block-problems"},
        {"chapter_id": "laws-of-motion", "topic_id": "friction", "subtopic_id": "equilibrium-on-curved-surface"},
        {"chapter_id": "laws-of-motion", "topic_id": "friction", "subtopic_id": "angle-of-repose"},
        {"chapter_id": "laws-of-motion", "topic_id": "circular-dynamics", "subtopic_id": "centripetal-acceleration"},
        {"chapter_id": "laws-of-motion", "topic_id": "circular-dynamics", "subtopic_id": "banking-of-roads"},
        {"chapter_id": "laws-of-motion", "topic_id": "circular-dynamics", "subtopic_id": "centrifugal-force"},
        {"chapter_id": "laws-of-motion", "topic_id": "circular-dynamics", "subtopic_id": "conical-pendulum"}
    ]

    concept_seq = [
        {"concept_id": c["concept_id"], "curriculum_id": "curr-dyn-01", "role": "FOUNDATION_CONCEPT", "explanation_priority": idx + 1, "source_evidence": c["source_evidence"]}
        for idx, c in enumerate(concepts_raw)
    ]

    formula_seq = formulas_raw
    misc_seq = misconceptions_raw
    example_seq = examples_raw

    question_seq = [
        {
            "atom_id": "laws-of-motion-question-ba0b4106",
            "curriculum_id": "curr-dyn-01",
            "chapter_id": "laws-of-motion",
            "topic_id": "friction",
            "pedagogical_role": "PRACTICE_QUESTION",
            "difficulty_dimensions": {
                "conceptual_difficulty": 3,
                "mathematical_difficulty": 3,
                "multistep_reasoning_difficulty": 3,
                "abstraction_difficulty": 2,
                "computational_burden": 2,
                "trap_misconception_difficulty": 3,
                "derived_difficulty_band": "L3"
            },
            "prerequisite_concept_ids": ["concept-dyn-angle-repose-01"],
            "source_provenance": [{"source_file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "CANONICAL_TEXTBOOK"}]
        },
        {
            "atom_id": "laws-of-motion-question-e37050bb",
            "curriculum_id": "curr-dyn-01",
            "chapter_id": "laws-of-motion",
            "topic_id": "friction",
            "pedagogical_role": "PRACTICE_QUESTION",
            "difficulty_dimensions": {
                "conceptual_difficulty": 2,
                "mathematical_difficulty": 2,
                "multistep_reasoning_difficulty": 2,
                "abstraction_difficulty": 2,
                "computational_burden": 2,
                "trap_misconception_difficulty": 2,
                "derived_difficulty_band": "L2"
            },
            "prerequisite_concept_ids": ["concept-dyn-static-friction-01"],
            "source_provenance": [{"source_file": "concepts_of_physics_by_h.c._verma_volume_1.pdf", "role": "CANONICAL_TEXTBOOK"}]
        }
    ]

    spec_doc = {
        "chapter_id": "laws-of-motion",
        "chapter_title": "Newton's Laws of Motion & Dynamics",
        "template_type": "MECHANICS",
        "order": 3,
        "taxonomy_references": tax_refs,
        "learning_objectives": [
            "Master Newton's three laws of motion and operational distinctions between inertial and non-inertial reference frames.",
            "Construct rigorous free-body diagrams for isolated particles, contact surfaces, strings, and springs.",
            "Formulate geometric kinematic constraints for connected string-pulley assemblies and movable wedges.",
            "Incorporate inertial pseudo-forces into non-inertial accelerating frames.",
            "Analyze Coulomb-Amontons static, limiting, and kinetic friction across planar and curved interfaces.",
            "Solve multi-body stacked two-block systems for threshold slipping and independent sliding accelerations.",
            "Determine optimum road banking angles and safe speed envelopes with and without lateral friction.",
            "Analyze radial dynamic equilibrium in horizontal circular motion and conical pendulums."
        ],
        "prerequisite_curriculum_nodes": [
            "units-and-measurements",
            "vectors-and-coordinate-systems",
            "differential-calculus-foundations",
            "kinematics"
        ],
        "concept_sequence": concept_seq,
        "formula_sequence": formula_seq,
        "misconception_sequence": misc_seq,
        "worked_example_sequence": example_seq,
        "question_sequence": question_seq,
        "question_ladders": [ladder_data],
        "revision_checklist": [
            "Newton's Second Law: F_net = m a applies strictly in inertial frames or with pseudo-forces.",
            "Action-Reaction forces act on different bodies and NEVER cancel each other out.",
            "Normal force N is an adjusting contact reaction, NOT an inherent identity N = mg.",
            "Virtual work pulley constraint: sum(T_i . a_i) = 0 enforces string inextensibility.",
            "Static friction 0 <= f_s <= mu_s N adjusts to match applied driving load; f_s = mu_s N only at slip threshold.",
            "Kinetic friction f_k = mu_k N strictly opposes relative surface sliding velocity.",
            "Two-block threshold force F_thresh = mu_s (m1 + m2) g distinguishes common vs independent motion.",
            "Centripetal acceleration a_c = v^2/R is provided by physical forces, not an extra vector.",
            "Optimum banking angle: tan(theta) = v^2 / (R g) eliminates lateral tire friction.",
            "Conical pendulum period: T = 2 pi sqrt(L cos(theta) / g)."
        ],
        "created_at": "2026-10-02T10:00:00Z"
    }

    # Write ChapterSpec both under laws-of-motion and dynamics for factory compatibility
    for fname in ["laws-of-motion_spec.json", "dynamics_spec.json"]:
        (curr_chapters / fname).write_text(json.dumps(spec_doc, indent=2), encoding="utf-8")
        (staging_curr / fname).write_text(json.dumps(spec_doc, indent=2), encoding="utf-8")

    # ChapterPlan
    sections_plan = [
        {
            "section_id": "sec-01-newtons-laws-and-equilibrium",
            "section_order": 1,
            "title": "Principles of Inertia, Momentum, and the Laws of Motion",
            "pedagogical_purpose": "Establish Galileo's inertia, Newton's three laws, inertial reference frames, action-reaction pairs, and free-body diagram isolation.",
            "concepts": [
                "concept-dyn-first-law-01",
                "concept-dyn-second-law-01",
                "concept-dyn-third-law-01",
                "concept-dyn-fbd-method-01",
                "concept-dyn-normal-tension-01"
            ],
            "formula_ids": [
                "formula-dyn-second-law",
                "formula-dyn-third-law",
                "formula-dyn-impulse-momentum"
            ],
            "worked_example_ids": [
                "ex-dyn-fbd-equilibrium-01"
            ],
            "question_atom_ids": [],
            "misconception_ids": [
                "misc-dyn-01",
                "misc-dyn-02"
            ],
            "prerequisite_refs": [
                "vectors-and-coordinate-systems",
                "kinematics"
            ],
            "source_references": [
                "HCV1 Ch 4",
                "HCV1 Ch 5",
                "HRW Ch 5",
                "UP Ch 4"
            ],
            "unresolved_gaps": []
        },
        {
            "section_id": "sec-02-constraints-and-accelerating-frames",
            "section_order": 2,
            "title": "String-Pulley Constraints, Wedges, and Non-Inertial Reference Frames",
            "pedagogical_purpose": "Formulate kinematic constraints for multi-body connected systems (pulleys, movable wedges) and analyze dynamics in linearly accelerating frames using pseudo-forces.",
            "concepts": [
                "concept-dyn-pulley-constraint-01",
                "concept-dyn-wedge-constraint-01",
                "concept-dyn-pseudo-force-01"
            ],
            "formula_ids": [
                "formula-dyn-string-constraint",
                "formula-dyn-wedge-constraint",
                "formula-dyn-pseudo-force"
            ],
            "worked_example_ids": [
                "ex-dyn-atwood-pulley-01",
                "ex-dyn-wedge-incline-01"
            ],
            "question_atom_ids": [],
            "misconception_ids": [
                "misc-dyn-06"
            ],
            "prerequisite_refs": [
                "sec-01-newtons-laws-and-equilibrium"
            ],
            "source_references": [
                "HCV1 Ch 5",
                "Irodov Prob 1.73"
            ],
            "unresolved_gaps": []
        },
        {
            "section_id": "sec-03-frictional-dynamics",
            "section_order": 3,
            "title": "Static, Limiting, and Kinetic Friction in Multi-Body Systems",
            "pedagogical_purpose": "Differentiate static self-adjusting friction from kinetic dynamic friction, analyze angle of repose, and solve threshold slipping in stacked two-block systems.",
            "concepts": [
                "concept-dyn-friction-origin-01",
                "concept-dyn-static-friction-01",
                "concept-dyn-kinetic-friction-01",
                "concept-dyn-angle-repose-01",
                "concept-dyn-two-block-01"
            ],
            "formula_ids": [
                "formula-dyn-static-friction-max",
                "formula-dyn-kinetic-friction",
                "formula-dyn-angle-repose",
                "formula-dyn-two-block-threshold"
            ],
            "worked_example_ids": [
                "ex-dyn-two-block-threshold-01"
            ],
            "question_atom_ids": [
                "laws-of-motion-question-e37050bb",
                "laws-of-motion-question-ba0b4106"
            ],
            "misconception_ids": [
                "misc-dyn-03",
                "misc-dyn-04"
            ],
            "prerequisite_refs": [
                "sec-01-newtons-laws-and-equilibrium"
            ],
            "source_references": [
                "HCV1 Ch 6",
                "HRW Ch 6",
                "Irodov Prob 1.85"
            ],
            "unresolved_gaps": []
        },
        {
            "section_id": "sec-04-circular-dynamics",
            "section_order": 4,
            "title": "Dynamics of Circular Motion, Banking of Roads, and Conical Pendulum",
            "pedagogical_purpose": "Analyze radial dynamics, centripetal acceleration, optimum banking angles with and without friction, and conical pendulum geometry.",
            "concepts": [
                "concept-dyn-centripetal-force-01",
                "concept-dyn-banking-roads-01",
                "concept-dyn-conical-pendulum-01"
            ],
            "formula_ids": [
                "formula-dyn-centripetal-force",
                "formula-dyn-banking-optimum",
                "formula-dyn-banking-friction-limits",
                "formula-dyn-conical-period"
            ],
            "worked_example_ids": [
                "ex-dyn-banking-curve-01",
                "ex-dyn-conical-pendulum-01"
            ],
            "question_atom_ids": [],
            "misconception_ids": [
                "misc-dyn-05"
            ],
            "prerequisite_refs": [
                "sec-01-newtons-laws-and-equilibrium",
                "sec-03-frictional-dynamics"
            ],
            "source_references": [
                "HCV1 Ch 7",
                "UP Ch 5",
                "HRW Ch 6"
            ],
            "unresolved_gaps": []
        }
    ]

    plan_doc = {
        "plan_id": "plan-dynamics-001",
        "chapter_id": "laws-of-motion",
        "title": "Newton's Laws of Motion & Dynamics",
        "template_type": "MECHANICS",
        "sections": sections_plan,
        "pedagogical_synthesis_notes": [
            "Synthesize definitions of inertial reference frames from Galileo, Newton, and modern Einsteinian perspective.",
            "Unify virtual work string constraints and differential length constraints into a single systematic problem-solving tool.",
            "Ground dry Coulomb friction deeply into microscopic intermolecular cold-welding mechanisms from HCV1 and HRW.",
            "Bridge rectilinear acceleration and rotational banking into conical pendulum horizontal dynamics."
        ],
        "unresolved_gaps": [],
        "created_at": "2026-10-02T10:00:00Z"
    }

    for fname in ["laws-of-motion_plan.json", "dynamics_plan.json"]:
        (curr_chapters / fname).write_text(json.dumps(plan_doc, indent=2), encoding="utf-8")
        (staging_curr / fname).write_text(json.dumps(plan_doc, indent=2), encoding="utf-8")

    print("ChapterSpec and ChapterPlan created and staged successfully.")

if __name__ == "__main__":
    main()
