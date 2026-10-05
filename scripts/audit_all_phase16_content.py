import sys
sys.path.insert(0, ".")
import json
from pathlib import Path
from src.jee_physics.content.gate import compute_content_hash

def get_json(p):
    path = Path(p)
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# The Phase 16 rotational motion artifacts to check:
concepts = [
    'concept-rot-moi-continuous-01',
    'concept-rot-rotational-work-energy-01',
    'concept-rot-angmom-rigid-body-01',
    'concept-rot-pure-rolling-kinematics-01',
    'concept-rot-rolling-horizontal-friction-01',
    'concept-rot-rolling-incline-01',
    'concept-rot-toppling-condition-01',
]

formulas = [
    'formula-rot-moi-discrete',
    'formula-rot-moi-standard-bodies',
    'formula-rot-moi-perpendicular',
    'formula-rot-moi-radius-gyration',
    'formula-rot-torque-def',
    'formula-rot-kinematics-equations',
    'formula-rot-ke-rotation',
    'formula-rot-work-energy-rot',
    'formula-rot-angmom-rigid-body',
    'formula-rot-rolling-no-slip-velocity',
    'formula-rot-rolling-incline-accel',
    'formula-rot-toppling-condition',
]

derivations = [
    'derivation-formula-rot-moi-perpendicular',
    'derivation-formula-rot-ke-rotation',
    'derivation-formula-rot-rolling-incline-accel',
]

examples = [
    'ex-rot-moi-disc-cavity-01',
    'ex-rot-pulley-atwood-01',
    'ex-rot-projectile-angmom-01',
    'ex-rot-rolling-incline-race-01',
    'ex-rot-toppling-block-01',
]

misconceptions = [
    'misc-rot-03',
    'misc-rot-04',
    'misc-rot-05',
    'misc-rot-06',
]

questions = [
    'gen-q-rot-misc-01',
    'gen-q-rot-angmom-01',
]

all_items = []
for c in concepts: all_items.append(('CONCEPT', c, f'content/verified/concepts/{c}.json'))
for f in formulas: all_items.append(('FORMULA', f, f'content/verified/formulas/{f}.json'))
for d in derivations: all_items.append(('DERIVATION', d, f'content/verified/derivations/{d}.json'))
for e in examples: all_items.append(('WORKED_EXAMPLE', e, f'content/verified/examples/{e}.json'))
for m in misconceptions: all_items.append(('MISCONCEPTION', m, f'content/verified/misconceptions/{m}.json'))
for q in questions: all_items.append(('QUESTION', q, f'content/verified/questions/{q}.json'))

print(f"Total Phase 16 newly introduced artifacts to audit: {len(all_items)}")

for atype, aid, apath in all_items:
    adata = get_json(apath)
    if not adata:
        print(f"MISSING ARTIFACT: {aid} at {apath}")
        continue
    chash = compute_content_hash(adata)
    vstatus = adata.get('verification_status')
    vrec_id = adata.get('verification_record_id')
    
    # Check CVR in build/staging/incoming/content_verification
    cvr1_path = Path(f'build/staging/incoming/content_verification/{vrec_id}.json') if vrec_id else None
    cvr1 = get_json(cvr1_path) if cvr1_path and cvr1_path.exists() else None
    
    # Check Dual CVR in content/verified/dual_verifications
    dual_path = Path(f'content/verified/dual_verifications/cvr-{aid}.json')
    dual = get_json(dual_path) if dual_path.exists() else None
    
    # Check Verifier B
    vb_path = Path(f'build/staging/incoming/content_verification/verifier_b/opinion-{aid}.json')
    vb = get_json(vb_path) if vb_path.exists() else None
    
    # Print summary
    print(f"\n--- [{atype}] {aid} ---")
    print(f"  Artifact status={vstatus}, rec_id={vrec_id}, chash={chash[:12]}")
    if cvr1:
        cvr_hash = cvr1.get('content_hash')
        hash_match = (cvr_hash == chash)
        print(f"  CVR 1: verifier={cvr1.get('verifier_id')}, hash_match={hash_match}, verdict={cvr1.get('verdict')}")
        print(f"  CVR 1 notes: {cvr1.get('verification_notes', cvr1.get('independent_derivation_or_calculation', ''))[:80]}...")
    else:
        print(f"  CVR 1: MISSING ({cvr1_path})")
        
    if dual:
        dual_hash = dual.get('content_hash')
        hash_match = (dual_hash == chash)
        print(f"  Dual CVR: dual_verified={dual.get('dual_verified')}, hash_match={hash_match}")
    elif atype in ['DERIVATION', 'WORKED_EXAMPLE']:
        print(f"  Dual CVR: MISSING ({dual_path})")
        
    if vb:
        print(f"  Verifier B: verifier={vb.get('verifier_id')}, verdict={vb.get('verdict')}")
    elif atype in ['DERIVATION', 'WORKED_EXAMPLE']:
        print(f"  Verifier B: MISSING ({vb_path})")
