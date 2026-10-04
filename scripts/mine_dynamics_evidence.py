import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def main():
    ev_dir = Path("sources/evidence")
    
    # Check section ledger
    print("=== Section Ledger for Laws of Motion / Dynamics ===")
    with open(ev_dir / "section_ledger.json", "r", encoding="utf-8") as f:
        ledger = json.load(f)
    print(f"Total ledger sections: {len(ledger)}")
    dyn_sections = [
        s for s in ledger
        if any(k in str(s).lower() for k in ["newton", "force", "friction", "laws of motion", "dynamics", "free body", "pseudo force"])
    ]
    print(f"Dynamics candidate sections in ledger: {len(dyn_sections)}")
    for s in dyn_sections[:15]:
        print(f"  [{s.get('source_id')[:25]}] Section: {s.get('section_id') or s.get('title')} | Pages: {s.get('page_start')}-{s.get('page_end')}")

    # Check exposition.json
    print("\n=== Exposition Records for Laws of Motion ===")
    with open(ev_dir / "exposition.json", "r", encoding="utf-8") as f:
        exposition = json.load(f)
    print(f"Total exposition records: {len(exposition)}")
    dyn_expo = [
        e for e in exposition
        if any(k in str(e).lower() for k in ["newton's laws", "second law", "third law", "friction", "pseudo force", "free body", "tension", "laws-of-motion"])
    ]
    print(f"Dynamics candidate exposition records: {len(dyn_expo)}")
    for e in dyn_expo[:10]:
        print(f"  [{e.get('evidence_id') or e.get('record_id')}] Source: {e.get('source_id')[:25]} | Page: {e.get('page_number')} | Title: {e.get('heading') or e.get('concept_title')}")

    # Check textbook_problems_ledger.json
    print("\n=== Textbook Problems for Laws of Motion ===")
    with open(ev_dir / "textbook_problems_ledger.json", "r", encoding="utf-8") as f:
        tb_probs = json.load(f)
    print(f"Total textbook problems: {len(tb_probs)}")
    dyn_probs = [
        p for p in tb_probs
        if any(k in str(p).lower() for k in ["newton", "friction", "pulley", "wedge", "incline", "laws of motion", "laws-of-motion"])
    ]
    print(f"Dynamics candidate textbook problems: {len(dyn_probs)}")
    for p in dyn_probs[:10]:
        print(f"  [{p.get('problem_id')}] Source: {p.get('source_id')[:25]} | Ch: {p.get('chapter_title') or p.get('chapter')} | Problem: {p.get('problem_number')}")

if __name__ == '__main__':
    main()
