import math
import re
from typing import Optional


def normalize_option_label(text: str) -> Optional[str]:
    """Extracts and normalizes an option label (e.g. 'A', 'B', '1', '2').
    
    Examples:
    - 'A' -> 'A'
    - '(A)' -> 'A'
    - 'Option A' -> 'A'
    - 'Option (3)' -> '3'
    - 'c' -> 'C'
    """
    if not text:
        return None
    cleaned = text.strip()

    # Pattern for "Option A", "Option (B)", "(C)", "D."
    match = re.search(r"^(?:option\s+)?[\(\[]?([A-Ea-e1-5])[\)\]\.]?$", cleaned, re.IGNORECASE)
    if match:
        token = match.group(1).upper()
        return token
    return None


def clean_latex_math_string(text: str) -> str:
    """Removes LaTeX display delimiters, text wrappers, and whitespace."""
    s = text.strip()
    # Strip $ or $$
    s = re.sub(r"^\$+(.*?)\$+$", r"\1", s).strip()
    # Strip \( and \) or \[ and \]
    s = re.sub(r"^\\\[(.*?)\\\]$", r"\1", s).strip()
    s = re.sub(r"^\\\((.*?)\\\)$", r"\1", s).strip()
    # Remove \text{...} wrappers
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    # Remove \left and \right
    s = re.sub(r"\\(?:left|right)", "", s)
    # Remove standard units
    s = re.sub(r"\b(?:m/s|ms\^{-1}|ms\^{-2}|m|s|kg|J|N|Nm\^{-1}|V|A|W|\u03a9|\\Omega)\b", "", s)
    return s.strip()


def parse_numerical_value(text: str) -> Optional[float]:
    """Attempts to extract and parse a single real numerical value from text."""
    if not text:
        return None
    cleaned = clean_latex_math_string(text)

    # Convert scientific notation: 1.5 \times 10^{-2} or 1.5 * 10^-2
    sci_match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*(?:\\times|\*)\s*10\^\{?([+-]?\d+)\}?", cleaned)
    if sci_match:
        try:
            base = float(sci_match.group(1))
            exp = float(sci_match.group(2))
            return base * (10 ** exp)
        except Exception:
            pass

    # Convert simple fraction: \frac{a}{b} or a/b
    frac_match = re.search(r"(?:\\frac\{([+-]?\d+(?:\.\d+)?)\}\{([+-]?\d+(?:\.\d+)?)\}|([+-]?\d+(?:\.\d+)?)\s*/\s*([+-]?\d+(?:\.\d+)?))", cleaned)
    if frac_match:
        try:
            num = float(frac_match.group(1) or frac_match.group(3))
            den = float(frac_match.group(2) or frac_match.group(4))
            if den != 0:
                return num / den
        except Exception:
            pass

    # Simple integer or float
    float_match = re.search(r"^[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?$", cleaned)
    if float_match:
        try:
            return float(float_match.group(0))
        except Exception:
            pass

    return None


def evaluate_simple_math_expression(text: str) -> Optional[float]:
    """Safely evaluates deterministic mathematical expressions with sqrt, pi, fractions.
    
    Handles expressions like '2/sqrt(3)' and '2*sqrt(3)/3'.
    """
    cleaned = clean_latex_math_string(text)
    
    # Replace \frac{a}{b} with (a)/(b)
    cleaned = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"(\1)/(\2)", cleaned)
    # Replace \sqrt{a} or \sqrt3 with sqrt(a)
    cleaned = re.sub(r"\\sqrt(?:\{([^}]+)\}|(\d+))", r"sqrt(\1\2)", cleaned)
    # Replace \pi with pi
    cleaned = re.sub(r"\\pi\b", "pi", cleaned)
    # Strip spaces
    cleaned = cleaned.replace(" ", "")
    # Handle implicit multiplication: 2sqrt -> 2*sqrt, 2( -> 2*(, )sqrt -> )*sqrt
    cleaned = re.sub(r"(\d)(sqrt|\()", r"\1*\2", cleaned)
    cleaned = re.sub(r"\)(sqrt|\(|\d)", r"\)*\1", cleaned)

    # Security check: only allow digits, arithmetic symbols, parentheses, sqrt, pi
    if not re.match(r"^[0-9\+\-\*\/\(\)\.\,sqrtpi]+$", cleaned):
        return None

    safe_dict = {
        "sqrt": math.sqrt,
        "pi": math.pi,
        "cos": math.cos,
        "sin": math.sin,
    }

    try:
        val = eval(cleaned, {"__builtins__": {}}, safe_dict)
        if isinstance(val, (int, float)) and not math.isnan(val) and not math.isinf(val):
            return float(val)
    except Exception:
        return None

    return None


def compare_answers(
    ans1: Optional[str],
    ans2: Optional[str],
    rel_tol: float = 0.001,
    abs_tol: float = 1e-6,
) -> bool:
    """Deterministically compares two answers for mathematical, symbolic, or categorical equivalence.
    
    Comparison hierarchy:
    1. Both None -> True; One None -> False
    2. Exact stripped string match
    3. Normalized option labels (e.g. 'A' vs 'Option (A)', or '1' vs '(1)')
    4. Numeric float comparison with relative/absolute tolerance
    5. Evaluated mathematical expressions (e.g. '2/sqrt(3)' vs '2\\sqrt{3}/3')
    6. Normalized LaTeX symbolic equivalence
    """
    if ans1 is None and ans2 is None:
        return True
    if ans1 is None or ans2 is None:
        return False

    s1 = ans1.strip()
    s2 = ans2.strip()

    if s1 == s2:
        return True

    # 1. Option Label Comparison
    opt1 = normalize_option_label(s1)
    opt2 = normalize_option_label(s2)
    if opt1 is not None and opt2 is not None:
        return opt1 == opt2

    # 2. Pure Numerical Value Comparison
    num1 = parse_numerical_value(s1)
    num2 = parse_numerical_value(s2)
    if num1 is not None and num2 is not None:
        return math.isclose(num1, num2, rel_tol=rel_tol, abs_tol=abs_tol)

    # 3. Simple Mathematical Expression Evaluation
    eval1 = evaluate_simple_math_expression(s1)
    eval2 = evaluate_simple_math_expression(s2)
    if eval1 is not None and eval2 is not None:
        return math.isclose(eval1, eval2, rel_tol=rel_tol, abs_tol=abs_tol)

    # 4. Normalized Math String Comparison
    clean1 = clean_latex_math_string(s1).replace(" ", "")
    clean2 = clean_latex_math_string(s2).replace(" ", "")
    if clean1 and clean1 == clean2:
        return True

    return False
