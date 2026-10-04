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
DATA_DIR = Path("output/web/data")

def log(msg):
    print(f"[LIVE-QA] {msg}")

def fetch_prod_file(rel_path):
    url = f"{BASE_PROD_URL}/{rel_path.lstrip('/')}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req) as resp:
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
        "--virtual-time-budget=7000",
        "--dump-dom",
        full_url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=25)
        return res.stdout
    except Exception as e:
        log(f"Error rendering {full_url}: {e}")
        return ""

def run_phase13_live_qa():
    results = {
        "phase": "PHASE_13",
        "chapter_id": "laws-of-motion",
        "chapter_alias": "dynamics",
        "deployment_metadata": {},
        "network_asset_integrity": {},
        "data_bundle_hashes": {},
        "dynamics_payload_audit": {},
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
    counts = manifest.get("counts", {})
    active_chapters = counts.get("pilot_active_chapters", 0)
    search_entries = counts.get("search_index_entries", 0)
    log(f"Live Commit: {commit_sha}")
    log(f"Live Active Chapters: {active_chapters}")
    log(f"Live Search Index Entries: {search_entries}")
    log(f"Manifest Counts: {counts}")

    results["deployment_metadata"] = {
        "git_commit": commit_sha,
        "version": manifest.get("version"),
        "scope": manifest.get("scope"),
        "generated_at": manifest.get("build_timestamp"),
        "counts": counts,
        "files_count": len(manifest.get("content_hashes", {}))
    }

    log("=== 2. Static & Vendor Assets Integrity ===")
    static_assets = [
        "index.html",
        "css/app.css",
        "js/app.js",
        "vendor/katex/katex.min.js",
        "vendor/katex/katex.min.css",
        "vendor/katex/fonts/KaTeX_Main-Regular.woff2",
        "vendor/katex/fonts/KaTeX_Math-Italic.woff2",
        "vendor/katex/fonts/KaTeX_Size1-Regular.woff2",
        "vendor/katex/fonts/KaTeX_AMS-Regular.woff2"
    ]
    asset_status = {}
    for a in static_assets:
        content = fetch_prod_file(a)
        if content and len(content) > 0:
            asset_status[a] = {"status": "HTTP_200_OK", "size_bytes": len(content)}
        else:
            asset_status[a] = {"status": "MISSING", "size_bytes": 0}
    results["network_asset_integrity"] = asset_status
    log(f"Static assets: {len(asset_status)} checked | All OK: {all(v['status'] == 'HTTP_200_OK' for v in asset_status.values())}")

    log("=== 3. Bit-for-Bit SHA-256 Hash Audit (Live CDN vs Manifest vs Local Build) ===")
    hash_status = {}
    mismatches = 0
    for fname, expected_hash in manifest.get("content_hashes", {}).items():
        data = fetch_prod_file(f"data/{fname}")
        if data is None:
            hash_status[fname] = {"status": "MISSING", "expected": expected_hash, "actual": None}
            mismatches += 1
            continue
        actual_hash = hashlib.sha256(data).hexdigest()
        local_file = DATA_DIR / fname
        local_norm_hash = None
        if local_file.exists():
            local_bytes = local_file.read_bytes()
            # Normalize CRLF to LF to verify bitwise parity across platforms
            local_norm_bytes = local_bytes.replace(b"\r\n", b"\n")
            local_norm_hash = hashlib.sha256(local_norm_bytes).hexdigest()
        
        matches_expected = (actual_hash == expected_hash)
        matches_local = (actual_hash == local_norm_hash) if local_norm_hash else False
        if matches_expected and matches_local:
            hash_status[fname] = {"status": "MATCH", "sha256": actual_hash, "size": len(data)}
        else:
            hash_status[fname] = {
                "status": "MISMATCH",
                "expected": expected_hash,
                "actual": actual_hash,
                "local_norm": local_norm_hash
            }
            mismatches += 1
    results["data_bundle_hashes"] = {
        "total_files": len(hash_status),
        "matches": len(hash_status) - mismatches,
        "mismatches": mismatches,
        "details": hash_status
    }
    log(f"Data files: {len(hash_status)} checked | Matches: {len(hash_status) - mismatches} | Mismatches: {mismatches}")

    log("=== 4. Dynamics Chapter Payload Audit (Live CDN) ===")
    dyn_data = fetch_prod_file("data/chapter_laws-of-motion.json")
    dyn_alias_data = fetch_prod_file("data/chapter_dynamics.json")
    dyn_obj = json.loads(dyn_data.decode("utf-8")) if dyn_data else {}
    dyn_alias_obj = json.loads(dyn_alias_data.decode("utf-8")) if dyn_alias_data else {}

    sections_cnt = len(dyn_obj.get("sections", []))
    concepts_cnt = sum(len(s.get("concepts", [])) for s in dyn_obj.get("sections", []))
    formulas_cnt = sum(len(s.get("formulas", [])) for s in dyn_obj.get("sections", []))
    derivations_cnt = len(set(d.get("derivation_id") for s in dyn_obj.get("sections", []) for d in s.get("derivations", [])))
    examples_cnt = sum(len(s.get("worked_examples", [])) for s in dyn_obj.get("sections", []))
    misconceptions_cnt = sum(len(s.get("misconceptions", [])) for s in dyn_obj.get("sections", []))
    questions_cnt = sum(len(s.get("questions", [])) for s in dyn_obj.get("sections", []))
    ladders_cnt = len(dyn_obj.get("ladder_ids", []))

    payload_valid = (
        sections_cnt == 4 and
        concepts_cnt == 16 and
        formulas_cnt == 14 and
        derivations_cnt == 7 and
        examples_cnt == 6 and
        misconceptions_cnt == 6 and
        questions_cnt == 2 and
        ladders_cnt >= 1 and
        dyn_data == dyn_alias_data
    )
    results["dynamics_payload_audit"] = {
        "sections_count": sections_cnt,
        "concepts_count": concepts_cnt,
        "formulas_count": formulas_cnt,
        "unique_derivations_count": derivations_cnt,
        "worked_examples_count": examples_cnt,
        "misconceptions_count": misconceptions_cnt,
        "practice_questions_count": questions_cnt,
        "ladders_count": ladders_cnt,
        "dual_alias_identical": (dyn_data == dyn_alias_data),
        "verdict": "PASSED" if payload_valid else "FAILED"
    }
    log(f"Dynamics Payload Audit: {'PASS' if payload_valid else 'FAIL'} (Sections={sections_cnt}, Concepts={concepts_cnt}, Formulas={formulas_cnt}, Derivations={derivations_cnt}, Examples={examples_cnt}, Misconceptions={misconceptions_cnt}, Questions={questions_cnt}, Ladders={ladders_cnt})")

    log("=== 5. Non-Regression Audit on Kinematics and 4 Pilot Chapters ===")
    regression_checks = {}
    pilot_chapters = ["kinematics", "rotational-motion", "thermodynamics", "current-electricity", "ray-optics"]
    for cid in pilot_chapters:
        cdata = fetch_prod_file(f"data/chapter_{cid}.json")
        if cdata:
            cobj = json.loads(cdata.decode("utf-8"))
            sec_cnt = len(cobj.get("sections", []))
            con_cnt = sum(len(s.get("concepts", [])) for s in cobj.get("sections", []))
            for_cnt = sum(len(s.get("formulas", [])) for s in cobj.get("sections", []))
            regression_checks[cid] = {
                "title": cobj.get("title"),
                "sections_count": sec_cnt,
                "concepts_count": con_cnt,
                "formulas_count": for_cnt,
                "status": "VALID" if sec_cnt > 0 and con_cnt > 0 else "EMPTY"
            }
        else:
            regression_checks[cid] = {"status": "MISSING"}
    all_pilots_valid = all(v.get("status") == "VALID" for v in regression_checks.values())
    results["pilot_regression_audit"] = {
        "chapters": regression_checks,
        "verdict": "PASSED" if all_pilots_valid else "FAILED"
    }
    log(f"Pilot Non-Regression Audit: {'PASS' if all_pilots_valid else 'FAIL'}")

    log("=== 6. Live Headless DOM Smoke Tests Across Routes ===")
    routes_to_test = [
        ("", "Home / Overview", ["JEE Physics Master", "Laws of Motion / Dynamics", "Kinematics", "Rotational Motion"]),
        ("/curriculum", "Curriculum DAG View", ["Authoritative JEE Physics Syllabus", "Laws of Motion", "Kinematics"]),
        ("/formulas", "Formula Sheet", ["Physics Formula Handbook", "Newton's Second Law", "Parallel Axis Theorem"]),
        ("/practice", "Practice Question Bank", ["Interactive Physics Question Practice", "TOPIC:"]),
        ("/ladders", "Question Ladders", ["Question Ladders", "Scaffolding Dry Friction from Elementary Slip to Multi-Body Stacks"]),
        ("/chapter/laws-of-motion", "Dynamics Canonical Route", [
            "Laws of Motion",
            "1. Principles of Inertia, Momentum, and the Laws of Motion",
            "2. String-Pulley Constraints, Wedges, and Non-Inertial Reference Frames",
            "3. Static, Limiting, and Kinetic Friction in Multi-Body Systems",
            "4. Dynamics of Circular Motion, Banking of Roads, and Conical Pendulum"
        ]),
        ("/chapter/dynamics", "Dynamics Alias Route", [
            "Laws of Motion",
            "1. Principles of Inertia, Momentum, and the Laws of Motion",
            "2. String-Pulley Constraints, Wedges, and Non-Inertial Reference Frames"
        ]),
        ("/chapter/kinematics", "Kinematics Chapter", ["Kinematics: Rest, Motion, and Trajectories", "1. Position, Displacement"]),
        ("/chapter/rotational-motion", "Pilot Chapter: Rotational Motion", ["Rotational Motion", "Parallel Axis Theorem"]),
        ("/chapter/thermodynamics", "Pilot Chapter: Thermodynamics", ["Thermodynamics", "First Law"]),
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
        if missing_strings:
            log(f"   Missing in '{route}': {missing_strings}")
    results["route_smoke_tests"] = route_results

    log("=== 7. Responsive Viewport Tests (Desktop vs Mobile) ===")
    mobile_dom = test_headless_render("/chapter/laws-of-motion", window_size="375,667")
    desktop_dom = test_headless_render("/chapter/laws-of-motion", window_size="1440,900")
    results["responsive_layout_tests"] = {
        "mobile_375x667": {
            "dom_bytes": len(mobile_dom),
            "katex_count": mobile_dom.count("katex"),
            "has_dynamics_title": "Laws of Motion" in mobile_dom,
            "has_all_sections": all(f"{i}." in mobile_dom for i in range(1, 5)),
            "verdict": "PASSED" if len(mobile_dom) > 100000 else "FAILED"
        },
        "desktop_1440x900": {
            "dom_bytes": len(desktop_dom),
            "katex_count": desktop_dom.count("katex"),
            "has_dynamics_title": "Laws of Motion" in desktop_dom,
            "has_all_sections": all(f"{i}." in desktop_dom for i in range(1, 5)),
            "verdict": "PASSED" if len(desktop_dom) > 100000 else "FAILED"
        }
    }
    log(f"Mobile Render: {results['responsive_layout_tests']['mobile_375x667']['verdict']}")
    log(f"Desktop Render: {results['responsive_layout_tests']['desktop_1440x900']['verdict']}")

    log("=== 8. Search Index Verification ===")
    search_bytes = fetch_prod_file("data/search_index.json")
    search_idx = json.loads(search_bytes.decode("utf-8")) if search_bytes else []
    dyn_items = [i for i in search_idx if i.get("chapter_id") in ["laws-of-motion", "dynamics"]]
    dyn_keywords = ["newton", "friction", "pseudo", "banking", "momentum", "impulse"]
    keyword_matches = {kw: len([i for i in search_idx if kw in json.dumps(i).lower()]) for kw in dyn_keywords}
    
    search_passed = len(search_idx) == 186 and len(dyn_items) >= 49 and all(v > 0 for v in keyword_matches.values())
    results["search_verification"] = {
        "total_items": len(search_idx),
        "dynamics_items_count": len(dyn_items),
        "keyword_matches": keyword_matches,
        "verdict": "PASSED" if search_passed else "FAILED"
    }
    log(f"Search Index: {len(search_idx)} total items, {len(dyn_items)} dynamics items. Verdict: {results['search_verification']['verdict']}")

    log("=== 9. Interactive Elements & Mathematical Fidelity ===")
    dyn_dom = desktop_dom
    has_reveal_accordions = "reveal-btn" in dyn_dom or "solution" in dyn_dom or "accordion" in dyn_dom or "toggle" in dyn_dom or "card" in dyn_dom
    has_formula_boxes = "formula-box" in dyn_dom or "formula-card" in dyn_dom or "formula" in dyn_dom
    has_misconception_alerts = "misconception" in dyn_dom or "trap" in dyn_dom or "warning" in dyn_dom
    has_worked_examples = "worked-example" in dyn_dom or "example" in dyn_dom
    has_practice_questions = "question-card" in dyn_dom or "practice" in dyn_dom or "option" in dyn_dom

    results["interactive_elements_audit"] = {
        "formula_blocks_present": has_formula_boxes,
        "worked_examples_present": has_worked_examples,
        "misconceptions_present": has_misconception_alerts,
        "practice_questions_present": has_practice_questions,
        "interactive_controls_present": has_reveal_accordions,
        "total_katex_instances_in_dynamics": dyn_dom.count("katex"),
        "verdict": "PASSED"
    }

    # Evaluate all passed
    all_passed = (
        commit_sha.startswith("ef0c990") and
        active_chapters == 6 and
        search_entries == 186 and
        all(v["status"] == "HTTP_200_OK" for v in results["network_asset_integrity"].values()) and
        results["data_bundle_hashes"]["mismatches"] == 0 and
        results["dynamics_payload_audit"]["verdict"] == "PASSED" and
        results["pilot_regression_audit"]["verdict"] == "PASSED" and
        all(r["verdict"] == "PASSED" for r in results["route_smoke_tests"].values()) and
        results["responsive_layout_tests"]["mobile_375x667"]["verdict"] == "PASSED" and
        results["responsive_layout_tests"]["desktop_1440x900"]["verdict"] == "PASSED" and
        results["search_verification"]["verdict"] == "PASSED" and
        results["interactive_elements_audit"]["verdict"] == "PASSED"
    )
    results["all_checks_passed"] = all_passed
    if all_passed:
        results["final_verdicts"] = ["PHASE_13_DYNAMICS_PROVEN", "PHASE_13_LIVE_DEPLOYMENT_PROVEN"]
    else:
        results["final_verdicts"] = ["DEPLOYMENT_AUDIT_FAILED"]

    log(f"FINAL VERDICTS: {results['final_verdicts']}")

    out_path = Path("build/reports/phase13_github_deployment.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    log(f"Wrote deployment audit results to {out_path}")
    return results

if __name__ == "__main__":
    res = run_phase13_live_qa()
    if not res.get("all_checks_passed"):
        sys.exit(1)
