"""D-190 (supersedes D-143): step 1a picks the criterion from its own statement, by the seven rules of 2b.

Declared prompt change (no flag, no code): hypothesis-design/SKILL.md is four steps (0 Mode, 1 Idea,
2 Statement with 2b The criterion, 3 Proof). Block 2b is pinned here byte for byte. Nothing in code
derives the criterion from the statement; the model picks it. These are text-level pins on the skill, the
criterion menu and the card schema; D-143's own pins that survive (the briefs-only Sharpe entry, the
`criteria_fit` string) are kept.
"""
import json
import re
from pathlib import Path

import jsonschema
import yaml

SR = Path(__file__).resolve().parent.parent
SKILL_DIR = SR / "workflow_artifacts" / "skills" / "hypothesis-design"
SCHEMA = SR / "workflow_artifacts" / "schemas" / "hypothesis_card.schema.json"
MENU = SR / "config" / "criterion_menu.yaml"

# Direction 2026-10-24, PR-7 (verbatim). Do not reflow.
BLOCK_2B = """### 2b. The criterion
Pick the criterion after the statement is written, from the statement alone, by id from the menu's live entries. Write nothing in `criteria` that is not a menu id.
1. Match the measure to what the statement predicts. A statement that predicts the direction of a return takes the measure that correlates the forecast with the forward return over all bars. A statement that predicts a market state takes the measure that correlates the label with the outcome the statement names. If the menu holds no measure for what the statement predicts, pick nothing and write `criteria_fit` naming the measure that is missing; the run parks on it.
2. Measure at the statement's horizon. Set the criterion's horizon to the card's horizon_bars, rounded to the nearest horizon the menu offers. A measure at another horizon tests a different statement.
3. One criterion per statement. The residual-information criterion is added by code where a block is proven; name nothing beside your one pick.
4. Never a profit measure. Sharpe, return, drawdown and cost ratios are the campaign's bars, checked on every backtest; a menu entry of that kind exists for briefs and is not yours.
5. Never a measure because it was picked before. Earlier cards, the brief template, the order of the menu and the number of times an entry was used are not reasons. Write the reason in one sentence in `criteria_rationale`: what the statement predicts, at which horizon, hence which measure.
6. Pre-registered criteria are not yours. A brief or a pass-through candidate that arrives with criteria keeps them unchanged.
7. Sign consistency across eras is a criterion only when the protocol's windows lie in two or more eras of the data policy. On one era it adds nothing to the forecast measure.
"""

# Fields the code reads from a card (grep of card.get / card[...] over workflow/ and tools/, 2026-10-24),
# plus the D-186 fields and the fields the skill's modes copy through.
CODE_READ_FIELDS = ["hypothesis_id", "claim", "timeframe", "target_market", "criteria", "thesis",
                    "library_lookup", "edge_source"]
NEW_FIELDS = ["idea_quantities", "not_expressible", "statement", "criteria_rationale", "criteria_fit"]
PASS_THROUGH_FIELDS = ["pass_through", "config", "manifest", "source"]
STATEMENT_KEYS = ["predicts", "predicts_kind", "horizon_bars", "condition", "if_pass", "if_fail"]


def _skill():
    return (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").replace("\r\n", "\n")


def _schema():
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def _validator():
    schema = _schema()
    return jsonschema.validators.validator_for(schema)(schema)


def _menu():
    return yaml.safe_load(MENU.read_text(encoding="utf-8"))


def _card_section(skill):
    return skill.split("\n## The card\n", 1)[1]


def _four_step_card(**extra):
    card = {
        "hypothesis_id": "H_D190", "timeframe": "1h", "thesis": "t",
        "idea_quantities": ["the operator's words: a formula"],
        "not_expressible": ["exits"],
        "statement": {"predicts": "the sign of the next 24 hours", "predicts_kind": "return_direction",
                      "horizon_bars": 24,
                      "condition": "all bars", "if_pass": "keep", "if_fail": "drop"},
        "criteria": [{"id": "forecast_ic_median", "horizon": 24}],
        "criteria_rationale": "The statement predicts a return over 24 bars, hence the 24-bar forecast IC.",
    }
    card.update(extra)
    return card


# ---------------------------------------------------------------------------
# 2b: the block, verbatim
# ---------------------------------------------------------------------------

def test_block_2b_is_in_the_skill_exactly_once_and_byte_for_byte():
    skill = _skill()
    assert skill.count(BLOCK_2B) == 1
    assert skill.count("### 2b. The criterion\n") == 1


def test_block_2b_sits_inside_step_2_before_step_3():
    skill = _skill()
    assert skill.index("\n## 2. Statement\n") < skill.index(BLOCK_2B) < skill.index("\n## 3. Proof\n")


def test_the_skill_is_the_four_steps_in_order():
    skill = _skill()
    heads = [skill.index(f"\n## {h}\n") for h in ("0. Mode", "1. Idea", "2. Statement", "3. Proof")]
    assert heads == sorted(heads)


def test_the_seven_rules_are_numbered_1_to_7():
    body = BLOCK_2B.split("\n", 2)[2]
    assert [line[:2] for line in body.splitlines()] == [f"{n}." for n in range(1, 8)]


# ---------------------------------------------------------------------------
# What the rules rely on: the menu and the schema
# ---------------------------------------------------------------------------

def test_the_skill_names_no_menu_id_except_the_composition_one():
    """Rule 5: no id is offered in the skill's text, so none is picked because it was picked before.
    `profit_bars` is named once, by the composition mode, where code writes the criterion."""
    menu = _menu()
    ids = {c["id"] for c in menu["criteria"]} | {c["id"] for c in menu.get("code_added_criteria", [])}
    named = {i for i in ids if i in _skill()}
    assert named == {"profit_bars"}
    assert _skill().count("profit_bars") == 1


def test_decide_next_never_offers_the_sharpe_entry():
    assert "whole_test_sharpe_positive" not in (SKILL_DIR / "DECIDE_NEXT_CANDIDATES.md").read_text(encoding="utf-8")


def test_the_menu_entry_says_briefs_only():
    menu = MENU.read_text(encoding="utf-8")
    entry = menu.split("- id: whole_test_sharpe_positive", 1)[1].splitlines()[1]
    assert entry.strip() == "# pre-registered by a brief only (D-121); not for step 1a"
    ids = [c["id"] for c in yaml.safe_load(menu)["criteria"]]
    assert "whole_test_sharpe_positive" in ids  # kept for briefs (D-121)


def test_rule_2_horizons_are_the_ones_the_menu_offers():
    entry = next(c for c in _menu()["criteria"] if c["id"] == "forecast_ic_median")
    assert entry["card_overridable"] == ["horizon"]
    assert entry["horizon_allowed"] == [1, 6, 24, 72, 168]


def test_the_statement_keys_in_the_skill_are_the_schema_keys():
    assert set(_schema()["properties"]["statement"]["properties"]) == set(STATEMENT_KEYS)
    section = _skill().split("### 2a. The statement\n", 1)[1].split("### 2b.", 1)[0]
    listed = section.split("It has six keys:", 1)[1].split(". ", 1)[0]
    assert re.findall(r"`(\w+)`", listed) == STATEMENT_KEYS


# ---------------------------------------------------------------------------
# The card list
# ---------------------------------------------------------------------------

def test_the_card_list_asks_for_every_code_read_field_by_its_exact_name():
    section = _card_section(_skill())
    listed = re.findall(r"^- `(\w+)`", section, flags=re.M)
    for name in CODE_READ_FIELDS + NEW_FIELDS:
        assert name in listed, name
    for name in PASS_THROUGH_FIELDS:
        assert f"`{name}`" in section, name


def test_every_field_the_card_list_names_is_a_schema_property():
    properties = _schema()["properties"]
    for name in re.findall(r"^- `(\w+)`", _card_section(_skill()), flags=re.M):
        assert name in properties, name


def test_the_edge_source_keys_and_categories_in_the_skill_are_the_schema_ones():
    es = _schema()["properties"]["edge_source"]
    line = next(l for l in _card_section(_skill()).splitlines() if l.startswith("- `edge_source`"))
    for key in es["required"]:
        assert f"`{key}`" in line, key
    for category in es["properties"]["category"]["enum"]:
        assert category in line, category


def test_the_mode_files_the_skill_names_exist_beside_it():
    named = set(re.findall(r"`([A-Z_]+\.md)`", _skill()))
    assert named == {"DECIDE_NEXT_CANDIDATES.md", "PREFILLED_CLAIM.md", "BRIEF_HYPOTHESES.md",
                     "CLAIM_TESTS.md", "CLAIM_TESTS_TRADE.md", "CLAIM_TESTS_EXECUTION.md"}
    for name in named:
        assert (SKILL_DIR / name).is_file(), name


def test_claim_tests_says_horizons_around_horizon_bars_and_the_opposite_reading():
    flat = re.sub(r"\s+", " ", (SKILL_DIR / "CLAIM_TESTS.md").read_text(encoding="utf-8"))
    assert "Test it at horizons around `horizon_bars`, not at `horizon_bars` alone." in flat
    assert "The opposite reading of the statement is its own test." in flat


# ---------------------------------------------------------------------------
# Removed from the body
# ---------------------------------------------------------------------------

def test_the_body_has_no_flag_name_decision_number_line_reference_or_example_block():
    skill = _skill()
    assert not re.search(r"D-\d+", skill)
    assert "orchestrator." not in skill
    assert "```" not in skill
    assert not re.search(r"run_\d+", skill)
    assert not re.search(r"\.(py|yaml|md):\d+", skill)


def test_the_removed_sections_are_gone():
    skill = _skill()
    for gone in ("IMPROVEMENT", "plausible_ic_upper", "power_parameters", "power_note", "cost_feasibility",
                 "cost_model", "Indicator Library Lookup", "Lookup protocol", "A8.6"):
        assert gone not in skill, gone


# ---------------------------------------------------------------------------
# The schema accepts what the skill asks for
# ---------------------------------------------------------------------------

def test_a_four_step_card_validates():
    assert list(_validator().iter_errors(_four_step_card())) == []


def test_criteria_fit_is_a_none_string_and_validates():
    assert "`none: ` then the measure that is missing" in _skill()
    card = _four_step_card(criteria_fit="none: a measure of the label against the outcome")
    assert list(_validator().iter_errors(card)) == []


def test_criteria_fit_must_be_a_string():
    errors = list(_validator().iter_errors(_four_step_card(criteria_fit=["none"])))
    assert [e.json_path for e in errors] == ["$.criteria_fit"]
