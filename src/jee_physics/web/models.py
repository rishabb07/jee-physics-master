"""
Pydantic data models for the JEE Physics Web Application.
Defines strict schemas for all emitted web JSON datasets.
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field


class WebConceptBlock(BaseModel):
    concept_id: str
    title: str
    statement: str
    physical_intuition: str
    boundary_conditions: List[str] = Field(default_factory=list)
    related_formula_ids: List[str] = Field(default_factory=list)


class WebFormulaBlock(BaseModel):
    formula_id: str
    title: str
    equation_latex: str
    variables: Dict[str, str] = Field(default_factory=dict)
    units: Dict[str, str] = Field(default_factory=dict)
    dimensions: Dict[str, str] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    validity_conditions: List[str] = Field(default_factory=list)
    common_misuse: List[str] = Field(default_factory=list)
    derivation_id: Optional[str] = None


class WebDerivationBlock(BaseModel):
    derivation_id: str
    title: str
    target_formula: str
    assumptions: List[str] = Field(default_factory=list)
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    limiting_cases: List[str] = Field(default_factory=list)


class WebWorkedExampleBlock(BaseModel):
    example_id: str
    problem_statement: str
    diagram_description: Optional[str] = None
    known_parameters: Dict[str, Any] = Field(default_factory=dict)
    target_variable: str = ""
    solution_strategy: str = ""
    solution_steps: List[Dict[str, Any]] = Field(default_factory=list)
    final_answer: str = ""
    trap_alerts: List[str] = Field(default_factory=list)
    sanity_checks: List[str] = Field(default_factory=list)


class WebMisconceptionBlock(BaseModel):
    misconception_id: str
    category: str
    statement: str
    erroneous_reasoning: str
    correct_physics_explanation: str
    refutation_counterexample: str
    diagnostic_check_latex: Optional[str] = None


class WebQuestionBlock(BaseModel):
    question_id: str
    chapter_id: str
    topic_id: str
    question_type: str
    problem_statement: str
    options: Optional[Dict[str, str]] = None
    correct_answer: Union[str, List[str]]
    solution_explanation: str
    difficulty: Dict[str, Any] = Field(default_factory=dict)
    distractor_rationales: Optional[Dict[str, str]] = None
    verification_status: str
    provenance: Optional[Dict[str, Any]] = None


class WebSection(BaseModel):
    section_id: str
    section_order: int
    title: str
    pedagogical_purpose: str = ""
    concepts: List[WebConceptBlock] = Field(default_factory=list)
    formulas: List[WebFormulaBlock] = Field(default_factory=list)
    derivations: List[WebDerivationBlock] = Field(default_factory=list)
    worked_examples: List[WebWorkedExampleBlock] = Field(default_factory=list)
    misconceptions: List[WebMisconceptionBlock] = Field(default_factory=list)
    questions: List[WebQuestionBlock] = Field(default_factory=list)


class WebChapterDetail(BaseModel):
    chapter_id: str
    title: str
    branch: str
    order: int
    status: str  # "PILOT_ACTIVE" | "PENDING"
    learning_objectives: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    sections: List[WebSection] = Field(default_factory=list)
    revision_checklist: List[str] = Field(default_factory=list)
    ladder_ids: List[str] = Field(default_factory=list)


class WebChapterSummary(BaseModel):
    chapter_id: str
    title: str
    branch: str
    order: int
    status: str  # "PILOT_ACTIVE" | "PENDING"
    topic_count: int = 0
    concept_count: int = 0
    formula_count: int = 0
    derivation_count: int = 0
    example_count: int = 0
    misconception_count: int = 0
    question_count: int = 0
    learning_objectives: List[str] = Field(default_factory=list)


class WebTaxonomyTopic(BaseModel):
    topic_id: str
    name: str
    subtopics: List[str] = Field(default_factory=list)


class WebTaxonomyChapter(BaseModel):
    chapter_id: str
    title: str
    branch: str
    order: int
    status: str  # "PILOT_ACTIVE" | "PENDING"
    topics: List[WebTaxonomyTopic] = Field(default_factory=list)


class WebTaxonomyTree(BaseModel):
    branches: List[str] = Field(default_factory=list)
    chapters: List[WebTaxonomyChapter] = Field(default_factory=list)


class WebLadderRung(BaseModel):
    rung_number: int
    rung_name: str
    question_id: str
    physical_delta: str
    reasoning_depth: int
    concepts_involved: List[str] = Field(default_factory=list)
    mathematical_complexity: str


class WebLadder(BaseModel):
    ladder_id: str
    chapter_id: str
    topic_id: str
    title: str
    physical_system: str
    rungs: List[WebLadderRung] = Field(default_factory=list)


class WebSearchItem(BaseModel):
    id: str
    title: str
    entity_type: str  # "chapter" | "concept" | "formula" | "example" | "question" | "misconception"
    chapter_id: str
    chapter_title: str
    snippet: str
    keywords: List[str] = Field(default_factory=list)
    route: str


class WebBuildManifest(BaseModel):
    build_id: str
    build_timestamp: str
    version: str
    git_commit: Optional[str] = "local-uncommitted"
    scope: str
    chapters: List[WebChapterSummary] = Field(default_factory=list)
    counts: Dict[str, int] = Field(default_factory=dict)
    content_hashes: Dict[str, str] = Field(default_factory=dict)
