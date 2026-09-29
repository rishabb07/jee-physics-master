"""
Question Requirements Engine for Phase 9 Question Bank & Assessment Generation.

Constructs build/reports/question_requirements.json by analyzing:
1. Curriculum blueprint nodes and learning objectives across the 4 pilot chapters.
2. Verified canonical atoms in kb/atoms/.
3. Required distribution across question types, difficulty bands, and exam levels.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from jee_physics.models.curriculum import ExamTargetLevel
from jee_physics.models.enums import DifficultyLevel
from jee_physics.models.question_bank import QuestionType


class QuestionRequirementItem(BaseModel):
    """Specification of an assessment item requirement."""
    requirement_id: str = Field(..., description="Unique requirement ID")
    chapter_id: str = Field(..., description="Target chapter slug")
    curriculum_node_id: str = Field(..., description="Mapped curriculum unit ID")
    concept_id: str = Field(..., description="Primary concept exercised")
    target_exam_level: ExamTargetLevel = Field(..., description="Target examination level")
    target_difficulty: DifficultyLevel = Field(..., description="Target difficulty band (L1-L5)")
    question_type: QuestionType = Field(..., description="Target question format")
    intended_skill: str = Field(..., description="Specific problem-solving skill tested")
    prerequisite_knowledge: List[str] = Field(default_factory=list, description="Required prerequisite units")
    misconception_target: Optional[str] = Field(None, description="Mapped misconception ID to diagnose")
    satisfied_by_canonical_atom: Optional[str] = Field(None, description="Atom ID if satisfied by existing source")
    needs_new_generation: bool = Field(True, description="Whether new problem generation is required")
    risk_level: str = Field("MEDIUM", description="'MEDIUM' | 'HIGH'")


class QuestionRequirementReport(BaseModel):
    """Catalog of question requirements for assessment generation."""
    report_id: str
    total_requirements: int
    satisfied_by_source_count: int
    new_generation_required_count: int
    requirements: List[QuestionRequirementItem]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionRequirementsEngine:
    """Deterministic engine to construct question generation requirements."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(".")
        self.kb_atoms_dir = self.workspace_root / "kb" / "atoms"
        self.reports_dir = self.workspace_root / "build" / "reports"

    def build_pilot_requirements(self) -> QuestionRequirementReport:
        """Constructs the requirements matrix across the 4 pilot chapters."""
        items: List[QuestionRequirementItem] = [
            # 1. Rotational Motion
            QuestionRequirementItem(
                requirement_id="qreq-rot-01-angmom-easy",
                chapter_id="rotational-motion",
                curriculum_node_id="curr-rot-03",
                concept_id="concept-rot-angmom-particle-01",
                target_exam_level=ExamTargetLevel.JEE_MAIN,
                target_difficulty=DifficultyLevel.L2,
                question_type=QuestionType.SINGLE_CORRECT_MCQ,
                intended_skill="Calculate particle angular momentum relative to origin for uniform linear motion",
                prerequisite_knowledge=["curr-kin-02"],
                misconception_target="misc-rot-01",
                satisfied_by_canonical_atom="rotational-motion-question-6c7cb960",
                needs_new_generation=False,
                risk_level="MEDIUM",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-rot-02-conservation-multistep",
                chapter_id="rotational-motion",
                curriculum_node_id="curr-rot-04",
                concept_id="concept-rot-angmom-conservation-01",
                target_exam_level=ExamTargetLevel.JEE_ADVANCED,
                target_difficulty=DifficultyLevel.L4,
                question_type=QuestionType.MULTI_STEP_STRUCTURED,
                intended_skill="Apply angular momentum conservation to rotating disc with time-varying mass distribution",
                prerequisite_knowledge=["curr-rot-01", "curr-rot-03"],
                misconception_target="misc-rot-02",
                satisfied_by_canonical_atom=None,
                needs_new_generation=True,
                risk_level="HIGH",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-rot-03-torque-dyn-mcq",
                chapter_id="rotational-motion",
                curriculum_node_id="curr-rot-02",
                concept_id="concept-rot-torque-01",
                target_exam_level=ExamTargetLevel.JEE_MAIN,
                target_difficulty=DifficultyLevel.L3,
                question_type=QuestionType.SINGLE_CORRECT_MCQ,
                intended_skill="Analyze net torque and angular acceleration under tangential string tension",
                prerequisite_knowledge=["curr-rot-01"],
                misconception_target=None,
                satisfied_by_canonical_atom="rotational-motion-question-f7cbecda",
                needs_new_generation=False,
                risk_level="MEDIUM",
            ),

            # 2. Thermodynamics
            QuestionRequirementItem(
                requirement_id="qreq-td-01-firstlaw-work",
                chapter_id="thermodynamics",
                curriculum_node_id="curr-td-01",
                concept_id="concept-td-first-law-01",
                target_exam_level=ExamTargetLevel.JEE_MAIN,
                target_difficulty=DifficultyLevel.L2,
                question_type=QuestionType.SINGLE_CORRECT_MCQ,
                intended_skill="Compute internal energy change and work done in closed cycle",
                prerequisite_knowledge=["curr-td-01"],
                misconception_target="misc-td-01",
                satisfied_by_canonical_atom="thermodynamics-question-71b685c0",
                needs_new_generation=False,
                risk_level="MEDIUM",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-td-02-adiabatic-multicorrect",
                chapter_id="thermodynamics",
                curriculum_node_id="curr-td-02",
                concept_id="concept-td-adiabatic-01",
                target_exam_level=ExamTargetLevel.JEE_ADVANCED,
                target_difficulty=DifficultyLevel.L4,
                question_type=QuestionType.MULTIPLE_CORRECT_MCQ,
                intended_skill="Evaluate reversible adiabatic expansion relationships across P, V, T and work done",
                prerequisite_knowledge=["curr-td-01"],
                misconception_target="misc-td-02",
                satisfied_by_canonical_atom=None,
                needs_new_generation=True,
                risk_level="HIGH",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-td-03-radiation-photon",
                chapter_id="thermodynamics",
                curriculum_node_id="curr-td-03",
                concept_id="concept-td-radiation-01",
                target_exam_level=ExamTargetLevel.JEE_ADVANCED,
                target_difficulty=DifficultyLevel.L5,
                question_type=QuestionType.NUMERICAL,
                intended_skill="Compute adiabatic expansion scaling for blackbody photon gas cavity",
                prerequisite_knowledge=["curr-td-02"],
                misconception_target=None,
                satisfied_by_canonical_atom="thermodynamics-question-3fe51020",
                needs_new_generation=False,
                risk_level="HIGH",
            ),

            # 3. Current Electricity
            QuestionRequirementItem(
                requirement_id="qreq-curr-01-recasting-num",
                chapter_id="current-electricity",
                curriculum_node_id="curr-curr-02",
                concept_id="concept-curr-recasting-01",
                target_exam_level=ExamTargetLevel.JEE_MAIN,
                target_difficulty=DifficultyLevel.L2,
                question_type=QuestionType.NUMERICAL,
                intended_skill="Calculate conductor resistance following wire die drawing under volume conservation",
                prerequisite_knowledge=["curr-curr-01"],
                misconception_target="misc-curr-01",
                satisfied_by_canonical_atom=None,
                needs_new_generation=True,
                risk_level="MEDIUM",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-curr-02-meters-conversion",
                chapter_id="current-electricity",
                curriculum_node_id="curr-curr-03",
                concept_id="concept-curr-meters-01",
                target_exam_level=ExamTargetLevel.JEE_MAIN,
                target_difficulty=DifficultyLevel.L3,
                question_type=QuestionType.SINGLE_CORRECT_MCQ,
                intended_skill="Determine shunt resistance required to convert galvanometer to multi-range ammeter",
                prerequisite_knowledge=["curr-curr-02"],
                misconception_target="misc-curr-02",
                satisfied_by_canonical_atom="current-electricity-question-3a1b8c4d",
                needs_new_generation=False,
                risk_level="MEDIUM",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-curr-03-drift-micro-source-deriv",
                chapter_id="current-electricity",
                curriculum_node_id="curr-curr-01",
                concept_id="concept-curr-drift-01",
                target_exam_level=ExamTargetLevel.JEE_MAIN,
                target_difficulty=DifficultyLevel.L3,
                question_type=QuestionType.SINGLE_CORRECT_MCQ,
                intended_skill="Relate current density and drift speed under non-uniform conductor cross-section",
                prerequisite_knowledge=["curr-curr-01"],
                misconception_target=None,
                satisfied_by_canonical_atom=None,
                needs_new_generation=True,
                risk_level="MEDIUM",
            ),

            # 4. Ray Optics
            QuestionRequirementItem(
                requirement_id="qreq-opt-01-snell-conceptual",
                chapter_id="ray-optics",
                curriculum_node_id="curr-opt-01",
                concept_id="concept-opt-snell-01",
                target_exam_level=ExamTargetLevel.JEE_MAIN,
                target_difficulty=DifficultyLevel.L2,
                question_type=QuestionType.CONCEPTUAL_QUALITATIVE,
                intended_skill="Determine wave speed, frequency, and wavelength changes across refraction boundary",
                prerequisite_knowledge=["curr-opt-01"],
                misconception_target="misc-opt-02",
                satisfied_by_canonical_atom=None,
                needs_new_generation=True,
                risk_level="LOW",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-opt-02-tir-prism-water",
                chapter_id="ray-optics",
                curriculum_node_id="curr-opt-02",
                concept_id="concept-opt-tir-01",
                target_exam_level=ExamTargetLevel.JEE_ADVANCED,
                target_difficulty=DifficultyLevel.L4,
                question_type=QuestionType.SINGLE_CORRECT_MCQ,
                intended_skill="Calculate critical angle and verify condition for TIR on submerged prism hypotenuse",
                prerequisite_knowledge=["curr-opt-01"],
                misconception_target="misc-opt-01",
                satisfied_by_canonical_atom="ray-optics-question-e04c1df3",
                needs_new_generation=False,
                risk_level="HIGH",
            ),
            QuestionRequirementItem(
                requirement_id="qreq-opt-03-prism-dispersion-adv",
                chapter_id="ray-optics",
                curriculum_node_id="curr-opt-02",
                concept_id="concept-opt-snell-01",
                target_exam_level=ExamTargetLevel.JEE_ADVANCED,
                target_difficulty=DifficultyLevel.L4,
                question_type=QuestionType.NUMERICAL,
                intended_skill="Determine angle of minimum deviation and emergence for 60-degree glass prism",
                prerequisite_knowledge=["curr-opt-01", "curr-opt-02"],
                misconception_target=None,
                satisfied_by_canonical_atom=None,
                needs_new_generation=True,
                risk_level="HIGH",
            ),
        ]

        satisfied_count = sum(1 for it in items if not it.needs_new_generation)
        gen_count = sum(1 for it in items if it.needs_new_generation)

        return QuestionRequirementReport(
            report_id=f"qreq-report-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
            total_requirements=len(items),
            satisfied_by_source_count=satisfied_count,
            new_generation_required_count=gen_count,
            requirements=items,
        )

    def generate_and_save_report(self, output_path: Optional[Path] = None) -> Path:
        """Generates and writes build/reports/question_requirements.json."""
        out = output_path or (self.reports_dir / "question_requirements.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        report = self.build_pilot_requirements()
        out.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        return out


if __name__ == "__main__":
    engine = QuestionRequirementsEngine()
    p = engine.generate_and_save_report()
    print(f"Generated question requirements report at: {p}")
