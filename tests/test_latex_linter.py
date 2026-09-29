from jee_physics.validation.latex_linter import lint_latex_syntax


def test_clean_latex_passes_with_zero_errors():
    clean_text = (
        "Under constant acceleration, the equation of motion is $v^2 = u^2 + 2as$. "
        "In vector form: $$\\vec{F} = \\frac{d\\vec{p}}{dt}$$ where $\\vec{p} = m\\vec{v}$."
    )
    errors = lint_latex_syntax(clean_text)
    assert len(errors) == 0


def test_unbalanced_dollar_flagged():
    bad_text = "The speed is $v = 10 m/s without closing delimiter."
    errors = lint_latex_syntax(bad_text)
    assert any("Unbalanced inline math delimiters" in e for e in errors)


def test_unbalanced_braces_in_math_flagged():
    bad_math = "Force is given by $\\frac{m v^2{r}$ where denominator brace is missing."
    errors = lint_latex_syntax(bad_math)
    assert any("unbalanced curly braces" in e for e in errors)


def test_unbalanced_display_brackets_flagged():
    bad_display = "Here is an equation: \\[ E = mc^2 without closing bracket."
    errors = lint_latex_syntax(bad_display)
    assert any("Unbalanced LaTeX display brackets" in e for e in errors)
