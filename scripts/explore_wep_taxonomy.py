import yaml

def explore():
    data = yaml.safe_load(open("kb/taxonomy/syllabus.yaml", encoding="utf-8"))
    nodes = data.get("nodes", {})

    def get_chain(nid):
        chain = [nid]
        curr = nodes.get(nid, {})
        while curr.get("parent_id"):
            chain.append(curr["parent_id"])
            curr = nodes.get(curr["parent_id"], {})
        return chain

    wep_descendants = [nid for nid in nodes if "work-energy-power" in get_chain(nid)]
    print(f"Total WEP nodes in hierarchy: {len(wep_descendants)}")
    for nid in wep_descendants:
        n = nodes[nid]
        print(f"{n.get('level'):10} | {nid:45} | parent: {n.get('parent_id')}")

if __name__ == "__main__":
    explore()
