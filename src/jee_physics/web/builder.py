"""
Web Data Builder for the JEE Physics Master Knowledge System.
Transforms canonical taxonomy, approved curriculum, verified content,
and verified question banks into deterministic web JSON datasets.
"""

import json
import hashlib
import uuid
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
import yaml

from jee_physics.web.models import (
    WebBuildManifest,
    WebChapterSummary,
    WebChapterDetail,
    WebSection,
    WebConceptBlock,
    WebFormulaBlock,
    WebDerivationBlock,
    WebWorkedExampleBlock,
    WebMisconceptionBlock,
    WebQuestionBlock,
    WebTaxonomyTree,
    WebTaxonomyChapter,
    WebTaxonomyTopic,
    WebLadder,
    WebLadderRung,
    WebSearchItem,
)

PILOT_CHAPTER_IDS = [
    "rotational-motion",
    "thermodynamics",
    "current-electricity",
    "ray-optics",
    "kinematics",
    "laws-of-motion",
    "work-energy-power",
]

CHAPTER_BRANCH_MAPPING = {
    "units-and-measurements": "Mechanics",
    "kinematics": "Mechanics",
    "laws-of-motion": "Mechanics",
    "work-energy-power": "Mechanics",
    "center-of-mass": "Mechanics",
    "rotational-motion": "Mechanics",
    "gravitation": "Mechanics",
    "properties-of-solids": "Mechanics",
    "fluid-mechanics": "Mechanics",
    "thermal-physics": "Thermodynamics & Thermal Physics",
    "thermodynamics": "Thermodynamics & Thermal Physics",
    "kinetic-theory-of-gases": "Thermodynamics & Thermal Physics",
    "oscillations": "Oscillations & Waves",
    "waves": "Oscillations & Waves",
    "electrostatics": "Electrodynamics",
    "capacitance": "Electrodynamics",
    "current-electricity": "Electrodynamics",
    "magnetic-effects-of-current": "Electrodynamics",
    "magnetism-and-matter": "Electrodynamics",
    "electromagnetic-induction": "Electrodynamics",
    "alternating-current": "Electrodynamics",
    "electromagnetic-waves": "Electrodynamics",
    "ray-optics": "Optics",
    "wave-optics": "Optics",
    "dual-nature-of-matter-and-radiation": "Modern Physics",
    "atomic-physics": "Modern Physics",
    "nuclear-physics": "Modern Physics",
    "semiconductors": "Modern Physics",
    "communication-systems": "Applied Physics",
    "experimental-physics": "Experimental & Applied Physics",
}


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _tokenize(text: str) -> List[str]:
    clean = re.sub(r"[^\w\s-]", " ", text.lower())
    words = clean.split()
    stop_words = {"the", "a", "an", "is", "in", "and", "or", "of", "to", "for", "with", "on", "at", "by", "from", "as"}
    return [w for w in words if len(w) > 2 and w not in stop_words]


class WebDataBuilder:
    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path.cwd()
        self.kb_dir = self.root_dir / "kb"
        self.curriculum_dir = self.root_dir / "curriculum"
        self.staging_curr_dir = self.root_dir / "build" / "staging" / "incoming" / "curriculum"
        self.content_dir = self.root_dir / "build" / "staging" / "incoming" / "content"
        self.drafts_dir = self.root_dir / "build" / "drafts"
        self.qb_verified_dir = self.root_dir / "question_bank" / "verified"
        self.review_queue_dir = self.root_dir / "review" / "queue" / "questions"

    def build_all(self, target_dir: Optional[Path] = None) -> WebBuildManifest:
        out_dir = target_dir or (self.root_dir / "build" / "web" / "data")
        out_dir.mkdir(parents=True, exist_ok=True)

        taxonomy_tree = self.build_taxonomy(out_dir)
        concepts = self.build_concepts(out_dir)
        formulas = self.build_formulas(out_dir)
        derivations = self.load_derivations()
        examples = self.load_examples()
        misconceptions = self.load_misconceptions()
        questions = self.build_questions(out_dir)
        ladders = self.build_ladders(out_dir)
        prerequisites = self.build_prerequisites(out_dir)

        chapters_detail, chapters_summary = self.build_chapters(
            out_dir, taxonomy_tree, concepts, formulas, derivations, examples, misconceptions, questions, ladders
        )

        search_items = self.build_search_index(
            out_dir, taxonomy_tree, chapters_detail, concepts, formulas, derivations, examples, misconceptions, questions
        )

        # Build manifest
        content_hashes = {}
        for path in out_dir.glob("*.json"):
            if path.name != "manifest.json":
                content_hashes[path.name] = _sha256(path.read_text(encoding="utf-8"))

        def _get_git_commit(rdir: Path) -> str:
            try:
                import subprocess
                res = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(rdir), capture_output=True, text=True)
                if res.returncode == 0 and res.stdout.strip():
                    return res.stdout.strip()
            except Exception:
                pass
            return "local-uncommitted"

        manifest = WebBuildManifest(
            build_id=str(uuid.uuid4()),
            build_timestamp=datetime.now(timezone.utc).isoformat(),
            version="1.0.0-pilot",
            git_commit=_get_git_commit(self.root_dir),
            scope="PILOT",
            chapters=chapters_summary,
            counts={
                "total_chapters": len(chapters_summary),
                "pilot_active_chapters": len([c for c in chapters_summary if c.status == "PILOT_ACTIVE"]),
                "concepts": len(concepts),
                "formulas": len(formulas),
                "derivations": len(derivations),
                "worked_examples": len(examples),
                "misconceptions": len(misconceptions),
                "verified_questions": len(questions),
                "question_ladders": len(ladders),
                "search_index_entries": len(search_items),
            },
            content_hashes=content_hashes,
        )

        manifest_path = out_dir / "manifest.json"
        manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        return manifest

    def build_taxonomy(self, out_dir: Path) -> WebTaxonomyTree:
        syllabus_file = self.kb_dir / "taxonomy" / "syllabus.yaml"
        with open(syllabus_file, "r", encoding="utf-8") as f:
            tax_raw = yaml.safe_load(f)

        branches_set = set(CHAPTER_BRANCH_MAPPING.values())
        raw_chapters = tax_raw.get("chapters", {})
        taxonomy_chapters: List[WebTaxonomyChapter] = []

        for idx, (ch_id, ch_info) in enumerate(raw_chapters.items(), start=1):
            branch = CHAPTER_BRANCH_MAPPING.get(ch_id, "General Physics")
            status = "PILOT_ACTIVE" if ch_id in PILOT_CHAPTER_IDS else "PENDING"
            topics_list: List[WebTaxonomyTopic] = []

            for topic_id, topic_info in ch_info.get("topics", {}).items():
                subtopics = topic_info.get("subtopics", [])
                topics_list.append(
                    WebTaxonomyTopic(
                        topic_id=topic_id,
                        name=topic_info.get("title", topic_id.replace("-", " ").title()),
                        subtopics=subtopics,
                    )
                )

            taxonomy_chapters.append(
                WebTaxonomyChapter(
                    chapter_id=ch_id,
                    title=ch_info.get("title", ch_id.replace("-", " ").title()),
                    branch=branch,
                    order=idx,
                    status=status,
                    topics=topics_list,
                )
            )

        taxonomy_tree = WebTaxonomyTree(
            branches=sorted(list(branches_set)),
            chapters=taxonomy_chapters,
        )

        tax_path = out_dir / "taxonomy.json"
        tax_path.write_text(taxonomy_tree.model_dump_json(indent=2), encoding="utf-8")
        return taxonomy_tree

    def build_concepts(self, out_dir: Path) -> List[WebConceptBlock]:
        concepts_dir = self.content_dir / "concepts"
        concepts: List[WebConceptBlock] = []

        if concepts_dir.exists():
            for p in sorted(concepts_dir.glob("*.json")):
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                c = WebConceptBlock(
                    concept_id=d.get("content_id", p.stem),
                    title=d.get("title", p.stem.replace("-", " ").title()),
                    statement=d.get("explanation") or d.get("formal_definition") or "",
                    physical_intuition=d.get("intuition", ""),
                    boundary_conditions=d.get("boundary_conditions", []),
                    related_formula_ids=d.get("related_formula_ids", []),
                )
                concepts.append(c)

        out_path = out_dir / "concepts.json"
        out_path.write_text(json.dumps([c.model_dump() for c in concepts], indent=2), encoding="utf-8")
        return concepts

    def build_formulas(self, out_dir: Path) -> List[WebFormulaBlock]:
        formulas_dir = self.content_dir / "formulas"
        formulas: List[WebFormulaBlock] = []

        if formulas_dir.exists():
            for p in sorted(formulas_dir.glob("*.json")):
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                formula = WebFormulaBlock(
                    formula_id=d.get("formula_id", p.stem),
                    title=d.get("title", p.stem.replace("-", " ").title()),
                    equation_latex=d.get("equation_latex") or d.get("equation") or "",
                    variables=d.get("variables", {}),
                    units=d.get("units", {}),
                    dimensions=d.get("dimensions", {}),
                    assumptions=d.get("assumptions", []),
                    validity_conditions=d.get("validity_conditions", []),
                    common_misuse=d.get("common_misuse", []),
                    derivation_id=d.get("derivation_reference"),
                )
                formulas.append(formula)

        out_path = out_dir / "formulas.json"
        out_path.write_text(json.dumps([f.model_dump() for f in formulas], indent=2), encoding="utf-8")
        return formulas

    def load_derivations(self) -> List[WebDerivationBlock]:
        derivations_dir = self.content_dir / "derivations"
        derivations: List[WebDerivationBlock] = []

        if derivations_dir.exists():
            for p in sorted(derivations_dir.glob("*.json")):
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                deriv = WebDerivationBlock(
                    derivation_id=d.get("derivation_id", p.stem),
                    title=f"Derivation: {d.get('target_formula_id', p.stem)}",
                    target_formula=d.get("target_equation", d.get("final_equation", "")),
                    assumptions=d.get("assumptions", []),
                    steps=d.get("ordered_steps", []),
                    limiting_cases=d.get("applicability_conditions", []),
                )
                derivations.append(deriv)
        return derivations

    def load_examples(self) -> List[WebWorkedExampleBlock]:
        examples_dir = self.content_dir / "examples"
        examples: List[WebWorkedExampleBlock] = []

        if examples_dir.exists():
            for p in sorted(examples_dir.glob("*.json")):
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                steps = d.get("solution_steps") or d.get("ordered_steps") or []
                ex = WebWorkedExampleBlock(
                    example_id=d.get("example_id", p.stem),
                    problem_statement=d.get("problem_statement", ""),
                    diagram_description=d.get("diagram_description"),
                    known_parameters=d.get("known_parameters") or d.get("known_quantities") or {},
                    target_variable=d.get("target_variable") or d.get("target_quantity") or "",
                    solution_strategy=d.get("solution_strategy", ""),
                    solution_steps=steps,
                    final_answer=d.get("final_answer", ""),
                    trap_alerts=d.get("trap_alerts", []),
                    sanity_checks=d.get("sanity_checks", []),
                )
                examples.append(ex)
        return examples

    def load_misconceptions(self) -> List[WebMisconceptionBlock]:
        misconceptions_dir = self.content_dir / "misconceptions"
        misconceptions: List[WebMisconceptionBlock] = []

        if misconceptions_dir.exists():
            for p in sorted(misconceptions_dir.glob("*.json")):
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                misc = WebMisconceptionBlock(
                    misconception_id=d.get("misconception_id", p.stem),
                    category=d.get("category", "GENERAL_MISCONCEPTION"),
                    statement=d.get("statement") or d.get("incorrect_statement") or "",
                    erroneous_reasoning=d.get("erroneous_reasoning") or d.get("why_it_fails") or "",
                    correct_physics_explanation=d.get("correct_physics_explanation") or d.get("corrective_explanation") or "",
                    refutation_counterexample=d.get("refutation_counterexample") or d.get("supporting_evidence") or "",
                    diagnostic_check_latex=d.get("diagnostic_check_latex") or d.get("diagnostic_symptom"),
                )
                misconceptions.append(misc)
        return misconceptions

    def build_questions(self, out_dir: Path) -> List[WebQuestionBlock]:
        questions: List[WebQuestionBlock] = []
        excluded_ids: Set[str] = set()

        # Gather excluded review queue questions
        if self.review_queue_dir.exists():
            for rq in self.review_queue_dir.glob("*.json"):
                try:
                    data = json.loads(rq.read_text(encoding="utf-8"))
                    qid = data.get("question_id") or data.get("staged_question", {}).get("question_id")
                    if qid:
                        excluded_ids.add(qid)
                except Exception:
                    pass

        # 1. Ingest verified question bank items
        qb_dirs = [
            self.qb_verified_dir,
            self.root_dir / "build" / "staging" / "incoming" / "question_bank" / "verified",
            self.root_dir / "content" / "verified" / "questions",
        ]
        seen_qids: Set[str] = set()
        for qb_dir in qb_dirs:
            if qb_dir.exists():
                for p in sorted(qb_dir.glob("*.json")):
                    with open(p, "r", encoding="utf-8") as f:
                        d = json.load(f)
                    qid = d.get("question_id", p.stem)
                    if qid in excluded_ids or qid in seen_qids:
                        continue  # Inviolate: zero review queue items
                    if d.get("verification_status") != "VERIFIED":
                        continue  # Must be strictly verified
                    seen_qids.add(qid)

                    tax_ref = d.get("taxonomy_reference", {})
                    ch_id = tax_ref.get("chapter_id", d.get("chapter_id", "general-physics"))
                    topic_id = tax_ref.get("topic_id", d.get("topic_id", "general"))

                    # Distractor rationales formatting
                    dr_map = {}
                    raw_dr = d.get("distractor_rationales")
                    if isinstance(raw_dr, list):
                        for item in raw_dr:
                            opt_key = item.get("option_key", "")
                            rationale = item.get("student_rationale") or item.get("physical_error") or ""
                            if opt_key:
                                dr_map[opt_key] = rationale
                    elif isinstance(raw_dr, dict):
                        dr_map = raw_dr

                    q = WebQuestionBlock(
                        question_id=qid,
                        chapter_id=ch_id,
                        topic_id=topic_id,
                        question_type=d.get("question_type", "MCQ"),
                        problem_statement=d.get("statement") or d.get("problem_statement", ""),
                        options=d.get("options"),
                        correct_answer=d.get("correct_answer", ""),
                        solution_explanation=d.get("solution", d.get("explanation", d.get("solution_strategy", ""))),
                        difficulty=d.get("difficulty_dimensions", {}),
                        distractor_rationales=dr_map if dr_map else None,
                        verification_status="VERIFIED",
                        provenance=d.get("source_grounding") or {"origin": "VERIFIED_QUESTION_BANK"},
                    )
                    questions.append(q)

        # 2. Ingest canonical verified atoms for active pilot chapters
        atoms_dir = self.kb_dir / "atoms"
        if atoms_dir.exists():
            for p in sorted(atoms_dir.glob("*.json")):
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                if d.get("atom_type") != "question":
                    continue
                if d.get("verification_status") != "VERIFIED":
                    continue
                qid = d.get("atom_id", p.stem)
                if qid in excluded_ids:
                    continue

                tax = d.get("taxonomy", {})
                ch_id = tax.get("chapter_id", "")
                if ch_id not in PILOT_CHAPTER_IDS:
                    continue  # Only include pilot chapters for initial publication

                q_data = d.get("question", {})
                options_dict = {}
                for opt in q_data.get("options", []):
                    if isinstance(opt, dict) and "id" in opt and "text" in opt:
                        options_dict[opt["id"]] = opt["text"]

                correct_ans = q_data.get("verified_answer") or q_data.get("source_claimed_answer") or q_data.get("answer") or ""
                solution_text = q_data.get("source_solution") or f"Verified Answer: {correct_ans}"

                canonical_q = WebQuestionBlock(
                    question_id=qid,
                    chapter_id=ch_id,
                    topic_id=tax.get("topic_id", "general"),
                    question_type="SINGLE_CORRECT_MCQ" if options_dict else "NUMERICAL",
                    problem_statement=q_data.get("statement", d.get("title", "")),
                    options=options_dict if options_dict else None,
                    correct_answer=correct_ans,
                    solution_explanation=solution_text,
                    difficulty={"difficulty_band": q_data.get("difficulty", "L2")},
                    distractor_rationales=None,
                    verification_status="VERIFIED",
                    provenance={"origin": "CANONICAL_SOURCE", "exam_metadata": q_data.get("exam_metadata")},
                )
                questions.append(canonical_q)

        out_path = out_dir / "questions.json"
        out_path.write_text(json.dumps([q.model_dump() for q in questions], indent=2), encoding="utf-8")
        return questions

    def build_ladders(self, out_dir: Path) -> List[WebLadder]:
        ladders: List[WebLadder] = []
        ladder_dirs = [
            self.staging_curr_dir / "ladders",
            self.curriculum_dir / "ladders",
        ]
        seen_ladders = set()

        for ldir in ladder_dirs:
            if ldir.exists():
                for p in sorted(ldir.glob("*.json")):
                    if p.name in seen_ladders:
                        continue
                    seen_ladders.add(p.name)
                    with open(p, "r", encoding="utf-8") as f:
                        d = json.load(f)

                    rungs = []
                    for r in d.get("rungs", []):
                        rungs.append(
                            WebLadderRung(
                                rung_number=r.get("level", 1),
                                rung_name=r.get("level_name", f"Level {r.get('level', 1)}"),
                                question_id=r.get("atom_id", ""),
                                physical_delta=r.get("physical_delta", ""),
                                reasoning_depth=r.get("reasoning_depth", 1),
                                concepts_involved=r.get("concepts_involved", []),
                                mathematical_complexity=r.get("mathematical_complexity", ""),
                            )
                        )

                    ladder = WebLadder(
                        ladder_id=d.get("ladder_id", p.stem),
                        chapter_id=d.get("chapter_id", "rotational-motion"),
                        topic_id=d.get("topic_id", "general"),
                        title=d.get("title", p.stem.replace("-", " ").title()),
                        physical_system=d.get("physical_system", ""),
                        rungs=rungs,
                    )
                    ladders.append(ladder)

        out_path = out_dir / "ladders.json"
        out_path.write_text(json.dumps([l.model_dump() for l in ladders], indent=2), encoding="utf-8")
        return ladders

    def build_prerequisites(self, out_dir: Path) -> Dict[str, Any]:
        prereq_file = self.curriculum_dir / "prerequisite_graph.json"
        data = {}
        if prereq_file.exists():
            with open(prereq_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        out_path = out_dir / "prerequisites.json"
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data

    def build_chapters(
        self,
        out_dir: Path,
        taxonomy_tree: WebTaxonomyTree,
        concepts: List[WebConceptBlock],
        formulas: List[WebFormulaBlock],
        derivations: List[WebDerivationBlock],
        examples: List[WebWorkedExampleBlock],
        misconceptions: List[WebMisconceptionBlock],
        questions: List[WebQuestionBlock],
        ladders: List[WebLadder],
    ):
        concepts_by_id = {c.concept_id: c for c in concepts}
        formulas_by_id = {f.formula_id: f for f in formulas}
        derivations_by_id = {d.derivation_id: d for d in derivations}
        examples_by_id = {e.example_id: e for e in examples}
        misconceptions_by_id = {m.misconception_id: m for m in misconceptions}
        questions_by_id = {q.question_id: q for q in questions}

        chapters_detail: List[WebChapterDetail] = []
        chapters_summary: List[WebChapterSummary] = []

        for tax_ch in taxonomy_tree.chapters:
            ch_id = tax_ch.chapter_id
            spec_file = self.staging_curr_dir / f"{ch_id}_spec.json"
            if not spec_file.exists():
                spec_file = self.curriculum_dir / "chapters" / f"{ch_id}_spec.json"
            plan_file = self.staging_curr_dir / f"{ch_id}_plan.json"
            if not plan_file.exists():
                plan_file = self.curriculum_dir / "chapters" / f"{ch_id}_plan.json"
            draft_blocks_file = self.drafts_dir / ch_id / f"{ch_id}_blocks.json"

            if ch_id in PILOT_CHAPTER_IDS and spec_file.exists():
                with open(spec_file, "r", encoding="utf-8") as f:
                    spec = json.load(f)
                plan = {}
                if plan_file.exists():
                    with open(plan_file, "r", encoding="utf-8") as f:
                        plan = json.load(f)

                # Assemble structured sections from ChapterPlan
                sections: List[WebSection] = []
                sec_plans = plan.get("sections", [])

                for s_idx, sp in enumerate(sec_plans, start=1):
                    sec_concepts = [concepts_by_id[cid] for cid in sp.get("concepts", []) if cid in concepts_by_id]
                    sec_formulas = [formulas_by_id[fid] for fid in sp.get("formula_ids", []) if fid in formulas_by_id]
                    
                    # Associate derivations belonging to formulas in this section
                    sec_derivations = []
                    for sf in sec_formulas:
                        if sf.derivation_id and sf.derivation_id in derivations_by_id:
                            sec_derivations.append(derivations_by_id[sf.derivation_id])

                    sec_examples = [examples_by_id[eid] for eid in sp.get("worked_example_ids", []) if eid in examples_by_id]
                    sec_misconceptions = [misconceptions_by_id[mid] for mid in sp.get("misconception_ids", []) if mid in misconceptions_by_id]
                    sec_questions = [questions_by_id[qid] for qid in sp.get("question_atom_ids", []) if qid in questions_by_id]

                    sections.append(
                        WebSection(
                            section_id=sp.get("section_id", f"sec-{s_idx}"),
                            section_order=s_idx,
                            title=sp.get("title", f"Section {s_idx}"),
                            pedagogical_purpose=sp.get("pedagogical_purpose", ""),
                            concepts=sec_concepts,
                            formulas=sec_formulas,
                            derivations=sec_derivations,
                            worked_examples=sec_examples,
                            misconceptions=sec_misconceptions,
                            questions=sec_questions,
                        )
                    )

                # Fallback if no sections in plan: create default section from spec
                if not sections:
                    ch_concepts = [c for c in concepts if ch_id in c.concept_id]
                    ch_formulas = [f for f in formulas if ch_id in f.formula_id]
                    ch_derivs = [d for d in derivations if ch_id in d.derivation_id]
                    ch_ex = [e for e in examples if ch_id in e.example_id]
                    ch_misc = [m for m in misconceptions if ch_id in m.misconception_id]
                    ch_q = [q for q in questions if q.chapter_id == ch_id]
                    sections.append(
                        WebSection(
                            section_id="sec-1",
                            section_order=1,
                            title="Core Concepts and Practice",
                            pedagogical_purpose="Core instructional section",
                            concepts=ch_concepts,
                            formulas=ch_formulas,
                            derivations=ch_derivs,
                            worked_examples=ch_ex,
                            misconceptions=ch_misc,
                            questions=ch_q,
                        )
                    )

                ch_ladders = [l.ladder_id for l in ladders if l.chapter_id == ch_id]

                # Chapter Detail
                ch_detail = WebChapterDetail(
                    chapter_id=ch_id,
                    title=spec.get("chapter_title", tax_ch.title),
                    branch=tax_ch.branch,
                    order=tax_ch.order,
                    status="PILOT_ACTIVE",
                    learning_objectives=spec.get("learning_objectives", []),
                    prerequisites=spec.get("prerequisite_curriculum_nodes", []),
                    sections=sections,
                    revision_checklist=spec.get("revision_checklist", []),
                    ladder_ids=ch_ladders,
                )

                # Save individual chapter JSON
                ch_file = out_dir / f"chapter_{ch_id}.json"
                ch_file.write_text(ch_detail.model_dump_json(indent=2), encoding="utf-8")
                chapters_detail.append(ch_detail)

                # Dual compatibility: if laws-of-motion, also emit chapter_dynamics.json
                if ch_id == "laws-of-motion":
                    dyn_file = out_dir / "chapter_dynamics.json"
                    dyn_file.write_text(ch_detail.model_dump_json(indent=2), encoding="utf-8")
                if ch_id == "work-energy-power":
                    wep_file = out_dir / "chapter_wep.json"
                    wep_file.write_text(ch_detail.model_dump_json(indent=2), encoding="utf-8")

                # Chapter Summary
                tot_concepts = sum(len(s.concepts) for s in sections)
                tot_formulas = sum(len(s.formulas) for s in sections)
                tot_derivations = sum(len(s.derivations) for s in sections)
                tot_examples = sum(len(s.worked_examples) for s in sections)
                tot_misc = sum(len(s.misconceptions) for s in sections)
                tot_q = sum(len(s.questions) for s in sections)

                ch_summary = WebChapterSummary(
                    chapter_id=ch_id,
                    title=spec.get("chapter_title", tax_ch.title),
                    branch=tax_ch.branch,
                    order=tax_ch.order,
                    status="PILOT_ACTIVE",
                    topic_count=len(tax_ch.topics),
                    concept_count=tot_concepts,
                    formula_count=tot_formulas,
                    derivation_count=tot_derivations,
                    example_count=tot_examples,
                    misconception_count=tot_misc,
                    question_count=tot_q,
                    learning_objectives=spec.get("learning_objectives", []),
                )
                chapters_summary.append(ch_summary)
            else:
                # Pending Chapter
                ch_summary = WebChapterSummary(
                    chapter_id=ch_id,
                    title=tax_ch.title,
                    branch=tax_ch.branch,
                    order=tax_ch.order,
                    status="PENDING",
                    topic_count=len(tax_ch.topics),
                    concept_count=0,
                    formula_count=0,
                    derivation_count=0,
                    example_count=0,
                    misconception_count=0,
                    question_count=0,
                    learning_objectives=[],
                )
                chapters_summary.append(ch_summary)

        # Write chapters.json summary
        ch_sum_path = out_dir / "chapters.json"
        ch_sum_path.write_text(json.dumps([c.model_dump() for c in chapters_summary], indent=2), encoding="utf-8")
        return chapters_detail, chapters_summary

    def build_search_index(
        self,
        out_dir: Path,
        taxonomy_tree: WebTaxonomyTree,
        chapters: List[WebChapterDetail],
        concepts: List[WebConceptBlock],
        formulas: List[WebFormulaBlock],
        derivations: List[WebDerivationBlock],
        examples: List[WebWorkedExampleBlock],
        misconceptions: List[WebMisconceptionBlock],
        questions: List[WebQuestionBlock],
    ) -> List[WebSearchItem]:
        items: List[WebSearchItem] = []
        chapter_titles = {ch.chapter_id: ch.title for ch in taxonomy_tree.chapters}

        def _resolve_chapter(item_id: str, fallback_ch: str = "") -> Tuple[str, str]:
            if fallback_ch in {"wep", "work-energy", "work-energy-power"}:
                return "work-energy-power", chapter_titles.get("work-energy-power", "Work, Energy and Power")
            if fallback_ch in {"dynamics", "laws-of-motion"}:
                return "laws-of-motion", chapter_titles.get("laws-of-motion", "Laws of Motion")
            if fallback_ch and fallback_ch in chapter_titles:
                return fallback_ch, chapter_titles[fallback_ch]
            tokens = item_id.split("-")
            for t in tokens:
                if t in {"wep", "work", "energy", "power"}:
                    return "work-energy-power", chapter_titles.get("work-energy-power", "Work, Energy and Power")
                if t in {"kin", "kinematics"}:
                    return "kinematics", chapter_titles.get("kinematics", "Kinematics")
                if t in {"dyn", "dynamics", "motion"}:
                    return "laws-of-motion", chapter_titles.get("laws-of-motion", "Laws of Motion")
                if t in {"rot", "rotational"}:
                    return "rotational-motion", chapter_titles.get("rotational-motion", "Rotational Motion")
                if t in {"td", "thermo", "thermodynamics"}:
                    return "thermodynamics", chapter_titles.get("thermodynamics", "Thermodynamics")
                if t in {"curr", "current"}:
                    return "current-electricity", chapter_titles.get("current-electricity", "Current Electricity")
                if t in {"opt", "optics", "ray"}:
                    return "ray-optics", chapter_titles.get("ray-optics", "Ray Optics")
            return fallback_ch or "", chapter_titles.get(fallback_ch, "")

        # 1. Chapters
        for ch in taxonomy_tree.chapters:
            text = f"{ch.title} {ch.branch} {' '.join(t.name for t in ch.topics)}"
            items.append(
                WebSearchItem(
                    id=ch.chapter_id,
                    title=ch.title,
                    entity_type="chapter",
                    chapter_id=ch.chapter_id,
                    chapter_title=ch.title,
                    snippet=f"Branch: {ch.branch} | Topics: {len(ch.topics)} | Status: {ch.status}",
                    keywords=_tokenize(text),
                    route=f"#/chapter/{ch.chapter_id}",
                )
            )

        # 2. Concepts
        for c in concepts:
            ch_id, ch_title = _resolve_chapter(c.concept_id)
            text = f"{c.title} {c.statement} {c.physical_intuition}"
            items.append(
                WebSearchItem(
                    id=c.concept_id,
                    title=c.title,
                    entity_type="concept",
                    chapter_id=ch_id,
                    chapter_title=ch_title or c.title,
                    snippet=c.statement[:160] + "..." if len(c.statement) > 160 else c.statement,
                    keywords=_tokenize(f"{text} {ch_title} {ch_id}"),
                    route=f"#/concept/{c.concept_id}",
                )
            )

        # 3. Formulas
        for f in formulas:
            ch_id, ch_title = _resolve_chapter(f.formula_id, getattr(f, "chapter_id", ""))
            text = f"{f.title} {f.equation_latex} {' '.join(f.variables.keys())} {' '.join(f.variables.values())}"
            items.append(
                WebSearchItem(
                    id=f.formula_id,
                    title=f.title,
                    entity_type="formula",
                    chapter_id=ch_id,
                    chapter_title=ch_title or f.title,
                    snippet=f"Equation: {f.equation_latex} | Assumptions: {', '.join(f.assumptions[:2])}",
                    keywords=_tokenize(f"{text} {ch_title} {ch_id}"),
                    route=f"#/formulas?id={f.formula_id}",
                )
            )

        # 4. Derivations
        for d in derivations:
            ch_id, ch_title = _resolve_chapter(d.derivation_id)
            step_texts = []
            for s in d.steps:
                if isinstance(s, dict):
                    eq = s.get("equation_latex") or s.get("step_equation") or ""
                    exp = s.get("explanation") or s.get("step_description") or s.get("justification") or ""
                else:
                    eq = getattr(s, "equation_latex", "") or ""
                    exp = getattr(s, "explanation", "") or ""
                step_texts.append(f"{eq} {exp}".strip())
            steps_text = " ".join(step_texts)
            text = f"{d.title} {d.target_formula} {steps_text}"
            items.append(
                WebSearchItem(
                    id=d.derivation_id,
                    title=f"Derivation: {d.title}",
                    entity_type="derivation",
                    chapter_id=ch_id,
                    chapter_title=ch_title or d.title,
                    snippet=f"Proof of {d.target_formula} ({len(d.steps)} steps)",
                    keywords=_tokenize(f"{text} {ch_title} {ch_id}"),
                    route=f"#/chapter/{ch_id}",
                )
            )

        # 5. Worked Examples
        for ex in examples:
            ch_id, ch_title = _resolve_chapter(ex.example_id, getattr(ex, "chapter_id", ""))
            text = f"{ex.problem_statement} {ex.solution_strategy} {ex.final_answer}"
            items.append(
                WebSearchItem(
                    id=ex.example_id,
                    title=f"Worked Example: {ex.example_id}",
                    entity_type="example",
                    chapter_id=ch_id,
                    chapter_title=ch_title or ex.example_id,
                    snippet=ex.problem_statement[:160] + "...",
                    keywords=_tokenize(f"{text} {ch_title} {ch_id}"),
                    route=f"#/chapter/{ch_id}",
                )
            )

        # 6. Misconceptions
        for m in misconceptions:
            ch_id, ch_title = _resolve_chapter(m.misconception_id, getattr(m, "chapter_id", ""))
            text = f"{m.statement} {m.erroneous_reasoning} {m.correct_physics_explanation}"
            items.append(
                WebSearchItem(
                    id=m.misconception_id,
                    title=f"Misconception: {m.category}",
                    entity_type="misconception",
                    chapter_id=ch_id,
                    chapter_title=ch_title or m.category,
                    snippet=m.statement[:160] + "...",
                    keywords=_tokenize(f"{text} {ch_title} {ch_id}"),
                    route=f"#/chapter/{ch_id}",
                )
            )

        # 7. Questions
        for q in questions:
            ch_id, ch_title = _resolve_chapter(q.question_id, q.chapter_id)
            text = f"{q.problem_statement} {q.solution_explanation}"
            items.append(
                WebSearchItem(
                    id=q.question_id,
                    title=f"Question: {q.question_id}",
                    entity_type="question",
                    chapter_id=ch_id,
                    chapter_title=ch_title or q.chapter_id.replace("-", " ").title(),
                    snippet=q.problem_statement[:160] + "...",
                    keywords=_tokenize(f"{text} {ch_title} {ch_id}"),
                    route=f"#/practice?q={q.question_id}",
                )
            )

        search_path = out_dir / "search_index.json"
        search_path.write_text(json.dumps([item.model_dump() for item in items], indent=2), encoding="utf-8")
        return items
