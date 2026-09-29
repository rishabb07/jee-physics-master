"""
Integration Test: Live Watcher Auto-Recompilation and HTTP Browser-Level Update.
Proves that mutating a canonical/staged source record while the dev server is running
triggers automatic filesystem detection, automatic recompilation, and instant browser-level HTTP update.
"""

import json
import time
import urllib.request
from pathlib import Path
import threading
import pytest

from jee_physics.web.server import DevServer


def test_live_dev_server_auto_update_end_to_end():
    root = Path.cwd()
    port = 8080
    host = "127.0.0.1"
    server = DevServer(root_dir=root, port=port, host=host)

    # 1. Start DevServer in a background thread
    server_thread = threading.Thread(target=server.start, kwargs={"watch": True}, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    assert server._server_ready.wait(timeout=5.0), "DevServer failed to start within 5 seconds"

    formula_path = root / "build" / "staging" / "incoming" / "content" / "formulas" / "formula-rot-moi-parallel.json"
    assert formula_path.exists(), "Target formula file does not exist"

    original_raw = formula_path.read_text(encoding="utf-8")
    original_data = json.loads(original_raw)
    original_title = original_data["title"]

    try:
        # 2. Check initial browser-level HTTP response
        url = f"http://{host}:{port}/data/formulas.json"
        req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200
            initial_formulas = json.loads(response.read().decode("utf-8"))

        found_initial = next((f for f in initial_formulas if f["formula_id"] == "formula-rot-moi-parallel"), None)
        assert found_initial is not None
        assert found_initial["title"] == original_title

        # 3. Perform mutation on source record
        mutated_title = "Parallel Axis Theorem (Auto-Update Live Proven)"
        mutated_data = dict(original_data)
        mutated_data["title"] = mutated_title
        formula_path.write_text(json.dumps(mutated_data, indent=2), encoding="utf-8")

        # 4. Wait for watcher to automatically detect and recompile (NO manual build command!)
        updated_title = None
        for _ in range(15):  # Wait up to 7.5 seconds
            time.sleep(0.5)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"Cache-Control": "no-cache"}), timeout=2) as resp:
                    cur_formulas = json.loads(resp.read().decode("utf-8"))
                    cur_f = next((f for f in cur_formulas if f["formula_id"] == "formula-rot-moi-parallel"), None)
                    if cur_f and cur_f["title"] == mutated_title:
                        updated_title = cur_f["title"]
                        break
            except Exception:
                pass

        assert updated_title == mutated_title, f"Watcher failed to auto-update: expected '{mutated_title}', got '{updated_title}'"

        # 5. Restore original record
        formula_path.write_text(original_raw, encoding="utf-8")

        # 6. Wait for watcher to automatically detect restoration and recompile
        restored_title = None
        for _ in range(15):
            time.sleep(0.5)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"Cache-Control": "no-cache"}), timeout=2) as resp:
                    cur_formulas = json.loads(resp.read().decode("utf-8"))
                    cur_f = next((f for f in cur_formulas if f["formula_id"] == "formula-rot-moi-parallel"), None)
                    if cur_f and cur_f["title"] == original_title:
                        restored_title = cur_f["title"]
                        break
            except Exception:
                pass

        assert restored_title == original_title, f"Watcher failed to restore: expected '{original_title}', got '{restored_title}'"

    finally:
        # 7. Clean restoration and stop server
        formula_path.write_text(original_raw, encoding="utf-8")
        server.stop()
        server_thread.join(timeout=3.0)
