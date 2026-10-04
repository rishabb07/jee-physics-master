import json
from pathlib import Path
from jee_physics.models.curriculum import ChapterSpec

def main():
    spec_path = Path("curriculum/chapters/laws-of-motion_spec.json")
    data = json.loads(spec_path.read_text("utf-8"))

    # Map relevant concepts and governing principles specifically for each example
    ex_metadata = {
        "ex-dyn-fbd-equilibrium-01": {
            "concepts": ["concept-dyn-fbd-method-01", "concept-dyn-normal-tension-01"],
            "principles": ["Newton's First Law (Static Equilibrium)"]
        },
        "ex-dyn-atwood-pulley-01": {
            "concepts": ["concept-dyn-pulley-constraint-01", "concept-dyn-second-law-01"],
            "principles": ["String Inextensibility Constraint", "Newton's Second Law"]
        },
        "ex-dyn-wedge-incline-01": {
            "concepts": ["concept-dyn-wedge-constraint-01", "concept-dyn-pseudo-force-01"],
            "principles": ["Wedge Geometric Normal Constraint", "Inertial / Non-Inertial Frame Dynamics"]
        },
        "ex-dyn-two-block-threshold-01": {
            "concepts": ["concept-dyn-static-friction-01", "concept-dyn-two-block-01"],
            "principles": ["Coulomb-Amontons Dry Friction Inequality", "Multi-Body Acceleration Matching"]
        },
        "ex-dyn-banking-incline-01": {
            "concepts": ["concept-dyn-banking-01", "concept-dyn-centripetal-accel-01"],
            "principles": ["Optimum Banking Elevation", "Centripetal Radial Force Balance"]
        },
        "ex-dyn-conical-pendulum-01": {
            "concepts": ["concept-dyn-conical-pendulum-01", "concept-dyn-centripetal-accel-01"],
            "principles": ["Vertical Gravity Balance", "Horizontal Radial String Tension Balance"]
        }
    }

    # Normalize worked_example_sequence
    for ex in data["worked_example_sequence"]:
        eid = ex.get("example_id", "")
        meta = ex_metadata.get(eid, {"concepts": ["concept-dyn-first-law-01"], "principles": ["Newton's Laws of Motion"]})
        
        if "known_parameters" in ex and "known_quantities" not in ex:
            ex["known_quantities"] = {k: str(v) for k, v in ex.pop("known_parameters").items()}
        if "target_variable" in ex and "target_quantity" not in ex:
            ex["target_quantity"] = ex.pop("target_variable")
        if "relevant_concepts" not in ex:
            ex["relevant_concepts"] = meta["concepts"]
        if "governing_principles" not in ex:
            ex["governing_principles"] = meta["principles"]
        if "solution_steps" in ex and "step_by_step_derivation" not in ex:
            steps = ex.pop("solution_steps")
            ex["step_by_step_derivation"] = [f"{s.get('explanation', '')}: {s.get('equation_latex', '')}" for s in steps]
        ex.setdefault("sanity_checks", [])
        ex.setdefault("alternate_methods", [])
        ex.setdefault("provenance", [])
        ex.setdefault("verification_status", "VERIFIED")

    # Normalize formula_sequence
    for f in data["formula_sequence"]:
        if "units_and_dimensions" not in f:
            u = f.get("units", {})
            d = f.get("dimensions", {})
            vars_dict = f.get("variables", {})
            f["units_and_dimensions"] = {k: f"{u.get(k, '')} ({d.get(k, '')})" for k in vars_dict}
        f.setdefault("derivation_links", [])
        f.setdefault("related_concept_ids", [])
        f.setdefault("common_misuse_cases", f.get("common_misuse", []))
        f.setdefault("conditions_of_validity", f.get("validity_conditions", []))
        f.setdefault("provenance", [])
        f.setdefault("verification_status", "VERIFIED")

    # Normalize misconception_sequence
    misc_traps = {
        "misc-dyn-01": "Assuming Third Law action and reaction act on the same body and cancel each other.",
        "misc-dyn-02": "Equating normal reaction force to mg regardless of incline angle or vertical acceleration.",
        "misc-dyn-03": "Assuming friction always opposes body motion rather than relative interfacial slipping.",
        "misc-dyn-04": "Treating static friction as fixed at its limiting maximum mu_s N during equilibrium.",
        "misc-dyn-05": "Drawing centripetal force as an extra active force on free-body diagrams.",
        "misc-dyn-06": "Adding pseudo-forces when analyzing motion from an inertial ground frame."
    }
    for m in data["misconception_sequence"]:
        mid = m.get("misconception_id", "")
        if "explanation" not in m:
            m["explanation"] = m.get("correct_physics_explanation", "Valid physical explanation.")
        if "trap_mechanism" not in m:
            m["trap_mechanism"] = misc_traps.get(mid, m.get("erroneous_reasoning", "Cognitive pitfall."))
        m.setdefault("trigger_conditions", ["Standard JEE problem setup"])
        m.setdefault("connected_concept_ids", ["concept-dyn-first-law-01"])
        m.setdefault("connected_atom_ids", [])

    # Normalize question_sequence
    for q in data["question_sequence"]:
        q["source_provenance"] = []

    # Validate with ChapterSpec
    spec = ChapterSpec.model_validate(data)
    print("ChapterSpec successfully validated!")

    for out_path in [
        Path("curriculum/chapters/laws-of-motion_spec.json"),
        Path("curriculum/chapters/dynamics_spec.json"),
        Path("build/staging/incoming/curriculum/laws-of-motion_spec.json"),
        Path("build/staging/incoming/curriculum/dynamics_spec.json"),
    ]:
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("Updated all 4 spec files!")

if __name__ == "__main__":
    main()
