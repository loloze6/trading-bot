"""D-143: step 1a picks criteria by three closed questions, never whole_test_sharpe_positive.

Declared prompt change (no flag, no code): IMPROVEMENT 07 of hypothesis-design/SKILL.md
and DECIDE_NEXT_CANDIDATES.md no longer offer whole_test_sharpe_positive (pre-registered by
a brief only, D-121); the menu entry says so in a comment. The "neither" answer records an
optional `criteria_fit` string on the card, added to hypothesis_card.schema.json so such a
card stays schema-clean (validation is warn-only; nothing reads the field to decide).
"""
import json
import re
from pathlib import Path

import jsonschema
import yaml

SR = Path(__file__).resolve().parent.parent
SKILL_DIR = SR / "workflow_artifacts" / "skills" / "hypothesis-design"
SCHEMA = SR / "workflow_artifacts" / "schemas" / "hypothesis_card.schema.json"


def _validator():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.validators.validator_for(schema)(schema)


def _minimal_card():
    return {
        "hypothesis_id": "H_D143", "thesis": "t", "rationale": "r",
        "edge_source": {"category": "persistent_behavioral_bias", "evidence_type": "price_volume_only",
                        "specific_mechanism": "m", "why_not_arbitraged": "w", "measurable_proxy": "p"},
        "signal_concept": "s", "target_market": "m", "timeframe": "1d",
        "assumptions": ["a"], "expected_failure_modes": ["f1", "f2", "f3"],
        "criteria": [{"id": "forecast_ic_median"}],
    }


def test_step_1a_prompts_no_longer_offer_the_sharpe_entry():
    for name in ("SKILL.md", "DECIDE_NEXT_CANDIDATES.md"):
        assert "whole_test_sharpe_positive" not in (SKILL_DIR / name).read_text(encoding="utf-8"), name


def test_the_menu_entry_says_briefs_only():
    menu = (SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8")
    entry = menu.split("- id: whole_test_sharpe_positive", 1)[1].splitlines()[1]
    assert entry.strip() == "# pre-registered by a brief only (D-121); not for step 1a"
    ids = [c["id"] for c in yaml.safe_load(menu)["criteria"]]
    assert "whole_test_sharpe_positive" in ids  # kept for briefs (D-121)


def test_the_criteria_fit_example_parses_and_validates():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    (example,) = re.findall(r"`(criteria_fit: [^`]+)`", skill)
    value = yaml.safe_load(example)["criteria_fit"]
    assert isinstance(value, str) and value.startswith("none: ")
    card = {**_minimal_card(), "criteria_fit": value}
    assert list(_validator().iter_errors(_minimal_card())) == []
    assert list(_validator().iter_errors(card)) == []


def test_criteria_fit_must_be_a_string():
    errors = list(_validator().iter_errors({**_minimal_card(), "criteria_fit": ["none"]}))
    assert [e.json_path for e in errors] == ["$.criteria_fit"]
