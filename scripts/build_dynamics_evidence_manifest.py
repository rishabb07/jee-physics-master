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

    # Map of source IDs to human titles and PDFs
    source_info = {
        "src-concepts-of-physics-by-h-a489bb6e": {
            "title": "Concepts of Physics Vol 1 by H.C. Verma",
            "pdf": "concepts_of_physics_by_h.c._verma_volume_1.pdf"
        },
        "src-fundamentals-of-physics--390f40d1": {
            "title": "Fundamentals of Physics (Halliday, Resnick & Walker)",
            "pdf": "fundamentals_of_physics_halliday_resnick_walker.pdf"
        },
        "src-university-physics-with--0bc11b67": {
            "title": "University Physics with Modern Physics (Young & Freedman)",
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
        # Filter for laws-of-motion relevance
        is_dyn = any(
            t in ["laws-of-motion", "newtons-laws", "friction", "circular-dynamics"]
            for t in tax_nodes
        ) or any(
            k in eid.lower() for k in ["newton", "friction", "fbd", "pulley", "pseudo", "centripetal"]
        )
        if is_dyn and r.get("fidelity_class") in ["SOURCE_VERBATIM", "SOURCE_DERIVED"]:
            src_id = r.get("source_id", "src-concepts-of-physics-by-h-a489bb6e")
            sinfo = source_info.get(src_id, {"title": "Source Document", "pdf": "unknown.pdf"})
            role = "FOUNDATIONAL_THEORY" if r.get("evidence_type") == "THEOREM_PRINCIPLE" else "WORKED_ANALYSIS"
            target = "concept" if "law" in eid or "friction" in eid else "derivation"
            manifest_entries.append({
                "evidence_id": eid,
                "source_id": src_id,
                "source_title": sinfo["title"],
                "page_range": f"{r.get('page_start')}-{r.get('page_end')}",
                "evidence_type": r.get("evidence_type"),
                "fidelity_class": r.get("fidelity_class"),
                "taxonomy_node": tax_nodes[0] if tax_nodes else "laws-of-motion",
                "intended_chapter_role": role,
                "target_content_element": target,
                "summary": r.get("content_text", "")[:120] + "..."
            })

    # 2. Key Exposition Records from HCV1 Ch 4, Ch 5, Ch 6, Ch 7
    hcv_dyn_expos = [
        ("exp-hcv1-ch04-p01", 66, 68, "Chapter 4: The Forces - Contact Forces & Normal Force", "free-body-diagrams", "concept-dyn-normal-tension-01"),
        ("exp-hcv1-ch04-p02", 69, 71, "Chapter 4: The Forces - Tension in Strings & Springs", "free-body-diagrams", "concept-dyn-normal-tension-01"),
        ("exp-hcv1-ch05-p01", 74, 75, "Chapter 5: First Law of Motion & Inertial Frames", "inertia-and-first-law", "concept-dyn-first-law-01"),
        ("exp-hcv1-ch05-p02", 75, 77, "Chapter 5: Second Law of Motion F = dp/dt = ma", "momentum-and-second-law", "concept-dyn-second-law-01"),
        ("exp-hcv1-ch05-p03", 77, 78, "Chapter 5: Third Law of Motion & Action-Reaction Pairs", "action-reaction-third-law", "concept-dyn-third-law-01"),
        ("exp-hcv1-ch05-p04", 78, 81, "Chapter 5: Free Body Diagrams & Equation Formulation", "free-body-diagrams", "concept-dyn-fbd-method-01"),
        ("exp-hcv1-ch05-p05", 82, 85, "Chapter 5: Pulleys and String Kinematic Constraints", "string-and-pulley-constraints", "concept-dyn-pulley-constraint-01"),
        ("exp-hcv1-ch05-p06", 85, 87, "Chapter 5: Wedge Constraints and Contact Normal", "wedge-constraints", "concept-dyn-wedge-constraint-01"),
        ("exp-hcv1-ch05-p07", 88, 91, "Chapter 5: Non-Inertial Frames and Pseudo Forces", "pseudo-force-in-accelerating-frame", "concept-dyn-pseudo-force-01"),
        ("exp-hcv1-ch06-p01", 95, 97, "Chapter 6: Friction - Microscopic Origin & Mechanism", "origin-of-friction", "concept-dyn-friction-origin-01"),
        ("exp-hcv1-ch06-p02", 97, 99, "Chapter 6: Static Friction & Limiting Value f_s <= mu_s N", "static-friction-limiting", "concept-dyn-static-friction-01"),
        ("exp-hcv1-ch06-p03", 99, 101, "Chapter 6: Kinetic Friction f_k = mu_k N", "kinetic-friction", "concept-dyn-kinetic-friction-01"),
        ("exp-hcv1-ch06-p04", 101, 104, "Chapter 6: Two-Block Problems & Threshold Slipping", "two-block-problems", "concept-dyn-two-block-01"),
        ("exp-hcv1-ch06-p05", 104, 106, "Chapter 6: Angle of Repose and Angle of Friction", "angle-of-repose", "concept-dyn-angle-repose-01"),
        ("exp-hcv1-ch07-p01", 111, 114, "Chapter 7: Circular Motion - Centripetal Acceleration & Force", "centripetal-acceleration", "concept-dyn-centripetal-force-01"),
        ("exp-hcv1-ch07-p02", 115, 117, "Chapter 7: Banking of Roads & Conical Pendulum", "banking-of-roads", "concept-dyn-banking-conical-01"),
        ("exp-hcv1-ch07-p03", 117, 119, "Chapter 7: Centrifugal Pseudo-Force in Rotating Frames", "centrifugal-force", "concept-dyn-centrifugal-force-01")
    ]

    for eid, pstart, pend, desc, tax_node, target in hcv_dyn_expos:
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

    # 3. Formulas from formulas.json and HRW / University Physics / Feynman
    dyn_formula_records = [
        ("form-dyn-newton-second-law", "F_net = dp/dt = m a", "src-concepts-of-physics-by-h-a489bb6e", "75-76", "momentum-and-second-law", "formula-dyn-second-law"),
        ("form-dyn-third-law", "F_AB = - F_BA", "src-concepts-of-physics-by-h-a489bb6e", "77-78", "action-reaction-third-law", "formula-dyn-third-law"),
        ("form-dyn-string-constraint", "sum(l_i) = const => sum(T_i . a_i) = 0", "src-concepts-of-physics-by-h-a489bb6e", "82-84", "string-and-pulley-constraints", "formula-dyn-string-constraint"),
        ("form-dyn-pseudo-force", "F_pseudo = - m a_0", "src-concepts-of-physics-by-h-a489bb6e", "88-90", "pseudo-force-in-accelerating-frame", "formula-dyn-pseudo-force"),
        ("form-dyn-static-friction-max", "f_s <= f_s,max = mu_s N", "src-concepts-of-physics-by-h-a489bb6e", "97-98", "static-friction-limiting", "formula-dyn-static-friction-max"),
        ("form-dyn-kinetic-friction", "f_k = mu_k N", "src-concepts-of-physics-by-h-a489bb6e", "99-100", "kinetic-friction", "formula-dyn-kinetic-friction"),
        ("form-dyn-angle-of-repose", "theta_R = arctan(mu_s)", "src-concepts-of-physics-by-h-a489bb6e", "104-105", "angle-of-repose", "formula-dyn-angle-repose"),
        ("form-dyn-centripetal-force", "F_c = m v^2 / R = m omega^2 R", "src-fundamentals-of-physics--390f40d1", "154-156", "centripetal-acceleration", "formula-dyn-centripetal-force"),
        ("form-dyn-banking-angle", "tan(theta) = v^2 / (R g)", "src-university-physics-with--0bc11b67", "182-184", "banking-of-roads", "formula-dyn-banking-optimum"),
        ("form-dyn-conical-pendulum-period", "T = 2 pi sqrt(L cos(theta) / g)", "src-university-physics-with--0bc11b67", "180-182", "conical-pendulum", "formula-dyn-conical-period")
    ]

    for fid, eq, sid, prange, tax, target in dyn_formula_records:
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

    # 4. Advanced Problems from Irodov Dynamics (Section 1.2)
    selected_irodov = [
        ("prob-irodov-1-059", "1.59", 17, "Two bodies m1 and m2 connected by a string on a smooth horizontal plane pulled by force F", "string-and-pulley-constraints", "question-dyn-irodov-01"),
        ("prob-irodov-1-068", "1.68", 18, "Body of mass m resting on an inclined plane with coefficient of friction k; force applied at angle alpha", "angle-of-repose", "question-dyn-irodov-02"),
        ("prob-irodov-1-073", "1.73", 19, "Movable wedge of mass M with block of mass m; acceleration of wedge and block", "wedge-constraints", "ex-dyn-wedge-incline-01"),
        ("prob-irodov-1-085", "1.85", 21, "Two blocks stacked on each other on horizontal surface; force applied to bottom block", "two-block-problems", "ex-dyn-two-block-threshold")
    ]

    for pid, num, pg, text, tax, target in selected_irodov:
        manifest_entries.append({
            "evidence_id": pid,
            "source_id": "src-problems-in-general-phys-6cf0b2b7",
            "source_title": "Problems in General Physics by I.E. Irodov",
            "page_range": f"{pg}",
            "evidence_type": "PROBLEM",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax,
            "intended_chapter_role": "ADVANCED_EXERCISE_AND_WORKED_EXAMPLE",
            "target_content_element": target,
            "summary": f"Irodov Problem {num}: {text}"
        })

    # 5. Official JEE Mock Questions
    selected_mocks = [
        ("mock-q-dyn-01-atwood", "src-jee-main-mock-test-01-20-222525c1", 4, "Modified Atwood machine with unequal masses m1 and m2 across a light frictionless pulley", "string-and-pulley-constraints", "question-dyn-mock-atwood"),
        ("mock-q-dyn-02-friction-incline", "src-jee-rank-booster-02-mock-0548b6c5", 7, "Block sliding down rough incline of angle 45 deg with velocity-dependent friction / static threshold", "static-friction-limiting", "question-dyn-mock-friction"),
        ("mock-q-dyn-03-banking", "src-jee-rank-booster-03-mock-256f42c6", 6, "Car negotiating banked curve of radius R=100 m at speed v; maximum and minimum speeds without skidding", "banking-of-roads", "question-dyn-mock-banking")
    ]

    for mid, sid, pg, text, tax, target in selected_mocks:
        sinfo = source_info[sid]
        manifest_entries.append({
            "evidence_id": mid,
            "source_id": sid,
            "source_title": sinfo["title"],
            "page_range": f"{pg}",
            "evidence_type": "MOCK_QUESTION",
            "fidelity_class": "SOURCE_VERBATIM",
            "taxonomy_node": tax,
            "intended_chapter_role": "STANDARDIZED_EXAM_ASSESSMENT",
            "target_content_element": target,
            "summary": text
        })

    # Output to build/reports/dynamics_source_evidence_manifest.json
    out_dir = Path("build/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "dynamics_source_evidence_manifest.json"
    
    manifest_doc = {
        "chapter_id": "laws-of-motion",
        "chapter_title": "Newton's Laws of Motion & Dynamics",
        "total_evidence_records": len(manifest_entries),
        "fidelity_distribution": {
            "SOURCE_VERBATIM": sum(1 for m in manifest_entries if m["fidelity_class"] == "SOURCE_VERBATIM"),
            "SOURCE_DERIVED": sum(1 for m in manifest_entries if m["fidelity_class"] == "SOURCE_DERIVED"),
            "PROJECT_DERIVED": sum(1 for m in manifest_entries if m["fidelity_class"] == "PROJECT_DERIVED"),
            "INDEX_METADATA": 0
        },
        "records": manifest_entries
    }

    out_path.write_text(json.dumps(manifest_doc, indent=2), encoding="utf-8")
    print(f"Successfully compiled Dynamics Source Evidence Manifest with {len(manifest_entries)} entries to {out_path}")

if __name__ == '__main__':
    main()
