"""D-134 (operator decisions 2026-10-14/15): plain IC is a step-1a-pickable grid criterion,
`forecast_ic_median` in config/criterion_menu.yaml: the median over windows of the window
`core` field forecast_return_corr_all_bars (forecast vs next-bar return, ALL bars) > 0.02,
at least 5 windows, one fixed default (card_overridable: []). No flag. No evaluator change:
the existing window + median path already does everything the entry needs.

(a) the grid grades it on synthetic per-window summaries; (b) a window whose correlation is
undefined (None) is left out of the median and of the window count; (c) step 1a's card gets
the menu's numbers and cannot override them; (d) the D-121 brief lint accepts it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tests"))
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
from _reader_test_helpers import _set_orchestrator  # noqa: E402
import test_c51_menu_criterion_lint as t51  # noqa: E402

# D-186: the raw file now also carries the `horizon` keys that only exist while orchestrator.forecast_ic_horizons
# is on; this file pins D-134 as the pipeline reads it with that flag OFF (the default), so it reads the menu
# through the same strip (tests/test_d186_forecast_ic_horizons.py covers the flag-on entry).
MENU = vce.menu_without_horizon(yaml.safe_load((SR / "config" / "criterion_menu.yaml").read_text(encoding="utf-8")))
CID = "forecast_ic_median"
METRIC = "forecast_return_corr_all_bars"
ENTRY = next(e for e in MENU["criteria"] if e["id"] == CID)
ON = {"brief_criteria": {"enabled": True}}


def _pr(values, trade_count=7):
    """A protocol_result with one window per value; None writes the field as null."""
    return {
        "results": [{"symbol": "ETHUSDT", "window": f"2021-{i + 1:02d}",
                     "core": {METRIC: v, "trade_count": trade_count}}
                    for i, v in enumerate(values)],
        "trade_diagnostics_summary": {}, "per_symbol_summary": {},
        "hypothesis_verdict": {"diagnostics": {}},
    }


# What the grid is given in production: the pass_rule step 1a registered, i.e. the id already
# resolved against the menu (an id-only rule is not "menu-shaped" and the grid refuses it).
RULE = {"pass_rule": {"criteria": vce.resolve_criteria_against_menu([{"id": CID}], MENU)}}


def _grid(values, trade_count=7, **kw):
    out = vce.evaluate_grid({"v1": _pr(values, trade_count)}, RULE, {}, MENU, **kw)
    return out["grid"][CID]["v1"]


# -- the entry itself ------------------------------------------------------------------------

def test_the_entry_is_the_one_the_decision_describes():
    assert ENTRY["metric"] == METRIC and ENTRY["source"] == "window"
    assert ENTRY["reducer"] == "median" and ENTRY["comparator"] == ">"
    assert ENTRY["threshold"] == 0.02 and ENTRY["floor"] == {"min_windows": 5}
    assert ENTRY["scale_free"] is True and ENTRY["symbol_reducer"] is None
    assert "retired_for" not in ENTRY
    assert [e["id"] for e in MENU["criteria"]].count(CID) == 1


# -- (a) the grid ----------------------------------------------------------------------------

def test_pass_when_the_median_is_above_the_threshold():
    cell = _grid([0.011, 0.0315, 0.044, -0.2, 0.0305])      # median 0.0305
    assert cell["result"] == "PASS" and cell["value"] == pytest.approx(0.0305)
    assert cell["threshold"] == 0.02 and cell["comparator"] == ">" and cell["n_windows"] == 5


@pytest.mark.parametrize("values", [
    [0.02, 0.02, 0.02, 0.02, 0.02],             # exactly at the threshold: strict ">" -> FAIL
    [0.0199, 0.05, 0.0199, 0.05, 0.0199],       # median 0.0199
    [-0.03, -0.01, -0.02, 0.4, 0.5],            # a few huge windows do not lift the median
])
def test_fail_at_or_below_the_threshold(values):
    assert _grid(values)["result"] == "FAIL"


def test_inconclusive_under_five_windows():
    cell = _grid([0.5, 0.6, 0.7, 0.8])
    assert cell["result"] == "INCONCLUSIVE" and cell["n_windows"] == 4
    assert "floor.min_windows=5" in cell["reason"]


def test_a_trade_count_of_zero_does_not_drop_a_window_even_with_the_cul415_flag():
    """forecast_return_corr_all_bars is a bar-level field (not in ZERO_TRADE_NOT_COMPUTED_FIELDS):
    a window with no trades still has an IC and still votes."""
    assert METRIC not in vce.ZERO_TRADE_NOT_COMPUTED_FIELDS
    cell = _grid([0.03] * 5, trade_count=0, zero_trade_windows_not_computed=True)
    assert cell["result"] == "PASS" and cell["n_windows"] == 5 and "skipped_windows" not in cell


# -- (b) a window whose metric is None ---------------------------------------------------------

def test_a_none_window_is_left_out_of_the_median_and_the_window_count():
    # median of the five defined values is 0.03; had the two Nones been read as 0 it would be 0.01
    cell = _grid([None, None, 0.01, 0.01, 0.03, 0.03, 0.03])
    assert cell["result"] == "PASS" and cell["value"] == pytest.approx(0.03)
    assert cell["n_windows"] == 5


def test_none_windows_count_against_the_floor():
    cell = _grid([None, 0.05, 0.05, 0.05, 0.05])
    assert cell["result"] == "INCONCLUSIVE" and cell["n_windows"] == 4


def test_a_window_without_the_field_is_the_same_as_none():
    pr = _pr([0.05] * 5)
    del pr["results"][0]["core"][METRIC]
    grid = vce.evaluate_grid({"v1": pr}, RULE, {}, MENU)
    assert grid["grid"][CID]["v1"]["result"] == "INCONCLUSIVE"


def test_all_none_does_not_crash_and_is_inconclusive():
    assert _grid([None] * 6)["result"] == "INCONCLUSIVE"


# -- (c) step 1a's card -----------------------------------------------------------------------

def test_card_naming_the_id_gets_the_menus_numbers():
    crit = rpr._pass_rule_from_card({"criteria": [{"id": CID}]}, MENU, "card.yaml")["criteria"][0]
    assert crit["id"] == CID and crit["metric"] == METRIC and crit["source"] == "window"
    assert crit["reducer"] == "median" and crit["comparator"] == ">"
    assert crit["threshold"] == 0.02 and crit["floor"] == {"min_windows": 5}
    assert not set(rpr._MENU_META_KEYS) & set(crit)


def test_the_entry_declares_no_overridable_field():
    assert ENTRY["card_overridable"] == []          # the key is present and empty, on purpose


@pytest.mark.parametrize("override", [
    {"threshold": 0.05}, {"threshold": 0.0}, {"comparator": ">="}, {"metric": "forecast_return_corr"},
    {"reducer": "mean"}, {"floor": {"min_windows": 3}}, {"symbol_reducer": "per_symbol_all"},
])
def test_a_card_trying_to_override_is_refused(override):
    with pytest.raises(ValueError, match="does not let a criterion override") as exc:
        rpr._pass_rule_from_card({"criteria": [{"id": CID, **override}]}, MENU, "card.yaml")
    assert "Refusing before 1b" in str(exc.value)


def test_restating_the_menus_own_threshold_is_not_an_override():
    out = rpr._pass_rule_from_card({"criteria": [{"id": CID, "threshold": 0.02}]}, MENU, "c")
    assert out["criteria"][0]["threshold"] == 0.02


def _card_run(sandbox, run_id, criteria):
    t51._seed_real_menu(sandbox)
    brief = t51._fresh_launch_brief(None)
    brief.pop("evaluation")
    brief["candidate"] = {"criteria_from": rpr.PASS_RULE_PENDING_AT_1A,
                          "source": {"hypothesis_id": "H__p-1"}}
    camp._materialize_run(run_id, brief)
    run_dir = camp.ROOT / "runs" / run_id
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "H__p-1", "criteria": criteria}), encoding="utf-8")
    return run_dir


def _pre_reg(run_id):
    return yaml.safe_load((camp.ROOT / "runs" / run_id / "artifacts" / "pre_registration.yaml")
                          .read_text(encoding="utf-8"))


def test_1a_writer_registers_it_and_refuses_an_override(_sandbox_by_default):
    run_dir = _card_run(_sandbox_by_default, "run_d134_1", [{"id": CID}])
    assert rpr._write_pass_rule_from_card(run_dir, "run_d134_1", False) is True
    crit = _pre_reg("run_d134_1")["pass_rule"]["criteria"][0]
    assert crit["id"] == CID and crit["threshold"] == 0.02 and crit["floor"] == {"min_windows": 5}

    run_dir = _card_run(_sandbox_by_default, "run_d134_2", [{"id": CID, "threshold": 0.01}])
    before = _pre_reg("run_d134_2")
    with pytest.raises(ValueError, match="does not let a criterion override"):
        rpr._write_pass_rule_from_card(run_dir, "run_d134_2", False)
    assert _pre_reg("run_d134_2") == before


# -- (d) the D-121 brief lint -------------------------------------------------------------------

def test_the_brief_lint_accepts_the_id_and_refuses_an_override():
    assert vce.lint_menu_shaped_pass_rule({"criteria": [{"id": CID}]}, MENU) == []
    resolved = vce.resolve_criteria_against_menu([{"id": CID}], MENU)
    assert vce.lint_menu_shaped_pass_rule({"criteria": resolved}, MENU) == []   # a restated copy
    (msg,) = vce.lint_menu_shaped_pass_rule({"criteria": [{"id": CID, "threshold": 0.05}]}, MENU)
    assert "does not let a criterion override" in msg


def test_a_flag_on_brief_naming_it_materializes_resolved(_sandbox_by_default):
    _set_orchestrator(ON)
    t51._seed_real_menu(_sandbox_by_default)
    camp._materialize_run("run_d134_3", t51._fresh_launch_brief({"criteria": [{"id": CID}]}))
    rule = _pre_reg("run_d134_3")["pass_rule"]
    assert rule == rpr._pass_rule_from_card({"criteria": [{"id": CID}]}, MENU, "t")
    with pytest.raises(ValueError, match="C5.1 menu lint"):
        camp._materialize_run("run_d134_4", t51._fresh_launch_brief(
            {"criteria": [{"id": CID, "threshold": 0.05}]}))
