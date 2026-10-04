import yaml
import json

data = yaml.safe_load(open('kb/taxonomy/syllabus.yaml', encoding='utf-8'))
nodes = data.get('nodes', {})
ch = nodes.get('center-of-mass', {})
print("Chapter:", ch)

topics = [v for v in nodes.values() if v.get('parent_id') == 'center-of-mass']
topics = sorted(topics, key=lambda x: x['order'])
print(f"Total topics under center-of-mass: {len(topics)}")
for t in topics:
    print(f"Topic: {t['id']} ({t['name']}, order={t['order']})")
    subtopics = [v for v in nodes.values() if v.get('parent_id') == t['id']]
    subtopics = sorted(subtopics, key=lambda x: x['order'])
    for s in subtopics:
        print(f"    Subtopic: {s['id']} ({s['name']}, order={s['order']})")

print("\n--- Check other chapters for momentum or collision ---")
for nid, n in nodes.items():
    if 'collis' in nid or 'impulse' in nid or 'momentum' in nid:
        print(f"{nid} -> parent: {n.get('parent_id')}, level: {n.get('level')}")
