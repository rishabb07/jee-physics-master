import re
from typing import List


def lint_latex_syntax(text: str) -> List[str]:
    """Deterministically audits text for malformed LaTeX delimiters and unclosed braces."""
    errors: List[str] = []
    if not text:
        return errors

    # Check unescaped inline dollars ($)
    # Remove escaped dollars (\$ or `\$`)
    cleaned = re.sub(r"\\\$", "", text)
    # Remove double dollars ($$) first to isolate them
    double_dollars = re.findall(r"\$\$", cleaned)
    if len(double_dollars) % 2 != 0:
        errors.append("Unbalanced display math delimiters ($$).")

    without_double = re.sub(r"\$\$", "", cleaned)
    single_dollars = re.findall(r"\$", without_double)
    if len(single_dollars) % 2 != 0:
        errors.append(f"Unbalanced inline math delimiters ($): found {len(single_dollars)} unescaped '$'.")

    # Check \( and \) balancing
    open_parens = len(re.findall(r"\\\(", text))
    close_parens = len(re.findall(r"\\\)", text))
    if open_parens != close_parens:
        errors.append(f"Unbalanced LaTeX inline parentheses: found {open_parens} '\\(' and {close_parens} '\\)'.")

    # Check \[ and \] balancing
    open_brackets = len(re.findall(r"\\\[", text))
    close_brackets = len(re.findall(r"\\\]", text))
    if open_brackets != close_brackets:
        errors.append(f"Unbalanced LaTeX display brackets: found {open_brackets} '\\[' and {close_brackets} '\\]'.")

    # Check curly braces within LaTeX blocks
    # Extract all math blocks: $$...$$, $...$, \(...\), \[...\]
    math_blocks: List[str] = []
    for match in re.finditer(r"\$\$(.*?)\$\$", cleaned, re.DOTALL):
        math_blocks.append(match.group(1))
    for match in re.finditer(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", without_double, re.DOTALL):
        math_blocks.append(match.group(1))
    for match in re.finditer(r"\\\[(.*?)\\\]", text, re.DOTALL):
        math_blocks.append(match.group(1))
    for match in re.finditer(r"\\\((.*?)\\\)", text, re.DOTALL):
        math_blocks.append(match.group(1))

    for idx, block in enumerate(math_blocks):
        # Count unescaped braces
        clean_block = re.sub(r"\\\{|\\\}", "", block)
        open_c = clean_block.count("{")
        close_c = clean_block.count("}")
        if open_c != close_c:
            errors.append(
                f"Math block #{idx + 1} has unbalanced curly braces: {open_c} '{{' vs {close_c} '}}'."
            )

    return errors
