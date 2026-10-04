import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def main():
    ev_dir = Path("sources/evidence")
    with open(ev_dir / "records.json", "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"Total records in records.json: {len(records)}")
    dyn_recs = [
        r for r in records
        if any(c in str(r.get("source_reference", "")).lower() or c in str(r.get("taxonomy_node_id", "")).lower() or c in str(r.get("evidence_id", "")).lower()
               for c in ["ch04", "ch05", "ch06", "laws-of-motion", "newton", "friction"])
    ]
    print(f"Dynamics records count: {len(dyn_recs)}")
    for r in dyn_recs[:10]:
        print(f"ID: {r.get('evidence_id')} | Type: {r.get('evidence_type')} | Class: {r.get('fidelity_class')} | Ref: {r.get('source_reference')}")

if __name__ == '__main__':
    main()
