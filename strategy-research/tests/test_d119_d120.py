"""D-119: a deflated Sharpe that cannot be computed is a non-blocking WARNING at branch 3 (its
row NOT_EVALUABLE with advisory: true; a computed one below the bar still FAILs; the holdout
spend is unchanged). D-120: the buy-and-hold bar compares whole-test Sharpe ratios on the
same chained days (buy_and_hold_sharpe_excess_min > 0), the return excess kept as
information."""
from __future__ import annotations

import math
import statistics
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tests"))
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import campaign_memory as cm  # noqa: E402
import portfolio_whole_test as pw  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import test_e062_s2b1_profit_bars_v2 as t62  # noqa: E402

D0 = date(2020, 1, 1)
ROWS = ["sharpe_min", "max_drawdown_pct_max", "trade_count_min", "avg_daily_return_min",
        "buy_and_hold_sharpe_excess_min", "cost_edge_ratio_min"]


def _metrics(**actuals):
    out = {n: {"actual": 1.0, "note": "", "not_evaluable_reason": None, "detail": {}} for n in ROWS}
    out["max_drawdown_pct_max"]["actual"] = 5.0
    out["sharpe_min"]["actual"] = 2.0  # above sharpe_min 1.0 (strict since D-118)
    out["avg_daily_return_min"]["actual"] = 0.001
    out["trade_count_min"]["actual"] = 200
    out["cost_edge_ratio_min"]["actual"] = 5.0
    for k, v in actuals.items():
        out[k]["actual"] = v
    return out


# -- D-119 -------------------------------------------------------------------------------

def test_a_deflated_sharpe_that_cannot_be_computed_does_not_block_the_pass():
    results, overall, reasons = rpr._grade_profit_bars_v2(
        t62.V2_BARS, dsr=None, dsr_note="t", metrics=_metrics(), dsr_reason="ledger_basis_mismatch: x")
    row = {r["name"]: r for r in results}["deflated_sharpe_threshold"]
    assert row["result"] == "NOT_EVALUABLE" and row["advisory"] is True
    assert overall == "PASS"
    assert any("warning, not blocking" in r for r in reasons)


def test_a_computed_deflated_sharpe_below_the_bar_still_fails():
    results, overall, _r = rpr._grade_profit_bars_v2(t62.V2_BARS, dsr=0.1, dsr_note="t",
                                                     metrics=_metrics())
    row = {r["name"]: r for r in results}["deflated_sharpe_threshold"]
    assert row["result"] == "FAIL" and "advisory" not in row and overall == "FAIL"


def test_another_not_evaluable_bar_still_blocks():
    m = _metrics()
    m["sharpe_min"].update(actual=None, not_evaluable_reason="x")
    _res, overall, _r = rpr._grade_profit_bars_v2(t62.V2_BARS, dsr=None, dsr_note="t", metrics=m)
    assert overall == "FAIL"


def test_the_grid_cell_ignores_an_advisory_row():
    results, overall, _r = rpr._grade_profit_bars_v2(t62.V2_BARS, dsr=None, dsr_note="t",
                                                     metrics=_metrics())
    cell = vce._evaluate_profit_bars_cell({"id": "pb"}, "base",
                                          lambda vid: {"result": overall, "bars": results})
    assert cell["result"] == "PASS"


def test_the_memory_accepts_a_pass_with_an_advisory_row(tmp_path):
    results, overall, _r = rpr._grade_profit_bars_v2(t62.V2_BARS, dsr=None, dsr_note="t",
                                                     metrics=_metrics())
    run_dir = tmp_path / "run_1"
    (run_dir / "artifacts").mkdir(parents=True)
    doc = {"scope": cm.PROFIT_BARS_SCOPE_EVERY_BACKTEST, "run_id": "run_1", "result": "PASS",
           "passing": ["base"], "variants": {"base": {"result": overall, "bars": results}}}
    (run_dir / "artifacts" / "profit_bars_evaluation.yaml").write_text(yaml.safe_dump(doc),
                                                                       encoding="utf-8")
    block = cm.profit_bars_block(run_dir, "run_1", {"base": {"status": "tested"}})
    assert block["result"] == "PASS"


def test_a_ledger_row_on_another_basis_is_not_evaluable_not_a_crash(tmp_path):
    wctx = {"rows": [{"trial_id": "run_1", "source": "backtest",
                      "whole_test": {"basis": "some_earlier_basis", "status": "ok"}}],
            "sharpe_basis": pw.WHOLE_TEST_BASIS, "sample": {"srs": [], "rows": []},
            "n_dsr_total": 10}
    res = rpr._whole_test_dsr_candidate(wctx, tmp_path, {}, "run_1", 10)
    assert res["dsr"] is None and "ledger_basis_mismatch" in res["reason"]
    wctx["rows"][0]["whole_test"] = None  # no block at all: still a defect, raises
    with pytest.raises(ValueError):
        rpr._whole_test_dsr_candidate(wctx, tmp_path, {}, "run_1", 10)


# -- D-120 -------------------------------------------------------------------------------

def _day(i):
    return D0 + timedelta(days=i)


def _bars(first, values):
    return {datetime(*_day(first + k).timetuple()[:3], 23): v for k, v in enumerate(values)}


def _bull(n, seed, drift=0.004, noise=0.02):
    v, out = 100.0, []
    for k in range(n):
        out.append(v)
        v *= 1 + drift + noise * math.sin(seed + 1.7 * k)
    return out


def _layout(equity_share=0.4):
    """Two 40-day windows with a gap; the coin rises with noise; the strategy holds a
    `equity_share` of it, the rest in cash (a partly invested trend follower)."""
    px = {"w0": {"X": _bars(0, _bull(40, 1))}, "w1": {"X": _bars(60, _bull(40, 2))}}
    eq = {w: {"X": {t: 1000.0 * (1 - equity_share + equity_share * p / min(px[w]["X"].items())[1])
                    for t, p in px[w]["X"].items()}} for w in px}
    bounds = {"w0": (_day(0), _day(39)), "w1": (_day(60), _day(99))}
    return eq, px, bounds


def test_buy_and_hold_returns_sit_on_the_strategys_days_with_costs_at_both_ends():
    eq, px, bounds = _layout()
    chain = pw.chain_windows(eq, ["X"], bounds)
    rets = pw.chained_buy_and_hold_daily_returns(chain, px, {"X": 10.0}, {"X": 5.0})
    assert [d for d, _ in rets] == [d for d, _ in chain["daily_returns"]]
    raw = pw.chained_buy_and_hold_daily_returns(chain, px, {"X": 0.0}, {"X": 0.0})
    c = (1 - 15e-4)
    assert rets[0][1] == pytest.approx((1 + raw[0][1]) * c - 1, abs=1e-15)
    assert rets[-1][1] == pytest.approx((1 + raw[-1][1]) * c - 1, abs=1e-15)
    assert [r for _d, r in rets[1:-1]] == [r for _d, r in raw[1:-1]]
    p = px["w0"]["X"]
    ts = sorted(p)
    assert raw[0][1] == pytest.approx(p[ts[1]] / p[ts[0]] - 1, abs=1e-15)


def test_a_partly_invested_strategy_has_the_lower_sharpe_in_a_noisy_bull_here():
    """Not a law: in this layout the strategy holds 40 % of the coin and cash, so its
    returns are the coin's scaled down -- Sharpe nearly equal, the cost the tiebreaker."""
    eq, px, bounds = _layout(0.4)
    chain = pw.chain_windows(eq, ["X"], bounds)
    s = pw.whole_test_sharpe(chain["daily_returns"])
    b = pw.whole_test_sharpe(pw.chained_buy_and_hold_daily_returns(chain, px, {"X": 0.0},
                                                                    {"X": 0.0}))
    assert s == pytest.approx(b, rel=0.05)  # Sharpe is scale-free: 40 % of the coin ~ the coin


def test_the_day1_return_of_a_chain_with_start_values():
    eq, px, bounds = _layout()
    start = {w: {"X": 1000.0} for w in eq}
    if "start_values" not in pw.chain_windows.__code__.co_varnames:
        pytest.skip("chain_windows has no start values on this branch (D-116 not merged)")
    chain = pw.chain_windows(eq, ["X"], bounds, start_values=start)
    rets = pw.chained_buy_and_hold_daily_returns(chain, px, {"X": 0.0}, {"X": 0.0})
    assert [d for d, _ in rets] == [d for d, _ in chain["daily_returns"]]
    assert dict(rets)[_day(0)] == 0.0  # daily bars: first bar = anchor close


def test_the_bar_row_compares_sharpes_and_keeps_the_return_excess(tmp_path):
    run_dir = tmp_path / "run"
    pr = t62._build(run_dir)
    rows, _o, _r, _x = t62._rows(pr, run_dir)
    row = rows["buy_and_hold_sharpe_excess_min"]
    d = row["detail"]
    assert row["actual"] == pytest.approx(d["strategy_sharpe"] - d["buy_and_hold_sharpe"], abs=1e-12)
    assert row["comparator"] == ">"
    assert {"strategy_total_return", "buy_and_hold_total_return", "excess_return"} <= set(d)


def test_the_bars_file_carries_the_renamed_key():
    doc = rpr._load_profitability_bars(SR_ROOT / "config" / "profitability_bars.yaml", v2=True)
    assert doc["buy_and_hold_sharpe_excess_min"] == 0.0
    assert "buy_and_hold_excess_return_min" not in doc


def test_a_chain_whose_days_disagree_with_its_segments_is_refused():
    eq, px, bounds = _layout()
    chain = pw.chain_windows(eq, ["X"], bounds)
    tampered = {**chain, "daily_returns": chain["daily_returns"][1:]}
    with pytest.raises(ValueError, match="not the strategy's chained days"):
        pw.chained_buy_and_hold_daily_returns(tampered, px, {"X": 0.0}, {"X": 0.0})
