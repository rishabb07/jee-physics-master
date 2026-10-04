import yaml

def main():
    with open('kb/taxonomy/syllabus.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    nodes = data['nodes']
    for nid, n in nodes.items():
        if 'circular' in nid.lower() or 'circular' in n.get('name', '').lower():
            print(f"{n.get('level')}: {nid} -> parent: {n.get('parent_id')}")

if __name__ == '__main__':
    main()
