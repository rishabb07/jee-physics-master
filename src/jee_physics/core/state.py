from typing import Dict, Set

from jee_physics.models.enums import AtomStatus, SourceStatus


class InvalidStateTransitionError(ValueError):
    """Raised when an illegal lifecycle state transition is attempted."""
    pass


VALID_ATOM_TRANSITIONS: Dict[AtomStatus, Set[AtomStatus]] = {
    AtomStatus.STAGED: {
        AtomStatus.VALIDATED,
        AtomStatus.REJECTED,
        AtomStatus.ARCHIVED,
    },
    AtomStatus.VALIDATED: {
        AtomStatus.VERIFICATION_PENDING,
        AtomStatus.ARCHIVED,
        AtomStatus.REJECTED,
    },
    AtomStatus.VERIFICATION_PENDING: {
        AtomStatus.VERIFIED,
        AtomStatus.AMBIGUOUS,
        AtomStatus.REJECTED,
        AtomStatus.ARCHIVED,
    },
    AtomStatus.AMBIGUOUS: {
        AtomStatus.VERIFIED,
        AtomStatus.REJECTED,
        AtomStatus.ARCHIVED,
    },
    AtomStatus.VERIFIED: {
        AtomStatus.ARCHIVED,  # Decommissioned or superseded
    },
    AtomStatus.ARCHIVED: {
        AtomStatus.VALIDATED,  # Restored from archive
    },
    AtomStatus.REJECTED: {
        AtomStatus.STAGED,  # Re-extracted / re-processed
    },
}


VALID_SOURCE_TRANSITIONS: Dict[SourceStatus, Set[SourceStatus]] = {
    SourceStatus.REGISTERED: {
        SourceStatus.SEGMENTED,
        SourceStatus.FAILED,
        SourceStatus.MISSING,
    },
    SourceStatus.SEGMENTED: {
        SourceStatus.EXTRACTION_PENDING,
        SourceStatus.FAILED,
        SourceStatus.MISSING,
    },
    SourceStatus.EXTRACTION_PENDING: {
        SourceStatus.EXTRACTION_COMPLETE,
        SourceStatus.FAILED,
        SourceStatus.MISSING,
    },
    SourceStatus.EXTRACTION_COMPLETE: {
        SourceStatus.EXTRACTION_PENDING,  # Re-triggered if source file updated
        SourceStatus.FAILED,
        SourceStatus.MISSING,
    },
    SourceStatus.MISSING: {
        SourceStatus.REGISTERED,  # Restored
        SourceStatus.EXTRACTION_PENDING,
    },
    SourceStatus.FAILED: {
        SourceStatus.REGISTERED,  # Retry from scratch
        SourceStatus.EXTRACTION_PENDING,
        SourceStatus.MISSING,
    },
}


def assert_valid_atom_transition(current: AtomStatus, target: AtomStatus) -> None:
    """Validates that an atom status transition obeys the lifecycle rules.
    
    Prevents unverified atoms from jumping straight from STAGED to VERIFIED.
    """
    if current == target:
        return
    allowed = VALID_ATOM_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise InvalidStateTransitionError(
            f"Invalid Atom transition: cannot transition from {current.value} to {target.value}. "
            f"Allowed targets: {[s.value for s in allowed]}"
        )


def assert_valid_source_transition(current: SourceStatus, target: SourceStatus) -> None:
    """Validates that a source status transition obeys the ingestion lifecycle."""
    if current == target:
        return
    allowed = VALID_SOURCE_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise InvalidStateTransitionError(
            f"Invalid Source transition: cannot transition from {current.value} to {target.value}. "
            f"Allowed targets: {[s.value for s in allowed]}"
        )
