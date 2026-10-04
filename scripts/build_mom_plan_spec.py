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
    dual_verif_dir = content_dir / "dual_verifications"
    
    for d in [staging_curr, staging_ladders, curr_chapters, curr_ladders, staging_verif, dual_verif_dir]:
        d.mkdir(parents=True, exist_ok=True)
        
    for sub in ["concepts", "formulas", "derivations", "examples", "misconceptions", "questions"]:
        (content_dir / sub).mkdir(parents=True, exist_ok=True)
        (staging_content / sub).mkdir(parents=True, exist_ok=True)

    now_iso = "2026-10-05T01:30:00Z"

    # =============================================================
    # 1. CHAPTER PLAN
    # =============================================================
    plan_data = {
        "plan_id": "plan-center-of-mass-001",
        "chapter_id": "center-of-mass",
        "title": "Center of Mass, Momentum, and Collisions",
        "template_type": "MECHANICS",
        "sections": [
            {
                "section_id": "sec-01-center-of-mass-dynamics",
                "section_order": 1,
                "title": "Center of Mass Calculation and System Dynamics",
                "pedagogical_purpose": "Establish discrete and continuous center of mass definitions, master negative mass cavity superposition, prove Newton's second law for a system of particles, and analyze zero-external-force internal displacements.",
                "concepts": [
                    "concept-mom-com-discrete-01",
                    "concept-mom-com-continuous-01",
                    "concept-mom-com-motion-01",
                    "concept-mom-cavity-shift-01"
                ],
                "formula_ids": [
                    "formula-mom-com-discrete",
                    "formula-mom-com-continuous",
                    "formula-mom-com-hemisphere",
                    "formula-mom-com-cone",
                    "formula-mom-com-cavity",
                    "formula-mom-com-velocity",
                    "formula-mom-com-acceleration"
                ],
                "worked_example_ids": [
                    "ex-mom-disc-cavity-01",
                    "ex-mom-man-plank-01"
                ],
                "question_atom_ids": [
                    "center-of-mass-question-e38050cc"
                ],
                "misconception_ids": [
                    "misc-mom-01"
                ],
                "prerequisite_refs": [
                    "vectors-and-coordinate-systems",
                    "integral-calculus-foundations",
                    "laws-of-motion"
                ],
                "source_references": [
                    "HCV1 Ch 9 pp. 150-157",
                    "HRW Ch 9 pp. 227-234",
                    "UP Ch 8 pp. 284-289"
                ],
                "unresolved_gaps": []
            },
            {
                "section_id": "sec-02-impulse-and-momentum",
                "section_order": 2,
                "title": "Linear Momentum and the Impulse-Momentum Theorem",
                "pedagogical_purpose": "Define system linear momentum as total mass times center of mass velocity, establish the vector impulse integral, and formulate the Impulse-Momentum Theorem distinguishing impulsive from non-impulsive interactions.",
                "concepts": [
                    "concept-mom-momentum-def-01",
                    "concept-mom-impulse-def-01",
                    "concept-mom-impulse-forces-01"
                ],
                "formula_ids": [
                    "formula-mom-momentum-vector",
                    "formula-mom-impulse-integral",
                    "formula-mom-impulse-momentum-thm"
                ],
                "worked_example_ids": [
                    "ex-mom-ball-wall-impulse-01"
                ],
                "question_atom_ids": [],
                "misconception_ids": [
                    "misc-mom-03"
                ],
                "prerequisite_refs": [
                    "laws-of-motion"
                ],
                "source_references": [
                    "HCV1 Ch 9 pp. 157-161",
                    "HRW Ch 9 pp. 238-242",
                    "UP Ch 8 pp. 267-271"
                ],
                "unresolved_gaps": []
            },
            {
                "section_id": "sec-03-conservation-and-variable-mass",
                "section_order": 3,
                "title": "Conservation of Linear Momentum and Variable Mass Systems",
                "pedagogical_purpose": "Formulate the universal Principle of Conservation of Linear Momentum along isolated coordinate axes, analyze explosive recoil dynamics, and derive variable-mass reactive thrust and Tsiolkovsky rocket flight.",
                "concepts": [
                    "concept-mom-conservation-01",
                    "concept-mom-explosion-recoil-01",
                    "concept-mom-variable-mass-01"
                ],
                "formula_ids": [
                    "formula-mom-conservation",
                    "formula-mom-recoil-velocity",
                    "formula-mom-rocket-thrust",
                    "formula-mom-rocket-tsiolkovsky"
                ],
                "worked_example_ids": [
                    "ex-mom-rocket-vertical-climb-01"
                ],
                "question_atom_ids": [],
                "misconception_ids": [
                    "misc-mom-02",
                    "misc-mom-05"
                ],
                "prerequisite_refs": [
                    "differential-calculus-foundations",
                    "work-energy-power"
                ],
                "source_references": [
                    "HCV1 Ch 9 pp. 157-163",
                    "HRW Ch 9 pp. 234-238, 254-258",
                    "UP Ch 8 pp. 271-275, 289-293"
                ],
                "unresolved_gaps": []
            },
            {
                "section_id": "sec-04-collisions-and-restitution",
                "section_order": 4,
                "title": "Collisions in One and Two Dimensions",
                "pedagogical_purpose": "Classify elastic and inelastic impact dynamics, define Newton's restitution coefficient along the line of impact, derive head-on velocity expressions and kinetic energy dissipation, analyze ballistic pendulums, and decompose 2D oblique collisions.",
                "concepts": [
                    "concept-mom-collision-types-01",
                    "concept-mom-restitution-01",
                    "concept-mom-elastic-1d-01",
                    "concept-mom-inelastic-energy-loss-01",
                    "concept-mom-inelastic-ballistic-01",
                    "concept-mom-oblique-collision-01"
                ],
                "formula_ids": [
                    "formula-mom-elastic-1d-v1",
                    "formula-mom-elastic-1d-v2",
                    "formula-mom-restitution-def",
                    "formula-mom-inelastic-energy-loss",
                    "formula-mom-oblique-angle-rebound"
                ],
                "worked_example_ids": [
                    "ex-mom-elastic-target-masses-01",
                    "ex-mom-ballistic-pendulum-01",
                    "ex-mom-oblique-two-disc-01"
                ],
                "question_atom_ids": [
                    "center-of-mass-question-ba1b4107"
                ],
                "misconception_ids": [
                    "misc-mom-04",
                    "misc-mom-06"
                ],
                "prerequisite_refs": [
                    "work-energy-power"
                ],
                "source_references": [
                    "HCV1 Ch 9 pp. 163-173",
                    "HRW Ch 9 pp. 242-254",
                    "UP Ch 8 pp. 275-284"
                ],
                "unresolved_gaps": []
            }
        ],
        "pedagogical_synthesis_notes": [
            "Progression moves from geometric and kinematic center of mass definitions to system dynamics (M A_cm = F_ext), vector impulse integration, conservation principles, and terminates in 1D and 2D collision energetics.",
            "Rigorous distinction maintained between internal forces (which cancel identically) and external forces (which dictate center of mass acceleration).",
            "Restitution coefficient is strictly formulated along the normal line of impact, with smooth tangential velocity invariance preserved in 2D oblique collisions."
        ],
        "unresolved_gaps": [],
        "created_at": now_iso
    }

    # Save Plan to both canonical and alias locations
    for p in [curr_chapters / "momentum-collisions_plan.json", curr_chapters / "center-of-mass_plan.json", staging_curr / "momentum-collisions_plan.json", staging_curr / "center-of-mass_plan.json"]:
        p.write_text(json.dumps(plan_data, indent=2), encoding="utf-8")

    # =============================================================
    # 2. CHAPTER SPEC
    # =============================================================
    spec_data = {
        "chapter_id": "center-of-mass",
        "chapter_title": "Center of Mass, Momentum, and Collisions",
        "template_type": "MECHANICS",
        "order": 5,
        "taxonomy_references": [
            {"chapter_id": "center-of-mass", "topic_id": "center-of-mass-fundamentals", "subtopic_id": "com-of-discrete-particles"},
            {"chapter_id": "center-of-mass", "topic_id": "center-of-mass-fundamentals", "subtopic_id": "com-of-continuous-bodies"},
            {"chapter_id": "center-of-mass", "topic_id": "center-of-mass-fundamentals", "subtopic_id": "motion-of-center-of-mass"},
            {"chapter_id": "center-of-mass", "topic_id": "center-of-mass-fundamentals", "subtopic_id": "shift-in-com-and-cavity-problems"},
            {"chapter_id": "center-of-mass", "topic_id": "linear-momentum-and-impulse", "subtopic_id": "conservation-of-linear-momentum"},
            {"chapter_id": "center-of-mass", "topic_id": "linear-momentum-and-impulse", "subtopic_id": "impulse-momentum-theorem"},
            {"chapter_id": "center-of-mass", "topic_id": "linear-momentum-and-impulse", "subtopic_id": "variable-mass-systems-and-rocket-propulsion"},
            {"chapter_id": "center-of-mass", "topic_id": "collisions", "subtopic_id": "elastic-collision-1d"},
            {"chapter_id": "center-of-mass", "topic_id": "collisions", "subtopic_id": "inelastic-collision-1d"},
            {"chapter_id": "center-of-mass", "topic_id": "collisions", "subtopic_id": "perfectly-inelastic-collision-2d"},
            {"chapter_id": "center-of-mass", "topic_id": "collisions", "subtopic_id": "coefficient-of-restitution"},
            {"chapter_id": "center-of-mass", "topic_id": "collisions", "subtopic_id": "oblique-collisions"}
        ],
        "learning_objectives": [
            "Compute the center of mass for discrete multi-particle systems and continuous symmetric bodies using integral calculus.",
            "Apply negative mass superposition to calculate shifts in the center of mass for bodies with hollow cavities.",
            "Master Newton's Second Law for systems of particles M A_cm = F_net,ext and analyze motion in the center of mass reference frame.",
            "Formulate the Impulse-Momentum Theorem J_net = Delta p and differentiate impulsive from non-impulsive forces.",
            "Apply the Principle of Conservation of Linear Momentum to isolated systems, explosions, gun recoil, and unconstrained coordinate axes.",
            "Derive reactive thrust forces and the Tsiolkovsky rocket equation for variable-mass flight.",
            "Analyze 1D elastic and inelastic collisions using Newton's experimental law of restitution e = v_sep / v_app.",
            "Calculate mechanical energy dissipation in inelastic impacts and analyze ballistic pendulums.",
            "Decompose 2D oblique collisions into line of impact and common tangential components, proving the 90 degree scattering angle for identical elastic spheres."
        ],
        "prerequisite_curriculum_nodes": [
            "vectors-and-coordinate-systems",
            "differential-calculus-foundations",
            "integral-calculus-foundations",
            "kinematics",
            "laws-of-motion",
            "work-energy-power"
        ],
        "concept_sequence": [
            {"concept_id": cid, "pedagogical_role": "CORE_PRINCIPLE", "section_id": s["section_id"]}
            for s in plan_data["sections"] for cid in s["concepts"]
        ],
        "formula_sequence": [
            {"formula_id": fid, "pedagogical_role": "CORE_PRINCIPLE", "section_id": s["section_id"]}
            for s in plan_data["sections"] for fid in s["formula_ids"]
        ],
        "misconception_sequence": [
            {"misconception_id": mid, "pedagogical_role": "COMMON_MISCONCEPTION", "section_id": s["section_id"]}
            for s in plan_data["sections"] for mid in s["misconception_ids"]
        ],
        "worked_example_sequence": [
            {"example_id": eid, "pedagogical_role": "WORKED_EXAMPLE", "section_id": s["section_id"]}
            for s in plan_data["sections"] for eid in s["worked_example_ids"]
        ],
        "question_sequence": [
            {"question_id": qid, "pedagogical_role": "PRACTICE_QUESTION", "section_id": s["section_id"]}
            for s in plan_data["sections"] for qid in s["question_atom_ids"]
        ],
        "question_ladders": [
            "ladder-mom-collision-restitution-01"
        ],
        "revision_checklist": [
            "Discrete center of mass position vector R_cm = sum(m_i r_i) / M",
            "Continuous center of mass integral R_cm = 1/M int r dm (Hemisphere: 3R/8, Cone: h/4)",
            "Cavity displacement by negative mass superposition",
            "System dynamics theorem M A_cm = F_net,ext (Internal forces cancel in pairs)",
            "Zero external force displacement invariance Delta X_cm = 0",
            "Linear momentum P = M V_cm and conservation dP/dt = 0 when F_net,ext = 0",
            "Impulse integral J = int F dt = Delta p and area under F-t curve",
            "Variable mass thrust F_thrust = v_rel (dm/dt) and rocket equation v = v0 + v_rel ln(m0/m) - gt",
            "1D head-on elastic collision velocities and equal-mass velocity exchange",
            "Restitution coefficient e = v_sep / v_app along line of impact",
            "Kinetic energy loss Delta K = 1/2 mu (1 - e^2) u_rel^2",
            "2D oblique impact: normal restitution with invariant tangential velocity component",
            "Identical elastic spheres scatter at 90 degrees when target is stationary"
        ],
        "created_at": now_iso
    }

    # Save Spec to both canonical and alias locations
    for p in [curr_chapters / "momentum-collisions_spec.json", curr_chapters / "center-of-mass_spec.json", staging_curr / "momentum-collisions_spec.json", staging_curr / "center-of-mass_spec.json"]:
        p.write_text(json.dumps(spec_data, indent=2), encoding="utf-8")

    print("Chapter Plan and Spec created successfully.")

if __name__ == "__main__":
    main()
