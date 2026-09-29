from jee_physics.core.ids import generate_atom_id, generate_source_id, slugify
from jee_physics.models.enums import AtomType


def test_slugify():
    assert slugify("Laws of Motion & Friction!") == "laws-of-motion-friction"
    assert slugify("Kinematics  1D - Motion") == "kinematics-1d-motion"


def test_stable_atom_id_generation():
    # Minor whitespace differences should normalize to the exact same stable ID
    text1 = "A particle moves with   constant acceleration  a."
    text2 = "A particle moves with constant acceleration a.\n"

    id1 = generate_atom_id("kinematics", AtomType.THEORY, text1)
    id2 = generate_atom_id("kinematics", AtomType.THEORY, text2)

    assert id1 == id2
    assert id1.startswith("kinematics-theory-")


def test_distinct_content_produces_distinct_ids():
    text1 = "A projectile is launched at angle 30 degrees."
    text2 = "A projectile is launched at angle 60 degrees."

    id1 = generate_atom_id("kinematics", AtomType.QUESTION, text1)
    id2 = generate_atom_id("kinematics", AtomType.QUESTION, text2)

    assert id1 != id2


def test_deterministic_source_id():
    fname = "H.C. Verma Vol 1.pdf"
    fhash = "abcdef1234567890" * 4

    src_id1 = generate_source_id(fname, fhash)
    src_id2 = generate_source_id(fname, fhash)

    assert src_id1 == src_id2
    assert src_id1.startswith("src-hc-verma-vol-1-")
