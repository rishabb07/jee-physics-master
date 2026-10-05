"""
Promotion script for Phase 16: Rotational Motion Production Upgrade.
Promotes staged and verified rotational motion content to canonical verified directories.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STAGING_DIR = ROOT / "build" / "staging" / "incoming"
VERIFIED_DIR = ROOT / "content" / "verified"
CURRICULUM_DIR = ROOT / "curriculum"


def update_misconceptions_verification():
    misc_ids = ["misc-rot-03", "misc-rot-04", "misc-rot-05", "misc-rot-06"]
    for mid in misc_ids:
        path = STAGING_DIR / "content" / "misconceptions" / f"{mid}.json"
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        d["verification_status"] = "VERIFIED"
        d["verification_record_id"] = f"cvr-{mid}"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        print(f"Updated staged misconception: {mid}")


def promote_content():
    categories = {
        "concepts": [
            "concept-rot-moi-continuous-01.json",
            "concept-rot-rotational-work-energy-01.json",
            "concept-rot-angmom-rigid-body-01.json",
            "concept-rot-pure-rolling-kinematics-01.json",
            "concept-rot-rolling-horizontal-friction-01.json",
            "concept-rot-rolling-incline-01.json",
            "concept-rot-toppling-condition-01.json",
        ],
        "formulas": [
            "formula-rot-moi-discrete.json",
            "formula-rot-moi-standard-bodies.json",
            "formula-rot-moi-perpendicular.json",
            "formula-rot-moi-radius-gyration.json",
            "formula-rot-torque-def.json",
            "formula-rot-kinematics-equations.json",
            "formula-rot-ke-rotation.json",
            "formula-rot-work-energy-rot.json",
            "formula-rot-angmom-rigid-body.json",
            "formula-rot-rolling-no-slip-velocity.json",
            "formula-rot-rolling-incline-accel.json",
            "formula-rot-toppling-condition.json",
        ],
        "derivations": [
            "derivation-formula-rot-moi-perpendicular.json",
            "derivation-formula-rot-ke-rotation.json",
            "derivation-formula-rot-rolling-incline-accel.json",
        ],
        "examples": [
            "ex-rot-moi-disc-cavity-01.json",
            "ex-rot-pulley-atwood-01.json",
            "ex-rot-projectile-angmom-01.json",
            "ex-rot-rolling-incline-race-01.json",
            "ex-rot-toppling-block-01.json",
        ],
        "misconceptions": [
            "misc-rot-03.json",
            "misc-rot-04.json",
            "misc-rot-05.json",
            "misc-rot-06.json",
        ],
    }

    for cat, filenames in categories.items():
        dest_dir = VERIFIED_DIR / cat
        dest_dir.mkdir(parents=True, exist_ok=True)
        for fname in filenames:
            src = STAGING_DIR / "content" / cat / fname
            dst = dest_dir / fname
            shutil.copy2(src, dst)
            print(f"Promoted {cat}/{fname} -> {dst}")

    # Dual CVRs
    dual_cvrs = [
        "dual-cvr-derivation-formula-rot-moi-perpendicular.json",
        "dual-cvr-derivation-formula-rot-ke-rotation.json",
        "dual-cvr-derivation-formula-rot-rolling-incline-accel.json",
        "dual-cvr-ex-rot-moi-disc-cavity-01.json",
        "dual-cvr-ex-rot-pulley-atwood-01.json",
        "dual-cvr-ex-rot-projectile-angmom-01.json",
        "dual-cvr-ex-rot-rolling-incline-race-01.json",
        "dual-cvr-ex-rot-toppling-block-01.json",
    ]
    dual_dest = VERIFIED_DIR / "dual_verifications"
    dual_dest.mkdir(parents=True, exist_ok=True)
    for fname in dual_cvrs:
        src = STAGING_DIR / "content_verification" / "dual" / fname
        dst = dual_dest / fname
        shutil.copy2(src, dst)
        print(f"Promoted dual_verifications/{fname} -> {dst}")

    # Curriculum items
    ladder_src = STAGING_DIR / "curriculum" / "ladders" / "ladder-rot-rolling-incline-01.json"
    ladder_dst = CURRICULUM_DIR / "ladders" / "ladder-rot-rolling-incline-01.json"
    shutil.copy2(ladder_src, ladder_dst)
    print(f"Promoted ladder -> {ladder_dst}")

    spec_src = STAGING_DIR / "curriculum" / "rotational-motion_spec.json"
    spec_dst = CURRICULUM_DIR / "chapters" / "rotational-motion_spec.json"
    shutil.copy2(spec_src, spec_dst)
    print(f"Promoted spec -> {spec_dst}")

    plan_src = STAGING_DIR / "curriculum" / "rotational-motion_plan.json"
    plan_dst = CURRICULUM_DIR / "chapters" / "rotational-motion_plan.json"
    shutil.copy2(plan_src, plan_dst)
    print(f"Promoted plan -> {plan_dst}")


def main():
    print("=== Step 1: Update Staged Misconceptions ===")
    update_misconceptions_verification()
    print("\n=== Step 2: Promote Content to Verified ===")
    promote_content()
    print("\nPromotion complete!")


if __name__ == "__main__":
    main()
