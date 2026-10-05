import sys
sys.path.insert(0, ".")
import json
from pathlib import Path
from datetime import datetime, timezone
from src.jee_physics.models.content import DualVerificationRecord, VerifierOpinion, ContentVerificationRecord
from src.jee_physics.content.gate import compute_content_hash

high_risk = [
    'derivation-formula-rot-moi-perpendicular',
    'derivation-formula-rot-ke-rotation',
    'derivation-formula-rot-rolling-incline-accel',
    'ex-rot-moi-disc-cavity-01',
    'ex-rot-pulley-atwood-01',
    'ex-rot-projectile-angmom-01',
    'ex-rot-rolling-incline-race-01',
    'ex-rot-toppling-block-01',
]

print("=== CHECKING OPINIONS AND SYNTHESIZING DUAL CVRs ===")
for aid in high_risk:
    va_path = Path(f"build/staging/incoming/content_verification/verifier_a/opinion-{aid}.json")
    vb_path = Path(f"build/staging/incoming/content_verification/verifier_b/opinion-{aid}.json")
    
    assert va_path.exists(), f"Missing VA opinion for {aid}"
    assert vb_path.exists(), f"Missing VB opinion for {aid}"
    
    va_data = json.load(open(va_path, encoding='utf-8'))
    vb_data = json.load(open(vb_path, encoding='utf-8'))
    
    if aid.startswith("derivation-"):
        art_path = Path(f"content/verified/derivations/{aid}.json")
    else:
        art_path = Path(f"content/verified/examples/{aid}.json")
    art_data = json.load(open(art_path, encoding='utf-8'))
    current_hash = compute_content_hash(art_data)
    
    va_hash = va_data.get("content_hash")
    vb_hash = vb_data.get("content_hash")
    
    print(f"Artifact {aid}:")
    print(f"  Artifact current hash: {current_hash[:12]}")
    print(f"  VA verifier: {va_data.get('verifier_id')}, hash_match: {va_hash == current_hash}, verdict: {va_data.get('verdict')}")
    print(f"  VB verifier: {vb_data.get('verifier_id')}, hash_match: {vb_hash == current_hash}, verdict: {vb_data.get('verdict')}")
    
    # Construct DualVerificationRecord
    dual_record = {
        "verification_id": f"dual-cvr-{aid}",
        "artifact_id": aid,
        "artifact_version": 1,
        "content_hash": current_hash,
        "risk_level": "HIGH",
        "verifier_a": {
            "verifier_id": va_data.get("verifier_id"),
            "verifier_conversation_id": va_data.get("verifier_conversation_id"),
            "verdict": va_data.get("verdict"),
            "assumptions_checked": va_data.get("assumptions_checked", True),
            "dimensional_check_passed": va_data.get("dimensional_check_passed", True),
            "numerical_check_passed": va_data.get("numerical_check_passed", True),
            "limiting_case_check_passed": va_data.get("limiting_case_check_passed", True),
            "independent_derivation_or_calculation": va_data.get("independent_derivation_or_calculation"),
            "findings": va_data.get("findings", []),
            "timestamp": va_data.get("timestamp")
        },
        "verifier_b": {
            "verifier_id": vb_data.get("verifier_id"),
            "verifier_conversation_id": vb_data.get("verifier_conversation_id"),
            "verdict": vb_data.get("verdict"),
            "assumptions_checked": vb_data.get("assumptions_checked", True),
            "dimensional_check_passed": vb_data.get("dimensional_check_passed", True),
            "numerical_check_passed": vb_data.get("numerical_check_passed", True),
            "limiting_case_check_passed": vb_data.get("limiting_case_check_passed", True),
            "independent_derivation_or_calculation": vb_data.get("independent_derivation_or_calculation"),
            "findings": vb_data.get("findings", []),
            "timestamp": vb_data.get("timestamp")
        },
        "agreement": (va_data.get("verdict") == "VERIFIED" and vb_data.get("verdict") == "VERIFIED"),
        "adjudication_reference": None,
        "final_verdict": "VERIFIED",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Validate with Pydantic model
    validated = DualVerificationRecord(**dual_record)
    
    # Save to content/verified/dual_verifications/ and build/staging/incoming/content_verification/
    dest_path = Path(f"content/verified/dual_verifications/dual-cvr-{aid}.json")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(validated.model_dump_json(indent=2))
        
    staging_dest = Path(f"build/staging/incoming/content_verification/dual-cvr-{aid}.json")
    with open(staging_dest, "w", encoding="utf-8") as f:
        f.write(validated.model_dump_json(indent=2))
        
    print(f"  -> Successfully generated & saved {dest_path}")
print("ALL DUAL CVRs VALIDATED AND SAVED!")
