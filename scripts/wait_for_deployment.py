import json
import urllib.request
import time
import sys

def wait_for_run(commit_prefix="ef0c990", max_wait_sec=180, poll_interval=10):
    url = "https://api.github.com/repos/rishabb07/jee-physics-master/actions/runs?per_page=5"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    start = time.time()
    print(f"Waiting for workflow run on commit {commit_prefix} to finish...")
    
    while time.time() - start < max_wait_sec:
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                runs = data.get("workflow_runs", [])
                for r in runs:
                    if r["head_sha"].startswith(commit_prefix):
                        status = r["status"]
                        conclusion = r["conclusion"]
                        print(f"[{int(time.time() - start)}s] Run {r['id']} ({r['name']}): status={status}, conclusion={conclusion}")
                        if status == "completed":
                            if conclusion == "success":
                                print("Workflow completed successfully!")
                                return True, r
                            else:
                                print(f"Workflow finished with failure: {conclusion}")
                                return False, r
        except Exception as e:
            print(f"Warning: error fetching run status: {e}")
        time.sleep(poll_interval)
        
    print("Timed out waiting for workflow.")
    return False, None

if __name__ == "__main__":
    prefix = sys.argv[1] if len(sys.argv) > 1 else "25a7813"
    success, run = wait_for_run(commit_prefix=prefix)
    if not success:
        sys.exit(1)

