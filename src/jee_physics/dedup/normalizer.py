import hashlib
import re
import unicodedata
from typing import Any, Dict, List, Optional, Tuple

from jee_physics.models.atom import KnowledgeAtom, QuestionOption
from jee_physics.models.dedup import NormalizedAtomFingerprint


# Harmless boilerplate prefixes or suffixes commonly introduced in exams/question banks
BOILERPLATE_PATTERNS = [
    re.compile(r"^(select|choose|mark)\s+the\s+correct\s+(option|choice|statement|alternative)[\.\:\;\-]?\s*", re.IGNORECASE),
    re.compile(r"^(in\s+the\s+given\s+question[,\s]*)", re.IGNORECASE),
    re.compile(r"\s*\(?(choose\s+the\s+correct\s+option|select\s+one)\)?[\.\:]?\s*$", re.IGNORECASE),
    re.compile(r"^\s*Question\s*\d+[\.\:\)]\s*", re.IGNORECASE),
    re.compile(r"^\s*Q\s*\d+[\.\:\)]\s*", re.IGNORECASE),
]

# Option prefix patterns like "(A) ", "A. ", "A) ", "[A] "
OPTION_PREFIX_PATTERN = re.compile(r"^\s*[\(\[]?([A-Da-d1-4])[\)\]\.\:\-]\s*")

# Common physics target phrases
PHYSICS_TARGET_TERMS = [
    ("time period", "time_period"),
    ("frequency", "frequency"),
    ("wavelength", "wavelength"),
    ("moment of inertia", "moment_of_inertia"),
    ("magnetic field", "magnetic_field"),
    ("magnetic moment", "magnetic_moment"),
    ("electric field", "electric_field"),
    ("electrostatic potential", "potential"),
    ("potential difference", "potential_difference"),
    ("capacitance", "capacitance"),
    ("current", "current"),
    ("resistance", "resistance"),
    ("drift velocity", "drift_velocity"),
    ("velocity", "velocity"),
    ("speed", "speed"),
    ("acceleration", "acceleration"),
    ("angular acceleration", "angular_acceleration"),
    ("angular velocity", "angular_velocity"),
    ("angular momentum", "angular_momentum"),
    ("torque", "torque"),
    ("force", "force"),
    ("tension", "tension"),
    ("work done", "work_done"),
    ("kinetic energy", "kinetic_energy"),
    ("potential energy", "potential_energy"),
    ("power", "power"),
    ("temperature", "temperature"),
    ("pressure", "pressure"),
    ("volume", "volume"),
    ("heat", "heat"),
    ("efficiency", "efficiency"),
    ("decay constant", "decay_constant"),
    ("half life", "half_life"),
    ("activity", "activity"),
    ("fringe width", "fringe_width"),
    ("refractive index", "refractive_index"),
    ("focal length", "focal_length"),
]


def normalize_unicode_and_symbols(text: str) -> str:
    """Normalize unicode characters, mathematical dashes, quotes, and symbols."""
    if not text:
        return ""
    # NFKC normalizes compatibility characters
    text = unicodedata.normalize("NFKC", text)

    # Standardize unicode dashes and minus signs
    text = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]", "-", text)

    # Standardize quotes
    text = re.sub(r"[\u2018\u2019\u201A\u201B]", "'", text)
    text = re.sub(r"[\u201C\u201D\u201E\u201F]", '"', text)

    # Standardize multiplication sign
    text = re.sub(r"\u00D7", r"\\times", text)

    # Standardize Greek micro symbol
    text = re.sub(r"[\u03BC\u00B5]", r"\\mu", text)

    # Standardize degree symbol
    text = re.sub(r"\u00B0", r"^{\\circ}", text)

    # Non-breaking and special spaces
    text = re.sub(r"[\u00A0\u2000-\u200B\u202F\u205F\u3000]", " ", text)

    return text


def normalize_latex(text: str) -> str:
    """Standardize LaTeX math delimiters, font commands, and spacing."""
    if not text:
        return ""

    # Replace \( and \) with $
    text = re.sub(r"\\\(", "$", text)
    text = re.sub(r"\\\)", "$", text)

    # Replace \[ and \] with $$
    text = re.sub(r"\\\[", "$$", text)
    text = re.sub(r"\\\]", "$$", text)

    # Standardize \rm, \mathrm, \text inside math
    # e.g. \rm{s} -> \text{s}, \mathrm{s} -> \text{s}
    text = re.sub(r"\\(?:mathrm|rm)\b", r"\\text", text)

    # Collapse internal whitespace in math delimiters: $  x  $ -> $x$
    def _clean_inline_math(match: re.Match) -> str:
        content = match.group(1).strip()
        # Clean extra spaces inside math commands: \text{ s} -> \text{s}
        content = re.sub(r"\\text\{\s+", r"\\text{", content)
        content = re.sub(r"\s+\}", r"}", content)
        # Standardize spacing around operators in math mode
        content = re.sub(r"\s*([=+\-*/^])\s*", r"\1", content)
        # Ensure single space after \text{...} if followed by another token
        content = re.sub(r"(\\text\{[^\}]+\})(\w)", r"\1 \2", content)
        return f"${content}$"

    # Process inline math (non-greedy match between unescaped $)
    text = re.sub(r"(?<!\\)\$(?!\$)(.*?)(?<!\\)\$", _clean_inline_math, text)

    # Normalize common units in math or text
    # e.g. \text{m/s} vs \text{m s}^{-1} vs m/s
    text = re.sub(r"\\text\{\s*m/s\s*\}", r"\\text{m/s}", text)
    text = re.sub(r"\\text\{\s*m\s+s\^\{-1\}\s*\}", r"\\text{m/s}", text)
    text = re.sub(r"\\text\{\s*m\s*\}", r"\\text{m}", text)
    text = re.sub(r"\\text\{\s*s\s*\}", r"\\text{s}", text)
    text = re.sub(r"\\text\{\s*kg\s*\}", r"\\text{kg}", text)

    return text


def clean_statement_text(text: str) -> str:
    """Non-destructive normalization of problem statement text."""
    if not text:
        return ""

    text = normalize_unicode_and_symbols(text)
    text = normalize_latex(text)

    # Strip exam-level boilerplate prefixes
    for pat in BOILERPLATE_PATTERNS:
        text = pat.sub("", text)

    # Collapse multiple whitespaces/newlines to single space
    text = re.sub(r"\s+", " ", text).strip()

    # Normalize punctuation at the very end (keep question mark, strip redundant trailing period/colon)
    if text.endswith(":") or text.endswith("."):
        text = text[:-1].strip()

    return text


def clean_option_text(text: str) -> str:
    """Non-destructive normalization of option text."""
    if not text:
        return ""

    text = normalize_unicode_and_symbols(text)
    # Strip (A), A., A), etc.
    text = OPTION_PREFIX_PATTERN.sub("", text)
    text = normalize_latex(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_numerical_values(text: str) -> List[str]:
    """Extract ordered numerical tokens and constants appearing in text or math."""
    if not text:
        return []
    # Match integer, decimal, fraction, scientific notation, square roots
    pattern = re.compile(
        r"(?:\\sqrt\{\d+\}|\d+\s*/\s*\d+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\b\d+\b)"
    )
    matches = pattern.findall(text)
    cleaned = [re.sub(r"\s+", "", m) for m in matches if m.strip()]
    return cleaned


def extract_target_quantity(text: str) -> Optional[str]:
    """Identify the primary target physics quantity sought in the statement."""
    lower_text = text.lower()
    for phrase, tag in PHYSICS_TARGET_TERMS:
        if phrase in lower_text:
            return tag
    return None


def compute_normalized_fingerprint(atom: KnowledgeAtom) -> NormalizedAtomFingerprint:
    """Produce deterministic auxiliary fingerprint without mutating the canonical atom."""
    statement_raw = atom.question.statement if atom.question else (atom.content or "")
    statement_norm = clean_statement_text(statement_raw)
    statement_hash = hashlib.sha256(statement_norm.encode("utf-8")).hexdigest()

    options_norm: Optional[List[str]] = None
    options_hash: Optional[str] = None
    problem_components: List[str] = [statement_norm]

    if atom.question and atom.question.options:
        # Sort options by normalized text to be invariant to option letter permutations
        sorted_opts = sorted(
            [clean_option_text(opt.text) for opt in atom.question.options]
        )
        options_norm = sorted_opts
        joined_opts = " || ".join(sorted_opts)
        options_hash = hashlib.sha256(joined_opts.encode("utf-8")).hexdigest()
        problem_components.append(joined_opts)

    full_problem_str = " ## ".join(problem_components)
    problem_hash = hashlib.sha256(full_problem_str.encode("utf-8")).hexdigest()

    # Taxonomy node
    tax_node: Optional[str] = None
    chap_id: Optional[str] = None
    top_id: Optional[str] = None
    subtop_id: Optional[str] = None
    if atom.taxonomy:
        chap_id = atom.taxonomy.chapter_id
        top_id = atom.taxonomy.topic_id
        subtop_id = atom.taxonomy.subtopic_id
        components = [chap_id, top_id]
        if subtop_id:
            components.append(subtop_id)
        tax_node = "/".join(components)

    # Target quantity and numericals
    target_q = extract_target_quantity(statement_norm)
    numericals = extract_numerical_values(statement_norm)
    has_fig = len(atom.figure_refs) > 0 or ("\\begin{figure}" in statement_raw or "figure" in statement_raw.lower() or "diagram" in statement_raw.lower())

    # Physics skeleton hash: captures essential structure (tax_node, target_q, sorted numericals, has_fig)
    skeleton_str = f"tax:{tax_node}|target:{target_q}|nums:{sorted(numericals)}|fig:{has_fig}"
    skeleton_hash = hashlib.sha256(skeleton_str.encode("utf-8")).hexdigest()

    q_type = "MCQ" if (atom.question and atom.question.options) else "NUMERICAL"

    return NormalizedAtomFingerprint(
        atom_id=atom.atom_id,
        statement_normalized=statement_norm,
        statement_hash=statement_hash,
        options_normalized=options_norm,
        options_hash=options_hash,
        problem_hash=problem_hash,
        taxonomy_node=tax_node,
        chapter_id=chap_id,
        topic_id=top_id,
        subtopic_id=subtop_id,
        question_type=q_type,
        target_quantity=target_q,
        numerical_values=numericals,
        has_figure=has_fig,
        physics_skeleton_hash=skeleton_hash,
    )
