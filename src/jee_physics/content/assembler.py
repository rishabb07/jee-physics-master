"""
Chapter Editorial Assembler for JEE Physics Master Knowledge System.
Transforms verified atomic content blocks, chapter specifications, and plans
into structured JSON content blocks and projected Markdown drafts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from jee_physics.models.content import (
    ChapterContentBlock,
    ClaimTraceClass,
    ContentBlockType,
    ContentVerificationStatus,
)


class ChapterAssembler:
    """Assembles structured chapters from verified content atoms."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.verified_dir = workspace_root / "content" / "verified"
        self.drafts_dir = workspace_root / "build" / "drafts"
        self.curriculum_dir = workspace_root / "build" / "staging" / "incoming" / "curriculum"
        self.kb_atoms_dir = workspace_root / "kb" / "atoms"

    def load_spec(self, chapter_id: str) -> Dict[str, Any]:
        """Loads ChapterSpec from staging or curriculum directory."""
        path = self.curriculum_dir / f"{chapter_id}_spec.json"
        if not path.exists():
            path = self.workspace_root / "curriculum" / f"{chapter_id}_spec.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_plan(self, chapter_id: str) -> Dict[str, Any]:
        """Loads ChapterPlan from staging or curriculum directory."""
        path = self.curriculum_dir / f"{chapter_id}_plan.json"
        if not path.exists():
            path = self.workspace_root / "curriculum" / f"{chapter_id}_plan.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_verified_artifact(self, category: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Loads verified content artifact from content/verified/{category}/."""
        path = self.verified_dir / category / f"{item_id}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        staging_path = self.workspace_root / "build" / "staging" / "incoming" / "content" / category / f"{item_id}.json"
        if staging_path.exists():
            with open(staging_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def load_canonical_atom(self, atom_id: str) -> Optional[Dict[str, Any]]:
        """Loads canonical verified atom from kb/atoms/."""
        path = self.kb_atoms_dir / f"{atom_id}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def assemble_chapter(self, chapter_id: str) -> List[ChapterContentBlock]:
        """Assembles complete typed content block sequence for a chapter."""
        spec = self.load_spec(chapter_id)
        plan = self.load_plan(chapter_id)

        blocks: List[ChapterContentBlock] = []
        global_order = 1

        # 1. Hero / Objectives Block
        hero_title = plan.get("title", spec.get("chapter_title", chapter_id))
        hero_md = [
            f"# Chapter: {hero_title}",
            "",
            f"**Template**: `{spec.get('template_type')}`  ",
            f"**Prerequisites**: {', '.join(spec.get('prerequisite_curriculum_nodes', []))}  ",
            "",
            "## Learning Objectives",
        ]
        for obj in spec.get("learning_objectives", []):
            hero_md.append(f"- {obj}")

        md_body = "\n".join(hero_md)
        blocks.append(
            ChapterContentBlock(
                block_id=f"block-{chapter_id}-{global_order:03d}",
                block_type=ContentBlockType.OBJECTIVE,
                chapter_id=chapter_id,
                section_id="sec-intro",
                order_in_section=1,
                payload_id=f"spec-{chapter_id}",
                payload_type="ChapterSpec",
                title=f"Introduction to {hero_title}",
                rendered_markdown=md_body,
                trace_class=ClaimTraceClass.EDITORIAL_TRANSITION,
                source_atom_ids=[],
                verification_status=ContentVerificationStatus.VERIFIED,
                content_hash=self._hash_text(md_body),
            )
        )
        global_order += 1

        # 2. Iterate through sections defined in ChapterPlan
        for sec in plan.get("sections", []):
            sec_id = sec.get("section_id", f"sec-{global_order}")
            sec_title = sec.get("title", f"Section {global_order}")
            sec_purpose = sec.get("pedagogical_purpose", "")
            sec_order = 1

            # Section Overview Block
            sec_intro_md = [
                f"## {sec_title}",
                "",
                f"> **Pedagogical Goal**: {sec_purpose}",
                "",
            ]
            sec_md_str = "\n".join(sec_intro_md)
            blocks.append(
                ChapterContentBlock(
                    block_id=f"block-{chapter_id}-{global_order:03d}",
                    block_type=ContentBlockType.EDITORIAL_TRANSITION,
                    chapter_id=chapter_id,
                    section_id=sec_id,
                    order_in_section=sec_order,
                    payload_id=sec_id,
                    payload_type="ChapterSectionPlan",
                    title=f"Section Overview: {sec_title}",
                    rendered_markdown=sec_md_str,
                    trace_class=ClaimTraceClass.EDITORIAL_TRANSITION,
                    source_atom_ids=[],
                    verification_status=ContentVerificationStatus.VERIFIED,
                    content_hash=self._hash_text(sec_md_str),
                )
            )
            global_order += 1
            sec_order += 1

            # Concepts in this section
            for concept_id in sec.get("concepts", []):
                concept_data = self.load_verified_artifact("concepts", concept_id)
                if concept_data:
                    c_title = concept_data.get("title", concept_id)
                    c_def = concept_data.get("formal_definition") or concept_data.get("core_definition", "")
                    c_intuition = concept_data.get("intuition") or concept_data.get("physical_significance", "")
                    c_math = concept_data.get("mathematical_statement", "")
                    c_scope = concept_data.get("assumptions") or concept_data.get("assumptions_and_scope", [])

                    c_md = [
                        f"### Concept: {c_title}",
                        "",
                        f"**Definition**: {c_def}",
                        "",
                        f"**Physical Significance**: {c_intuition}",
                        "",
                    ]
                    if c_math:
                        c_md.extend(["$$", c_math, "$$", ""])
                    if c_scope:
                        c_md.append("**Assumptions & Scope of Validity**:")
                        for s in c_scope:
                            c_md.append(f"- {s}")
                        c_md.append("")

                    c_md_str = "\n".join(c_md)
                    blocks.append(
                        ChapterContentBlock(
                            block_id=f"block-{chapter_id}-{global_order:03d}",
                            block_type=ContentBlockType.CONCEPT_EXPLANATION,
                            chapter_id=chapter_id,
                            section_id=sec_id,
                            order_in_section=sec_order,
                            payload_id=concept_id,
                            payload_type="ConceptExplanation",
                            title=c_title,
                            rendered_markdown=c_md_str,
                            trace_class=ClaimTraceClass.SOURCE_DERIVED,
                            source_atom_ids=[],
                            verification_status=ContentVerificationStatus.VERIFIED,
                            content_hash=self._hash_text(c_md_str),
                        )
                    )
                    global_order += 1
                    sec_order += 1

            # Formulas & Derivations in this section
            for formula_id in sec.get("formula_ids", []):
                formula_data = self.load_verified_artifact("formulas", formula_id)
                if formula_data:
                    f_title = formula_data.get("title", formula_id)
                    f_eq = formula_data.get("equation") or formula_data.get("equation_latex", "")
                    f_vars = formula_data.get("variables", {})
                    f_units = formula_data.get("units", {}) or formula_data.get("units_and_dimensions", {})
                    f_dims = formula_data.get("dimensions", {})
                    f_assumptions = formula_data.get("assumptions", [])
                    f_validity = formula_data.get("validity_conditions") or formula_data.get("conditions_of_validity", [])

                    f_md = [
                        f"### Formula: {f_title}",
                        "",
                        "**Governing Equation**:",
                        f"$$ {f_eq} $$",
                        "",
                        "**Variable Inventory & SI Units**:",
                    ]
                    for v_name, v_desc in f_vars.items():
                        u_str = f_units.get(v_name, "")
                        d_str = f_dims.get(v_name, "")
                        dim_part = f" | Dim: `{d_str}`" if d_str else ""
                        unit_part = f" (Unit: `{u_str}`{dim_part})" if u_str else ""
                        f_md.append(f"- ${v_name}$: {v_desc}{unit_part}")
                    f_md.append("")

                    if f_assumptions:
                        f_md.append("**Physical Assumptions**:")
                        for a in f_assumptions:
                            f_md.append(f"- {a}")
                        f_md.append("")

                    if f_validity:
                        f_md.append("**Domain of Validity**:")
                        for v in f_validity:
                            f_md.append(f"- {v}")
                        f_md.append("")

                    f_md_str = "\n".join(f_md)
                    blocks.append(
                        ChapterContentBlock(
                            block_id=f"block-{chapter_id}-{global_order:03d}",
                            block_type=ContentBlockType.FORMULA,
                            chapter_id=chapter_id,
                            section_id=sec_id,
                            order_in_section=sec_order,
                            payload_id=formula_id,
                            payload_type="FormulaRecord",
                            title=f"Formula: {f_title}",
                            rendered_markdown=f_md_str,
                            trace_class=ClaimTraceClass.GENERATED_AND_VERIFIED,
                            source_atom_ids=[],
                            verification_status=ContentVerificationStatus.VERIFIED,
                            content_hash=self._hash_text(f_md_str),
                        )
                    )
                    global_order += 1
                    sec_order += 1

                derivation_data = self.load_verified_artifact("derivations", f"derivation-{formula_id}")
                if derivation_data:
                    d_sys = derivation_data.get("physical_system", "")
                    d_eq = derivation_data.get("target_equation") or derivation_data.get("target_equation_latex", "")
                    d_steps = derivation_data.get("ordered_steps") or derivation_data.get("steps", [])
                    d_dim = derivation_data.get("dimensional_check", "")
                    d_limits = derivation_data.get("applicability_conditions") or derivation_data.get("limiting_case_checks", [])

                    d_md = [
                        f"### Derivation: Formula `{formula_id}`",
                        "",
                        "**Target Governing Relation**:",
                        f"$$ {d_eq} $$",
                        "",
                    ]
                    if d_sys:
                        d_md.extend([f"**Physical System Under Consideration**: {d_sys}", ""])
                    d_md.append("#### Step-by-Step Proof")

                    for step in d_steps:
                        s_num = step.get("step_number", 1)
                        s_desc = step.get("description") or step.get("action_description", "")
                        s_eq = step.get("result_equation") or step.get("equation_latex", "")
                        s_just = step.get("operation") or step.get("justification", "")
                        d_md.extend([
                            f"**Step {s_num}**: {s_desc}",
                            f"$$ {s_eq} $$",
                            f"*Physical Operation*: {s_just}",
                            "",
                        ])

                    if d_dim:
                        d_md.extend([f"**Dimensional Homogeneity**: {d_dim}", ""])
                    if d_limits:
                        d_md.append("**Applicability & Limiting Conditions**:")
                        for l in d_limits:
                            d_md.append(f"- {l}")
                        d_md.append("")

                    d_md_str = "\n".join(d_md)
                    blocks.append(
                        ChapterContentBlock(
                            block_id=f"block-{chapter_id}-{global_order:03d}",
                            block_type=ContentBlockType.DERIVATION,
                            chapter_id=chapter_id,
                            section_id=sec_id,
                            order_in_section=sec_order,
                            payload_id=f"derivation-{formula_id}",
                            payload_type="DerivationRecord",
                            title=f"Derivation: {formula_id}",
                            rendered_markdown=d_md_str,
                            trace_class=ClaimTraceClass.GENERATED_AND_VERIFIED,
                            source_atom_ids=[],
                            verification_status=ContentVerificationStatus.VERIFIED,
                            content_hash=self._hash_text(d_md_str),
                        )
                    )
                    global_order += 1
                    sec_order += 1

            # Worked Examples in this section
            for ex_id in sec.get("worked_example_ids", []):
                ex_data = self.load_verified_artifact("examples", ex_id)
                if ex_data:
                    ex_stmt = ex_data.get("problem_statement", "")
                    ex_target = ex_data.get("target_quantity") or ex_data.get("target_variable", "")
                    ex_steps = ex_data.get("ordered_steps") or ex_data.get("solution_steps", [])
                    ex_ans = ex_data.get("final_answer", "")
                    ex_traps = ex_data.get("trap_alerts", [])
                    ex_sanity = ex_data.get("sanity_checks", [])

                    ex_md = [
                        f"### Worked Pedagogical Example: `{ex_id}`",
                        "",
                        "**Problem Statement**:",
                        f"> {ex_stmt}",
                        "",
                        f"**Target Quantity**: `{ex_target}`",
                        "",
                        "#### Systematic Solution",
                    ]
                    for s in ex_steps:
                        s_num = s.get("step_number", 1)
                        s_concept = s.get("principle_applied") or s.get("concept_applied", "")
                        s_eq = s.get("equation") or s.get("equation_latex", "")
                        s_calc = s.get("substitution") or s.get("calculation_details", "")
                        s_res = s.get("intermediate_result", "")
                        ex_md.extend([
                            f"**Step {s_num} ({s_concept})**:",
                            f"$$ {s_eq} $$",
                            f"{s_calc}",
                            f"Result: `{s_res}`",
                            "",
                        ])

                    ex_md.extend([
                        f"**Final Answer**: {ex_ans}",
                        "",
                    ])
                    if ex_traps:
                        ex_md.append("> [!WARNING] **Common Cognitive Traps & Pitfalls**:")
                        for t in ex_traps:
                            ex_md.append(f"> - {t}")
                        ex_md.append("")
                    if ex_sanity:
                        ex_md.append("**Sanity & Consistency Checks**:")
                        for sc in ex_sanity:
                            ex_md.append(f"- {sc}")
                        ex_md.append("")

                    ex_md_str = "\n".join(ex_md)
                    blocks.append(
                        ChapterContentBlock(
                            block_id=f"block-{chapter_id}-{global_order:03d}",
                            block_type=ContentBlockType.WORKED_EXAMPLE,
                            chapter_id=chapter_id,
                            section_id=sec_id,
                            order_in_section=sec_order,
                            payload_id=ex_id,
                            payload_type="WorkedExampleContentRecord",
                            title=f"Worked Example: {ex_id}",
                            rendered_markdown=ex_md_str,
                            trace_class=ClaimTraceClass.GENERATED_AND_VERIFIED,
                            source_atom_ids=[],
                            verification_status=ContentVerificationStatus.VERIFIED,
                            content_hash=self._hash_text(ex_md_str),
                        )
                    )
                    global_order += 1
                    sec_order += 1

            # Misconceptions in this section
            for misc_id in sec.get("misconception_ids", []):
                misc_data = self.load_verified_artifact("misconceptions", misc_id)
                if misc_data:
                    m_cat = misc_data.get("category", "")
                    m_stmt = misc_data.get("incorrect_statement") or misc_data.get("statement", "")
                    m_err = misc_data.get("why_it_fails") or misc_data.get("erroneous_reasoning", "")
                    m_corr = misc_data.get("corrective_explanation") or misc_data.get("correct_physics_explanation", "")
                    m_counter = misc_data.get("supporting_evidence") or misc_data.get("refutation_counterexample", "")
                    m_diag = misc_data.get("diagnostic_symptom") or misc_data.get("diagnostic_check_latex", "")

                    misc_md = [
                        f"### Inoculation Against Misconception: `{misc_id}`",
                        "",
                        f"**Misconception Category**: `{m_cat}`  ",
                        f"**Erroneous Intuition**: *\"{m_stmt}\"*  ",
                        "",
                        "> [!CAUTION] **Flawed Reasoning Mechanism**:",
                        f"> {m_err}",
                        "",
                        "**Physical Truth & Resolution**:",
                        f"{m_corr}",
                        "",
                        "**Refutation Counterexample & Supporting Evidence**:",
                        f"{m_counter}",
                        "",
                    ]
                    if m_diag:
                        misc_md.extend([
                            f"**Diagnostic Symptom**: {m_diag}",
                            "",
                        ])

                    misc_md_str = "\n".join(misc_md)
                    blocks.append(
                        ChapterContentBlock(
                            block_id=f"block-{chapter_id}-{global_order:03d}",
                            block_type=ContentBlockType.MISCONCEPTION,
                            chapter_id=chapter_id,
                            section_id=sec_id,
                            order_in_section=sec_order,
                            payload_id=misc_id,
                            payload_type="MisconceptionContentRecord",
                            title=f"Misconception Inoculation: {misc_id}",
                            rendered_markdown=misc_md_str,
                            trace_class=ClaimTraceClass.SOURCE_DERIVED,
                            source_atom_ids=[],
                            verification_status=ContentVerificationStatus.VERIFIED,
                            content_hash=self._hash_text(misc_md_str),
                        )
                    )
                    global_order += 1
                    sec_order += 1

            # Verified Questions in this section
            for atom_id in sec.get("question_atom_ids", []):
                atom_data = self.load_canonical_atom(atom_id)
                if atom_data:
                    q_payload = atom_data.get("content_payload") or atom_data.get("question") or {}
                    q_stmt = q_payload.get("problem_statement") or q_payload.get("statement", "")
                    q_opts = q_payload.get("options", [])
                    q_ver_answer = atom_data.get("verified_answer") or q_payload.get("verified_answer", "")
                    q_type = q_payload.get("question_type", "SINGLE_CORRECT" if q_opts else "NUMERICAL")

                    prov_list = atom_data.get('provenance', [])
                    prov_title = (prov_list[0].get('source_title') or prov_list[0].get('source_id', 'Canonical KB')) if prov_list else 'Canonical KB'
                    q_md = [
                        f"### Verified JEE Practice Problem: `{atom_id}`",
                        "",
                        f"**Type**: `{q_type}`  ",
                        f"**Provenance Source**: `{prov_title}`  ",
                        "",
                        f"> {q_stmt}",
                        "",
                    ]
                    if q_opts:
                        q_md.append("**Options**:")
                        for opt in q_opts:
                            opt_id = opt.get('identifier') or opt.get('id') or ""
                            opt_txt = opt.get('text', "")
                            q_md.append(f"- **({opt_id})**: {opt_txt}")
                        q_md.append("")

                    q_md.extend([
                        "<details>",
                        "<summary>Click to view independently verified solution key</summary>",
                        "",
                        f"**Verified Answer**: **{q_ver_answer}**  ",
                        f"**Independent Verification Record**: `{atom_data.get('verification_record_id') or atom_data.get('atom_id')}`",
                        "",
                        "</details>",
                        "",
                    ])

                    q_md_str = "\n".join(q_md)
                    blocks.append(
                        ChapterContentBlock(
                            block_id=f"block-{chapter_id}-{global_order:03d}",
                            block_type=ContentBlockType.QUESTION_SET,
                            chapter_id=chapter_id,
                            section_id=sec_id,
                            order_in_section=sec_order,
                            payload_id=atom_id,
                            payload_type="CanonicalQuestionAtom",
                            title=f"Practice Problem: {atom_id}",
                            rendered_markdown=q_md_str,
                            trace_class=ClaimTraceClass.CANONICAL_KB,
                            source_atom_ids=[atom_id],
                            verification_status=ContentVerificationStatus.VERIFIED,
                            content_hash=self._hash_text(q_md_str),
                        )
                    )
                    global_order += 1
                    sec_order += 1

        # 3. Chapter Summary Block
        sum_md = [
            f"## Chapter Summary & Formula Recap: {hero_title}",
            "",
            "### Core Equations & Domains of Validity",
        ]
        all_formulas = spec.get("formula_sequence", [])
        for f in all_formulas:
            f_title = f.get("title", f.get("formula_id"))
            f_eq = f.get("equation_latex", "")
            f_conds = f.get("conditions_of_validity", [])
            sum_md.extend([
                f"- **{f_title}**: $${f_eq}$$",
                f"  *Validity*: {', '.join(f_conds) if f_conds else 'General'}",
            ])
        sum_md.append("")

        sum_md_str = "\n".join(sum_md)
        blocks.append(
            ChapterContentBlock(
                block_id=f"block-{chapter_id}-{global_order:03d}",
                block_type=ContentBlockType.SUMMARY,
                chapter_id=chapter_id,
                section_id="sec-summary",
                order_in_section=1,
                payload_id=f"summary-{chapter_id}",
                payload_type="ChapterSummary",
                title=f"Summary & Revision: {hero_title}",
                rendered_markdown=sum_md_str,
                trace_class=ClaimTraceClass.EDITORIAL_TRANSITION,
                source_atom_ids=[],
                verification_status=ContentVerificationStatus.VERIFIED,
                content_hash=self._hash_text(sum_md_str),
            )
        )

        return blocks

    def save_draft(self, chapter_id: str, blocks: List[ChapterContentBlock]) -> Path:
        """Saves blocks JSON and projected markdown draft."""
        chap_dir = self.drafts_dir / chapter_id
        chap_dir.mkdir(parents=True, exist_ok=True)

        # 1. Blocks JSON
        blocks_data = [b.model_dump(mode="json") for b in blocks]
        blocks_path = chap_dir / f"{chapter_id}_blocks.json"
        with open(blocks_path, "w", encoding="utf-8") as f:
            json.dump(blocks_data, f, indent=2)

        # 2. Projected Markdown
        md_content = "\n\n---\n\n".join(b.rendered_markdown for b in blocks)
        md_path = chap_dir / f"{chapter_id}_draft.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return chap_dir
