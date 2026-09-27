"""E-062 S2a -- whole-test portfolio functions (tools/portfolio_whole_test.py).

Pure functions, nothing wired: chain_windows (G1/G2), whole_test_max_drawdown
(D-034), whole_test_sharpe (G3), whole_test_trade_counts (G5),
chained_buy_and_hold (G6) and pooled_edge_to_cost_ratio (G7). Every expected
number below is computed by hand in the test's docstring or inline arithmetic,
never read back from the function under test. All dates are synthetic 2020
dates.
"""
from __future__ import annotations

import hashlib
import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "workflow"))

import portfolio_daily as pdv1  # noqa: E402
import portfolio_whole_test as pw  # noqa: E402

NE = pdv1.PortfolioNotEvaluable
D0 = date(2020, 1, 1)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _day(i: int) -> date:
    return D0 + timedelta(days=i)


def _bars(first: int, closes: list, intraday: dict | None = None) -> dict:
    """{datetime: value}: day `first + k` gets a 23:00 bar carrying closes[k];
    intraday {k: [v01, v02, ...]} adds bars at 01:00, 02:00, ... that day."""
    out = {}
    for k, v in enumerate(closes):
        d = _day(first + k)
        for h, x in enumerate((intraday or {}).get(k, [])):
            out[datetime(d.year, d.month, d.day, h + 1)] = x
        out[datetime(d.year, d.month, d.day, 23)] = v
    return out


def _skip_days(bars: dict, days: set) -> dict:
    return {t: v for t, v in bars.items() if t.date() not in days}


def _v1_pooled_returns(windows: dict, coins: list) -> list:
    """Today's (v1) pooled daily returns, results order."""
    out = []
    for win, by_coin in windows.items():
        wc = pdv1.window_common_curve(win, by_coin, coins)
        out.extend(pdv1.consecutive_daily_returns(wc["common"], wc["curve"])[0])
    return out


def _write_states(root: Path, run_id: str, equity: dict, close: dict | None = None,
                  warmup: bool = True) -> None:
    d = root / "results" / run_id
    d.mkdir(parents=True, exist_ok=True)
    lines = ["timestamp,regime,postRebalance_total_value,close"]
    if warmup:
        lines.append("2019-12-31 22:00:00,NOT_READY,999999.0,-1")
    for t in sorted(equity):
        c = (close or {}).get(t, 1.0)
        lines.append(f"{t:%Y-%m-%d %H:%M:%S},trend,{equity[t]!r},{c!r}")
    (d / "portfolio_states.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _rpr():
    import run_phase1_research as rpr  # heavy import, only where the v1 drawdown is needed
    return rpr


# Three contiguous monthly-style windows, one-day overlap (end == next start),
# two coins with non-trivial paths. Window k covers days [10k, 10k+10].
def _contiguous_layout() -> dict:
    wins = {}
    for k in range(3):
        a = [100.0 * (1.0 + 0.01 * ((i * 7 + k) % 5 - 2)) * (1.0 + 0.003 * i) for i in range(11)]
        b = [50.0 * (1.0 + 0.02 * ((i * 3 + k) % 4 - 1.5)) for i in range(11)]
        wins[f"w{k}"] = {"A": _bars(10 * k, a), "B": _bars(10 * k, b)}
    return wins


# ---------------------------------------------------------------------------
# G1: chaining
# ---------------------------------------------------------------------------

def test_contiguous_one_day_overlap_reproduces_v1_pooled_returns_exactly():
    """The S1 finding: on the one-day-overlap layout every protocol has, the
    chained daily returns ARE today's pooled daily returns -- same days, same
    floats (==, not approx)."""
    wins = _contiguous_layout()
    ch = pw.chain_windows(wins, ["A", "B"])
    assert ch["daily_returns"] == _v1_pooled_returns(wins, ["A", "B"])
    assert len(ch["daily_returns"]) == 30  # 3 windows x 10 returns, day 0 is the anchor
    assert [s["kind"] for s in ch["segments"]] == ["first", "junction", "junction"]
    assert ch["n_gap_days"] == 0 and ch["n_gap_links"] == 0 and ch["n_multi_day_steps"] == 0
    assert ch["first_day"] == _day(0) and ch["last_day"] == _day(30)
    assert ch["coverage"] == 31 / 31
    days = [d for d, _r in ch["daily_returns"]]
    assert days == [_day(i) for i in range(1, 31)]


def test_contiguous_layout_through_the_real_readers_matches_v1_file_path(tmp_path):
    """load_windows (v1 reader) -> chain_windows gives the same returns as v1's
    portfolio_daily_returns on the same portfolio_states.csv files."""
    wins = _contiguous_layout()
    results = []
    for win, by_coin in wins.items():
        for coin, bars in by_coin.items():
            rid = f"{coin}-{win}"
            _write_states(tmp_path, rid, bars)
            results.append({"symbol": coin, "window": win, "run_id": rid})
    pr = {"results": results}
    windows, coins = pdv1.load_windows(tmp_path, pr)
    ch = pw.chain_windows(windows, coins)
    assert ch["daily_returns"] == pdv1.portfolio_daily_returns(tmp_path, pr)


def test_chained_levels_multiply_across_junctions():
    """One coin. w0 days 0..2: 100, 110, 121 (level 1.0, 1.1, 1.21). w1 days
    2..4: 1000, 900, 990 (joins at day 2, scale 1.21/1.0; levels day 3 =
    1.21 * 0.9 = 1.089, day 4 = 1.21 * 0.99 = 1.1979)."""
    ch = pw.chain_windows({"w0": {"X": _bars(0, [100.0, 110.0, 121.0])},
                           "w1": {"X": _bars(2, [1000.0, 900.0, 990.0])}}, ["X"])
    lv = dict(ch["daily_levels"])
    assert lv[_day(0)] == 1.0
    assert lv[_day(3)] == pytest.approx(1.21 * 0.9, rel=1e-12)
    assert lv[_day(4)] == pytest.approx(1.21 * 0.99, rel=1e-12)
    assert [r for _d, r in ch["daily_returns"]] == pytest.approx([0.1, 0.1, -0.1, 0.1])


def test_out_of_order_windows_give_the_same_chain_as_sorted():
    wins = _contiguous_layout()
    rev = {k: wins[k] for k in reversed(list(wins))}
    a, b = pw.chain_windows(wins, ["A", "B"]), pw.chain_windows(rev, ["A", "B"])
    assert a["daily_returns"] == b["daily_returns"]
    assert a["bar_levels"] == b["bar_levels"]
    assert [s["window"] for s in b["segments"]] == ["w0", "w1", "w2"]


def test_gap_is_linked_flat_and_not_counted():
    """w0 days 0..19, w1 days 21..40 (day 20 missing from both). The chain is
    flat from day 19 to day 21 (level unchanged), no return on day 21, one gap
    day. Returns 19 + 19 = 38; calendar 0..40 = 41 days; coverage 39/41."""
    w0 = [100.0 + i for i in range(20)]
    w1 = [500.0 * (1.0 + 0.001 * i) for i in range(20)]
    ch = pw.chain_windows({"w0": {"X": _bars(0, w0)}, "w1": {"X": _bars(21, w1)}}, ["X"])
    assert [s["kind"] for s in ch["segments"]] == ["first", "gap"]
    assert ch["n_gap_days"] == 1 and ch["n_gap_links"] == 1
    lv = dict(ch["daily_levels"])
    assert lv[_day(21)] == pytest.approx(lv[_day(19)], rel=1e-15)
    ret_days = [d for d, _r in ch["daily_returns"]]
    assert _day(20) not in ret_days and _day(21) not in ret_days
    assert len(ret_days) == 38
    assert ch["coverage"] == 39 / 41
    # the bar curve is flat across the gap too: the first w1 bar equals the last w0 bar
    bars = ch["bar_levels"]
    i = next(k for k, (t, _v) in enumerate(bars) if t.date() == _day(21))
    assert bars[i][1] == pytest.approx(bars[i - 1][1], rel=1e-15)


def test_long_gap_fails_whole_test_coverage():
    """w0 days 0..9, w1 days 15..24: returns 9 + 9 = 18, calendar 25 days,
    (18 + 1) / 25 = 0.76 < 0.9 -> NOT_EVALUABLE (each window alone is fine)."""
    with pytest.raises(NE, match="WHOLE_TEST_MIN_COVERAGE"):
        pw.chain_windows({"w0": {"X": _bars(0, [100.0] * 9 + [101.0])},
                          "w1": {"X": _bars(15, [100.0] * 9 + [99.0])}}, ["X"])


def test_overlap_longer_than_one_day_keeps_the_earliest_windows_days():
    """w0 days 0..10, w1 days 7..20 (4 shared days: 7, 8, 9, 10). w0 keeps days
    up to 10; w1 joins at day 10 and contributes days 11..20. The return on day
    11 is w1's v(11)/v(10) - 1; days 8..10 come from w0."""
    w0 = [100.0 * 1.01 ** i for i in range(11)]
    w1 = [70.0 + 3.0 * ((i * 5) % 7) for i in range(14)]  # day 7+i
    ch = pw.chain_windows({"w0": {"X": _bars(0, w0)}, "w1": {"X": _bars(7, w1)}}, ["X"])
    seg = ch["segments"][1]
    assert seg["kind"] == "overlap" and seg["join_day"] == _day(10)
    rets = dict(ch["daily_returns"])
    assert sorted(rets) == [_day(i) for i in range(1, 21)]
    assert rets[_day(9)] == pytest.approx(0.01)            # from w0
    assert rets[_day(11)] == pytest.approx(w1[4] / w1[3] - 1.0)  # w1: day 11 / day 10
    # w1's bars up to and including its day-10 close are not in the chain: one
    # bar per day (w0's) on the shared days 7..10
    for i in (7, 8, 9, 10):
        assert len([t for t, _v in ch["bar_levels"] if t.date() == _day(i)]) == 1
    lv = dict(ch["daily_levels"])
    assert dict(ch["bar_levels"])[datetime(2020, 1, 11, 23)] == pytest.approx(lv[_day(10)])


def test_missing_junction_day_is_treated_as_a_gap():
    """w0 days 0..10; w1 would start on day 10 but lacks it (first bar day 11).
    Not NOT_EVALUABLE (G1 decision): a gap link at day 11 with 0 missing
    calendar days, and no return on day 11."""
    ch = pw.chain_windows({"w0": {"X": _bars(0, [100.0 + i for i in range(11)])},
                           "w1": {"X": _bars(11, [200.0 + i for i in range(10)])}}, ["X"])
    seg = ch["segments"][1]
    assert seg["kind"] == "gap" and seg["join_day"] == _day(11)
    assert ch["n_gap_links"] == 1 and ch["n_gap_days"] == 0
    assert _day(11) not in dict(ch["daily_returns"])
    assert len(ch["daily_returns"]) == 10 + 9


def test_missing_junction_day_inside_a_longer_overlap_is_a_gap():
    """w0 days 0..10; w1 days 7..20 without day 10: w1 joins at day 11."""
    w1 = _skip_days(_bars(7, [300.0 + i for i in range(14)]), {_day(10)})
    ch = pw.chain_windows({"w0": {"X": _bars(0, [100.0 + i for i in range(11)])},
                           "w1": {"X": w1}}, ["X"])
    seg = ch["segments"][1]
    assert seg["kind"] == "gap" and seg["join_day"] == _day(11)
    assert _day(11) not in dict(ch["daily_returns"])


def test_window_inside_an_earlier_window_contributes_nothing():
    ch = pw.chain_windows({"w0": {"X": _bars(0, [100.0 + i for i in range(21)])},
                           "w1": {"X": _bars(5, [1.0, 2.0, 3.0])}}, ["X"])
    assert ch["segments"][1]["kind"] == "contained"
    assert len(ch["daily_returns"]) == 20
    assert all(t.date() <= _day(20) for t, _v in ch["bar_levels"])


def test_duplicate_anchor_is_not_evaluable():
    with pytest.raises(NE, match="share the anchor day"):
        pw.chain_windows({"w0": {"X": _bars(0, [1.0, 2.0])},
                          "w1": {"X": _bars(0, [1.0, 2.0, 3.0])}}, ["X"])


def test_two_coins_common_day_drop():
    """B lacks day 5 of 0..20: day 5 dropped for both (per-window coverage
    20/21 >= 0.9); the day-4 -> day-6 step is a multi-day step, not a return.
    Returns 20 - 2 = 18; whole-test coverage (18 + 1) / 21 = 0.905 >= 0.9."""
    a = _bars(0, [100.0 + i for i in range(21)])
    b = _skip_days(_bars(0, [50.0 + 2 * i for i in range(21)]), {_day(5)})
    ch = pw.chain_windows({"w0": {"A": a, "B": b}}, ["A", "B"])
    rd = [d for d, _r in ch["daily_returns"]]
    assert _day(5) not in rd and _day(6) not in rd and len(rd) == 18
    assert ch["n_multi_day_steps"] == 1
    assert ch["coverage"] == 19 / 21
    assert ch["daily_returns"] == _v1_pooled_returns({"w0": {"A": a, "B": b}}, ["A", "B"])


def test_whole_test_coverage_counts_return_days_so_it_is_stricter_than_per_window():
    """S1 Q1.6's whole-span rule counts RETURN days (+1): one dropped day inside
    a window costs two counted days. An 11-day window missing one day passes
    v1's per-window floor (10/11) but not the chained span ((8 + 1)/11)."""
    a = _bars(0, [100.0 + i for i in range(11)])
    b = _skip_days(_bars(0, [50.0 + 2 * i for i in range(11)]), {_day(5)})
    pdv1.window_common_curve("w0", {"A": a, "B": b}, ["A", "B"])  # v1: passes
    with pytest.raises(NE, match="8 daily return"):
        pw.chain_windows({"w0": {"A": a, "B": b}}, ["A", "B"])


def test_per_window_coverage_below_floor_is_not_evaluable():
    """B lacks 2 of 10 days: 8 / 10 = 0.8 < 0.9 -- v1's per-window floor."""
    a = _bars(0, [100.0] * 10)
    b = _skip_days(_bars(0, [100.0] * 10), {_day(4), _day(5)})
    with pytest.raises(NE, match="PORTFOLIO_MIN_COMMON_DAY_COVERAGE"):
        pw.chain_windows({"w0": {"A": a, "B": b}}, ["A", "B"])


def test_coin_set_differs_is_not_evaluable():
    with pytest.raises(NE, match="has coins"):
        pw.chain_windows({"w0": {"A": _bars(0, [1.0, 2.0])}}, ["A", "B"])
    with pytest.raises(NE, match="no windows"):
        pw.chain_windows({}, ["A"])


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), 0.0, -1.0, True, "1.0"])
def test_degenerate_values_raise(bad):
    bars = _bars(0, [100.0, 101.0, 102.0])
    bars[datetime(2020, 1, 2, 23)] = bad
    with pytest.raises(ValueError) as ei:
        pw.chain_windows({"w0": {"X": bars}}, ["X"])
    assert not isinstance(ei.value, NE)


def test_unsorted_timestamps_raise():
    bars = _bars(0, [100.0, 101.0, 102.0])
    unsorted = dict(reversed(list(bars.items())))
    with pytest.raises(ValueError, match="strictly increasing") as ei:
        pw.chain_windows({"w0": {"X": unsorted}}, ["X"])
    assert not isinstance(ei.value, NE)


def test_non_datetime_or_aware_timestamp_raises():
    from datetime import timezone
    with pytest.raises(ValueError, match="not a datetime"):
        pw.chain_windows({"w0": {"X": {"2020-01-01 23:00": 1.0}}}, ["X"])
    with pytest.raises(ValueError, match="naive"):
        pw.chain_windows({"w0": {"X": {datetime(2020, 1, 1, 23, tzinfo=timezone.utc): 1.0}}},
                         ["X"])


def test_duplicate_coins_raise():
    with pytest.raises(ValueError, match="without duplicates"):
        pw.chain_windows({"w0": {"X": _bars(0, [1.0, 2.0])}}, ["X", "X"])


# ---------------------------------------------------------------------------
# D-034: drawdown
# ---------------------------------------------------------------------------

def test_drawdown_spanning_two_windows_is_found_where_v1_misses_it(tmp_path):
    """One coin. w0 days 0..3: 100, 120, 115, 110 (peak 1.2, ends 1.1: w0's own
    drawdown 1 - 1.1/1.2 = 8.33%). w1 days 3..5: 1000, 950, 900 (its own
    drawdown 10%). Chained: 1.1 * 0.9 = 0.99 at day 5 against the 1.2 peak ->
    100 * (1 - 0.99/1.2) = 17.5%. v1 reports the worst window: 10%."""
    w0, w1 = _bars(0, [100.0, 120.0, 115.0, 110.0]), _bars(3, [1000.0, 950.0, 900.0])
    ch = pw.chain_windows({"w0": {"X": w0}, "w1": {"X": w1}}, ["X"])
    dd = pw.whole_test_max_drawdown(ch)
    assert dd["max_drawdown_pct"] == pytest.approx(17.5, rel=1e-12)
    assert dd["peak_ts"] == datetime(2020, 1, 2, 23) and dd["trough_ts"] == datetime(2020, 1, 6, 23)
    for rid, bars in (("X-w0", w0), ("X-w1", w1)):
        _write_states(tmp_path, rid, bars)
    pr = {"results": [{"symbol": "X", "window": "w0", "run_id": "X-w0"},
                      {"symbol": "X", "window": "w1", "run_id": "X-w1"}]}
    v1 = _rpr()._portfolio_profit_metrics(tmp_path, pr)["max_drawdown_pct"][0]
    assert v1 == round(10.0, 6)
    assert dd["max_drawdown_pct"] > v1


def test_drawdown_within_one_window_equals_v1(tmp_path):
    """Two coins, intraday bars (the intraday dip counts on the bar basis).
    A: 100 / 120 / (01:00 80, close 90) / 96; B: 100 / 100 / (01:00 110,
    close 110) / 99. Portfolio bars: 1.0, 1.1, 0.95 (the 01:00 dip), 1.0,
    0.975 -> 100 * (1 - 0.95/1.1) = 13.63..%. On a single window the chained
    bar curve IS v1's per-window bar curve: v1 reports the same number."""
    a = _bars(0, [100.0, 120.0, 90.0, 96.0], intraday={2: [80.0]})
    b = _bars(0, [100.0, 100.0, 110.0, 99.0], intraday={2: [110.0]})
    ch = pw.chain_windows({"w1": {"A": a, "B": b}}, ["A", "B"])
    dd = pw.whole_test_max_drawdown(ch)["max_drawdown_pct"]
    assert dd == pytest.approx(100.0 * (1.0 - 0.95 / 1.1), rel=1e-12)
    for rid, bars in (("A-w1", a), ("B-w1", b)):
        _write_states(tmp_path, rid, bars)
    pr = {"results": [{"symbol": "A", "window": "w1", "run_id": "A-w1"},
                      {"symbol": "B", "window": "w1", "run_id": "B-w1"}]}
    v1 = _rpr()._portfolio_profit_metrics(tmp_path, pr)["max_drawdown_pct"][0]
    assert round(dd, 6) == v1


def test_drawdown_of_monotone_curve_is_zero_and_bad_chain_raises():
    ch = pw.chain_windows({"w0": {"X": _bars(0, [1.0, 2.0, 3.0])}}, ["X"])
    assert pw.whole_test_max_drawdown(ch)["max_drawdown_pct"] == 0.0
    with pytest.raises(ValueError):
        pw.whole_test_max_drawdown({"bar_levels": []})
    with pytest.raises(ValueError, match="strictly increasing"):
        pw.whole_test_max_drawdown({"bar_levels": [(datetime(2020, 1, 2), 1.0),
                                                   (datetime(2020, 1, 1), 1.0)]})
    with pytest.raises(ValueError):
        pw.whole_test_max_drawdown({"bar_levels": [(datetime(2020, 1, 1), float("nan"))]})


# ---------------------------------------------------------------------------
# G3: Sharpe
# ---------------------------------------------------------------------------

def _rets(values: list) -> list:
    return [(_day(i + 1), v) for i, v in enumerate(values)]


def test_sharpe_hand_computed():
    """15 x 0.02 and 15 x 0.0: mean 0.01, every deviation 0.01, sample variance
    30 * 1e-4 / 29, so Sharpe = 0.01 / (0.01 * sqrt(30/29)) * sqrt(365)
    = sqrt(365 * 29 / 30) = 18.7838..."""
    s = pw.whole_test_sharpe(_rets([0.02, 0.0] * 15))
    assert s == pytest.approx(math.sqrt(365 * 29 / 30), rel=1e-12)
    assert s == pytest.approx(18.78385, abs=1e-5)


def test_sharpe_from_a_chain_uses_the_chained_daily_returns():
    wins = _contiguous_layout()
    ch = pw.chain_windows(wins, ["A", "B"])
    r = [x for _d, x in ch["daily_returns"]]
    m = sum(r) / len(r)
    sd = math.sqrt(sum((x - m) ** 2 for x in r) / (len(r) - 1))
    assert pw.whole_test_sharpe(ch["daily_returns"]) == pytest.approx(m / sd * math.sqrt(365),
                                                                      rel=1e-12)


def test_sharpe_not_evaluable_below_30_returns_or_zero_stdev():
    with pytest.raises(NE, match="fewer than SHARPE_MIN_DAILY_RETURNS=30"):
        pw.whole_test_sharpe(_rets([0.02, 0.0] * 14 + [0.01]))  # 29
    with pytest.raises(NE, match="zero standard deviation"):
        pw.whole_test_sharpe(_rets([0.001] * 40))


def test_sharpe_degenerate_inputs_raise():
    with pytest.raises(ValueError, match="not a finite return"):
        pw.whole_test_sharpe(_rets([0.01] * 29 + [float("nan")]))
    dup = _rets([0.01, 0.02] * 20)
    dup[5] = (dup[4][0], 0.01)
    with pytest.raises(ValueError, match="duplicate day"):
        pw.whole_test_sharpe(dup)
    with pytest.raises(ValueError, match="strictly increasing"):
        pw.whole_test_sharpe(list(reversed(_rets([0.01, 0.02] * 20))))


# ---------------------------------------------------------------------------
# G5: trade counts
# ---------------------------------------------------------------------------

def _rec(sym, win, reason="signal_flip"):
    return {"symbol": sym, "window": win, "exit_reason": reason}


def _res(sym, win, n):
    return {"symbol": sym, "window": win, "run_id": f"{sym}-{win}", "core": {"trade_count": n}}


def test_always_long_strategy_counts_zero_trades_excluding_window_closes():
    """One forced close per window, 96 windows: raw 96, excluding 0."""
    recs = [_rec("BTC", f"w{k}", "end_of_window") for k in range(96)]
    res = [_res("BTC", f"w{k}", 1) for k in range(96)]
    assert pw.whole_test_trade_counts(recs, res) == {
        "BTC": {"raw": 96, "end_of_window": 96, "excluding_end_of_window": 0}}


def test_trade_counts_with_and_without_window_closes_two_coins():
    """BTC: w0 3 signal + 1 forced, w1 2 signal. ETH: w0 1 forced, w1 none."""
    recs = ([_rec("BTC", "w0")] * 3 + [_rec("BTC", "w0", "end_of_window")]
            + [_rec("BTC", "w1")] * 2 + [_rec("ETH", "w0", "end_of_window")])
    res = [_res("BTC", "w0", 4), _res("BTC", "w1", 2), _res("ETH", "w0", 1), _res("ETH", "w1", 0)]
    out = pw.whole_test_trade_counts(recs, res)
    assert out == {"BTC": {"raw": 6, "end_of_window": 1, "excluding_end_of_window": 5},
                   "ETH": {"raw": 1, "end_of_window": 1, "excluding_end_of_window": 0}}
    assert pw.whole_test_trade_counts(recs) == out  # no cross-check, same coins here


def test_trade_counts_no_trades_anywhere_is_zero():
    res = [_res("BTC", "w0", 0), _res("BTC", "w1", 0)]
    assert pw.whole_test_trade_counts([], res) == {
        "BTC": {"raw": 0, "end_of_window": 0, "excluding_end_of_window": 0}}
    assert pw.whole_test_trade_counts(None, res)["BTC"]["raw"] == 0


def test_trade_counts_record_core_mismatch_is_not_evaluable():
    with pytest.raises(NE, match="do not match core.trade_count"):
        pw.whole_test_trade_counts([_rec("BTC", "w0")], [_res("BTC", "w0", 2)])
    with pytest.raises(NE, match="do not match core.trade_count"):  # file missing, trades > 0
        pw.whole_test_trade_counts([], [_res("BTC", "w0", 3)])


def test_trade_counts_malformed_inputs_raise():
    with pytest.raises(ValueError, match="exit_reason 'take_profit'"):
        pw.whole_test_trade_counts([_rec("BTC", "w0", "take_profit")])
    with pytest.raises(ValueError, match="exit_reason None"):
        pw.whole_test_trade_counts([{"symbol": "BTC", "window": "w0"}])
    with pytest.raises(ValueError, match="lacks symbol/window"):
        pw.whole_test_trade_counts([{"window": "w0", "exit_reason": "signal_flip"}])
    with pytest.raises(ValueError, match="not in the results"):
        pw.whole_test_trade_counts([_rec("BTC", "w9")], [_res("BTC", "w0", 0)])
    with pytest.raises(ValueError, match="twice"):
        pw.whole_test_trade_counts([], [_res("BTC", "w0", 0), _res("BTC", "w0", 0)])
    with pytest.raises(ValueError, match="core.trade_count"):
        pw.whole_test_trade_counts([], [{"symbol": "BTC", "window": "w0", "core": {}}])


def test_exit_reason_vocabulary_matches_the_trade_diagnostics_schema():
    schema = yaml.safe_load((SR_ROOT / "workflow_artifacts" / "schemas"
                             / "trade_diagnostics.schema.json").read_text(encoding="utf-8"))
    enums = []

    def walk(node):
        if isinstance(node, dict):
            if "exit_reason" in node and isinstance(node["exit_reason"], dict):
                enums.append(node["exit_reason"].get("enum"))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(schema)
    assert enums and all(set(e) == pw.EXIT_REASONS for e in enums)


# ---------------------------------------------------------------------------
# G6: buy-and-hold
# ---------------------------------------------------------------------------

def test_buy_and_hold_rising_prices_flat_strategy_fails_by_hand():
    """One coin, days 0..10, close 100 -> 110 linearly; strategy flat (equity
    constant). Strategy total 0. B&H gross 110/100 - 1 = 0.1; c = (7.5 + 1)/1e4
    = 0.00085 per side; B&H total = 1.1 * (1 - 0.00085)^2 - 1; excess < 0."""
    closes = [100.0 + i for i in range(11)]
    eq = _bars(0, [1000.0] * 11)
    ch = pw.chain_windows({"w0": {"X": eq}}, ["X"])
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, closes)}}, {"X": 7.5}, {"X": 1.0})
    expected_bh = 1.1 * (1.0 - 0.00085) ** 2 - 1.0
    assert bh["strategy_total_return"] == 0.0
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.1, rel=1e-12)
    assert bh["buy_and_hold_total_return"] == pytest.approx(expected_bh, rel=1e-12)
    assert bh["excess_return"] == pytest.approx(-expected_bh, rel=1e-12)
    assert bh["excess_return"] < 0 and bh["n_days"] == 10


def test_buy_and_hold_falling_prices_flat_strategy_passes_by_hand():
    closes = [100.0 - 2 * i for i in range(11)]  # 100 -> 80
    ch = pw.chain_windows({"w0": {"X": _bars(0, [1000.0] * 11)}}, ["X"])
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, closes)}}, {"X": 7.5}, {"X": 1.5})
    expected_bh = 0.8 * (1.0 - 0.0009) ** 2 - 1.0
    assert bh["buy_and_hold_total_return"] == pytest.approx(expected_bh, rel=1e-12)
    assert bh["excess_return"] == pytest.approx(-expected_bh, rel=1e-12) and bh["excess_return"] > 0


def test_buy_and_hold_strategy_tracking_price_net_of_its_own_costs_fails_by_the_cost_gap():
    """Strategy equity = close exactly (fully invested, no cost in its equity):
    it ties B&H gross, so excess = 1.1 - 1.1 * m = 1.1 * (1 - m) > 0. Charge the
    strategy's own round trip (equity x m on the last day) and it ties B&H net:
    excess 0, which the strict `> 0` bar fails."""
    closes = [100.0 + i for i in range(11)]
    m = (1.0 - 0.00085) ** 2
    ch = pw.chain_windows({"w0": {"X": _bars(0, closes)}}, ["X"])
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, closes)}}, {"X": 7.5}, {"X": 1.0})
    assert bh["excess_return"] == pytest.approx(1.1 * (1.0 - m), rel=1e-9)
    net = closes[:-1] + [closes[-1] * m]
    ch2 = pw.chain_windows({"w0": {"X": _bars(0, net)}}, ["X"])
    bh2 = pw.chained_buy_and_hold(ch2, {"w0": {"X": _bars(0, closes)}}, {"X": 7.5}, {"X": 1.0})
    assert bh2["excess_return"] == pytest.approx(0.0, abs=1e-12)


def test_buy_and_hold_two_coins_reset_to_equal_weight_each_window_by_hand():
    """w0 days 0..2: A 100, 105, 110; B 50, 40, 45 -> portfolio 1.0, 0.925, 1.0
    (growth 1.0). w1 days 2..4: A 110, 121, 99; B 45, 45, 54 -> normalised at
    day 2: 1.0, 1.05, 1.05 (growth 1.05). Chained B&H gross = 1.05 (a
    never-rebalanced book would be (99/100 + 54/50)/2 = 1.035). Costs: A
    (7.5 + 1)/1e4, B (7.5 + 1.5)/1e4; multiplier mean of (1 - c)^2."""
    eq = {"w0": {"A": _bars(0, [1.0] * 3), "B": _bars(0, [1.0] * 3)},
          "w1": {"A": _bars(2, [1.0] * 3), "B": _bars(2, [1.0] * 3)}}
    cl = {"w0": {"A": _bars(0, [100.0, 105.0, 110.0]), "B": _bars(0, [50.0, 40.0, 45.0])},
          "w1": {"A": _bars(2, [110.0, 121.0, 99.0]), "B": _bars(2, [45.0, 45.0, 54.0])}}
    # 5 calendar days, 4 returns: coverage (4+1)/5 = 1.0
    ch = pw.chain_windows(eq, ["A", "B"])
    bh = pw.chained_buy_and_hold(ch, cl, {"A": 7.5, "B": 7.5}, {"A": 1.0, "B": 1.5})
    mult = ((1.0 - 0.00085) ** 2 + (1.0 - 0.0009) ** 2) / 2.0
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.05, rel=1e-12)
    assert bh["cost_multiplier"] == pytest.approx(mult, rel=1e-15)
    assert bh["buy_and_hold_total_return"] == pytest.approx(1.05 * mult - 1.0, rel=1e-12)
    assert bh["n_days"] == 4
    assert bh["cost_per_side_bps"] == pytest.approx({"A": 8.5, "B": 9.0})


def test_buy_and_hold_uses_only_the_chains_counted_days():
    """A gap day (no return) and an overlap: B&H is measured on exactly the
    strategy's counted days -- the price move across the gap is not counted."""
    eq = {"w0": {"X": _bars(0, [1.0] * 20)}, "w1": {"X": _bars(21, [1.0] * 20)}}
    cl = {"w0": {"X": _bars(0, [100.0] * 20)},
          "w1": {"X": _bars(21, [200.0] * 19 + [220.0])}}  # jump across the gap not counted
    ch = pw.chain_windows(eq, ["X"])
    bh = pw.chained_buy_and_hold(ch, cl, {"X": 0.0}, {"X": 0.0})
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.1, rel=1e-12)
    assert bh["n_days"] == len(ch["daily_returns"]) == 38


def test_buy_and_hold_mismatched_inputs_raise():
    eq = {"w0": {"X": _bars(0, [1.0] * 5)}}
    ch = pw.chain_windows(eq, ["X"])
    with pytest.raises(ValueError, match="different common days"):
        pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, [1.0] * 6)}}, {"X": 1}, {"X": 1})
    with pytest.raises(ValueError, match="differ from the chained windows"):
        pw.chained_buy_and_hold(ch, {"w9": {"X": _bars(0, [1.0] * 5)}}, {"X": 1}, {"X": 1})
    with pytest.raises(ValueError, match="no fee/slippage"):
        pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, [1.0] * 5)}}, {}, {"X": 1})
    with pytest.raises(ValueError, match="non-negative"):
        pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, [1.0] * 5)}}, {"X": -1}, {"X": 1})
    bad = _bars(0, [1.0] * 5)
    bad[datetime(2020, 1, 3, 23)] = float("nan")
    with pytest.raises(ValueError):
        pw.chained_buy_and_hold(ch, {"w0": {"X": bad}}, {"X": 1}, {"X": 1})


def test_fee_comes_from_cost_model_yaml_not_the_manifest_fee_bps():
    """The engine charged cost_model.yaml's fee_rate_bps (7.5 spot), not the
    manifest's fee_bps (cost_model.json table, 10)."""
    cm = yaml.safe_load((SR_ROOT / "config" / "cost_model.yaml").read_text(encoding="utf-8"))
    assert pw.spot_fee_rate_bps(cm, "BTCUSDT") == float(cm["fee_rate_bps"]["BTCUSDT"]) == 7.5
    assert pw.spot_fee_rate_bps(cm, "NOPEUSDT") == float(cm["fee_rate_bps"]["default"])
    manifest_fee = {"fee_bps": 10, "slippage_bps": {"default": 1.5, "BTCUSDT": 1}}
    assert pw.spot_fee_rate_bps(cm, "BTCUSDT") != manifest_fee["fee_bps"]
    with pytest.raises(ValueError, match="neither"):
        pw.spot_fee_rate_bps({"fee_rate_bps": {"BTCUSDT": 7.5}}, "ETHUSDT")
    with pytest.raises(ValueError, match="no fee_rate_bps"):
        pw.spot_fee_rate_bps({}, "BTCUSDT")


def test_slippage_resolution_mirrors_the_engine():
    """Table: symbol, else default (execution_handler._resolve_slippage_bps);
    a flat override applies to every symbol. Real committed table checked."""
    import json
    table = json.loads((SR_ROOT.parent / "trading-bot" / "config" / "cost_model.json")
                       .read_text(encoding="utf-8"))["binance"]["margin"]["slippage_bps"]
    assert pw.slippage_bps_for_symbol(table, "BTCUSDT") == float(table["BTCUSDT"])
    assert pw.slippage_bps_for_symbol(table, "NOPEUSDT") == float(table["default"])
    assert pw.slippage_bps_for_symbol(2.0, "ANY") == 2.0
    with pytest.raises(ValueError, match="neither"):
        pw.slippage_bps_for_symbol({"BTCUSDT": 1}, "ETHUSDT")
    with pytest.raises(ValueError):
        pw.slippage_bps_for_symbol(float("nan"), "BTCUSDT")


def test_window_close_bars_reader(tmp_path):
    eq = _bars(0, [1000.0, 1001.0, 1002.0])
    cl = _bars(0, [10.0, 11.0, 12.0])
    _write_states(tmp_path, "r1", eq, cl)
    p = tmp_path / "results" / "r1" / "portfolio_states.csv"
    got = pw.window_close_bars(p)
    assert got == cl  # warm-up row (close -1) dropped by the NOT_READY filter
    assert list(got) == list(pdv1.window_equity_bars(p))  # same bars as the equity reader
    # missing close column
    q = tmp_path / "noclose.csv"
    q.write_text("timestamp,regime,postRebalance_total_value\n2020-01-01 23:00:00,trend,1\n",
                 encoding="utf-8")
    with pytest.raises(ValueError, match="lacks column"):
        pw.window_close_bars(q)
    # non-positive close after warm-up
    z = tmp_path / "zero.csv"
    z.write_text("timestamp,regime,close\n2020-01-01 23:00:00,trend,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="close 0.0"):
        pw.window_close_bars(z)
    # a timestamp repeated with a different close
    dup = tmp_path / "dup.csv"
    dup.write_text("timestamp,regime,close\n2020-01-01 23:00:00,trend,5\n"
                   "2020-01-01 23:00:00,trend,6\n", encoding="utf-8")
    with pytest.raises(ValueError, match="two different closes"):
        pw.window_close_bars(dup)
    same = tmp_path / "same.csv"
    same.write_text("timestamp,regime,close\n2020-01-01 23:00:00,trend,5\n"
                    "2020-01-01 23:00:00,trend,5\n", encoding="utf-8")
    assert pw.window_close_bars(same) == {datetime(2020, 1, 1, 23): 5.0}


# ---------------------------------------------------------------------------
# G7: pooled edge / cost ratio
# ---------------------------------------------------------------------------

def _summary(ratio, n, fees=True):
    return {"realized_edge_to_cost_ratio": ratio, "per_trade_expectancy_bps": {"n": n},
            "cost_components_measured": {"fees": fees, "funding": False}}


def test_edge_cost_ratio_reads_the_existing_value_with_the_floor():
    assert pw.pooled_edge_to_cost_ratio(_summary(2.3, 100), min_trades=100) == {
        "ratio": 2.3, "n_trades": 100}
    assert pw.pooled_edge_to_cost_ratio(_summary(-0.5, 250), min_trades=100)["ratio"] == -0.5


@pytest.mark.parametrize("summary,frag", [
    (None, "no trade_diagnostics_summary"),
    ({}, "no trade_diagnostics_summary"),
    (_summary(2.3, 99), "fewer than min_trades=100"),
    (_summary(None, 150), "is None"),
    (_summary(2.3, 150, fees=False), "fees is False"),
    ({"realized_edge_to_cost_ratio": 2.3, "per_trade_expectancy_bps": {"n": 150}},
     "fees is None"),
])
def test_edge_cost_ratio_not_evaluable(summary, frag):
    with pytest.raises(NE, match=frag):
        pw.pooled_edge_to_cost_ratio(summary, min_trades=100)


def test_edge_cost_ratio_bad_inputs_raise():
    with pytest.raises(ValueError, match="min_trades"):
        pw.pooled_edge_to_cost_ratio(_summary(2.3, 100), min_trades=0)
    with pytest.raises(ValueError, match="realized_edge_to_cost_ratio is nan"):
        pw.pooled_edge_to_cost_ratio(_summary(float("nan"), 100), min_trades=100)
    with pytest.raises(ValueError, match="per_trade_expectancy_bps.n"):
        pw.pooled_edge_to_cost_ratio(_summary(2.3, None), min_trades=100)


def test_edge_cost_ratio_is_the_run_protocol_figure_not_a_second_formula():
    """Pooled over two coins: the value returned is exactly the one
    run_protocol._aggregate_trade_diagnostics put in the summary."""
    import run_protocol as rp
    recs = []
    for k in range(120):
        sym = "BTCUSDT" if k % 2 else "ETHUSDT"
        recs.append({"symbol": sym, "window": f"w{k % 4}", "exit_reason": "signal_flip",
                     "realized_return": 0.2 + 0.01 * (k % 7), "cost_paid": 15.0,
                     "net_portfolio_return_pct": 0.05, "holding_bars": 3, "mae": 0.1,
                     "mfe": 0.3, "profitable_net": True, "entry_efficiency": None,
                     "exit_efficiency": None})
    results = [{"core": {"trade_count": 30}} for _ in range(4)]
    summary = rp._aggregate_trade_diagnostics(recs, results)
    got = pw.pooled_edge_to_cost_ratio(summary, min_trades=100)
    assert got["ratio"] == summary["realized_edge_to_cost_ratio"] and got["n_trades"] == 120


# ---------------------------------------------------------------------------
# Regression: the v1 per-window functions are untouched
# ---------------------------------------------------------------------------

# sha256 of tools/portfolio_daily.py at origin/master 21920594 (the base of this
# branch). S2a adds a sibling module and does not edit the v1 file; a change to
# it belongs to a later slice that must re-pin this value deliberately.
_V1_SHA256 = "3091ef77aa796ca5ff379d1179fee20af2babdc5b17f940b4e862e91f7ae015d"


def test_v1_module_file_is_unchanged():
    got = hashlib.sha256((SR_ROOT / "tools" / "portfolio_daily.py").read_bytes()
                         .replace(b"\r\n", b"\n")).hexdigest()
    assert got == _V1_SHA256


def test_v1_outputs_pinned_on_a_fixture(tmp_path):
    """v1 outputs on a fixed fixture, pinned as literals computed at the base
    commit: portfolio_daily_returns and _portfolio_profit_metrics are
    byte-identical after importing the v2 module."""
    a = [100.0, 120.0, 90.0, 96.0]
    b = [100.0, 100.0, 110.0, 99.0]
    results = []
    for win, first in (("w0", 0), ("w1", 3)):
        for coin, closes in (("A", a), ("B", b)):
            rid = f"{coin}-{win}"
            _write_states(tmp_path, rid, _bars(first, closes, intraday={2: [closes[2] * 0.9]}))
            results.append({"symbol": coin, "window": win, "run_id": rid})
    pr = {"results": results}
    rets = pdv1.portfolio_daily_returns(tmp_path, pr)
    assert [(d.isoformat(), repr(r)) for d, r in rets] == _V1_PINNED_RETURNS
    m = _rpr()._portfolio_profit_metrics(tmp_path, pr)
    assert (m["avg_daily_return"][0], m["max_drawdown_pct"][0]) == _V1_PINNED_METRICS
    assert pdv1.PORTFOLIO_MIN_COMMON_DAY_COVERAGE == 0.9
    assert pw.WHOLE_TEST_MIN_COVERAGE is pdv1.PORTFOLIO_MIN_COMMON_DAY_COVERAGE


# Computed with the base commit's portfolio_daily.py / run_phase1_research.py
# (origin/master 21920594) on the fixture above. Hand check: A normalised 1,
# 1.2, 0.9, 0.96; B 1, 1.0, 1.1, 0.99 -> portfolio 1, 1.1, 1.0, 0.975 in each
# window (returns 0.1, -1/11, -0.025, twice); the 01:00 dip (A 81, B 99) is
# 0.9 against the 1.1 peak -> drawdown 100 * (1 - 0.9/1.1) = 18.181818%.
_V1_PINNED_RETURNS = [
    ("2020-01-02", "0.10000000000000009"), ("2020-01-03", "-0.09090909090909094"),
    ("2020-01-04", "-0.025000000000000022"), ("2020-01-05", "0.10000000000000009"),
    ("2020-01-06", "-0.09090909090909094"), ("2020-01-07", "-0.025000000000000022"),
]
_V1_PINNED_METRICS = (-0.00530303, 18.181818)
