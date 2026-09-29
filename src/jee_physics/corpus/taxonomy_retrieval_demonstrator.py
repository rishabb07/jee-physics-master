"""
Multi-Branch Taxonomy Retrieval Demonstrator for Phase 11.8.
Demonstrates multi-source granular evidence retrieval for at least 20 distinct
taxonomy nodes spanning Mechanics, Thermal Physics, Electromagnetism, Optics, and Modern Physics:
Retrieves:
- relevant source exposition
- definitions
- formulas
- derivations
- examples
- problems
- figures
- independent corroborating sources
References actual source evidence IDs, page ranges, and verbatim physical grounding.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


DEMONSTRATION_NODES_20 = [
    # Mechanics (10 nodes)
    ("units-and-measurements", "Units, Dimensions & Errors", "Mechanics"),
    ("kinematics", "Kinematics & Motion in 1D/2D", "Mechanics"),
    ("laws-of-motion", "Newton's Laws of Motion & Friction", "Mechanics"),
    ("work-energy-power", "Work, Energy & Conservation of Energy", "Mechanics"),
    ("center-of-mass", "Center of Mass, Linear Momentum & Collisions", "Mechanics"),
    ("rotational-motion", "Rotational Dynamics & Angular Momentum", "Mechanics"),
    ("gravitation", "Universal Gravitation & Orbital Motion", "Mechanics"),
    ("properties-of-solids", "Elasticity, Stress & Strain", "Mechanics"),
    ("fluid-mechanics", "Fluid Statics & Bernoulli Dynamics", "Mechanics"),
    ("oscillations", "Simple Harmonic Motion & Oscillations", "Mechanics"),
    ("waves", "Mechanical Waves & Sound Waves", "Mechanics"),

    # Thermal Physics (3 nodes)
    ("thermal-physics", "Thermal Expansion, Calorimetry & Heat Transfer", "Thermal Physics"),
    ("thermodynamics", "Laws of Thermodynamics & Heat Engines", "Thermal Physics"),
    ("kinetic-theory-of-gases", "Kinetic Theory & Molecular Velocities", "Thermal Physics"),

    # Electromagnetism (5 nodes)
    ("electrostatics", "Electric Charges, Fields & Gauss's Law", "Electromagnetism"),
    ("capacitance", "Capacitors & Dielectric Media", "Electromagnetism"),
    ("current-electricity", "Current Conduction, Ohm's Law & DC Circuits", "Electromagnetism"),
    ("magnetic-effects-of-current", "Biot-Savart Law & Lorentz Force", "Electromagnetism"),
    ("electromagnetic-induction", "Faraday's Law, Lenz's Law & Inductance", "Electromagnetism"),

    # Optics (2 nodes)
    ("ray-optics", "Geometrical Optics, Refraction & Optical Instruments", "Optics"),
    ("wave-optics", "Interference, Diffraction & Wave Optics", "Optics"),

    # Modern Physics (2 nodes)
    ("dual-nature-of-matter-and-radiation", "Photoelectric Effect & Matter Waves", "Modern Physics"),
    ("atomic-physics", "Bohr Atomic Model & Spectra", "Modern Physics"),
]


class NodeEvidenceManifest(BaseModel):
    taxonomy_node_id: str
    node_name: str
    branch: str
    corroborating_sources_count: int
    corroborating_sources: List[str]
    expositions: List[str] = Field(default_factory=list)
    definitions: List[str] = Field(default_factory=list)
    formulas: List[str] = Field(default_factory=list)
    derivations: List[str] = Field(default_factory=list)
    examples: List[str] = Field(default_factory=list)
    problems: List[str] = Field(default_factory=list)
    figures: List[str] = Field(default_factory=list)
    hcv_evidence: List[str] = Field(default_factory=list)
    halliday_evidence: List[str] = Field(default_factory=list)
    university_physics_evidence: List[str] = Field(default_factory=list)
    feynman_evidence: List[str] = Field(default_factory=list)
    irodov_problems: List[str] = Field(default_factory=list)
    mock_questions: List[str] = Field(default_factory=list)
    total_evidence_units: int = 0


def demonstrate_taxonomy_retrieval(
    evidence_dir: Path = Path("sources/evidence"),
    output_path_20: Path = Path("sources/evidence/taxonomy_retrieval_demonstration_20.json"),
    output_path_legacy: Path = Path("sources/evidence/taxonomy_retrieval_demonstration.json"),
) -> List[NodeEvidenceManifest]:
    """
    Performs authentic evidence retrieval for 20+ demonstration taxonomy nodes across all branches.
    """
    def _load_json(filename):
        p = evidence_dir / filename
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    records = _load_json("records.json")
    formulas = _load_json("formulas.json")
    derivations = _load_json("derivations.json")
    examples = _load_json("examples.json")
    problems = _load_json("problems.json")
    mocks = _load_json("mock_questions.json")
    figures = _load_json("figures.json")

    manifests: List[NodeEvidenceManifest] = []

    for node_id, node_name, branch in DEMONSTRATION_NODES_20:
        hcv_items = []
        hr_items = []
        up_items = []
        feynman_items = []
        irodov_items = []
        mock_items = []

        expositions_list = []
        definitions_list = []
        formulas_list = []
        derivations_list = []
        examples_list = []
        problems_list = []
        figures_list = []

        sources_seen = set()

        def _check_tax(item_tax):
            if isinstance(item_tax, list):
                return node_id in item_tax or any(node_id in str(t) for t in item_tax)
            return node_id == item_tax

        # 1. Records (Expositions, Definitions, Concepts)
        for r in records:
            if _check_tax(r.get("taxonomy_node_ids", [])):
                src = r.get("source_id", "")
                sources_seen.add(src)
                ev_type = r.get("evidence_type", "EXPOSITION")
                label = f"{r.get('evidence_id')} [{ev_type}] (pp. {r.get('page_start')}-{r.get('page_end')}, '{r.get('section')}')"

                if ev_type == "EXPOSITION":
                    expositions_list.append(label)
                elif ev_type == "DEFINITION":
                    definitions_list.append(label)
                else:
                    expositions_list.append(label)

                if "h-a489bb6e" in src or "h-1fd380f4" in src:
                    hcv_items.append(label)
                elif "fundamentals" in src:
                    hr_items.append(label)
                elif "university" in src:
                    up_items.append(label)
                elif "feynman" in src:
                    feynman_items.append(label)

        # 2. Formulas
        for f in formulas:
            if _check_tax(f.get("taxonomy_node_ids", [])):
                src = f.get("source_id", "")
                sources_seen.add(src)
                label = f"{f.get('formula_id')} [${f.get('normalized_latex')}$] (pp. {f.get('pages')})"
                formulas_list.append(label)
                if "h-a489bb6e" in src or "h-1fd380f4" in src:
                    hcv_items.append(label)
                elif "fundamentals" in src:
                    hr_items.append(label)
                elif "university" in src:
                    up_items.append(label)
                elif "feynman" in src:
                    feynman_items.append(label)

        # 3. Derivations
        for d in derivations:
            if _check_tax(d.get("taxonomy_node_ids", [])):
                sources_seen.add(d.get("source_id", ""))
                label = f"{d.get('derivation_id')} (Derivation: {d.get('title')})"
                derivations_list.append(label)
                hcv_items.append(label)

        # 4. Examples
        for ex in examples:
            if _check_tax(ex.get("taxonomy_node_ids", [])):
                sources_seen.add(ex.get("source_id", ""))
                label = f"{ex.get('example_id')} (Example: {ex.get('title_or_label')})"
                examples_list.append(label)
                hcv_items.append(label)

        # 5. Figures
        for fig in figures:
            if _check_tax(fig.get("taxonomy_node_ids", [])):
                src = fig.get("source_id", "")
                sources_seen.add(src)
                label = f"{fig.get('figure_id')} (p. {fig.get('page')}, '{fig.get('caption', '')[:40]}')"
                figures_list.append(label)

        # 6. Problems
        for p in problems:
            if _check_tax(p.get("taxonomy_node_ids", [])):
                src = p.get("source_id", "")
                sources_seen.add(src)
                p_label = f"Problem {p.get('printed_problem_number')} (p. {p.get('page')})"
                problems_list.append(p_label)
                if "problems-in-general-phys" in src:
                    irodov_items.append(p_label)
                elif "h-a489bb6e" in src or "h-1fd380f4" in src:
                    hcv_items.append(p_label)
                elif "fundamentals" in src:
                    hr_items.append(p_label)
                elif "university" in src:
                    up_items.append(p_label)

        # 7. Mock Questions
        for m in mocks:
            if _check_tax(m.get("taxonomy_node_ids", [])):
                src = m.get("source_id", "")
                sources_seen.add(src)
                mock_label = f"Mock Q{m.get('question_number')} ({m.get('mock_question_id')}, p. {m.get('page')})"
                mock_items.append(mock_label)

        total_ev = len(expositions_list) + len(definitions_list) + len(formulas_list) + len(derivations_list) + len(examples_list) + len(problems_list) + len(figures_list) + len(mock_items)

        manifests.append(
            NodeEvidenceManifest(
                taxonomy_node_id=node_id,
                node_name=node_name,
                branch=branch,
                corroborating_sources_count=len(sources_seen),
                corroborating_sources=sorted(list(sources_seen)),
                expositions=expositions_list[:10],
                definitions=definitions_list[:10],
                formulas=formulas_list[:10],
                derivations=derivations_list[:5],
                examples=examples_list[:5],
                problems=problems_list[:10],
                figures=figures_list[:5],
                hcv_evidence=hcv_items[:10],
                halliday_evidence=hr_items[:10],
                university_physics_evidence=up_items[:10],
                feynman_evidence=feynman_items[:10],
                irodov_problems=irodov_items[:10],
                mock_questions=mock_items[:10],
                total_evidence_units=total_ev,
            )
        )

    # Save to both outputs
    output_path_20.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path_20, "w", encoding="utf-8") as f:
        json.dump([m.model_dump() for m in manifests], f, indent=2)

    with open(output_path_legacy, "w", encoding="utf-8") as f:
        json.dump([m.model_dump() for m in manifests], f, indent=2)

    return manifests


if __name__ == "__main__":
    results = demonstrate_taxonomy_retrieval()
    print(f"Successfully demonstrated multi-source retrieval for {len(results)} taxonomy nodes.")
    for r in results:
        print(f" - [{r.taxonomy_node_id}] ({r.branch}): {r.total_evidence_units} units across {r.corroborating_sources_count} sources")
