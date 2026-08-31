"""
E-037: the guide must keep up with the code.

WHY THIS EXISTS
---------------
Every drift finding in E-037 has the same shape: the code moved and the
documentation did not, and nothing noticed for months. E037-19 is the clearest
case — five artifacts, all of them recent additions, shipped with no entry in
§3, including `pass_rule_evaluation.yaml`, which has been the decision authority
since 2026-07-13.

Documentation cannot be kept current by intention. This test makes the two
tables that define the pipeline's *shape* — `STAGE_CONFIGS` (which stages exist)
and `_SKILL_MAP` (which are run by an LLM) — fail the suite when the guide has
not kept up.

WHAT IT CHECKS
--------------
1. Every stage in `STAGE_CONFIGS` has a block in USER_GUIDE §2.2.
2. Every stage the guide documents is either in `STAGE_CONFIGS`, or is listed
   in NON_REGISTRY below with the reason it is not.
3. Every LLM stage in `_SKILL_MAP` is documented as `Claude` in the index table.

WHAT IT CANNOT CHECK
--------------------
That the prose is *correct* — only that a stage is not silently missing or
silently invented. Coverage is not accuracy. A block can be present and wrong;
that is what a human review is for.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

_SR = Path(__file__).resolve().parent.parent
_GUIDE = _SR / "docs" / "USER_GUIDE.md"
_ORCH = _SR / "workflow" / "run_phase1_research.py"

# Guide stages that are deliberately NOT in STAGE_CONFIGS, with the reason.
# Adding to this set is a decision, not a formality -- say why.
NON_REGISTRY = {
    "research_brief": "a human input, not an orchestrator stage",
    "regime_detector_validation": "a helper called from inside verdict_interpreter, not a dispatched stage",
    "regime_auditor": "never dispatched; a human runs the skill on a paused pipeline (E037-16)",
}

# Guide name -> code name, where they differ (E037-15).
ALIASES = {"validation_gate": "validation"}


def _literal_from_orchestrator(name: str) -> dict:
    """Read a module-level dict literal without importing the module."""
    tree = ast.parse(_ORCH.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found at module level in {_ORCH.name}")


def _documented_stages() -> dict[str, str]:
    """stage name -> engine, from the §2.2 index table."""
    s = _GUIDE.read_text(encoding="utf-8")
    table = s[s.index("### 2.2 Stage Objectives"): s.index("### 2.2.x Stage detail blocks")]
    out = {}
    for m in re.finditer(r"^\| \d+ \| \[\*\*([a-z_]+)\*\*\]\([^)]*\) \| ([^|]+) \|", table, re.M):
        out[m.group(1)] = m.group(2).strip()
    return out


def _blocks() -> set[str]:
    s = _GUIDE.read_text(encoding="utf-8")
    return set(re.findall(r"^#### Stage \d+ — `([a-z_]+)`", s, re.M))


def test_every_registry_stage_is_documented() -> None:
    registry = set(_literal_from_orchestrator("STAGE_CONFIGS"))
    documented = {ALIASES.get(n, n) for n in _documented_stages()}
    missing = registry - documented
    assert not missing, (
        f"STAGE_CONFIGS defines stage(s) the guide does not document: {sorted(missing)}.\n"
        f"A stage was added to the orchestrator without a §2.2 entry -- the defect "
        f"class E037-19 recorded for artifacts, one level up."
    )


def test_every_documented_stage_exists_or_is_declared_non_registry() -> None:
    registry = set(_literal_from_orchestrator("STAGE_CONFIGS"))
    invented = {
        n for n in _documented_stages()
        if ALIASES.get(n, n) not in registry and n not in NON_REGISTRY
    }
    assert not invented, (
        f"The guide documents stage(s) that are not in STAGE_CONFIGS and are not "
        f"declared non-registry: {sorted(invented)}.\n"
        f"Either the stage was removed from the code, or the guide invented it. If it "
        f"is genuinely not a registry stage, add it to NON_REGISTRY with the reason."
    )


def test_every_registry_stage_has_a_detail_block() -> None:
    registry = set(_literal_from_orchestrator("STAGE_CONFIGS"))
    blocks = {ALIASES.get(b, b) for b in _blocks()}
    missing = registry - blocks
    assert not missing, (
        f"No §2.2.x detail block for: {sorted(missing)}. The index table alone is "
        f"not documentation -- the block is where the input/output contract lives."
    )


def test_llm_stages_are_documented_as_claude() -> None:
    skill_map = _literal_from_orchestrator("_SKILL_MAP")
    documented = _documented_stages()
    wrong = []
    for guide_name, engine in documented.items():
        code_name = ALIASES.get(guide_name, guide_name)
        if code_name in skill_map and "Claude" not in engine:
            wrong.append((guide_name, engine))
    assert not wrong, (
        f"Stage(s) dispatched to an LLM via _SKILL_MAP but not documented as Claude: "
        f"{wrong}. The engine column decides what a reader thinks runs the stage."
    )
