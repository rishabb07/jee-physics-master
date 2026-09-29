import json
from pathlib import Path

subagents = [
    {
        'id': '126488a8-d6c5-4eb1-953f-9b833f4b917c',
        'role': 'Mechanics and Thermodynamics Content Generator',
        'type': 'content-generator',
        'department': 'Generation (Concepts + Derivations: Rotational + Thermo)',
    },
    {
        'id': '068c12c6-05bc-4521-81c4-e5ff6ad6d7f9',
        'role': 'Electrodynamics and Optics Content Generator',
        'type': 'content-generator',
        'department': 'Generation (Concepts + Derivations: Electrodynamics + Optics)',
    },
    {
        'id': '6dce4bbd-45ec-4de0-95e5-461836f2ba08',
        'role': 'Examples and Misconceptions Content Generator',
        'type': 'content-generator',
        'department': 'Generation (Examples + Misconceptions)',
    },
    {
        'id': 'afe5bcb6-93b3-4ed7-bae6-9489343cc25d',
        'role': 'Physics Formula Writer',
        'type': 'content-generator',
        'department': 'Generation (13 Standalone Formulas)',
    },
    {
        'id': 'bdcda0e3-0496-4ba9-a62e-6fe79ffe6824',
        'role': 'Mechanics and Thermo Content Verifier',
        'type': 'content-verifier',
        'department': 'Verification (Verifier A: Rotational + Thermo)',
    },
    {
        'id': 'e9f3b7da-683c-457e-a22d-d6c43d8f1368',
        'role': 'Electrodynamics, Optics and Examples Verifier',
        'type': 'content-verifier',
        'department': 'Verification (Verifier A: Electrodynamics, Optics, Examples, Misconceptions)',
    },
    {
        'id': 'ab85d650-e1e8-42e2-ac4a-8bc8a6460e30',
        'role': 'Formula Content Verifier',
        'type': 'physics-content-verifier',
        'department': 'Verification (13 Formulas Single Verification)',
    },
    {
        'id': 'f33459f6-ad0e-40a2-970e-a7326be40666',
        'role': 'Independent Physics Verifier B - High Risk',
        'type': 'physics-content-verifier',
        'department': 'Verification (Verifier B: 17 High-Risk Derivations & Examples)',
    },
    {
        'id': 'eb7e5cc3-5774-450c-987f-fa57f7de795a',
        'role': 'Chapter Editorial Assembler',
        'type': 'physics-editorial-assembler',
        'department': 'Editorial Assembly (4 Chapters)',
    },
    {
        'id': '833a142b-14c0-42b6-bf27-f3b38235193d',
        'role': 'Independent Chapter QA Auditor',
        'type': 'physics-chapter-qa',
        'department': 'Chapter QA (4 Chapters)',
    },
]

base_brain = Path(r'C:\Users\Win11\.gemini\antigravity\brain')

results = []
for sa in subagents:
    cid = sa['id']
    t_path = base_brain / cid / '.system_generated' / 'logs' / 'transcript.jsonl'
    exists = t_path.exists()
    written_files = []
    run_commands = []
    if exists:
        with open(t_path, 'r', encoding='utf-8') as f:
            for line in f:
                rec = json.loads(line)
                for tc in rec.get('tool_calls', []):
                    tname = tc.get('name')
                    args = tc.get('args', {})
                    if tname in ('write_to_file', 'replace_file_content'):
                        tf = args.get('TargetFile')
                        if tf:
                            written_files.append(tf)
                    elif tname == 'run_command':
                        cmd = args.get('CommandLine')
                        if cmd:
                            run_commands.append(cmd)

    entry = {
        'conversation_id': cid,
        'role': sa['role'],
        'type': sa['type'],
        'department': sa['department'],
        'transcript_path': str(t_path),
        'transcript_exists': exists,
        'written_files': written_files,
        'run_command_count': len(run_commands),
    }
    results.append(entry)
    print(f"=== {sa['role']} ({cid[:8]}) ===")
    print(f"  Type: {sa['type']}")
    print(f"  Transcript: {exists}")
    print(f"  Direct files written: {len(written_files)}")
    for wf in written_files[:6]:
        print(f"    - {Path(wf).name}")
    if len(written_files) > 6:
        print(f"    ... and {len(written_files) - 6} more")

rep_path = Path('build/reports/phase8_subagent_forensic_audit.json')
rep_path.parent.mkdir(parents=True, exist_ok=True)
with open(rep_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print(f"Wrote {rep_path}")
