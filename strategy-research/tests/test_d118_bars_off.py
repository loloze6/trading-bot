"""D-118: a profit bar can be OFF (null in config/profitability_bars.yaml): it is removed
from the verdict -- no row at all, never a lowered threshold, never a NOT_EVALUABLE row
(which would cap the verdict). trade_count_min and cost_edge_ratio_min may be off;
cost_edge_min_trades goes with the cost bar, trade_count_min_floor with both. sharpe_min
is compared strictly (> threshold)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tests"))
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import test_e062_s2b1_profit_bars_v2 as t62  # noqa: E402  (run builders and bars)

OFF = {"trade_count_min": None, "cost_edge_ratio_min": None, "cost_edge_min_trades": None,
       "trade_count_min_floor": None}
D118 = {**t62.V2_BARS, **OFF, "sharpe_min": 0.0, "deflated_sharpe_threshold": 0.5}


def _write(tmp_path, doc):
    p = tmp_path / "bars.yaml"
    p.write_text(yaml.safe_dump(doc), encoding="utf-8")
    return p


# -- the loader -----------------------------------------------------------------------

def test_both_loaders_accept_the_d118_file(tmp_path):
    p = _write(tmp_path, D118)
    for v2 in (False, True):
        doc = rpr._load_profitability_bars(p, v2=v2)
        assert doc["trade_count_min"] is None and doc["sharpe_min"] == 0.0


@pytest.mark.parametrize("change, match", [
    ({"cost_edge_min_trades": 100}, "must both be null"),               # floor of an off bar
    ({"cost_edge_ratio_min": 2.2}, "must both be null"),                # bar on, floor null
    ({"trade_count_min_floor": 60}, "null exactly when both"),          # floor with nothing to floor
    ({"trade_count_min": 100}, "null exactly when both"),               # a base on, floor null
    ({"sharpe_min": None}, "wrong-typed"),                              # only the two may be off
    ({"deflated_sharpe_threshold": None}, "wrong-typed"),
])
def test_the_loader_refuses_an_inconsistent_off(tmp_path, change, match):
    with pytest.raises(rpr.ProfitabilityBarsSchemaError, match=match):
        rpr._load_profitability_bars(_write(tmp_path, {**D118, **change}), v2=True)


def test_one_bar_on_one_off_loads(tmp_path):
    doc = {**D118, "trade_count_min": 100, "trade_count_min_floor": 60}
    assert rpr._load_profitability_bars(_write(tmp_path, doc), v2=True)["trade_count_min"] == 100


# -- the v2 rows ------------------------------------------------------------------------

def test_off_bars_have_no_row_and_the_others_decide(tmp_path):
    run_dir = tmp_path / "run"
    pr = t62._build(run_dir)
    rows, overall, reasons, ordered = t62._rows(pr, run_dir, bars=D118)
    assert [r["name"] for r in ordered] == ["sharpe_min", "deflated_sharpe_threshold",
                                            "max_drawdown_pct_max", "avg_daily_return_min",
                                            "buy_and_hold_excess_return_min"]
    assert overall == "PASS" and reasons == []


def test_an_off_bar_is_never_computed(tmp_path):
    """The cost row is not computed at all (cost_edge_min_trades is null): no records needed."""
    run_dir = tmp_path / "run"
    pr = t62._build(run_dir, trades_file=False)
    metrics = t62._metrics(pr, run_dir, D118)
    assert "trade_count_min" not in metrics and "cost_edge_ratio_min" not in metrics


def test_with_the_bars_on_nothing_changes(tmp_path):
    run_dir = tmp_path / "run"
    pr = t62._build(run_dir)
    rows, overall, _r, ordered = t62._rows(pr, run_dir, bars=t62.V2_BARS)
    assert [r["name"] for r in ordered] == t62.ROW_ORDER


@pytest.mark.parametrize("actual, result", [(0.0, "FAIL"), (1e-9, "PASS"), (-0.5, "FAIL")])
def test_sharpe_min_is_strict(tmp_path, actual, result):
    metrics = {n: {"actual": 1.0, "note": "", "not_evaluable_reason": None, "detail": {}}
               for n in t62.ROW_ORDER if n != "deflated_sharpe_threshold"}
    metrics["sharpe_min"]["actual"] = actual
    results, _o, _r = rpr._grade_profit_bars_v2(D118, dsr=0.9, dsr_note="t", metrics=metrics)
    assert {r["name"]: r["result"] for r in results}["sharpe_min"] == result


# -- the v1 rows (flag off) ----------------------------------------------------------------

def test_v1_rows_skip_an_off_trade_count_and_sharpe_is_strict():
    results, _o, _r = rpr._grade_profit_bars(
        {**D118}, sharpe=0.0, sharpe_note="t", dsr=0.9, dsr_note="t",
        pss={"BTCUSDT": {"max_abs_drawdown_pct": 5.0, "min_trade_count": 3}})
    names = {r["name"]: r["result"] for r in results}
    assert "trade_count_min" not in names and names["sharpe_min"] == "FAIL"


# -- D-047 normalisation and the holdout spend -----------------------------------------------

def test_normalisation_only_touches_the_bars_that_are_on():
    eff, norm = rpr._normalised_profit_bars(D118, (60, 120))
    assert set(norm) == {"max_drawdown_pct_max"}
    assert eff["trade_count_min"] is None and eff["cost_edge_min_trades"] is None


def test_the_spend_cost_basis_check_has_nothing_to_check_without_a_cost_row(monkeypatch):
    monkeypatch.setattr(rpr, "_cost_bar_all_costs_enabled", lambda: True)
    entry = {"bars": [{"name": "sharpe_min", "result": "PASS"}]}
    assert rpr._cost_basis_at_spend("base", entry) is None
    with pytest.raises(rpr.HoldoutUnlockRefused):  # a cost row graded fee-only still refuses
        rpr._cost_basis_at_spend("base", {"bars": [{"name": "cost_edge_ratio_min", "detail": {}}]})


def test_the_spend_rederivation_skips_off_bars(tmp_path):
    """A full-coverage variant graded under D-118 has no trade-count or cost row; the
    spend's re-derivation checks only the drawdown row then (and still checks it)."""
    entry = {"bars": [{"name": "max_drawdown_pct_max", "threshold": 20.0, "detail": {}}]}
    assert rpr._normalisation_at_spend(tmp_path, "run_x", "base", entry, D118) is None
    bad = {"bars": [{"name": "max_drawdown_pct_max", "threshold": 25.0, "detail": {}}]}
    with pytest.raises(rpr.HoldoutUnlockRefused, match="bars_changed"):
        rpr._normalisation_at_spend(tmp_path, "run_x", "base", bad, D118)


def test_only_the_two_offable_bars_can_be_dropped_by_the_grader():
    """A null on any other bar is never read as 'off' (the loader refuses it; the grader
    does not drop the row either)."""
    assert rpr._PROFIT_BARS_OFFABLE == ("trade_count_min", "cost_edge_ratio_min")
    for name in ("sharpe_min", "deflated_sharpe_threshold", "max_drawdown_pct_max",
                 "avg_daily_return_min", "buy_and_hold_excess_return_min"):
        assert rpr._bar_is_off({**D118, name: None}, name) is False
