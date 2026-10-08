"""
CUL-414 (D-082; audit finding A7, docs/DATA_DICTIONARY.md): the D-038 "survives
2x costs" bar (ratio > 2.2) counts fees AND slippage, behind
orchestrator.cost_bar_all_costs.enabled (off by default).

Flag off, the ratio divides realized_return (from the FILL prices, so already
net of slippage) by cost_paid (the configured fee x 2, no slippage). Flag on,
both D-038 bars compare the gross edge BEFORE fees and slippage
(gross_return_before_costs, at the bar closes the fills were priced from) with
fees + slippage, both legs (cost_paid_all).

Covers:
  1. run_protocol._all_costs_fields on synthetic LONG and SHORT trades whose
     fee and slippage are known (hand-computed values), and None when a leg's
     bar is missing.
  2. The ratio (cost_helpers) equals the hand-computed value; the BTC-like
     28 bps trade (Kraken perp: 5 bps fee and 2.5 bps slippage a side) PASSES
     the bar today and FAILS it flag on.
  3. Flag off is byte-identical: trade records, the summary, the grid, the
     pooled bar, run_protocol's arguments and the evaluate_grid keywords.
  4. Flag on: records gain three fields after the existing ones (existing
     values unchanged); the summary gains realized_edge_to_cost_ratio_all_costs;
     the menu criterion reads it; profit_bars_v2's cost row uses the new fields;
     a record without them is NOT_EVALUABLE / INCONCLUSIVE, never fee-only.
  5. The flag: off in the shipped config, registered everywhere, non-bool
     refused; a holdout spend refuses a cost row graded on another basis.

No LLM, no backtest, no market data.
"""
import csv
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import cost_helpers as ch  # noqa: E402
import portfolio_whole_test as pwt  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import run_protocol as rp  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

FLAG_ON = {"cost_bar_all_costs": {"enabled": True}}
FLAG_OFF = {"cost_bar_all_costs": {"enabled": False}}
NEW_FIELDS = ["gross_return_before_costs", "slippage_paid", "cost_paid_all"]
# The record keys, in order, before CUL-414 (tools/run_protocol.py at origin/master
# 309e9eb6) -- flag off they must stay exactly these.
OLD_KEYS = [
    "trade_id", "symbol", "window", "regime_at_entry", "direction", "entry_time", "exit_time",
    "holding_bars", "realized_return", "profitable_net", "net_portfolio_return_pct", "mae",
    "mfe", "entry_efficiency", "exit_efficiency", "exit_reason", "post_exit_return_5bars",
    "post_exit_return_20bars", "cost_paid", "entry_price", "exit_price", "entry_idx",
    "exit_idx", "pre_entry_drift_pct", "entered_earlier_better", "post_exit_drift_pct",
    "held_longer_better",
]


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# Synthetic trades, priced the way MockExecutionHandler prices them:
# buy = close * (1 + s), sell = close * (1 - s).
# ---------------------------------------------------------------------------

BTC_FEE, BTC_SLIP = 5.0, 2.5      # Kraken perp: fee one way, slippage one way (bps)
SOL_FEE, SOL_SLIP = 5.0, 7.5


def _fills(side, ref_in, ref_out, slip_bps):
    s = slip_bps / 1e4
    if side == "LONG":
        return ref_in * (1 + s), ref_out * (1 - s)
    return ref_in * (1 - s), ref_out * (1 + s)


def _engine_return_pct(side, entry, exit_):
    """PM:CompletedTrade.profit_loss_percent (realized_return)."""
    return (exit_ / entry - 1) * 100 if side == "LONG" else (1 - exit_ / entry) * 100


def _bars(*closes):
    return [{"timestamp": f"2020-01-01 0{i}:00:00", "close": c} for i, c in enumerate(closes)]


def test_all_costs_fields_long_btc_hand_computed():
    # entry close 100, exit close 100.28: 28 bps before costs.
    e, x = _fills("LONG", 100.0, 100.28, BTC_SLIP)
    f = rp._all_costs_fields("LONG", e, x, _bars(100.0, 100.28), 0, 1, 2 * BTC_FEE)
    assert list(f) == NEW_FIELDS
    assert f["gross_return_before_costs"] == pytest.approx(0.28, abs=1e-6)
    assert f["slippage_paid"] == pytest.approx(5.0, abs=1e-6)       # 2.5 + 2.5
    assert f["cost_paid_all"] == pytest.approx(15.0, abs=1e-6)      # 10 fee + 5 slippage


def test_all_costs_fields_short_sol_hand_computed():
    # short from close 50 to close 49: 200 bps before costs.
    e, x = _fills("SHORT", 50.0, 49.0, SOL_SLIP)
    f = rp._all_costs_fields("SHORT", e, x, _bars(50.0, 49.0), 0, 1, 2 * SOL_FEE)
    assert f["gross_return_before_costs"] == pytest.approx(2.0, abs=1e-6)
    assert f["slippage_paid"] == pytest.approx(15.0, abs=1e-6)      # 7.5 + 7.5
    assert f["cost_paid_all"] == pytest.approx(25.0, abs=1e-6)      # 10 fee + 15 slippage


@pytest.mark.parametrize("entry_idx, exit_idx, bars", [
    (-1, 1, _bars(100.0, 101.0)),          # entry bar not found
    (0, 5, _bars(100.0, 101.0)),           # exit index past the bars
    (0, 1, _bars(100.0, None)),            # a missing close
    (0, 1, _bars(0.0, 101.0)),             # a non-positive close
])
def test_all_costs_fields_none_when_a_leg_has_no_reference_close(entry_idx, exit_idx, bars):
    f = rp._all_costs_fields("LONG", 100.0, 101.0, bars, entry_idx, exit_idx, 10.0)
    assert f == {k: None for k in NEW_FIELDS}


def _record(side, ref_in, ref_out, fee, slip, reason="signal_flip"):
    e, x = _fills(side, ref_in, ref_out, slip)
    rec = {"symbol": "BTCUSD", "window": "w1", "exit_reason": reason,
           "realized_return": round(_engine_return_pct(side, e, x), 4),
           "cost_paid": 2 * fee}
    rec.update(rp._all_costs_fields(side, e, x, _bars(ref_in, ref_out), 0, 1, 2 * fee))
    return rec


def test_ratio_equals_the_hand_computed_value():
    long_btc = _record("LONG", 100.0, 100.28, BTC_FEE, BTC_SLIP)    # 28 bps / 15 bps
    short_sol = _record("SHORT", 50.0, 49.0, SOL_FEE, SOL_SLIP)     # 200 bps / 25 bps
    assert ch.edge_to_all_costs_ratio_unrounded([long_btc]) == pytest.approx(28 / 15, rel=1e-6)
    assert ch.edge_to_all_costs_ratio_unrounded([short_sol]) == pytest.approx(8.0, rel=1e-6)
    # pooled: mean gross / mean cost = (28 + 200) / 2 / ((15 + 25) / 2) = 5.7
    assert ch.edge_to_all_costs_ratio_unrounded([long_btc, short_sol]) \
        == pytest.approx(5.7, rel=1e-6)
    assert ch.edge_to_all_costs_ratio([long_btc]) == round(28 / 15, 4) == 1.8667
    # a record without the fields is left out of numerator and denominator
    assert ch.edge_to_all_costs_ratio_unrounded(
        [long_btc, {**short_sol, "cost_paid_all": None}]) == pytest.approx(28 / 15, rel=1e-6)
    assert ch.edge_to_all_costs_ratio_unrounded([]) is None
    assert ch.edge_to_all_costs_ratio_unrounded([{**long_btc, "cost_paid_all": 0.0}]) is None


def test_28_bps_btc_trade_passes_today_and_fails_with_all_costs():
    """The reviewer's case, recomputed from the code: a BTC trade 28 bps up
    between the two bar closes, Kraken perp costs (5 bps fee, 2.5 bps slippage
    a side). Its fill-to-fill return is ~22.99 bps, so today's ratio is
    ~22.99 / 10 = 2.299 > 2.2 (PASS); with all costs it is 28 / 15 = 1.867
    (FAIL). Today's bar passes BTC above ~22 + 5 = 27 bps before costs; the
    flag-on bar above 2.2 x 15 = 33 bps (SOL/UNI: 22 + 15 = 37 vs 2.2 x 25 = 55)."""
    recs = [_record("LONG", 100.0, 100.28, BTC_FEE, BTC_SLIP) for _ in range(100)]
    assert recs[0]["realized_return"] == pytest.approx(0.2299, abs=1e-4)
    off = pwt.pooled_edge_to_cost_ratio(recs, 100)
    on = pwt.pooled_edge_to_cost_ratio(recs, 100, all_costs=True)
    assert off["ratio"] == pytest.approx(2.299, abs=1e-3) and off["ratio"] > 2.2
    assert on["ratio"] == pytest.approx(28 / 15, rel=1e-6) and not on["ratio"] > 2.2
    assert "cost_basis" not in off and on["cost_basis"] == "fees_and_slippage"
    # 34 bps before costs passes flag on (34/15 = 2.267), 33 does not (strict >)
    assert pwt.pooled_edge_to_cost_ratio(
        [_record("LONG", 100.0, 100.34, BTC_FEE, BTC_SLIP)] * 100, 100,
        all_costs=True)["ratio"] > 2.2
    assert not pwt.pooled_edge_to_cost_ratio(
        [_record("LONG", 100.0, 100.33, BTC_FEE, BTC_SLIP)] * 100, 100,
        all_costs=True)["ratio"] > 2.2 + 1e-9


def test_pooled_all_costs_refuses_records_without_the_fields():
    recs = [_record("LONG", 100.0, 100.28, BTC_FEE, BTC_SLIP) for _ in range(100)]
    bare = [{k: v for k, v in r.items() if k not in NEW_FIELDS} for r in recs]
    with pytest.raises(pwt.PortfolioNotEvaluable, match="fees \\+ slippage.*lack a measured"):
        pwt.pooled_edge_to_cost_ratio(bare, 100, all_costs=True)
    one_none = [dict(r) for r in recs]
    one_none[3]["gross_return_before_costs"] = None
    with pytest.raises(pwt.PortfolioNotEvaluable, match="1 of 100"):
        pwt.pooled_edge_to_cost_ratio(one_none, 100, all_costs=True)
    # flag off ignores the new fields entirely
    assert pwt.pooled_edge_to_cost_ratio(bare, 100) == pwt.pooled_edge_to_cost_ratio(recs, 100)
    bad = [dict(r) for r in recs]
    bad[0]["cost_paid_all"] = -1.0
    with pytest.raises(ValueError, match="cost_paid_all"):
        pwt.pooled_edge_to_cost_ratio(bad, 100, all_costs=True)


# ---------------------------------------------------------------------------
# run_protocol end to end on a tmp window (bars.csv + trades.json)
# ---------------------------------------------------------------------------

def _write_window(run_dir: Path):
    run_dir.mkdir()
    closes = [100.0, 100.0, 100.28, 100.5, 49.0, 50.0, 49.0, 48.0]
    with open(run_dir / "bars.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["timestamp", "open", "high", "low", "close"])
        w.writeheader()
        for i, c in enumerate(closes):
            w.writerow({"timestamp": f"2020-01-01 0{i}:00:00", "open": c, "high": c * 1.001,
                        "low": c * 0.999, "close": c})
    trades = []
    for tid, side, i_in, i_out, slip in (("t1", "LONG", 1, 2, BTC_SLIP),
                                         ("t2", "SHORT", 5, 6, SOL_SLIP)):
        e, x = _fills(side, closes[i_in], closes[i_out], slip)
        trades.append({
            "trade_id": tid, "symbol": "BTCUSD", "side": side, "entry_price": e,
            "exit_price": x, "entry_time": f"2020-01-01T0{i_in}:00:00",
            "exit_time": f"2020-01-01T0{i_out}:00:00", "duration_minutes": 60.0,
            "profit_loss_percent": _engine_return_pct(side, e, x),
            "net_portfolio_profit_loss_percent": 0.1, "profitable_net": True,
            "exit_forecast": 0.0, "total_commission_percent": 0.1})
    (run_dir / "trades.json").write_text(json.dumps(trades), encoding="utf-8")


def test_trade_records_flag_off_byte_identical_and_flag_on_additive(tmp_path):
    run_dir = tmp_path / "run"
    _write_window(run_dir)
    args = (run_dir, "BTCUSD", "w1", "2020-01-02", None)
    default = rp._compute_trade_records_for_window(*args, commission_bps=5.0)
    off = rp._compute_trade_records_for_window(*args, commission_bps=5.0, cost_bar_all_costs=False)
    on = rp._compute_trade_records_for_window(*args, commission_bps=5.0, cost_bar_all_costs=True)
    assert json.dumps(default) == json.dumps(off)
    assert all(list(r) == OLD_KEYS for r in off)
    assert all(list(r) == OLD_KEYS + NEW_FIELDS for r in on)
    for r_off, r_on in zip(off, on):  # existing fields keep their values
        assert {k: r_on[k] for k in OLD_KEYS} == r_off
    t1, t2 = on
    assert t1["cost_paid"] == 10.0 and t1["cost_paid_all"] == pytest.approx(15.0, abs=1e-6)
    assert t1["gross_return_before_costs"] == pytest.approx(0.28, abs=1e-6)
    assert t2["cost_paid_all"] == pytest.approx(25.0, abs=1e-6)
    assert t2["gross_return_before_costs"] == pytest.approx(2.0, abs=1e-6)

    results = [{"core": {"trade_count": 2}}]
    s_default = rp._aggregate_trade_diagnostics(off, results, None)
    s_off = rp._aggregate_trade_diagnostics(off, results, None, cost_bar_all_costs=False)
    s_on = rp._aggregate_trade_diagnostics(on, results, None, cost_bar_all_costs=True)
    assert json.dumps(s_default) == json.dumps(s_off)
    assert "realized_edge_to_cost_ratio_all_costs" not in s_off
    assert list(s_on) == list(s_off) + ["realized_edge_to_cost_ratio_all_costs"]
    assert {k: s_on[k] for k in s_off} == s_off  # existing summary values unchanged
    assert s_on["realized_edge_to_cost_ratio_all_costs"] == round(114 / 20, 4) == 5.7


def test_run_protocol_cli_passes_the_flag_only_when_given():
    src = (SR_ROOT / "tools" / "run_protocol.py").read_text(encoding="utf-8")
    assert src.count('"--cost-bar-all-costs"') == 1
    assert src.count('**({"cost_bar_all_costs": True} if args.cost_bar_all_costs else {})') == 2


# ---------------------------------------------------------------------------
# The menu criterion (evaluate_grid)
# ---------------------------------------------------------------------------

MENU = yaml.safe_load((SR_ROOT / "config" / "criterion_menu.yaml").read_text(encoding="utf-8"))
PRE_REG = {"pass_rule": {"criteria": [{"id": "realized_edge_to_cost_ratio", "source": "pooled"}]}}


def _protocol_result(summary: dict) -> dict:
    return {"results": [{"symbol": "BTCUSD", "window": f"w{k}", "core": {"trade_count": 30}}
                        for k in range(5)],
            "trade_diagnostics_summary": summary}


def _cell(pr, **kw):
    g = vce.evaluate_grid({"base": pr}, PRE_REG, None, MENU, **kw)
    return g, g["grid"]["realized_edge_to_cost_ratio"]["base"]


def test_grid_reads_the_all_costs_field_only_under_the_flag():
    pr = _protocol_result({"realized_edge_to_cost_ratio": 2.299,
                           "realized_edge_to_cost_ratio_all_costs": 1.8667})
    g_default, c_default = _cell(pr)
    g_off, c_off = _cell(pr, cost_bar_all_costs=False)
    assert json.dumps(g_default, default=str) == json.dumps(g_off, default=str)
    assert c_off["result"] == "PASS" and c_off["value"] == 2.299
    _g_on, c_on = _cell(pr, cost_bar_all_costs=True)
    assert c_on["result"] == "FAIL" and c_on["value"] == 1.8667 and c_on["threshold"] == 2.2


def test_grid_flag_on_without_the_field_is_inconclusive_never_fee_only():
    _g, cell = _cell(_protocol_result({"realized_edge_to_cost_ratio": 9.0}),
                     cost_bar_all_costs=True)
    assert cell["result"] == "INCONCLUSIVE"
    assert "realized_edge_to_cost_ratio_all_costs" in cell["reason"]


# ---------------------------------------------------------------------------
# profit_bars_v2's cost row (reuses the S2b-1 fixture builders)
# ---------------------------------------------------------------------------

def _graded_cost_row(tmp_path, orchestrator, *, with_fields=True):
    import test_e062_s2b1_profit_bars_v2 as s2b1
    run_dir = tmp_path / "run"
    # fee 7.5 a side (the fixture's cost model), 1 bp slippage a side: 36 bps
    # before costs, ~34 bps fill to fill: today 34/15 = 2.27 (PASS), all costs
    # 36/17 = 2.12 (FAIL).
    pr = s2b1._build(run_dir, rr=0.34, cost=15.0)
    if with_fields:
        path = run_dir / "trade_diagnostics.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        for t in doc["trades"]:
            t.update(gross_return_before_costs=0.36, slippage_paid=2.0, cost_paid_all=17.0)
        path.write_text(json.dumps(doc), encoding="utf-8")
    _set_orchestrator(orchestrator)
    rows, _o, _r, _x = s2b1._rows(pr, run_dir)
    return rows["cost_edge_ratio_min"]


def test_profit_bar_cost_row_flag_off_unchanged(tmp_path):
    row_absent = _graded_cost_row(tmp_path / "a", None)
    row_off = _graded_cost_row(tmp_path / "b", FLAG_OFF)
    row_bare = _graded_cost_row(tmp_path / "c", FLAG_OFF, with_fields=False)
    assert row_absent == row_off == row_bare
    assert row_off["result"] == "PASS" and row_off["actual"] == pytest.approx(34 / 15)
    assert "cost_basis" not in row_off["detail"]


def test_profit_bar_cost_row_flag_on_counts_slippage(tmp_path):
    row = _graded_cost_row(tmp_path, FLAG_ON)
    assert row["result"] == "FAIL" and row["actual"] == pytest.approx(36 / 17)
    assert row["detail"]["cost_basis"] == "fees_and_slippage"
    assert "fees + slippage" in row["note"]


def test_profit_bar_cost_row_flag_on_without_the_fields_is_not_evaluable(tmp_path):
    row = _graded_cost_row(tmp_path, FLAG_ON, with_fields=False)
    assert row["result"] == "NOT_EVALUABLE"
    assert "--cost-bar-all-costs" in row["not_evaluable_reason"]


# ---------------------------------------------------------------------------
# The flag and its wiring
# ---------------------------------------------------------------------------

def test_flag_reader_default_off_and_strict_bool():
    _set_orchestrator(None)
    assert rpr._cost_bar_all_costs_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert shipped["orchestrator"]["cost_bar_all_costs"]["enabled"] is False
    assert rpr._cost_bar_all_costs_enabled(shipped) is False
    _set_orchestrator(FLAG_ON)
    assert rpr._cost_bar_all_costs_enabled() is True
    for bad in ("true", "false", 1, None):
        _set_orchestrator({"cost_bar_all_costs": {"enabled": bad}})
        with pytest.raises(ValueError, match="not a real boolean"):
            rpr._cost_bar_all_costs_enabled()


def test_flag_off_adds_no_argument_and_no_keyword():
    for orch in (None, FLAG_OFF):
        _set_orchestrator(orch)
        assert rpr._cost_bar_args() == [] and rpr._cost_bar_grid_kw() == {}
    _set_orchestrator(FLAG_ON)
    assert rpr._cost_bar_args() == ["--cost-bar-all-costs"]
    assert rpr._cost_bar_grid_kw() == {"cost_bar_all_costs": True}


def test_every_run_protocol_call_and_grid_call_carries_the_flag():
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    n_calls = src.count('str(ROOT / "tools" / "run_protocol.py")')
    assert n_calls == 2
    assert src.count("*cost_bar_args,") + src.count("*_cost_bar_args(),") == n_calls
    assert src.count("_vce.evaluate_grid(") == src.count("**_cost_bar_grid_kw()") == 3


def test_flag_registered_everywhere():
    import run_campaign as camp
    sys.path.insert(0, str(Path(__file__).parent))
    import test_e061_end_to_end_wiring as wiring
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(
        encoding="utf-8"))
    [entry] = [f for f in reg["flags"] if f["name"] == "cost_bar_all_costs"]
    assert entry["config_key"] == "orchestrator.cost_bar_all_costs.enabled"
    assert entry["reader"] == "run_phase1_research._cost_bar_all_costs_enabled"
    assert entry["state"] == "off_incomplete" and entry["blocked_on"]
    assert camp._flag_readers()["cost_bar_all_costs"] is rpr._cost_bar_all_costs_enabled
    assert wiring.TARGET_FLAGS["cost_bar_all_costs"] is False


def _entry(cost_basis=None):
    detail = {"min_trades": 100, **({"cost_basis": cost_basis} if cost_basis else {})}
    return {"bars": [{"name": "cost_edge_ratio_min", "result": "PASS", "detail": detail}]}


def test_holdout_spend_refuses_a_cost_row_graded_on_another_basis():
    _set_orchestrator(None)
    rpr._cost_basis_at_spend("base", _entry())  # fee-only graded, flag off: unchanged
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._cost_basis_at_spend("base", _entry("fees_and_slippage"))
    assert exc.value.code == "bars_changed"
    _set_orchestrator(FLAG_ON)
    rpr._cost_basis_at_spend("base", _entry("fees_and_slippage"))
    with pytest.raises(rpr.HoldoutUnlockRefused) as exc:
        rpr._cost_basis_at_spend("base", _entry())  # passed fee-only, flag now on
    assert exc.value.code == "bars_changed" and "fees only" in exc.value.detail
    _set_orchestrator({"cost_bar_all_costs": {"enabled": "yes"}})
    with pytest.raises(rpr.HoldoutUnlockRefused, match="does not read"):
        rpr._cost_basis_at_spend("base", _entry())
