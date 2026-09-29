from typing import List

from jee_physics.atomization.extractor import (
    build_staged_question_atom,
    build_staged_theory_atom,
)
from jee_physics.models.atom import KnowledgeAtom
from jee_physics.models.enums import DifficultyLevel


def get_mock03_pages1_to_3_atoms(source_id: str, file_name: str) -> List[KnowledgeAtom]:
    """Returns faithfully extracted, visually grounded Knowledge Atoms for pages 1-3 of Mock Test 3.
    
    Transcribed from multimodal visual page inspection to ensure zero distortion
    of mathematics, vectors, exponents, fractions, and diagram labels.
    """
    atoms: List[KnowledgeAtom] = []

    # -------------------------------------------------------------
    # Page 1: Instructions & Questions 1, 2
    # -------------------------------------------------------------
    atoms.append(
        build_staged_theory_atom(
            chapter_id="general-physics",
            topic_id="exam-structure",
            title="JEE Main Full Mock Test Instructions",
            content=(
                "Test duration is 3 hours with a maximum score of 300 marks. The paper comprises three parts: "
                "Physics (Q1–30), Chemistry (Q31–60), and Mathematics (Q61–90). Each part contains Section A "
                "(20 multiple choice questions with +4 for correct, -1 for incorrect) and Section B "
                "(10 numerical value answer questions, where candidates attempt any 5 with +4 for correct, 0 for incorrect)."
            ),
            source_id=source_id,
            file_name=file_name,
            page_number=1,
            source_locator="Page 1, Test Instructions",
            confidence=0.99,
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="optics",
            topic_id="ray-optics",
            subtopic_id="total-internal-reflection",
            title="Prism total internal reflection in water",
            statement=(
                "A glass prism of refractive index $1.5$ is immersed in water (refractive index $\\frac{4}{3}$) "
                "as shown in figure. A light beam incident normally on the face $AB$ is totally reflected to reach "
                "the face $BC$, if"
            ),
            options=[
                {"id": "1", "text": "$\\sin\\theta \\ge \\frac{5}{9}$"},
                {"id": "2", "text": "$\\sin\\theta \\ge \\frac{2}{3}$"},
                {"id": "3", "text": "$\\sin\\theta \\ge \\frac{8}{9}$"},
                {"id": "4", "text": "$\\sin\\theta \\ge \\frac{1}{3}$"},
            ],
            answer="3",
            difficulty=DifficultyLevel.L2,
            source_id=source_id,
            file_name=file_name,
            page_number=1,
            source_locator="Section A, Q1",
            confidence=0.98,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "1"},
            concepts=["total-internal-reflection", "critical-angle", "prism-optics"],
            figure_refs=[
                {
                    "figure_id": f"{source_id}-fig-p01-q01",
                    "caption": "Right-angled prism ABC with angle theta at vertex A, immersed in water",
                    "alt_text": "Prism ABC with light beam incident perpendicularly on face AB undergoing TIR on face AC towards face BC.",
                }
            ],
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="gravitation",
            topic_id="orbital-motion",
            subtopic_id="satellite-energy",
            title="Minimum launch energy for satellite to reach altitude 2R",
            statement=(
                "What is the minimum energy required to launch a satellite of mass $m$ from the surface of a planet "
                "of mass $M$ and radius $R$ in a circular orbit at an altitude of $2R$?"
            ),
            options=[
                {"id": "1", "text": "$\\frac{5GmM}{6R}$"},
                {"id": "2", "text": "$\\frac{2GmM}{3R}$"},
                {"id": "3", "text": "$\\frac{GmM}{2R}$"},
                {"id": "4", "text": "$\\frac{3GmM}{2R}$"},
            ],
            answer="1",
            difficulty=DifficultyLevel.L2,
            source_id=source_id,
            file_name=file_name,
            page_number=1,
            source_locator="Section A, Q2",
            confidence=0.99,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "2"},
            concepts=["gravitational-potential-energy", "orbital-kinetic-energy", "total-mechanical-energy"],
        )
    )

    # -------------------------------------------------------------
    # Page 2: Questions 3, 4, 5, 6
    # -------------------------------------------------------------
    atoms.append(
        build_staged_question_atom(
            chapter_id="mechanics",
            topic_id="laws-of-motion",
            subtopic_id="friction-equilibrium",
            title="Maximum force preventing block slip with downward angle",
            statement=(
                "What is the maximum value of the force $F$ such that the block shown in the arrangement, "
                "does not move?"
            ),
            options=[
                {"id": "1", "text": "$20\\text{ N}$"},
                {"id": "2", "text": "$10\\text{ N}$"},
                {"id": "3", "text": "$12\\text{ N}$"},
                {"id": "4", "text": "$15\\text{ N}$"},
            ],
            answer="1",
            difficulty=DifficultyLevel.L2,
            source_id=source_id,
            file_name=file_name,
            page_number=2,
            source_locator="Section A, Q3",
            confidence=0.98,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "3"},
            concepts=["static-friction", "equilibrium", "normal-reaction"],
            figure_refs=[
                {
                    "figure_id": f"{source_id}-fig-p02-q03",
                    "caption": "Block of mass m = sqrt(3) kg on rough floor with mu = 1/(2*sqrt(3)) pushed by force F at 60 degrees",
                    "alt_text": "Block on horizontal floor with downward inclined pushing force F at 60 degrees to the horizontal.",
                }
            ],
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="mechanics",
            topic_id="rotational-dynamics",
            subtopic_id="angular-momentum-torque",
            title="Angular momentum and torque of freely falling particle about fixed point",
            statement=(
                "A particle falls freely near the surface of the earth. Consider a fixed point $O$ "
                "(not vertically below the particle) on the ground. Then pickup the incorrect alternative"
            ),
            options=[
                {"id": "1", "text": "The magnitude of angular momentum of the particle about $O$ is increasing"},
                {"id": "2", "text": "The magnitude of torque of the gravitational force on the particle about $O$ is decreasing"},
                {"id": "3", "text": "The moment of inertia of the particle about $O$ is decreasing"},
                {"id": "4", "text": "The magnitude of angular velocity of the particle about $O$ is increasing"},
            ],
            answer="2",
            difficulty=DifficultyLevel.L3,
            source_id=source_id,
            file_name=file_name,
            page_number=2,
            source_locator="Section A, Q4",
            confidence=0.99,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "4"},
            concepts=["angular-momentum", "torque", "free-fall"],
            insight="Gravity exerts constant force mg with constant perpendicular distance from point O; hence torque is constant, not decreasing.",
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="thermal-physics",
            topic_id="thermodynamics",
            subtopic_id="photon-gas-expansion",
            title="Adiabatic expansion of black body radiation in spherical shell",
            statement=(
                "Consider a spherical shell of radius $R$ at temperature $T$. The black body radiation inside it "
                "can be considered as an ideal gas of photons with internal energy per unit volume "
                "$u = \\frac{U}{V} \\propto T^4$ and pressure $p = \\frac{1}{3}\\left(\\frac{U}{V}\\right)$. "
                "If the shell now undergoes an adiabatic expansion the relation between $T$ and $R$ is :"
            ),
            options=[
                {"id": "1", "text": "$T \\propto \\frac{1}{R}$"},
                {"id": "2", "text": "$T \\propto \\frac{1}{R^3}$"},
                {"id": "3", "text": "$T \\propto e^{-R}$"},
                {"id": "4", "text": "$T \\propto e^{-3R}$"},
            ],
            answer="1",
            difficulty=DifficultyLevel.L4,
            source_id=source_id,
            file_name=file_name,
            page_number=2,
            source_locator="Section A, Q5",
            confidence=0.97,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "5"},
            concepts=["blackbody-radiation", "photon-gas", "first-law-thermodynamics", "adiabatic-process"],
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="mechanics",
            topic_id="momentum-collisions",
            subtopic_id="2d-inelastic-collision",
            title="Completely inelastic collision of two particles in 2D",
            statement=(
                "Two particles $A$ and $B$ of equal mass $M$ are moving with the same speed $v$ as shown in the "
                "figure. They collide completely inelastically and move as a single particle $C$. The angle $\\theta$ "
                "that the path of $C$ makes with the X-axis is given by:"
            ),
            options=[
                {"id": "1", "text": "$\\tan\\theta = \\frac{\\sqrt{3}+\\sqrt{2}}{1-\\sqrt{2}}$"},
                {"id": "2", "text": "$\\tan\\theta = \\frac{\\sqrt{3}-\\sqrt{2}}{1-\\sqrt{2}}$"},
                {"id": "3", "text": "$\\tan\\theta = \\frac{1-\\sqrt{2}}{\\sqrt{2}(1+\\sqrt{3})}$"},
                {"id": "4", "text": "$\\tan\\theta = \\frac{1-\\sqrt{3}}{1+\\sqrt{2}}$"},
            ],
            answer="2",
            difficulty=DifficultyLevel.L3,
            source_id=source_id,
            file_name=file_name,
            page_number=2,
            source_locator="Section A, Q6",
            confidence=0.98,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "6"},
            concepts=["conservation-of-momentum", "inelastic-collision", "vector-resolution"],
            figure_refs=[
                {
                    "figure_id": f"{source_id}-fig-p02-q06",
                    "caption": "Collision diagram showing particle A moving at 30 deg to -Y and particle B at 45 deg to +X",
                    "alt_text": "Particle A and particle B colliding at the origin and coalescing into particle C at angle theta to X-axis.",
                }
            ],
        )
    )

    # -------------------------------------------------------------
    # Page 3: Questions 7, 8, 9, 10, 11
    # -------------------------------------------------------------
    atoms.append(
        build_staged_question_atom(
            chapter_id="waves",
            topic_id="sound-waves",
            subtopic_id="sonometer-beats",
            title="Beat frequency produced by displaced sonometer bridge",
            statement=(
                "The fundamental frequency of a sonometer wire of length $l$ is $n_0$. A bridge is now introduced at a "
                "distance of $\\Delta l$ ($\\Delta l \\ll l$) from the centre of the wire. The lengths of wire on the "
                "two sides of the bridge are now vibrated in their fundamental modes. Then, the beat frequency nearly is –"
            ),
            options=[
                {"id": "1", "text": "$n_0 \\frac{\\Delta l}{l}$"},
                {"id": "2", "text": "$8 n_0 \\frac{\\Delta l}{l}$"},
                {"id": "3", "text": "$2 n_0 \\frac{\\Delta l}{l}$"},
                {"id": "4", "text": "$n_0 \\frac{\\Delta l}{2l}$"},
            ],
            answer="2",
            difficulty=DifficultyLevel.L3,
            source_id=source_id,
            file_name=file_name,
            page_number=3,
            source_locator="Section A, Q7",
            confidence=0.97,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "7"},
            concepts=["sonometer", "standing-waves-string", "beat-frequency"],
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="optics",
            topic_id="wave-optics",
            subtopic_id="ydse-interference",
            title="Strong intensity wavelength in YDSE with off-center hole",
            statement=(
                "In Young's double slit experiment shown in figure $S_1$ and $S_2$ are coherent sources and $S$ is the "
                "screen having a hole at a point $1.0\\text{ mm}$ away from the central line. White light ($400$ to $700\\text{ nm}$) "
                "is sent through the slits. Which wavelength passing through the hole has strong intensity?"
            ),
            options=[
                {"id": "1", "text": "$400\\text{ nm}$"},
                {"id": "2", "text": "$700\\text{ nm}$"},
                {"id": "3", "text": "$500\\text{ nm}$"},
                {"id": "4", "text": "$667\\text{ nm}$"},
            ],
            answer="4",
            difficulty=DifficultyLevel.L2,
            source_id=source_id,
            file_name=file_name,
            page_number=3,
            source_locator="Section A, Q8",
            confidence=0.98,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "8"},
            concepts=["ydse", "constructive-interference", "path-difference"],
            figure_refs=[
                {
                    "figure_id": f"{source_id}-fig-p03-q08",
                    "caption": "YDSE geometry with d = 0.5 mm, D = 50 cm, and hole at y = 1.0 mm",
                    "alt_text": "Slits S1 and S2 sending light to screen S with a small hole 1.0mm above center line.",
                }
            ],
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="electrodynamics",
            topic_id="alternating-current",
            subtopic_id="lc-circuit-oscillations",
            title="LC circuit rate of change of current and charge",
            statement=(
                "In the LC circuit, the current in the direction shown and the charges on the capacitor plates "
                "have the signs shown. At this time"
            ),
            options=[
                {"id": "1", "text": "$I$ is increasing and $Q$ is increasing"},
                {"id": "2", "text": "$I$ is increasing and $Q$ is decreasing"},
                {"id": "3", "text": "$I$ is decreasing and $Q$ is increasing"},
                {"id": "4", "text": "$I$ is decreasing and $Q$ is decreasing"},
            ],
            answer="2",
            difficulty=DifficultyLevel.L3,
            source_id=source_id,
            file_name=file_name,
            page_number=3,
            source_locator="Section A, Q9",
            confidence=0.96,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "9"},
            concepts=["lc-oscillations", "capacitors", "electromagnetic-induction"],
            figure_refs=[
                {
                    "figure_id": f"{source_id}-fig-p03-q09",
                    "caption": "LC loop showing capacitor plates with +Q on left, -Q on right, and clockwise current I",
                    "alt_text": "Schematic of LC tank circuit with capacitor charges and directional current arrow.",
                }
            ],
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="electrodynamics",
            topic_id="capacitance",
            subtopic_id="equivalent-capacitance-network",
            title="Equivalent capacitance network between terminals A and B",
            statement=(
                "Figure shows a network of capacitors where the numbers indicates capacitances in micro Farad. "
                "The value of capacitance $C$ if the equivalent capacitance between point $A$ and $B$ is to be "
                "$1\\ \\mu\\text{F}$ is:"
            ),
            options=[
                {"id": "1", "text": "$\\frac{32}{23}\\ \\mu\\text{F}$"},
                {"id": "2", "text": "$\\frac{31}{23}\\ \\mu\\text{F}$"},
                {"id": "3", "text": "$\\frac{33}{23}\\ \\mu\\text{F}$"},
                {"id": "4", "text": "$\\frac{34}{23}\\ \\mu\\text{F}$"},
            ],
            answer="1",
            difficulty=DifficultyLevel.L3,
            source_id=source_id,
            file_name=file_name,
            page_number=3,
            source_locator="Section A, Q10",
            confidence=0.97,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "10"},
            concepts=["capacitors-in-series", "capacitors-in-parallel", "bridge-reduction"],
            figure_refs=[
                {
                    "figure_id": f"{source_id}-fig-p03-q10",
                    "caption": "Network of capacitors with values C, 1, 8, 6, 4, 2, 2, 12 uF between terminals A and B",
                    "alt_text": "Complex ladder and bridge capacitor network between terminals A and B.",
                }
            ],
        )
    )

    atoms.append(
        build_staged_question_atom(
            chapter_id="mechanics",
            topic_id="kinematics",
            subtopic_id="projectile-motion",
            title="Launch angle from position vector at time t",
            statement=(
                "The position of a projectile launched from the origin at $t = 0$ is given by "
                "$\\vec{r} = (40\\hat{i} + 50\\hat{j})\\text{ m}$ at $t = 2\\text{ s}$. "
                "If the projectile was launched at an angle $\\theta$ from the horizontal, then $\\theta$ is "
                "(take $g = 10\\text{ ms}^{-2}$)"
            ),
            options=[
                {"id": "1", "text": "$\\tan^{-1}\\left(\\frac{2}{3}\\right)$"},
                {"id": "2", "text": "$\\tan^{-1}\\left(\\frac{3}{2}\\right)$"},
                {"id": "3", "text": "$\\tan^{-1}\\left(\\frac{7}{4}\\right)$"},
                {"id": "4", "text": "$\\tan^{-1}\\left(\\frac{4}{5}\\right)$"},
            ],
            answer="3",
            difficulty=DifficultyLevel.L2,
            source_id=source_id,
            file_name=file_name,
            page_number=3,
            source_locator="Section A, Q11",
            confidence=0.99,
            exam_metadata={"exam": "JEE Main Mock", "paper": 1, "question_number": "11"},
            concepts=["projectile-motion", "2d-kinematics", "equations-of-motion"],
        )
    )

    return atoms
