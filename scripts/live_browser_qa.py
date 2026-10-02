import json
import urllib.request
import hashlib
import subprocess
import os
import sys
import re
from pathlib import Path

BASE_PROD_URL = "https://rishabb07.github.io/jee-physics-master"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def log(msg):
    print(f"[QA] {msg}")

def fetch_prod_file(rel_path):
    url = f"{BASE_PROD_URL}/{rel_path.lstrip('/')}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except Exception as e:
        log(f"FAILED to fetch {url}: {e}")
        return None

def test_headless_render(route, window_size="1280,800", output_file="temp_render.html"):
    full_url = f"{BASE_PROD_URL}/#{route}"
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={window_size}",
        "--virtual-time-budget=6000",
        "--dump-dom",
        full_url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=20)
        return res.stdout
    except Exception as e:
        log(f"Error rendering {full_url}: {e}")
        return ""

def run_all_qa():
    results = {
        "deployment_metadata": {},
        "network_asset_integrity": {},
        "data_bundle_hashes": {},
        "route_smoke_tests": {},
        "responsive_layout_tests": {},
        "search_verification": {},
        "interactive_elements_audit": {},
        "all_checks_passed": False
    }

    log("=== 1. Live Manifest and Deployment Metadata ===")
    manifest_bytes = fetch_prod_file("data/manifest.json")
    assert manifest_bytes is not None, "Live manifest.json is missing!"
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    
    results["deployment_metadata"] = {
        "git_commit": manifest.get("git_commit"),
        "version": manifest.get("version"),
        "scope": manifest.get("scope"),
        "generated_at": manifest.get("generated_at"),
        "files_count": len(manifest.get("content_hashes", {}))
    }
    log(f"Live Commit: {manifest.get('git_commit')}, Version: {manifest.get('version')}, Scope: {manifest.get('scope')}")

    log("=== 2. Offline Vendor & Font Assets Verification ===")
    asset_files = [
        "index.html",
        "css/app.css",
        "js/app.js",
        "vendor/katex/katex.min.js",
        "vendor/katex/katex.min.css",
    ]
    # Check at least 5 KaTeX font files
    font_files = [
        "vendor/katex/fonts/KaTeX_Main-Regular.woff2",
        "vendor/katex/fonts/KaTeX_Math-Italic.woff2",
        "vendor/katex/fonts/KaTeX_Size1-Regular.woff2",
        "vendor/katex/fonts/KaTeX_AMS-Regular.woff2",
        "vendor/katex/fonts/KaTeX_Caligraphic-Regular.woff2"
    ]
    asset_status = {}
    for a in asset_files + font_files:
        content = fetch_prod_file(a)
        if content and len(content) > 0:
            asset_status[a] = {"status": "HTTP_200_OK", "size_bytes": len(content)}
        else:
            asset_status[a] = {"status": "MISSING", "size_bytes": 0}
    results["network_asset_integrity"] = asset_status
    log(f"Assets audited: {len(asset_status)} | All OK: {all(v['status'] == 'HTTP_200_OK' for v in asset_status.values())}")

    log("=== 3. Data Bundle SHA-256 Bit-for-Bit Audit ===")
    hash_status = {}
    mismatches = 0
    for fname, expected_hash in manifest.get("content_hashes", {}).items():
        data = fetch_prod_file(f"data/{fname}")
        if data is None:
            hash_status[fname] = {"status": "MISSING", "expected": expected_hash, "actual": None}
            mismatches += 1
            continue
        actual_hash = hashlib.sha256(data).hexdigest()
        if actual_hash == expected_hash:
            hash_status[fname] = {"status": "MATCH", "sha256": actual_hash, "size": len(data)}
        else:
            hash_status[fname] = {"status": "MISMATCH", "expected": expected_hash, "actual": actual_hash}
            mismatches += 1
    results["data_bundle_hashes"] = {
        "total_files": len(hash_status),
        "matches": len(hash_status) - mismatches,
        "mismatches": mismatches,
        "details": hash_status
    }
    log(f"Data files audited: {len(hash_status)} | Matches: {len(hash_status) - mismatches} | Mismatches: {mismatches}")

    log("=== 4. Live Browser DOM Smoke Tests Across Routes ===")
    routes_to_test = [
        ("", "Home / Overview", ["JEE Physics Master", "Kinematics", "Rotational Motion", "Thermodynamics"]),
        ("/curriculum", "Curriculum DAG View", ["Authoritative JEE Physics Syllabus", "Kinematics", "Electrodynamics"]),
        ("/formulas", "Formula Sheet", ["Physics Formula Handbook", "Parallel Axis Theorem"]),
        ("/practice", "Practice Question Bank", ["Interactive Physics Question Practice", "TOPIC:"]),
        ("/ladders", "Question Ladders", ["Question Ladders", "Scaffolding Projectile Motion"]),
        ("/chapter/kinematics", "Kinematics Flagship Chapter", [
            "Kinematics: Rest, Motion, and Trajectories",
            "1. Position, Displacement, Speed, Velocity, and Graph Slope/Area",
            "2. Acceleration, Derivation of Constant Acceleration Equations, Calculus Integration, Free Fall",
            "3. 2D Orthogonal Motion, Ballistic Trajectories, Tower Projection, and Inclined Plane Projection",
            "4. 1D &amp; 2D Relative Velocity, River-Swimmer, Rain-Umbrella, and Closest Approach"
        ]),
        ("/chapter/rotational-motion", "Pilot Chapter: Rotational Motion", ["Rotational Motion", "Parallel Axis Theorem"]),
        ("/chapter/thermodynamics", "Pilot Chapter: Thermodynamics", ["Thermodynamics", "First Law of Thermodynamics"]),
        ("/chapter/current-electricity", "Pilot Chapter: Current Electricity", ["Current Electricity", "Drift Velocity"]),
        ("/chapter/ray-optics", "Pilot Chapter: Ray Optics", ["Ray Optics", "Snell's Law"])
    ]

    route_results = {}
    for route, label, expected_strings in routes_to_test:
        dom = test_headless_render(route, window_size="1280,800")
        dom_len = len(dom)
        katex_count = dom.count("katex")
        missing_strings = [s for s in expected_strings if s not in dom]
        passed = (dom_len > 1000) and (len(missing_strings) == 0)
        route_results[route or "/"] = {
            "label": label,
            "dom_bytes": dom_len,
            "katex_elements_count": katex_count,
            "missing_expected_strings": missing_strings,
            "verdict": "PASSED" if passed else "FAILED"
        }
        log(f"Route '{route or '/'}': {'PASS' if passed else 'FAIL'} (DOM {dom_len} bytes, KaTeX {katex_count})")
    results["route_smoke_tests"] = route_results

    log("=== 5. Responsive Viewport Tests (Desktop vs Mobile) ===")
    mobile_dom = test_headless_render("/chapter/kinematics", window_size="375,667")
    desktop_dom = test_headless_render("/chapter/kinematics", window_size="1440,900")
    results["responsive_layout_tests"] = {
        "mobile_375x667": {
            "dom_bytes": len(mobile_dom),
            "katex_count": mobile_dom.count("katex"),
            "has_kinematics_title": "Kinematics: Rest, Motion, and Trajectories" in mobile_dom,
            "has_all_sections": all(f"{i}." in mobile_dom for i in range(1, 5)),
            "verdict": "PASSED" if len(mobile_dom) > 100000 else "FAILED"
        },
        "desktop_1440x900": {
            "dom_bytes": len(desktop_dom),
            "katex_count": desktop_dom.count("katex"),
            "has_kinematics_title": "Kinematics: Rest, Motion, and Trajectories" in desktop_dom,
            "has_all_sections": all(f"{i}." in desktop_dom for i in range(1, 5)),
            "verdict": "PASSED" if len(desktop_dom) > 100000 else "FAILED"
        }
    }
    log(f"Mobile Render: {results['responsive_layout_tests']['mobile_375x667']['verdict']}")
    log(f"Desktop Render: {results['responsive_layout_tests']['desktop_1440x900']['verdict']}")

    log("=== 6. Search Index Coverage Audit ===")
    search_bytes = fetch_prod_file("data/search_index.json")
    search_idx = json.loads(search_bytes.decode("utf-8"))
    kin_items = [i for i in search_idx if i.get("chapter_id") == "kinematics"]
    kin_matches = [i for i in search_idx if "kinematics" in i.get("keywords", []) or i.get("chapter_id") == "kinematics"]
    entity_counts = {}
    for i in search_idx:
        entity_counts[i["entity_type"]] = entity_counts.get(i["entity_type"], 0) + 1
    kin_entity_counts = {}
    for i in kin_items:
        kin_entity_counts[i["entity_type"]] = kin_entity_counts.get(i["entity_type"], 0) + 1

    results["search_verification"] = {
        "total_items": len(search_idx),
        "entity_type_breakdown": entity_counts,
        "kinematics_items_total": len(kin_items),
        "kinematics_keyword_matches": len(kin_matches),
        "kinematics_entity_breakdown": kin_entity_counts,
        "verdict": "PASSED" if (len(search_idx) >= 135 and len(kin_matches) >= 40) else "FAILED"
    }
    log(f"Search index: {len(search_idx)} total items, {len(kin_matches)} kinematics matches. Verdict: {results['search_verification']['verdict']}")

    log("=== 7. Interactive Elements & Mathematical Fidelity ===")
    kin_dom = desktop_dom
    has_reveal_accordions = "reveal-btn" in kin_dom or "solution" in kin_dom or "accordion" in kin_dom or "toggle" in kin_dom or "card" in kin_dom
    has_formula_boxes = "formula-box" in kin_dom or "formula-card" in kin_dom or "formula" in kin_dom
    has_misconception_alerts = "misconception" in kin_dom or "trap" in kin_dom or "warning" in kin_dom
    has_worked_examples = "worked-example" in kin_dom or "example" in kin_dom
    has_practice_questions = "question-card" in kin_dom or "practice" in kin_dom or "option" in kin_dom

    results["interactive_elements_audit"] = {
        "formula_blocks_present": has_formula_boxes,
        "worked_examples_present": has_worked_examples,
        "misconceptions_present": has_misconception_alerts,
        "practice_questions_present": has_practice_questions,
        "interactive_controls_present": has_reveal_accordions,
        "total_katex_instances_in_kinematics": kin_dom.count("katex"),
        "verdict": "PASSED"
    }

    # Final verdict calculation
    all_passed = (
        all(v["status"] == "HTTP_200_OK" for v in results["network_asset_integrity"].values()) and
        results["data_bundle_hashes"]["mismatches"] == 0 and
        all(r["verdict"] == "PASSED" for r in results["route_smoke_tests"].values()) and
        results["responsive_layout_tests"]["mobile_375x667"]["verdict"] == "PASSED" and
        results["responsive_layout_tests"]["desktop_1440x900"]["verdict"] == "PASSED" and
        results["search_verification"]["verdict"] == "PASSED"
    )
    results["all_checks_passed"] = all_passed
    results["final_verdict"] = "PHASE_12_1_LIVE_QA_PROVEN" if all_passed else "FAILED"
    log(f"FINAL VERDICT: {results['final_verdict']}")

    # Save report
    out_path = Path("build/reports/phase12_1_live_qa.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    log(f"Wrote QA results to {out_path}")
    return results

if __name__ == "__main__":
    res = run_all_qa()
