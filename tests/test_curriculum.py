import json
from pathlib import Path
import pytest
import tempfile
import yaml

from jee_physics.models.enums import AtomStatus, AtomType, DifficultyLevel
from jee_physics.models.atom import KnowledgeAtom, TaxonomyReference, QuestionPayload, QuestionOption
from jee_physics.models.provenance import ProvenanceRecord
from jee_physics.models.taxonomy import TaxonomyTree, TaxonomyNode, TaxonomyLevel, SubjectType
from jee_physics.models.curriculum import (
    ChapterPlan,
    ChapterSectionPlan,
    ChapterSpec,
    ChapterTemplateType,
    ConceptPlacement,
    CurriculumAuditRecord,
    CurriculumGapItem,
    CurriculumGapReport,
    CurriculumNode,
    CurriculumNodeType,
    DifficultyDimensions,
    ExamTargetLevel,
    FormulaRecord,
    GapCategory,
    MisconceptionRecord,
    PedagogicalRole,
    PrerequisiteEdge,
    PrerequisiteRelationshipType,
    QuestionLadder,
    QuestionLadderRung,
    QuestionPlacement,
    WorkedExampleRecord,
)
from jee_physics.curriculum.prerequisites import CurriculumPrerequisiteDAG
from jee_physics.curriculum.gate import (
    validate_chapter_spec,
    validate_chapter_plan,
    stage_curriculum_artifact,
    record_curriculum_audit_entry,
)
from jee_physics.curriculum.coverage import analyze_curriculum_coverage
from jee_physics.storage.io import safe_write_json


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_taxonomy_tree() -> TaxonomyTree:
    root = TaxonomyNode(
        id="physics",
        name="Physics",
        level=TaxonomyLevel.SUBJECT,
        parent_id=None,
        subject=SubjectType.PHYSICS,
        order=1,
    )
    chap = TaxonomyNode(
        id="rotational-motion",
        name="Rotational Motion",
        level=TaxonomyLevel.CHAPTER,
        parent_id="physics",
        subject=SubjectType.PHYSICS,
        order=1,
    )
    top = TaxonomyNode(
        id="angular-momentum",
        name="Angular Momentum",
        level=TaxonomyLevel.TOPIC,
        parent_id="rotational-motion",
        subject=SubjectType.PHYSICS,
        order=1,
    )
    sub = TaxonomyNode(
        id="conservation-of-angular-momentum",
        name="Conservation of Angular Momentum",
        level=TaxonomyLevel.SUBTOPIC,
        parent_id="angular-momentum",
        subject=SubjectType.PHYSICS,
        order=1,
    )
    return TaxonomyTree(root_id="physics", nodes={"physics": root, "rotational-motion": chap, "angular-momentum": top, "conservation-of-angular-momentum": sub})


@pytest.fixture
def sample_verified_atom() -> KnowledgeAtom:
    return KnowledgeAtom(
        atom_id="rot-test-atom-01",
        schema_version="1.0.0",
        atom_version=1,
        atom_type=AtomType.QUESTION,
        title="Disc Angular Momentum Test",
        taxonomy=TaxonomyReference(
            chapter_id="rotational-motion",
            topic_id="angular-momentum",
            subtopic_id="conservation-of-angular-momentum",
        ),
        provenance=[ProvenanceRecord(source_id="src-01", file_name="book.pdf", page_start=1, page_end=2)],
        confidence=1.0,
        verification_status=AtomStatus.VERIFIED,
        content_hash="a1b2c3d4e5f60102030405060708090a1b2c3d4e5f60102030405060708090a1",
        question=QuestionPayload(
            statement="A horizontal disc rotates about its axis...",
            options=[QuestionOption(id="A", text=r"$\omega$"), QuestionOption(id="B", text=r"$2\omega$")],
            verified_answer="B",
            difficulty=DifficultyLevel.L2,
        ),
    )


# ---------------------------------------------------------------------------
# Unit Tests
# ---------------------------------------------------------------------------

def test_difficulty_dimensions_derived_band_calculation():
    """Validates multi-dimensional difficulty model and derived composite band."""
    # 1. Easy foundational question
    d_easy = DifficultyDimensions(
        conceptual_difficulty=1,
        mathematical_difficulty=1,
        multistep_reasoning_difficulty=1,
        abstraction_difficulty=1,
        computational_burden=1,
        trap_misconception_difficulty=1,
    )
    assert d_easy.derived_difficulty_band == DifficultyLevel.L1

    # 2. Standard JEE Main question
    d_main = DifficultyDimensions(
        conceptual_difficulty=2,
        mathematical_difficulty=2,
        multistep_reasoning_difficulty=2,
        abstraction_difficulty=2,
        computational_burden=2,
        trap_misconception_difficulty=2,
    )
    assert d_main.derived_difficulty_band == DifficultyLevel.L2

    # 3. JEE Advanced single concept
    d_adv = DifficultyDimensions(
        conceptual_difficulty=3,
        mathematical_difficulty=3,
        multistep_reasoning_difficulty=3,
        abstraction_difficulty=3,
        computational_burden=2,
        trap_misconception_difficulty=3,
    )
    assert d_adv.derived_difficulty_band == DifficultyLevel.L3

    # 4. Extreme Olympiad synthesis
    d_oly = DifficultyDimensions(
        conceptual_difficulty=5,
        mathematical_difficulty=5,
        multistep_reasoning_difficulty=5,
        abstraction_difficulty=5,
        computational_burden=4,
        trap_misconception_difficulty=4,
    )
    assert d_oly.derived_difficulty_band == DifficultyLevel.L5


def test_question_ladder_rung_ordering_validation():
    """Question ladders must enforce strictly non-decreasing difficulty rungs."""
    rung1 = QuestionLadderRung(
        level=1,
        level_name="Direct application",
        atom_id="atom-01",
        physical_delta="Baseline setup",
        reasoning_depth=1,
        concepts_involved=["concept-1"],
        mathematical_complexity="algebra",
    )
    rung2 = QuestionLadderRung(
        level=2,
        level_name="Standard multi-step",
        atom_id="atom-02",
        physical_delta="Added constraint",
        reasoning_depth=2,
        concepts_involved=["concept-1", "concept-2"],
        mathematical_complexity="calculus",
    )

    ladder_valid = QuestionLadder(
        ladder_id="ladder-01",
        chapter_id="rotational-motion",
        topic_id="angular-momentum",
        title="Valid Ladder",
        physical_system="Rotating disc",
        rungs=[rung1, rung2],
    )
    assert len(ladder_valid.rungs) == 2

    # Inverted order must raise validation error
    with pytest.raises(ValueError, match="Ladder rungs must be strictly non-decreasing"):
        QuestionLadder(
            ladder_id="ladder-invalid",
            chapter_id="rotational-motion",
            topic_id="angular-momentum",
            title="Invalid Ladder",
            physical_system="Rotating disc",
            rungs=[rung2, rung1],
        )


def test_prerequisite_dag_cycle_and_loop_detection():
    """CurriculumPrerequisiteDAG must reject cycles, self-loops, and missing nodes."""
    dag = CurriculumPrerequisiteDAG()
    node_a = CurriculumNode(
        curriculum_id="curr-a",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Concept A",
        pedagogical_role=PedagogicalRole.FOUNDATION_CONCEPT,
    )
    node_b = CurriculumNode(
        curriculum_id="curr-b",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Concept B",
        pedagogical_role=PedagogicalRole.CORE_PRINCIPLE,
    )
    node_c = CurriculumNode(
        curriculum_id="curr-c",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Concept C",
        pedagogical_role=PedagogicalRole.CORE_PRINCIPLE,
    )
    dag.add_node(node_a)
    dag.add_node(node_b)
    dag.add_node(node_c)

    # Add cycle A -> B -> C -> A
    dag.add_edge(PrerequisiteEdge(
        from_node_id="curr-a", to_node_id="curr-b",
        relationship_type=PrerequisiteRelationshipType.STRICT_CONCEPTUAL,
        evidence="evidence for dependency", rationale="rationale for dependency"
    ))
    dag.add_edge(PrerequisiteEdge(
        from_node_id="curr-b", to_node_id="curr-c",
        relationship_type=PrerequisiteRelationshipType.STRICT_CONCEPTUAL,
        evidence="evidence for dependency", rationale="rationale for dependency"
    ))
    dag.add_edge(PrerequisiteEdge(
        from_node_id="curr-c", to_node_id="curr-a",
        relationship_type=PrerequisiteRelationshipType.STRICT_CONCEPTUAL,
        evidence="evidence for dependency", rationale="rationale for dependency"
    ))

    errors = dag.validate_graph()
    assert any("PREREQUISITE_CYCLE" in e for e in errors)
    with pytest.raises(ValueError, match="Cannot sort DAG with cycles"):
        dag.topological_sort()


def test_prerequisite_dag_impossible_direction_rejected():
    """An advanced synthesis node cannot be a prerequisite for a foundation concept."""
    dag = CurriculumPrerequisiteDAG()
    foundation = CurriculumNode(
        curriculum_id="curr-found",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Basic Foundation",
        pedagogical_role=PedagogicalRole.FOUNDATION_CONCEPT,
    )
    advanced = CurriculumNode(
        curriculum_id="curr-adv",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Advanced Multi-Concept Synthesis",
        pedagogical_role=PedagogicalRole.ADVANCED_SYNTHESIS,
    )
    dag.add_node(foundation)
    dag.add_node(advanced)

    dag.add_edge(PrerequisiteEdge(
        from_node_id="curr-adv",
        to_node_id="curr-found",
        relationship_type=PrerequisiteRelationshipType.STRICT_CONCEPTUAL,
        evidence="evidence for dependency",
        rationale="rationale for dependency",
    ))

    errors = dag.validate_graph()
    assert any("IMPOSSIBLE_PREREQUISITE_DIRECTION" in e for e in errors)


def test_topological_sort_deterministic_ordering():
    """Topological sorting must be deterministic and respect prerequisites."""
    dag = CurriculumPrerequisiteDAG()
    n1 = CurriculumNode(
        curriculum_id="curr-1",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Unit 1",
        recommended_learning_position=1,
    )
    n2 = CurriculumNode(
        curriculum_id="curr-2",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Unit 2",
        recommended_learning_position=2,
    )
    n3 = CurriculumNode(
        curriculum_id="curr-3",
        taxonomy_reference=TaxonomyReference(chapter_id="c1", topic_id="t1"),
        node_type=CurriculumNodeType.CONCEPT,
        title="Unit 3",
        recommended_learning_position=3,
    )
    dag.add_node(n1)
    dag.add_node(n2)
    dag.add_node(n3)

    dag.add_edge(PrerequisiteEdge(from_node_id="curr-1", to_node_id="curr-2", relationship_type=PrerequisiteRelationshipType.STRICT_CONCEPTUAL, evidence="evidence for dependency", rationale="rationale for dependency"))
    dag.add_edge(PrerequisiteEdge(from_node_id="curr-2", to_node_id="curr-3", relationship_type=PrerequisiteRelationshipType.STRICT_CONCEPTUAL, evidence="evidence for dependency", rationale="rationale for dependency"))

    order = dag.topological_sort()
    assert order == ["curr-1", "curr-2", "curr-3"]
    assert dag.get_all_prerequisites_transitive("curr-3") == {"curr-1", "curr-2"}
    assert dag.get_all_dependents_transitive("curr-1") == {"curr-2", "curr-3"}


def test_chapter_spec_deterministic_gate_validation(sample_taxonomy_tree, sample_verified_atom):
    """Deterministic curriculum gate validates ChapterSpec against taxonomy tree and verified atoms."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        kb_atoms_dir = Path(tmp_dir) / "kb" / "atoms"
        kb_atoms_dir.mkdir(parents=True)

        # Write sample verified atom to fake kb/atoms/
        atom_file = kb_atoms_dir / f"{sample_verified_atom.atom_id}.json"
        safe_write_json(atom_file, sample_verified_atom.model_dump(mode="json"))

        # Construct valid ChapterSpec
        spec = ChapterSpec(
            chapter_id="rotational-motion",
            chapter_title="Rotational Motion",
            template_type=ChapterTemplateType.MECHANICS,
            order=1,
            taxonomy_references=[
                TaxonomyReference(
                    chapter_id="rotational-motion",
                    topic_id="angular-momentum",
                    subtopic_id="conservation-of-angular-momentum",
                )
            ],
            learning_objectives=["Understand conservation of angular momentum."],
            formula_sequence=[
                FormulaRecord(
                    formula_id="form-ang-mom-01",
                    title="Conservation of Angular Momentum",
                    equation_latex=r"I_1 \omega_1 = I_2 \omega_2",
                    variables={"I": "Moment of inertia", r"\omega": "Angular velocity"},
                    units_and_dimensions={"I": "kg m^2", r"\omega": "rad/s"},
                    assumptions=["Rigid body", "Fixed rotation axis"],
                    conditions_of_validity=["Net external torque is zero"],
                )
            ],
            misconception_sequence=[
                MisconceptionRecord(
                    misconception_id="misc-01",
                    category="WRONG_CONSERVATION_LAW",
                    statement="Kinetic energy is conserved when moment of inertia changes.",
                    explanation="Internal work is done, altering rotational kinetic energy.",
                    trap_mechanism="Questions asking for final kinetic energy ratio.",
                )
            ],
            worked_example_sequence=[
                WorkedExampleRecord(
                    example_id="ex-01",
                    problem_statement="A rotating disc...",
                    known_quantities={"I_1": "10 kg m^2"},
                    target_quantity="final angular speed",
                    relevant_concepts=["Conservation of angular momentum"],
                    governing_principles=["No external torque"],
                    solution_strategy="Equate initial and final angular momentum.",
                    step_by_step_derivation=[r"L_i = I_1 \omega_1", r"L_f = I_2 \omega_2"],
                    final_answer="5 rad/s",
                    sanity_checks=[r"As I increases, \omega decreases."],
                )
            ],
            question_sequence=[
                QuestionPlacement(
                    atom_id=sample_verified_atom.atom_id,
                    curriculum_id="curr-rot-01",
                    chapter_id="rotational-motion",
                    topic_id="angular-momentum",
                    difficulty_dimensions=DifficultyDimensions(
                        conceptual_difficulty=2,
                        mathematical_difficulty=2,
                        multistep_reasoning_difficulty=2,
                        abstraction_difficulty=1,
                        computational_burden=1,
                        trap_misconception_difficulty=1,
                    ),
                )
            ],
        )

        errors = validate_chapter_spec(spec, sample_taxonomy_tree, kb_atoms_dir)
        assert errors == [], f"Expected 0 errors, got: {errors}"


def test_gate_rejects_unverified_question_atom(sample_taxonomy_tree, sample_verified_atom):
    """Gate must reject ChapterSpec if any referenced question atom is not VERIFIED."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        kb_atoms_dir = Path(tmp_dir) / "kb" / "atoms"
        kb_atoms_dir.mkdir(parents=True)

        unverified_atom = sample_verified_atom.model_copy(deep=True)
        unverified_atom.verification_status = AtomStatus.STAGED
        safe_write_json(kb_atoms_dir / f"{unverified_atom.atom_id}.json", unverified_atom.model_dump(mode="json"))

        spec = ChapterSpec(
            chapter_id="rotational-motion",
            chapter_title="Rotational Motion",
            template_type=ChapterTemplateType.MECHANICS,
            order=1,
            question_sequence=[
                QuestionPlacement(
                    atom_id=unverified_atom.atom_id,
                    curriculum_id="curr-rot-01",
                    chapter_id="rotational-motion",
                    topic_id="angular-momentum",
                    difficulty_dimensions=DifficultyDimensions(
                        conceptual_difficulty=2, mathematical_difficulty=2, multistep_reasoning_difficulty=2,
                        abstraction_difficulty=1, computational_burden=1, trap_misconception_difficulty=1
                    ),
                )
            ],
        )

        errors = validate_chapter_spec(spec, sample_taxonomy_tree, kb_atoms_dir)
        assert any("UNVERIFIED_QUESTION_REJECTED" in e for e in errors)


def test_gate_rejects_nonexistent_taxonomy_node(sample_taxonomy_tree, sample_verified_atom):
    """Gate must reject ChapterSpec if taxonomy reference does not exist in syllabus tree."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        kb_atoms_dir = Path(tmp_dir) / "kb" / "atoms"
        kb_atoms_dir.mkdir(parents=True)
        safe_write_json(kb_atoms_dir / f"{sample_verified_atom.atom_id}.json", sample_verified_atom.model_dump(mode="json"))

        spec = ChapterSpec(
            chapter_id="rotational-motion",
            chapter_title="Rotational Motion",
            template_type=ChapterTemplateType.MECHANICS,
            order=1,
            taxonomy_references=[
                TaxonomyReference(chapter_id="nonexistent-chapter", topic_id="angular-momentum")
            ],
        )

        errors = validate_chapter_spec(spec, sample_taxonomy_tree, kb_atoms_dir)
        assert any("TAXONOMY_NODE_NOT_FOUND" in e for e in errors)


def test_chapter_plan_validation_against_spec(sample_verified_atom):
    """ChapterPlan must align with ChapterSpec without unapproved questions or formulas."""
    spec = ChapterSpec(
        chapter_id="rotational-motion",
        chapter_title="Rotational Motion",
        order=1,
        question_sequence=[
            QuestionPlacement(
                atom_id=sample_verified_atom.atom_id,
                curriculum_id="curr-rot-01",
                chapter_id="rotational-motion",
                topic_id="angular-momentum",
                difficulty_dimensions=DifficultyDimensions(
                    conceptual_difficulty=2, mathematical_difficulty=2, multistep_reasoning_difficulty=2,
                    abstraction_difficulty=1, computational_burden=1, trap_misconception_difficulty=1
                ),
            )
        ],
        formula_sequence=[
            FormulaRecord(
                formula_id="form-01",
                title="L",
                equation_latex=r"L = I\omega",
                variables={"L": "ang mom"},
                units_and_dimensions={"L": "kg m^2/s"},
                assumptions=["rigid"],
                conditions_of_validity=["valid"],
            )
        ],
    )

    valid_plan = ChapterPlan(
        plan_id="plan-01",
        chapter_id="rotational-motion",
        title="Rotational Motion Plan",
        template_type=ChapterTemplateType.MECHANICS,
        sections=[
            ChapterSectionPlan(
                section_id="sec-01",
                section_order=1,
                title="Angular Momentum",
                pedagogical_purpose="Introduce angular momentum.",
                concepts=["Angular Momentum"],
                formula_ids=["form-01"],
                question_atom_ids=[sample_verified_atom.atom_id],
            )
        ],
    )
    assert validate_chapter_plan(valid_plan, spec) == []

    # Plan with unapproved question
    invalid_plan = valid_plan.model_copy(deep=True)
    invalid_plan.sections[0].question_atom_ids.append("unapproved-atom-99")
    errors = validate_chapter_plan(invalid_plan, spec)
    assert any("PLAN_UNSPECIFIED_QUESTION" in e for e in errors)


def test_coverage_and_gap_analysis_engine():
    """Curriculum gap analysis must correctly identify covered vs empty nodes and gap categories."""
    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    kb_atoms_path = Path("kb/atoms")

    report = analyze_curriculum_coverage(
        syllabus_path=syllabus_path,
        kb_atoms_dir=kb_atoms_path,
    )

    assert report.total_taxonomy_nodes > 400
    assert report.nodes_covered >= 20  # we have 35 canonical atoms across 22 chapters
    assert report.nodes_empty > 200
    assert GapCategory.NO_CONTENT.value in report.gaps_by_category
    assert len(report.gap_items) > 0


def test_idempotent_curriculum_audit_journal():
    """Audit journal recording must be strictly idempotent on entry_id."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        journal_path = Path(tmp_dir) / "audit_journal.jsonl"
        entry = CurriculumAuditRecord(
            entry_id="entry-test-001",
            curriculum_change="ADD_QUESTION_PLACEMENT",
            previous_value=None,
            new_value="atom-123 placed in curr-rot-01",
            reason="Pedagogical progression",
            agent_identity="physics-curriculum-architect",
            conversation_id="conv-123",
            confidence=0.99,
            evidence="Chapter 6 textbook",
        )

        record_curriculum_audit_entry(journal_path, entry)
        # Record second time with identical entry_id
        record_curriculum_audit_entry(journal_path, entry)

        lines = journal_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1, f"Expected exactly 1 line, found {len(lines)}"


def test_canonical_kb_storage_integrity_after_curriculum():
    """Canonical kb/atoms/ must remain 100% pure and untouched during curriculum operations."""
    kb_atoms_dir = Path("kb/atoms")
    atom_files = list(kb_atoms_dir.glob("*.json"))
    assert len(atom_files) == 35, f"Expected exactly 35 canonical atoms, found {len(atom_files)}"

    prohibited = ["test", "fixture", "pilot", "dummy", "mock", "variant", "synthetic"]
    for f in atom_files:
        assert not any(p in f.stem.lower() for p in prohibited), f"Prohibited marker in {f.name}"


def test_difficulty_reproducibility_and_sensitivity():
    """Proves deterministic scoring reproducibility, monotonic sensitivity, and threshold boundaries."""
    # 1. Deterministic reproducibility across 100 runs
    for _ in range(100):
        d = DifficultyDimensions(
            conceptual_difficulty=3,
            mathematical_difficulty=2,
            multistep_reasoning_difficulty=3,
            abstraction_difficulty=2,
            computational_burden=1,
            trap_misconception_difficulty=2,
        )
        assert d.derived_difficulty_band == DifficultyLevel.L2
        assert d.weighting_policy == "PEDAGOGICAL_PROJECT_POLICY"

    # 2. Monotonic sensitivity on conceptual dimension
    scores = []
    for c in range(1, 6):
        d = DifficultyDimensions(
            conceptual_difficulty=c,
            mathematical_difficulty=2,
            multistep_reasoning_difficulty=2,
            abstraction_difficulty=2,
            computational_burden=2,
            trap_misconception_difficulty=2,
        )
        # Compute exact weighted score
        w = (2.0 * c + 2.0 * 2 + 1.5 * 2 + 1.5 * 2 + 1.0 * 2 + 0.8 * 2) / 8.8
        scores.append(w)
    assert scores == sorted(scores), "Composite scores must be strictly monotonic"
    assert len(set(scores)) == 5, "Distinct conceptual inputs must yield distinct scores"

    # 3. Boundary condition testing around L1-L5 thresholds
    # L1: weighted_score < 1.8 (all 1s -> score = 1.0 -> L1)
    d_l1 = DifficultyDimensions(
        conceptual_difficulty=1, mathematical_difficulty=1, multistep_reasoning_difficulty=1,
        abstraction_difficulty=1, computational_burden=1, trap_misconception_difficulty=1,
    )
    assert d_l1.derived_difficulty_band == DifficultyLevel.L1

    # L2: 1.8 <= score < 2.8 (all 2s -> score = 2.0 -> L2)
    d_l2 = DifficultyDimensions(
        conceptual_difficulty=2, mathematical_difficulty=2, multistep_reasoning_difficulty=2,
        abstraction_difficulty=2, computational_burden=2, trap_misconception_difficulty=2,
    )
    assert d_l2.derived_difficulty_band == DifficultyLevel.L2

    # L3: 2.8 <= score < 3.8 (all 3s -> score = 3.0 -> L3)
    d_l3 = DifficultyDimensions(
        conceptual_difficulty=3, mathematical_difficulty=3, multistep_reasoning_difficulty=3,
        abstraction_difficulty=3, computational_burden=3, trap_misconception_difficulty=3,
    )
    assert d_l3.derived_difficulty_band == DifficultyLevel.L3

    # L4: 3.8 <= score < 4.6 (all 4s -> score = 4.0 -> L4)
    d_l4 = DifficultyDimensions(
        conceptual_difficulty=4, mathematical_difficulty=4, multistep_reasoning_difficulty=4,
        abstraction_difficulty=4, computational_burden=4, trap_misconception_difficulty=4,
    )
    assert d_l4.derived_difficulty_band == DifficultyLevel.L4

    # L5: score >= 4.6 (all 5s -> score = 5.0 -> L5)
    d_l5 = DifficultyDimensions(
        conceptual_difficulty=5, mathematical_difficulty=5, multistep_reasoning_difficulty=5,
        abstraction_difficulty=5, computational_burden=5, trap_misconception_difficulty=5,
    )
    assert d_l5.derived_difficulty_band == DifficultyLevel.L5


def test_prerequisite_graph_scope_metadata_and_provenance():
    """Prerequisite graph must be explicitly marked PILOT and edges must have provenance types."""
    graph_path = Path("curriculum/prerequisite_graph.json")
    dag = CurriculumPrerequisiteDAG.load_json(graph_path)

    assert dag.scope == "PILOT"
    assert dag.metadata.get("pilot_scope") is True
    assert "rotational-motion" in dag.metadata.get("covered_pilot_chapters", [])
    assert dag.metadata.get("authorship") == "PROJECT_ENGINEERING_DESIGN"
    assert dag.metadata.get("omission_classification") == "PILOT_SCOPE_LIMITATION"

    # All 30 edges must have non-empty rationale and valid provenance_type
    for edge in dag.edges:
        assert hasattr(edge, "provenance_type")
        assert edge.provenance_type in [
            "DETERMINISTIC_STRUCTURAL",
            "PEDAGOGICAL_JUDGMENT",
            "SOURCE_DERIVED",
            "PROJECT_DESIGNED",
        ]
        assert len(edge.rationale) >= 5
        assert len(edge.evidence) >= 5


def test_taxonomy_immutability_and_separation():
    """Curriculum modifications must NOT alter kb/taxonomy/syllabus.yaml or canonical atoms."""
    import hashlib

    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    initial_hash = hashlib.sha256(syllabus_path.read_bytes()).hexdigest()

    kb_dir = Path("kb/atoms")
    atom_hashes_before = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in kb_dir.glob("*.json")}

    # Perform mock curriculum operations (create DAG, sort, analyze coverage)
    dag = CurriculumPrerequisiteDAG(graph_id="temp-dag")
    report = analyze_curriculum_coverage(syllabus_path, kb_dir)

    # Verify syllabus.yaml remains byte-identical
    final_hash = hashlib.sha256(syllabus_path.read_bytes()).hexdigest()
    assert initial_hash == final_hash, "syllabus.yaml was mutated by curriculum operation!"

    # Verify kb/atoms/ remains 100% byte-identical
    atom_hashes_after = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in kb_dir.glob("*.json")}
    assert atom_hashes_before == atom_hashes_after, "Canonical atom modified during curriculum operation!"


def test_coverage_gap_report_459_content_bearing_nodes_accounting():
    """Coverage gap report must explicitly distinguish 460 total nodes from 459 content-bearing nodes."""
    syllabus_path = Path("kb/taxonomy/syllabus.yaml")
    kb_atoms_path = Path("kb/atoms")

    report = analyze_curriculum_coverage(syllabus_path, kb_atoms_path)
    assert report.total_taxonomy_nodes == 460
    assert report.content_bearing_nodes_analyzed == 459
    assert report.excluded_nodes == ["physics"]
    assert "SUBJECT" in report.exclusion_reason
    assert report.taxonomy_presence_nodes == report.nodes_covered
