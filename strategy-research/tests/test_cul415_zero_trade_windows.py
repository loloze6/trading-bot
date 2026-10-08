"""
CUL-415 (D-084; audit finding A8 in docs/DATA_DICTIONARY.md): a window with
no trades does not vote in the grid's window-source criteria, behind
orchestrator.zero_trade_windows_not_computed.enabled (off by default).

The engine writes 0.0 (not null) for the trade-based core fields of a window
without trades (net_return_pct, max_drawdown_pct, win_rate, ...). Flag off,
that 0.0 is a value: it votes in the sign_consistent_by_era era median and in
the scalar reducers, and counts toward floor.min_windows -- pinned here as
today's behaviour. Flag on, the window is skipped for a trade-based metric and
the cell records it in `skipped_windows`.

Synthetic protocol_result dicts only (no run, no backtest, no model call);
window labels in the train / walk-forward eras only.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import explore_confirm as ec  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

ON = {"zero_trade_windows_not_computed": True}


def _w(window: str, trade_count, symbol: str = "BTCUSDT", **core) -> dict:
    base = {"trade_count": trade_count, "net_return_pct": 0.0, "max_drawdown_pct": 0.0,
            "win_rate": 0.0, "sharpe": None, "forecast_return_corr": 0.1}
    base.update(core)
    return {"symbol": symbol, "window": window, "core": base}


def _era_pr() -> dict:
    """Era 2019-2023: +1.0 and two zero-trade windows (median 0.0 with them,
    +1.0 without); era 2024-2025: +1, +2, +3."""
    return {"results": [
        _w("2021-01", 10, net_return_pct=1.0),
        _w("2021-02", 0),
        _w("2021-03", 0),
        _w("2025-01", 10, net_return_pct=1.0),
        _w("2025-02", 10, net_return_pct=2.0),
        _w("2025-03", 10, net_return_pct=3.0),
    ]}


def _era_crit(min_windows: int = 4) -> dict:
    return {"id": "sign_consistent_by_era", "metric": "net_return_pct", "source": "window",
            "reducer": "sign_consistent_by_era", "symbol_reducer": None,
            "floor": {"min_windows": min_windows, "min_trades": 15}}


def _eras():
    return vce._load_campaign_data_policy_eras()


def _cell(crit, pr, **kw):
    return vce._evaluate_grid_cell(crit, pr, _eras(), **kw)


# ---------------------------------------------------------------------------
# sign_consistent_by_era
# ---------------------------------------------------------------------------

def test_flag_off_pins_todays_behaviour_zero_trade_window_votes():
    cell = _cell(_era_crit(), _era_pr())
    assert cell["result"] == "FAIL"
    assert cell["n_windows"] == 6
    assert cell["detail"]["era_medians"]["era_2019_2023_full_feed"] == 0.0
    assert "exactly zero" in cell["detail"]["reason"]
    assert "skipped_windows" not in cell


def test_flag_off_is_byte_identical_to_the_call_without_the_keyword():
    pr = _era_pr()
    for crit in (_era_crit(), _era_crit(5)):
        a = _cell(crit, pr)
        b = _cell(crit, pr, zero_trade_windows_not_computed=False)
        assert yaml.safe_dump(a) == yaml.safe_dump(b)


def test_flag_on_skips_zero_trade_windows_in_era_median_and_floor():
    pr = _era_pr()
    before = copy.deepcopy(pr)
    cell = _cell(_era_crit(), pr, **ON)
    assert pr == before, "the protocol_result must not be mutated"
    assert cell["result"] == "PASS"
    assert cell["n_windows"] == 4
    assert cell["n_trades"] == 40
    assert cell["detail"]["era_medians"] == {"era_2019_2023_full_feed": 1.0,
                                              "era_2024_2025_walk_forward_extension": 2.0}
    sk = cell["skipped_windows"]
    assert sk["count"] == 2
    assert sk["windows"] == ["BTCUSDT 2021-02", "BTCUSDT 2021-03"]
    assert sk["reason"] == vce.ZERO_TRADE_SKIP_REASON


def test_flag_on_below_floor_is_inconclusive_not_fail():
    off = _cell(_era_crit(5), _era_pr())
    assert off["result"] == "FAIL"  # 6 windows >= 5, the zero-trade 0.0 median fails
    on = _cell(_era_crit(5), _era_pr(), **ON)
    assert on["result"] == "INCONCLUSIVE"
    assert on["n_windows"] == 4
    assert on["reason"].startswith("n_windows=4 < floor.min_windows=5")
    assert "2 zero-trade window(s) not computed" in on["reason"]
    assert on["skipped_windows"]["count"] == 2


def test_flag_on_every_window_zero_trade_is_inconclusive():
    pr = {"results": [_w(f"2021-0{i}", 0) for i in range(1, 7)]}
    crit = _era_crit()
    crit["floor"] = {}
    off = _cell(crit, pr)
    assert off["result"] == "FAIL"
    on = _cell(crit, pr, **ON)
    assert on["result"] == "INCONCLUSIVE"
    assert on["n_windows"] == 0
    assert on["skipped_windows"]["count"] == 6


def test_evaluate_grid_idea_status_refuted_off_validated_on():
    pre_reg = {"pass_rule": {"criteria": [_era_crit()]}}
    off = vce.evaluate_grid({"base": _era_pr()}, pre_reg, None, None)
    same = vce.evaluate_grid({"base": _era_pr()}, pre_reg, None, None,
                             zero_trade_windows_not_computed=False)
    assert yaml.safe_dump(off) == yaml.safe_dump(same)
    assert off["idea_status"] == "refuted"
    on = vce.evaluate_grid({"base": _era_pr()}, pre_reg, None, None, **ON)
    assert on["idea_status"] == "validated"
    assert on["grid"]["sign_consistent_by_era"]["base"]["skipped_windows"]["count"] == 2


def test_per_symbol_all_records_skips_per_symbol():
    pr = _era_pr()
    pr["results"] += [_w(r["window"], r["core"]["trade_count"], symbol="ETHUSDT",
                         net_return_pct=r["core"]["net_return_pct"]) for r in _era_pr()["results"]]
    pr["results"][-1]["core"]["trade_count"] = 0  # ETH 2025-03: a third zero-trade window
    crit = {**_era_crit(), "symbol_reducer": "per_symbol_all"}
    on = _cell(crit, pr, **ON)
    assert on["per_symbol"]["BTCUSDT"]["skipped_windows"]["windows"] == [
        "BTCUSDT 2021-02", "BTCUSDT 2021-03"]
    assert on["per_symbol"]["ETHUSDT"]["skipped_windows"]["windows"] == [
        "ETHUSDT 2021-02", "ETHUSDT 2021-03", "ETHUSDT 2025-03"]
    assert on["per_symbol"]["ETHUSDT"]["n_windows"] == 3


# ---------------------------------------------------------------------------
# review fix (PR #349): skipping never removes an era from the vote
# ---------------------------------------------------------------------------

E2018 = "era_2018_pre_funding"
LOST_2018 = f"era {E2018}: every window had no trades -- the sign cannot be judged there"


def _lost_2018_pr(later=("2021-01", "2022-01", "2024-03", "2025-03")) -> dict:
    """2018: three zero-trade windows (its only windows); later eras trade, all
    positive."""
    return {"results": [_w("2018-03", 0), _w("2018-07", 0), _w("2018-11", 0)]
            + [_w(m, 10, net_return_pct=1.0 + i) for i, m in enumerate(later)]}


def test_review_scenario_1_lost_era_is_inconclusive_not_pass():
    # 2018 all zero-trade + trading windows in 2021 / 2022 / 2024 / 2025.
    crit = _era_crit()
    off = _cell(crit, _lost_2018_pr())
    assert off["result"] == "FAIL" and off["detail"]["era_medians"][E2018] == 0.0
    on = _cell(crit, _lost_2018_pr(), **ON)
    assert on["result"] == "INCONCLUSIVE"
    assert on["reason"].startswith(LOST_2018)
    assert "3 zero-trade window(s) not computed" in on["reason"]
    assert on["skipped_windows"]["eras_left_empty"] == [E2018]
    assert on["skipped_windows"]["count"] == 3
    assert E2018 not in on["detail"]["era_medians"]


def test_review_scenario_2_single_remaining_era_is_inconclusive_not_pass():
    # 2018 all zero-trade + 2021-2023 trading, single_era_inconclusive OFF.
    pr = _lost_2018_pr(later=("2021-01", "2022-01", "2023-01", "2023-06"))
    off = _cell(_era_crit(), pr)
    assert off["result"] == "FAIL"
    on = _cell(_era_crit(), pr, **ON)
    assert on["result"] == "INCONCLUSIVE"
    assert on["reason"].startswith(LOST_2018)
    assert list(on["detail"]["era_medians"]) == ["era_2019_2023_full_feed"]
    # with the single-era rule as well: still INCONCLUSIVE, the lost era named first
    both = _cell(_era_crit(), pr, single_era_inconclusive=True, **ON)
    assert both["result"] == "INCONCLUSIVE"
    assert both["reason"].startswith(LOST_2018 + "; single_era")


def test_every_era_keeps_a_window_behaves_as_before_the_review_fix():
    cell = _cell(_era_crit(), _era_pr(), **ON)
    assert cell["result"] == "PASS"
    assert cell["skipped_windows"]["eras_left_empty"] == []
    assert "reason" not in cell
    # the cell is exactly the pre-fix flag-on cell plus the empty eras_left_empty
    view = {"results": [e for e in _era_pr()["results"] if e["core"]["trade_count"] != 0]}
    bare = _cell(_era_crit(), view)
    sk = dict(cell["skipped_windows"])
    assert sk.pop("eras_left_empty") == []
    assert {k: v for k, v in cell.items() if k != "skipped_windows"} == bare
    assert sk == {"count": 2, "windows": ["BTCUSDT 2021-02", "BTCUSDT 2021-03"],
                  "reason": vce.ZERO_TRADE_SKIP_REASON}


def test_lost_era_with_remaining_eras_disagreeing_stays_fail():
    pr = _lost_2018_pr()
    pr["results"][-1]["core"]["net_return_pct"] = -5.0  # 2025 era negative
    off = _cell(_era_crit(), pr)
    on = _cell(_era_crit(), pr, **ON)
    assert off["result"] == "FAIL" and on["result"] == "FAIL"
    assert "disagree in sign" in on["detail"]["reason"]
    assert on["skipped_windows"]["eras_left_empty"] == [E2018]


def test_lost_era_below_floor_names_the_era_first():
    on = _cell(_era_crit(5), _lost_2018_pr(), **ON)
    assert on["result"] == "INCONCLUSIVE"
    assert on["reason"].startswith(LOST_2018 + "; n_windows=4 < floor.min_windows=5")


def test_era_not_compared_flag_off_is_not_counted_as_lost():
    # sharpe is null in a zero-trade window: flag off 2018 is not compared either.
    pr = {"results": [_w("2018-03", 0, sharpe=None), _w("2021-01", 10, sharpe=1.0),
                      _w("2025-01", 10, sharpe=2.0)]}
    crit = {**_era_crit(2), "metric": "sharpe"}
    off = _cell(crit, pr)
    on = _cell(crit, pr, **ON)
    assert off["result"] == on["result"] == "PASS"
    assert on["skipped_windows"] == {"count": 0, "windows": [], "eras_left_empty": [],
                                     "reason": vce.ZERO_TRADE_SKIP_REASON}


def test_scalar_reducers_carry_no_era_field():
    pr = {"results": [_w("2018-03", 0), _w("2021-01", 10, win_rate=55.0),
                      _w("2021-02", 10, win_rate=60.0)]}
    on = _cell(_scalar_crit("win_rate", "min", ">=", 40.0), pr, **ON)
    assert on["result"] == "PASS"
    assert "eras_left_empty" not in on["skipped_windows"]


def test_per_symbol_all_lost_era_is_judged_per_symbol():
    # BTC loses 2018 (only zero-trade windows there); ETH trades in 2018.
    pr = _lost_2018_pr()
    pr["results"] += [_w("2018-03", 10, symbol="ETHUSDT", net_return_pct=1.0),
                      _w("2021-01", 10, symbol="ETHUSDT", net_return_pct=1.0),
                      _w("2022-01", 10, symbol="ETHUSDT", net_return_pct=1.0),
                      _w("2025-03", 10, symbol="ETHUSDT", net_return_pct=1.0)]
    crit = {**_era_crit(), "symbol_reducer": "per_symbol_all"}
    on = _cell(crit, pr, **ON)
    assert on["per_symbol"]["BTCUSDT"]["result"] == "INCONCLUSIVE"
    assert on["per_symbol"]["BTCUSDT"]["skipped_windows"]["eras_left_empty"] == [E2018]
    assert on["per_symbol"]["ETHUSDT"]["result"] == "PASS"
    assert on["per_symbol"]["ETHUSDT"]["skipped_windows"]["eras_left_empty"] == []
    assert on["result"] == "INCONCLUSIVE"
    # pooled (symbol_reducer null): 2018 keeps ETH's trading window, nothing lost
    pooled = _cell(_era_crit(), pr, **ON)
    assert pooled["result"] == "PASS"
    assert pooled["skipped_windows"]["eras_left_empty"] == []


def test_per_symbol_all_symbol_with_only_zero_trade_windows_is_never_pass():
    pr = _era_pr()
    pr["results"] += [_w("2021-01", 0, symbol="ETHUSDT"), _w("2025-01", 0, symbol="ETHUSDT")]
    for crit in ({**_era_crit(2), "symbol_reducer": "per_symbol_all", "floor": {}},
                 {**_scalar_crit("win_rate", "min", ">=", 0.0), "symbol_reducer": "per_symbol_all",
                  "floor": {}}):
        on = _cell(crit, pr, **ON)
        eth = on["per_symbol"]["ETHUSDT"]
        assert eth["result"] == "INCONCLUSIVE"
        assert eth["n_windows"] == 0 and eth["skipped_windows"]["count"] == 2
        assert on["result"] in ("INCONCLUSIVE", "FAIL")


def test_evaluate_grid_lost_era_idea_status_inconclusive_not_validated():
    pre_reg = {"pass_rule": {"criteria": [_era_crit()]}}
    off = vce.evaluate_grid({"base": _lost_2018_pr()}, pre_reg, None, None)
    on = vce.evaluate_grid({"base": _lost_2018_pr()}, pre_reg, None, None, **ON)
    assert off["idea_status"] == "refuted"
    assert on["idea_status"] == "inconclusive"
    assert on["grid"]["sign_consistent_by_era"]["base"]["skipped_windows"]["eras_left_empty"] == [E2018]


# ---------------------------------------------------------------------------
# scalar reducers: drawdown flatters, win_rate penalises
# ---------------------------------------------------------------------------

def _scalar_crit(metric, reducer, comparator, threshold):
    return {"id": f"{metric}_{reducer}", "metric": metric, "source": "window",
            "reducer": reducer, "comparator": comparator, "threshold": threshold,
            "symbol_reducer": None, "floor": {"min_windows": 2}}


def test_drawdown_median_zero_trade_flatters_off_skipped_on():
    pr = {"results": [_w("2021-01", 10, max_drawdown_pct=-20.0),
                      _w("2021-02", 10, max_drawdown_pct=-20.0),
                      _w("2021-03", 0), _w("2021-04", 0), _w("2021-05", 0)]}
    crit = _scalar_crit("max_drawdown_pct", "median", ">=", -10.0)
    off = _cell(crit, pr)
    assert (off["result"], off["value"], off["n_windows"]) == ("PASS", 0.0, 5)
    on = _cell(crit, pr, **ON)
    assert (on["result"], on["value"], on["n_windows"]) == ("FAIL", -20.0, 2)
    assert on["skipped_windows"]["count"] == 3


def test_win_rate_min_zero_trade_penalises_off_skipped_on():
    pr = {"results": [_w("2021-01", 10, win_rate=55.0), _w("2021-02", 10, win_rate=60.0),
                      _w("2021-03", 0)]}
    crit = _scalar_crit("win_rate", "min", ">=", 40.0)
    off = _cell(crit, pr)
    assert (off["result"], off["value"]) == ("FAIL", 0.0)
    on = _cell(crit, pr, **ON)
    assert (on["result"], on["value"], on["n_windows"]) == ("PASS", 55.0, 2)


@pytest.mark.parametrize("reducer,arg,off_value,on_value", [
    ("mean", None, 20.0, 30.0),
    ("max", None, 40.0, 40.0),
    ("fraction_above", 10.0, 2 / 3, 1.0),
])
def test_other_scalar_reducers_skip_zero_trade_windows(reducer, arg, off_value, on_value):
    pr = {"results": [_w("2021-01", 10, win_rate=20.0), _w("2021-02", 10, win_rate=40.0),
                      _w("2021-03", 0)]}
    crit = {**_scalar_crit("win_rate", reducer, ">=", 0.0), "reducer_arg": arg}
    assert _cell(crit, pr)["value"] == pytest.approx(off_value)
    assert _cell(crit, pr, **ON)["value"] == pytest.approx(on_value)


def test_floor_drop_on_scalar_reducer_is_inconclusive():
    pr = {"results": [_w("2021-01", 10, win_rate=55.0), _w("2021-02", 0)]}
    on = _cell(_scalar_crit("win_rate", "min", ">=", 40.0), pr, **ON)
    assert on["result"] == "INCONCLUSIVE"
    assert "1 zero-trade window(s) not computed" in on["reason"]


# ---------------------------------------------------------------------------
# what the flag does NOT touch
# ---------------------------------------------------------------------------

def test_bar_level_metric_is_unchanged_under_the_flag():
    pr = {"results": [_w("2021-01", 10, forecast_return_corr=0.2),
                      _w("2021-02", 0, forecast_return_corr=-0.5),
                      _w("2025-01", 10, forecast_return_corr=0.3)]}
    crit = {**_era_crit(2), "metric": "forecast_return_corr"}
    assert "forecast_return_corr" not in vce.ZERO_TRADE_NOT_COMPUTED_FIELDS
    assert "trade_count" not in vce.ZERO_TRADE_NOT_COMPUTED_FIELDS
    assert yaml.safe_dump(_cell(crit, pr)) == yaml.safe_dump(_cell(crit, pr, **ON))


def test_missing_trade_count_is_not_treated_as_zero():
    pr = _era_pr()
    pr["results"][1]["core"]["trade_count"] = None
    on = _cell(_era_crit(), pr, **ON)
    assert on["skipped_windows"]["windows"] == ["BTCUSDT 2021-03"]
    assert on["n_windows"] == 5


def test_null_value_in_a_zero_trade_window_is_not_counted_as_skipped():
    # sharpe is already nulled below 5 trades by run_protocol: nothing to skip.
    pr = {"results": [_w("2021-01", 10, sharpe=1.0), _w("2021-02", 0, sharpe=None),
                      _w("2021-03", 10, sharpe=2.0)]}
    on = _cell(_scalar_crit("sharpe", "median", ">", 0.0), pr, **ON)
    assert on["skipped_windows"]["count"] == 0
    assert on["value"] == 1.5


def test_pooled_source_is_unchanged_under_the_flag():
    pr = {**_era_pr(), "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0}}}
    crit = {"id": "pooled_x", "metric": "median_sharpe", "source": "pooled",
            "comparator": ">", "threshold": 0.0, "symbol_reducer": None}
    assert yaml.safe_dump(_cell(crit, pr)) == yaml.safe_dump(_cell(crit, pr, **ON))


# ---------------------------------------------------------------------------
# exploration copy, flag reader, wiring
# ---------------------------------------------------------------------------

def test_exploration_grid_passes_the_keyword():
    pre_reg = {"pass_rule": {"criteria": [_era_crit()]}}
    grid_doc = {"criteria": ["sign_consistent_by_era"], "variants": ["base"]}
    shown = [r["window"] for r in _era_pr()["results"]]
    off = ec.exploration_grid(grid_doc, {"base": _era_pr()}, pre_reg, None, shown)
    same = ec.exploration_grid(grid_doc, {"base": _era_pr()}, pre_reg, None, shown,
                               zero_trade_windows_not_computed=False)
    assert yaml.safe_dump(off) == yaml.safe_dump(same)
    assert off["grid"]["sign_consistent_by_era"]["base"]["result"] == "FAIL"
    on = ec.exploration_grid(grid_doc, {"base": _era_pr()}, pre_reg, None, shown, **ON)
    assert on["grid"]["sign_consistent_by_era"]["base"]["result"] == "PASS"


def _cfg(value, grid=True):
    return {"orchestrator": {"zero_trade_windows_not_computed": {"enabled": value},
                             "grid_evaluation": {"enabled": grid}}}


def test_flag_reader():
    assert rpr._zero_trade_windows_not_computed_enabled({}) is False
    assert rpr._zero_trade_windows_not_computed_enabled({"orchestrator": {}}) is False
    assert rpr._zero_trade_windows_not_computed_enabled(_cfg(False, grid=False)) is False
    assert rpr._zero_trade_windows_not_computed_enabled(_cfg(True)) is True
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._zero_trade_windows_not_computed_enabled(_cfg("true"))
    with pytest.raises(ValueError, match="requires orchestrator.grid_evaluation"):
        rpr._zero_trade_windows_not_computed_enabled(_cfg(True, grid=False))


def test_real_config_has_the_flag_off():
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["zero_trade_windows_not_computed"]["enabled"] is False
    assert rpr._zero_trade_windows_not_computed_enabled(cfg) is False


def test_grid_kw_is_empty_flag_off(monkeypatch):
    monkeypatch.setattr(rpr, "_zero_trade_windows_not_computed_enabled", lambda cfg=None: False)
    assert rpr._zero_trade_grid_kw() == {}
    monkeypatch.setattr(rpr, "_zero_trade_windows_not_computed_enabled", lambda cfg=None: True)
    assert rpr._zero_trade_grid_kw() == ON


def test_every_grid_call_site_carries_the_keyword():
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    assert src.count("**_zero_trade_grid_kw())") == 4
    assert src.count("_vce.evaluate_grid(") == 3
    assert src.count("ec.exploration_grid(") == 1


def test_flag_is_in_the_launch_preflight():
    readers = camp._flag_readers()
    assert readers["zero_trade_windows_not_computed"] is rpr._zero_trade_windows_not_computed_enabled
