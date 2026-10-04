import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def main():
    ev_dir = Path("sources/evidence")
    with open(ev_dir / "exposition.json", "r", encoding="utf-8") as f:
        expo = json.load(f)

    print("=== HCV1 Chapter 8 (Work and Energy) ===")
    hcv_wep = [e for e in expo if e.get("evidence_id", "").startswith("exp-hcv1-ch08")]
    print(f"Total HCV1 Ch 8: {len(hcv_wep)}")
    for e in hcv_wep:
        text_snip = e.get("content_text", "")[:100].replace("\n", " ")
        print(f"  {e['evidence_id']} | pp {e.get('page_start')}-{e.get('page_end')} | {text_snip}")

    print("\n=== Halliday / HRW Work & Energy ===")
    hrw_wep = [e for e in expo if "ch07" in e.get("evidence_id", "") or "ch08" in e.get("evidence_id", "")]
    hrw_wep = [e for e in hrw_wep if e.get("evidence_id", "").startswith("exp-hr")]
    print(f"Total HRW Ch 7 & 8: {len(hrw_wep)}")
    for e in hrw_wep:
        text_snip = e.get("content_text", "")[:100].replace("\n", " ")
        print(f"  {e['evidence_id']} | pp {e.get('page_start')}-{e.get('page_end')} | {text_snip}")

    print("\n=== University Physics Work & Energy ===")
    up_wep = [e for e in expo if "ch06" in e.get("evidence_id", "") or "ch07" in e.get("evidence_id", "")]
    up_wep = [e for e in up_wep if e.get("evidence_id", "").startswith("exp-up")]
    print(f"Total UP Ch 6 & 7: {len(up_wep)}")
    for e in up_wep:
        text_snip = e.get("content_text", "")[:100].replace("\n", " ")
        print(f"  {e['evidence_id']} | pp {e.get('page_start')}-{e.get('page_end')} | {text_snip}")

    print("\n=== Feynman Conservation of Energy / Work ===")
    feyn_wep = [e for e in expo if e.get("evidence_id", "").startswith("exp-feynman-lec04") or e.get("evidence_id", "").startswith("exp-feynman-lec13") or e.get("evidence_id", "").startswith("exp-feynman-lec14")]
    print(f"Total Feynman: {len(feyn_wep)}")
    for e in feyn_wep:
        text_snip = e.get("content_text", "")[:100].replace("\n", " ")
        print(f"  {e['evidence_id']} | pp {e.get('page_start')}-{e.get('page_end')} | {text_snip}")

if __name__ == "__main__":
    main()
