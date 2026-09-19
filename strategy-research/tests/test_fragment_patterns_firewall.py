"""
Mechanical enforcement of the fragment_patterns firewall (2026-07-10). See
docs/VERIFICATION_DOCTRINE.md section 2 for the doctrine this enforces:
fragment_patterns.yaml is an ideation-only diagnostic artifact and must never
be a decision-path input. These are static/import-graph checks, not
convention -- if any of them fail, the firewall has been breached in code or
in a skill's documented required inputs, regardless of intent.
"""
import ast
from pathlib import Path

STRATEGY_RESEARCH = Path(__file__).parent.parent
TOOLS = STRATEGY_RESEARCH / "tools"
SKILLS = STRATEGY_RESEARCH / "workflow_artifacts" / "skills"


def _imported_module_names(py_path: Path) -> set:
    tree = ast.parse(py_path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[0])
    return names


def test_run_protocol_does_not_import_fragment_patterns():
    """The decision-path module (evaluate_against_decision_rules,
    _aggregate_trade_diagnostics, Gate B, A3.4) must never import
    fragment_patterns -- a static AST check, not a grep, so it can't be
    fooled by a comment mentioning the name."""
    run_protocol_path = TOOLS / "run_protocol.py"
    imported = _imported_module_names(run_protocol_path)
    assert "fragment_patterns" not in imported, (
        "run_protocol.py imports fragment_patterns -- this breaches the "
        "ideation-only firewall; fragment_patterns output must never reach "
        "the decision path."
    )


def test_no_decision_path_module_imports_fragment_patterns():
    """Broader sweep: no .py file under workflow/ or tools/ EXCEPT
    fragment_patterns.py itself (and this test file) may import it. Anything
    that does is either a new decision-path consumer (forbidden) or a
    legitimate ideation-side consumer that should be reviewed and, if
    legitimate, explicitly excluded here with a reason -- not silently
    allowed."""
    allowed = {"fragment_patterns.py", "test_fragment_patterns_firewall.py"}
    offenders = []
    for py_path in list((STRATEGY_RESEARCH / "tools").glob("*.py")) + \
                    list((STRATEGY_RESEARCH / "workflow").glob("*.py")):
        if py_path.name in allowed:
            continue
        if "fragment_patterns" in _imported_module_names(py_path):
            offenders.append(str(py_path))
    assert not offenders, f"Unexpected fragment_patterns import(s) in decision-path code: {offenders}"


def test_verdict_interpreter_skill_does_not_require_fragment_patterns():
    """workflow_artifacts/skills/verdict-interpreter/SKILL.md's 'Required inputs' section must
    never list fragment_patterns.yaml -- verdict_interpreter reads
    protocol_result.yaml / validation_protocol.yaml / backtest_spec.yaml /
    research_brief.yaml / campaign_state.yaml / trade_diagnostics.json /
    prescreen_result.yaml only. A future edit that adds fragment_patterns.yaml
    to that list would silently let fragment-level ideation data relitigate
    a verdict."""
    skill_path = SKILLS / "verdict-interpreter" / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    # Isolate the "Required inputs" section specifically (up to the next "##").
    start = text.index("## Required inputs")
    end = text.index("\n## ", start + 1)
    required_inputs_section = text[start:end]
    assert "fragment_patterns" not in required_inputs_section, (
        "fragment_patterns.yaml appears in verdict-interpreter's Required "
        "inputs section -- this breaches the ideation-only firewall."
    )


def test_fragment_patterns_module_has_no_decision_rule_functions():
    """Sanity check on the module's own surface: it must not define anything
    named like a decision rule (evaluate_*, *_decision_rules, *_verdict),
    which would suggest scope creep back into the decision path."""
    import importlib
    import sys
    sys.path.insert(0, str(TOOLS))
    fp = importlib.import_module("fragment_patterns")
    forbidden_substrings = ["evaluate_against_decision_rules", "decision_rule", "_verdict"]
    for name in dir(fp):
        lname = name.lower()
        assert not any(s in lname for s in forbidden_substrings), (
            f"fragment_patterns.py defines {name!r}, which looks decision-path-shaped"
        )
