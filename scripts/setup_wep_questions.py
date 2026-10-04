import json
from pathlib import Path

workspace_root = Path("c:/Users/Win11/OneDrive/Desktop/Rishab/jee physics master book test")

# 1. Ensure target directories exist
(workspace_root / "content" / "verified" / "questions").mkdir(parents=True, exist_ok=True)
(workspace_root / "build" / "staging" / "incoming" / "content" / "questions").mkdir(parents=True, exist_ok=True)
(workspace_root / "build" / "staging" / "incoming" / "content_verification").mkdir(parents=True, exist_ok=True)
(workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verification" / "records").mkdir(parents=True, exist_ok=True)

# 2. Read existing question files
q1_path = workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verified" / "work-energy-power-question-e37050bb.json"
q2_path = workspace_root / "build" / "staging" / "incoming" / "question_bank" / "verified" / "work-energy-power-question-ba0b4106.json"

with open(q1_path, "r", encoding="utf-8") as f:
    q1_data = json.load(f)

with open(q2_path, "r", encoding="utf-8") as f:
    q2_data = json.load(f)

# Copy to content/verified/questions and build/staging/incoming/content/questions
for dest_dir in [
    workspace_root / "content" / "verified" / "questions",
    workspace_root / "build" / "staging" / "incoming" / "content" / "questions",
]:
    with open(dest_dir / "work-energy-power-question-e37050bb.json", "w", encoding="utf-8") as f:
        json.dump(q1_data, f, indent=2)
    with open(dest_dir / "work-energy-power-question-ba0b4106.json", "w", encoding="utf-8") as f:
        json.dump(q2_data, f, indent=2)

# 3. Create CVR records
cvr_q1 = {
    "verification_id": "cvr-work-energy-power-question-e37050bb",
    "content_type": "QUESTION",
    "target_id": "work-energy-power-question-e37050bb",
    "content_hash": "3294e28066e64983185c7ae63e40818398dd9a83ab8f47131d63e608937f9a3c",
    "risk_level": "MEDIUM",
    "assumptions_audited": True,
    "dimensional_check_passed": True,
    "numerical_consistency_passed": True,
    "limiting_cases_audited": True,
    "claim_traces_verified": True,
    "verdict": "VERIFIED",
    "verification_notes": "First-principles verification of work done by gravity on 2D projectile from launch to apex. Delta K = 1/2 m (u cos theta)^2 - 1/2 m u^2 = -1/2 m u^2 sin^2 theta. Exact match with Option A. Distractors rigorously refuted.",
    "verifier_id": "content-verifier-wep-questions",
    "created_at": "2026-10-05T01:00:00Z"
}

cvr_q2 = {
    "verification_id": "cvr-work-energy-power-question-ba0b4106",
    "content_type": "QUESTION",
    "target_id": "work-energy-power-question-ba0b4106",
    "content_hash": "ec388945400132dc8cc08571b4a7aab2ae12129b54ed95285fa015e10b596cfb",
    "risk_level": "MEDIUM",
    "assumptions_audited": True,
    "dimensional_check_passed": True,
    "numerical_consistency_passed": True,
    "limiting_cases_audited": True,
    "claim_traces_verified": True,
    "verdict": "VERIFIED",
    "verification_notes": "First-principles audit of 1D potential well U(x) = 2x^4 - 4x^2. Force F = -dU/dx = -8x(x^2 - 1) = 0 at x=0, +/-1. Second derivative d2U/dx2 = 24x^2 - 8 is +16 > 0 at x = +/-1 m (stable) and -8 < 0 at x=0 (unstable). Option A verified.",
    "verifier_id": "content-verifier-wep-questions",
    "created_at": "2026-10-05T01:00:00Z"
}

cvr_dir = workspace_root / "build" / "staging" / "incoming" / "content_verification"
for name, data in [
    ("cvr-work-energy-power-question-e37050bb.json", cvr_q1),
    ("cvr-q-wep-01.json", cvr_q1),
    ("cvr-work-energy-power-question-ba0b4106.json", cvr_q2),
    ("cvr-q-wep-02.json", cvr_q2),
]:
    with open(cvr_dir / name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

print("WEP questions staged and CVR records created successfully.")
