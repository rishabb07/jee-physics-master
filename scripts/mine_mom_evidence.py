import json
from pathlib import Path

evidence_dir = Path("sources/evidence")
for fname in ["records.json", "exposition.json", "formulas.json", "derivations.json", "examples.json", "problems.json", "irodov_problems.json", "mock_questions.json"]:
    fpath = evidence_dir / fname
    if not fpath.exists():
        continue
    data = json.loads(fpath.read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("records", data.get("problems", data.get("questions", [])))
    if isinstance(items, dict):
        items = list(items.values())
    
    com_matches = []
    for item in items:
        # Check taxonomy or text
        tax = str(item.get("taxonomy", item.get("taxonomy_node", "")))
        txt = str(item.get("text", item.get("statement", item.get("formula", item.get("title", "")))))
        src = str(item.get("source_id", item.get("source", "")))
        if "center-of-mass" in tax or "collision" in tax or "momentum" in tax or "impulse" in tax or "center of mass" in txt.lower() or "collision" in txt.lower():
            com_matches.append(item)
    print(f"{fname}: {len(com_matches)} matches out of {len(items)}")
