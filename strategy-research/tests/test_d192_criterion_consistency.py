"""D-192 (direction 2026-10-24, PR-8): after step 1a, code compares the card's criteria with its
`statement` and records a WARNING beside the card (artifacts/criterion_consistency.yaml, the
claim_prefill.yaml shape). It refuses nothing, retries nothing, has no flag.

return_direction expects forecast_ic_median at the menu horizon nearest horizon_bars; market_state
expects a label measure, which the menu lacks ("no label measure in the menu"); a statement without
predicts_kind warns "statement has no predicts_kind"; a card with no statement at all is not checked.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tests"))
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
import test_c51_menu_criterion_lint as t51  # noqa: E402

RAW = yaml.safe_load((SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
MENU_ON = RAW                                    # orchestrator.forecast_ic_horizons on: horizon keys kept
MENU_OFF = vce.menu_without_horizon(RAW)         # flag off (the default): no horizon keys
SCHEMA = json.loads((SR / "workflow_artifacts" / "schemas" / "hypothesis_card.schema.json")
                    .read_text(encoding="utf-8"))
IC = "forecast_ic_median"


def _card(kind="return_direction", bars=24, **extra):
    st = {"predicts": "the sign of the next return", "horizon_bars": bars, "condition": "all bars",
          "if_pass": "keep", "if_fail": "drop"}
    if kind is not None:
        st["predicts_kind"] = kind
    return {"hypothesis_id": "H", "timeframe": "1h", "statement": st, **extra}


def _rule(*items, menu=MENU_ON):
    return {"criteria": vce.resolve_criteria_against_menu(list(items), menu)}


def _warn(card, rule, menu=MENU_ON):
    return rpr._criterion_consistency_warnings(card, rule, menu)


# -- the four specified tests, plus the absent field ---------------------------------------------

def test_return_direction_matching_horizon_gives_no_warning():
    assert _warn(_card(bars=24), _rule({"id": IC, "horizon": 24})) == []
    assert _warn(_card(bars=20), _rule({"id": IC, "horizon": 24})) == []   # 20 rounds to 24


def test_return_direction_wrong_horizon_warns_with_both_values():
    (w,) = _warn(_card(bars=24), _rule({"id": IC, "horizon": 6}))
    assert "horizon 24" in w and "horizon [6]" in w and IC in w


def test_return_direction_with_another_measure_warns_with_both_values():
    (w,) = _warn(_card(bars=24), _rule({"id": "sign_consistent_by_era"}))
    assert f"expected {IC} at horizon 24" in w and "sign_consistent_by_era" in w


def test_market_state_warns_no_label_measure_in_the_menu():
    assert not [e for e in RAW["criteria"] if e.get("predicts_kind")]    # still true today
    assert _warn(_card("market_state"), _rule({"id": IC, "horizon": 24})) == ["no label measure in the menu"]
    assert _warn(_card("market_state"), _rule({"id": IC, "horizon": 24}), MENU_OFF) == \
        ["no label measure in the menu"]


def test_market_state_warning_stops_once_the_menu_holds_a_label_measure():
    menu = copy.deepcopy(MENU_ON)
    menu["criteria"].append({"id": "label_outcome_corr", "predicts_kind": "market_state"})
    assert _warn(_card("market_state"), {"criteria": [{"id": "label_outcome_corr"}]}, menu) == []
    (w,) = _warn(_card("market_state"), _rule({"id": IC, "horizon": 24}), menu)
    assert "label_outcome_corr" in w and IC in w


def test_absent_predicts_kind_warns():
    assert _warn(_card(None), _rule({"id": IC, "horizon": 24})) == ["statement has no predicts_kind"]


def test_a_card_with_no_statement_is_not_checked():
    old = {"hypothesis_id": "H", "timeframe": "1h", "thesis": "t"}
    assert _warn(old, _rule({"id": IC})) == []


# -- rules around the edges ---------------------------------------------------------------------

def test_the_nearest_horizon_ties_to_the_smaller_one():
    assert _warn(_card(bars=15), _rule({"id": IC, "horizon": 6})) == []      # 15 is 9 from 6 and 9 from 24
    (w,) = _warn(_card(bars=15), _rule({"id": IC, "horizon": 24}))
    assert "at horizon 6," in w and "horizon [24]" in w


def test_flag_off_the_expected_horizon_is_one():
    # the menu offers only horizon 1 and the resolved criterion has no horizon key (reads as 1)
    assert _warn(_card(bars=24), _rule({"id": IC}, menu=MENU_OFF), MENU_OFF) == []
    (w,) = _warn(_card(bars=24), _rule({"id": "sign_consistent_by_era"}, menu=MENU_OFF), MENU_OFF)
    assert "at horizon 1," in w


def test_unusable_horizon_bars_and_unknown_kind_warn():
    (w,) = _warn(_card(bars="24"), _rule({"id": IC, "horizon": 24}))
    assert "horizon_bars" in w
    (w,) = _warn(_card("sentiment"), _rule({"id": IC, "horizon": 24}))
    assert "sentiment" in w


# -- the writer ---------------------------------------------------------------------------------

def test_the_writer_records_a_warning_beside_the_card(tmp_path, capsys):
    (tmp_path / "artifacts").mkdir()
    rpr._write_criterion_consistency(tmp_path, "run_x", _card(bars=24), _rule({"id": IC, "horizon": 6}), MENU_ON)
    doc = yaml.safe_load((tmp_path / "artifacts" / "criterion_consistency.yaml").read_text(encoding="utf-8"))
    assert doc["run_id"] == "run_x" and doc["status"] == "warning" and len(doc["warnings"]) == 1
    assert "D-192" in capsys.readouterr().out
    rpr._write_criterion_consistency(tmp_path, "run_x", _card(bars=24), _rule({"id": IC, "horizon": 24}), MENU_ON)
    assert yaml.safe_load((tmp_path / "artifacts" / "criterion_consistency.yaml")
                          .read_text(encoding="utf-8")) == {"run_id": "run_x", "status": "ok", "warnings": []}
    rpr._write_criterion_consistency(tmp_path, "run_x", {"hypothesis_id": "H"}, _rule({"id": IC}), MENU_ON)
    assert yaml.safe_load((tmp_path / "artifacts" / "criterion_consistency.yaml")
                          .read_text(encoding="utf-8"))["status"] == "not_checked"


@pytest.mark.parametrize("card,rule,menu", [
    (None, None, None), ("x", "y", "z"), ({"statement": 3}, {"criteria": 5}, {"criteria": "no"}),
    (_card(), {"criteria": [None, 3]}, {"criteria": [None]}),
])
def test_the_writer_never_raises(tmp_path, card, rule, menu):
    (tmp_path / "artifacts").mkdir()
    rpr._write_criterion_consistency(tmp_path, "run_y", card, rule, menu)
    doc = yaml.safe_load((tmp_path / "artifacts" / "criterion_consistency.yaml").read_text(encoding="utf-8"))
    assert doc["run_id"] == "run_y" and doc["status"] in ("ok", "warning", "not_checked", "error")


def test_the_writer_survives_an_unwritable_artifacts_dir(tmp_path):
    rpr._write_criterion_consistency(tmp_path / "missing", "run_z", _card(), _rule({"id": IC}), MENU_ON)


def test_the_check_changes_none_of_its_arguments():
    card, rule = _card(bars=24), _rule({"id": IC, "horizon": 6})
    before = (copy.deepcopy(card), copy.deepcopy(rule), copy.deepcopy(MENU_ON))
    _warn(card, rule)
    assert (card, rule, MENU_ON) == before


# -- through the 1a writer: the pass_rule is written unchanged, nothing is refused ---------------

def _card_run(sandbox, run_id, card):
    t51._seed_real_menu(sandbox)
    brief = t51._fresh_launch_brief(None)
    brief.pop("evaluation")
    brief["candidate"] = {"criteria_from": rpr.PASS_RULE_PENDING_AT_1A,
                          "source": {"hypothesis_id": "H__p-1"}}
    camp._materialize_run(run_id, brief)
    run_dir = camp.ROOT / "runs" / run_id
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({**card, "hypothesis_id": "H__p-1"}), encoding="utf-8")
    return run_dir


def _pre_reg(run_id):
    return yaml.safe_load((camp.ROOT / "runs" / run_id / "artifacts" / "pre_registration.yaml")
                          .read_text(encoding="utf-8"))


def test_a_mismatch_through_the_1a_writer_refuses_nothing(_sandbox_by_default):
    # flag off (default): resolved criteria carry no horizon; a statement predicting a market state warns
    ms = {"statement": _card("market_state")["statement"], "criteria": [{"id": IC}]}
    run_dir = _card_run(_sandbox_by_default, "run_d192_1", ms)
    assert rpr._write_pass_rule_from_card(run_dir, "run_d192_1", False) is True
    rec = yaml.safe_load((run_dir / "artifacts" / "criterion_consistency.yaml").read_text(encoding="utf-8"))
    assert rec["status"] == "warning" and rec["warnings"] == ["no label measure in the menu"]
    with_warning = _pre_reg("run_d192_1")["pass_rule"]

    plain = {"criteria": [{"id": IC}]}                       # the same criteria, no statement
    run_dir = _card_run(_sandbox_by_default, "run_d192_2", plain)
    assert rpr._write_pass_rule_from_card(run_dir, "run_d192_2", False) is True
    assert _pre_reg("run_d192_2")["pass_rule"] == with_warning     # the warning changed nothing
    assert yaml.safe_load((run_dir / "artifacts" / "criterion_consistency.yaml")
                          .read_text(encoding="utf-8"))["status"] == "not_checked"


def test_flag_on_through_the_1a_writer_a_wrong_horizon_warns_and_is_registered(_sandbox_by_default):
    _set_orchestrator({"forecast_ic_horizons": {"enabled": True}})
    card = {**_card(bars=24), "criteria": [{"id": IC, "horizon": 6}]}
    run_dir = _card_run(_sandbox_by_default, "run_d192_3", card)
    assert rpr._write_pass_rule_from_card(run_dir, "run_d192_3", False) is True
    assert _pre_reg("run_d192_3")["pass_rule"]["criteria"][0]["horizon"] == 6     # registered as written
    rec = yaml.safe_load((run_dir / "artifacts" / "criterion_consistency.yaml").read_text(encoding="utf-8"))
    assert rec["status"] == "warning" and "horizon 24" in rec["warnings"][0] and "[6]" in rec["warnings"][0]


def test_a_composition_card_is_not_checked(_sandbox_by_default):
    card = {**_card("market_state"), "criteria": [{"id": IC}],
            "composition": {"registry_hash": "h", "timeframe": "1h", "block_ids": ["b"], "manifest_ref": "m"}}
    run_dir = _card_run(_sandbox_by_default, "run_d192_4", card)
    rpr._write_pass_rule_from_card(run_dir, "run_d192_4", False)
    assert not (run_dir / "artifacts" / "criterion_consistency.yaml").exists()


def test_a_pre_registered_candidate_is_not_checked(_sandbox_by_default):
    t51._seed_real_menu(_sandbox_by_default)
    brief = t51._fresh_launch_brief(None)
    brief.pop("evaluation")
    brief["candidate"] = {"criteria_from": "somewhere_else", "source": {"hypothesis_id": "H__p-1"}}
    camp._materialize_run("run_d192_5", brief)
    run_dir = camp.ROOT / "runs" / "run_d192_5"
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({**_card("market_state"), "hypothesis_id": "H__p-1"}), encoding="utf-8")
    rpr._write_pass_rule_from_card(run_dir, "run_d192_5", False)
    assert not (run_dir / "artifacts" / "criterion_consistency.yaml").exists()


# -- the schema ---------------------------------------------------------------------------------

def _valid(card):
    jsonschema.validate(card, SCHEMA)


def test_schema_accepts_both_kinds_and_refuses_another():
    _valid(_card("return_direction"))
    _valid(_card("market_state"))
    with pytest.raises(jsonschema.ValidationError):
        _valid(_card("sentiment"))


def test_schema_requires_predicts_kind_inside_a_statement_but_not_a_statement():
    with pytest.raises(jsonschema.ValidationError):
        _valid(_card(None))
    _valid({"hypothesis_id": "H", "timeframe": "1h", "thesis": "t", "criteria": [{"id": IC}]})   # old card
    assert SCHEMA["properties"]["statement"]["required"] == ["predicts", "predicts_kind"]
    assert "statement" not in SCHEMA["else"]["required"]
