from enum import Enum


class SourceStatus(str, Enum):
    REGISTERED = "REGISTERED"
    SEGMENTED = "SEGMENTED"
    EXTRACTION_PENDING = "EXTRACTION_PENDING"
    EXTRACTION_COMPLETE = "EXTRACTION_COMPLETE"
    MISSING = "MISSING"  # File previously registered but removed from sources/raw/
    FAILED = "FAILED"


class SourceType(str, Enum):
    TEXTBOOK = "textbook"
    PROBLEM_BOOK = "problem_book"
    COACHING_NOTES = "coaching_notes"
    TEST_PAPER = "test_paper"
    HANDWRITTEN_NOTES = "handwritten_notes"
    REFERENCE_BOOK = "reference_book"
    OTHER = "other"


class FileFormat(str, Enum):
    PDF = "pdf"
    IMAGE = "image"
    UNSUPPORTED = "unsupported"


class SegmentType(str, Enum):
    DETERMINISTIC_PAGE_SEGMENT = "DETERMINISTIC_PAGE_SEGMENT"
    LLM_PROPOSED_SEMANTIC_SEGMENT = "LLM_PROPOSED_SEMANTIC_SEGMENT"


class AtomStatus(str, Enum):
    STAGED = "STAGED"
    VALIDATED = "VALIDATED"
    VERIFICATION_PENDING = "VERIFICATION_PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    AMBIGUOUS = "AMBIGUOUS"
    ARCHIVED = "ARCHIVED"


class AtomType(str, Enum):
    THEORY = "theory"
    FORMULA = "formula"
    SOLVED_EXAMPLE = "solved_example"
    QUESTION = "question"
    FIGURE = "figure"
    INSIGHT = "insight"
    MISCONCEPTION = "misconception"


class DifficultyLevel(str, Enum):
    L1 = "L1"  # Direct formula / recall
    L2 = "L2"  # Standard JEE Main
    L3 = "L3"  # JEE Advanced single concept
    L4 = "L4"  # JEE Advanced multi-concept
    L5 = "L5"  # Olympiad / deep synthesis


class VerificationVerdict(str, Enum):
    VERIFIED = "VERIFIED"
    SOURCE_ERROR = "SOURCE_ERROR"
    MODEL_ERROR = "MODEL_ERROR"
    AMBIGUOUS = "AMBIGUOUS"
    UNRESOLVED = "UNRESOLVED"


class ReviewIssueType(str, Enum):
    OCR_AMBIGUITY = "OCR_AMBIGUITY"
    PHYSICS_CONFLICT = "PHYSICS_CONFLICT"
    UNMAPPED_ATOM = "UNMAPPED_ATOM"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    SCHEMA_VIOLATION = "SCHEMA_VIOLATION"
    CORRUPTED_SOURCE = "CORRUPTED_SOURCE"
    OTHER = "OTHER"


class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CORRECTED = "CORRECTED"
    REJECTED = "REJECTED"
    UNRESOLVED = "UNRESOLVED"
