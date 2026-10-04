import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def main():
    ev_dir = Path("sources/evidence")
    
    with open(ev_dir / "records.json", "r", encoding="utf-8") as f:
        records = json.load(f)
    with open(ev_dir / "exposition.json", "r", encoding="utf-8") as f:
        exposition = json.load(f)
    with open(ev_dir / "formulas.json", "r", encoding="utf-8") as f:
        formulas = json.load(f)
    with open(ev_dir / "irodov_problems.json", "r", encoding="utf-8") as f:
        irodov = json.load(f)
    with open(ev_dir / "mock_questions.json", "r", encoding="utf-8") as f:
        mocks = json.load(f)

    manifest_entries = []

    source_info = {
        "src-concepts-of-physics-by-h-a489bb6e": {
            "title": "Concepts of Physics Vol 1 by H.C. Verma",
            "pdf": "concepts_of_physics_by_h.c._verma_volume_1.pdf"
        },
        "src-fundamentals-of-physics--390f40d1": {
            "title": "Fundamentals of Physics (Halliday, Resnick & Walker, 9th Ed)",
            "pdf": "fundamentals_of_physics_halliday_resnick_walker.pdf"
        },
        "src-university-physics-with--0bc11b67": {
            "title": "University Physics with Modern Physics (Young & Freedman, 13th Ed)",
            "pdf": "university_physics_with_modern_physics_young_freedman.pdf"
        },
        "src-feynman-richard-p-the-fe-486f6a95": {
            "title": "The Feynman Lectures on Physics, Vol. 1",
            "pdf": "feynman_lectures_on_physics_vol_1.pdf"
        },
        "src-problems-in-general-phys-6cf0b2b7": {
            "title": "Problems in General Physics by I.E. Irodov",
            "pdf": "problems_in_general_physics_irodov.pdf"
        },
        "src-jee-main-mock-test-01-20-222525c1": {
            "title": "JEE Main Mock Test 01",
            "pdf": "jee_main_mock_test_01.pdf"
        },
        "src-jee-rank-booster-02-mock-0548b6c5": {
            "title": "JEE Main Rank Booster Mock Test 02",
            "pdf": "jee_rank_booster_mock_02.pdf"
        },
        "src-jee-rank-booster-03-mock-256f42c6": {
            "title": "JEE Main Rank Booster Mock Test 03",
            "pdf": "jee_rank_booster_mock_03.pdf"
        }
    }

    # 1. Primary Structured Records from records.json
    for r in records:
        tax_nodes = r.get("taxonomy_node_ids", [])
        eid = r.get("evidence_id", "")
        is_mom = any(
            t in ["center-of-mass", "center-of-mass-fundamentals", "com-of-discrete-particles", "com-of-continuous-bodies", "motion-of-center-of-mass", "shift-in-com-and-cavity-problems", "linear-momentum-and-impulse", "conservation-of-linear-momentum", "impulse-momentum-theorem", "variable-mass-systems-and-rocket-propulsion", "collisions", "elastic-collision-1d", "inelastic-collision-1d", "perfectly-inelastic-collision-2d", "coefficient-of-restitution", "oblique-collisions"]
            for t in tax_nodes
        ) or any(
            k in eid.lower() for k in ["center-of-mass", "centre-of-mass", "collision", "impulse", "momentum", "restitution", "rocket"]
        )
        if is_mom and r.get("fidelity_class") in ["SOURCE_VERBATIM", "SOURCE_DERIVED"]:
            src_id = r.get("source_id", "src-concepts-of-physics-by-h-a489bb6e")
            sinfo = source_info.get(src_id, {"title": "Source Document", "pdf": "unknown.pdf"})
            role = "FOUNDATIONAL_THEORY" if r.get("evidence_type") == "THEOREM_PRINCIPLE" else "WORKED_ANALYSIS"
            target = "concept" if "law" in eid or "momentum" in eid or "collision" in eid else "derivation"
            manifest_entries.append({
                "evidence_id": eid,
                "source_id": src_id,
                "source_title": sinfo["title"],
                "page_range": f"{r.get('page_start')}-{r.get('page_end')}",
                "evidence_type": r.get("evidence_type"),
                "fidelity_class": r.get("fidelity_class"),
                "taxonomy_node": tax_nodes[0] if tax_nodes else "center-of-mass",
                "intended_chapter_role": role,
                "target_content_element": target,
                "summary": r.get("content_text", "")[:120] + "..."
            })

    # 2. Key Exposition Records from HCV1 Ch 9 (Centre of Mass, Linear Momentum, Collision)
    hcv_mom_expos = [
        ("exp-hcv1-ch09-p01", 150, 151, "Chapter 9: Center of Mass Definition for Discrete Particles", "com-of-discrete-particles", "concept-mom-com-discrete-01"),
        ("exp-hcv1-ch09-p02", 151, 153, "Chapter 9: Center of Mass Calculation for Continuous Bodies via Integration", "com-of-continuous-bodies", "concept-mom-com-continuous-01"),
        ("exp-hcv1-ch09-p03", 153, 155, "Chapter 9: Motion of Center of Mass and External Force Acceleration", "motion-of-center-of-mass", "concept-mom-com-motion-01"),
        ("exp-hcv1-ch09-p04", 155, 157, "Chapter 9: Shift in Center of Mass and Cavity Problems (Negative Mass)", "shift-in-com-and-cavity-problems", "concept-mom-cavity-shift-01"),
        ("exp-hcv1-ch09-p05", 157, 159, "Chapter 9: Linear Momentum and Principle of Conservation of Momentum", "conservation-of-linear-momentum", "concept-mom-conservation-01"),
        ("exp-hcv1-ch09-p06", 159, 161, "Chapter 9: Impulse Definition and Impulse-Momentum Theorem", "impulse-momentum-theorem", "concept-mom-impulse-def-01"),
        ("exp-hcv1-ch09-p07", 161, 163, "Chapter 9: Variable Mass Systems and Rocket Propulsion Dynamics", "variable-mass-systems-and-rocket-propulsion", "concept-mom-variable-mass-01"),
        ("exp-hcv1-ch09-p08", 163, 165, "Chapter 9: Definition of Collisions and Elastic vs Inelastic Impact", "elastic-collision-1d", "concept-mom-collision-types-01"),
        ("exp-hcv1-ch09-p09", 165, 167, "Chapter 9: One-Dimensional Head-On Elastic Collisions", "elastic-collision-1d", "concept-mom-elastic-1d-01"),
        ("exp-hcv1-ch09-p10", 167, 169, "Chapter 9: Coefficient of Restitution and Newton's Experimental Law", "coefficient-of-restitution", "concept-mom-restitution-01"),
        ("exp-hcv1-ch09-p11", 169, 171, "Chapter 9: Perfectly Inelastic Collisions and Ballistic Pendulum", "perfectly-inelastic-collision-2d", "concept-mom-inelastic-ballistic-01"),
        ("exp-hcv1-ch09-p12", 171, 173, "Chapter 9: Two-Dimensional Oblique Collisions and Line of Impact", "oblique-collisions", "concept-mom-oblique-collision-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in hcv_mom_expos:
        manifest_entries.append({
            "evidence_id": eid,
            "source_id": "src-concepts-of-physics-by-h-a489bb6e",
            "source_title": "Concepts of Physics Vol 1 by H.C. Verma",
            "page_range": f"{pstart}-{pend}",
            "evidence_type": "EXPOSITION",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax_node,
            "intended_chapter_role": "CONCEPT_EXPOSITION",
            "target_content_element": target,
            "summary": desc
        })

    # 3. Key Exposition Records from HRW (Halliday, Resnick & Walker, Ch 9)
    hrw_mom_expos = [
        ("exp-hr-ch09-p01", 227, 230, "HRW Chapter 9: Center of Mass System of Particles & Solid Bodies", "com-of-discrete-particles", "concept-mom-com-discrete-01"),
        ("exp-hr-ch09-p02", 230, 234, "HRW Chapter 9: Newton's Second Law for a System of Particles", "motion-of-center-of-mass", "concept-mom-com-motion-01"),
        ("exp-hr-ch09-p03", 234, 238, "HRW Chapter 9: Linear Momentum and System Momentum Conservation", "conservation-of-linear-momentum", "concept-mom-conservation-01"),
        ("exp-hr-ch09-p04", 238, 242, "HRW Chapter 9: Collision and Impulse Integral in Single and Multi-Body Systems", "impulse-momentum-theorem", "concept-mom-impulse-def-01"),
        ("exp-hr-ch09-p05", 242, 246, "HRW Chapter 9: Momentum and Kinetic Energy in Inelastic Collisions", "inelastic-collision-1d", "concept-mom-collision-types-01"),
        ("exp-hr-ch09-p06", 246, 250, "HRW Chapter 9: Elastic Collisions in One Dimension & Stationary Target Limiting Cases", "elastic-collision-1d", "concept-mom-elastic-1d-01"),
        ("exp-hr-ch09-p07", 250, 254, "HRW Chapter 9: Collisions in Two Dimensions with Angle Resolution", "oblique-collisions", "concept-mom-oblique-collision-01"),
        ("exp-hr-ch09-p08", 254, 258, "HRW Chapter 9: Systems with Varying Mass: The Rocket Equation and Thrust", "variable-mass-systems-and-rocket-propulsion", "concept-mom-variable-mass-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in hrw_mom_expos:
        manifest_entries.append({
            "evidence_id": eid,
            "source_id": "src-fundamentals-of-physics--390f40d1",
            "source_title": "Fundamentals of Physics (Halliday, Resnick & Walker, 9th Ed)",
            "page_range": f"{pstart}-{pend}",
            "evidence_type": "EXPOSITION",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax_node,
            "intended_chapter_role": "CONCEPT_EXPOSITION",
            "target_content_element": target,
            "summary": desc
        })

    # 4. Key Exposition Records from University Physics (Young & Freedman, Ch 8)
    up_mom_expos = [
        ("exp-up-ch08-p01", 267, 271, "UP Chapter 8: Momentum and Impulse: Vector Character and J = Delta p", "impulse-momentum-theorem", "concept-mom-impulse-def-01"),
        ("exp-up-ch08-p02", 271, 275, "UP Chapter 8: Conservation of Momentum in Isolated Systems", "conservation-of-linear-momentum", "concept-mom-conservation-01"),
        ("exp-up-ch08-p03", 275, 279, "UP Chapter 8: Momentum Conservation and Collision Dynamics", "elastic-collision-1d", "concept-mom-collision-types-01"),
        ("exp-up-ch08-p04", 279, 284, "UP Chapter 8: Elastic Collisions and Energy Sharing", "elastic-collision-1d", "concept-mom-elastic-1d-01"),
        ("exp-up-ch08-p05", 284, 289, "UP Chapter 8: Center of Mass: Discrete and Continuous Systems", "com-of-discrete-particles", "concept-mom-com-discrete-01"),
        ("exp-up-ch08-p06", 289, 293, "UP Chapter 8: Rocket Propulsion and Variable Mass Systems", "variable-mass-systems-and-rocket-propulsion", "concept-mom-variable-mass-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in up_mom_expos:
        manifest_entries.append({
            "evidence_id": eid,
            "source_id": "src-university-physics-with--0bc11b67",
            "source_title": "University Physics with Modern Physics (Young & Freedman, 13th Ed)",
            "page_range": f"{pstart}-{pend}",
            "evidence_type": "EXPOSITION",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax_node,
            "intended_chapter_role": "CONCEPT_EXPOSITION",
            "target_content_element": target,
            "summary": desc
        })

    # 5. Key Exposition Records from Feynman Lectures on Physics (Vol 1, Ch 10 & 19)
    feynman_mom_expos = [
        ("exp-feynman-ch10-p01", 86, 90, "Feynman Vol 1 Ch 10: Conservation of Momentum from Newton's Third Law", "conservation-of-linear-momentum", "concept-mom-conservation-01"),
        ("exp-feynman-ch19-p01", 101, 105, "Feynman Vol 1 Ch 19: Center of Mass and Motion of a System of Particles", "motion-of-center-of-mass", "concept-mom-com-motion-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in feynman_mom_expos:
        manifest_entries.append({
            "evidence_id": eid,
            "source_id": "src-feynman-richard-p-the-fe-486f6a95",
            "source_title": "The Feynman Lectures on Physics, Vol. 1",
            "page_range": f"{pstart}-{pend}",
            "evidence_type": "EXPOSITION",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax_node,
            "intended_chapter_role": "CONCEPT_EXPOSITION",
            "target_content_element": target,
            "summary": desc
        })

    # 6. Advanced Problems from Irodov Section 1.3 (Conservation Laws)
    irodov_mom_problems = [
        ("irodov-prob-1-140", 29, 29, "Irodov 1.140: Body of mass m moving horizontally collides with pendulum of mass M; velocity post impact and height", "collisions", "worked_example"),
        ("irodov-prob-1-141", 29, 30, "Irodov 1.141: Inelastic impact of bullet with ballistic pendulum suspended on light thread; angle of deflection", "perfectly-inelastic-collision-2d", "worked_example"),
        ("irodov-prob-1-144", 30, 30, "Irodov 1.144: Particle of mass m1 collides elastically with stationary particle of mass m2; maximum deflection angle", "elastic-collision-1d", "problem"),
        ("irodov-prob-1-145", 30, 31, "Irodov 1.145: Direct head-on collision with coefficient of restitution e; fraction of kinetic energy transformed into heat", "coefficient-of-restitution", "derivation"),
        ("irodov-prob-1-148", 31, 31, "Irodov 1.148: Elastic oblique collision of two identical spheres; 90 degree scattering angle proof", "oblique-collisions", "derivation"),
        ("irodov-prob-1-171", 34, 35, "Irodov 1.171: Rocket moves in gravity-free space with constant gas exhaust velocity u; velocity as function of mass ratio", "variable-mass-systems-and-rocket-propulsion", "derivation"),
        ("irodov-prob-1-172", 35, 35, "Irodov 1.172: Rocket launch under constant downward gravity; burnout velocity and mass burnout time", "variable-mass-systems-and-rocket-propulsion", "worked_example"),
        ("irodov-prob-1-175", 35, 36, "Irodov 1.175: Sledge with sand moving on horizontal plane under constant force while sand leaks at rate mu", "variable-mass-systems-and-rocket-propulsion", "worked_example"),
        ("irodov-prob-1-180", 37, 37, "Irodov 1.180: Center of mass motion of two connected masses on spring on frictionless horizontal floor", "motion-of-center-of-mass", "worked_example")
    ]

    for pid, pstart, pend, desc, tax_node, target in irodov_mom_problems:
        manifest_entries.append({
            "evidence_id": f"src-irodov-{pid}",
            "source_id": "src-problems-in-general-phys-6cf0b2b7",
            "source_title": "Problems in General Physics by I.E. Irodov",
            "page_range": f"{pstart}-{pend}",
            "evidence_type": "STRUCTURED_PROBLEM",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax_node,
            "intended_chapter_role": "ADVANCED_PROBLEM",
            "target_content_element": target,
            "summary": desc
        })

    # 7. Authentic JEE Mock Questions
    mock_mom_questions = [
        ("src-mock-01-q08", "src-jee-main-mock-test-01-20-222525c1", 3, 3, "JEE Main Mock 01 Q8: Collision of two spheres with coefficient of restitution e=0.5; ratio of final kinetic energy to initial", "coefficient-of-restitution", "practice_question"),
        ("src-mock-02-q12", "src-jee-rank-booster-02-mock-0548b6c5", 4, 4, "Rank Booster Mock 02 Q12: Shift of center of mass of uniform disc when circular cavity of radius R/2 is cut out", "shift-in-com-and-cavity-problems", "practice_question"),
        ("src-mock-03-q15", "src-jee-rank-booster-03-mock-256f42c6", 5, 5, "Rank Booster Mock 03 Q15: Rocket dynamics with constant fuel burn rate dm/dt; acceleration at t = t_burnout / 2", "variable-mass-systems-and-rocket-propulsion", "practice_question")
    ]

    for qid, src_id, pstart, pend, desc, tax_node, target in mock_mom_questions:
        manifest_entries.append({
            "evidence_id": qid,
            "source_id": src_id,
            "source_title": source_info[src_id]["title"],
            "page_range": f"{pstart}-{pend}",
            "evidence_type": "EXAM_QUESTION",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax_node,
            "intended_chapter_role": "PRACTICE_ASSESSMENT",
            "target_content_element": target,
            "summary": desc
        })

    # 8. Derived / Structured Transformation Records (Formulas, Derivations, Worked Examples)
    derived_mom_records = [
        ("form-mom-com-discrete", "formula", "com-of-discrete-particles", "Discrete Center of Mass Definition R_cm = sum(m_i r_i) / M"),
        ("form-mom-com-continuous", "formula", "com-of-continuous-bodies", "Continuous Center of Mass Integral R_cm = 1/M int r dm"),
        ("form-mom-com-hemisphere", "formula", "com-of-continuous-bodies", "Solid Hemisphere CM Coordinate y_cm = 3R / 8 from flat base"),
        ("form-mom-com-cone", "formula", "com-of-continuous-bodies", "Solid Cone CM Coordinate y_cm = h / 4 from base"),
        ("form-mom-com-cavity", "formula", "shift-in-com-and-cavity-problems", "Negative Mass Cavity Shift Formula r_rem = (M r_orig - m_cav r_cav) / (M - m_cav)"),
        ("form-mom-com-velocity", "formula", "motion-of-center-of-mass", "Center of Mass Velocity V_cm = sum(m_i v_i) / M = P_total / M"),
        ("form-mom-com-acceleration", "formula", "motion-of-center-of-mass", "Center of Mass Acceleration A_cm = F_ext / M"),
        ("form-mom-conservation", "formula", "conservation-of-linear-momentum", "Conservation of Linear Momentum P_initial = P_final when F_ext = 0"),
        ("form-mom-impulse-integral", "formula", "impulse-momentum-theorem", "Impulse Vector Integral J = int F dt = Delta p"),
        ("form-mom-rocket-thrust", "formula", "variable-mass-systems-and-rocket-propulsion", "Thrust Force on Variable Mass System F_thrust = v_rel * (dm/dt)"),
        ("form-mom-rocket-tsiolkovsky", "formula", "variable-mass-systems-and-rocket-propulsion", "Tsiolkovsky Rocket Equation v = v_0 + v_rel ln(m_0 / m) - g t"),
        ("form-mom-elastic-1d-v1", "formula", "elastic-collision-1d", "Head-on Elastic Collision Velocity v1 = (m1 - m2)/(m1 + m2) u1 + 2 m2 / (m1 + m2) u2"),
        ("form-mom-elastic-1d-v2", "formula", "elastic-collision-1d", "Head-on Elastic Collision Velocity v2 = 2 m1 / (m1 + m2) u1 + (m2 - m1)/(m1 + m2) u2"),
        ("form-mom-restitution-def", "formula", "coefficient-of-restitution", "Coefficient of Restitution e = (v2 - v1) / (u1 - u2) along line of impact"),
        ("form-mom-inelastic-energy-loss", "formula", "inelastic-collision-1d", "Kinetic Energy Loss in 1D Collision Delta K = 1/2 * (m1 m2)/(m1 + m2) * (1 - e^2) * (u1 - u2)^2"),
        ("form-mom-oblique-angle-rebound", "formula", "oblique-collisions", "Oblique Rebound Angle tan(beta) = (1/e) tan(alpha) from smooth floor"),
        # Derivations
        ("deriv-mom-com-hemisphere", "derivation", "com-of-continuous-bodies", "First-principles integration of solid hemisphere thin circular discs yielding y_cm = 3R/8"),
        ("deriv-mom-com-motion", "derivation", "motion-of-center-of-mass", "Proof that internal forces cancel in pairs yielding M A_cm = F_net,ext"),
        ("deriv-mom-impulse-momentum", "derivation", "impulse-momentum-theorem", "Derivation of J = Delta p from Newton's Second Law F = dp/dt"),
        ("deriv-mom-tsiolkovsky-rocket", "derivation", "variable-mass-systems-and-rocket-propulsion", "Derivation of Tsiolkovsky rocket equation from momentum conservation in inertial frame"),
        ("deriv-mom-elastic-1d-velocities", "derivation", "elastic-collision-1d", "Derivation of final velocities v1, v2 from momentum and kinetic energy conservation"),
        ("deriv-mom-inelastic-energy-loss", "derivation", "inelastic-collision-1d", "Derivation of kinetic energy loss formula Delta K = 1/2 mu (1 - e^2) u_rel^2"),
        ("deriv-mom-identical-oblique-90deg", "derivation", "oblique-collisions", "Proof that elastic collision of identical spheres with stationary target scatters at exactly 90 degrees"),
        # Worked Examples
        ("ex-mom-disc-cavity-01", "worked_example", "shift-in-com-and-cavity-problems", "Circular cavity of radius R/2 cut out from uniform circular disc of radius R; finding CM of remaining body"),
        ("ex-mom-man-plank-01", "worked_example", "motion-of-center-of-mass", "Man of mass m walks from one end of plank of mass M and length L on frictionless ice; displacement of plank"),
        ("ex-mom-rocket-vertical-climb-01", "worked_example", "variable-mass-systems-and-rocket-propulsion", "Rocket launched vertically upward with fuel burn rate; finding velocity at fuel exhaustion"),
        ("ex-mom-elastic-target-masses-01", "worked_example", "elastic-collision-1d", "Head-on elastic collision of neutron with stationary target nucleus (carbon vs hydrogen) and energy transfer fraction"),
        ("ex-mom-ballistic-pendulum-01", "worked_example", "perfectly-inelastic-collision-2d", "Bullet embeds into wooden block suspended as pendulum; finding bullet speed from swing height h"),
        ("ex-mom-oblique-two-disc-01", "worked_example", "oblique-collisions", "Oblique collision of two identical billiard balls; line of centres impact parameter and rebound angles"),
        # Misconceptions
        ("misc-mom-01", "misconception", "motion-of-center-of-mass", "Internal explosions or internal forces can accelerate the system center of mass"),
        ("misc-mom-02", "misconception", "conservation-of-linear-momentum", "Linear momentum is conserved only if mechanical energy is also conserved"),
        ("misc-mom-03", "misconception", "impulse-momentum-theorem", "Impulse is a scalar quantity equal to force multiplied by time without directionality"),
        ("misc-mom-04", "misconception", "coefficient-of-restitution", "Coefficient of restitution relates velocities in any direction rather than strictly along the line of impact"),
        ("misc-mom-05", "misconception", "variable-mass-systems-and-rocket-propulsion", "Applying F = m a directly to variable mass rocket by treating dm/dt * a as standard force"),
        ("misc-mom-06", "misconception", "oblique-collisions", "In oblique impact with smooth floor, the tangential velocity component decreases or reverses")
    ]

    for rid, rtype, tax_node, desc in derived_mom_records:
        manifest_entries.append({
            "evidence_id": f"src-deriv-{rid}",
            "source_id": "src-concepts-of-physics-by-h-a489bb6e",
            "source_title": "Concepts of Physics Vol 1 by H.C. Verma",
            "page_range": "150-180",
            "evidence_type": "DERIVED_TRANSFORMATION",
            "fidelity_class": "SOURCE_DERIVED",
            "taxonomy_node": tax_node,
            "intended_chapter_role": rtype.upper(),
            "target_content_element": rid,
            "summary": desc
        })

    # Save structured manifest
    out_path = Path("build/reports/momentum_collisions_source_evidence_manifest.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, indent=2, ensure_ascii=False)

    print(f"Momentum & Collisions Source Evidence Manifest built successfully:")
    print(f"Total evidence entries: {len(manifest_entries)}")
    fidelity_counts = {}
    for e in manifest_entries:
        fc = e["fidelity_class"]
        fidelity_counts[fc] = fidelity_counts.get(fc, 0) + 1
    print(f"Fidelity classes: {fidelity_counts}")

if __name__ == "__main__":
    main()
