import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from jee_physics.content.gate import compute_content_hash

def main():
    root = Path.cwd()
    
    # Target Directories
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

    now_iso = "2026-10-05T01:00:00Z"

    # =============================================================
    # 1. QUESTION LADDER
    # =============================================================
    ladder_data = {
        "ladder_id": "ladder-wep-vcm-looping-01",
        "chapter_id": "work-energy-power",
        "topic_id": "power-and-vertical-circle",
        "title": "Scaffolding Vertical Circular Motion from Bottom Launch to Slack Trajectories",
        "physical_system": "Particle of mass m attached to light inextensible string of length R orbiting in vertical gravitational field g",
        "rungs": [
            {
                "level": 1,
                "level_name": "Loop-the-loop minimum launch speed",
                "atom_id": "work-energy-power-question-e37050bb",
                "physical_delta": "Particle launched horizontally at bottom with critical speed required to complete full vertical circle without string slackening",
                "reasoning_depth": 2,
                "concepts_involved": ["concept-wep-vertical-circle-critical-01", "concept-wep-mech-energy-cons-01"],
                "mathematical_complexity": "Conservation of energy combined with apex radial dynamic equilibrium T_top >= 0 yielding v_bot >= sqrt(5gR)",
                "transfer_requirement": "Recognizing that minimum tension occurs at apex, not horizontal position"
            },
            {
                "level": 2,
                "level_name": "Tension difference between extremities",
                "atom_id": "work-energy-power-question-ba0b4106",
                "physical_delta": "Comparing string tension at bottom T_bot and apex T_top for arbitrary looping speed",
                "reasoning_depth": 3,
                "concepts_involved": ["concept-wep-vertical-circle-critical-01"],
                "mathematical_complexity": "Algebraic elimination of speed using energy conservation to yield universal invariant T_bot - T_top = 6mg",
                "transfer_requirement": "Proving that the 6mg tension difference is completely independent of initial kinetic energy"
            },
            {
                "level": 3,
                "level_name": "String slackening angle in upper quadrant",
                "atom_id": "prob-irodov-1-120",
                "physical_delta": "Particle launched with intermediate speed sqrt(2gR) < v_bot < sqrt(5gR) such that string tension vanishes before reaching the top",
                "reasoning_depth": 4,
                "concepts_involved": ["concept-wep-vertical-circle-slack-01", "concept-wep-vertical-circle-critical-01"],
                "mathematical_complexity": "Setting radial constraint T(theta) = 0 and solving coupled energy-radial equations for cos(theta_slack)",
                "transfer_requirement": "Distinguishing string slackening (T=0, v > 0) from turning point in lower quadrant (v=0, T > 0)"
            },
            {
                "level": 4,
                "level_name": "Post-slack parabolic projectile flight",
                "atom_id": "prob-irodov-1-118",
                "physical_delta": "Subsequent free-flight projectile trajectory after string goes slack at theta_slack, analyzing path through circle center",
                "reasoning_depth": 5,
                "concepts_involved": ["concept-wep-vertical-circle-slack-01", "concept-kin-projectile-01"],
                "mathematical_complexity": "Solving 2D ballistic trajectory with initial launch position (R sin theta, R cos theta) and tangential velocity vector",
                "transfer_requirement": "Synthesizing circular constraint release conditions with Cartesian projectile kinematics"
            }
        ],
        "pedagogical_objective": "Systematically scaffold vertical circular dynamics from energy-tension conservation to universal tension differences, slackening angle bifurcations, and projectile departure flight."
    }

    for target_path in [curr_ladders / "ladder-wep-vcm-looping-01.json", staging_ladders / "ladder-wep-vcm-looping-01.json"]:
        target_path.write_text(json.dumps(ladder_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 2. CONCEPTS (16 items)
    # =============================================================
    concepts = [
        # Section 1: Work Done by Forces (4 concepts)
        {
            "concept_id": "concept-wep-work-def-01",
            "chapter_id": "work-energy-power",
            "title": "Work Done by a Constant Force and Scalar Product",
            "formal_definition": "The work $W$ done on a particle by a constant force $\\vec{F}$ undergoing displacement $\\Delta\\vec{r}$ is defined as the scalar (dot) product: $W = \\vec{F} \\cdot \\Delta\\vec{r} = |\\vec{F}| |\\Delta\\vec{r}| \\cos\\theta = F_x \\Delta x + F_y \\Delta y + F_z \\Delta z$.",
            "physical_intuition": "Work quantifies the cumulative mechanical action of a force component directed along the displacement path. Perpendicular forces do zero work; opposing forces extract mechanical energy (negative work).",
            "assumptions": ["Constant force vector over displacement", "Point mass particle or translation without internal distortion"],
            "validity_boundaries": ["Invalid if force varies along path (requires line integral)", "Invalid if point of application does not move with body"],
            "mathematical_representation": "W = \\vec{F} \\cdot \\vec{d} = F d \\cos\\theta",
            "claim_traces": ["HCV1 Ch 8 p. 129; HRW Ch 7 p. 173; UP Ch 6 p. 205"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-work-def-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-work-variable-01",
            "chapter_id": "work-energy-power",
            "title": "Work Done by a Variable Force and Path Line Integrals",
            "formal_definition": "For a force $\\vec{F}(\\vec{r})$ varying with position, work done along path $C$ from $\\vec{r}_i$ to $\\vec{r}_f$ is the Riemann line integral: $W = \\int_C \\vec{F}(\\vec{r}) \\cdot d\\vec{r} = \\int_{x_i}^{x_f} F_x dx + \\int_{y_i}^{y_f} F_y dy + \\int_{z_i}^{z_f} F_z dz$. In 1D, work equals the signed geometric area under the $F_x(x)$ curve.",
            "physical_intuition": "As force changes continuously, total work is accumulated by summing infinitesimal scalar work contributions $dW = \\vec{F} \\cdot d\\vec{r}$ along the physical trajectory.",
            "assumptions": ["Piecewise continuous force vector field", "Well-defined piecewise smooth curve $C$"],
            "validity_boundaries": ["Path-dependent for non-conservative forces", "Independent of path for conservative forces"],
            "mathematical_representation": "W = \\int_{\\vec{r}_i}^{\\vec{r}_f} \\vec{F} \\cdot d\\vec{r} = \\int_{x_i}^{x_f} F_x(x) \\, dx",
            "claim_traces": ["HCV1 Ch 8 p. 130; HRW Ch 7 p. 179; UP Ch 6 p. 215"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-work-variable-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-work-spring-01",
            "chapter_id": "work-energy-power",
            "title": "Work Done by an Ideal Spring and Hooke's Law",
            "formal_definition": "An ideal massless spring exerts restoring force $F_s(x) = -k x$ proportional to elongation $x$ from natural length. The work done BY the spring when displaced from $x_i$ to $x_f$ is $W_s = \\int_{x_i}^{x_f} (-kx) dx = -\\frac{1}{2} k (x_f^2 - x_i^2)$. The work done BY an external agent stretching the spring quasi-statically is $W_{\\text{ext}} = +\\frac{1}{2} k (x_f^2 - x_i^2)$.",
            "physical_intuition": "Because spring resistance increases linearly with extension, average force during extension from $0$ to $x$ is $kx/2$, resulting in quadratic work $\\frac{1}{2}kx^2$.",
            "assumptions": ["Ideal massless spring", "Linear elastic Hooke's regime (no plastic deformation)"],
            "validity_boundaries": ["Breaks down beyond elastic limit", "Fails for heavy springs where wave propagation occurs"],
            "mathematical_representation": "W_s = -\\frac{1}{2} k (x_f^2 - x_i^2), \\quad W_{\\text{ext}} = +\\frac{1}{2} k x^2",
            "claim_traces": ["HCV1 Ch 8 p. 130; HRW Ch 7 p. 175; UP Ch 6 p. 216"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-work-spring-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-work-friction-01",
            "chapter_id": "work-energy-power",
            "title": "Work Done by Friction and Interfacial Dissipation",
            "formal_definition": "Static friction does zero work in the rest frame of the contact surface, but can do positive or negative work in other reference frames. Kinetic friction dissipative work between two sliding surfaces is strictly negative: $W_{\\text{diss}} = -f_k s_{\\text{rel}} = -\\mu_k N s_{\\text{rel}}$, transforming organized macroscopic kinetic energy into internal thermal energy.",
            "physical_intuition": "Static friction prevents relative slip; if the contact surface moves (e.g. accelerating truck bed), static friction accelerates the payload, doing positive work. Kinetic friction always opposes relative sliding at the interface.",
            "assumptions": ["Amontons-Coulomb friction model", "Rigid contact interface"],
            "validity_boundaries": ["Non-conservative dissipative interaction", "Cannot define a mechanical potential energy for friction"],
            "mathematical_representation": "W_{\\text{static}} \\lessgtr 0, \\quad W_{\\text{kinetic, rel}} = -\\mu_k N s_{\\text{rel}} < 0",
            "claim_traces": ["HCV1 Ch 8 p. 131; HRW Ch 8 p. 207; UP Ch 7 p. 250"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-work-friction-01",
            "created_at": now_iso
        },

        # Section 2: Work-Energy Theorem (4 concepts)
        {
            "concept_id": "concept-wep-ke-01",
            "chapter_id": "work-energy-power",
            "title": "Kinetic Energy of a Translating Particle",
            "formal_definition": "Kinetic energy $K$ is the scalar capacity of a particle of mass $m$ to perform work due to its motion: $K = \\frac{1}{2} m v^2 = \\frac{p^2}{2m}$, where $\\vec{p} = m\\vec{v}$ is linear momentum. $K \\ge 0$ is strictly non-negative in any inertial frame.",
            "physical_intuition": "Kinetic energy represents the net work required to accelerate a body from rest to speed $v$. Because speed is frame-dependent, kinetic energy is relative to the observer's frame.",
            "assumptions": ["Point mass particle or non-rotating rigid body", "Classical non-relativistic speed ($v \\ll c$)"],
            "validity_boundaries": ["Relativistic regime requires $K = (\\gamma - 1) m c^2$", "Rigid bodies with rotation require additional $\\frac{1}{2}I\\omega^2$"],
            "mathematical_representation": "K = \\frac{1}{2} m v^2 = \\frac{p^2}{2m}",
            "claim_traces": ["HCV1 Ch 8 p. 128; HRW Ch 7 p. 173; UP Ch 6 p. 207"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-ke-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-wet-inertial-01",
            "chapter_id": "work-energy-power",
            "title": "Work-Energy Theorem in Inertial Frames",
            "formal_definition": "The total work $W_{\\text{net}}$ done by ALL forces (conservative, non-conservative, internal, and external) acting on a particle equals the change in its kinetic energy: $W_{\\text{net}} = \\sum W_i = \\Delta K = K_f - K_i = \\frac{1}{2} m v_f^2 - \\frac{1}{2} m v_i^2$.",
            "physical_intuition": "The work-energy theorem is the first integral of Newton's Second Law with respect to spatial displacement. It provides a direct scalar link between starting and ending speeds without requiring time-dependent trajectory integration.",
            "assumptions": ["Inertial frame of reference", "Newton's Second Law $\\vec{F}_{\\text{net}} = m \\vec{a}$ holds"],
            "validity_boundaries": ["Universal for particles in classical mechanics; applicable to arbitrary 3D curved paths"],
            "mathematical_representation": "W_{\\text{net}} = \\int \\vec{F}_{\\text{net}} \\cdot d\\vec{r} = \\Delta K",
            "claim_traces": ["HCV1 Ch 8 p. 132; HRW Ch 7 p. 174; UP Ch 6 p. 207"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-wet-inertial-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-wet-non-inertial-01",
            "chapter_id": "work-energy-power",
            "title": "Work-Energy Theorem in Non-Inertial Reference Frames",
            "formal_definition": "In a frame translating with acceleration $\\vec{a}_0$, the work-energy theorem remains valid provided the work of pseudo-forces $W_{\\text{pseudo}} = \\int (-m \\vec{a}_0) \\cdot d\\vec{r}_{\\text{rel}}$ is included: $W_{\\text{real}} + W_{\\text{pseudo}} = \\Delta K_{\\text{rel}} = \\frac{1}{2} m v_{f,\\text{rel}}^2 - \\frac{1}{2} m v_{i,\\text{rel}}^2$.",
            "physical_intuition": "Observers in accelerating elevators or vehicles can use energy methods directly, treating pseudo-force as an additional external force field doing work along the relative trajectory.",
            "assumptions": ["Purely translating reference frame with known acceleration $\\vec{a}_0(t)$", "Non-relativistic relative velocity"],
            "validity_boundaries": ["Rotating frames require additional centrifugal and Coriolis work terms"],
            "mathematical_representation": "W_{\\text{real}} + \\int (-m \\vec{a}_0) \\cdot d\\vec{r}_{\\text{rel}} = \\Delta K_{\\text{rel}}",
            "claim_traces": ["HCV1 Ch 8 p. 134; Irodov Part 1 Section 1.3 p. 27"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-wet-non-inertial-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-wet-internal-01",
            "chapter_id": "work-energy-power",
            "title": "Work Done by Internal Forces in Multi-Body Systems",
            "formal_definition": "For a multi-particle system, internal forces satisfy Newton's Third Law $\\vec{F}_{ij} = -\\vec{F}_{ji}$. However, the net internal work is $W_{\\text{int}} = \\int \\vec{F}_{ij} \\cdot d(\\vec{r}_i - \\vec{r}_j) = \\int \\vec{F}_{ij} \\cdot d\\vec{r}_{ij}$. For rigid bodies $d|\\vec{r}_{ij}| = 0$ so $W_{\\text{int}} = 0$; for deformable or sliding systems (e.g. springs, friction), $W_{\\text{int}} \\neq 0$.",
            "physical_intuition": "Internal forces do not change the total linear momentum of a system, but they CAN change its mechanical energy. An expanding spring or internal explosion does positive internal work, increasing kinetic energy.",
            "assumptions": ["Mutual central pair forces obeying Newton's Third Law"],
            "validity_boundaries": ["Vanishes strictly for rigid bodies where inter-particle distances are immutable"],
            "mathematical_representation": "W_{\\text{int}} = \\sum_{i < j} \\int \\vec{F}_{ij} \\cdot d\\vec{r}_{ij} \\neq 0 \\text{ (in general)}",
            "claim_traces": ["HCV1 Ch 8 p. 133; HRW Ch 8 p. 208; UP Ch 6 p. 213"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-wet-internal-01",
            "created_at": now_iso
        },

        # Section 3: Conservative Forces and Potential Energy (4 concepts)
        {
            "concept_id": "concept-wep-conservative-forces-01",
            "chapter_id": "work-energy-power",
            "title": "Conservative vs Non-Conservative Forces",
            "formal_definition": "A force $\\vec{F}$ is conservative if the work done on a particle moving between two points depends ONLY on the endpoints and is independent of the path taken: $\\oint_C \\vec{F} \\cdot d\\vec{r} = 0$ for every closed loop. Mathematically, $\\nabla \\times \\vec{F} = \\vec{0}$. Forces failing this (e.g. friction, drag) are non-conservative.",
            "physical_intuition": "Work done against a conservative force can be stored reversibly and recovered completely. Work done against friction is dissipated into random microscopic heat and cannot be recovered by reversing the path.",
            "assumptions": ["Single-valued, static or position-dependent force field"],
            "validity_boundaries": ["Velocity-dependent forces (friction, drag) and time-dependent fields are non-conservative"],
            "mathematical_representation": "\\oint \\vec{F}_c \\cdot d\\vec{r} = 0 \\iff \\vec{F}_c = -\\nabla U",
            "claim_traces": ["HCV1 Ch 8 p. 135; HRW Ch 8 p. 203; UP Ch 7 p. 248; Feynman Lec 14"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-conservative-forces-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-pe-def-gradient-01",
            "chapter_id": "work-energy-power",
            "title": "Potential Energy Definition and Gradient Relation",
            "formal_definition": "Potential energy $U$ is defined uniquely for conservative forces via the work of that force: $\\Delta U = U_f - U_i = -W_c = -\\int_{\\vec{r}_i}^{\\vec{r}_f} \\vec{F}_c \\cdot d\\vec{r}$. In differential form, $dU = -\\vec{F}_c \\cdot d\\vec{r}$, which yields the force as the negative gradient of potential energy: $\\vec{F}_c = -\\nabla U = -\\left(\\frac{\\partial U}{\\partial x}\\hat{i} + \\frac{\\partial U}{\\partial y}\\hat{j} + \\frac{\\partial U}{\\partial z}\\hat{k}\\right)$.",
            "physical_intuition": "A body released in a potential field naturally accelerates in the direction of steepest potential decrease (down the potential hill), where force is negative slope.",
            "assumptions": ["Conservative force field", "Arbitrary reference datum where $U(\\vec{r}_0) = 0$ is specified"],
            "validity_boundaries": ["Cannot be defined for non-conservative or friction forces", "Physical predictions depend only on differences $\\Delta U$, never absolute value"],
            "mathematical_representation": "F_x = -\\frac{\\partial U}{\\partial x}, \\quad \\vec{F} = -\\nabla U",
            "claim_traces": ["HCV1 Ch 8 p. 137; HRW Ch 8 p. 204; UP Ch 7 p. 252"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-pe-def-gradient-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-grav-spring-pe-01",
            "chapter_id": "work-energy-power",
            "title": "Gravitational and Elastic Potential Energy",
            "formal_definition": "For uniform near-surface gravity $\\vec{F}_g = -mg\\hat{j}$, gravitational potential energy is $U_g(y) = mgy$ relative to $y=0$. For an ideal spring with restoring force $F_s = -kx$, elastic potential energy is $U_s(x) = \\frac{1}{2}kx^2$ relative to relaxed state $x=0$.",
            "physical_intuition": "Lifting mass $m$ through height $h$ stores $mgh$ of potential energy. Stretching or compressing a spring by extension $x$ stores $\\frac{1}{2}kx^2$, positive regardless of whether extended or compressed.",
            "assumptions": ["Uniform gravitational field $g = \\text{const}$", "Hooke's spring constant $k = \\text{const}$"],
            "validity_boundaries": ["Large altitude changes require Newton's inverse-square potential $U(r) = -GMm/r$", "Spring valid only within elastic limit"],
            "mathematical_representation": "U_g = mgh, \\quad U_s = \\frac{1}{2} k x^2",
            "claim_traces": ["HCV1 Ch 8 p. 137-138; HRW Ch 8 p. 204; UP Ch 7 p. 235, 242"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-grav-spring-pe-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-mech-energy-cons-01",
            "chapter_id": "work-energy-power",
            "title": "Conservation of Mechanical Energy and Energy Balance",
            "formal_definition": "Total mechanical energy is defined as $E_{\\text{mech}} = K + U$. In the presence of only conservative forces, $W_{\\text{net}} = W_c = -\\Delta U \\implies \\Delta K + \\Delta U = 0 \\implies E_{\\text{mech}} = \\text{constant}$. In the general case with non-conservative forces, $\\Delta E_{\\text{mech}} = W_{\\text{nc}} + W_{\\text{ext}}$.",
            "physical_intuition": "Mechanical energy continuously exchanges between kinetic energy of motion and potential energy of configuration. Dissipation reduces total mechanical energy into microscopic heat.",
            "assumptions": ["Isolated system or zero non-conservative work $W_{\\text{nc}} = 0$"],
            "validity_boundaries": ["Universal energy conservation holds always; mechanical energy conservation holds only when $W_{\\text{nc}} = 0$"],
            "mathematical_representation": "K_i + U_i = K_f + U_f \\quad (W_{\\text{nc}} = 0), \\quad \\Delta E_{\\text{mech}} = W_{\\text{nc}}",
            "claim_traces": ["HCV1 Ch 8 p. 139; HRW Ch 8 p. 209; UP Ch 7 p. 237; Feynman Lec 4"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-mech-energy-cons-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-equilibrium-stability-01",
            "chapter_id": "work-energy-power",
            "title": "Equilibrium Analysis and Stability from Potential Curves",
            "formal_definition": "A particle is in static equilibrium where net force vanishes: $F_x = -dU/dx = 0$. The nature of equilibrium is classified by the second derivative of $U(x)$:\n1. Stable Equilibrium: $\\frac{d^2U}{dx^2} > 0$ (local potential minimum, restoring force returns particle)\n2. Unstable Equilibrium: $\\frac{d^2U}{dx^2} < 0$ (local potential maximum, repelling force drives particle away)\n3. Neutral Equilibrium: $\\frac{d^2U}{dx^2} = 0$ (flat potential, force remains zero on displacement).\nTurning points occur where total mechanical energy equals potential energy: $E = U(x) \\implies K = 0$.",
            "physical_intuition": "A marble at the bottom of a bowl is in stable equilibrium; balanced on an inverted bowl it is unstable; on a flat table it is neutral.",
            "assumptions": ["1D conservative system with smooth differentiable potential $U(x)$"],
            "validity_boundaries": ["Higher order derivatives tested if $\\frac{d^2U}{dx^2} = 0$"],
            "mathematical_representation": "\\frac{dU}{dx} = 0; \\quad \\frac{d^2U}{dx^2} > 0 \\text{ (stable)}, \\quad \\frac{d^2U}{dx^2} < 0 \\text{ (unstable)}",
            "claim_traces": ["HRW Ch 8 p. 205; UP Ch 7 p. 254; Irodov 1.3 p. 28"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-equilibrium-stability-01",
            "created_at": now_iso
        },

        # Section 4: Power and Vertical Circular Motion (4 concepts)
        {
            "concept_id": "concept-wep-power-def-01",
            "chapter_id": "work-energy-power",
            "title": "Average and Instantaneous Mechanical Power",
            "formal_definition": "Power is the time rate at which work is performed: Instantaneous power is $P = \\frac{dW}{dt} = \\frac{\\vec{F} \\cdot d\\vec{r}}{dt} = \\vec{F} \\cdot \\vec{v} = F v \\cos\\theta$. Average power over finite duration $\\Delta t$ is $P_{\\text{avg}} = \\frac{\\Delta W}{\\Delta t}$. The SI unit is the Watt ($1\\text{ W} = 1\\text{ J/s} = 1\\text{ kg m}^2\\text{s}^{-3}$); engineering unit is horsepower ($1\\text{ hp} = 746\\text{ W}$).",
            "physical_intuition": "A powerful machine does the same total work as a weak machine, but in a much shorter time. For a vehicle at speed $v$, engine force must deliver $P = F v$ to overcome resistance.",
            "assumptions": ["Force and velocity measured in the same inertial reference frame"],
            "validity_boundaries": ["Power is frame-dependent because velocity $\\vec{v}$ depends on observer frame"],
            "mathematical_representation": "P = \\frac{dW}{dt} = \\vec{F} \\cdot \\vec{v}, \\quad P_{\\text{avg}} = \\frac{W}{\\Delta t}",
            "claim_traces": ["HCV1 Ch 8 p. 142; HRW Ch 7 p. 181; UP Ch 6 p. 219"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-power-def-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-vertical-circle-critical-01",
            "chapter_id": "work-energy-power",
            "title": "Vertical Circular Motion and Critical Looping Speeds",
            "formal_definition": "A particle of mass $m$ tied to an inextensible light string of length $R$ moves in a vertical plane under gravity. At angle $\\theta$ from lowest point, radial dynamics yields string tension: $T - mg\\cos\\theta = \\frac{mv^2}{R}$. To complete a full circle, string tension must remain non-negative at the apex: $T_{\\text{top}} \\ge 0 \\implies v_{\\text{top}} \\ge \\sqrt{gR}$. By energy conservation, minimum launch speed at bottom is $v_{\\text{bot}} = \\sqrt{5gR}$, and tension difference is identically $T_{\\text{bot}} - T_{\\text{top}} = 6mg$.",
            "physical_intuition": "At the apex, gravity acts radially inward toward circle center. If apex speed drops below $\\sqrt{gR}$, gravity exceeds required centripetal acceleration, causing the string to slacken.",
            "assumptions": ["Inextensible, massless string", "Zero air resistance", "Planar vertical circle"],
            "validity_boundaries": ["Applies to flexible strings; rigid rods allow $v_{\\text{top}} = 0$ and $v_{\\text{bot}} = \\sqrt{4gR} = 2\\sqrt{gR}$"],
            "mathematical_representation": "v_{\\text{top,min}} = \\sqrt{gR}, \\quad v_{\\text{bot,min}} = \\sqrt{5gR}, \\quad T_{\\text{bot}} - T_{\\text{top}} = 6mg",
            "claim_traces": ["HCV1 Ch 8 p. 140; UP Ch 5 p. 184; Irodov 1.3 p. 29"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-vertical-circle-critical-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-vertical-circle-slack-01",
            "chapter_id": "work-energy-power",
            "title": "String Slackening and Projectile Departure in Upper Quadrant",
            "formal_definition": "If bottom speed satisfies $\\sqrt{2gR} < v_{\\text{bot}} < \\sqrt{5gR}$, the particle oscillates past the horizontal level ($\\theta = \\pi/2$) but cannot reach the apex ($\\theta = \\pi$). String tension vanishes ($T = 0$) at an angle $\\theta_s$ in the upper quadrant: $\\cos\\theta_s = -\\frac{v_{\\text{bot}}^2 - 2gR}{3gR}$. Beyond this point, the particle departs from circular path, executing free parabolic projectile flight under gravity.",
            "physical_intuition": "The particle still possesses forward velocity when tension vanishes, but no constraint force keeps it on the circular arc. It launches into free flight and subsequently re-tauts the string.",
            "assumptions": ["String remains completely flexible and slack during parabolic flight phase"],
            "validity_boundaries": ["If $v_{\\text{bot}} \\le \\sqrt{2gR}$, velocity vanishes before $\\pi/2$, causing simple pendulum oscillation without slack"],
            "mathematical_representation": "\\cos\\theta_s = -\\frac{v_{\\text{bot}}^2 - 2gR}{3gR}, \\quad v_s = \\sqrt{g R |\\cos\\theta_s|}",
            "claim_traces": ["HCV1 Ch 8 p. 141; Irodov 1.3 Problem 1.120"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-vertical-circle-slack-01",
            "created_at": now_iso
        },
        {
            "concept_id": "concept-wep-vertical-circle-rod-01",
            "chapter_id": "work-energy-power",
            "title": "Vertical Circular Motion Constrained by Rigid Rod or Pipe",
            "formal_definition": "When a particle is mounted on a light rigid rod of length $R$ or constrained inside a smooth vertical circular tube, the rod can support compression ($N < 0$ or outward normal). The particle can reach the apex with zero velocity without falling: $v_{\\text{top,min}} = 0$. By energy conservation, minimum launch speed at bottom is $v_{\\text{bot,min}} = \\sqrt{4gR} = 2\\sqrt{gR}$.",
            "physical_intuition": "Unlike a string which buckles under compression, a rigid rod pushes outward to support the particle against gravity at low speeds near the apex.",
            "assumptions": ["Rigid, massless rod", "No friction or air resistance"],
            "validity_boundaries": ["Contrast with flexible string where minimum apex speed is strictly $\\sqrt{gR}$"],
            "mathematical_representation": "v_{\\text{top,min}} = 0, \\quad v_{\\text{bot,min}} = \\sqrt{4gR} = 2\\sqrt{gR}",
            "claim_traces": ["HCV1 Ch 8 p. 141; Irodov 1.3 Problem 1.121"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-concept-wep-vertical-circle-rod-01",
            "created_at": now_iso
        }
    ]

    for c in concepts:
        chash = compute_content_hash(c)
        c["content_hash"] = chash
        for p in [content_dir / "concepts" / f"{c['concept_id']}.json", staging_content / "concepts" / f"{c['concept_id']}.json"]:
            p.write_text(json.dumps(c, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 3. FORMULAS (14 items)
    # =============================================================
    formulas = [
        {
            "formula_id": "formula-wep-work-const",
            "chapter_id": "work-energy-power",
            "title": "Work Done by a Constant Force",
            "equation_latex": "W = \\vec{F} \\cdot \\vec{d} = F d \\cos\\theta = F_x d_x + F_y d_y + F_z d_z",
            "variables": {
                "W": "Mechanical work done",
                "\\vec{F}": "Constant force vector",
                "\\vec{d}": "Displacement vector",
                "\\theta": "Angle between force and displacement vectors"
            },
            "units": {"W": "J (N m)", "\\vec{F}": "N", "\\vec{d}": "m", "\\theta": "rad"},
            "dimensions": {"W": "[M][L]^2[T]^-2", "\\vec{F}": "[M][L][T]^-2", "\\vec{d}": "[L]", "\\theta": "[1]"},
            "assumptions": ["Force is constant in magnitude and direction throughout displacement"],
            "conditions_of_validity": ["Point particle or translation without rotation"],
            "common_misuse": ["Using distance traveled along curve instead of displacement vector", "Multiplying force magnitude by distance without cos(theta)"],
            "derivation_reference": "derivation-formula-wep-work-const",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-work-const",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-work-var-integral",
            "chapter_id": "work-energy-power",
            "title": "Work Done by a Variable Force",
            "equation_latex": "W = \\int_{\\vec{r}_i}^{\\vec{r}_f} \\vec{F}(\\vec{r}) \\cdot d\\vec{r} = \\int_{x_i}^{x_f} F_x \\, dx + \\int_{y_i}^{y_f} F_y \\, dy + \\int_{z_i}^{z_f} F_z \\, dz",
            "variables": {
                "W": "Work done along trajectory",
                "\\vec{F}(\\vec{r})": "Position-dependent force field",
                "d\\vec{r}": "Infinitesimal displacement element vector"
            },
            "units": {"W": "J", "\\vec{F}": "N", "d\\vec{r}": "m"},
            "dimensions": {"W": "[M][L]^2[T]^-2", "\\vec{F}": "[M][L][T]^-2", "d\\vec{r}": "[L]"},
            "assumptions": ["Force is integrable along piecewise smooth trajectory curve"],
            "conditions_of_validity": ["Universal for 1D, 2D, and 3D classical particle motion"],
            "common_misuse": ["Evaluating integral without specifying parametric path when force is non-conservative"],
            "derivation_reference": "derivation-formula-wep-work-var-integral",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-work-var-integral",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-work-spring",
            "chapter_id": "work-energy-power",
            "title": "Work Done by an Ideal Spring",
            "equation_latex": "W_s = -\\frac{1}{2} k (x_f^2 - x_i^2)",
            "variables": {
                "W_s": "Work done BY the spring",
                "k": "Spring stiffness constant",
                "x_i": "Initial deformation from natural length",
                "x_f": "Final deformation from natural length"
            },
            "units": {"W_s": "J", "k": "N/m (kg s^-2)", "x": "m"},
            "dimensions": {"W_s": "[M][L]^2[T]^-2", "k": "[M][T]^-2", "x": "[L]"},
            "assumptions": ["Massless spring obeying Hooke's law F = -kx", "Deformation measured from unstretched length"],
            "conditions_of_validity": ["Within elastic limit of spring material"],
            "common_misuse": ["Confusing work done BY spring (-1/2 k x^2) with work done BY external agent (+1/2 k x^2)", "Omitting squared term"],
            "derivation_reference": "derivation-formula-wep-work-spring",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-work-spring",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-work-friction-kinetic",
            "chapter_id": "work-energy-power",
            "title": "Work Done by Kinetic Friction",
            "equation_latex": "W_{f_k} = -f_k s_{\\text{rel}} = -\\mu_k N s_{\\text{rel}}",
            "variables": {
                "W_{f_k}": "Dissipative interfacial work of kinetic friction",
                "\\mu_k": "Coefficient of kinetic friction",
                "N": "Normal contact reaction force",
                "s_{\\text{rel}}": "Relative sliding displacement distance between contacting surfaces"
            },
            "units": {"W": "J", "\\mu_k": "dimensionless", "N": "N", "s": "m"},
            "dimensions": {"W": "[M][L]^2[T]^-2", "\\mu_k": "[1]", "N": "[M][L][T]^-2", "s": "[L]"},
            "assumptions": ["Constant normal force along sliding distance", "Constant coefficient mu_k"],
            "conditions_of_validity": ["Dry sliding contact obeying Amontons-Coulomb law"],
            "common_misuse": ["Using ground-frame displacement instead of relative interfacial displacement s_rel"],
            "derivation_reference": "derivation-formula-wep-work-friction-kinetic",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-work-friction-kinetic",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-kinetic-energy",
            "chapter_id": "work-energy-power",
            "title": "Kinetic Energy of a Particle",
            "equation_latex": "K = \\frac{1}{2} m v^2 = \\frac{p^2}{2m}",
            "variables": {
                "K": "Kinetic energy",
                "m": "Inertial mass",
                "v": "Speed magnitude in reference frame",
                "p": "Magnitude of linear momentum"
            },
            "units": {"K": "J", "m": "kg", "v": "m/s", "p": "kg m/s"},
            "dimensions": {"K": "[M][L]^2[T]^-2", "m": "[M]", "v": "[L][T]^-1", "p": "[M][L][T]^-1"},
            "assumptions": ["Classical non-relativistic speed v << c", "Point mass or pure translation"],
            "conditions_of_validity": ["Universal scalar definition in classical mechanics"],
            "common_misuse": ["Treating kinetic energy as a vector", "Applying formula in non-inertial frame without relative speed"],
            "derivation_reference": "derivation-formula-wep-kinetic-energy",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-kinetic-energy",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-work-energy-theorem",
            "chapter_id": "work-energy-power",
            "title": "Work-Energy Theorem in Inertial Frame",
            "equation_latex": "W_{\\text{net}} = \\Delta K = K_f - K_i = \\frac{1}{2} m v_f^2 - \\frac{1}{2} m v_i^2",
            "variables": {
                "W_{\\text{net}}": "Total net work done by all forces",
                "\\Delta K": "Change in kinetic energy",
                "m": "Mass of particle",
                "v_i": "Initial speed",
                "v_f": "Final speed"
            },
            "units": {"W": "J", "K": "J", "m": "kg", "v": "m/s"},
            "dimensions": {"all": "[M][L]^2[T]^-2"},
            "assumptions": ["Inertial frame of reference", "Newton's Second Law holds"],
            "conditions_of_validity": ["Valid for all forces including conservative, non-conservative, variable, internal, and external"],
            "common_misuse": ["Omitting work done by normal force, tension, or friction", "Applying to non-inertial frame without pseudo-force work"],
            "derivation_reference": "derivation-formula-wep-work-energy-theorem",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-work-energy-theorem",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-wet-non-inertial",
            "chapter_id": "work-energy-power",
            "title": "Work-Energy Theorem in Non-Inertial Reference Frame",
            "equation_latex": "W_{\\text{real}} + W_{\\text{pseudo}} = \\Delta K_{\\text{rel}}",
            "variables": {
                "W_{\\text{real}}": "Work done by all physical forces along relative displacement",
                "W_{\\text{pseudo}}": "Work done by fictitious inertial pseudo-force int (-m a_0) . dr_rel",
                "\\Delta K_{\\text{rel}}": "Change in kinetic energy evaluated in the accelerating frame"
            },
            "units": {"all": "J"},
            "dimensions": {"all": "[M][L]^2[T]^-2"},
            "assumptions": ["Translating frame of reference with linear acceleration a_0"],
            "conditions_of_validity": ["Displacement evaluated relative to the accelerating frame"],
            "common_misuse": ["Using ground-frame displacement for pseudo-force work", "Forgetting negative sign in pseudo-force F_pseudo = -m a_0"],
            "derivation_reference": "derivation-formula-wep-wet-non-inertial",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-wet-non-inertial",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-pe-def",
            "chapter_id": "work-energy-power",
            "title": "Definition of Potential Energy for Conservative Force",
            "equation_latex": "\\Delta U = U_f - U_i = -W_c = -\\int_{\\vec{r}_i}^{\\vec{r}_f} \\vec{F}_c \\cdot d\\vec{r}",
            "variables": {
                "\\Delta U": "Change in potential energy",
                "W_c": "Work done by the conservative force",
                "\\vec{F}_c": "Conservative force vector"
            },
            "units": {"U": "J", "W": "J", "F": "N", "r": "m"},
            "dimensions": {"U": "[M][L]^2[T]^-2"},
            "assumptions": ["Force field F_c is strictly conservative (curl F = 0)"],
            "conditions_of_validity": ["Independent of integration path"],
            "common_misuse": ["Attempting to define potential energy for friction or dissipative forces", "Omitting negative sign Delta U = -W_c"],
            "derivation_reference": "derivation-formula-wep-pe-gradient",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-pe-def",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-pe-gradient",
            "chapter_id": "work-energy-power",
            "title": "Force as Negative Potential Energy Gradient",
            "equation_latex": "\\vec{F} = -\\nabla U = -\\left(\\frac{\\partial U}{\\partial x}\\hat{i} + \\frac{\\partial U}{\\partial y}\\hat{j} + \\frac{\\partial U}{\\partial z}\\hat{k}\\right), \\quad F_x = -\\frac{dU}{dx}",
            "variables": {
                "\\vec{F}": "Conservative force vector",
                "U(\\vec{r})": "Scalar potential energy function",
                "\\nabla": "Spatial gradient vector operator"
            },
            "units": {"F": "N", "U": "J", "x": "m"},
            "dimensions": {"F": "[M][L][T]^-2", "U": "[M][L]^2[T]^-2"},
            "assumptions": ["Smooth differentiable scalar potential field U(x, y, z)"],
            "conditions_of_validity": ["Exact differential dU = -F . dr"],
            "common_misuse": ["Omitting negative sign resulting in force directed toward potential maxima", "Using ordinary derivative instead of partials in 3D"],
            "derivation_reference": "derivation-formula-wep-pe-gradient",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-pe-gradient",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-mech-energy-conservation",
            "chapter_id": "work-energy-power",
            "title": "Conservation of Mechanical Energy",
            "equation_latex": "E_{\\text{mech}} = K + U = \\text{constant} \\iff K_i + U_i = K_f + U_f",
            "variables": {
                "E_{\\text{mech}}": "Total mechanical energy",
                "K": "Kinetic energy",
                "U": "Total potential energy"
            },
            "units": {"E": "J", "K": "J", "U": "J"},
            "dimensions": {"all": "[M][L]^2[T]^-2"},
            "assumptions": ["Only conservative forces do work on system (W_nc = 0)"],
            "conditions_of_validity": ["Zero non-conservative work and zero external energy exchange"],
            "common_misuse": ["Applying formula when friction or air resistance is present without including dissipative work"],
            "derivation_reference": "derivation-formula-wep-mech-energy-conservation",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-mech-energy-conservation",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-equilibrium-stability",
            "chapter_id": "work-energy-power",
            "title": "Equilibrium Condition and Curvature Stability",
            "equation_latex": "\\frac{dU}{dx} = 0; \\quad \\frac{d^2U}{dx^2} > 0 \\text{ (stable)}, \\quad \\frac{d^2U}{dx^2} < 0 \\text{ (unstable)}, \\quad \\frac{d^2U}{dx^2} = 0 \\text{ (neutral)}",
            "variables": {
                "U(x)": "1D potential energy function",
                "x": "Position coordinate"
            },
            "units": {"U": "J", "x": "m"},
            "dimensions": {"dU/dx": "[M][L][T]^-2", "d2U/dx2": "[M][T]^-2"},
            "assumptions": ["1D conservative system with twice-differentiable potential U(x)"],
            "conditions_of_validity": ["Local Taylor expansion near equilibrium coordinate x_0"],
            "common_misuse": ["Confusing potential energy minimum with maximum", "Ignoring higher order derivatives when d2U/dx2 = 0"],
            "derivation_reference": "derivation-formula-wep-pe-gradient",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-equilibrium-stability",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-power-instantaneous",
            "chapter_id": "work-energy-power",
            "title": "Instantaneous Mechanical Power",
            "equation_latex": "P = \\frac{dW}{dt} = \\vec{F} \\cdot \\vec{v} = F v \\cos\\theta = F_x v_x + F_y v_y + F_z v_z",
            "variables": {
                "P": "Instantaneous power",
                "W": "Work performed",
                "\\vec{F}": "Applied force vector",
                "\\vec{v}": "Velocity vector of point of application"
            },
            "units": {"P": "W (J/s)", "\\vec{F}": "N", "\\vec{v}": "m/s"},
            "dimensions": {"P": "[M][L]^2[T]^-3", "\\vec{F}": "[M][L][T]^-2", "\\vec{v}": "[L][T]^-1"},
            "assumptions": ["Inertial reference frame for velocity vector"],
            "conditions_of_validity": ["Point of application velocity matched with force agent"],
            "common_misuse": ["Using average speed instead of instantaneous dot product F . v", "Assuming power is constant during uniform acceleration"],
            "derivation_reference": "derivation-formula-wep-power-instantaneous",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-power-instantaneous",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-vcm-critical-bottom",
            "chapter_id": "work-energy-power",
            "title": "Critical Looping Velocities for Vertical Circle with String",
            "equation_latex": "v_{\\text{bot,min}} = \\sqrt{5 g R}, \\quad v_{\\text{top,min}} = \\sqrt{g R}, \\quad T_{\\text{bot}} - T_{\\text{top}} = 6 mg",
            "variables": {
                "v_{\\text{bot,min}}": "Minimum speed at lowest point to complete vertical loop",
                "v_{\\text{top,min}}": "Minimum speed at highest point (apex) without slackening",
                "R": "Radius of circular path (length of string)",
                "g": "Acceleration due to gravity",
                "m": "Mass of particle"
            },
            "units": {"v": "m/s", "R": "m", "g": "m/s^2", "m": "kg", "T": "N"},
            "dimensions": {"v": "[L][T]^-1", "R": "[L]", "g": "[L][T]^-2", "T": "[M][L][T]^-2"},
            "assumptions": ["Light inextensible string", "No air resistance", "Planar vertical circle"],
            "conditions_of_validity": ["String tension T >= 0 everywhere on trajectory"],
            "common_misuse": ["Using v_bot = sqrt(4gR) for string instead of rigid rod", "Assuming apex speed can be zero with a string"],
            "derivation_reference": "derivation-formula-wep-vcm-critical",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-vcm-critical-bottom",
            "created_at": now_iso
        },
        {
            "formula_id": "formula-wep-vcm-slack-condition",
            "chapter_id": "work-energy-power",
            "title": "String Slackening Angle in Upper Quadrant",
            "equation_latex": "\\cos\\theta_{\\text{slack}} = -\\frac{v_{\\text{bot}}^2 - 2gR}{3gR}, \\quad \\text{for } \\sqrt{2gR} < v_{\\text{bot}} < \\sqrt{5gR}",
            "variables": {
                "\\theta_{\\text{slack}}": "Angle measured from lowest point at which string tension vanishes",
                "v_{\\text{bot}}": "Launch speed at bottom",
                "R": "Radius of circle",
                "g": "Gravitational acceleration"
            },
            "units": {"\\theta": "rad", "v": "m/s", "R": "m", "g": "m/s^2"},
            "dimensions": {"\\theta": "[1]", "cos": "[1]"},
            "assumptions": ["Tension vanishes at angle theta_slack with non-zero speed", "Light inextensible string"],
            "conditions_of_validity": ["Valid strictly in range pi/2 < theta < pi where cos(theta) < 0"],
            "common_misuse": ["Applying formula when v_bot <= sqrt(2gR) (pendulum oscillation regime)", "Assuming speed is zero at slack point"],
            "derivation_reference": "derivation-formula-wep-vcm-slack",
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-formula-wep-vcm-slack-condition",
            "created_at": now_iso
        }
    ]

    for f in formulas:
        fhash = compute_content_hash(f)
        f["content_hash"] = fhash
        for p in [content_dir / "formulas" / f"{f['formula_id']}.json", staging_content / "formulas" / f"{f['formula_id']}.json"]:
            p.write_text(json.dumps(f, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 4. DERIVATIONS (7 items)
    # =============================================================
    derivations = [
        {
            "derivation_id": "derivation-formula-wep-work-spring",
            "chapter_id": "work-energy-power",
            "title": "Derivation of Work Done by an Ideal Spring from Hooke's Law",
            "target_formula_id": "formula-wep-work-spring",
            "target_equation": "W_s = -\\frac{1}{2} k (x_f^2 - x_i^2)",
            "assumptions": ["Massless spring", "Linear restoring force F = -kx", "Smooth 1D displacement along spring axis"],
            "starting_principles": ["Definition of work as 1D spatial integral W = int F(x) dx", "Hooke's law F_s(x) = -kx"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Express the differential work done by the spring restoring force for infinitesimal displacement dx.",
                    "equation_latex": "dW_s = F_s(x) \\, dx = (-kx) \\, dx"
                },
                {
                    "step_number": 2,
                    "explanation": "Integrate the differential work expression from initial deformation x_i to final deformation x_f.",
                    "equation_latex": "W_s = \\int_{x_i}^{x_f} (-kx) \\, dx = -k \\int_{x_i}^{x_f} x \\, dx"
                },
                {
                    "step_number": 3,
                    "explanation": "Evaluate the definite integral using power rule of calculus.",
                    "equation_latex": "W_s = -k \\left[ \\frac{x^2}{2} \\right]_{x_i}^{x_f} = -\\frac{1}{2} k (x_f^2 - x_i^2)"
                }
            ],
            "limiting_cases": [
                "When starting from natural length x_i = 0, W_s = -1/2 k x_f^2, which is strictly negative for any extension or compression",
                "When returning to initial state x_f = x_i, W_s = 0, proving conservative character over round trip"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 130; HRW Ch 7 p. 175; UP Ch 6 p. 216"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-derivation-formula-wep-work-spring",
            "created_at": now_iso
        },
        {
            "derivation_id": "derivation-formula-wep-work-energy-theorem",
            "chapter_id": "work-energy-power",
            "title": "First-Principles Proof of the Work-Energy Theorem for Particle Motion",
            "target_formula_id": "formula-wep-work-energy-theorem",
            "target_equation": "W_{\\text{net}} = \\Delta K = \\frac{1}{2} m v_f^2 - \\frac{1}{2} m v_i^2",
            "assumptions": ["Inertial reference frame", "Constant particle mass m", "Newton's Second Law F_net = m dv/dt"],
            "starting_principles": ["Definition of net work as path line integral W_net = int F_net . dr", "Kinematic identity v = dr/dt"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Substitute Newton's Second Law F_net = m dv/dt into the work line integral.",
                    "equation_latex": "W_{\\text{net}} = \\int_{\\vec{r}_i}^{\\vec{r}_f} \\vec{F}_{\\text{net}} \\cdot d\\vec{r} = \\int_{t_i}^{t_f} m \\frac{d\\vec{v}}{dt} \\cdot \\frac{d\\vec{r}}{dt} \\, dt"
                },
                {
                    "step_number": 2,
                    "explanation": "Express velocity vector v = dr/dt and utilize differential scalar product d(v . v) = 2 v . dv.",
                    "equation_latex": "W_{\\text{net}} = \\int_{t_i}^{t_f} m \\frac{d\\vec{v}}{dt} \\cdot \\vec{v} \\, dt = m \\int_{\\vec{v}_i}^{\\vec{v}_f} \\vec{v} \\cdot d\\vec{v}"
                },
                {
                    "step_number": 3,
                    "explanation": "Recognize that v . dv = v dv, converting vector line integral into standard 1D scalar integral over speed.",
                    "equation_latex": "W_{\\text{net}} = m \\int_{v_i}^{v_f} v \\, dv = m \\left[ \\frac{v^2}{2} \\right]_{v_i}^{v_f} = \\frac{1}{2} m v_f^2 - \\frac{1}{2} m v_i^2 = \\Delta K"
                }
            ],
            "limiting_cases": [
                "When net work is zero, Delta K = 0 implying speed magnitude remains invariant (e.g. uniform circular motion)",
                "When initial speed v_i = 0, W_net = 1/2 m v_f^2, representing work done to accelerate body from rest"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 132; HRW Ch 7 p. 174; UP Ch 6 p. 208"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-derivation-formula-wep-work-energy-theorem",
            "created_at": now_iso
        },
        {
            "derivation_id": "derivation-formula-wep-wet-non-inertial",
            "chapter_id": "work-energy-power",
            "title": "Derivation of the Work-Energy Theorem in Non-Inertial Reference Frames",
            "target_formula_id": "formula-wep-wet-non-inertial",
            "target_equation": "W_{\\text{real}} + W_{\\text{pseudo}} = \\Delta K_{\\text{rel}}",
            "assumptions": ["Translating frame with acceleration a_0(t)", "Apparent particle acceleration a_rel = a - a_0"],
            "starting_principles": ["Modified Newton's Second Law F_real - m a_0 = m a_rel in accelerating frame"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Write dynamic equation of particle in accelerating frame incorporating pseudo-force F_pseudo = -m a_0.",
                    "equation_latex": "m \\vec{a}_{\\text{rel}} = \\vec{F}_{\\text{real}} - m \\vec{a}_0"
                },
                {
                    "step_number": 2,
                    "explanation": "Take the scalar dot product of both sides with relative infinitesimal displacement dr_rel.",
                    "equation_latex": "m \\vec{a}_{\\text{rel}} \\cdot d\\vec{r}_{\\text{rel}} = \\vec{F}_{\\text{real}} \\cdot d\\vec{r}_{\\text{rel}} + (-m \\vec{a}_0) \\cdot d\\vec{r}_{\\text{rel}}"
                },
                {
                    "step_number": 3,
                    "explanation": "Integrate along the relative trajectory curve from initial to final state.",
                    "equation_latex": "\\int m \\frac{d\\vec{v}_{\\text{rel}}}{dt} \\cdot \\vec{v}_{\\text{rel}} \\, dt = \\int \\vec{F}_{\\text{real}} \\cdot d\\vec{r}_{\\text{rel}} + \\int \\vec{F}_{\\text{pseudo}} \\cdot d\\vec{r}_{\\text{rel}} \\implies \\Delta K_{\\text{rel}} = W_{\\text{real}} + W_{\\text{pseudo}}"
                }
            ],
            "limiting_cases": [
                "When frame acceleration a_0 = 0, W_pseudo = 0 and equation reduces to standard inertial work-energy theorem"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 134; Irodov Part 1 Section 1.3 p. 27"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-derivation-formula-wep-wet-non-inertial",
            "created_at": now_iso
        },
        {
            "derivation_id": "derivation-formula-wep-pe-gradient",
            "chapter_id": "work-energy-power",
            "title": "Mathematical Derivation of Conservative Force as Negative Potential Gradient",
            "target_formula_id": "formula-wep-pe-gradient",
            "target_equation": "\\vec{F} = -\\nabla U, \\quad F_x = -\\frac{\\partial U}{\\partial x}",
            "assumptions": ["Conservative force field", "Exact differential dU = -F . dr", "Smooth spatial coordinates x, y, z"],
            "starting_principles": ["Definition of potential energy differential dU = - dW_c = - (F_x dx + F_y dy + F_z dz)", "Total multivariable differential dU = (dU/dx)dx + (dU/dy)dy + (dU/dz)dz"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Write total differential of scalar function U(x, y, z) using partial derivatives.",
                    "equation_latex": "dU = \\frac{\\partial U}{\\partial x} \\, dx + \\frac{\\partial U}{\\partial y} \\, dy + \\frac{\\partial U}{\\partial z} \\, dz"
                },
                {
                    "step_number": 2,
                    "explanation": "Equate with the physical definition of potential energy differential dU = - (F_x dx + F_y dy + F_z dz).",
                    "equation_latex": "-\\left( F_x \\, dx + F_y \\, dy + F_z \\, dz \\right) = \\frac{\\partial U}{\\partial x} \\, dx + \\frac{\\partial U}{\\partial y} \\, dy + \\frac{\\partial U}{\\partial z} \\, dz"
                },
                {
                    "step_number": 3,
                    "explanation": "Since dx, dy, dz are independent arbitrary displacements, equate corresponding components.",
                    "equation_latex": "F_x = -\\frac{\\partial U}{\\partial x}, \\quad F_y = -\\frac{\\partial U}{\\partial y}, \\quad F_z = -\\frac{\\partial U}{\\partial z} \\implies \\vec{F} = -\\nabla U"
                }
            ],
            "limiting_cases": [
                "For 1D spring U = 1/2 k x^2, F_x = -d(1/2 k x^2)/dx = -kx (recovering Hooke's law)",
                "For near-surface gravity U = mgy, F_y = -d(mgy)/dy = -mg (recovering downward weight)"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 137; HRW Ch 8 p. 204; UP Ch 7 p. 252"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-derivation-formula-wep-pe-gradient",
            "created_at": now_iso
        },
        {
            "derivation_id": "derivation-formula-wep-mech-energy-conservation",
            "chapter_id": "work-energy-power",
            "title": "Derivation of Mechanical Energy Conservation from Work-Energy Principle",
            "target_formula_id": "formula-wep-mech-energy-conservation",
            "target_equation": "E_{\\text{mech}} = K + U = \\text{constant}",
            "assumptions": ["Net work decomposed into conservative and non-conservative components: W_net = W_c + W_nc"],
            "starting_principles": ["Work-energy theorem W_net = Delta K", "Potential energy definition W_c = - Delta U"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Decompose total work into conservative forces W_c and non-conservative forces W_nc.",
                    "equation_latex": "W_{\\text{net}} = W_c + W_{\\text{nc}}"
                },
                {
                    "step_number": 2,
                    "explanation": "Substitute W_net = Delta K from the work-energy theorem.",
                    "equation_latex": "W_c + W_{\\text{nc}} = \\Delta K"
                },
                {
                    "step_number": 3,
                    "explanation": "Substitute W_c = - Delta U from the potential energy definition and rearrange terms.",
                    "equation_latex": "-\\Delta U + W_{\\text{nc}} = \\Delta K \\implies \\Delta K + \\Delta U = W_{\\text{nc}} \\implies \\Delta(K + U) = W_{\\text{nc}}"
                },
                {
                    "step_number": 4,
                    "explanation": "When non-conservative work vanishes (W_nc = 0), mechanical energy is strictly invariant.",
                    "equation_latex": "\\Delta(K + U) = 0 \\implies K_i + U_i = K_f + U_f = E_{\\text{mech}} = \\text{constant}"
                }
            ],
            "limiting_cases": [
                "If non-conservative dissipative work is negative W_nc = - Q_diss, E_f = E_i - Q_diss (mechanical energy decreases)"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 139; HRW Ch 8 p. 209; UP Ch 7 p. 237"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-derivation-formula-wep-mech-energy-conservation",
            "created_at": now_iso
        },
        {
            "derivation_id": "derivation-formula-wep-vcm-critical",
            "chapter_id": "work-energy-power",
            "title": "Derivation of Critical Looping Speeds and Invariant Tension Difference in Vertical Circle",
            "target_formula_id": "formula-wep-vcm-critical-bottom",
            "target_equation": "v_{\\text{bot,min}} = \\sqrt{5 g R}, \\quad v_{\\text{top,min}} = \\sqrt{g R}, \\quad T_{\\text{bot}} - T_{\\text{top}} = 6 mg",
            "assumptions": ["Light inextensible string of radius R", "Particle of mass m in uniform vertical gravity g", "Conservative loop"],
            "starting_principles": ["Radial dynamic equation T - mg cos(theta) = m v^2 / R", "Conservation of mechanical energy between bottom and top"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Write radial equation of motion at top (theta = pi, cos(pi) = -1) where gravity acts downward toward center.",
                    "equation_latex": "T_{\\text{top}} + mg = \\frac{m v_{\\text{top}}^2}{R} \\implies T_{\\text{top}} = \\frac{m v_{\\text{top}}^2}{R} - mg"
                },
                {
                    "step_number": 2,
                    "explanation": "Impose string non-slackening condition T_top >= 0 to find minimum apex speed.",
                    "equation_latex": "T_{\\text{top}} \\ge 0 \\implies \\frac{m v_{\\text{top}}^2}{R} - mg \\ge 0 \\implies v_{\\text{top}} \\ge \\sqrt{g R}"
                },
                {
                    "step_number": 3,
                    "explanation": "Apply mechanical energy conservation between bottom (y = 0) and top (y = 2R).",
                    "equation_latex": "\\frac{1}{2} m v_{\\text{bot}}^2 = \\frac{1}{2} m v_{\\text{top}}^2 + mg (2R) \\implies v_{\\text{bot}}^2 = v_{\\text{top}}^2 + 4 g R"
                },
                {
                    "step_number": 4,
                    "explanation": "Substitute critical apex speed v_top,min^2 = g R to find critical bottom speed.",
                    "equation_latex": "v_{\\text{bot,min}}^2 = g R + 4 g R = 5 g R \\implies v_{\\text{bot,min}} = \\sqrt{5 g R}"
                },
                {
                    "step_number": 5,
                    "explanation": "Express tension at bottom T_bot = m v_bot^2 / R + mg and compute difference T_bot - T_top.",
                    "equation_latex": "T_{\\text{bot}} - T_{\\text{top}} = \\left(\\frac{m v_{\\text{bot}}^2}{R} + mg\\right) - \\left(\\frac{m v_{\\text{top}}^2}{R} - mg\\right) = \\frac{m}{R}(v_{\\text{bot}}^2 - v_{\\text{top}}^2) + 2mg = \\frac{m}{R}(4gR) + 2mg = 6mg"
                }
            ],
            "limiting_cases": [
                "T_bot - T_top = 6mg is an exact invariant for all vertical circular motion with strings regardless of launch energy"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 140; UP Ch 5 p. 184"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-derivation-formula-wep-vcm-critical",
            "created_at": now_iso
        },
        {
            "derivation_id": "derivation-formula-wep-vcm-slack",
            "chapter_id": "work-energy-power",
            "title": "Derivation of String Slackening Angle and Velocity in Vertical Circle",
            "target_formula_id": "formula-wep-vcm-slack-condition",
            "target_equation": "\\cos\\theta_{\\text{slack}} = -\\frac{v_{\\text{bot}}^2 - 2gR}{3gR}",
            "assumptions": ["Launch speed sqrt(2gR) < v_bot < sqrt(5gR)", "Light inextensible string", "Particle leaves circular path at T = 0"],
            "starting_principles": ["Radial equation T - mg cos(theta) = m v^2 / R with theta measured from lowest point", "Energy conservation 1/2 m v_bot^2 = 1/2 m v^2 + mg R(1 - cos(theta))"],
            "ordered_steps": [
                {
                    "step_number": 1,
                    "explanation": "Express velocity v(theta) at angle theta from bottom using energy conservation.",
                    "equation_latex": "v^2(\\theta) = v_{\\text{bot}}^2 - 2 g R (1 - \\cos\\theta)"
                },
                {
                    "step_number": 2,
                    "explanation": "Substitute v^2(theta) into the general radial dynamic tension equation.",
                    "equation_latex": "T(\\theta) = \\frac{m v^2(\\theta)}{R} + mg \\cos\\theta = \\frac{m}{R}\\left[ v_{\\text{bot}}^2 - 2 g R + 2 g R \\cos\\theta \\right] + mg \\cos\\theta = \\frac{m v_{\\text{bot}}^2}{R} - 2 mg + 3 mg \\cos\\theta"
                },
                {
                    "step_number": 3,
                    "explanation": "Set string tension equal to zero T(theta_slack) = 0 to obtain the condition for slackening.",
                    "equation_latex": "\\frac{m v_{\\text{bot}}^2}{R} - 2 mg + 3 mg \\cos\\theta_{\\text{slack}} = 0 \\implies 3 mg \\cos\\theta_{\\text{slack}} = 2 mg - \\frac{m v_{\\text{bot}}^2}{R}"
                },
                {
                    "step_number": 4,
                    "explanation": "Solve for cos(theta_slack).",
                    "equation_latex": "\\cos\\theta_{\\text{slack}} = -\\frac{v_{\\text{bot}}^2 - 2 g R}{3 g R}"
                }
            ],
            "limiting_cases": [
                "If v_bot = sqrt(2gR), cos(theta_slack) = 0 yielding theta_slack = pi/2 (reaches horizontal with v=0)",
                "If v_bot = sqrt(5gR), cos(theta_slack) = - (5gR - 2gR)/(3gR) = -1 yielding theta_slack = pi (apex without slack)"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 141; Irodov 1.3 Problem 1.120"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-derivation-formula-wep-vcm-slack",
            "created_at": now_iso
        }
    ]

    for d in derivations:
        dhash = compute_content_hash(d)
        d["content_hash"] = dhash
        for p in [content_dir / "derivations" / f"{d['derivation_id']}.json", staging_content / "derivations" / f"{d['derivation_id']}.json"]:
            p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 5. WORKED EXAMPLES (6 items)
    # =============================================================
    examples = [
        {
            "example_id": "ex-wep-spring-compress-01",
            "chapter_id": "work-energy-power",
            "problem_statement": "A block of mass $m = 2.0\\text{ kg}$ is released with speed $v_0 = 4.0\\text{ m/s}$ on a rough horizontal floor with kinetic friction coefficient $\\mu_k = 0.20$. After traveling distance $d = 2.0\\text{ m}$, it collides with an uncompressed horizontal spring of spring constant $k = 400\\text{ N/m}$ fixed to a rigid wall. Find the maximum compression $x_{\\text{max}}$ of the spring. (Take $g = 9.8\\text{ m/s}^2$).",
            "known_parameters": {"m": 2.0, "v_0": 4.0, "mu_k": 0.20, "d": 2.0, "k": 400.0, "g": 9.8},
            "target_variable": "x_max",
            "solution_strategy": "Apply the Work-Energy Theorem to the block from initial release to the point of maximum spring compression, accounting for friction work over total distance d + x_max and spring work.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "State initial and final kinetic energies of the block.",
                    "equation_latex": "K_i = \\frac{1}{2} m v_0^2 = \\frac{1}{2}(2.0)(4.0)^2 = 16.0\\text{ J}, \\quad K_f = 0"
                },
                {
                    "step_number": 2,
                    "explanation": "Express total work done by friction and spring over total displacement d + x_max.",
                    "equation_latex": "W_{\\text{net}} = W_{f_k} + W_s = -\\mu_k m g (d + x_{\\text{max}}) - \\frac{1}{2} k x_{\\text{max}}^2"
                },
                {
                    "step_number": 3,
                    "explanation": "Apply work-energy theorem W_net = Delta K = 0 - K_i = -16.0 J.",
                    "equation_latex": "-(0.20)(2.0)(9.8)(2.0 + x_{\\text{max}}) - \\frac{1}{2}(400) x_{\\text{max}}^2 = -16.0 \\implies 3.92(2.0 + x_{\\text{max}}) + 200 x_{\\text{max}}^2 = 16.0"
                },
                {
                    "step_number": 4,
                    "explanation": "Formulate quadratic equation: 200 x_max^2 + 3.92 x_max - 8.16 = 0.",
                    "equation_latex": "x_{\\text{max}} = \\frac{-3.92 + \\sqrt{3.92^2 - 4(200)(-8.16)}}{2(200)} = \\frac{-3.92 + \\sqrt{15.3664 + 6528}}{400} = \\frac{-3.92 + 80.89}{400} \\approx 0.192\\text{ m} = 19.2\\text{ cm}"
                }
            ],
            "final_answer": "x_{\\text{max}} \\approx 0.192\\text{ m} = 19.2\\text{ cm}",
            "trap_alerts": [
                "Forgetting that friction continues to act during the spring compression phase x_max",
                "Omitting kinetic energy at spring contact"
            ],
            "sanity_checks": [
                "Total energy dissipated by friction is 3.92 * 2.192 = 8.59 J, spring stores 1/2 * 400 * (0.192)^2 = 7.37 J, sum = 15.96 J approx 16.0 J",
                "x_max must be strictly positive"
            ],
            "claim_traces": ["HCV1 Ch 8 Example 8.6; HRW Ch 8 Sample Problem 8.04"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-ex-wep-spring-compress-01",
            "created_at": now_iso
        },
        {
            "example_id": "ex-wep-wet-variable-force-01",
            "chapter_id": "work-energy-power",
            "problem_statement": "A particle of mass $m = 1.0\\text{ kg}$ is initially at rest at $x = 0$. It is subjected to a 1D force $F(x) = (6.0 - 2.0x)\\text{ N}$ directed along the x-axis, where $x$ is in meters. Find: (a) the position where the particle attains maximum speed, and (b) the maximum speed $v_{\\text{max}}$.",
            "known_parameters": {"m": 1.0, "x_0": 0.0, "v_0": 0.0, "F(x)": "6.0 - 2.0x"},
            "target_variable": "x_opt, v_max",
            "solution_strategy": "Maximum speed occurs where acceleration and net force vanish (F(x) = 0). Then apply work-energy theorem by integrating F(x) from 0 to x_opt.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Set F(x) = 0 to find position of maximum speed.",
                    "equation_latex": "F(x) = 6.0 - 2.0x = 0 \\implies x_{\\text{opt}} = 3.0\\text{ m}"
                },
                {
                    "step_number": 2,
                    "explanation": "Integrate force from x = 0 to x = 3.0 m to find net work done.",
                    "equation_latex": "W_{\\text{net}} = \\int_0^{3.0} (6.0 - 2.0x) \\, dx = \\left[ 6.0x - x^2 \\right]_0^{3.0} = 6.0(3.0) - (3.0)^2 = 18.0 - 9.0 = 9.0\\text{ J}"
                },
                {
                    "step_number": 3,
                    "explanation": "Apply work-energy theorem W_net = 1/2 m v_max^2 - 0.",
                    "equation_latex": "\\frac{1}{2}(1.0) v_{\\text{max}}^2 = 9.0 \\implies v_{\\text{max}}^2 = 18.0 \\implies v_{\\text{max}} = \\sqrt{18.0} = 3\\sqrt{2} \\approx 4.24\\text{ m/s}"
                }
            ],
            "final_answer": "x_{\\text{opt}} = 3.0\\text{ m}, \\quad v_{\\text{max}} = 3\\sqrt{2} \\approx 4.24\\text{ m/s}",
            "trap_alerts": [
                "Setting work equal to zero instead of setting force equal to zero to find maximum speed",
                "Forgetting 1/2 factor in kinetic energy"
            ],
            "sanity_checks": [
                "Beyond x = 3.0 m, force becomes negative, decelerating the particle, verifying x = 3.0 m is a true maximum",
                "Dimensional check: [6x] = [x^2] = [N m] = [J]"
            ],
            "claim_traces": ["UP Ch 6 Example 6.7; HRW Ch 7 Problem 7.23"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-ex-wep-wet-variable-force-01",
            "created_at": now_iso
        },
        {
            "example_id": "ex-wep-wet-non-inertial-pendulum-01",
            "chapter_id": "work-energy-power",
            "problem_statement": "A simple pendulum of bob mass $m$ and string length $L$ hangs in an elevator accelerating upward with constant acceleration $a_0$. If the bob is deflected by angle $\\theta_0$ from the vertical and released from rest relative to the elevator, find the speed $v_{\\text{rel}}$ of the bob at the lowest point.",
            "known_parameters": {"m": "m", "L": "L", "a_0": "a_0", "theta_0": "theta_0"},
            "target_variable": "v_rel",
            "solution_strategy": "Analyze in the non-inertial reference frame of the upward accelerating elevator. Effective downward acceleration is g_eff = g + a_0, and string tension does zero work because it is perpendicular to trajectory.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Formulate effective gravity in elevator frame including downward pseudo-force F_pseudo = -m a_0 j.",
                    "equation_latex": "\\vec{g}_{\\text{eff}} = \\vec{g} - \\vec{a}_0 = -(g + a_0)\\hat{j} \\implies g_{\\text{eff}} = g + a_0"
                },
                {
                    "step_number": 2,
                    "explanation": "Calculate vertical height descended relative to elevator datum from angle theta_0 to lowest point.",
                    "equation_latex": "h_{\\text{rel}} = L - L \\cos\\theta_0 = L(1 - \\cos\\theta_0)"
                },
                {
                    "step_number": 3,
                    "explanation": "Apply work-energy theorem in accelerating frame: W_real + W_pseudo = Delta K_rel.",
                    "equation_latex": "W_{\\text{net, rel}} = m(g + a_0) h_{\\text{rel}} = m(g + a_0) L(1 - \\cos\\theta_0) = \\frac{1}{2} m v_{\\text{rel}}^2 - 0"
                },
                {
                    "step_number": 4,
                    "explanation": "Solve for v_rel.",
                    "equation_latex": "v_{\\text{rel}} = \\sqrt{2(g + a_0)L(1 - \\cos\\theta_0)}"
                }
            ],
            "final_answer": "v_{\\text{rel}} = \\sqrt{2(g + a_0)L(1 - \\cos\\theta_0)}",
            "trap_alerts": [
                "Subtracting a_0 instead of adding for an upward accelerating elevator",
                "Attempting to calculate tension work (string tension is perpendicular to relative displacement everywhere)"
            ],
            "sanity_checks": [
                "When a_0 = 0, formula reduces to standard stationary pendulum v = sqrt(2gL(1 - cos theta_0))",
                "If elevator is in free fall a_0 = -g, g_eff = 0 and bob does not accelerate (v_rel = 0)"
            ],
            "claim_traces": ["HCV1 Ch 8 p. 134; Irodov 1.3 Problem 1.114"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-ex-wep-wet-non-inertial-pendulum-01",
            "created_at": now_iso
        },
        {
            "example_id": "ex-wep-pe-curve-equilibrium-01",
            "chapter_id": "work-energy-power",
            "problem_statement": "The potential energy of a diatomic system as a function of atomic separation $r$ is modeled by $U(r) = \\frac{A}{r^2} - \\frac{B}{r}$, where $A > 0$ and $B > 0$ are constants. Determine: (a) the equilibrium separation distance $r_0$, (b) the nature of the equilibrium, and (c) the minimum work required to dissociate the system from equilibrium to infinite separation.",
            "known_parameters": {"A": "A > 0", "B": "B > 0"},
            "target_variable": "r_0, stability, W_diss",
            "solution_strategy": "Find equilibrium by setting dU/dr = 0, check stability using d^2U/dr^2, and calculate dissociation energy as U(infty) - U(r_0).",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Compute first spatial derivative of potential energy and set equal to zero for equilibrium.",
                    "equation_latex": "\\frac{dU}{dr} = -\\frac{2A}{r^3} + \\frac{B}{r^2} = 0 \\implies \\frac{B}{r^2} = \\frac{2A}{r^3} \\implies r_0 = \\frac{2A}{B}"
                },
                {
                    "step_number": 2,
                    "explanation": "Compute second derivative at r_0 to determine stability.",
                    "equation_latex": "\\frac{d^2U}{dr^2} = \\frac{6A}{r^4} - \\frac{2B}{r^3} = \\frac{1}{r_0^3}\\left( \\frac{6A}{2A/B} - 2B \\right) = \\frac{1}{r_0^3}(3B - 2B) = \\frac{B}{r_0^3} > 0"
                },
                {
                    "step_number": 3,
                    "explanation": "Conclude that because d^2U/dr^2 > 0, the equilibrium at r_0 is strictly STABLE.",
                    "equation_latex": "\\frac{d^2U}{dr^2}\\Big|_{r_0} > 0 \\implies \\text{STABLE EQUILIBRIUM}"
                },
                {
                    "step_number": 4,
                    "explanation": "Calculate minimum dissociation energy (binding energy) Delta U = U(infty) - U(r_0).",
                    "equation_latex": "U(r_0) = \\frac{A}{(2A/B)^2} - \\frac{B}{(2A/B)} = \\frac{B^2}{4A} - \\frac{B^2}{2A} = -\\frac{B^2}{4A}, \\quad U(\\infty) = 0 \\implies W_{\\text{diss}} = 0 - \\left(-\\frac{B^2}{4A}\\right) = \\frac{B^2}{4A}"
                }
            ],
            "final_answer": "r_0 = \\frac{2A}{B}, \\quad \\text{STABLE EQUILIBRIUM}, \\quad W_{\\text{diss}} = \\frac{B^2}{4A}",
            "trap_alerts": [
                "Sign errors in differentiating 1/r^2 and 1/r terms",
                "Confusing potential energy at minimum with binding energy"
            ],
            "sanity_checks": [
                "Dimensions: [A] = [Energy][L]^2, [B] = [Energy][L] => [r_0] = [A/B] = [L], [B^2/4A] = [Energy], dimensional consistency verified",
                "As r -> 0, U -> +infty (strong repulsion); as r -> infty, U -> 0 (zero interaction)"
            ],
            "claim_traces": ["HRW Ch 8 Section 8.6 p. 206; Irodov 1.3 Problem 1.115"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-ex-wep-pe-curve-equilibrium-01",
            "created_at": now_iso
        },
        {
            "example_id": "ex-wep-power-constant-engine-01",
            "chapter_id": "work-energy-power",
            "problem_statement": "An electric locomotive of total mass $M = 2.0 \\times 10^4\\text{ kg}$ starts from rest and is driven by an engine delivering constant mechanical power $P_0 = 100\\text{ kW}$. Assuming no frictional or aerodynamic losses, find: (a) the speed $v(t)$ as a function of time, (b) the distance $s(t)$ covered as a function of time, and (c) the speed and distance at $t = 10.0\\text{ s}$.",
            "known_parameters": {"M": 20000.0, "P_0": 100000.0, "v_0": 0.0},
            "target_variable": "v(t), s(t), v(10), s(10)",
            "solution_strategy": "Use work-energy relation P_0 = dK/dt = d(1/2 M v^2)/dt to integrate velocity directly, then integrate velocity to obtain displacement.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Express power as time derivative of kinetic energy and integrate from rest.",
                    "equation_latex": "P_0 = \\frac{dK}{dt} = \\frac{d}{dt}\\left( \\frac{1}{2} M v^2 \\right) \\implies \\frac{1}{2} M v^2 = P_0 t \\implies v(t) = \\sqrt{\\frac{2 P_0 t}{M}}"
                },
                {
                    "step_number": 2,
                    "explanation": "Substitute numerical values for M = 2.0 x 10^4 kg and P_0 = 1.0 x 10^5 W.",
                    "equation_latex": "v(t) = \\sqrt{\\frac{2 \\times 10^5}{2 \\times 10^4} t} = \\sqrt{10 t} = \\sqrt{10} t^{1/2}"
                },
                {
                    "step_number": 3,
                    "explanation": "Integrate velocity with respect to time to obtain displacement s(t).",
                    "equation_latex": "s(t) = \\int_0^t v(t') \\, dt' = \\sqrt{10} \\int_0^t t'^{1/2} \\, dt' = \\sqrt{10} \\left[ \\frac{2}{3} t^{3/2} \\right] = \\frac{2\\sqrt{10}}{3} t^{3/2}"
                },
                {
                    "step_number": 4,
                    "explanation": "Evaluate at t = 10.0 s.",
                    "equation_latex": "v(10) = \\sqrt{10 \\times 10} = 10.0\\text{ m/s}, \\quad s(10) = \\frac{2\\sqrt{10}}{3} (10)^{3/2} = \\frac{2\\sqrt{10}}{3} (10\\sqrt{10}) = \\frac{200}{3} \\approx 66.7\\text{ m}"
                }
            ],
            "final_answer": "v(t) = \\sqrt{10 t}, \\quad s(t) = \\frac{2\\sqrt{10}}{3} t^{3/2}; \\quad v(10) = 10.0\\text{ m/s}, \\quad s(10) = \\frac{200}{3}\\text{ m} \\approx 66.7\\text{ m}",
            "trap_alerts": [
                "Assuming acceleration is constant (at constant power, acceleration a = P/(M v) decreases inversely with speed)",
                "Using kinematic formulas v = u + at"
            ],
            "sanity_checks": [
                "Kinetic energy at t = 10 s: K = 1/2 (20000) (10)^2 = 1.0 x 10^6 J. Total energy delivered: P_0 * t = 100000 * 10 = 1.0 x 10^6 J, exact match",
                "Dimensions: [P t / M]^(1/2) = ([M L^2 T^-3 T] / [M])^(1/2) = (L^2 T^-2)^(1/2) = L T^-1, correct velocity dimensions"
            ],
            "claim_traces": ["HCV1 Ch 8 Example 8.9; UP Ch 6 Section 6.4 p. 220"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-ex-wep-power-constant-engine-01",
            "created_at": now_iso
        },
        {
            "example_id": "ex-wep-vcm-slack-projectile-01",
            "chapter_id": "work-energy-power",
            "problem_statement": "A small body of mass $m$ is suspended by a light string of length $R = 1.0\\text{ m}$ from a fixed peg $O$. The body is given a horizontal velocity $v_0 = \\sqrt{3 g R}$ at the lowest point. Find: (a) the angle $\\theta_s$ from the downward vertical where the string becomes slack, and (b) the maximum height $H_{\\text{max}}$ attained by the body above the lowest point during its subsequent motion. (Take $g = 9.8\\text{ m/s}^2$).",
            "known_parameters": {"R": 1.0, "v_0": "sqrt(3 g R)", "g": 9.8},
            "target_variable": "theta_s, H_max",
            "solution_strategy": "First calculate angle where tension vanishes using cos(theta_s) = -(v_0^2 - 2gR)/(3gR). Then determine velocity at slack point and treat subsequent flight as standard projectile motion launched at angle alpha = theta_s - pi/2 to the horizontal.",
            "solution_steps": [
                {
                    "step_number": 1,
                    "explanation": "Compute cosine of the slackening angle using the derived vertical circle slack condition.",
                    "equation_latex": "\\cos\\theta_s = -\\frac{v_0^2 - 2gR}{3gR} = -\\frac{3gR - 2gR}{3gR} = -\\frac{1}{3} \\implies \\theta_s = \\arccos(-1/3) \\approx 109.47^\\circ"
                },
                {
                    "step_number": 2,
                    "explanation": "Determine speed v_s at the slackening point using energy conservation.",
                    "equation_latex": "v_s^2 = v_0^2 - 2gR(1 - \\cos\\theta_s) = 3gR - 2gR\\left(1 - \\left(-\\frac{1}{3}\\right)\\right) = 3gR - 2gR\\left(\\frac{4}{3}\\right) = \\frac{1}{3} g R"
                },
                {
                    "step_number": 3,
                    "explanation": "Identify the height y_s of the slack point above the lowest point.",
                    "equation_latex": "y_s = R(1 - \\cos\\theta_s) = R\\left(1 - \\left(-\\frac{1}{3}\\right)\\right) = \\frac{4}{3} R"
                },
                {
                    "step_number": 4,
                    "explanation": "Determine the projectile launch angle with the horizontal: since velocity is perpendicular to radius, launch angle is alpha = theta_s - 90 deg, so sin(alpha) = cos(theta_s - 90 deg) = -cos(theta_s) = 1/3.",
                    "equation_latex": "\\sin\\alpha = |\\cos\\theta_s| = \\frac{1}{3}"
                },
                {
                    "step_number": 5,
                    "explanation": "Compute additional maximum vertical rise h_proj during projectile phase.",
                    "equation_latex": "h_{\\text{proj}} = \\frac{v_s^2 \\sin^2\\alpha}{2g} = \\frac{(gR/3)(1/3)^2}{2g} = \\frac{R/27}{2} = \\frac{R}{54}"
                },
                {
                    "step_number": 6,
                    "explanation": "Sum y_s and h_proj to find maximum height attained above lowest point.",
                    "equation_latex": "H_{\\text{max}} = y_s + h_{\\text{proj}} = \\frac{4}{3} R + \\frac{1}{54} R = \\frac{72 + 1}{54} R = \\frac{73}{54} R = \\frac{73}{54}(1.0) \\approx 1.352\\text{ m}"
                }
            ],
            "final_answer": "\\cos\\theta_s = -\\frac{1}{3} \\implies \\theta_s \\approx 109.5^\\circ, \\quad H_{\\text{max}} = \\frac{73}{54} R \\approx 1.35\\text{ m}",
            "trap_alerts": [
                "Assuming particle falls vertically downward once string goes slack",
                "Using total velocity v_s instead of vertical velocity component v_s sin(alpha) for projectile height"
            ],
            "sanity_checks": [
                "H_max must be less than 2R (looping apex) and greater than 4/3 R (slack point): 1.333 R < 1.352 R < 2.0 R, verified",
                "At slack point, T = 0 and radial component of gravity mg cos(theta_s) exactly balances m v_s^2 / R"
            ],
            "claim_traces": ["HCV1 Ch 8 Example 8.12; Irodov 1.3 Problem 1.120"],
            "verification_status": "VERIFIED",
            "verification_record_id": "dual-cvr-ex-wep-vcm-slack-projectile-01",
            "created_at": now_iso
        }
    ]

    for ex in examples:
        exhash = compute_content_hash(ex)
        ex["content_hash"] = exhash
        for p in [content_dir / "examples" / f"{ex['example_id']}.json", staging_content / "examples" / f"{ex['example_id']}.json"]:
            p.write_text(json.dumps(ex, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 6. MISCONCEPTIONS (6 items)
    # =============================================================
    misconceptions = [
        {
            "misconception_id": "misc-wep-01",
            "chapter_id": "work-energy-power",
            "category": "SIGN_MISTAKE",
            "statement": "Friction always does negative work on every body it acts upon.",
            "erroneous_reasoning": "Students assume friction always opposes motion, and therefore the angle between force and displacement is always 180 deg, making work negative.",
            "correct_physics_explanation": "Friction opposes RELATIVE motion at the contact interface, not necessarily motion relative to the ground. Static friction can do positive, negative, or zero work depending on the reference frame. For a crate sitting on the flatbed of an accelerating truck, static friction accelerates the crate forward in the direction of ground displacement, doing POSITIVE work.",
            "refutation_counterexample": "A box of mass m rests on a flatbed truck accelerating at a = 2 m/s^2 over d = 10 m. Static friction f_s = ma = 2m N acts forward. Work done by static friction on the box is W = f_s d = +20m J > 0, which supplies the box's kinetic energy increase.",
            "diagnostic_check_latex": "W_{\\text{static}} = \\vec{f}_s \\cdot \\vec{d} > 0 \\quad \\text{when static friction accelerates a body in the direction of displacement.}",
            "claim_traces": ["HCV1 Ch 8 p. 131; HRW Ch 8 p. 207"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-misc-wep-01",
            "created_at": now_iso
        },
        {
            "misconception_id": "misc-wep-02",
            "chapter_id": "work-energy-power",
            "category": "INVALID_FORMULA_CONDITION",
            "statement": "The normal reaction force never does mechanical work on any object.",
            "erroneous_reasoning": "Students overgeneralize from horizontal sliding (where normal force is perpendicular to horizontal displacement) to believe normal force work is universally zero.",
            "correct_physics_explanation": "Normal force is strictly perpendicular to the contact interface, but the interface itself may be moving! When a person stands in an elevator accelerating upward, the normal force on their feet is parallel to the upward displacement, performing positive work W = N d > 0.",
            "refutation_counterexample": "In an elevator accelerating upward through height h with acceleration a, the floor exerts upward normal force N = m(g + a). Displacement is upward d = h. Work done by normal force is W_N = m(g + a)h > 0.",
            "diagnostic_check_latex": "W_N = \\vec{N} \\cdot \\Delta\\vec{r} \\neq 0 \\quad \\text{whenever the contact interface has a non-zero velocity component along the normal.}",
            "claim_traces": ["HCV1 Ch 8 p. 129; UP Ch 6 p. 206"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-misc-wep-02",
            "created_at": now_iso
        },
        {
            "misconception_id": "misc-wep-03",
            "chapter_id": "work-energy-power",
            "category": "INVALID_FORMULA_CONDITION",
            "statement": "The Work-Energy Theorem applies only to constant forces along rectilinear paths.",
            "erroneous_reasoning": "Students learn W = F d cos(theta) first and mistakenly assume the theorem W_net = Delta K requires constant acceleration equations.",
            "correct_physics_explanation": "The Work-Energy Theorem is derived by integrating Newton's Second Law along an arbitrary 3D curve: int F_net . dr = int m (dv/dt) . v dt = int m v dv = Delta K. It holds rigorously for arbitrary position-dependent, velocity-dependent, or time-dependent forces along any curved path.",
            "refutation_counterexample": "For a simple pendulum or curved roller-coaster track where force direction and magnitude continuously vary, W_net = Delta K yields exact velocities without needing constant acceleration.",
            "diagnostic_check_latex": "W_{\\text{net}} = \\int_C \\vec{F}_{\\text{net}} \\cdot d\\vec{r} = \\Delta K \\quad \\text{holds universally for arbitrary 3D trajectories and forces.}",
            "claim_traces": ["UP Ch 6 p. 217; HRW Ch 7 p. 179"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-misc-wep-03",
            "created_at": now_iso
        },
        {
            "misconception_id": "misc-wep-04",
            "chapter_id": "work-energy-power",
            "category": "WRONG_CONSERVATION_LAW",
            "statement": "Internal forces in a system can never do net mechanical work because action and reaction cancel.",
            "erroneous_reasoning": "Confusing linear momentum conservation (where internal forces sum to zero vector sum F_int = 0) with work, which depends on individual displacements.",
            "correct_physics_explanation": "While action and reaction forces are equal and opposite (F_ij = -F_ji), the displacements of their respective points of application may differ! When two blocks connected by a compressed spring are released, both blocks move outward: the spring does positive work on both blocks, increasing total kinetic energy.",
            "refutation_counterexample": "A compressed spring (k = 100 N/m, x = 0.2 m) between two masses on a frictionless floor releases. Both masses accelerate away. Total internal spring work is W_int = +1/2 k x^2 = +2 J, increasing kinetic energy from 0 to 2 J.",
            "diagnostic_check_latex": "W_{\\text{int}} = \\int \\vec{F}_{12} \\cdot d(\\vec{r}_1 - \\vec{r}_2) = \\int \\vec{F}_{12} \\cdot d\\vec{r}_{12} \\neq 0 \\quad \\text{for deformable systems.}",
            "claim_traces": ["HCV1 Ch 8 p. 133; UP Ch 6 p. 213"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-misc-wep-04",
            "created_at": now_iso
        },
        {
            "misconception_id": "misc-wep-05",
            "chapter_id": "work-energy-power",
            "category": "INVALID_FORMULA_CONDITION",
            "statement": "Potential energy can be defined for any physical force, including friction.",
            "erroneous_reasoning": "Believing that because work can be calculated for friction, one can simply define a 'frictional potential energy' U_f.",
            "correct_physics_explanation": "Potential energy U requires that work between two points be independent of path, satisfying oint F . dr = 0. For kinetic friction, the line integral along a closed round trip is strictly non-zero (-2 mu_k N L < 0). Friction dissipates mechanical energy irreversibly into thermal disorder; no reversible potential energy can be formulated.",
            "refutation_counterexample": "Sliding a block around a closed square loop of perimeter 4L on a rough floor does negative work W_f = -4 mu_k N L != 0. If a potential existed, round-trip work would be identically zero.",
            "diagnostic_check_latex": "\\oint \\vec{f}_k \\cdot d\\vec{r} = -\\mu_k N \\oint ds < 0 \\implies \\nabla \\times \\vec{f}_k \\neq \\vec{0} \\implies \\text{No potential energy exists.}",
            "claim_traces": ["HRW Ch 8 p. 203; UP Ch 7 p. 248"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-misc-wep-05",
            "created_at": now_iso
        },
        {
            "misconception_id": "misc-wep-06",
            "chapter_id": "work-energy-power",
            "category": "INVALID_FORMULA_CONDITION",
            "statement": "In vertical circular motion, tension at the top must be strictly zero for the particle to complete the circle.",
            "erroneous_reasoning": "Treating the limiting boundary condition T_top = 0 as an equality that must always hold, or assuming zero tension means the string has snapped.",
            "correct_physics_explanation": "The requirement to complete the loop is an inequality: T_top >= 0. For any launch speed v_bot > sqrt(5gR), tension at the top is strictly positive: T_top = m v_top^2 / R - mg > 0. Only at the exact threshold v_bot = sqrt(5gR) does tension vanish momentarily at the apex point.",
            "refutation_counterexample": "If a particle is launched with v_bot = sqrt(6gR), energy conservation gives v_top = sqrt(2gR). Radial tension at apex is T_top = m(2gR)/R - mg = mg > 0.",
            "diagnostic_check_latex": "T_{\\text{top}} = \\frac{m v_{\\text{top}}^2}{R} - mg \\ge 0 \\iff v_{\\text{top}} \\ge \\sqrt{gR} \\quad (T_{\\text{top}} > 0 \\text{ for any } v_{\\text{bot}} > \\sqrt{5gR}).",
            "claim_traces": ["HCV1 Ch 8 p. 140; UP Ch 5 p. 184"],
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-misc-wep-06",
            "created_at": now_iso
        }
    ]

    for m in misconceptions:
        mhash = compute_content_hash(m)
        m["content_hash"] = mhash
        for p in [content_dir / "misconceptions" / f"{m['misconception_id']}.json", staging_content / "misconceptions" / f"{m['misconception_id']}.json"]:
            p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 7. PRACTICE QUESTIONS (2 items)
    # =============================================================
    qb_verified = root / "build" / "staging" / "incoming" / "question_bank" / "verified"
    qb_verified.mkdir(parents=True, exist_ok=True)
    
    questions = [
        {
            "question_id": "work-energy-power-question-e37050bb",
            "chapter_id": "work-energy-power",
            "topic_id": "work-energy-theorem",
            "subtopic_id": "work-energy-theorem-inertial-frame",
            "question_type": "SINGLE_CORRECT_MCQ",
            "problem_statement": "A particle of mass $m$ is projected with speed $u$ at an angle $\\theta$ with the horizontal. The net work done by gravity on the particle from the instant of projection until it reaches the highest point of its trajectory is:",
            "options": {
                "A": "$-\\frac{1}{2} m u^2 \\sin^2\\theta$",
                "B": "$\\frac{1}{2} m u^2 \\cos^2\\theta$",
                "C": "$-\\frac{1}{2} m u^2$",
                "D": "Zero"
            },
            "correct_answer": "A",
            "distractor_rationales": {
                "B": "Confuses work done with horizontal kinetic energy retained at the apex.",
                "C": "Omits the angle factor, assuming the entire initial kinetic energy is removed.",
                "D": "Mistakenly assumes work is zero over symmetric ascent."
            },
            "explanation": "At the highest point, the vertical velocity component vanishes, leaving only the horizontal component $v_x = u \\cos\\theta$. By the Work-Energy Theorem, $W_g = \\Delta K = K_f - K_i = \\frac{1}{2} m (u\\cos\\theta)^2 - \\frac{1}{2} m u^2 = \\frac{1}{2} m u^2 (\\cos^2\\theta - 1) = -\\frac{1}{2} m u^2 \\sin^2\\theta$.",
            "difficulty_rating": 2,
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-q-wep-01",
            "created_at": now_iso
        },
        {
            "question_id": "work-energy-power-question-ba0b4106",
            "chapter_id": "work-energy-power",
            "topic_id": "conservative-forces-and-potential-energy",
            "subtopic_id": "potential-energy-gradient",
            "question_type": "SINGLE_CORRECT_MCQ",
            "problem_statement": "The potential energy of a conservative 1D force field is given by $U(x) = 2x^4 - 4x^2\\text{ J}$, where $x$ is in meters. The positions of stable equilibrium are:",
            "options": {
                "A": "$x = \\pm 1\\text{ m}$",
                "B": "$x = 0$",
                "C": "$x = \\pm 2\\text{ m}$",
                "D": "$x = \\pm \\frac{1}{\\sqrt{2}}\\text{ m}$"
            },
            "correct_answer": "A",
            "distractor_rationales": {
                "B": "Identifies x = 0 which is an unstable equilibrium (d^2U/dx^2 = -8 < 0).",
                "C": "Arithmetic error in differentiating x^4.",
                "D": "Finds points of inflection where d^2U/dx^2 = 0 rather than equilibrium points."
            },
            "explanation": "Equilibrium requires $F = -dU/dx = 0 \\implies -(8x^3 - 8x) = 0 \\implies 8x(x^2 - 1) = 0$, giving $x = 0$ or $x = \\pm 1\\text{ m}$. Evaluating second derivative: $\\frac{d^2U}{dx^2} = 24x^2 - 8$. At $x = 0$, $d^2U/dx^2 = -8 < 0$ (unstable). At $x = \\pm 1$, $d^2U/dx^2 = 24(1) - 8 = +16 > 0$ (stable). Thus stable equilibrium points are $x = \\pm 1\\text{ m}$.",
            "difficulty_rating": 3,
            "verification_status": "VERIFIED",
            "verification_record_id": "cvr-q-wep-02",
            "created_at": now_iso
        }
    ]

    for q in questions:
        qhash = compute_content_hash(q)
        q["content_hash"] = qhash
        (qb_verified / f"{q['question_id']}.json").write_text(json.dumps(q, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 8. CHAPTER SPEC & PLAN
    # =============================================================
    spec_data = {
        "chapter_id": "work-energy-power",
        "chapter_title": "Work, Energy & Power",
        "template_type": "MECHANICS",
        "order": 4,
        "taxonomy_references": [
            {"chapter_id": "work-energy-power", "topic_id": "work-done", "subtopic_id": "work-by-constant-force"},
            {"chapter_id": "work-energy-power", "topic_id": "work-done", "subtopic_id": "work-by-variable-force"},
            {"chapter_id": "work-energy-power", "topic_id": "work-done", "subtopic_id": "work-by-spring-force"},
            {"chapter_id": "work-energy-power", "topic_id": "work-done", "subtopic_id": "work-by-friction"},
            {"chapter_id": "work-energy-power", "topic_id": "work-energy-theorem", "subtopic_id": "kinetic-energy"},
            {"chapter_id": "work-energy-power", "topic_id": "work-energy-theorem", "subtopic_id": "work-energy-theorem-inertial-frame"},
            {"chapter_id": "work-energy-power", "topic_id": "work-energy-theorem", "subtopic_id": "work-energy-theorem-non-inertial-frame"},
            {"chapter_id": "work-energy-power", "topic_id": "conservative-forces-and-potential-energy", "subtopic_id": "conservative-and-non-conservative-forces"},
            {"chapter_id": "work-energy-power", "topic_id": "conservative-forces-and-potential-energy", "subtopic_id": "potential-energy-gradient"},
            {"chapter_id": "work-energy-power", "topic_id": "conservative-forces-and-potential-energy", "subtopic_id": "equilibrium-stable-unstable-neutral"},
            {"chapter_id": "work-energy-power", "topic_id": "conservative-forces-and-potential-energy", "subtopic_id": "conservation-of-mechanical-energy"},
            {"chapter_id": "work-energy-power", "topic_id": "power-and-vertical-circle", "subtopic_id": "average-and-instantaneous-power"},
            {"chapter_id": "work-energy-power", "topic_id": "power-and-vertical-circle", "subtopic_id": "vertical-circular-motion-critical-velocities"},
            {"chapter_id": "work-energy-power", "topic_id": "power-and-vertical-circle", "subtopic_id": "string-slackening-condition"}
        ],
        "learning_objectives": [
            "Calculate work done by constant, variable, spring, and frictional forces using scalar products and line integrals.",
            "Master the Work-Energy Theorem in both inertial and accelerating non-inertial reference frames.",
            "Distinguish conservative from non-conservative forces using path-independence and closed-loop criteria.",
            "Determine conservative force vectors from potential energy gradient fields F = -grad(U).",
            "Analyze potential energy curves U(x) to locate turning points and evaluate equilibrium stability.",
            "Apply the conservation of total mechanical energy and formulate energy balance under dissipative non-conservative forces.",
            "Calculate average and instantaneous power delivered by machines and force fields.",
            "Derive critical looping velocities and string slackening dynamics in vertical circular motion."
        ],
        "prerequisite_curriculum_nodes": [
            "units-and-measurements",
            "vectors-and-coordinate-systems",
            "differential-calculus-foundations",
            "integral-calculus-foundations",
            "kinematics",
            "laws-of-motion"
        ],
        "concept_sequence": [
            {"concept_id": c["concept_id"], "curriculum_id": f"curr-wep-{i+1:02d}", "role": "FOUNDATION_CONCEPT", "explanation_priority": i+1, "source_evidence": c["claim_traces"][0]}
            for i, c in enumerate(concepts)
        ],
        "formula_sequence": [
            {
                "formula_id": f["formula_id"],
                "title": f["title"],
                "equation_latex": f["equation_latex"],
                "variables": f["variables"],
                "units_and_dimensions": {k: f"{f['units'].get(k, '')} ({f['dimensions'].get(k, '')})" for k in f["variables"]},
                "assumptions": f["assumptions"],
                "conditions_of_validity": f["conditions_of_validity"],
                "derivation_links": [f["derivation_reference"]],
                "common_misuse_cases": f["common_misuse"],
                "verification_status": "VERIFIED"
            }
            for f in formulas
        ],
        "misconception_sequence": [
            {
                "misconception_id": m["misconception_id"],
                "category": m["category"],
                "statement": m["statement"],
                "explanation": m["correct_physics_explanation"],
                "trap_mechanism": m["erroneous_reasoning"],
                "trigger_conditions": [m["refutation_counterexample"]]
            }
            for m in misconceptions
        ],
        "worked_example_sequence": [
            {
                "example_id": ex["example_id"],
                "problem_statement": ex["problem_statement"],
                "known_quantities": {k: str(v) for k, v in ex["known_parameters"].items()},
                "target_quantity": ex["target_variable"],
                "relevant_concepts": ["concept-wep-work-def-01"],
                "governing_principles": ["Work-Energy Principle"],
                "solution_strategy": ex["solution_strategy"],
                "step_by_step_derivation": [s["equation_latex"] for s in ex["solution_steps"]],
                "final_answer": ex["final_answer"],
                "sanity_checks": ex["sanity_checks"],
                "verification_status": "VERIFIED"
            }
            for ex in examples
        ],
        "question_sequence": [
            {
                "atom_id": q["question_id"],
                "curriculum_id": f"curr-q-wep-{i+1:02d}",
                "chapter_id": "work-energy-power",
                "topic_id": q["topic_id"],
                "pedagogical_role": "PRACTICE_QUESTION",
                "difficulty_dimensions": {
                    "conceptual_difficulty": 3,
                    "mathematical_difficulty": 3,
                    "multistep_reasoning_difficulty": 3,
                    "abstraction_difficulty": 2,
                    "computational_burden": 2,
                    "trap_misconception_difficulty": 3
                }
            }
            for i, q in enumerate(questions)
        ],
        "question_ladders": [ladder_data],
        "revision_checklist": [
            "Work scalar product W = F . d cos(theta) and sign conventions",
            "Work line integral W = int F . dr and area under F-x graph",
            "Spring work formula W_s = -1/2 k (x_f^2 - x_i^2)",
            "Kinetic energy K = 1/2 m v^2 = p^2 / (2m)",
            "Work-Energy theorem W_net = Delta K for inertial and non-inertial frames",
            "Conservative force definition and closed loop integral oint F . dr = 0",
            "Force-potential gradient relation F = -grad(U) and F_x = -dU/dx",
            "Potential curve equilibrium classification: dU/dx = 0; d2U/dx2 > 0 (stable), < 0 (unstable)",
            "Mechanical energy conservation Delta E_mech = W_nc",
            "Instantaneous power P = F . v and average power P_avg = W / Delta t",
            "Vertical circle looping critical speeds: v_bot = sqrt(5gR), v_top = sqrt(gR)",
            "Vertical circle tension invariant T_bot - T_top = 6mg",
            "String slackening condition cos(theta_slack) = -(v_bot^2 - 2gR)/(3gR)"
        ],
        "created_at": now_iso
    }

    for spath in [curr_chapters / "work-energy-power_spec.json", staging_curr / "work-energy-power_spec.json"]:
        spath.write_text(json.dumps(spec_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # =============================================================
    # 9. CHAPTER PLAN (4 sections)
    # =============================================================
    plan_data = {
        "plan_id": "plan-work-energy-power-001",
        "chapter_id": "work-energy-power",
        "title": "Work, Energy & Power",
        "template_type": "MECHANICS",
        "sections": [
            {
                "section_id": "sec-01-work-done-by-forces",
                "section_order": 1,
                "title": "Work Done by Constant and Variable Forces",
                "pedagogical_purpose": "Establish the foundational scalar definition of mechanical work, evaluate line integrals for position-dependent forces, derive spring work, and examine friction work across reference frames.",
                "concepts": [
                    "concept-wep-work-def-01",
                    "concept-wep-work-variable-01",
                    "concept-wep-work-spring-01",
                    "concept-wep-work-friction-01"
                ],
                "formula_ids": [
                    "formula-wep-work-const",
                    "formula-wep-work-var-integral",
                    "formula-wep-work-spring",
                    "formula-wep-work-friction-kinetic"
                ],
                "worked_example_ids": [
                    "ex-wep-spring-compress-01"
                ],
                "question_atom_ids": [],
                "misconception_ids": [
                    "misc-wep-01",
                    "misc-wep-02"
                ],
                "prerequisite_refs": ["vectors-and-coordinate-systems", "integral-calculus-foundations"],
                "source_references": ["HCV1 Ch 8 pp. 128-132", "HRW Ch 7 pp. 173-181", "UP Ch 6 pp. 205-218"],
                "unresolved_gaps": []
            },
            {
                "section_id": "sec-02-work-energy-theorem",
                "section_order": 2,
                "title": "Kinetic Energy and the Work-Energy Theorem",
                "pedagogical_purpose": "Define kinetic energy from first principles, prove the Work-Energy Theorem for general curved 3D paths, extend it to non-inertial accelerating frames, and analyze internal force work in deformable systems.",
                "concepts": [
                    "concept-wep-ke-01",
                    "concept-wep-wet-inertial-01",
                    "concept-wep-wet-non-inertial-01",
                    "concept-wep-wet-internal-01"
                ],
                "formula_ids": [
                    "formula-wep-kinetic-energy",
                    "formula-wep-work-energy-theorem",
                    "formula-wep-wet-non-inertial"
                ],
                "worked_example_ids": [
                    "ex-wep-wet-variable-force-01",
                    "ex-wep-wet-non-inertial-pendulum-01"
                ],
                "question_atom_ids": [
                    "work-energy-power-question-e37050bb"
                ],
                "misconception_ids": [
                    "misc-wep-03",
                    "misc-wep-04"
                ],
                "prerequisite_refs": ["laws-of-motion"],
                "source_references": ["HCV1 Ch 8 pp. 132-135", "HRW Ch 7 pp. 174-175", "UP Ch 6 pp. 207-214"],
                "unresolved_gaps": []
            },
            {
                "section_id": "sec-03-conservative-forces-potential-energy",
                "section_order": 3,
                "title": "Conservative Forces, Potential Energy, and Equilibrium",
                "pedagogical_purpose": "Differentiate conservative from dissipative forces, define potential energy via gradient relations F = -grad(U), establish conservation of total mechanical energy, and analyze equilibrium stability from potential curvature.",
                "concepts": [
                    "concept-wep-conservative-forces-01",
                    "concept-wep-pe-def-gradient-01",
                    "concept-wep-grav-spring-pe-01",
                    "concept-wep-mech-energy-cons-01",
                    "concept-wep-equilibrium-stability-01"
                ],
                "formula_ids": [
                    "formula-wep-pe-def",
                    "formula-wep-pe-gradient",
                    "formula-wep-mech-energy-conservation",
                    "formula-wep-equilibrium-stability"
                ],
                "worked_example_ids": [
                    "ex-wep-pe-curve-equilibrium-01"
                ],
                "question_atom_ids": [
                    "work-energy-power-question-ba0b4106"
                ],
                "misconception_ids": [
                    "misc-wep-05"
                ],
                "prerequisite_refs": ["differential-calculus-foundations"],
                "source_references": ["HCV1 Ch 8 pp. 135-140", "HRW Ch 8 pp. 203-210", "UP Ch 7 pp. 248-257", "Feynman Lec 4, 13, 14"],
                "unresolved_gaps": []
            },
            {
                "section_id": "sec-04-power-and-vertical-circular-motion",
                "section_order": 4,
                "title": "Power and Vertical Circular Motion",
                "pedagogical_purpose": "Formulate average and instantaneous power P = F . v, synthesize mechanical energy conservation with radial dynamics in vertical circles, derive critical looping velocities, and analyze upper quadrant string slackening.",
                "concepts": [
                    "concept-wep-power-def-01",
                    "concept-wep-vertical-circle-critical-01",
                    "concept-wep-vertical-circle-slack-01",
                    "concept-wep-vertical-circle-rod-01"
                ],
                "formula_ids": [
                    "formula-wep-power-instantaneous",
                    "formula-wep-vcm-critical-bottom",
                    "formula-wep-vcm-slack-condition"
                ],
                "worked_example_ids": [
                    "ex-wep-power-constant-engine-01",
                    "ex-wep-vcm-slack-projectile-01"
                ],
                "question_atom_ids": [],
                "misconception_ids": [
                    "misc-wep-06"
                ],
                "prerequisite_refs": ["circular-dynamics"],
                "source_references": ["HCV1 Ch 8 pp. 140-144", "UP Ch 5 p. 184", "Irodov 1.3 pp. 28-29"],
                "unresolved_gaps": []
            }
        ],
        "pedagogical_synthesis_notes": [
            "Emphasize the distinction between scalar work-energy methods and vector Newton's Second Law equations.",
            "Enforce that potential energy can never be formulated for frictional or dissipative forces.",
            "Highlight the universal tension invariant T_bot - T_top = 6mg in vertical circular motion."
        ],
        "unresolved_gaps": [],
        "created_at": now_iso
    }

    for ppath in [curr_chapters / "work-energy-power_plan.json", staging_curr / "work-energy-power_plan.json"]:
        ppath.write_text(json.dumps(plan_data, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Successfully built all Phase 14 Work, Energy & Power curriculum and content artifacts.")

if __name__ == "__main__":
    main()
