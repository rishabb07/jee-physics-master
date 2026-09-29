from dataclasses import dataclass
from typing import Optional

from jee_physics.models.enums import VerificationVerdict
from jee_physics.verification.normalizer import compare_answers


@dataclass
class ComparisonResult:
    solvers_agree: bool
    matches_source: Optional[bool]
    preliminary_consensus: Optional[str]
    preliminary_verdict: VerificationVerdict
    discrepancy_classification: Optional[str]
    requires_adjudication: bool


def compare_solver_runs(
    source_claimed_answer: Optional[str],
    solver_a_answer: Optional[str],
    solver_b_answer: Optional[str],
) -> ComparisonResult:
    """Evaluates agreement between two independent solvers and the source claim.
    
    Decision Table:
    1. A == B and (source is None or A == source):
       -> Solvers agree and match source -> VERIFIED
    2. A == B and source is not None and A != source:
       -> Solvers agree but contradict source -> SOURCE_ERROR_CANDIDATE -> Requires adjudication to confirm
    3. A != B:
       -> Solvers disagree -> SOLVER_DISAGREEMENT -> Requires adjudication
    4. A is None or B is None:
       -> Solver failure or ambiguity -> Requires adjudication
    """
    # Check if either solver failed to produce an answer
    if solver_a_answer is None or solver_b_answer is None:
        return ComparisonResult(
            solvers_agree=False,
            matches_source=False if source_claimed_answer else None,
            preliminary_consensus=None,
            preliminary_verdict=VerificationVerdict.UNRESOLVED,
            discrepancy_classification="SOLVER_MISSING_ANSWER",
            requires_adjudication=True,
        )

    solvers_agree = compare_answers(solver_a_answer, solver_b_answer)

    if not solvers_agree:
        return ComparisonResult(
            solvers_agree=False,
            matches_source=False if source_claimed_answer else None,
            preliminary_consensus=None,
            preliminary_verdict=VerificationVerdict.UNRESOLVED,
            discrepancy_classification="SOLVER_DISAGREEMENT",
            requires_adjudication=True,
        )

    # Solvers agree on an answer
    consensus = solver_a_answer

    if source_claimed_answer is None:
        # Source provided no answer key; verified by independent consensus
        return ComparisonResult(
            solvers_agree=True,
            matches_source=None,
            preliminary_consensus=consensus,
            preliminary_verdict=VerificationVerdict.VERIFIED,
            discrepancy_classification="SOURCE_ANSWER_MISSING",
            requires_adjudication=False,
        )

    matches_source = compare_answers(consensus, source_claimed_answer)

    if matches_source:
        return ComparisonResult(
            solvers_agree=True,
            matches_source=True,
            preliminary_consensus=consensus,
            preliminary_verdict=VerificationVerdict.VERIFIED,
            discrepancy_classification=None,
            requires_adjudication=False,
        )
    else:
        # Solvers agreed, but their answer differs from the source key
        return ComparisonResult(
            solvers_agree=True,
            matches_source=False,
            preliminary_consensus=consensus,
            preliminary_verdict=VerificationVerdict.SOURCE_ERROR,
            discrepancy_classification="SOURCE_ERROR_CANDIDATE",
            requires_adjudication=True,  # Require adjudication to confirm textbook error
        )
