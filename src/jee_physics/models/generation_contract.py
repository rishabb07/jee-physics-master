from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, model_validator


class PhysicsClaimType(str, Enum):
    """Classification of individual student-facing physics claims."""
    FORMULA_ASSERTION = "FORMULA_ASSERTION"
    DERIVATION_STEP = "DERIVATION_STEP"
    CONCEPTUAL_PROPERTY = "CONCEPTUAL_PROPERTY"
    PHENOMENON_EXPLANATION = "PHENOMENON_EXPLANATION"
    LIMITING_CASE = "LIMITING_CASE"
    NUMERICAL_DATA = "NUMERICAL_DATA"
    DIAGRAM_INTERPRETATION = "DIAGRAM_INTERPRETATION"
    HISTORICAL_CONVENTION = "HISTORICAL_CONVENTION"


class GroundingMode(str, Enum):
    """Strict basis of authority for a physics claim."""
    SOURCE_EVIDENCE_BACKED = "SOURCE_EVIDENCE_BACKED"          # Supported by >= 1 granular evidence IDs
    FIRST_PRINCIPLES_PROOF = "FIRST_PRINCIPLES_PROOF"          # Mathematically proven from core definitions
    EXPLICIT_AXIOM = "EXPLICIT_AXIOM"                          # Fundamental axiom (e.g. Newton's laws, Maxwell's laws)


class GroundedClaim(BaseModel):
    """An individual physics assertion with mandatory evidence binding."""
    claim_id: str = Field(..., description="Unique claim identifier")
    claim_statement: str = Field(..., description="The physical or mathematical assertion")
    claim_type: PhysicsClaimType = Field(...)
    grounding_mode: GroundingMode = Field(...)
    cited_evidence_ids: List[str] = Field(default_factory=list, description="IDs of source evidence records")
    first_principles_proof: Optional[str] = Field(None, description="Mathematical proof if FIRST_PRINCIPLES_PROOF")
    verification_status: str = Field("PENDING", description="PENDING, VERIFIED, REJECTED")

    @model_validator(mode="after")
    def validate_grounding(self) -> "GroundedClaim":
        if self.grounding_mode == GroundingMode.SOURCE_EVIDENCE_BACKED:
            if not self.cited_evidence_ids:
                raise ValueError(f"Claim {self.claim_id} is marked SOURCE_EVIDENCE_BACKED but provides zero cited_evidence_ids.")
        elif self.grounding_mode == GroundingMode.FIRST_PRINCIPLES_PROOF:
            if not self.first_principles_proof and not self.cited_evidence_ids:
                raise ValueError(f"Claim {self.claim_id} is marked FIRST_PRINCIPLES_PROOF but provides no proof text or source backing.")
        return self


class SourceGroundedContentPayload(BaseModel):
    """A generated content block with full claim-to-evidence binding."""
    payload_id: str = Field(...)
    chapter_id: str = Field(...)
    topic_id: str = Field(...)
    claims: List[GroundedClaim] = Field(default_factory=list)
    cited_evidence_ids: List[str] = Field(default_factory=list)


class GenerationContractValidator:
    """Deterministic validator enforcing the Source-Grounded Generation Contract."""

    @staticmethod
    def audit_content_block(
        payload: SourceGroundedContentPayload,
        valid_evidence_ids: Set[str],
    ) -> Dict[str, Any]:
        """
        Audits a generated content block against registered source evidence.
        Rejects:
        1. Nonexistent cited evidence IDs (hallucinated citations)
        2. Claims with zero evidence and no first-principles proof (uncited claims)
        """
        violations: List[str] = []
        hallucinated_citations: List[str] = []

        # Audit top-level citations
        for eid in payload.cited_evidence_ids:
            if eid not in valid_evidence_ids:
                hallucinated_citations.append(eid)
                violations.append(f"Top-level cited evidence ID '{eid}' does not exist in source library.")

        # Audit individual claims
        for claim in payload.claims:
            for eid in claim.cited_evidence_ids:
                if eid not in valid_evidence_ids:
                    hallucinated_citations.append(eid)
                    violations.append(f"Claim '{claim.claim_id}' cites nonexistent evidence ID '{eid}'.")

            if claim.grounding_mode == GroundingMode.SOURCE_EVIDENCE_BACKED and not claim.cited_evidence_ids:
                violations.append(f"Claim '{claim.claim_id}' lacks source evidence citations.")

        passed = len(violations) == 0
        return {
            "payload_id": payload.payload_id,
            "passed": passed,
            "total_claims": len(payload.claims),
            "hallucinated_citations_count": len(hallucinated_citations),
            "hallucinated_citations": hallucinated_citations,
            "violations": violations,
        }
