"""E-078 item 1 (D-127): the branch-3 trade-frequency bar, `trade_frequency_min` in
config/profitability_bars.yaml (v2): trades / backtest bars >= X, pooled over every coin
and window of a run. Trades = trade_diagnostics.json's lots without the end_of_window
forced close (D-035's rule); bars = each (coin, window) backtest's bars. The key is
optional: absent (or null) = no row, grading byte-identical to before.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tests"))
sys.path.insert(0, str(SR / "workflow"))

import run_phase1_research as rpr  # noqa: E402
import test_e062_s2b1_profit_bars_v2 as t62  # noqa: E402

# _build's default windows W1 2020-01-01..01-31 and W2 2020-02-01..02-29 (tail 1 day off
# the protocol's end), two bars a day (11:00 and 23:00): 62 + 58 = 120 bars per coin;
# 59 signal trades and 1 end_of_window close per coin-window.
BARS_PER_COIN = 2 * 31 + 2 * 29
WITH = {**t62.V2_BARS, "trade_frequency_min": 0.01}


def _rows(run_dir, bars, **build):
    pr = t62._build(run_dir, **build)
    return t62._rows(pr, run_dir, bars=bars)


def test_absent_or_null_key_has_no_row_and_grades_exactly_as_before(tmp_path):
    base = _rows(tmp_path / "a", t62.V2_BARS)
    null = _rows(tmp_path / "b", {**t62.V2_BARS, "trade_frequency_min": None})
    assert "trade_frequency_min" not in base[0] and "trade_frequency_min" not in null[0]
    strip = lambda rs: [{k: v for k, v in r.items() if k not in ("note", "detail")} for r in rs]  # noqa: E731
    assert strip(base[3]) == strip(null[3]) and base[1] == null[1]
    assert [r["name"] for r in base[3]] == t62.ROW_ORDER


def test_the_value_is_pooled_trades_without_window_closes_over_backtest_bars(tmp_path):
    rows, overall, _reasons, results = _rows(tmp_path / "r", WITH, coins=("BTCUSDT", "ETHUSDT"))
    row = rows["trade_frequency_min"]
    assert row["actual"] == pytest.approx((59 * 2 * 2) / (BARS_PER_COIN * 2))
    assert row["detail"] == {"trades": 236, "bars": 240, "end_of_window": 4, "n_coin_windows": 4}
    assert row["basis"] == "pooled_trades_excl_window_closes_per_backtest_bar"
    assert row["comparator"] == ">=" and row["result"] == "PASS"
    assert results[-1]["name"] == "trade_frequency_min"  # appended after the existing rows


def test_window_end_closes_are_not_counted(tmp_path):
    one = _rows(tmp_path / "a", WITH, n_eow=1)[0]["trade_frequency_min"]["actual"]
    five = _rows(tmp_path / "b", WITH, n_eow=5)[0]["trade_frequency_min"]["actual"]
    assert one == five == pytest.approx(118 / BARS_PER_COIN)


@pytest.mark.parametrize("n_signal, result", [(1, "FAIL"), (2, "PASS")])
def test_the_boundary_is_inclusive(tmp_path, n_signal, result):
    """Threshold 2/120 (= 1/60): 2 trades over 120 bars sits exactly on it and PASSes;
    1 trade FAILs. The trades are put in the first window only."""
    import json
    bars = {**t62.V2_BARS, "trade_frequency_min": 2 / BARS_PER_COIN}
    run_dir = tmp_path / "r"
    pr = t62._build(run_dir, n_signal=0, n_eow=1)
    pr["results"][0]["core"]["trade_count"] = n_signal + 1
    p = run_dir / "trade_diagnostics.json"
    doc = json.loads(p.read_text(encoding="utf-8"))
    doc["trades"] += [t62._trade("BTCUSDT", "w1", "signal_flip", 0.45, 15.0)] * n_signal
    p.write_text(json.dumps(doc), encoding="utf-8")
    got = t62._rows(pr, run_dir, bars=bars)[0]["trade_frequency_min"]
    assert got["actual"] == pytest.approx(n_signal / BARS_PER_COIN)
    assert got["result"] == result


def test_a_failing_frequency_fails_the_variant(tmp_path):
    rows, overall, reasons, _ = _rows(tmp_path / "r", {**t62.V2_BARS, "trade_frequency_min": 0.99})
    assert rows["trade_frequency_min"]["result"] == "FAIL" and overall == "FAIL"
    assert any(r.startswith("trade_frequency_min: FAIL") for r in reasons)


def test_records_that_do_not_match_the_results_read_not_evaluable(tmp_path):
    rows = _rows(tmp_path / "r", WITH, trades_file=False)[0]
    row = rows["trade_frequency_min"]
    assert row["result"] == "NOT_EVALUABLE" and row["actual"] is None
    assert row["not_evaluable_reason"].startswith("trade frequency NOT_EVALUABLE")


def test_no_trade_at_all_reads_zero_and_fails(tmp_path):
    rows = _rows(tmp_path / "r", WITH, n_signal=0, n_eow=0)[0]
    assert rows["trade_frequency_min"]["actual"] == 0 and rows["trade_frequency_min"]["result"] == "FAIL"


@pytest.mark.parametrize("value, ok", [(0.01, True), (1, True), (None, True), (0, False),
                                       (1.5, False), (-0.1, False), (True, False), ("1%", False)])
def test_the_loader_checks_the_key_only_when_present(value, ok):
    t62._write_bars({**t62.V2_BARS, "trade_frequency_min": value})
    if ok:
        assert rpr._load_profitability_bars(v2=True)["trade_frequency_min"] == value
    else:
        with pytest.raises(rpr.ProfitabilityBarsSchemaError, match="trade_frequency_min"):
            rpr._load_profitability_bars(v2=True)
    t62._write_bars(t62.V2_BARS)
    assert "trade_frequency_min" not in rpr._load_profitability_bars(v2=True)
    assert "trade_frequency_min" not in rpr._load_profitability_bars(v2=False)  # v1: untouched


def test_the_committed_bars_file_carries_the_key():
    """D-127: one bars-file edit with the leave-one-block-out bar (re-sign by the operator)."""
    doc = yaml.safe_load((SR / "config" / "profitability_bars.yaml").read_text(encoding="utf-8"))
    assert doc["trade_frequency_min"] == 0.01  # D-127: the bars-file edit (re-sign pending)


def test_no_backtest_bar_reads_not_evaluable_never_a_division(tmp_path):
    run_dir = tmp_path / "r"
    pr = t62._build(run_dir, n_signal=0, n_eow=0)
    for f in run_dir.glob("results/*/portfolio_states.csv"):
        f.write_text("timestamp,regime,postRebalance_total_value,total_portfolio_value,close\n"
                     "2019-12-31 23:00:00,NOT_READY,1.0,1.0,1.0\n", encoding="utf-8")
    freq = rpr._trade_frequency(run_dir, pr, {"BTCUSDT": {"excluding_end_of_window": 0,
                                                          "end_of_window": 0}})
    assert freq["bars"] == 0 and freq["reason"] == "no backtest bar in any window"


def test_a_missing_equity_file_reads_not_evaluable(tmp_path):
    run_dir = tmp_path / "r"
    pr = t62._build(run_dir)
    next(run_dir.glob("results/*/portfolio_states.csv")).unlink()
    freq = rpr._trade_frequency(run_dir, pr, {"BTCUSDT": {"excluding_end_of_window": 1,
                                                          "end_of_window": 0}})
    assert freq["reason"].startswith("no portfolio_states.csv for BTCUSDT")
