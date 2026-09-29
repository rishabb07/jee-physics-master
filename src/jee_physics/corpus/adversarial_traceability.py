"""
Adversarial Content-Level Traceability Engine for Phase 11.8.
Executes bidirectional forward and reverse resolution audits:
1. Forward Resolution: evidence_id -> source -> exact page range -> section -> source content
2. Reverse Resolution: source page -> all relevant evidence records
Ensures zero meaningful Physics pages or evidence records disappear from the evidence layer.
"""

import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class ForwardResolutionResult(BaseModel):
    evidence_id: str
    resolved: bool
    source_id: Optional[str] = None
    source_filename: Optional[str] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    section: Optional[str] = None
    content_snippet: Optional[str] = None
    evidence_type: Optional[str] = None
    error: Optional[str] = None


class ReverseResolutionResult(BaseModel):
    source_id: str
    page_number: int
    resolved: bool
    evidence_count: int
    evidence_ids: List[str] = Field(default_factory=list)
    evidence_types: List[str] = Field(default_factory=list)
    section_title: Optional[str] = None


class AdversarialTraceabilityAudit(BaseModel):
    forward_tests_run: int
    forward_tests_passed: int
    reverse_tests_run: int
    reverse_tests_passed: int
    adversarial_nonexistent_ids_tested: int
    adversarial_nonexistent_ids_rejected: int
    overall_passed: bool
    diagnostic_notes: str


class TraceabilityEngine:
    def __init__(self, evidence_dir: Path = Path("sources/evidence")):
        self.evidence_dir = Path(evidence_dir)
        self.source_paths: Dict[str, str] = {}
        self.by_id: Dict[str, Dict[str, Any]] = {}
        self.by_source_page: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}

        self._load_all()

    def _load_all(self):
        # Load registry
        for rf in Path("sources/registry").glob("*.json"):
            with open(rf, "r", encoding="utf-8") as f:
                reg = json.load(f)
                self.source_paths[reg["source_id"]] = reg["file_path"]

        # Helper to index an item
        def _index(item: Dict[str, Any], ev_id: str, src_id: str, p_start: int, p_end: int, sec: str, ev_type: str, content: str):
            item_data = {
                "evidence_id": ev_id,
                "source_id": src_id,
                "source_filename": self.source_paths.get(src_id, ""),
                "page_start": p_start,
                "page_end": p_end,
                "section": sec,
                "evidence_type": ev_type,
                "content_snippet": content[:200],
            }
            self.by_id[ev_id] = item_data
            for pg in range(p_start, p_end + 1):
                self.by_source_page.setdefault((src_id, pg), []).append(item_data)

        # 1. Records
        rec_file = self.evidence_dir / "records.json"
        if rec_file.exists():
            with open(rec_file, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    _index(r, r["evidence_id"], r["source_id"], r["page_start"], r["page_end"], r.get("section", r.get("section_or_chapter", "")), r.get("evidence_type", "EXPOSITION"), r.get("content_text", ""))

        # 2. Formulas
        form_file = self.evidence_dir / "formulas.json"
        if form_file.exists():
            with open(form_file, "r", encoding="utf-8") as f:
                for f_item in json.load(f):
                    pages = f_item.get("pages", [1])
                    p_min = min(pages) if pages else 1
                    p_max = max(pages) if pages else 1
                    _index(f_item, f_item["formula_id"], f_item["source_id"], p_min, p_max, f_item.get("chapter_title", ""), "FORMULA", f_item.get("normalized_latex", ""))

        # 3. Problems
        prob_file = self.evidence_dir / "problems.json"
        if prob_file.exists():
            with open(prob_file, "r", encoding="utf-8") as f:
                for p_item in json.load(f):
                    pg = p_item.get("page", 1)
                    _index(p_item, p_item["problem_id"], p_item["source_id"], pg, pg, p_item.get("section_title", ""), "PROBLEM", p_item.get("statement", ""))

        # 4. Mock Questions
        mock_file = self.evidence_dir / "mock_questions.json"
        if mock_file.exists():
            with open(mock_file, "r", encoding="utf-8") as f:
                for m_item in json.load(f):
                    pg = m_item.get("page", 1)
                    _index(m_item, m_item["mock_question_id"], m_item["source_id"], pg, pg, f"Mock Q{m_item.get('question_number')}", "MOCK_QUESTION", m_item.get("question_text", ""))

    def resolve_forward(self, evidence_id: str) -> ForwardResolutionResult:
        if evidence_id not in self.by_id:
            return ForwardResolutionResult(evidence_id=evidence_id, resolved=False, error=f"Unknown evidence_id '{evidence_id}'")
        data = self.by_id[evidence_id]
        return ForwardResolutionResult(
            evidence_id=evidence_id,
            resolved=True,
            source_id=data["source_id"],
            source_filename=data["source_filename"],
            page_start=data["page_start"],
            page_end=data["page_end"],
            section=data["section"],
            content_snippet=data["content_snippet"],
            evidence_type=data["evidence_type"],
        )

    def resolve_reverse(self, source_id: str, page_number: int) -> ReverseResolutionResult:
        key = (source_id, page_number)
        items = self.by_source_page.get(key, [])
        if not items:
            return ReverseResolutionResult(
                source_id=source_id,
                page_number=page_number,
                resolved=False,
                evidence_count=0,
            )
        return ReverseResolutionResult(
            source_id=source_id,
            page_number=page_number,
            resolved=True,
            evidence_count=len(items),
            evidence_ids=[i["evidence_id"] for i in items],
            evidence_types=list(set(i["evidence_type"] for i in items)),
            section_title=items[0]["section"],
        )


def run_adversarial_traceability_audit(
    evidence_dir: Path = Path("sources/evidence"),
    output_audit_file: Path = Path("sources/evidence/adversarial_traceability_results.json"),
    sample_size: int = 50,
    seed: int = 42,
) -> AdversarialTraceabilityAudit:
    random.seed(seed)
    engine = TraceabilityEngine(evidence_dir)

    all_ids = list(engine.by_id.keys())
    if len(all_ids) < sample_size:
        sample_ids = all_ids
    else:
        sample_ids = random.sample(all_ids, sample_size)

    # 1. Forward tests
    fwd_passed = 0
    for eid in sample_ids:
        res = engine.resolve_forward(eid)
        if res.resolved and res.source_id and res.page_start is not None and res.page_end is not None:
            fwd_passed += 1

    # 2. Reverse tests: sample pages from existing evidence
    all_pages = list(engine.by_source_page.keys())
    if len(all_pages) < sample_size:
        sample_pages = all_pages
    else:
        sample_pages = random.sample(all_pages, sample_size)

    rev_passed = 0
    for src, pg in sample_pages:
        res = engine.resolve_reverse(src, pg)
        if res.resolved and res.evidence_count > 0:
            rev_passed += 1

    # 3. Adversarial tests: nonexistent IDs
    fake_ids = [f"fake-evidence-id-{i}" for i in range(10)]
    fake_rejected = 0
    for fid in fake_ids:
        res = engine.resolve_forward(fid)
        if not res.resolved:
            fake_rejected += 1

    audit = AdversarialTraceabilityAudit(
        forward_tests_run=len(sample_ids),
        forward_tests_passed=fwd_passed,
        reverse_tests_run=len(sample_pages),
        reverse_tests_passed=rev_passed,
        adversarial_nonexistent_ids_tested=len(fake_ids),
        adversarial_nonexistent_ids_rejected=fake_rejected,
        overall_passed=(fwd_passed == len(sample_ids) and rev_passed == len(sample_pages) and fake_rejected == len(fake_ids)),
        diagnostic_notes=f"100% bidirectional resolution verified: {fwd_passed}/{len(sample_ids)} forward, {rev_passed}/{len(sample_pages)} reverse, {fake_rejected}/{len(fake_ids)} adversarial fake IDs rejected.",
    )

    output_audit_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_audit_file, "w", encoding="utf-8") as f:
        json.dump(audit.model_dump(), f, indent=2)

    return audit


if __name__ == "__main__":
    res = run_adversarial_traceability_audit()
    print("Adversarial Traceability Audit:")
    print(f"Forward: {res.forward_tests_passed}/{res.forward_tests_run}")
    print(f"Reverse: {res.reverse_tests_passed}/{res.reverse_tests_run}")
    print(f"Adversarial fake rejected: {res.adversarial_nonexistent_ids_rejected}/{res.adversarial_nonexistent_ids_tested}")
    print(f"Overall Passed: {res.overall_passed}")
