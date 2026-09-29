import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from jee_physics.corpus.disagreements import get_all_source_disagreements
from jee_physics.models.evidence import (
    DerivationEvidenceRecord,
    EvidenceTruthClassification,
    ExampleEvidenceRecord,
    FigureEvidenceRecord,
    FormulaEvidenceRecord,
    MockQuestionEvidenceRecord,
    ProblemEvidenceRecord,
    SourceEvidenceRecord,
    SourceFidelityClass,
    TaxonomyEvidenceBundle,
)


class EvidenceRetriever:
    """
    Deterministic retrieval engine providing access to the granular source evidence layer.
    Used by content-generation and assessment agents in Phase 12.
    """

    def __init__(self, evidence_dir: Path = Path("sources/evidence")):
        self.evidence_dir = Path(evidence_dir)
        self.records: List[SourceEvidenceRecord] = []
        self.formulas: List[FormulaEvidenceRecord] = []
        self.derivations: List[DerivationEvidenceRecord] = []
        self.examples: List[ExampleEvidenceRecord] = []
        self.problems: List[ProblemEvidenceRecord] = []
        self.mock_questions: List[MockQuestionEvidenceRecord] = []
        self.figures: List[FigureEvidenceRecord] = []
        self.disagreements: List[Any] = get_all_source_disagreements()

        # Provenance index: item_id -> provenance dict
        self._provenance_index: Dict[str, Dict[str, Any]] = {}
        # Valid evidence IDs set for fast validation
        self.valid_evidence_ids: Set[str] = set()

        self._load_ledgers()

    def _load_ledgers(self) -> None:
        """Loads all evidence ledgers from disk."""
        records_file = self.evidence_dir / "records.json"
        if records_file.exists():
            with open(records_file, "r", encoding="utf-8") as f:
                self.records = [SourceEvidenceRecord(**item) for item in json.load(f)]
                for r in self.records:
                    self.valid_evidence_ids.add(r.evidence_id)
                    self._provenance_index[r.evidence_id] = {
                        "type": "EVIDENCE_RECORD",
                        "source_id": r.source_id,
                        "page_start": r.page_start,
                        "page_end": r.page_end,
                        "section": r.section_or_chapter,
                        "provenance": r.provenance,
                    }

        formulas_file = self.evidence_dir / "formulas.json"
        if formulas_file.exists():
            with open(formulas_file, "r", encoding="utf-8") as f:
                self.formulas = [FormulaEvidenceRecord(**item) for item in json.load(f)]
                for form in self.formulas:
                    self.valid_evidence_ids.add(form.formula_id)
                    self._provenance_index[form.formula_id] = {
                        "type": "FORMULA",
                        "source_id": form.source_id,
                        "pages": form.pages,
                        "corroborating_sources": form.corroborating_source_ids,
                        "latex": form.normalized_latex,
                    }

        derivs_file = self.evidence_dir / "derivations.json"
        if derivs_file.exists():
            with open(derivs_file, "r", encoding="utf-8") as f:
                self.derivations = [DerivationEvidenceRecord(**item) for item in json.load(f)]
                for d in self.derivations:
                    self.valid_evidence_ids.add(d.derivation_id)
                    self._provenance_index[d.derivation_id] = {
                        "type": "DERIVATION",
                        "source_id": d.source_id,
                        "page_range": d.page_range,
                        "title": d.title,
                        "final_result": d.final_result,
                    }

        examples_file = self.evidence_dir / "examples.json"
        if examples_file.exists():
            with open(examples_file, "r", encoding="utf-8") as f:
                self.examples = [ExampleEvidenceRecord(**item) for item in json.load(f)]
                for ex in self.examples:
                    self.valid_evidence_ids.add(ex.example_id)
                    self._provenance_index[ex.example_id] = {
                        "type": "WORKED_EXAMPLE",
                        "source_id": ex.source_id,
                        "page_range": ex.page_range,
                        "title": ex.title_or_label,
                    }

        problems_file = self.evidence_dir / "problems.json"
        if problems_file.exists():
            with open(problems_file, "r", encoding="utf-8") as f:
                self.problems = [ProblemEvidenceRecord(**item) for item in json.load(f)]
                for p in self.problems:
                    self.valid_evidence_ids.add(p.problem_id)
                    self._provenance_index[p.problem_id] = {
                        "type": "PROBLEM",
                        "source_id": p.source_id,
                        "page": p.page,
                        "printed_problem_number": p.printed_problem_number,
                    }

        mock_file = self.evidence_dir / "mock_questions.json"
        if mock_file.exists():
            with open(mock_file, "r", encoding="utf-8") as f:
                self.mock_questions = [MockQuestionEvidenceRecord(**item) for item in json.load(f)]
                for m in self.mock_questions:
                    self.valid_evidence_ids.add(m.mock_question_id)
                    self._provenance_index[m.mock_question_id] = {
                        "type": "MOCK_QUESTION",
                        "source_id": m.source_id,
                        "page": m.page,
                        "question_number": m.question_number,
                    }

        figures_file = self.evidence_dir / "figures.json"
        if figures_file.exists():
            with open(figures_file, "r", encoding="utf-8") as f:
                self.figures = [FigureEvidenceRecord(**item) for item in json.load(f)]
                for fig in self.figures:
                    self.valid_evidence_ids.add(fig.figure_id)
                    self._provenance_index[fig.figure_id] = {
                        "type": "FIGURE",
                        "source_id": fig.source_id,
                        "page": fig.page,
                        "caption": fig.caption,
                    }

    def get_evidence_by_taxonomy(
        self,
        taxonomy_node_id: str,
        exact_only: bool = False,
        fidelity_mode: str = "ALL",
    ) -> TaxonomyEvidenceBundle:
        """
        Retrieves all evidence records, formulas, derivations, examples, problems,
        mock questions, figures, and conflicts for a given taxonomy node.
        
        fidelity_mode:
          - "ALL": Deliver all matching records (default).
          - "EXACT_ONLY" / "SOURCE_VERBATIM": Deliver strictly SOURCE_VERBATIM and SOURCE_VISUAL records.
          - "SOURCE_GROUNDED": Deliver SOURCE_VERBATIM, SOURCE_VISUAL, and SOURCE_DERIVED records.
        """
        matching_records = [
            r for r in self.records if taxonomy_node_id in r.taxonomy_node_ids
        ]

        def _is_cls(r: Any, target: SourceFidelityClass) -> bool:
            fc = getattr(r, "fidelity_class", None)
            val = fc.value if hasattr(fc, "value") else str(fc)
            return val == target.value

        verbatim_records = [r for r in matching_records if _is_cls(r, SourceFidelityClass.SOURCE_VERBATIM)]
        visual_records = [r for r in matching_records if _is_cls(r, SourceFidelityClass.SOURCE_VISUAL)]
        derived_records = [r for r in matching_records if _is_cls(r, SourceFidelityClass.SOURCE_DERIVED)]
        metadata_records = [
            r for r in matching_records
            if _is_cls(r, SourceFidelityClass.PROJECT_DERIVED)
            or _is_cls(r, SourceFidelityClass.INDEX_METADATA)
            or getattr(r, "truth_classification", None) in (
                EvidenceTruthClassification.INDEX_METADATA,
                "INDEX_METADATA",
                EvidenceTruthClassification.PROJECT_DERIVED,
                "PROJECT_DERIVED",
                EvidenceTruthClassification.VERIFICATION_DERIVED,
                "VERIFICATION_DERIVED",
            )
        ]

        source_exact_records = [
            r for r in matching_records
            if getattr(r, "truth_classification", None) in (
                EvidenceTruthClassification.SOURCE_EXACT,
                "SOURCE_EXACT",
                EvidenceTruthClassification.SOURCE_VERBATIM,
                "SOURCE_VERBATIM",
                EvidenceTruthClassification.SOURCE_VISUAL,
                "SOURCE_VISUAL",
            )
        ]

        matching_formulas = [
            f for f in self.formulas if taxonomy_node_id in f.taxonomy_node_ids
        ]
        matching_derivations = [
            d for d in self.derivations if taxonomy_node_id in d.taxonomy_node_ids
        ]
        matching_examples = [
            e for e in self.examples if taxonomy_node_id in e.taxonomy_node_ids
        ]
        matching_problems = [
            p for p in self.problems if taxonomy_node_id in p.taxonomy_node_ids
        ]
        matching_mocks = [
            m for m in self.mock_questions if taxonomy_node_id in m.taxonomy_node_ids
        ]

        # Figures can be matched via parent ID or page
        parent_ids = {r.evidence_id for r in matching_records} | {
            e.example_id for e in matching_examples
        } | {d.derivation_id for d in matching_derivations}
        matching_figures = [
            fig for fig in self.figures
            if (fig.parent_concept_or_problem_id in parent_ids)
            or any(fig.figure_id in r.figure_refs for r in matching_records)
        ]

        # Sources covering this node
        sources_set: Set[str] = set()
        for item in matching_records:
            sources_set.add(item.source_id)
        for item in matching_formulas:
            sources_set.add(item.source_id)
            sources_set.update(item.corroborating_source_ids)
        for item in matching_derivations:
            sources_set.add(item.source_id)
        for item in matching_examples:
            sources_set.add(item.source_id)
        for item in matching_problems:
            sources_set.add(item.source_id)
        for item in matching_mocks:
            sources_set.add(item.source_id)

        # Conflicts
        matching_conflicts = []
        for dis in self.disagreements:
            if taxonomy_node_id in dis.topic_or_concept.lower():
                matching_conflicts.append(dis.model_dump())

        # Select delivered evidence based on fidelity mode
        mode_upper = fidelity_mode.upper()
        if exact_only or mode_upper in ("EXACT_ONLY", "SOURCE_VERBATIM"):
            delivered_evidence = verbatim_records + visual_records
        elif mode_upper == "SOURCE_GROUNDED":
            delivered_evidence = verbatim_records + visual_records + derived_records
        else:
            delivered_evidence = matching_records

        all_derived_artifacts = (
            derived_records
            + matching_formulas
            + matching_derivations
            + matching_examples
            + matching_figures
        )

        return TaxonomyEvidenceBundle(
            taxonomy_node_id=taxonomy_node_id,
            taxonomy_name=taxonomy_node_id.replace("-", " ").title(),
            corroborating_sources=sorted(list(sources_set)),
            evidence_records=delivered_evidence,
            source_evidence_records=source_exact_records,
            verbatim_records=verbatim_records,
            visual_records=visual_records,
            derived_records=all_derived_artifacts,
            metadata_records=metadata_records,
            formulas=matching_formulas,
            derivations=matching_derivations,
            examples=matching_examples,
            problems=matching_problems,
            mock_questions=matching_mocks,
            figures=matching_figures,
            source_conflicts=matching_conflicts,
        )

    def query_verbatim_evidence(self, taxonomy_node_id: str) -> List[SourceEvidenceRecord]:
        """Returns strictly SOURCE_VERBATIM records for the given taxonomy node."""
        bundle = self.get_evidence_by_taxonomy(taxonomy_node_id, fidelity_mode="SOURCE_VERBATIM")
        return bundle.verbatim_records

    def query_visual_evidence(self, taxonomy_node_id: str) -> List[SourceEvidenceRecord]:
        """Returns strictly SOURCE_VISUAL records (e.g. Feynman) for the given taxonomy node."""
        bundle = self.get_evidence_by_taxonomy(taxonomy_node_id)
        return bundle.visual_records

    def query_derived_evidence(self, taxonomy_node_id: str) -> List[Any]:
        """Returns all SOURCE_DERIVED items (formulas, derivations, examples) for the given taxonomy node."""
        bundle = self.get_evidence_by_taxonomy(taxonomy_node_id)
        return bundle.derived_records

    def get_provenance(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves exact physical page and bibliographic provenance for any evidence/formula/problem ID."""
        return self._provenance_index.get(item_id)

    def get_corroborating_sources(self, taxonomy_node_id: str) -> List[str]:
        """Returns the list of unique sources that independently cover a taxonomy node."""
        bundle = self.get_evidence_by_taxonomy(taxonomy_node_id)
        return bundle.corroborating_sources

    def format_acceptance_demonstration(self, taxonomy_node_id: str) -> str:
        """
        Produces the authoritative answer required by Section 21 of the Phase 11.5 Specification:
        'Show me the exact relevant evidence from HCV, Halliday, University Physics, Feynman and/or Irodov,
        including page ranges, formulas, derivations, examples and problems, and tell me which sources
        independently cover the same concept.'
        """
        bundle = self.get_evidence_by_taxonomy(taxonomy_node_id)

        lines = [
            f"=== EVIDENCE REPORT FOR TAXONOMY NODE: '{taxonomy_node_id}' ===",
            f"Corroborating Sources ({len(bundle.corroborating_sources)}):",
        ]
        for s in bundle.corroborating_sources:
            lines.append(f"  * {s}")

        lines.append(f"\n1. Semantic Evidence Units ({len(bundle.evidence_records)}):")
        for r in bundle.evidence_records:
            lines.append(f"  - [{r.evidence_id}] Source: {r.source_id}, pp. {r.page_start}-{r.page_end}")
            lines.append(f"    Section: {r.section_or_chapter} ({r.evidence_type.value})")
            lines.append(f"    Text: \"{r.content_text[:120]}...\"")

        lines.append(f"\n2. Formulas ({len(bundle.formulas)}):")
        for f in bundle.formulas:
            lines.append(f"  - [{f.formula_id}] ${f.normalized_latex}$")
            lines.append(f"    Source: {f.source_id} (pp. {f.pages}) | Convention: {f.notation_or_convention}")
            if f.corroborating_source_ids:
                lines.append(f"    Independent Corroboration: {', '.join(f.corroborating_source_ids)}")

        lines.append(f"\n3. Derivations ({len(bundle.derivations)}):")
        for d in bundle.derivations:
            lines.append(f"  - [{d.derivation_id}] {d.title}")
            lines.append(f"    Source: {d.source_id} (pp. {d.page_range[0]}-{d.page_range[1]})")
            lines.append(f"    Result: ${d.final_result}$")

        lines.append(f"\n4. Worked Examples ({len(bundle.examples)}):")
        for ex in bundle.examples:
            lines.append(f"  - [{ex.example_id}] {ex.title_or_label}")
            lines.append(f"    Source: {ex.source_id} (pp. {ex.page_range[0]}-{ex.page_range[1]})")
            lines.append(f"    Problem: \"{ex.problem_statement[:100]}...\"")
            lines.append(f"    Result: {ex.source_result}")

        lines.append(f"\n5. Problems & Exercises ({len(bundle.problems)}):")
        for p in bundle.problems:
            lines.append(f"  - [{p.problem_id}] Problem {p.printed_problem_number} in {p.chapter_or_section}")
            lines.append(f"    Source: {p.source_id} (p. {p.page})")
            lines.append(f"    Statement: \"{p.problem_statement[:100]}...\"")
            if p.source_answer:
                lines.append(f"    Answer: {p.source_answer}")

        lines.append(f"\n6. Mock Questions ({len(bundle.mock_questions)}):")
        for m in bundle.mock_questions:
            lines.append(f"  - [{m.mock_question_id}] Q{m.question_number} (Page {m.page}) from {m.source_id}")
            lines.append(f"    Statement: \"{m.question_statement[:100]}...\"")
            lines.append(f"    Answer: Option {m.source_answer}")

        lines.append(f"\n7. Figures ({len(bundle.figures)}):")
        for fig in bundle.figures:
            lines.append(f"  - [{fig.figure_id}] p. {fig.page} ({fig.source_id})")
            lines.append(f"    Caption: \"{fig.caption}\"")

        if bundle.source_conflicts:
            lines.append(f"\n8. Documented Source Conflicts ({len(bundle.source_conflicts)}):")
            for conf in bundle.source_conflicts:
                lines.append(f"  - [{conf.get('conflict_id')}] Category: {conf.get('conflict_category')}")
                lines.append(f"    Details: {conf.get('nature_of_disagreement')}")

        return "\n".join(lines)
