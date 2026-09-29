"""
Question Ladder Architecture for Phase 9 Question Bank.

Defines progressive cognitive sequences of questions from direct recognition
up through advanced multi-concept transfer and synthesis.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from jee_physics.models.question_bank import (
    CognitiveLadderLevel,
    GeneratedQuestion,
    QuestionLadder,
    QuestionLadderRung,
)


class QuestionLadderRegistry(BaseModel):
    """Catalog of question ladders."""
    ladders: List[QuestionLadder] = Field(default_factory=list)
    total_ladders: int = 0
    total_rungs: int = 0


class QuestionLadderBuilder:
    """Builds and validates progressive cognitive question ladders."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(".")

    def build_rotational_angular_momentum_ladder(
        self,
        questions_by_id: Dict[str, GeneratedQuestion],
    ) -> QuestionLadder:
        """Constructs a 4-rung cognitive ladder for rotational angular momentum."""
        rungs = [
            QuestionLadderRung(
                rung_number=1,
                cognitive_level=CognitiveLadderLevel.DIRECT_APPLICATION,
                question_id="rotational-motion-question-6c7cb960",
                prerequisite_rungs=[],
                cognitive_delta="Direct application of L = r x p = m v d for linear motion past origin",
                pedagogical_purpose="Establish baseline definition and origin dependence of particle angular momentum",
            ),
            QuestionLadderRung(
                rung_number=2,
                cognitive_level=CognitiveLadderLevel.RECOGNITION,
                question_id="gen-q-rot-misc-01",
                prerequisite_rungs=[1],
                cognitive_delta="Confront pitfall that straight-line motion supposedly has zero angular momentum",
                pedagogical_purpose="Eliminate common misconception and solidify coordinate independence of perpendicular distance",
            ),
            QuestionLadderRung(
                rung_number=3,
                cognitive_level=CognitiveLadderLevel.CONCEPT_COMBINATION,
                question_id="gen-q-rot-angmom-01",
                prerequisite_rungs=[1, 2],
                cognitive_delta="Combine rigid body disc moment of inertia with moving point mass and conservation law",
                pedagogical_purpose="Bridge particle angular momentum to rotating rigid bodies with time-varying geometry",
            ),
            QuestionLadderRung(
                rung_number=4,
                cognitive_level=CognitiveLadderLevel.ADVANCED_SYNTHESIS,
                question_id="rotational-motion-question-84f91c20",
                prerequisite_rungs=[1, 2, 3],
                cognitive_delta="Synthesize continuous time-dependent radial motion omega(t) with mechanical energy transformation",
                pedagogical_purpose="Master JEE Advanced multi-concept synthesis under non-conservative internal forces",
            ),
        ]

        return QuestionLadder(
            ladder_id="ladder-rot-angmom-cognitive-01",
            chapter_id="rotational-motion",
            topic_id="angular-momentum",
            title="Cognitive Scaffolding Ladder: Angular Momentum from Particle to Composite Rigid Disc",
            rungs=rungs,
        )

    def validate_ladder(self, ladder: QuestionLadder) -> List[str]:
        """Validates sequential cognitive integrity and prerequisite ladder links."""
        errors: List[str] = []
        if len(ladder.rungs) < 2:
            errors.append(f"Ladder '{ladder.ladder_id}' must have at least 2 rungs")

        seen_rungs = set()
        for rung in ladder.rungs:
            seen_rungs.add(rung.rung_number)
            for prereq in rung.prerequisite_rungs:
                if prereq >= rung.rung_number:
                    errors.append(
                        f"PREREQUISITE_CYCLE: Rung {rung.rung_number} references non-preceding rung {prereq}"
                    )
                if prereq not in seen_rungs and prereq >= rung.rung_number:
                    errors.append(f"MISSING_PREREQUISITE_RUNG: Rung {rung.rung_number} references unknown rung {prereq}")
        return errors
