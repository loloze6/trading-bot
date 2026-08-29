"""Mechanical enforcement of the near-miss scoreboard firewall (E-018 S1/S2).

Doctrine, verbatim from docs/CAMPAIGN_PROGRAM.md Part 1: "we build both,
firewalled: the near-miss scoreboard ... that the idea-generation stage reads
as raw material, and that promotion is *forbidden* to read. The scoreboard
inspires; only the gates decide." E-018/EPIC.md: "the promotion decision path
has no read access to it, verified by inspection of what promotion
code/process actually consults."

BY INSPECTION (2026-08-23, this file's own audit trail -- not just the
conclusion): the promotion decision path in this codebase is
  - workflow/run_campaign.py -- writes/reads promotion_audit.yaml and the
    provisional_promote_* routing states (grep: `promotion_audit`,
    `provisional_promote`).
  - workflow/run_phase1_research.py -- shares campaign state/KB machinery
    with run_campaign.py and feeds it.
  - tools/deflate_sharpe.py -- the DSR gate that must clear before a
    candidate is promotable (see E-018's sibling epics, E-025/E-026).
No other .py file under workflow/ or tools/ was found (grep -rl
"promotion_audit|promot") to touch promotion machinery as of this writing.

This test suite does NOT trust that inspection alone -- same pattern as
test_fragment_patterns_firewall.py's precedent for the fragment_patterns
ideation-only firewall: an AST import scan plus a broad text-reference scan
across the WHOLE of workflow/ and tools/ (not just the three files named
above), so a *new* promotion-adjacent module gaining access is caught even
before anyone updates this docstring's inspection notes.

The `test_scanner_actually_detects_an_injected_violation` test proves the
scanner itself is not vacuous (i.e. it isn't silently matching nothing).
"""

import ast
from pathlib import Path

STRATEGY_RESEARCH = Path(__file__).parent.parent
TOOLS = STRATEGY_RESEARCH / "tools"
WORKFLOW = STRATEGY_RESEARCH / "workflow"
SKILLS = STRATEGY_RESEARCH / "workflow_artifacts" / "skills"

MODULE_NAME = "near_miss_scoreboard"
ARTIFACT_NAMES = ("near_miss_scoreboard.yaml", "near_miss_scoreboard.md")

# Files that are allowed to mention the module/artifact: the generator
# itself and this suite's own test files.
_ALLOWED_FILENAMES = {
    "near_miss_scoreboard.py",
    "test_near_miss_scoreboard.py",
    "test_near_miss_scoreboard_firewall.py",
}

# The specific modules the epic and this docstring name as "the promotion
# path" -- asserted individually, with a message that names the doctrine,
# in addition to the blanket sweep below.
_NAMED_PROMOTION_MODULES = [
    WORKFLOW / "run_campaign.py",
    WORKFLOW / "run_phase1_research.py",
    TOOLS / "deflate_sharpe.py",
]


def _imported_module_names(py_path: Path) -> set:
    tree = ast.parse(py_path.read_text(encoding="utf-8", errors="replace"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[0])
    return names


def _references_scoreboard(py_path: Path) -> bool:
    """True if the file imports the module OR mentions its name/output
    filenames anywhere in its source text. The text scan (not just AST
    imports) is deliberate: it also catches importlib.import_module(...),
    subprocess calls, or a hardcoded output path string -- none of which
    show up as an `ast.Import` node."""
    if MODULE_NAME in _imported_module_names(py_path):
        return True
    text = py_path.read_text(encoding="utf-8", errors="replace")
    if MODULE_NAME in text:
        return True
    return any(name in text for name in ARTIFACT_NAMES)


def _sweep(root: Path):
    """Returns the list of offending file paths under `root` (recursive over
    *.py), excluding the allow-listed generator/test files."""
    offenders = []
    for py_path in sorted(root.rglob("*.py")):
        if py_path.name in _ALLOWED_FILENAMES:
            continue
        if _references_scoreboard(py_path):
            try:
                offenders.append(str(py_path.relative_to(STRATEGY_RESEARCH)))
            except ValueError:
                offenders.append(str(py_path))
    return offenders


# --- the actual firewall assertions -----------------------------------------


def test_named_promotion_modules_do_not_reference_the_scoreboard():
    offenders = []
    for path in _NAMED_PROMOTION_MODULES:
        if not path.exists():
            continue
        if _references_scoreboard(path):
            offenders.append(str(path))
    assert not offenders, (
        "Promotion-path module(s) reference the near-miss scoreboard: "
        f"{offenders}. Per docs/CAMPAIGN_PROGRAM.md Part 1, promotion is "
        "forbidden to read the scoreboard -- 'the scoreboard inspires, only "
        "the gates decide.'"
    )


def test_no_workflow_or_tools_module_reads_the_scoreboard():
    """Blanket sweep, not limited to the three named modules above: nothing
    under workflow/ or tools/ (besides the generator and this test file) may
    import near_miss_scoreboard or reference its output filenames. A future
    promotion-adjacent module gaining read access is caught here even before
    this file's own docstring is updated to name it."""
    offenders = _sweep(WORKFLOW) + _sweep(TOOLS)
    assert not offenders, f"Unexpected near-miss-scoreboard reference(s) in decision-path code: {offenders}"


def test_no_skill_lists_the_scoreboard_as_a_required_input():
    """No skill under workflow_artifacts/skills/ -- decision-adjacent ones
    (verdict-interpreter, quant-validation, campaign-review) most of all --
    may name the scoreboard or its artifact files anywhere in its SKILL.md.
    Idea-generation (E-032) does not exist as a skill yet, so today this
    should be a clean zero across the board; the day E-032 is built, its
    skill is expected to be the one and only exception, and this test will
    need an explicit, reviewed allow-list entry at that point -- not a
    silent pass."""
    offenders = []
    if not SKILLS.exists():
        return
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        if MODULE_NAME in text or any(a in text for a in ARTIFACT_NAMES):
            offenders.append(str(skill_md.relative_to(STRATEGY_RESEARCH)))
    assert not offenders, f"Skill(s) reference the near-miss scoreboard: {offenders}"


def test_scoreboard_module_defines_no_decision_rule_functions():
    """Sanity check on the module's own surface, mirroring the
    fragment_patterns precedent: it must not define anything shaped like a
    decision rule, which would suggest scope creep back toward promotion."""
    import importlib
    import sys

    sys.path.insert(0, str(TOOLS))
    mod = importlib.import_module("near_miss_scoreboard")
    forbidden_substrings = ["evaluate_against_decision_rules", "decision_rule", "promote", "_verdict_gate"]
    offenders = [name for name in dir(mod) if any(s in name.lower() for s in forbidden_substrings)]
    assert not offenders, f"near_miss_scoreboard.py defines decision-path-shaped name(s): {offenders}"


def test_scanner_actually_detects_an_injected_violation(tmp_path):
    """Proves the scanner is not vacuous: an intentionally-injected
    'promotion-path' file that imports the scoreboard module IS caught."""
    fake_root = tmp_path / "workflow"
    fake_root.mkdir()
    (fake_root / "fake_promotion.py").write_text(
        "import near_miss_scoreboard\n\ndef promote(x):\n    return x\n",
        encoding="utf-8",
    )
    offenders = _sweep(fake_root)
    assert offenders, "the scanner failed to catch a deliberately injected violation"


def test_scanner_ignores_the_generator_and_its_own_tests():
    """The generator module obviously references its own name/output paths
    extensively -- confirm _references_scoreboard() correctly flags it as a
    positive (proving the detector isn't just blind to this file), and that
    the allow-list in _sweep() is what keeps it out of the offender list
    (not some accidental non-match)."""
    self_path = TOOLS / "near_miss_scoreboard.py"
    assert _references_scoreboard(self_path), "detector should see the generator's own self-references"
    offenders = _sweep(TOOLS)
    assert str(self_path.relative_to(STRATEGY_RESEARCH)) not in offenders
