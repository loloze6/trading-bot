"""
F4b (2026-07-05): _repair_yaml previously gave up ("unrepairable") on a colon
appearing on a WRAPPED CONTINUATION line of a multi-line plain-scalar list item
— a real failure discovered live when run_047 (H-041-A reactivation, P1b) halted
at hypothesis_generation. Fixture is the frozen, real, broken LLM output from
that run (tests/fixtures/run_047_broken_hypothesis_card.yaml) — per this
project's standing rule, regression tests use the actual historical failure as
fixture, frozen so a later successful re-run of the live directory can't
invalidate the test.
"""
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = ROOT / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "run_047_broken_hypothesis_card.yaml"


def test_fixture_is_genuinely_broken():
    """Sanity check: the raw fixture must fail to parse (guards against the
    fixture silently becoming valid YAML and the test passing vacuously)."""
    content = FIXTURE.read_text(encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        list(yaml.safe_load_all(content))


def test_real_run_047_output_is_now_repairable():
    content = FIXTURE.read_text(encoding="utf-8")
    repaired = rpr._repair_yaml(content, source="run_047_broken_hypothesis_card.yaml")
    docs = list(yaml.safe_load_all(repaired))  # must not raise
    card = docs[0]
    assert card["hypothesis_id"] == "H-041-A"
    # The offending list item must survive as one folded, quoted string containing
    # the originally-unquoted colon, not be dropped or truncated.
    assumptions = card["assumptions"]
    folded = [a for a in assumptions if "empirical lag" in a]
    assert len(folded) == 1
    assert "lag: 0" in folded[0] or "lag:" in folded[0]


def test_repair_multiline_list_item_merges_and_quotes():
    lines = [
        "assumptions:",
        "  - first line of a wrapped value",
        "    (note: contains an unquoted colon).",
        "  - a normal single-line item",
    ]
    new_lines = rpr._repair_multiline_list_item(lines, 2)
    assert new_lines is not None
    merged_yaml = "\n".join(new_lines)
    parsed = yaml.safe_load(merged_yaml)
    assert parsed["assumptions"] == [
        "first line of a wrapped value (note: contains an unquoted colon).",
        "a normal single-line item",
    ]


def test_repair_multiline_list_item_returns_none_for_non_continuation_lines():
    """A line that IS a `- ` marker or `key:` mapping is not a continuation —
    _quote_yaml_line already handles those shapes, this function must defer."""
    lines = ["assumptions:", "  - a normal item", "key: value"]
    assert rpr._repair_multiline_list_item(lines, 1) is None
    assert rpr._repair_multiline_list_item(lines, 2) is None


def test_repair_multiline_list_item_handles_multiple_continuation_lines():
    lines = [
        "assumptions:",
        "  - line one of three",
        "    line two (with: colon)",
        "    line three, still continuing",
        "  - next item",
    ]
    new_lines = rpr._repair_multiline_list_item(lines, 2)
    assert new_lines is not None
    parsed = yaml.safe_load("\n".join(new_lines))
    assert parsed["assumptions"] == [
        "line one of three line two (with: colon) line three, still continuing",
        "next item",
    ]
