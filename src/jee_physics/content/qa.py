"""
Independent Chapter QA and LaTeX Rendering Auditor for JEE Physics Master Knowledge System.
Evaluates physics soundness, curriculum blueprint alignment, claim trace integrity,
and LaTeX rendering health.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from jee_physics.content.claim_resolver import ClaimResolver, ClaimResolutionStatus
from jee_physics.models.content import (
    ChapterContentBlock,
    ChapterQAFinding,
    ChapterQAReport,
    ClaimTraceClass,
    ContentVerificationStatus,
    RenderingQAReport,
)


class ChapterQAAuditor:
    """Performs rigorous multi-dimensional QA on assembled chapter drafts."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root

    def lint_latex_math(self, text: str) -> Tuple[int, List[str], List[str]]:
        """
        Lints LaTeX mathematical syntax in text.
        Returns:
            total_expressions, errors, warnings
        """
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Check double dollar $$ balance
        double_dollar_count = text.count("$$")
        if double_dollar_count % 2 != 0:
            errors.append(f"Odd number of display math delimiters ($$): {double_dollar_count}")

        # Remove double dollars to inspect single dollars
        text_without_double = text.replace("$$", " ")

        # 2. Check inline $ balance line by line or paragraph by paragraph
        paragraphs = text_without_double.split("\n\n")
        inline_exprs: List[str] = []

        for p_idx, p in enumerate(paragraphs):
            # Exclude code blocks
            if p.strip().startswith("```"):
                continue
            # Strip inline backticks so code literals don't break inline math parsing
            cleaned_p = re.sub(r"`[^`]*`", " ", p)
            dollar_count = cleaned_p.count("$")
            if dollar_count % 2 != 0:
                errors.append(f"Unbalanced inline dollar delimiter in paragraph {p_idx + 1}")
            else:
                parts = cleaned_p.split("$")
                for i in range(1, len(parts), 2):
                    inline_exprs.append(parts[i])

        # Also extract display math expressions
        display_parts = text.split("$$")
        display_exprs = [display_parts[i] for i in range(1, len(display_parts), 2)]

        all_exprs = inline_exprs + display_exprs
        total_expressions = len(all_exprs)

        # 3. Check brace balancing inside math expressions
        for expr in all_exprs:
            open_braces = expr.count("{")
            close_braces = expr.count("}")
            if open_braces != close_braces:
                errors.append(f"Unbalanced braces in math expression: {expr[:40]}... ({{: {open_braces}, }}: {close_braces})")

            if "%" in expr:
                unescaped_pct = re.findall(r"(?<!\\)%", expr)
                if unescaped_pct:
                    warnings.append(f"Unescaped percent sign in math: {expr[:40]}...")

            if re.search(r"\\frac\s*$", expr):
                errors.append(f"Incomplete \\frac command in math: {expr[:40]}...")

        return total_expressions, errors, warnings

    def audit_chapter(
        self,
        chapter_id: str,
        blocks: List[ChapterContentBlock],
        plan: Dict[str, Any],
        spec: Dict[str, Any],
    ) -> Tuple[ChapterQAReport, RenderingQAReport]:
        """Audits an assembled chapter draft."""
        findings: List[ChapterQAFinding] = []

        physics_passed = True
        curriculum_passed = True
        editorial_passed = True
        pedagogy_passed = True

        all_text_for_latex: List[str] = []
        claim_traces_map: Dict[str, ClaimTraceClass] = {}

        # 1. Audit blocks verification and claim traces
        for b in blocks:
            all_text_for_latex.append(b.rendered_markdown)
            claim_traces_map[b.block_id] = b.trace_class

            if b.verification_status != ContentVerificationStatus.VERIFIED:
                physics_passed = False
                findings.append(
                    ChapterQAFinding(
                        category="PHYSICS",
                        severity="CRITICAL",
                        location=b.block_id,
                        description=f"Block {b.block_id} ('{b.title}') has unverified status: {b.verification_status}",
                        remediation="Route to independent physics verifier before promotion",
                    )
                )

            if not b.trace_class:
                editorial_passed = False
                findings.append(
                    ChapterQAFinding(
                        category="EDITORIAL",
                        severity="WARNING",
                        location=b.block_id,
                        description=f"Block {b.block_id} is missing trace_class",
                        remediation="Assign valid ClaimTraceClass",
                    )
                )

        # 2. Provenance QA via ClaimResolver
        resolver = ClaimResolver(self.workspace_root)
        claim_report = resolver.audit_chapter_blocks(chapter_id, blocks)
        provenance_passed = claim_report.passed
        if not provenance_passed:
            for item in claim_report.items:
                if item.status != ClaimResolutionStatus.RESOLVED:
                    findings.append(
                        ChapterQAFinding(
                            category="PROVENANCE",
                            severity="CRITICAL",
                            location=item.claim_location,
                            description=f"Claim trace issue for '{item.referenced_id}': {item.status.value} - {item.notes}",
                            remediation="Ensure referenced target exists on disk, content hash matches, and status is VERIFIED",
                        )
                    )

        # 3. Audit blueprint coverage
        plan_question_atom_ids = set()
        for sec in plan.get("sections", []):
            plan_question_atom_ids.update(sec.get("question_atom_ids", []))

        block_question_ids = set()
        for b in blocks:
            block_question_ids.update(b.source_atom_ids)

        missing_questions = plan_question_atom_ids - block_question_ids
        if missing_questions:
            curriculum_passed = False
            findings.append(
                ChapterQAFinding(
                    category="CURRICULUM",
                    severity="CRITICAL",
                    location=f"chapter-{chapter_id}",
                    description=f"Draft omitted required questions from blueprint: {missing_questions}",
                    remediation="Ensure all blueprint practice question atoms are assembled into draft",
                )
            )

        # 3. LaTeX Rendering QA
        full_text = "\n\n".join(all_text_for_latex)
        tot_expr, s_err, s_warn = self.lint_latex_math(full_text)

        rendering_passed = (len(s_err) == 0)
        if not rendering_passed:
            findings.append(
                ChapterQAFinding(
                    category="RENDERING",
                    severity="WARNING",
                    location=f"chapter-{chapter_id}",
                    description=f"Found {len(s_err)} LaTeX syntax errors in math expressions",
                    remediation="Balance delimiters and brace nesting",
                )
            )

        rendering_report = RenderingQAReport(
            report_id=f"rendering-qa-{chapter_id}",
            chapter_id=chapter_id,
            latex_errors=s_err,
            broken_references=[],
            empty_sections=[],
            passed=rendering_passed,
            timestamp=datetime.now(timezone.utc),
        )

        critical_count = sum(1 for f in findings if f.severity == "CRITICAL")
        if critical_count > 0:
            overall_verdict = "FAILED"
        elif len(findings) > 0:
            overall_verdict = "NEEDS_REVISION"
        else:
            overall_verdict = "PASSED"

        chapter_qa_report = ChapterQAReport(
            report_id=f"chapter-qa-{chapter_id}",
            chapter_id=chapter_id,
            verdict=overall_verdict,
            physics_passed=physics_passed,
            curriculum_passed=curriculum_passed,
            editorial_passed=editorial_passed,
            pedagogy_passed=pedagogy_passed,
            provenance_passed=provenance_passed,
            findings=findings,
            claim_traces=claim_traces_map,
            timestamp=datetime.now(timezone.utc),
        )

        return chapter_qa_report, rendering_report
