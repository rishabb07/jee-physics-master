import pytest
from jee_physics.core.state import (
    InvalidStateTransitionError,
    assert_valid_atom_transition,
    assert_valid_source_transition,
)
from jee_physics.models.enums import AtomStatus, SourceStatus


def test_valid_atom_state_transitions():
    # Staged -> Validated
    assert_valid_atom_transition(AtomStatus.STAGED, AtomStatus.VALIDATED)
    # Validated -> Verification Pending
    assert_valid_atom_transition(AtomStatus.VALIDATED, AtomStatus.VERIFICATION_PENDING)
    # Verification Pending -> Verified
    assert_valid_atom_transition(AtomStatus.VERIFICATION_PENDING, AtomStatus.VERIFIED)
    # Verified -> Archived
    assert_valid_atom_transition(AtomStatus.VERIFIED, AtomStatus.ARCHIVED)


def test_invalid_atom_direct_jump_to_verified_rejected():
    # Critical invariant: Unverified extractions cannot jump straight from STAGED to VERIFIED!
    with pytest.raises(InvalidStateTransitionError) as exc:
        assert_valid_atom_transition(AtomStatus.STAGED, AtomStatus.VERIFIED)
    assert "cannot transition from STAGED to VERIFIED" in str(exc.value)


def test_invalid_source_state_transition_rejected():
    with pytest.raises(InvalidStateTransitionError):
        assert_valid_source_transition(SourceStatus.REGISTERED, SourceStatus.EXTRACTION_COMPLETE)
