import json
from pathlib import Path

seg_files = {
    "HRW": "src-fundamentals-of-physics--390f40d1_segments.json",
    "UP": "src-university-physics-with--0bc11b67_segments.json",
    "Feynman": "src-feynman-richard-p-the-fe-486f6a95_segments.json",
    "Irodov": "src-problems-in-general-phys-6cf0b2b7_segments.json"
}

for name, fname in seg_files.items():
    fpath = Path("sources/segments") / fname
    if not fpath.exists():
        continue
    data = json.loads(fpath.read_text(encoding="utf-8"))
    print(f"=== {name} ===")
    for s in data.get("segments", []):
        stitle = s.get("segment_title", "")
        ssummary = s.get("segment_summary", "")
        pstart = s.get("page_start")
        pend = s.get("page_end")
        combined = f"{stitle} {ssummary}".lower()
        if any(k in combined for k in ["center of mass", "centre of mass", "momentum", "collision", "impulse"]):
            print(f"  Pages {pstart}-{pend}: {stitle} | {ssummary[:80]}")
