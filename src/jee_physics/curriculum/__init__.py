"""Curriculum, Chapter Architecture, and Pedagogical Assembly Package."""

from jee_physics.curriculum.prerequisites import CurriculumPrerequisiteDAG
from jee_physics.curriculum.gate import (
    validate_chapter_spec,
    validate_chapter_plan,
    stage_curriculum_artifact,
    record_curriculum_audit_entry,
)
from jee_physics.curriculum.coverage import analyze_curriculum_coverage

__all__ = [
    "CurriculumPrerequisiteDAG",
    "validate_chapter_spec",
    "validate_chapter_plan",
    "stage_curriculum_artifact",
    "record_curriculum_audit_entry",
    "analyze_curriculum_coverage",
]
