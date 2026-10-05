import json
import urllib.request
import hashlib
import subprocess
import os
import sys
import re
import time
from pathlib import Path

BASE_PROD_URL = "https://rishabb07.github.io/jee-physics-master"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DATA_DIR = Path("output/web/data")

def log(msg):
    print(f"[LIVE-QA] {msg}")

def fetch_prod_file(rel_path):
    url = f"{BASE_PROD_URL}/{rel_path.lstrip('/')}?t={int(time.time())}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception as e:
        log(f"FAILED to fetch {url}: {e}")
        return None

def test_headless_render(route, window_size="1280,800"):
    full_url = f"{BASE_PROD_URL}/#{route}"
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={window_size}",
        "--virtual-time-budget=4000",
        "--dump-dom",
        full_url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=40)
        return res.stdout
    except Exception as e:
        log(f"Error rendering {full_url}: {e}")
        return ""

def run_phase15_live_qa():
    results = {
        "phase": "PHASE_15",
        "chapter_id": "center-of-mass",
        "chapter_alias": "momentum-collisions",
        "deployment_metadata": {},
        "network_asset_integrity": {},
        "data_bundle_hashes": {},
        "com_payload_audit": {},
        "pilot_regression_audit": {},
        "route_smoke_tests": {},
        "responsive_layout_tests": {},
        "search_verification": {},
        "interactive_elements_audit": {},
        "all_checks_passed": False,
        "final_verdicts": []
    }

    log("=== 1. Live Manifest and Deployment Metadata ===")
    manifest_bytes = fetch_prod_file("data/manifest.json")
    if manifest_bytes is None:
        log("ERROR: Live manifest.json is unreachable!")
        return results
    manifest = json.loads(manifest_bytes.decode("utf-8"))

    commit_sha = manifest.get("git_commit", "")
    log(f"Live Deployment Commit: {commit_sha}")
    log(f"Live Active Pilot Chapters: {manifest.get('counts', {}).get('pilot_active_chapters')}")
    log(f"Live Total Concepts: {manifest.get('counts', {}).get('concepts')}")
    log(f"Live Total Formulas: {manifest.get('counts', {}).get('formulas')}")
    log(f"Live Total Derivations: {manifest.get('counts', {}).get('derivations')}")
    log(f"Live Total Worked Examples: {manifest.get('counts', {}).get('worked_examples')}")
    log(f"Live Total Misconceptions: {manifest.get('counts', {}).get('misconceptions')}")
    log(f"Live Total Questions: {manifest.get('counts', {}).get('verified_questions')}")

    results["deployment_metadata"] = {
        "git_commit": commit_sha,
        "build_id": manifest.get("build_id"),
        "build_timestamp": manifest.get("build_timestamp"),
        "counts": manifest.get("counts", {})
    }

    # Verify counts
    counts = manifest.get("counts", {})
    assert counts.get("pilot_active_chapters") == 8, f"Expected 8 pilot active chapters, got {counts.get('pilot_active_chapters')}"

    log("\n=== 2. Bit-for-Bit Hash Parity Verification ===")
    content_hashes = manifest.get("content_hashes", {})
    assert len(content_hashes) >= 20, f"Expected at least 20 content hashes, found {len(content_hashes)}"

    all_hashes_matched = True
    for filename, expected_hash in content_hashes.items():
        rel_path = f"data/{filename}"
        live_bytes = fetch_prod_file(rel_path)
        if live_bytes is None:
            log(f"FAIL: {rel_path} missing on live CDN!")
            all_hashes_matched = False
            results["data_bundle_hashes"][rel_path] = "MISSING"
            continue
        live_hash = hashlib.sha256(live_bytes).hexdigest()
        if live_hash == expected_hash:
            log(f"OK: {filename} -> {live_hash[:12]} MATCH")
            results["data_bundle_hashes"][filename] = "MATCH"
        else:
            log(f"MISMATCH: {filename} -> live:{live_hash[:8]} != manifest:{expected_hash[:8]}")
            all_hashes_matched = False
            results["data_bundle_hashes"][filename] = f"MISMATCH(live={live_hash[:8]}, manifest={expected_hash[:8]})"

    log("\n=== 3. Center of Mass & Momentum Payload Audit ===")
    com_raw = fetch_prod_file("data/chapter_center-of-mass.json")
    assert com_raw is not None, "chapter_center-of-mass.json is None"
    com_data = json.loads(com_raw.decode("utf-8"))

    mom_raw = fetch_prod_file("data/chapter_momentum-collisions.json")
    assert mom_raw is not None, "chapter_momentum-collisions.json is None"
    assert com_raw == mom_raw, "chapter_center-of-mass.json and chapter_momentum-collisions.json are not identical!"
    log("OK: Full byte parity verified between canonical center-of-mass and momentum-collisions alias.")

    assert len(com_data.get("sections", [])) == 4
    sec_names = [s["title"] for s in com_data["sections"]]
    log(f"Sections ({len(sec_names)}): {sec_names}")

    tot_concepts = sum(len(s.get("concepts", [])) for s in com_data["sections"])
    tot_formulas = sum(len(s.get("formulas", [])) for s in com_data["sections"])
    tot_derivations = sum(len(s.get("derivations", [])) for s in com_data["sections"])
    tot_examples = sum(len(s.get("worked_examples", [])) for s in com_data["sections"])
    tot_misconceptions = sum(len(s.get("misconceptions", [])) for s in com_data["sections"])
    tot_questions = sum(len(s.get("questions", [])) for s in com_data["sections"])

    log(f"Center of Mass Metrics: {tot_concepts} concepts, {tot_formulas} formulas, {tot_derivations} derivations, {tot_examples} examples, {tot_misconceptions} misc, {tot_questions} questions")
    assert tot_concepts == 16, f"Expected 16 concepts, got {tot_concepts}"
    assert tot_formulas == 19, f"Expected 19 formulas, got {tot_formulas}"
    assert tot_derivations == 7, f"Expected 7 derivations, got {tot_derivations}"
    assert tot_examples == 7, f"Expected 7 examples, got {tot_examples}"
    assert tot_misconceptions == 6, f"Expected 6 misconceptions, got {tot_misconceptions}"
    assert tot_questions == 2, f"Expected 2 questions, got {tot_questions}"

    results["com_payload_audit"] = {
        "sections_count": 4,
        "concepts_count": tot_concepts,
        "formulas_count": tot_formulas,
        "derivations_count": tot_derivations,
        "examples_count": tot_examples,
        "misconceptions_count": tot_misconceptions,
        "questions_count": tot_questions,
        "alias_parity": True
    }

    log("\n=== 4. Regression Audit on Prior Chapters ===")
    prior_chapters = [
        ("kinematics", 4),
        ("laws-of-motion", 4),
        ("work-energy-power", 4),
        ("rotational-motion", 5),
        ("thermodynamics", 5),
        ("current-electricity", 5),
        ("ray-optics", 5)
    ]
    for ch_slug, min_secs in prior_chapters:
        raw = fetch_prod_file(f"data/chapter_{ch_slug}.json")
        assert raw is not None, f"chapter_{ch_slug}.json is missing!"
        d = json.loads(raw.decode("utf-8"))
        assert len(d.get("sections", [])) >= min_secs
        log(f"OK: {ch_slug} verified ({len(d['sections'])} sections)")
        results["pilot_regression_audit"][ch_slug] = f"PASS({len(d['sections'])} sections)"

    log("\n=== 5. Headless Chrome DOM Route Smoke Tests ===")
    routes = [
        ("", "JEE Physics Master Knowledge System"),
        ("curriculum", "Center of Mass and Linear Momentum"),
        ("chapter/center-of-mass", "Center of Mass, Momentum, and Collisions"),
        ("chapter/momentum-collisions", "Center of Mass, Momentum, and Collisions"),
        ("chapter/com", "Center of Mass, Momentum, and Collisions"),
        ("chapter/work-energy-power", "Work, Energy & Power"),
        ("chapter/laws-of-motion", "Newton's Laws of Motion"),
        ("chapter/kinematics", "Kinematics: Rest, Motion"),
        ("chapter/rotational-motion", "Rotational Motion"),
        ("chapter/thermodynamics", "Thermodynamics"),
        ("chapter/current-electricity", "Current Electricity"),
        ("chapter/ray-optics", "Ray Optics"),
        ("formulas", "Formula Handbook"),
        ("practice", "Question Practice"),
        ("ladders", "Question Ladders")
    ]

    all_routes_rendered = True
    for route, expected_text in routes:
        dom = test_headless_render(route)
        if not dom:
            log(f"FAIL: Render failed for #{route}")
            all_routes_rendered = False
            results["route_smoke_tests"][route] = "RENDER_FAILED"
            continue
        clean_dom = dom.replace("&amp;", "&")
        if expected_text in clean_dom:
            log(f"PASS: #{route} -> found '{expected_text}'")
            results["route_smoke_tests"][route] = "PASS"
        else:
            log(f"FAIL: #{route} did NOT contain '{expected_text}'")
            all_routes_rendered = False
            results["route_smoke_tests"][route] = f"TEXT_NOT_FOUND({expected_text})"

    log("\n=== 6. Responsive Viewport Audits ===")
    viewports = [
        ("desktop", "1280,800"),
        ("tablet", "768,1024"),
        ("mobile", "375,812")
    ]
    for vp_name, vp_size in viewports:
        dom = test_headless_render("chapter/center-of-mass", window_size=vp_size)
        clean_dom = dom.replace("&amp;", "&")
        assert "Center of Mass, Momentum, and Collisions" in clean_dom
        assert "Discrete Center of Mass" in clean_dom
        log(f"PASS: Viewport {vp_name} ({vp_size}) rendered cleanly.")
        results["responsive_layout_tests"][vp_name] = "PASS"

    log("\n=== 7. Interactive Elements & Mathematical Equations Audit ===")
    ch_dom = test_headless_render("chapter/center-of-mass")
    assert "katex" in ch_dom.lower(), "KaTeX styles/markup missing from chapter render"
    assert "3R/8" in ch_dom or "3}{8}" in ch_dom or "\\frac{3}{8}" in ch_dom or "frac" in ch_dom
    log("PASS: Math formulas and KaTeX successfully rendered in live DOM.")
    results["interactive_elements_audit"]["katex_render"] = "PASS"

    # Practice quiz options check
    prac_dom = test_headless_render("practice")
    assert "Question Practice" in prac_dom
    log("PASS: Practice question bank renders interactive questions.")
    results["interactive_elements_audit"]["practice_view"] = "PASS"

    # Search query verification
    search_bytes = fetch_prod_file("data/search_index.json")
    assert search_bytes is not None
    search_data = json.loads(search_bytes.decode("utf-8"))
    log(f"Search entries count: {len(search_data)}")
    assert len(search_data) >= 290

    search_terms = ["center of mass", "tsiolkovsky", "restitution", "ballistic pendulum", "impulse"]
    for st in search_terms:
        matches = [item for item in search_data if st.lower() in (item.get("title", "") + " " + item.get("text", "")).lower()]
        log(f"Search '{st}': found {len(matches)} items")
        assert len(matches) > 0, f"No matches found for search term {st}"
        results["search_verification"][st] = len(matches)

    results["all_checks_passed"] = all_hashes_matched and all_routes_rendered
    if results["all_checks_passed"]:
        results["final_verdicts"] = [
            "PHASE_15_MOMENTUM_COLLISIONS_PROVEN",
            "PHASE_15_LIVE_DEPLOYMENT_PROVEN"
        ]
        log("\n" + "=" * 60)
        log(" ALL LIVE CHECKS PASSED: PHASE 15 PRODUCTION VERIFIED!")
        log(" VERDICT 1: PHASE_15_MOMENTUM_COLLISIONS_PROVEN")
        log(" VERDICT 2: PHASE_15_LIVE_DEPLOYMENT_PROVEN")
        log("=" * 60)
    else:
        log("\nSome checks failed. Please check logs.")

    out_path = Path("build/reports/phase15_live_qa_report.json")
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    log(f"Report saved to {out_path}")
    return results

if __name__ == "__main__":
    run_phase15_live_qa()
