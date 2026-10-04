import json
from pathlib import Path

seg_dir = Path("sources/segments")
for fpath in seg_dir.glob("*.json"):
    data = json.loads(fpath.read_text(encoding="utf-8"))
    segments = data.get("segments", data if isinstance(data, list) else [])
    print(f"=== {fpath.name} ({len(segments)} segments) ===")
    for s in segments:
        title = s.get("title", s.get("section_title", s.get("chapter_title", "")))
        pstart = s.get("page_start", s.get("start_page"))
        pend = s.get("page_end", s.get("end_page"))
        if any(k in title.lower() for k in ["centre of mass", "center of mass", "momentum", "collision", "impulse"]):
            print(f"  Pages {pstart}-{pend}: {title}")
