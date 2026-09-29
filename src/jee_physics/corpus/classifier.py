from typing import Dict, List, Optional
from jee_physics.models.corpus import EnhancedSourceSegment, SourceContentType
from jee_physics.models.subject import SubjectClassificationRecord
from jee_physics.models.taxonomy import SubjectType


def classify_segment_subject(
    segment: EnhancedSourceSegment,
    source_file_name: str,
) -> SubjectType:
    """Classifies the subject domain boundary of a source segment.
    
    CRITICAL INVARIANT: Never allow Chemistry or Mathematics to enter the Physics KB.
    """
    title = segment.segment_title.lower()
    fname = source_file_name.lower()

    if "chemistry" in title:
        return SubjectType.CHEMISTRY
    if "mathematics" in title or "maths" in title:
        return SubjectType.MATHEMATICS
    if "front matter" in title or "preface" in title or "appendix" in title or "index" in title:
        return SubjectType.NON_CONTENT

    # For mock tests, check page boundaries explicitly
    if "mock" in fname:
        if segment.subject_type == "CHEMISTRY":
            return SubjectType.CHEMISTRY
        elif segment.subject_type == "MATHEMATICS":
            return SubjectType.MATHEMATICS
        elif segment.subject_type == "PHYSICS":
            return SubjectType.PHYSICS

    # For core physics textbooks
    if any(k in fname for k in ["verma", "halliday", "university physics", "feynman", "irodov"]):
        if any(nm in title for nm in ["preface", "contents", "cover", "about the authors", "index"]):
            return SubjectType.NON_CONTENT
        return SubjectType.PHYSICS

    return SubjectType.UNCERTAIN


def classify_segment_content_types(
    segment: EnhancedSourceSegment,
    sample_text: str,
) -> List[SourceContentType]:
    """Identifies content types present within a Physics segment."""
    types = set(segment.content_types)
    text = sample_text.lower()

    if "example" in text or "worked out example" in text or "sample problem" in text:
        types.add(SourceContentType.EXAMPLE)
    if "exercise" in text or "problem" in text or "questions for short answer" in text:
        types.add(SourceContentType.PROBLEM)
    if "law" in text or "newton's" in text or "kepler" in text or "gauss" in text:
        types.add(SourceContentType.LAW)
    if "definition" in text or "defined as" in text:
        types.add(SourceContentType.DEFINITION)
    if "derive" in text or "derivation" in text or "proof" in text or "we obtain" in text:
        types.add(SourceContentType.DERIVATION)
    if "misconception" in text or "caution" in text or "pitfall" in text or "warning" in text:
        types.add(SourceContentType.MISCONCEPTION_CAUTION)
    if "experiment" in text or "apparatus" in text or "observation" in text:
        types.add(SourceContentType.EXPERIMENT_OBSERVATION)

    if not types:
        types.add(SourceContentType.CONCEPT)

    return sorted(list(types), key=lambda x: x.value)
