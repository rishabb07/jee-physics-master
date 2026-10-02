import json
import urllib.request
import sys

def check_runs():
    url = "https://api.github.com/repos/rishabb07/jee-physics-master/actions/runs?per_page=5"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            runs = data.get("workflow_runs", [])
            for r in runs:
                print(f"Run ID: {r['id']} | Commit: {r['head_sha'][:7]} | Name: {r['name']} | Status: {r['status']} | Conclusion: {r['conclusion']}")
            return runs
    except Exception as e:
        print(f"Error fetching runs: {e}")
        return []

if __name__ == "__main__":
    check_runs()
