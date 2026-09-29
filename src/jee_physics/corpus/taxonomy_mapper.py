from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import yaml

from jee_physics.models.corpus import CoverageStatus, EnhancedSourceSegment, TaxonomyCoverageRecord
from jee_physics.models.taxonomy import TaxonomyTree


# Mapping table from source segments/chapters to canonical syllabus chapter IDs
SEGMENT_TO_CHAPTER_MAP: Dict[str, Dict[str, str]] = {
    # HCV Vol 1
    "src-concepts-of-physics-by-h-a489bb6e": {
        "Chapter 1: Introduction to Physics": "units-and-measurements",
        "Chapter 2: Physics and Mathematics": "units-and-measurements",
        "Chapter 3: Rest and Motion: Kinematics": "kinematics",
        "Chapter 4: The Forces": "laws-of-motion",
        "Chapter 5: Newton's Laws of Motion": "laws-of-motion",
        "Chapter 6: Friction": "laws-of-motion",
        "Chapter 7: Circular Motion": "kinematics",
        "Chapter 8: Work and Energy": "work-energy-power",
        "Chapter 9: Centre of Mass, Linear Momentum, Collision": "center-of-mass",
        "Chapter 10: Rotational Mechanics": "rotational-motion",
        "Chapter 11: Gravitation": "gravitation",
        "Chapter 12: Simple Harmonic Motion": "oscillations",
        "Chapter 13: Fluid Mechanics": "fluid-mechanics",
        "Chapter 14: Some Mechanical Properties of Matter": "properties-of-solids",
        "Chapter 15: Wave Motion and Waves on a String": "waves",
        "Chapter 16: Sound Waves": "waves",
        "Chapter 17: Light Waves": "wave-optics",
        "Chapter 18: Geometrical Optics": "ray-optics",
        "Chapter 19: Optical Instruments": "ray-optics",
        "Chapter 20: Dispersion and Spectra": "ray-optics",
        "Chapter 21: Speed of Light": "electromagnetic-waves",
        "Chapter 22: Photometry": "ray-optics",
    },
    # HCV Vol 2
    "src-concepts-of-physics-by-h-1fd380f4": {
        "Chapter 23: Heat and Temperature": "thermal-physics",
        "Chapter 24: Kinetic Theory of Gases": "kinetic-theory-of-gases",
        "Chapter 25: Calorimetry": "thermal-physics",
        "Chapter 26: Laws of Thermodynamics": "thermodynamics",
        "Chapter 27: Specific Heat Capacities of Gases": "thermodynamics",
        "Chapter 28: Heat Transfer": "thermal-physics",
        "Chapter 29: Electric Field and Potential": "electrostatics",
        "Chapter 30: Gauss's Law": "electrostatics",
        "Chapter 31: Capacitors": "capacitance",
        "Chapter 32: Electric Current in Conductors": "current-electricity",
        "Chapter 33: Thermal and Chemical Effects of Electric Current": "current-electricity",
        "Chapter 34: Magnetic Field": "magnetic-effects-of-current",
        "Chapter 35: Magnetic Field due to a Current": "magnetic-effects-of-current",
        "Chapter 36: Permanent Magnets": "magnetism-and-matter",
        "Chapter 37: Magnetic Properties of Matter": "magnetism-and-matter",
        "Chapter 38: Electromagnetic Induction": "electromagnetic-induction",
        "Chapter 39: Alternating Current": "alternating-current",
        "Chapter 40: Electromagnetic Waves": "electromagnetic-waves",
        "Chapter 41: Electric Current through Gases": "dual-nature-of-matter-and-radiation",
        "Chapter 42: Photoelectric Effect and Wave-Particle Duality": "dual-nature-of-matter-and-radiation",
        "Chapter 43: Bohr's Model and Physics of the Atom": "atomic-physics",
        "Chapter 44: X-rays": "atomic-physics",
        "Chapter 45: Semiconductors and Semiconductor Devices": "semiconductors",
        "Chapter 46: The Nucleus": "nuclear-physics",
        "Chapter 47: Special Theory of Relativity": "laws-of-motion",
    },
    # Irodov Problems
    "src-problems-in-general-phys-6cf0b2b7": {
        "1.1 Kinematics": "kinematics",
        "1.2 The Fundamental Equation of Dynamics": "laws-of-motion",
        "1.3 Conservation Laws (Energy, Momentum, Angular Momentum)": "work-energy-power",
        "1.4 Universal Gravitation": "gravitation",
        "1.5 Dynamics of a Solid Body": "rotational-motion",
        "1.6 Elastic Deformations of a Solid Body": "properties-of-solids",
        "1.7 Hydrodynamics": "fluid-mechanics",
        "1.8 Relativistic Mechanics": "laws-of-motion",
        "2.1 Equation of the Gas State. Processes": "kinetic-theory-of-gases",
        "2.2 The First Law of Thermodynamics. Heat Capacity": "thermodynamics",
        "2.3 Kinetic Theory of Gases. Boltzmann's Law and Maxwell's Distribution": "kinetic-theory-of-gases",
        "2.4 The Second Law of Thermodynamics. Entropy": "thermodynamics",
        "2.5 Liquids. Capillary Effects": "fluid-mechanics",
        "2.6 Phase Transformations": "thermal-physics",
        "2.7 Transport Phenomena": "thermal-physics",
        "3.1 Constant Electric Field in Vacuum": "electrostatics",
        "3.2 Conductors and Dielectrics in an Electric Field": "electrostatics",
        "3.3 Electric Capacitance. Energy of an Electric Field": "capacitance",
        "3.4 Electric Current": "current-electricity",
        "3.5 Constant Magnetic Field. Magnetics": "magnetic-effects-of-current",
        "3.6 Electromagnetic Induction. Maxwell's Equations": "electromagnetic-induction",
        "3.7 Motion of Charged Particles in Electric and Magnetic Fields": "magnetic-effects-of-current",
        "4.1 Mechanical Oscillations": "oscillations",
        "4.2 Electric Oscillations": "alternating-current",
        "4.3 Elastic Waves. Acoustics": "waves",
        "4.4 Electromagnetic Waves. Radiation": "electromagnetic-waves",
        "5.1 Photometry and Geometrical Optics": "ray-optics",
        "5.2 Interference of Light": "wave-optics",
        "5.3 Diffraction of Light": "wave-optics",
        "5.4 Polarization of Light": "wave-optics",
        "5.5 Dispersion and Absorption of Light": "ray-optics",
        "5.6 Optics of Moving Sources": "wave-optics",
        "5.7 Thermal Radiation. Quantum Nature of Light": "dual-nature-of-matter-and-radiation",
        "6.1 Scattering of Particles. Rutherford-Bohr Atom": "atomic-physics",
        "6.2 Wave Properties of Particles. Schrodinger Equation": "dual-nature-of-matter-and-radiation",
        "6.3 Properties of Atoms. Spectra": "atomic-physics",
        "6.4 Molecules and Crystals": "properties-of-solids",
        "6.5 Radioactivity": "nuclear-physics",
        "6.6 Nuclear Reactions": "nuclear-physics",
        "6.7 Elementary Particles": "nuclear-physics",
    },
    # Mock tests
    "src-jee-main-mock-test-01-20-222525c1": {
        "Physics Section A & B (Q1-30)": "experimental-physics",
    },
    "src-jee-rank-booster-02-mock-0548b6c5": {
        "Physics Section A & B (Q1-30)": "experimental-physics",
    },
    "src-jee-rank-booster-03-mock-256f42c6": {
        "Physics Section A & B (Q1-30)": "ray-optics",
    },
}


def map_segment_to_taxonomy(
    segment: EnhancedSourceSegment,
    taxonomy_tree: TaxonomyTree,
) -> Optional[str]:
    """Resolves the canonical chapter node ID for a source segment."""
    if segment.subject_type != "PHYSICS":
        return None

    sid = segment.source_id
    title = segment.segment_title

    # 1. Lookup in explicit dictionary
    if sid in SEGMENT_TO_CHAPTER_MAP and title in SEGMENT_TO_CHAPTER_MAP[sid]:
        return SEGMENT_TO_CHAPTER_MAP[sid][title]

    # 2. Textual heuristics for Halliday, University Physics, and Feynman
    title_lower = title.lower()
    
    if any(k in title_lower for k in ["measurement", "unit", "vectors"]):
        return "units-and-measurements"
    if any(k in title_lower for k in ["straight line", "two and three", "projectile", "motion along"]):
        return "kinematics"
    if any(k in title_lower for k in ["force and motion", "newton", "friction", "laws of dynamics"]):
        return "laws-of-motion"
    if any(k in title_lower for k in ["kinetic energy and work", "potential energy", "conservation of energy"]):
        return "work-energy-power"
    if any(k in title_lower for k in ["center of mass", "linear momentum", "impulse"]):
        return "center-of-mass"
    if any(k in title_lower for k in ["rotation", "rolling", "torque", "angular momentum", "rigid bodies"]):
        return "rotational-motion"
    if any(k in title_lower for k in ["gravitation"]):
        return "gravitation"
    if any(k in title_lower for k in ["elasticity", "solids", "equilibrium and elasticity"]):
        return "properties-of-solids"
    if any(k in title_lower for k in ["fluid"]):
        return "fluid-mechanics"
    if any(k in title_lower for k in ["temperature and heat", "thermal properties", "heat transfer"]):
        return "thermal-physics"
    if any(k in title_lower for k in ["laws of thermodynamics", "entropy"]):
        return "thermodynamics"
    if any(k in title_lower for k in ["kinetic theory"]):
        return "kinetic-theory-of-gases"
    if any(k in title_lower for k in ["oscillation", "periodic motion", "harmonic oscillator"]):
        return "oscillations"
    if any(k in title_lower for k in ["mechanical waves", "sound"]):
        return "waves"
    if any(k in title_lower for k in ["coulomb", "electric field", "electric potential", "gauss"]):
        return "electrostatics"
    if any(k in title_lower for k in ["capacitance"]):
        return "capacitance"
    if any(k in title_lower for k in ["current and resistance", "circuits", "direct-current"]):
        return "current-electricity"
    if any(k in title_lower for k in ["magnetic field", "sources of magnetic"]):
        return "magnetic-effects-of-current"
    if any(k in title_lower for k in ["magnetism of matter", "magnetic properties"]):
        return "magnetism-and-matter"
    if any(k in title_lower for k in ["induction", "inductance"]):
        return "electromagnetic-induction"
    if any(k in title_lower for k in ["alternating current", "ac"]):
        return "alternating-current"
    if any(k in title_lower for k in ["electromagnetic waves", "maxwell"]):
        return "electromagnetic-waves"
    if any(k in title_lower for k in ["geometric optics", "images", "light waves behaving"]):
        return "ray-optics"
    if any(k in title_lower for k in ["interference", "diffraction"]):
        return "wave-optics"
    if any(k in title_lower for k in ["photons", "matter waves", "particles behaving", "photoelectric"]):
        return "dual-nature-of-matter-and-radiation"
    if any(k in title_lower for k in ["atoms", "atomic", "bohr"]):
        return "atomic-physics"
    if any(k in title_lower for k in ["nuclear", "nucleus"]):
        return "nuclear-physics"
    if any(k in title_lower for k in ["semiconductor", "conduction of electricity in solids"]):
        return "semiconductors"

    return "kinematics"  # default fallback within mechanics
