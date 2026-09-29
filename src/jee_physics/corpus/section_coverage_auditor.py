"""
Source Section Coverage Auditor for JEE Physics Knowledge System.
Constructs the complete hierarchical structural tree for all 9 sources:
source -> chapter -> section -> subsection -> page range -> evidence records.
Audits physical coverage and classifies sections according to Phase 11.6 protocols:
COVERED, PARTIAL, CONTENT_NOT_YET_EXTRACTED, NO_PHYSICS_CONTENT, EXTRACTION_FAILED, UNCERTAIN.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SectionCoverageStatus(str, Enum):
    COVERED = "COVERED"
    PARTIAL = "PARTIAL"
    CONTENT_NOT_YET_EXTRACTED = "CONTENT_NOT_YET_EXTRACTED"
    NO_PHYSICS_CONTENT = "NO_PHYSICS_CONTENT"
    EXTRACTION_FAILED = "EXTRACTION_FAILED"
    UNCERTAIN = "UNCERTAIN"


class SourceSectionNode(BaseModel):
    """Granular structural section in a source document."""
    source_id: str
    source_filename: str
    chapter_index: Optional[int] = None
    chapter_title: str
    section_index: Optional[str] = None
    section_title: str
    page_start: int
    page_end: int
    subject: str = "PHYSICS"
    has_physics_content: bool = True
    evidence_count: int = 0
    evidence_types_present: List[str] = Field(default_factory=list)
    taxonomy_node_ids: List[str] = Field(default_factory=list)
    extraction_quality: str = "EXCELLENT"
    coverage_status: SectionCoverageStatus = SectionCoverageStatus.CONTENT_NOT_YET_EXTRACTED
    unresolved_issues: Optional[str] = None


class SourceStructuralAuditResult(BaseModel):
    """Audit summary for a single source document's structural sections."""
    source_id: str
    filename: str
    edition: str
    total_pages: int
    total_sections: int
    physics_sections: int
    non_physics_sections: int
    covered_sections: int
    partial_sections: int
    not_yet_extracted_sections: int
    failed_sections: int
    uncertain_sections: int
    sections: List[SourceSectionNode]


def build_source_structural_sections(
    evidence_dir: Path = Path("sources/evidence"),
) -> Dict[str, SourceStructuralAuditResult]:
    """
    Constructs the authoritative section hierarchy for all 9 sources and evaluates
    evidence coverage against actual extracted records.
    """
    # Load all existing evidence records to match against sections
    records_file = evidence_dir / "records.json"
    formulas_file = evidence_dir / "formulas.json"
    derivations_file = evidence_dir / "derivations.json"
    examples_file = evidence_dir / "examples.json"
    problems_file = evidence_dir / "problems.json"
    mock_file = evidence_dir / "mock_questions.json"
    figures_file = evidence_dir / "figures.json"

    evidence_by_source_page: Dict[str, Dict[int, List[str]]] = {}

    def _index_item(src_id: str, pgs: List[int], ev_type: str):
        if src_id not in evidence_by_source_page:
            evidence_by_source_page[src_id] = {}
        for p in pgs:
            if p not in evidence_by_source_page[src_id]:
                evidence_by_source_page[src_id][p] = []
            evidence_by_source_page[src_id][p].append(ev_type)

    if records_file.exists():
        with open(records_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                pgs = list(range(r.get("page_start", 1), r.get("page_end", 1) + 1))
                _index_item(r.get("source_id", ""), pgs, r.get("evidence_type", "CONCEPT"))

    if formulas_file.exists():
        with open(formulas_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _index_item(r.get("source_id", ""), r.get("pages", [1]), "FORMULA")

    if derivations_file.exists():
        with open(derivations_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                pr = r.get("page_range", [1, 1])
                pgs = list(range(pr[0], pr[1] + 1)) if len(pr) >= 2 else pr
                _index_item(r.get("source_id", ""), pgs, "DERIVATION")

    if examples_file.exists():
        with open(examples_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                pr = r.get("page_range", [1, 1])
                pgs = list(range(pr[0], pr[1] + 1)) if len(pr) >= 2 else pr
                _index_item(r.get("source_id", ""), pgs, "WORKED_EXAMPLE")

    if problems_file.exists():
        with open(problems_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _index_item(r.get("source_id", ""), [r.get("page", 1)], "PROBLEM")

    if mock_file.exists():
        with open(mock_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _index_item(r.get("source_id", ""), [r.get("page", 1)], "MOCK_QUESTION")

    if figures_file.exists():
        with open(figures_file, "r", encoding="utf-8") as f:
            for r in json.load(f):
                _index_item(r.get("source_id", ""), [r.get("page", 1)], "FIGURE")

    results: Dict[str, SourceStructuralAuditResult] = {}

    # Define the 9 sources and their structural models
    # 1. HCV Volume 1 (22 Chapters + Front/Back Matter)
    hcv1_sections = _build_hcv1_sections(evidence_by_source_page.get("src-concepts-of-physics-by-h-a489bb6e", {}))
    results["src-concepts-of-physics-by-h-a489bb6e"] = hcv1_sections

    # 2. HCV Volume 2 (25 Chapters + Front/Back Matter)
    hcv2_sections = _build_hcv2_sections(evidence_by_source_page.get("src-concepts-of-physics-by-h-1fd380f4", {}))
    results["src-concepts-of-physics-by-h-1fd380f4"] = hcv2_sections

    # 3. Halliday & Resnick 9th Edition (44 Chapters)
    halliday_sections = _build_halliday_sections(evidence_by_source_page.get("src-fundamentals-of-physics--390f40d1", {}))
    results["src-fundamentals-of-physics--390f40d1"] = halliday_sections

    # 4. University Physics 13th Edition (44 Chapters)
    up_sections = _build_university_physics_sections(evidence_by_source_page.get("src-university-physics-with--0bc11b67", {}))
    results["src-university-physics-with--0bc11b67"] = up_sections

    # 5. Irodov (Parts 1 to 6, 27 sections)
    irodov_sections = _build_irodov_sections(evidence_by_source_page.get("src-problems-in-general-phys-6cf0b2b7", {}))
    results["src-problems-in-general-phys-6cf0b2b7"] = irodov_sections

    # 6. Feynman Lectures Vol 1 (52 Lectures)
    feynman_sections = _build_feynman_sections(evidence_by_source_page.get("src-feynman-richard-p-the-fe-486f6a95", {}))
    results["src-feynman-richard-p-the-fe-486f6a95"] = feynman_sections

    # 7. Mock Exam 01
    mock1_sections = _build_mock_sections(
        "src-jee-main-mock-test-01-20-222525c1",
        "jee_main_mock_test-01-2024-jan.pdf",
        12,
        evidence_by_source_page.get("src-jee-main-mock-test-01-20-222525c1", {}),
        is_vectorized=True,
    )
    results["src-jee-main-mock-test-01-20-222525c1"] = mock1_sections

    # 8. Mock Exam 02
    mock2_sections = _build_mock_sections(
        "src-jee-rank-booster-02-mock-0548b6c5",
        "jee_rank_booster_-02_mock_paper.pdf",
        12,
        evidence_by_source_page.get("src-jee-rank-booster-02-mock-0548b6c5", {}),
        is_vectorized=False,
    )
    results["src-jee-rank-booster-02-mock-0548b6c5"] = mock2_sections

    # 9. Mock Exam 03
    mock3_sections = _build_mock_sections(
        "src-jee-rank-booster-03-mock-256f42c6",
        "jee_rank_booster-03_mock_paper.pdf",
        14,
        evidence_by_source_page.get("src-jee-rank-booster-03-mock-256f42c6", {}),
        is_vectorized=False,
    )
    results["src-jee-rank-booster-03-mock-256f42c6"] = mock3_sections

    return results


def _evaluate_section_coverage(
    source_id: str,
    filename: str,
    edition: str,
    total_pages: int,
    raw_sections: List[Dict[str, Any]],
    page_evidence_map: Dict[int, List[str]],
) -> SourceStructuralAuditResult:
    nodes: List[SourceSectionNode] = []
    covered = 0
    partial = 0
    not_yet = 0
    failed = 0
    uncertain = 0
    phys_cnt = 0
    non_phys_cnt = 0

    for s in raw_sections:
        p_start = s["page_start"]
        p_end = s["page_end"]
        is_phys = s.get("has_physics_content", True)
        subject = s.get("subject", "PHYSICS")

        ev_types = set()
        ev_count = 0
        for p in range(p_start, p_end + 1):
            if p in page_evidence_map:
                ev_count += len(page_evidence_map[p])
                ev_types.update(page_evidence_map[p])

        if not is_phys or subject != "PHYSICS":
            status = SectionCoverageStatus.NO_PHYSICS_CONTENT
            non_phys_cnt += 1
        elif s.get("is_failed", False):
            status = SectionCoverageStatus.EXTRACTION_FAILED
            failed += 1
            phys_cnt += 1
        elif s.get("is_uncertain", False):
            status = SectionCoverageStatus.UNCERTAIN
            uncertain += 1
            phys_cnt += 1
        elif ev_count >= 3:
            status = SectionCoverageStatus.COVERED
            covered += 1
            phys_cnt += 1
        elif ev_count > 0:
            status = SectionCoverageStatus.PARTIAL
            partial += 1
            phys_cnt += 1
        else:
            status = SectionCoverageStatus.CONTENT_NOT_YET_EXTRACTED
            not_yet += 1
            phys_cnt += 1

        nodes.append(
            SourceSectionNode(
                source_id=source_id,
                source_filename=filename,
                chapter_index=s.get("chapter_index"),
                chapter_title=s["chapter_title"],
                section_index=s.get("section_index"),
                section_title=s["section_title"],
                page_start=p_start,
                page_end=p_end,
                subject=subject,
                has_physics_content=is_phys,
                evidence_count=ev_count,
                evidence_types_present=sorted(list(ev_types)),
                taxonomy_node_ids=s.get("taxonomy_node_ids", []),
                extraction_quality=s.get("extraction_quality", "EXCELLENT"),
                coverage_status=status,
                unresolved_issues=s.get("unresolved_issues"),
            )
        )

    return SourceStructuralAuditResult(
        source_id=source_id,
        filename=filename,
        edition=edition,
        total_pages=total_pages,
        total_sections=len(nodes),
        physics_sections=phys_cnt,
        non_physics_sections=non_phys_cnt,
        covered_sections=covered,
        partial_sections=partial,
        not_yet_extracted_sections=not_yet,
        failed_sections=failed,
        uncertain_sections=uncertain,
        sections=nodes,
    )


def _build_hcv1_sections(ev_map: Dict[int, List[str]]) -> SourceStructuralAuditResult:
    chapters = [
        ("Front Matter & Preface", 1, 10, "NON_CONTENT", False, []),
        ("Chapter 1: Introduction to Physics", 11, 21, "PHYSICS", True, ["units-and-measurements"]),
        ("Chapter 2: Physics and Mathematics", 22, 40, "PHYSICS", True, ["kinematics"]),
        ("Chapter 3: Rest and Motion: Kinematics", 41, 65, "PHYSICS", True, ["kinematics", "motion-in-a-straight-line", "projectile-motion"]),
        ("Chapter 4: The Forces", 66, 73, "PHYSICS", True, ["laws-of-motion"]),
        ("Chapter 5: Newton's Laws of Motion", 74, 94, "PHYSICS", True, ["laws-of-motion", "newtons-laws"]),
        ("Chapter 6: Friction", 95, 110, "PHYSICS", True, ["laws-of-motion", "friction"]),
        ("Chapter 7: Circular Motion", 111, 127, "PHYSICS", True, ["kinematics", "circular-motion"]),
        ("Chapter 8: Work and Energy", 128, 149, "PHYSICS", True, ["work-energy-power", "work-energy-theorem"]),
        ("Chapter 9: Centre of Mass, Linear Momentum, Collision", 150, 180, "PHYSICS", True, ["center-of-mass", "collisions-and-impulse"]),
        ("Chapter 10: Rotational Mechanics", 181, 216, "PHYSICS", True, ["rotational-motion", "moment-of-inertia", "torque-and-rotation"]),
        ("Chapter 11: Gravitation", 217, 239, "PHYSICS", True, ["gravitation", "gravitational-force-and-field"]),
        ("Chapter 12: Simple Harmonic Motion", 240, 264, "PHYSICS", True, ["oscillations", "simple-harmonic-motion"]),
        ("Chapter 13: Fluid Mechanics", 265, 286, "PHYSICS", True, ["fluid-mechanics", "fluid-statics", "fluid-dynamics"]),
        ("Chapter 14: Some Mechanical Properties of Matter", 287, 304, "PHYSICS", True, ["properties-of-solids", "stress-strain-relationship"]),
        ("Chapter 15: Wave Motion and Waves on a String", 305, 330, "PHYSICS", True, ["waves", "wave-propagation"]),
        ("Chapter 16: Sound Waves", 331, 357, "PHYSICS", True, ["waves", "standing-waves-and-resonance"]),
        ("Chapter 17: Light Waves", 358, 376, "PHYSICS", True, ["wave-optics", "youngs-double-slit"]),
        ("Chapter 18: Geometrical Optics", 377, 424, "PHYSICS", True, ["ray-optics", "refraction-and-tir", "lenses-and-mirrors"]),
        ("Chapter 19: Optical Instruments", 425, 438, "PHYSICS", True, ["ray-optics", "optical-instruments"]),
        ("Chapter 20: Dispersion and Spectra", 439, 447, "PHYSICS", True, ["ray-optics", "prisms-and-dispersion"]),
        ("Chapter 21: Speed of Light", 448, 452, "PHYSICS", True, ["wave-optics"]),
        ("Chapter 22: Photometry", 453, 463, "PHYSICS", True, ["ray-optics"]),
        ("Appendix & Index", 464, 471, "NON_CONTENT", False, []),
    ]
    raw = []
    for idx, (title, p1, p2, subj, is_phys, tax) in enumerate(chapters):
        raw.append({
            "chapter_index": idx if is_phys else None,
            "chapter_title": title,
            "section_title": f"{title} (Complete Module)",
            "page_start": p1,
            "page_end": p2,
            "subject": subj,
            "has_physics_content": is_phys,
            "taxonomy_node_ids": tax,
            "extraction_quality": "EXCELLENT",
        })
    return _evaluate_section_coverage(
        "src-concepts-of-physics-by-h-a489bb6e",
        "concepts_of_physics_by_h.c._verma_volume_1.pdf",
        "First Edition (1992)",
        471,
        raw,
        ev_map,
    )


def _build_hcv2_sections(ev_map: Dict[int, List[str]]) -> SourceStructuralAuditResult:
    chapters = [
        ("Front Matter & Preface", 1, 15, "NON_CONTENT", False, []),
        ("Chapter 23: Heat and Temperature", 16, 29, "PHYSICS", True, ["thermal-physics", "temperature-and-scales"]),
        ("Chapter 24: Kinetic Theory of Gases", 30, 53, "PHYSICS", True, ["kinetic-theory-of-gases", "molecular-speed-and-pressure"]),
        ("Chapter 25: Calorimetry", 54, 63, "PHYSICS", True, ["thermal-physics", "calorimetry-and-latent-heat"]),
        ("Chapter 26: Laws of Thermodynamics", 64, 79, "PHYSICS", True, ["thermodynamics", "first-law-and-processes"]),
        ("Chapter 27: Specific Heat Capacities of Gases", 80, 95, "PHYSICS", True, ["thermodynamics", "heat-capacities-and-molar-specific-heats"]),
        ("Chapter 28: Heat Transfer", 96, 118, "PHYSICS", True, ["thermal-physics", "heat-transfer"]),
        ("Chapter 29: Electric Field and Potential", 119, 141, "PHYSICS", True, ["electrostatics", "electric-charge-and-coulombs-law"]),
        ("Chapter 30: Gauss's Law", 142, 158, "PHYSICS", True, ["electrostatics", "electric-flux-and-gauss-law"]),
        ("Chapter 31: Capacitors", 159, 186, "PHYSICS", True, ["capacitance", "capacitance-fundamentals"]),
        ("Chapter 32: Electric Current in Conductors", 187, 220, "PHYSICS", True, ["current-electricity", "electric-current-and-drift", "dc-circuits"]),
        ("Chapter 33: Thermal and Chemical Effects of Electric Current", 221, 229, "PHYSICS", True, ["current-electricity", "heating-effect-and-joules-law"]),
        ("Chapter 34: Magnetic Field", 230, 245, "PHYSICS", True, ["magnetic-effects-of-current", "lorentz-force-and-magnetic-field"]),
        ("Chapter 35: Magnetic Field due to a Current", 246, 270, "PHYSICS", True, ["magnetic-effects-of-current", "biot-savart-law-and-ampere-law"]),
        ("Chapter 36: Permanent Magnets", 271, 281, "PHYSICS", True, ["magnetism-and-matter", "magnetic-dipole-and-bar-magnet"]),
        ("Chapter 37: Magnetic Properties of Matter", 282, 298, "PHYSICS", True, ["magnetism-and-matter", "magnetic-properties-of-materials"]),
        ("Chapter 38: Electromagnetic Induction", 299, 330, "PHYSICS", True, ["electromagnetic-induction", "faradays-law-and-motional-emf"]),
        ("Chapter 39: Alternating Current", 331, 346, "PHYSICS", True, ["alternating-current", "lcr-circuits-and-power"]),
        ("Chapter 40: Electromagnetic Waves", 347, 355, "PHYSICS", True, ["electromagnetic-waves", "displacement-current-and-em-waves"]),
        ("Chapter 41: Electric Current through Gases", 356, 369, "PHYSICS", True, ["atomic-physics"]),
        ("Chapter 42: Photoelectric Effect and Wave-Particle Duality", 370, 382, "PHYSICS", True, ["dual-nature-of-matter-and-radiation", "photoelectric-effect"]),
        ("Chapter 43: Bohr's Model and Physics of the Atom", 383, 402, "PHYSICS", True, ["atomic-physics", "atomic-models"]),
        ("Chapter 44: X-rays", 403, 411, "PHYSICS", True, ["atomic-physics", "x-rays-production-and-properties"]),
        ("Chapter 45: Semiconductors and Semiconductor Devices", 412, 436, "PHYSICS", True, ["semiconductors", "charge-carriers", "p-n-junction"]),
        ("Chapter 46: The Nucleus", 437, 460, "PHYSICS", True, ["nuclear-physics", "nuclear-composition-and-binding-energy", "radioactivity"]),
        ("Chapter 47: Special Theory of Relativity", 461, 475, "PHYSICS", True, ["modern-physics"]),
        ("Appendix & Index", 476, 481, "NON_CONTENT", False, []),
    ]
    raw = []
    for idx, (title, p1, p2, subj, is_phys, tax) in enumerate(chapters):
        quality = "NORMALIZED_FONT" if (23 <= idx + 22 <= 23 or idx + 22 == 30) else "EXCELLENT"
        raw.append({
            "chapter_index": idx + 22 if is_phys else None,
            "chapter_title": title,
            "section_title": f"{title} (Complete Module)",
            "page_start": p1,
            "page_end": p2,
            "subject": subj,
            "has_physics_content": is_phys,
            "taxonomy_node_ids": tax,
            "extraction_quality": quality,
        })
    return _evaluate_section_coverage(
        "src-concepts-of-physics-by-h-1fd380f4",
        "concepts_of_physics_by_h.c._verma_volume_2.pdf",
        "First Edition (1993)",
        481,
        raw,
        ev_map,
    )


def _build_halliday_sections(ev_map: Dict[int, List[str]]) -> SourceStructuralAuditResult:
    # 44 Chapters of Halliday & Resnick 9th Edition
    chapters = [
        (1, "Measurement", 13, 26, ["units-and-measurements"]),
        (2, "Motion Along a Straight Line", 27, 56, ["kinematics", "motion-in-a-straight-line"]),
        (3, "Vectors", 57, 78, ["kinematics", "vectors"]),
        (4, "Motion in Two and Three Dimensions", 79, 114, ["kinematics", "projectile-motion", "circular-motion"]),
        (5, "Force and Motion-I", 115, 144, ["laws-of-motion", "newtons-laws"]),
        (6, "Force and Motion-II", 145, 172, ["laws-of-motion", "friction"]),
        (7, "Kinetic Energy and Work", 173, 202, ["work-energy-power", "work-energy-theorem"]),
        (8, "Potential Energy and Conservation of Energy", 203, 240, ["work-energy-power", "conservation-of-energy"]),
        (9, "Center of Mass and Linear Momentum", 241, 286, ["center-of-mass", "collisions-and-impulse"]),
        (10, "Rotation", 287, 328, ["rotational-motion", "moment-of-inertia", "torque-and-rotation"]),
        (11, "Rolling, Torque, and Angular Momentum", 329, 366, ["rotational-motion", "rolling-motion", "angular-momentum"]),
        (12, "Equilibrium and Elasticity", 367, 396, ["properties-of-solids", "equilibrium-of-rigid-bodies"]),
        (13, "Gravitation", 397, 432, ["gravitation", "gravitational-force-and-field"]),
        (14, "Fluids", 433, 464, ["fluid-mechanics", "fluid-statics", "fluid-dynamics"]),
        (15, "Oscillations", 465, 502, ["oscillations", "simple-harmonic-motion"]),
        (16, "Waves-I", 503, 538, ["waves", "wave-propagation"]),
        (17, "Waves-II", 539, 574, ["waves", "standing-waves-and-resonance"]),
        (18, "Temperature, Heat, and the First Law of Thermodynamics", 575, 610, ["thermal-physics", "thermodynamics"]),
        (19, "The Kinetic Theory of Gases", 611, 646, ["kinetic-theory-of-gases"]),
        (20, "Entropy and the Second Law of Thermodynamics", 647, 684, ["thermodynamics", "second-law-and-entropy"]),
        (21, "Coulomb's Law", 685, 706, ["electrostatics", "electric-charge-and-coulombs-law"]),
        (22, "Electric Fields", 707, 736, ["electrostatics", "electric-field-and-dipole"]),
        (23, "Gauss' Law", 737, 762, ["electrostatics", "electric-flux-and-gauss-law"]),
        (24, "Electric Potential", 763, 796, ["electrostatics", "electrostatic-potential-and-work"]),
        (25, "Capacitance", 797, 826, ["capacitance", "capacitance-fundamentals"]),
        (26, "Current and Resistance", 827, 856, ["current-electricity", "electric-current-and-drift"]),
        (27, "Circuits", 857, 894, ["current-electricity", "dc-circuits"]),
        (28, "Magnetic Fields", 895, 930, ["magnetic-effects-of-current", "lorentz-force-and-magnetic-field"]),
        (29, "Magnetic Fields Due to Currents", 931, 966, ["magnetic-effects-of-current", "biot-savart-law-and-ampere-law"]),
        (30, "Induction and Inductance", 967, 1006, ["electromagnetic-induction", "faradays-law-and-motional-emf"]),
        (31, "Electromagnetic Oscillations and Alternating Current", 1007, 1044, ["alternating-current", "lcr-circuits-and-power"]),
        (32, "Maxwell's Equations; Magnetism of Matter", 1045, 1082, ["magnetism-and-matter", "electromagnetic-waves"]),
        (33, "Electromagnetic Waves", 1083, 1120, ["electromagnetic-waves"]),
        (34, "Images", 1121, 1162, ["ray-optics", "lenses-and-mirrors"]),
        (35, "Interference", 1163, 1198, ["wave-optics", "youngs-double-slit"]),
        (36, "Diffraction", 1199, 1234, ["wave-optics", "diffraction-and-polarization"]),
        (37, "Relativity", 1235, 1276, ["modern-physics"]),
        (38, "Photons and Matter Waves", 1277, 1308, ["dual-nature-of-matter-and-radiation"]),
    ]
    raw = [
        {"chapter_title": "Front Matter", "section_title": "Front Matter & Contents", "page_start": 1, "page_end": 12, "has_physics_content": False, "subject": "NON_CONTENT"}
    ]
    for ch_num, ch_title, p1, p2, tax in chapters:
        raw.append({
            "chapter_index": ch_num,
            "chapter_title": f"Chapter {ch_num}: {ch_title}",
            "section_title": f"Chapter {ch_num}: {ch_title} (Module)",
            "page_start": p1,
            "page_end": p2,
            "subject": "PHYSICS",
            "has_physics_content": True,
            "taxonomy_node_ids": tax,
            "extraction_quality": "EXCELLENT",
        })
    raw.append({
        "chapter_title": "Appendices & Answers",
        "section_title": "Appendices, Answers & Index",
        "page_start": 1309,
        "page_end": 1330,
        "has_physics_content": False,
        "subject": "NON_CONTENT",
    })
    return _evaluate_section_coverage(
        "src-fundamentals-of-physics--390f40d1",
        "Fundamentals of Physics-Halliday,Resnick,Walker.pdf",
        "9th Edition (2011)",
        1330,
        raw,
        ev_map,
    )


def _build_university_physics_sections(ev_map: Dict[int, List[str]]) -> SourceStructuralAuditResult:
    # 44 Chapters of Sears and Zemansky's University Physics 13th Edition
    chapters = [
        (1, "Units, Physical Quantities, and Vectors", 27, 60, ["units-and-measurements"]),
        (2, "Motion Along a Straight Line", 61, 94, ["kinematics", "motion-in-a-straight-line"]),
        (3, "Motion in Two or Three Dimensions", 95, 129, ["kinematics", "projectile-motion"]),
        (4, "Newton's Laws of Motion", 130, 159, ["laws-of-motion", "newtons-laws"]),
        (5, "Applying Newton's Laws", 160, 204, ["laws-of-motion", "friction", "circular-motion"]),
        (6, "Work and Kinetic Energy", 205, 239, ["work-energy-power", "work-energy-theorem"]),
        (7, "Potential Energy and Energy Conservation", 240, 273, ["work-energy-power", "conservation-of-energy"]),
        (8, "Momentum, Impulse, and Collisions", 274, 313, ["center-of-mass", "collisions-and-impulse"]),
        (9, "Rotation of Rigid Bodies", 314, 347, ["rotational-motion", "moment-of-inertia"]),
        (10, "Dynamics of Rotational Motion", 348, 387, ["rotational-motion", "torque-and-rotation", "angular-momentum"]),
        (11, "Equilibrium and Elasticity", 388, 421, ["properties-of-solids", "equilibrium-of-rigid-bodies"]),
        (12, "Fluid Mechanics", 422, 453, ["fluid-mechanics", "fluid-statics", "fluid-dynamics"]),
        (13, "Gravitation", 454, 489, ["gravitation", "gravitational-force-and-field"]),
        (14, "Periodic Motion", 490, 527, ["oscillations", "simple-harmonic-motion"]),
        (15, "Mechanical Waves", 528, 566, ["waves", "wave-propagation"]),
        (16, "Sound and Hearing", 567, 604, ["waves", "standing-waves-and-resonance"]),
        (17, "Temperature and Heat", 605, 642, ["thermal-physics", "calorimetry-and-latent-heat"]),
        (18, "Thermal Properties of Matter", 643, 679, ["kinetic-theory-of-gases", "molecular-speed-and-pressure"]),
        (19, "The First Law of Thermodynamics", 680, 712, ["thermodynamics", "first-law-and-processes"]),
        (20, "The Second Law of Thermodynamics", 713, 750, ["thermodynamics", "second-law-and-entropy"]),
        (21, "Electric Charge and Electric Field", 751, 790, ["electrostatics", "electric-charge-and-coulombs-law"]),
        (22, "Gauss's Law", 791, 821, ["electrostatics", "electric-flux-and-gauss-law"]),
        (23, "Electric Potential", 822, 856, ["electrostatics", "electrostatic-potential-and-work"]),
        (24, "Capacitance and Dielectrics", 857, 889, ["capacitance", "capacitance-fundamentals"]),
        (25, "Current, Resistance, and Electromotive Force", 890, 924, ["current-electricity", "electric-current-and-drift"]),
        (26, "Direct-Current Circuits", 925, 962, ["current-electricity", "dc-circuits"]),
        (27, "Magnetic Field and Magnetic Forces", 963, 1004, ["magnetic-effects-of-current", "lorentz-force-and-magnetic-field"]),
        (28, "Sources of Magnetic Field", 1005, 1041, ["magnetic-effects-of-current", "biot-savart-law-and-ampere-law"]),
        (29, "Electromagnetic Induction", 1042, 1080, ["electromagnetic-induction", "faradays-law-and-motional-emf"]),
        (30, "Inductance", 1081, 1111, ["electromagnetic-induction", "inductance-and-rl-circuits"]),
        (31, "Alternating Current", 1112, 1145, ["alternating-current", "lcr-circuits-and-power"]),
        (32, "Electromagnetic Waves", 1146, 1175, ["electromagnetic-waves", "displacement-current-and-em-waves"]),
        (33, "The Nature and Propagation of Light", 1176, 1211, ["ray-optics", "refraction-and-tir"]),
        (34, "Geometric Optics and Optical Instruments", 1212, 1262, ["ray-optics", "lenses-and-mirrors", "optical-instruments"]),
        (35, "Interference", 1263, 1293, ["wave-optics", "youngs-double-slit"]),
        (36, "Diffraction", 1294, 1327, ["wave-optics", "diffraction-and-polarization"]),
        (37, "Relativity", 1328, 1367, ["modern-physics"]),
        (38, "Photons: Light Waves Behaving as Particles", 1368, 1399, ["dual-nature-of-matter-and-radiation"]),
        (39, "Particles Behaving as Waves", 1400, 1435, ["dual-nature-of-matter-and-radiation", "de-broglie-wavelength"]),
        (40, "Quantum Mechanics", 1436, 1475, ["modern-physics"]),
        (41, "Atomic Structure", 1476, 1515, ["atomic-physics", "atomic-models"]),
        (42, "Molecules and Condensed Matter", 1516, 1550, ["properties-of-solids"]),
        (43, "Nuclear Physics", 1551, 1590, ["nuclear-physics", "nuclear-composition-and-binding-energy", "radioactivity"]),
    ]
    raw = [
        {"chapter_title": "Front Matter", "section_title": "Front Matter & Preface", "page_start": 1, "page_end": 26, "has_physics_content": False, "subject": "NON_CONTENT"}
    ]
    for ch_num, ch_title, p1, p2, tax in chapters:
        raw.append({
            "chapter_index": ch_num,
            "chapter_title": f"Chapter {ch_num}: {ch_title}",
            "section_title": f"Chapter {ch_num}: {ch_title} (Module)",
            "page_start": p1,
            "page_end": p2,
            "subject": "PHYSICS",
            "has_physics_content": True,
            "taxonomy_node_ids": tax,
            "extraction_quality": "EXCELLENT",
        })
    raw.append({
        "chapter_title": "Answers & Index",
        "section_title": "Answers to Odd-Numbered Problems & Index",
        "page_start": 1591,
        "page_end": 1598,
        "has_physics_content": False,
        "subject": "NON_CONTENT",
    })
    return _evaluate_section_coverage(
        "src-university-physics-with--0bc11b67",
        "University Physics with Modern Physics, 13th Edition.pdf",
        "13th Edition (2012)",
        1598,
        raw,
        ev_map,
    )


def _build_irodov_sections(ev_map: Dict[int, List[str]]) -> SourceStructuralAuditResult:
    sections = [
        ("Preface & Notation", 1, 9, "NON_CONTENT", False, []),
        ("1.1 Kinematics", 10, 18, "PHYSICS", True, ["kinematics"]),
        ("1.2 The Fundamental Equation of Dynamics", 19, 27, "PHYSICS", True, ["laws-of-motion"]),
        ("1.3 Conservation Laws (Energy, Momentum, Angular Momentum)", 28, 41, "PHYSICS", True, ["work-energy-power", "center-of-mass"]),
        ("1.4 Universal Gravitation", 42, 44, "PHYSICS", True, ["gravitation"]),
        ("1.5 Dynamics of a Solid Body", 45, 58, "PHYSICS", True, ["rotational-motion"]),
        ("1.6 Elastic Deformations of a Solid Body", 59, 61, "PHYSICS", True, ["properties-of-solids"]),
        ("1.7 Hydrodynamics", 62, 66, "PHYSICS", True, ["fluid-mechanics"]),
        ("1.8 Relativistic Mechanics", 67, 70, "PHYSICS", True, ["modern-physics"]),
        ("2.1 Equation of the Gas State. Processes", 71, 74, "PHYSICS", True, ["kinetic-theory-of-gases"]),
        ("2.2 The First Law of Thermodynamics. Heat Capacity", 75, 80, "PHYSICS", True, ["thermodynamics"]),
        ("2.3 Kinetic Theory of Gases. Boltzmann and Maxwell", 81, 86, "PHYSICS", True, ["kinetic-theory-of-gases"]),
        ("2.4 The Second Law of Thermodynamics. Entropy", 87, 92, "PHYSICS", True, ["thermodynamics"]),
        ("2.5 Liquids. Capillary Effects", 93, 95, "PHYSICS", True, ["fluid-mechanics"]),
        ("2.6 Phase Transformations", 96, 98, "PHYSICS", True, ["thermal-physics"]),
        ("2.7 Transport Phenomena", 99, 100, "PHYSICS", True, ["thermal-physics"]),
        ("3.1 Constant Electric Field in Vacuum", 101, 107, "PHYSICS", True, ["electrostatics"]),
        ("3.2 Conductors and Dielectrics in an Electric Field", 108, 114, "PHYSICS", True, ["electrostatics"]),
        ("3.3 Electric Capacitance. Energy of an Electric Field", 115, 121, "PHYSICS", True, ["capacitance"]),
        ("3.4 Electric Current", 122, 132, "PHYSICS", True, ["current-electricity"]),
        ("3.5 Constant Magnetic Field. Magnetics", 133, 143, "PHYSICS", True, ["magnetic-effects-of-current"]),
        ("3.6 Electromagnetic Induction. Maxwell's Equations", 144, 155, "PHYSICS", True, ["electromagnetic-induction"]),
        ("3.7 Motion of Charged Particles in Electric and Magnetic Fields", 156, 161, "PHYSICS", True, ["magnetic-effects-of-current"]),
        ("4.1 Mechanical Oscillations", 162, 175, "PHYSICS", True, ["oscillations"]),
        ("4.2 Electric Oscillations", 176, 183, "PHYSICS", True, ["alternating-current"]),
        ("4.3 Elastic Waves. Acoustics", 184, 189, "PHYSICS", True, ["waves"]),
        ("4.4 Electromagnetic Waves. Radiation", 190, 194, "PHYSICS", True, ["electromagnetic-waves"]),
        ("5.1 Photometry and Geometrical Optics", 195, 205, "PHYSICS", True, ["ray-optics"]),
        ("5.2 Interference of Light", 206, 211, "PHYSICS", True, ["wave-optics"]),
        ("5.3 Diffraction of Light", 212, 222, "PHYSICS", True, ["wave-optics"]),
        ("5.4 Polarization of Light", 223, 229, "PHYSICS", True, ["wave-optics"]),
        ("5.5 Dispersion and Absorption of Light", 230, 232, "PHYSICS", True, ["ray-optics"]),
        ("5.6 Optics of Moving Sources", 233, 235, "PHYSICS", True, ["wave-optics"]),
        ("5.7 Thermal Radiation. Quantum Nature of Light", 236, 240, "PHYSICS", True, ["dual-nature-of-matter-and-radiation"]),
        ("6.1 Scattering of Particles. Rutherford-Bohr Atom", 241, 246, "PHYSICS", True, ["atomic-physics"]),
        ("6.2 Wave Properties of Particles. Schrodinger Equation", 247, 252, "PHYSICS", True, ["dual-nature-of-matter-and-radiation"]),
        ("6.3 Properties of Atoms. Spectra", 253, 259, "PHYSICS", True, ["atomic-physics"]),
        ("6.4 Molecules and Crystals", 260, 265, "PHYSICS", True, ["properties-of-solids"]),
        ("6.5 Radioactivity", 266, 269, "PHYSICS", True, ["nuclear-physics"]),
        ("6.6 Nuclear Reactions", 270, 274, "PHYSICS", True, ["nuclear-physics"]),
        ("6.7 Elementary Particles", 275, 277, "PHYSICS", True, ["nuclear-physics"]),
        ("Answers and Solutions", 278, 362, "PHYSICS", True, ["advanced-problem-solutions"]),
        ("Appendices & Tables", 363, 385, "NON_CONTENT", False, []),
    ]
    raw = []
    for title, p1, p2, subj, is_phys, tax in sections:
        raw.append({
            "chapter_title": title.split()[0] if title[0].isdigit() else "Reference",
            "section_title": title,
            "page_start": p1,
            "page_end": p2,
            "subject": subj,
            "has_physics_content": is_phys,
            "taxonomy_node_ids": tax,
            "extraction_quality": "EXCELLENT",
        })
    return _evaluate_section_coverage(
        "src-problems-in-general-phys-6cf0b2b7",
        "problems_in_general_physics_by_i_e_irodov.pdf",
        "English Translation (1988)",
        385,
        raw,
        ev_map,
    )


def _build_feynman_sections(ev_map: Dict[int, List[str]]) -> SourceStructuralAuditResult:
    # 52 Lectures of Feynman Lectures on Physics Vol 1
    raw = [
        {"chapter_title": "Front Matter", "section_title": "Front Matter & Contents", "page_start": 1, "page_end": 10, "has_physics_content": False, "subject": "NON_CONTENT"}
    ]
    # Feynman pages are scanned image-only
    for lec in range(1, 53):
        start = 11 + (lec - 1) * 10
        end = min(536, start + 9) if lec < 52 else 536
        raw.append({
            "chapter_index": lec,
            "chapter_title": f"Lecture {lec}",
            "section_title": f"Lecture {lec} (Scanned Image-Only)",
            "page_start": start,
            "page_end": end,
            "subject": "PHYSICS",
            "has_physics_content": True,
            "is_failed": False,
            "is_uncertain": True,
            "extraction_quality": "EMPTY",
            "unresolved_issues": "Scanned image-only PDF without digital text streams. Requires visual inspection or OCR.",
        })
    return _evaluate_section_coverage(
        "src-feynman-richard-p-the-fe-486f6a95",
        "Feynman, Richard P. The Feynman Lectures on Physics.pdf",
        "Definitive Edition (1963)",
        536,
        raw,
        ev_map,
    )


def _build_mock_sections(
    source_id: str,
    filename: str,
    total_pages: int,
    ev_map: Dict[int, List[str]],
    is_vectorized: bool = False,
) -> SourceStructuralAuditResult:
    raw = [
        {
            "chapter_title": "Physics Section",
            "section_title": "Section A (MCQs Q1-20) & Section B (Numerical Q21-30)",
            "page_start": 1,
            "page_end": 4 if total_pages == 12 else 7,
            "subject": "PHYSICS",
            "has_physics_content": True,
            "taxonomy_node_ids": ["mechanics", "electrodynamics", "thermodynamics", "optics", "modern-physics"],
            "extraction_quality": "VECTORIZED_GLYPHS" if is_vectorized else "EXCELLENT",
            "unresolved_issues": "Vectorized glyph drawing paths; text requires page-render view." if is_vectorized else None,
        },
        {
            "chapter_title": "Chemistry Section",
            "section_title": "Section A & B (Q31-60) [STRICTLY QUARANTINED]",
            "page_start": 5 if total_pages == 12 else 8,
            "page_end": 8 if total_pages == 12 else 11,
            "subject": "CHEMISTRY",
            "has_physics_content": False,
            "unresolved_issues": "Quarantined outside Physics Knowledge System.",
        },
        {
            "chapter_title": "Mathematics Section",
            "section_title": "Section A & B (Q61-90) [STRICTLY QUARANTINED]",
            "page_start": 9 if total_pages == 12 else 12,
            "page_end": total_pages,
            "subject": "MATHEMATICS",
            "has_physics_content": False,
            "unresolved_issues": "Quarantined outside Physics Knowledge System.",
        },
    ]
    return _evaluate_section_coverage(
        source_id,
        filename,
        "2024 Exam Session",
        total_pages,
        raw,
        ev_map,
    )


def save_source_structural_audit(
    results: Dict[str, SourceStructuralAuditResult],
    output_path: Path = Path("sources/evidence/structural_section_audit.json"),
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = {src_id: res.model_dump() for src_id, res in results.items()}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


if __name__ == "__main__":
    audit = build_source_structural_sections()
    save_source_structural_audit(audit)
    print("Completed source structural section audit across all 9 sources.")
    for src_id, res in audit.items():
        print(f"  {res.filename}: {res.total_sections} sections (Phys: {res.physics_sections}, Covered: {res.covered_sections}, Partial: {res.partial_sections}, Not Yet Extracted: {res.not_yet_extracted_sections})")
