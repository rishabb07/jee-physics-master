import sys
sys.path.insert(0, '.')
import json
from pathlib import Path
from src.jee_physics.content.gate import compute_content_hash

inherited_concepts = ['concept-rot-moi-01', 'concept-rot-torque-01', 'concept-rot-angmom-particle-01', 'concept-rot-angmom-conservation-01']
inherited_formulas = ['formula-rot-moi-parallel', 'formula-rot-torque-dyn', 'formula-rot-angmom-particle', 'formula-rot-conservation-angmom']
inherited_derivations = ['derivation-formula-rot-moi-parallel', 'derivation-formula-rot-torque-dyn', 'derivation-formula-rot-angmom-particle', 'derivation-formula-rot-conservation-angmom']
inherited_examples = ['ex-rot-angmom-disc-01']
inherited_misconceptions = ['misc-rot-01', 'misc-rot-02']

print('=== INHERITED PILOT ARTIFACTS AUDIT ===')
for c in inherited_concepts:
    p = Path(f'content/verified/concepts/{c}.json')
    data = json.load(open(p, encoding='utf-8'))
    chash = compute_content_hash(data)
    vrec = data.get('verification_record_id')
    cvr_p = Path(f'build/staging/incoming/content_verification/{vrec}.json')
    cvr = json.load(open(cvr_p, encoding='utf-8')) if cvr_p.exists() else None
    cvr_hash = cvr.get('content_hash') if cvr else None
    v_id = cvr.get('verifier_id') if cvr else None
    print(f"Concept {c}: vrec={vrec}, hash_match={chash == cvr_hash}, verifier={v_id}")

for f in inherited_formulas:
    p = Path(f'content/verified/formulas/{f}.json')
    data = json.load(open(p, encoding='utf-8'))
    chash = compute_content_hash(data)
    vrec = data.get('verification_record_id')
    cvr_p = Path(f'build/staging/incoming/content_verification/{vrec}.json')
    cvr = json.load(open(cvr_p, encoding='utf-8')) if cvr_p.exists() else None
    cvr_hash = cvr.get('content_hash') if cvr else None
    v_id = cvr.get('verifier_id') if cvr else None
    print(f"Formula {f}: vrec={vrec}, hash_match={chash == cvr_hash}, verifier={v_id}")

for d in inherited_derivations:
    p = Path(f'content/verified/derivations/{d}.json')
    data = json.load(open(p, encoding='utf-8'))
    chash = compute_content_hash(data)
    vrec = data.get('verification_record_id')
    dual_p = Path(f'content/verified/dual_verifications/dual-cvr-{d}.json')
    dual = json.load(open(dual_p, encoding='utf-8')) if dual_p.exists() else None
    dual_hash = dual.get('content_hash') if dual else None
    print(f"Derivation {d}: vrec={vrec}, dual_exists={dual_p.exists()}, hash_match={chash == dual_hash}")

for e in inherited_examples:
    p = Path(f'content/verified/examples/{e}.json')
    data = json.load(open(p, encoding='utf-8'))
    chash = compute_content_hash(data)
    dual_p = Path(f'content/verified/dual_verifications/dual-cvr-{e}.json')
    dual = json.load(open(dual_p, encoding='utf-8')) if dual_p.exists() else None
    dual_hash = dual.get('content_hash') if dual else None
    print(f"Example {e}: dual_exists={dual_p.exists()}, hash_match={chash == dual_hash}")

for m in inherited_misconceptions:
    p = Path(f'content/verified/misconceptions/{m}.json')
    data = json.load(open(p, encoding='utf-8'))
    chash = compute_content_hash(data)
    vrec = data.get('verification_record_id')
    cvr_p = Path(f'build/staging/incoming/content_verification/{vrec}.json')
    cvr = json.load(open(cvr_p, encoding='utf-8')) if cvr_p.exists() else None
    cvr_hash = cvr.get('content_hash') if cvr else None
    v_id = cvr.get('verifier_id') if cvr else None
    print(f"Misconception {m}: vrec={vrec}, hash_match={chash == cvr_hash}, verifier={v_id}")
