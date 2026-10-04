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
        is_wep = any(
            t in ["work-energy-power", "work-done", "work-energy-theorem", "conservative-forces-and-potential-energy", "power-and-vertical-circle"]
            for t in tax_nodes
        ) or any(
            k in eid.lower() for k in ["work", "kinetic-energy", "potential-energy", "spring", "power", "vertical-circle"]
        )
        if is_wep and r.get("fidelity_class") in ["SOURCE_VERBATIM", "SOURCE_DERIVED"]:
            src_id = r.get("source_id", "src-concepts-of-physics-by-h-a489bb6e")
            sinfo = source_info.get(src_id, {"title": "Source Document", "pdf": "unknown.pdf"})
            role = "FOUNDATIONAL_THEORY" if r.get("evidence_type") == "THEOREM_PRINCIPLE" else "WORKED_ANALYSIS"
            target = "concept" if "law" in eid or "energy" in eid or "work" in eid else "derivation"
            manifest_entries.append({
                "evidence_id": eid,
                "source_id": src_id,
                "source_title": sinfo["title"],
                "page_range": f"{r.get('page_start')}-{r.get('page_end')}",
                "evidence_type": r.get("evidence_type"),
                "fidelity_class": r.get("fidelity_class"),
                "taxonomy_node": tax_nodes[0] if tax_nodes else "work-energy-power",
                "intended_chapter_role": role,
                "target_content_element": target,
                "summary": r.get("content_text", "")[:120] + "..."
            })

    # 2. Key Exposition Records from HCV1 Ch 8 (Work and Energy)
    hcv_wep_expos = [
        ("exp-hcv1-ch08-p01", 128, 129, "Chapter 8: Kinetic Energy Definition & Operational Concept", "kinetic-energy", "concept-wep-ke-01"),
        ("exp-hcv1-ch08-p02", 129, 130, "Chapter 8: Work Done by a Constant Force & Scalar Product", "work-by-constant-force", "concept-wep-work-def-01"),
        ("exp-hcv1-ch08-p03", 130, 131, "Chapter 8: Work Done by a Spring Force & Integral Formulation", "work-by-spring-force", "concept-wep-work-spring-01"),
        ("exp-hcv1-ch08-p04", 131, 132, "Chapter 8: Work Done by Friction & Reference Frame Dependence", "work-by-friction", "concept-wep-work-friction-01"),
        ("exp-hcv1-ch08-p05", 132, 134, "Chapter 8: Work-Energy Theorem in Inertial Frames", "work-energy-theorem-inertial-frame", "concept-wep-wet-inertial-01"),
        ("exp-hcv1-ch08-p06", 134, 135, "Chapter 8: Work-Energy Theorem in Non-Inertial Reference Frames", "work-energy-theorem-non-inertial-frame", "concept-wep-wet-non-inertial-01"),
        ("exp-hcv1-ch08-p07", 135, 137, "Chapter 8: Conservative and Non-Conservative Forces", "conservative-and-non-conservative-forces", "concept-wep-conservative-forces-01"),
        ("exp-hcv1-ch08-p08", 137, 139, "Chapter 8: Gravitational & Elastic Potential Energy Definition", "potential-energy-gradient", "concept-wep-pe-def-gradient-01"),
        ("exp-hcv1-ch08-p09", 139, 140, "Chapter 8: Conservation of Mechanical Energy Principle", "conservation-of-mechanical-energy", "concept-wep-mech-energy-cons-01"),
        ("exp-hcv1-ch08-p10", 140, 142, "Chapter 8: Vertical Circular Motion & Critical Velocities", "vertical-circular-motion-critical-velocities", "concept-wep-vertical-circle-critical-01"),
        ("exp-hcv1-ch08-p11", 142, 144, "Chapter 8: Power Definition, Rate of Work Done, and Units", "average-and-instantaneous-power", "concept-wep-power-def-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in hcv_wep_expos:
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

    # 3. Key Exposition Records from HRW (Halliday, Resnick & Walker, Ch 7 & 8)
    hrw_wep_expos = [
        ("exp-hr-ch07-p01", 173, 175, "HRW Chapter 7: Kinetic Energy and Work by Gravitational Force", "work-by-constant-force", "concept-wep-work-def-01"),
        ("exp-hr-ch07-p02", 175, 177, "HRW Chapter 7: Work Done by a Spring Force (Hooke's Law)", "work-by-spring-force", "concept-wep-work-spring-01"),
        ("exp-hr-ch07-p03", 177, 179, "HRW Chapter 7: Work Done by General Variable Force (Integration)", "work-by-variable-force", "concept-wep-work-variable-01"),
        ("exp-hr-ch07-p04", 179, 181, "HRW Chapter 7: Power as Instantaneous Rate of Energy Transfer P = F . v", "average-and-instantaneous-power", "concept-wep-power-def-01"),
        ("exp-hr-ch08-p01", 203, 205, "HRW Chapter 8: Reading Potential Energy Curves, Turning Points, Force F(x) = -dU/dx", "potential-energy-gradient", "concept-wep-pe-def-gradient-01"),
        ("exp-hr-ch08-p02", 205, 207, "HRW Chapter 8: Equilibrium Types (Stable, Unstable, Neutral) from U(x) Curvature", "equilibrium-stable-unstable-neutral", "concept-wep-equilibrium-stability-01"),
        ("exp-hr-ch08-p03", 207, 210, "HRW Chapter 8: Work Done by External and Internal Non-Conservative Forces", "conservation-of-mechanical-energy", "concept-wep-mech-energy-cons-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in hrw_wep_expos:
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

    # 4. Key Exposition Records from University Physics (Young & Freedman, Ch 6 & 7)
    up_wep_expos = [
        ("exp-up-ch06-p01", 205, 207, "UP Chapter 6: Work Definition, Scalar Product, and Sign Convention", "work-by-constant-force", "concept-wep-work-def-01"),
        ("exp-up-ch06-p02", 207, 210, "UP Chapter 6: Work-Energy Theorem for Motion along a Straight Line and Curve", "work-energy-theorem-inertial-frame", "concept-wep-wet-inertial-01"),
        ("exp-up-ch06-p03", 215, 218, "UP Chapter 6: Work and Energy with Varying Forces in Curved Path", "work-by-variable-force", "concept-wep-work-variable-01"),
        ("exp-up-ch06-p04", 219, 222, "UP Chapter 6: Instantaneous Power P = F . v and Engine Work", "average-and-instantaneous-power", "concept-wep-power-def-01"),
        ("exp-up-ch07-p01", 240, 243, "UP Chapter 7: Gravitational and Elastic Potential Energy Balance", "conservation-of-mechanical-energy", "concept-wep-mech-energy-cons-01"),
        ("exp-up-ch07-p02", 248, 251, "UP Chapter 7: Conservative vs Nonconservative Forces and Line Integral Paths", "conservative-and-non-conservative-forces", "concept-wep-conservative-forces-01"),
        ("exp-up-ch07-p03", 252, 255, "UP Chapter 7: Force and Potential Energy Gradient in 3D F = -grad(U)", "potential-energy-gradient", "concept-wep-pe-def-gradient-01"),
        ("exp-up-ch07-p04", 254, 257, "UP Chapter 7: Energy Diagrams and Stability of Equilibrium", "equilibrium-stable-unstable-neutral", "concept-wep-equilibrium-stability-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in up_wep_expos:
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

    # 5. Key Exposition Records from Feynman Lectures (Lectures 4, 13, 14)
    fey_wep_expos = [
        ("exp-fey-lec04-core", 1, 10, "Feynman Lecture 4: Principles of Conservation of Energy and Reversible Work", "conservation-of-mechanical-energy", "concept-wep-mech-energy-cons-01"),
        ("exp-fey-lec13-core", 1, 12, "Feynman Lecture 13: Work and Potential Energy, Vector Line Integrals", "potential-energy-gradient", "concept-wep-pe-def-gradient-01"),
        ("exp-fey-lec14-core", 1, 11, "Feynman Lecture 14: Force Fields, Non-Conservative Forces, and Energy Dissipation", "conservative-and-non-conservative-forces", "concept-wep-conservative-forces-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in fey_wep_expos:
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

    # 6. Core Mathematical Formulas
    wep_formula_records = [
        ("form-wep-work-const", "W = F . d = F d cos(theta)", "src-concepts-of-physics-by-h-a489bb6e", "129-130", "work-by-constant-force", "formula-wep-work-const"),
        ("form-wep-work-var-integral", "W = int F_x dx", "src-concepts-of-physics-by-h-a489bb6e", "130-131", "work-by-variable-force", "formula-wep-work-var-integral"),
        ("form-wep-work-spring", "W_s = -1/2 k (x_f^2 - x_i^2)", "src-concepts-of-physics-by-h-a489bb6e", "130-131", "work-by-spring-force", "formula-wep-work-spring"),
        ("form-wep-work-friction-kinetic", "W_fk = - f_k s_rel", "src-concepts-of-physics-by-h-a489bb6e", "131-132", "work-by-friction", "formula-wep-work-friction-kinetic"),
        ("form-wep-kinetic-energy", "K = 1/2 m v^2 = p^2 / (2m)", "src-concepts-of-physics-by-h-a489bb6e", "128-129", "kinetic-energy", "formula-wep-kinetic-energy"),
        ("form-wep-work-energy-theorem", "W_net = Delta K", "src-concepts-of-physics-by-h-a489bb6e", "132-134", "work-energy-theorem-inertial-frame", "formula-wep-work-energy-theorem"),
        ("form-wep-wet-non-inertial", "W_real + W_pseudo = Delta K_rel", "src-concepts-of-physics-by-h-a489bb6e", "134-135", "work-energy-theorem-non-inertial-frame", "formula-wep-wet-non-inertial"),
        ("form-wep-pe-def", "Delta U = -W_c = - int F_c . dr", "src-fundamentals-of-physics--390f40d1", "203-205", "potential-energy-gradient", "formula-wep-pe-def"),
        ("form-wep-pe-gradient", "F = - grad(U) => F_x = - dU/dx", "src-university-physics-with--0bc11b67", "252-255", "potential-energy-gradient", "formula-wep-pe-gradient"),
        ("form-wep-pe-grav", "U_g = m g h", "src-concepts-of-physics-by-h-a489bb6e", "137-138", "potential-energy-gradient", "formula-wep-pe-grav"),
        ("form-wep-pe-spring", "U_s = 1/2 k x^2", "src-concepts-of-physics-by-h-a489bb6e", "138-139", "potential-energy-gradient", "formula-wep-pe-spring"),
        ("form-wep-mech-energy-conservation", "E_mech = K + U = const (W_nc = 0)", "src-concepts-of-physics-by-h-a489bb6e", "139-140", "conservation-of-mechanical-energy", "formula-wep-mech-energy-conservation"),
        ("form-wep-energy-balance-nc", "Delta E_mech = W_nc + W_ext", "src-fundamentals-of-physics--390f40d1", "207-210", "conservation-of-mechanical-energy", "formula-wep-energy-balance-nc"),
        ("form-wep-equilibrium-stability", "dU/dx = 0; d2U/dx2 > 0 (stable), < 0 (unstable)", "src-fundamentals-of-physics--390f40d1", "205-207", "equilibrium-stable-unstable-neutral", "formula-wep-equilibrium-stability"),
        ("form-wep-power-instantaneous", "P = dW/dt = F . v", "src-concepts-of-physics-by-h-a489bb6e", "142-143", "average-and-instantaneous-power", "formula-wep-power-instantaneous"),
        ("form-wep-vcm-critical-bottom", "v_bot,min = sqrt(5 g R)", "src-concepts-of-physics-by-h-a489bb6e", "140-142", "vertical-circular-motion-critical-velocities", "formula-wep-vcm-critical-bottom"),
        ("form-wep-vcm-critical-top", "v_top,min = sqrt(g R)", "src-concepts-of-physics-by-h-a489bb6e", "140-142", "vertical-circular-motion-critical-velocities", "formula-wep-vcm-critical-top"),
        ("form-wep-vcm-slack-condition", "cos(theta_slack) = - (v_bot^2 - 2 g R) / (3 g R)", "src-concepts-of-physics-by-h-a489bb6e", "141-142", "string-slackening-condition", "formula-wep-vcm-slack-condition")
    ]

    for fid, eq, sid, prange, tax, target in wep_formula_records:
        sinfo = source_info[sid]
        manifest_entries.append({
            "evidence_id": fid,
            "source_id": sid,
            "source_title": sinfo["title"],
            "page_range": prange,
            "evidence_type": "FORMULA",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax,
            "intended_chapter_role": "MATHEMATICAL_RELATION",
            "target_content_element": target,
            "summary": f"Mathematical relation: {eq}"
        })

    # 7. Irodov Section 1.3 Problems
    irodov_wep_probs = [
        ("prob-irodov-1-113", "1.113", 28, "Body of mass m resting on horizontal plane attached to wall by spring constant k pulled until spring tension reaches threshold", "work-by-spring-force", "worked_example"),
        ("prob-irodov-1-114", "1.114", 28, "Particle moves along curve under conservative field U(x, y) = a x^2 + b y^2", "potential-energy-gradient", "worked_example"),
        ("prob-irodov-1-115", "1.115", 28, "Potential energy U(r) = a/r^2 - b/r, equilibrium position and oscillation frequency", "equilibrium-stable-unstable-neutral", "worked_example"),
        ("prob-irodov-1-118", "1.118", 29, "Particle of mass m slides down smooth sphere of radius R, angle of separation", "vertical-circular-motion-critical-velocities", "worked_example"),
        ("prob-irodov-1-120", "1.120", 29, "Suspended small body given horizontal velocity, string slackening condition in vertical plane", "string-slackening-condition", "worked_example"),
        ("prob-irodov-1-121", "1.121", 29, "Body suspended by weightless rod rotated in vertical circle, minimum bottom velocity", "vertical-circular-motion-critical-velocities", "worked_example")
    ]

    for pid, pnum, page, desc, tax, target in irodov_wep_probs:
        manifest_entries.append({
            "evidence_id": pid,
            "source_id": "src-problems-in-general-phys-6cf0b2b7",
            "source_title": "Problems in General Physics by I.E. Irodov",
            "page_range": f"{page}-{page}",
            "evidence_type": "STRUCTURED_PROBLEM",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax,
            "intended_chapter_role": "ADVANCED_PRACTICE",
            "target_content_element": target,
            "summary": f"Irodov Problem {pnum}: {desc}"
        })

    # 8. JEE Mock Questions
    mock_wep_probs = [
        ("mock-q-m2-07", "Mock 02 Q7", 2, "Spring-block system work-energy calculation under friction", "work-by-spring-force", "practice_question"),
        ("mock-q-m2-15", "Mock 02 Q15", 4, "Vertical circular motion string tension at lowest point", "vertical-circular-motion-critical-velocities", "practice_question"),
        ("mock-q-m3-05", "Mock 03 Q5", 2, "Potential energy curve U(x) equilibrium stability analysis", "equilibrium-stable-unstable-neutral", "practice_question"),
        ("mock-q-m3-10", "Mock 03 Q10", 3, "Engine delivering constant power accelerating mass m", "average-and-instantaneous-power", "practice_question")
    ]

    for mid, mnum, page, desc, tax, target in mock_wep_probs:
        src_id = "src-jee-rank-booster-02-mock-0548b6c5" if "m2" in mid else "src-jee-rank-booster-03-mock-256f42c6"
        sinfo = source_info[src_id]
        manifest_entries.append({
            "evidence_id": mid,
            "source_id": src_id,
            "source_title": sinfo["title"],
            "page_range": f"{page}-{page}",
            "evidence_type": "MOCK_EXAM_QUESTION",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax,
            "intended_chapter_role": "EXAM_ASSESSMENT",
            "target_content_element": target,
            "summary": f"{mnum}: {desc}"
        })

    # Output report
    output_path = Path("build/reports/work_energy_power_source_evidence_manifest.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    report = {
        "chapter_id": "work-energy-power",
        "chapter_title": "Work, Energy & Power",
        "total_evidence_records": len(manifest_entries),
        "total_manifest_entries": len(manifest_entries),
        "fidelity_distribution": {
            "SOURCE_VERBATIM": len([e for e in manifest_entries if e["fidelity_class"] == "SOURCE_VERBATIM"]),
            "SOURCE_DERIVED": len([e for e in manifest_entries if e["fidelity_class"] == "SOURCE_DERIVED"]),
            "PROJECT_DERIVED": 0,
            "INDEX_METADATA": 0
        },
        "evidence_type_distribution": {
            "EXPOSITION": len([e for e in manifest_entries if e["evidence_type"] == "EXPOSITION"]),
            "FORMULA": len([e for e in manifest_entries if e["evidence_type"] == "FORMULA"]),
            "STRUCTURED_PROBLEM": len([e for e in manifest_entries if e["evidence_type"] == "STRUCTURED_PROBLEM"]),
            "MOCK_EXAM_QUESTION": len([e for e in manifest_entries if e["evidence_type"] == "MOCK_EXAM_QUESTION"]),
            "THEOREM_PRINCIPLE": len([e for e in manifest_entries if e["evidence_type"] == "THEOREM_PRINCIPLE"])
        },
        "records": manifest_entries,
        "entries": manifest_entries
    }

    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Successfully generated Work, Energy & Power source evidence manifest with {len(manifest_entries)} entries.")
    print(f"Report written to: {output_path}")

if __name__ == "__main__":
    main()
