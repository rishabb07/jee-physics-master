import sys
sys.path.insert(0, ".")
import json
from pathlib import Path
from src.jee_physics.content.gate import compute_content_hash

def check_file(p):
    path = Path(p)
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

print("=== AUDIT OF MISCONCEPTIONS ===")
for m_id in ['misc-rot-01', 'misc-rot-02', 'misc-rot-03', 'misc-rot-04', 'misc-rot-05', 'misc-rot-06']:
    f_path = Path(f'content/verified/misconceptions/{m_id}.json')
    if f_path.exists():
        data = check_file(f_path)
        chash = compute_content_hash(data)
        v_status = data.get('verification_status')
        v_rec_id = data.get('verification_record_id')
        print(f"{m_id}: status={v_status}, rec_id={v_rec_id}, chash={chash[:12]}")
        
        # Check if cvr file exists anywhere
        cvr_staged = Path(f'build/staging/incoming/content_verification/{v_rec_id}.json')
        print(f"   build/staging/incoming cvr exists? {cvr_staged.exists()}")
        if cvr_staged.exists():
            cvr_data = check_file(cvr_staged)
            print(f"   cvr target={cvr_data.get('target_id') or cvr_data.get('artifact_id')} hash={str(cvr_data.get('content_hash'))[:12]} verifier={cvr_data.get('verifier_id')}")
        
        # Check if in content/verified/dual_verifications
        cvr_dual = Path(f'content/verified/dual_verifications/cvr-{m_id}.json')
        print(f"   dual_verifications cvr exists? {cvr_dual.exists()}")
        
        # Search all cvr files for this target_id
        matching_cvrs = list(Path('.').glob(f'**/cvr-{m_id}.json'))
        print(f"   matching cvrs found anywhere: {[str(p) for p in matching_cvrs]}")
    else:
        print(f"{m_id} does not exist at {f_path}")
