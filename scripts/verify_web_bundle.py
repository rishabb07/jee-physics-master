"""
Verification script for Phase 16 web bundle.
Inspects output/web/data/chapter_rotational-motion.json and manifest.json.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "output" / "web" / "data"


def verify():
    ch_path = DATA_DIR / "chapter_rotational-motion.json"
    with open(ch_path, "r", encoding="utf-8") as f:
        d = json.load(f)

    print("Chapter title:", d.get("title"))
    print("Chapter branch:", d.get("branch"))
    print("Sections count:", len(d.get("sections", [])))
    print("Ladders:", d.get("ladder_ids"))

    total_c = 0
    total_f = 0
    total_d = 0
    total_e = 0
    total_m = 0
    total_q = 0

    for s in d.get("sections", []):
        sec_id = s["section_id"]
        c_count = len(s["concepts"])
        f_count = len(s["formulas"])
        d_count = len(s["derivations"])
        e_count = len(s["worked_examples"])
        m_count = len(s["misconceptions"])
        q_count = len(s["questions"])

        total_c += c_count
        total_f += f_count
        total_d += d_count
        total_e += e_count
        total_m += m_count
        total_q += q_count

        print(f"\n--- Section: {sec_id} ({s['title']}) ---")
        print(f"  Concepts ({c_count}): {[c['concept_id'] for c in s['concepts']]}")
        print(f"  Formulas ({f_count}): {[f['formula_id'] for f in s['formulas']]}")
        print(f"  Derivations ({d_count}): {[dv['derivation_id'] for dv in s['derivations']]}")
        print(f"  Examples ({e_count}): {[e['example_id'] for e in s['worked_examples']]}")
        print(f"  Misconceptions ({m_count}): {[m['misconception_id'] for m in s['misconceptions']]}")
        print(f"  Questions ({q_count}): {[q['question_id'] for q in s['questions']]}")

    print("\n=== TOTALS FOR ROTATIONAL MOTION CHAPTER ===")
    print(f"Concepts: {total_c}")
    print(f"Formulas: {total_f}")
    print(f"Derivations: {total_d}")
    print(f"Worked Examples: {total_e}")
    print(f"Misconceptions: {total_m}")
    print(f"Questions: {total_q}")

    # Check manifest
    with open(DATA_DIR / "manifest.json", "r", encoding="utf-8") as f:
        m = json.load(f)
    print("\n=== MANIFEST METRICS ===")
    print("Counts:", m.get("counts"))
    print("Content hashes count:", len(m.get("content_hashes", {})))

    # Check aliases
    aliases = [
        "chapter_rotation.json",
        "chapter_rigid-body-dynamics.json",
        "chapter_rbd.json",
        "chapter-rotational-motion.json",
    ]
    for a in aliases:
        ap = DATA_DIR / a
        print(f"Alias file {a} exists: {ap.exists()} (size: {ap.stat().st_size if ap.exists() else 0} bytes)")


if __name__ == "__main__":
    verify()
