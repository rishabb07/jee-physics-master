import json
import sys
from pathlib import Path

def main():
    ev_dir = Path("sources/evidence")
    
    # 1. Section Ledger
    print("=== Section Ledger for Work, Energy & Power ===")
    with open(ev_dir / "section_ledger.json", "r", encoding="utf-8") as f:
        ledger = json.load(f)
    print(f"Total ledger sections: {len(ledger)}")
    wep_keywords = ["work", "kinetic energy", "potential energy", "power", "conservative force", "work-energy", "work and energy", "energy conservation"]
    wep_sections = [
        s for s in ledger
        if any(k in str(s).lower() for k in wep_keywords)
    ]
    print(f"WEP candidate sections in ledger: {len(wep_sections)}")
    for s in wep_sections[:15]:
        sid = s.get("source_id", "")[:30]
        title = s.get("section_id") or s.get("title") or s.get("heading")
        pstart = s.get("page_start") or s.get("page_number")
        pend = s.get("page_end") or s.get("page_number")
        print(f"  [{sid}] Section: {title} | Pages: {pstart}-{pend}")

    # 2. Exposition records
    print("\n=== Exposition Records for Work, Energy & Power ===")
    with open(ev_dir / "exposition.json", "r", encoding="utf-8") as f:
        exposition = json.load(f)
    print(f"Total exposition records: {len(exposition)}")
    wep_expo = [
        e for e in exposition
        if any(k in str(e).lower() for k in ["work-energy-power", "work done", "kinetic energy", "work-energy theorem", "potential energy", "conservative force", "spring force", "vertical circle", "instantaneous power"])
    ]
    print(f"WEP candidate exposition records: {len(wep_expo)}")
    for e in wep_expo[:10]:
        eid = e.get("evidence_id") or e.get("record_id")
        sid = e.get("source_id", "")[:30]
        page = e.get("page_number") or e.get("page")
        heading = e.get("heading") or e.get("concept_title") or e.get("title")
        print(f"  [{eid}] Source: {sid} | Page: {page} | Title: {heading}")

    # 3. Formulas
    print("\n=== Formulas for Work, Energy & Power ===")
    if (ev_dir / "formulas.json").exists():
        with open(ev_dir / "formulas.json", "r", encoding="utf-8") as f:
            formulas = json.load(f)
        wep_forms = [f for f in formulas if any(k in str(f).lower() for k in ["work", "kinetic energy", "potential energy", "power", "spring", "work-energy"])]
        print(f"WEP candidate formulas: {len(wep_forms)}")
        for f in wep_forms[:10]:
            print(f"  [{f.get('formula_id') or f.get('record_id')}] Expr: {f.get('latex') or f.get('expression') or f.get('name')}")

    # 4. Derivations
    print("\n=== Derivations for Work, Energy & Power ===")
    if (ev_dir / "derivations.json").exists():
        with open(ev_dir / "derivations.json", "r", encoding="utf-8") as f:
            derivs = json.load(f)
        wep_derivs = [d for d in derivs if any(k in str(d).lower() for k in ["work", "kinetic energy", "potential energy", "power", "work-energy"])]
        print(f"WEP candidate derivations: {len(wep_derivs)}")
        for d in wep_derivs[:10]:
            print(f"  [{d.get('derivation_id') or d.get('record_id')}] Target: {d.get('target_formula') or d.get('title')}")

    # 5. Examples
    print("\n=== Examples for Work, Energy & Power ===")
    if (ev_dir / "examples.json").exists():
        with open(ev_dir / "examples.json", "r", encoding="utf-8") as f:
            examples = json.load(f)
        wep_exs = [ex for ex in examples if any(k in str(ex).lower() for k in ["work", "kinetic energy", "potential energy", "spring", "power", "vertical circle"])]
        print(f"WEP candidate examples: {len(wep_exs)}")
        for ex in wep_exs[:10]:
            print(f"  [{ex.get('example_id') or ex.get('record_id')}] Title: {ex.get('title') or ex.get('problem_statement', '')[:60]}")

    # 6. Problems & Irodov
    print("\n=== Textbook Problems & Irodov for Work, Energy & Power ===")
    with open(ev_dir / "textbook_problems_ledger.json", "r", encoding="utf-8") as f:
        tb_probs = json.load(f)
    wep_tb = [p for p in tb_probs if any(k in str(p).lower() for k in ["work", "energy", "power", "work-energy-power"])]
    print(f"WEP candidate textbook problems: {len(wep_tb)}")

    with open(ev_dir / "irodov_problems.json", "r", encoding="utf-8") as f:
        irodov = json.load(f)
    wep_irodov = [p for p in irodov if any(k in str(p).lower() for k in ["work", "kinetic energy", "potential energy", "power", "spring"])]
    print(f"WEP candidate Irodov problems: {len(wep_irodov)}")

if __name__ == "__main__":
    main()
