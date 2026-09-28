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


def _bnd(**spans) -> dict:
    """{label: (nominal start, nominal end)} from day indices."""
    return {w: (_day(a), _day(b)) for w, (a, b) in spans.items()}


def _auto_bounds(wins) -> dict:
    """Bounds equal to each window's recorded day range (complete data only)."""
    out = {}
    for w, by_coin in wins.items():
        days = [t.date() for bars in (by_coin.values() if isinstance(by_coin, dict) else [])
                if isinstance(bars, dict) for t in bars if isinstance(t, datetime)]
        out[w] = (min(days), max(days)) if days else (D0, D0)
    return out


def _chain(wins, coins, bounds=None, **kw):
    return pw.chain_windows(wins, coins, _auto_bounds(wins) if bounds is None else bounds, **kw)


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
    ch = _chain(wins, ["A", "B"])
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
    ch = _chain(windows, coins)
    assert ch["daily_returns"] == pdv1.portfolio_daily_returns(tmp_path, pr)


def test_chained_levels_multiply_across_junctions():
    """One coin. w0 days 0..2: 100, 110, 121 (level 1.0, 1.1, 1.21). w1 days
    2..4: 1000, 900, 990 (joins at day 2, scale 1.21/1.0; levels day 3 =
    1.21 * 0.9 = 1.089, day 4 = 1.21 * 0.99 = 1.1979)."""
    ch = _chain({"w0": {"X": _bars(0, [100.0, 110.0, 121.0])},
                           "w1": {"X": _bars(2, [1000.0, 900.0, 990.0])}}, ["X"])
    lv = dict(ch["daily_levels"])
    assert lv[_day(0)] == 1.0
    assert lv[_day(3)] == pytest.approx(1.21 * 0.9, rel=1e-12)
    assert lv[_day(4)] == pytest.approx(1.21 * 0.99, rel=1e-12)
    assert [r for _d, r in ch["daily_returns"]] == pytest.approx([0.1, 0.1, -0.1, 0.1])


def test_out_of_order_windows_give_the_same_chain_as_sorted():
    wins = _contiguous_layout()
    rev = {k: wins[k] for k in reversed(list(wins))}
    a, b = _chain(wins, ["A", "B"]), _chain(rev, ["A", "B"])
    assert a["daily_returns"] == b["daily_returns"]
    assert a["bar_levels"] == b["bar_levels"]
    assert [s["window"] for s in b["segments"]] == ["w0", "w1", "w2"]


def test_gap_is_linked_flat_and_not_counted():
    """Protocol bounds w0 = days 0..19, w1 = days 21..40: a real gap (day 20).
    The chain is flat from day 19 to day 21 (level unchanged), no return on day
    21, one gap day. Returns 19 + 19 = 38; nominal span 0..40 = 41 days;
    coverage 39/41."""
    w0 = [100.0 + i for i in range(20)]
    w1 = [500.0 * (1.0 + 0.001 * i) for i in range(20)]
    ch = _chain({"w0": {"X": _bars(0, w0)}, "w1": {"X": _bars(21, w1)}}, ["X"],
                _bnd(w0=(0, 19), w1=(21, 40)))
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
    """Bounds w0 = 0..9, w1 = 15..24: returns 9 + 9 = 18, nominal span 25 days,
    (18 + 1) / 25 = 0.76 < 0.9 -> NOT_EVALUABLE (each window alone is fine)."""
    with pytest.raises(NE, match="WHOLE_TEST_MIN_COVERAGE"):
        _chain({"w0": {"X": _bars(0, [100.0] * 9 + [101.0])},
                "w1": {"X": _bars(15, [100.0] * 9 + [99.0])}}, ["X"],
               _bnd(w0=(0, 9), w1=(15, 24)))


def test_overlap_longer_than_one_day_keeps_the_earliest_windows_days():
    """w0 days 0..10, w1 days 7..20 (4 shared days: 7, 8, 9, 10). w0 keeps days
    up to 10; w1 joins at day 10 and contributes days 11..20. The return on day
    11 is w1's v(11)/v(10) - 1; days 8..10 come from w0."""
    w0 = [100.0 * 1.01 ** i for i in range(11)]
    w1 = [70.0 + 3.0 * ((i * 5) % 7) for i in range(14)]  # day 7+i
    ch = _chain({"w0": {"X": _bars(0, w0)}, "w1": {"X": _bars(7, w1)}}, ["X"],
                _bnd(w0=(0, 10), w1=(7, 20)))
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


def test_missing_junction_day_for_one_coin_is_not_evaluable_and_names_the_cell():
    """Code review finding 4 (deviation from G1's "treat as gap"): w0 = days
    0..10, w1 nominal 10..20 (one-day overlap). Coin A has w1's junction day
    10, coin B's w1 data starts on day 11: the coins disagree on w1's first
    day -> missing data -> NOT_EVALUABLE naming the one missing cell."""
    w0 = {c: _bars(0, [100.0 + i for i in range(11)]) for c in ("A", "B")}
    w1 = {"A": _bars(10, [200.0 + i for i in range(11)]),
          "B": _bars(11, [200.0 + i for i in range(10)])}
    with pytest.raises(NE, match="coins start on different days") as ei:
        _chain({"w0": w0, "w1": w1}, ["A", "B"], _bnd(w0=(0, 10), w1=(10, 20)))
    assert "1 missing (window, coin, day) cell(s): ('w1', 'B', 2020-01-11)" in str(ei.value)


def test_junction_hole_inside_a_window_lists_every_coin_and_count():
    """w1 (nominal 7..20) has data from day 7 for both coins but neither has
    the junction day 10 (last chained day): NOT_EVALUABLE, both cells, count 2."""
    w0 = {c: _bars(0, [100.0] * 11) for c in ("A", "B")}
    w1 = {c: _skip_days(_bars(7, [100.0] * 14), {_day(10)}) for c in ("A", "B")}
    with pytest.raises(NE, match="junction day 2020-01-11") as ei:
        _chain({"w0": w0, "w1": w1}, ["A", "B"], _bnd(w0=(0, 10), w1=(7, 20)))
    msg = str(ei.value)
    assert "2 missing (window, coin, day) cell(s)" in msg
    assert "('w1', 'A', 2020-01-11)" in msg and "('w1', 'B', 2020-01-11)" in msg


def test_measured_engine_layout_all_coins_stop_three_days_short_is_evaluable():
    """The layout measured on real runs: every coin of a window stops 3 days
    before test.end (w0 nominal 0..30, recorded 0..27; w1 nominal 30..60,
    recorded 30..57). The engine tail days 28, 29 are flat and excluded from
    coverage (day 30 is w1's first day, still counted); w1's own tail 58..60
    too. Returns: w0 27 + w1 27 = 54 (w1 joins flat at day 30, no return on
    it). Counted days: nominal 61 - 5 engine days = 56; coverage 55/56."""
    w0 = {c: _bars(0, [100.0 + i * (1 + k) for i in range(28)]) for k, c in enumerate("AB")}
    w1 = {c: _bars(30, [50.0 + i for i in range(28)]) for c in "AB"}
    ch = _chain({"w0": w0, "w1": w1}, ["A", "B"], _bnd(w0=(0, 30), w1=(30, 60)))
    assert [s["kind"] for s in ch["segments"]] == ["first", "gap"]
    assert [s["engine_tail_days"] for s in ch["segments"]] == [3, 3]
    assert ch["n_engine_tail_days"] == 6 and ch["n_engine_head_days"] == 0
    assert ch["engine_gap_days_excluded"] == [_day(28), _day(29), _day(58), _day(59), _day(60)]
    assert ch["n_gap_days"] == 0 and ch["n_gap_links"] == 1
    lv = dict(ch["daily_levels"])
    assert lv[_day(30)] == pytest.approx(lv[_day(27)], rel=1e-15)  # flat across the tail
    assert _day(30) not in dict(ch["daily_returns"])
    assert len(ch["daily_returns"]) == 54
    assert ch["n_calendar_days"] == 61 and ch["n_counted_calendar_days"] == 56
    assert ch["coverage"] == 55 / 56
    assert ch["first_day"] == _day(0) and ch["last_day"] == _day(57)


def test_measured_layout_buy_and_hold_is_flat_across_the_engine_tail():
    """Prices jump 100 -> 200 across the engine tail days: buy-and-hold is flat
    there like the strategy (nobody traded), so its gross is w0 (110/100) x
    w1 (220/200) - 1 = 0.21."""
    eq = {"w0": {"X": _bars(0, [1.0] * 28)}, "w1": {"X": _bars(30, [1.0] * 28)}}
    cl = {"w0": {"X": _bars(0, [100.0] * 27 + [110.0])},
          "w1": {"X": _bars(30, [200.0] * 27 + [220.0])}}
    ch = _chain(eq, ["X"], _bnd(w0=(0, 30), w1=(30, 60)))
    bh = pw.chained_buy_and_hold(ch, cl, {"X": 0.0}, {"X": 0.0})
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.21, rel=1e-12)


def test_engine_head_shortfall_all_coins_agree_is_a_flat_gap():
    """A gap window whose coins all start one day after test.start (within
    warmup_days): a protocol gap, flat, the head day excluded from coverage."""
    wins = {"w0": {"X": _bars(0, [100.0] * 20)}, "w1": {"X": _bars(22, [100.0] * 19)}}
    ch = _chain(wins, ["X"], _bnd(w0=(0, 19), w1=(21, 40)))
    seg = ch["segments"][1]
    assert seg["kind"] == "gap" and seg["join_day"] == _day(22) and seg["engine_head_days"] == 1
    assert ch["n_gap_days"] == 1 and ch["engine_gap_days_excluded"] == [_day(21)]


def test_missing_tail_of_one_coin_is_not_evaluable_probe():
    """Second-round finding 1 probe: coin B falls 100 -> 60 over w0's last 3
    days, but those 3 days are missing from B's data while coin A continues
    (per-window coverage 28/31 still passes v1's floor). w1 then restarts both
    coins at 1.0, so the loss would vanish. The coins disagree on w0's last
    day -> NOT_EVALUABLE naming the 3 cells. Bounds are required, so there is
    no path without them."""
    a0 = _bars(0, [100.0] * 31)
    b0 = _skip_days(_bars(0, [100.0] * 28 + [80.0, 70.0, 60.0]), {_day(28), _day(29), _day(30)})
    w1 = {c: _bars(30, [100.0] * 31) for c in ("A", "B")}
    wins = {"w0": {"A": a0, "B": b0}, "w1": w1}
    pdv1.window_common_curve("w0", wins["w0"], ["A", "B"])  # v1 floor passes
    with pytest.raises(NE, match="coins stop on different days") as ei:
        pw.chain_windows(wins, ["A", "B"], _bnd(w0=(0, 30), w1=(30, 60)))
    msg = str(ei.value)
    assert "3 missing (window, coin, day) cell(s)" in msg
    assert "('w0', 'B', 2020-01-29)" in msg and "('w0', 'B', 2020-01-31)" in msg
    with pytest.raises(TypeError):
        pw.chain_windows(wins, ["A", "B"])  # window_bounds is required


def test_tail_shortfall_beyond_the_engine_limit_is_not_evaluable():
    """Every coin stops 6 days before test.end (> MAX_ENGINE_TAIL_DAYS = 5):
    not the engine's systematic shortfall -> NOT_EVALUABLE with 6 cells; 5
    days is still accepted; a larger declared limit accepts 6."""
    assert pw.MAX_ENGINE_TAIL_DAYS == 5
    six = {"w0": {"X": _bars(0, [100.0] * 25)}}
    with pytest.raises(NE, match="6 days before its nominal end") as ei:
        pw.chain_windows(six, ["X"], _bnd(w0=(0, 30)))
    assert "6 missing (window, coin, day) cell(s)" in str(ei.value)
    five = {"w0": {"X": _bars(0, [100.0] * 26)}}
    assert pw.chain_windows(five, ["X"], _bnd(w0=(0, 30)))["n_engine_tail_days"] == 5
    assert pw.chain_windows(six, ["X"], _bnd(w0=(0, 30)),
                            max_engine_tail_days=6)["n_engine_tail_days"] == 6


def test_first_window_head_and_bounds_misuse():
    wins = {"w0": {"X": _bars(1, [100.0] * 20)}}
    # one day of head shortfall, the (only) coin agrees: engine head gap
    ch = pw.chain_windows(wins, ["X"], _bnd(w0=(0, 20)))
    assert ch["n_engine_head_days"] == 1 and ch["engine_gap_days_excluded"] == [_day(0)]
    assert ch["n_counted_calendar_days"] == 20
    # coins disagree on the first day: missing head data
    two = {"w0": {"A": _bars(0, [100.0] * 21), "B": _bars(1, [100.0] * 20)}}
    with pytest.raises(NE, match="coins start on different days") as ei:
        pw.chain_windows(two, ["A", "B"], _bnd(w0=(0, 20)))
    assert "('w0', 'B', 2020-01-01)" in str(ei.value)
    # data before the given start / after the given end: wrong bounds
    for b in (_bnd(w0=(2, 20)), _bnd(w0=(1, 19))):
        with pytest.raises(ValueError, match="nominal (start|end)") as ei:
            _chain(wins, ["X"], b)
        assert not isinstance(ei.value, NE)
    # a start far before the first recorded day: a manifest (prefetch) start
    far = {"w0": {"X": _bars(10, [100.0] * 11)}}
    with pytest.raises(ValueError, match="manifest's start .*warm-up prefetch") as ei:
        pw.chain_windows(far, ["X"], _bnd(w0=(0, 20)))
    assert not isinstance(ei.value, NE)
    ch = pw.chain_windows(far, ["X"], _bnd(w0=(0, 20)), warmup_days=10)  # declared warm-up
    assert ch["n_engine_head_days"] == 10
    with pytest.raises(ValueError, match="exactly the windows' labels"):
        _chain(wins, ["X"], _bnd(w9=(1, 20)))
    with pytest.raises(ValueError, match="is not a date"):
        _chain(wins, ["X"], {"w0": (datetime(2020, 1, 2), _day(20))})
    with pytest.raises(ValueError, match="is before start"):
        _chain(wins, ["X"], {"w0": (_day(20), _day(1))})
    for kw in ({"warmup_days": -1}, {"max_engine_tail_days": True}):
        with pytest.raises(ValueError, match="non-negative int"):
            pw.chain_windows(wins, ["X"], _bnd(w0=(1, 20)), **kw)


def test_window_inside_an_earlier_window_raises():
    """w1 (nominal 5..7) lies inside w0 (0..20): a protocol layout error."""
    with pytest.raises(ValueError, match="lies inside earlier windows") as ei:
        _chain({"w0": {"X": _bars(0, [100.0 + i for i in range(21)])},
                "w1": {"X": _bars(5, [1.0, 2.0, 3.0])}}, ["X"])
    assert not isinstance(ei.value, NE)


def test_join_bar_includes_the_anchor_level_when_a_coin_lacks_the_close_bar():
    """Code review finding 5 probe: B has no 23:00 bar on the anchor day (its
    close is at 22:00), so no COMMON bar sits at the anchor close. Both coins
    then fall 10% the next day. The anchor level 1.0 must be in the bar curve:
    drawdown 10% (v1 starts at the first common bar, 0.9, and reports 0%)."""
    a = _bars(0, [100.0, 90.0, 90.0])
    b = _bars(0, [100.0, 90.0, 90.0])
    del b[datetime(2020, 1, 1, 23)]
    b[datetime(2020, 1, 1, 22)] = 100.0
    b = dict(sorted(b.items()))
    ch = _chain({"w0": {"A": a, "B": b}}, ["A", "B"])
    assert ch["bar_levels"][0] == (datetime(2020, 1, 1, 23), 1.0)
    dd = pw.whole_test_max_drawdown(ch)
    assert dd["max_drawdown_pct"] == pytest.approx(10.0, rel=1e-12)
    assert dd["peak_ts"] == datetime(2020, 1, 1, 23)


def test_duplicate_nominal_start_raises():
    with pytest.raises(ValueError, match="same nominal start"):
        _chain({"w0": {"X": _bars(0, [1.0, 2.0])},
                "w1": {"X": _bars(0, [1.0, 2.0, 3.0])}}, ["X"])


def test_window_bounds_from_the_protocol_json():
    """The real committed baseline_v1 protocol: 11 monthly windows, label ->
    (test.start, test.end), each end equal to the next start (one-day overlap,
    end inclusive by day)."""
    b = pw.load_protocol_window_bounds(SR_ROOT / "protocols" / "baseline_v1.json")
    assert len(b) == 11
    assert b["2024-01"] == (date(2024, 1, 1), date(2024, 2, 1))
    spans = sorted(b.values())
    assert all(spans[i][1] == spans[i + 1][0] for i in range(len(spans) - 1))


@pytest.mark.parametrize("protocol,frag", [
    ({}, "no `windows` list"),
    ({"windows": []}, "no `windows` list"),
    ({"windows": [{"label": "a"}]}, "lacks label/test"),
    ({"windows": [{"label": "a", "test": {"start": "2020-1-1", "end": "2020-02-01"}}]},
     "not a YYYY-MM-DD date"),
    ({"windows": [{"label": "a", "test": {"start": "2020-02-01", "end": "2020-01-01"}}]},
     "is before test.start"),
    ({"windows": [{"label": "a", "test": {"start": "2020-01-01", "end": "2020-02-01"}},
                  {"label": "a", "test": {"start": "2020-02-01", "end": "2020-03-01"}}]},
     "missing or repeated"),
    ({"windows": [{"label": ["a"], "test": {"start": "2020-01-01", "end": "2020-02-01"}}]},
     "not hashable"),
])
def test_window_bounds_from_protocol_rejects_malformed(protocol, frag):
    with pytest.raises(ValueError, match=frag):
        pw.window_bounds_from_protocol(protocol)


def test_two_coins_common_day_drop():
    """B lacks day 5 of 0..20: day 5 dropped for both (per-window coverage
    20/21 >= 0.9); the day-4 -> day-6 step is a multi-day step, not a return.
    Returns 20 - 2 = 18; whole-test coverage (18 + 1) / 21 = 0.905 >= 0.9."""
    a = _bars(0, [100.0 + i for i in range(21)])
    b = _skip_days(_bars(0, [50.0 + 2 * i for i in range(21)]), {_day(5)})
    ch = _chain({"w0": {"A": a, "B": b}}, ["A", "B"])
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
        _chain({"w0": {"A": a, "B": b}}, ["A", "B"])


def test_per_window_coverage_below_floor_is_not_evaluable():
    """B lacks 2 of 10 days: 8 / 10 = 0.8 < 0.9 -- v1's per-window floor."""
    a = _bars(0, [100.0] * 10)
    b = _skip_days(_bars(0, [100.0] * 10), {_day(4), _day(5)})
    with pytest.raises(NE, match="PORTFOLIO_MIN_COMMON_DAY_COVERAGE"):
        _chain({"w0": {"A": a, "B": b}}, ["A", "B"])


def test_coin_set_differs_is_not_evaluable():
    with pytest.raises(NE, match="has coins"):
        _chain({"w0": {"A": _bars(0, [1.0, 2.0])}}, ["A", "B"])
    with pytest.raises(NE, match="no windows"):
        _chain({}, ["A"])


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), 0.0, -1.0, True, "1.0"])
def test_degenerate_values_raise(bad):
    bars = _bars(0, [100.0, 101.0, 102.0])
    bars[datetime(2020, 1, 2, 23)] = bad
    with pytest.raises(ValueError) as ei:
        _chain({"w0": {"X": bars}}, ["X"])
    assert not isinstance(ei.value, NE)


def test_unsorted_timestamps_raise():
    bars = _bars(0, [100.0, 101.0, 102.0])
    unsorted = dict(reversed(list(bars.items())))
    with pytest.raises(ValueError, match="strictly increasing") as ei:
        _chain({"w0": {"X": unsorted}}, ["X"])
    assert not isinstance(ei.value, NE)


def test_non_datetime_or_aware_timestamp_raises():
    from datetime import timezone
    with pytest.raises(ValueError, match="not a datetime"):
        _chain({"w0": {"X": {"2020-01-01 23:00": 1.0}}}, ["X"])
    with pytest.raises(ValueError, match="naive"):
        _chain({"w0": {"X": {datetime(2020, 1, 1, 23, tzinfo=timezone.utc): 1.0}}},
                         ["X"])


def test_duplicate_coins_raise():
    with pytest.raises(ValueError, match="without duplicates"):
        _chain({"w0": {"X": _bars(0, [1.0, 2.0])}}, ["X", "X"])


# ---------------------------------------------------------------------------
# D-034: drawdown
# ---------------------------------------------------------------------------

def test_drawdown_spanning_two_windows_is_found_where_v1_misses_it(tmp_path):
    """One coin. w0 days 0..3: 100, 120, 115, 110 (peak 1.2, ends 1.1: w0's own
    drawdown 1 - 1.1/1.2 = 8.33%). w1 days 3..5: 1000, 950, 900 (its own
    drawdown 10%). Chained: 1.1 * 0.9 = 0.99 at day 5 against the 1.2 peak ->
    100 * (1 - 0.99/1.2) = 17.5%. v1 reports the worst window: 10%."""
    w0, w1 = _bars(0, [100.0, 120.0, 115.0, 110.0]), _bars(3, [1000.0, 950.0, 900.0])
    ch = _chain({"w0": {"X": w0}, "w1": {"X": w1}}, ["X"])
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
    ch = _chain({"w1": {"A": a, "B": b}}, ["A", "B"])
    dd = pw.whole_test_max_drawdown(ch)["max_drawdown_pct"]
    assert dd == pytest.approx(100.0 * (1.0 - 0.95 / 1.1), rel=1e-12)
    for rid, bars in (("A-w1", a), ("B-w1", b)):
        _write_states(tmp_path, rid, bars)
    pr = {"results": [{"symbol": "A", "window": "w1", "run_id": "A-w1"},
                      {"symbol": "B", "window": "w1", "run_id": "B-w1"}]}
    v1 = _rpr()._portfolio_profit_metrics(tmp_path, pr)["max_drawdown_pct"][0]
    assert round(dd, 6) == v1


def test_running_peak_drawdown_matches_the_engines_bar_equity_formula():
    """Code review finding 8: the running-peak formula equals
    trading-bot/performance/bar_equity.max_drawdown_pct (sign flipped) on a
    shared fixture -- a chained multi-window, two-coin curve with intraday dips."""
    pd = pytest.importorskip("pandas")
    sys.path.insert(0, str(SR_ROOT.parent / "trading-bot"))
    from performance.bar_equity import max_drawdown_pct as engine_dd
    wins = _contiguous_layout()
    for k, win in enumerate(wins.values()):
        for coin in ("A", "B"):
            d = _day(10 * k + 4)
            win[coin][datetime(d.year, d.month, d.day, 5)] = 60.0 - 5 * k
            win[coin] = dict(sorted(win[coin].items()))
    ch = _chain(wins, ["A", "B"])
    ours = pw.whole_test_max_drawdown(ch)["max_drawdown_pct"]
    theirs = engine_dd(pd.Series([v for _t, v in ch["bar_levels"]]))
    assert ours > 0
    assert ours == pytest.approx(-theirs, rel=1e-12)


def test_drawdown_of_monotone_curve_is_zero_and_bad_chain_raises():
    ch = _chain({"w0": {"X": _bars(0, [1.0, 2.0, 3.0])}}, ["X"])
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
    ch = _chain(wins, ["A", "B"])
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


def test_trade_counts_two_coins_zero_trade_coin_is_listed():
    """BTC: w0 3 signal + 1 forced, w1 2 signal. ETH: no trade at all (and no
    record) -- it must still appear, with 0 (code review finding 2)."""
    recs = ([_rec("BTC", "w0")] * 3 + [_rec("BTC", "w0", "end_of_window")]
            + [_rec("BTC", "w1")] * 2)
    res = [_res("BTC", "w0", 4), _res("BTC", "w1", 2), _res("ETH", "w0", 0), _res("ETH", "w1", 0)]
    assert pw.whole_test_trade_counts(recs, res) == {
        "BTC": {"raw": 6, "end_of_window": 1, "excluding_end_of_window": 5},
        "ETH": {"raw": 0, "end_of_window": 0, "excluding_end_of_window": 0}}


def test_trade_counts_results_are_required():
    with pytest.raises(TypeError):
        pw.whole_test_trade_counts([_rec("BTC", "w0")])  # noqa -- no results argument
    with pytest.raises(ValueError, match="results must be a list"):
        pw.whole_test_trade_counts([_rec("BTC", "w0")], None)
    with pytest.raises(ValueError, match="results is empty"):
        pw.whole_test_trade_counts([], [])
    with pytest.raises(ValueError, match="trade_records must be a list"):
        pw.whole_test_trade_counts(None, [_res("BTC", "w0", 0)])


def test_signal_trade_crossing_a_junction_is_counted_once():
    """A position opened in w0 and still held at its end is force-closed there
    (end_of_window, excluded) and re-opened in w1, where a signal flip closes
    it (counted): one trade, not two."""
    recs = [_rec("BTC", "w0", "end_of_window"), _rec("BTC", "w1", "signal_flip")]
    res = [_res("BTC", "w0", 1), _res("BTC", "w1", 1)]
    assert pw.whole_test_trade_counts(recs, res)["BTC"] == {
        "raw": 2, "end_of_window": 1, "excluding_end_of_window": 1}


def test_trade_counts_no_trades_anywhere_is_zero():
    res = [_res("BTC", "w0", 0), _res("BTC", "w1", 0)]
    assert pw.whole_test_trade_counts([], res) == {
        "BTC": {"raw": 0, "end_of_window": 0, "excluding_end_of_window": 0}}


def test_trade_counts_record_core_mismatch_is_not_evaluable():
    with pytest.raises(NE, match="do not match core.trade_count"):
        pw.whole_test_trade_counts([_rec("BTC", "w0")], [_res("BTC", "w0", 2)])
    with pytest.raises(NE, match="do not match core.trade_count"):  # file missing, trades > 0
        pw.whole_test_trade_counts([], [_res("BTC", "w0", 3)])


def test_trade_counts_malformed_inputs_raise():
    res = [_res("BTC", "w0", 1)]
    with pytest.raises(ValueError, match="exit_reason 'take_profit'"):
        pw.whole_test_trade_counts([_rec("BTC", "w0", "take_profit")], res)
    with pytest.raises(ValueError, match="exit_reason None"):
        pw.whole_test_trade_counts([{"symbol": "BTC", "window": "w0"}], res)
    with pytest.raises(ValueError, match="lacks symbol/window"):
        pw.whole_test_trade_counts([{"window": "w0", "exit_reason": "signal_flip"}], res)
    with pytest.raises(ValueError, match="not in the results"):
        pw.whole_test_trade_counts([_rec("BTC", "w9")], res)
    with pytest.raises(ValueError, match="twice"):
        pw.whole_test_trade_counts([], [_res("BTC", "w0", 0), _res("BTC", "w0", 0)])
    with pytest.raises(ValueError, match="core.trade_count"):
        pw.whole_test_trade_counts([], [{"symbol": "BTC", "window": "w0", "core": {}}])
    with pytest.raises(ValueError, match="core.trade_count"):
        pw.whole_test_trade_counts([], [{"symbol": "BTC", "window": "w0",
                                          "core": {"trade_count": True}}])
    # unhashable symbol / exit_reason: ValueError, never TypeError
    with pytest.raises(ValueError, match="not hashable"):
        pw.whole_test_trade_counts([_rec(["BTC"], "w0")], res)
    with pytest.raises(ValueError, match="not hashable"):
        pw.whole_test_trade_counts([_rec("BTC", "w0", ["signal_flip"])], res)
    with pytest.raises(ValueError, match="not hashable"):
        pw.whole_test_trade_counts([], [{"symbol": {"a": 1}, "window": "w0",
                                          "core": {"trade_count": 0}}])


def test_trade_counts_accept_numpy_integers():
    np = pytest.importorskip("numpy")
    res = [{"symbol": "BTC", "window": "w0", "core": {"trade_count": np.int64(1)}}]
    assert pw.whole_test_trade_counts([_rec("BTC", "w0")], res)["BTC"]["raw"] == 1


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
    ch = _chain({"w0": {"X": eq}}, ["X"])
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, closes)}}, {"X": 7.5}, {"X": 1.0})
    expected_bh = 1.1 * (1.0 - 0.00085) ** 2 - 1.0
    assert bh["strategy_total_return"] == 0.0
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.1, rel=1e-12)
    assert bh["buy_and_hold_total_return"] == pytest.approx(expected_bh, rel=1e-12)
    assert bh["excess_return"] == pytest.approx(-expected_bh, rel=1e-12)
    assert bh["excess_return"] < 0 and bh["n_daily_returns"] == 10
    assert bh["n_calendar_days"] == 11


def test_buy_and_hold_falling_prices_flat_strategy_passes_by_hand():
    closes = [100.0 - 2 * i for i in range(11)]  # 100 -> 80
    ch = _chain({"w0": {"X": _bars(0, [1000.0] * 11)}}, ["X"])
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
    ch = _chain({"w0": {"X": _bars(0, closes)}}, ["X"])
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": _bars(0, closes)}}, {"X": 7.5}, {"X": 1.0})
    assert bh["excess_return"] == pytest.approx(1.1 * (1.0 - m), rel=1e-9)
    net = closes[:-1] + [closes[-1] * m]
    ch2 = _chain({"w0": {"X": _bars(0, net)}}, ["X"])
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
    ch = _chain(eq, ["A", "B"])  # 5 calendar days, 4 returns: coverage 1.0
    bh = pw.chained_buy_and_hold(ch, cl, {"A": 7.5, "B": 7.5}, {"A": 1.0, "B": 1.5})
    mult = ((1.0 - 0.00085) ** 2 + (1.0 - 0.0009) ** 2) / 2.0
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.05, rel=1e-12)
    assert bh["cost_multiplier"] == pytest.approx(mult, rel=1e-15)
    assert bh["buy_and_hold_total_return"] == pytest.approx(1.05 * mult - 1.0, rel=1e-12)
    assert bh["n_daily_returns"] == 4
    assert bh["cost_per_side_bps"] == pytest.approx({"A": 8.5, "B": 9.0})


def test_buy_and_hold_strategy_loss_across_a_missing_day_fails_the_bar():
    """Code review finding 1 probe: prices flat at 100; the strategy's equity
    falls 100 -> 50 across a day missing from the data (day 10 absent inside
    the window; days 0..30 otherwise). The multi-day step is not a daily
    return, but it IS in the chained level: strategy total = 0.5 - 1 = -0.5,
    buy-and-hold = 1.0 x (1 - 0.00085)^2 - 1 -> excess < 0 (FAIL). Counting
    only daily returns would have hidden the loss (strategy 0, excess > 0)."""
    eq = _skip_days(_bars(0, [100.0] * 10 + [50.0] * 21), {_day(10)})
    cl = _skip_days(_bars(0, [100.0] * 31), {_day(10)})
    ch = _chain({"w0": {"X": eq}}, ["X"])
    assert ch["n_multi_day_steps"] == 1
    assert all(r == 0.0 for _d, r in ch["daily_returns"])  # the loss is in no daily return
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": cl}}, {"X": 7.5}, {"X": 1.0})
    assert bh["strategy_total_return"] == pytest.approx(-0.5, rel=1e-12)
    assert bh["buy_and_hold_total_return"] == pytest.approx((1.0 - 0.00085) ** 2 - 1.0,
                                                            rel=1e-12)
    assert bh["excess_return"] < 0


def test_buy_and_hold_price_move_across_a_multi_day_step_is_included():
    """Strategy flat; the PRICE doubles across the missing day 10: buy-and-hold
    gross = 1.0 (level 100 -> 200), not 0 -- both sides on the chained level."""
    eq = _skip_days(_bars(0, [1000.0] * 31), {_day(10)})
    cl = _skip_days(_bars(0, [100.0] * 10 + [200.0] * 21), {_day(10)})
    ch = _chain({"w0": {"X": eq}}, ["X"])
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": cl}}, {"X": 0.0}, {"X": 0.0})
    assert bh["buy_and_hold_gross_return"] == pytest.approx(1.0, rel=1e-12)
    assert bh["excess_return"] == pytest.approx(-1.0, rel=1e-12)


def test_buy_and_hold_is_flat_across_a_real_protocol_gap_for_both_sides():
    """w0 days 0..19 and w1 days 21..40 with nominal starts 0 and 21 (a real
    gap, day 20). Prices jump 100 -> 200 across the gap and then rise to 220 on
    w1's last day. Across the gap both sides are flat (no window was trading),
    so buy-and-hold gross = (100/100) x (220/200) - 1 = 0.1; the strategy
    (flat equity) is 0."""
    eq = {"w0": {"X": _bars(0, [1.0] * 20)}, "w1": {"X": _bars(21, [1.0] * 20)}}
    cl = {"w0": {"X": _bars(0, [100.0] * 20)},
          "w1": {"X": _bars(21, [200.0] * 19 + [220.0])}}
    ch = _chain(eq, ["X"], _bnd(w0=(0, 19), w1=(21, 40)))
    bh = pw.chained_buy_and_hold(ch, cl, {"X": 0.0}, {"X": 0.0})
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.1, rel=1e-12)
    assert bh["strategy_total_return"] == 0.0
    assert bh["n_daily_returns"] == len(ch["daily_returns"]) == 38


def test_buy_and_hold_mismatched_inputs_raise_value_error_not_not_evaluable():
    eq = {"w0": {"X": _bars(0, [1.0] * 5)}}
    ch = _chain(eq, ["X"])

    def raises(exc_match, *args):
        with pytest.raises(ValueError, match=exc_match) as ei:
            pw.chained_buy_and_hold(ch, *args)
        assert not isinstance(ei.value, NE)

    raises("different common days", {"w0": {"X": _bars(0, [1.0] * 6)}}, {"X": 1}, {"X": 1})
    raises("differ from the chained windows", {"w9": {"X": _bars(0, [1.0] * 5)}},
           {"X": 1}, {"X": 1})
    raises("has coins", {"w0": {"X": _bars(0, [1.0] * 5), "Y": _bars(0, [1.0] * 5)}},
           {"X": 1}, {"X": 1})
    raises("has coins", {"w0": {"Y": _bars(0, [1.0] * 5)}}, {"X": 1}, {"X": 1})
    raises("inconsistent", {"w0": {"X": _bars(0, [1.0])}}, {"X": 1}, {"X": 1})
    raises("no fee/slippage", {"w0": {"X": _bars(0, [1.0] * 5)}}, {}, {"X": 1})
    raises("non-negative", {"w0": {"X": _bars(0, [1.0] * 5)}}, {"X": -1}, {"X": 1})
    raises("non-negative", {"w0": {"X": _bars(0, [1.0] * 5)}}, {"X": True}, {"X": 1})
    bad = _bars(0, [1.0] * 5)
    bad[datetime(2020, 1, 3, 23)] = float("nan")
    raises("finite positive", {"w0": {"X": bad}}, {"X": 1}, {"X": 1})
    with pytest.raises(ValueError, match="not a chain_windows result"):
        pw.chained_buy_and_hold({}, {"w0": {"X": _bars(0, [1.0] * 5)}}, {"X": 1}, {"X": 1})


def test_numpy_scalars_are_numbers_and_numpy_bools_are_not():
    np = pytest.importorskip("numpy")
    eq = {t: np.float64(v) for t, v in _bars(0, [1000.0] * 11).items()}
    cl = {t: np.float32(v) for t, v in _bars(0, [100.0 + i for i in range(11)]).items()}
    ch = _chain({"w0": {"X": eq}}, ["X"])
    bh = pw.chained_buy_and_hold(ch, {"w0": {"X": cl}}, {"X": np.float64(7.5)},
                                 {"X": np.int64(1)})
    assert bh["buy_and_hold_gross_return"] == pytest.approx(0.1, rel=1e-6)
    bad = dict(eq)
    bad[datetime(2020, 1, 2, 23)] = np.bool_(True)
    with pytest.raises(ValueError, match="not a number"):
        _chain({"w0": {"X": bad}}, ["X"])


def test_fee_is_the_commission_run_protocol_charged_via_the_shared_function():
    """One definition (code review finding 3): charged_fee_bps is
    cost_helpers.resolve_fee_bps, of which resolve_commission_rate -- what
    run_protocol passes to run_backtest (its old names are aliases of it) -- is
    the /10000 form. Spot 7.5, perp 5, --commission-bps wins; never the
    manifest's fee_bps (10)."""
    import cost_helpers
    import run_protocol as rp
    assert rp._commission_rate_for_symbol is cost_helpers.commission_rate_for_symbol
    assert rp._resolve_commission_rate is cost_helpers.resolve_commission_rate
    cm = yaml.safe_load((SR_ROOT / "config" / "cost_model.yaml").read_text(encoding="utf-8"))
    for sym, bps, prod in (("BTCUSDT", None, "spot"), ("ETHUSDT", None, "perp"),
                           ("BTCUSDT", 10.0, "spot"), ("NOPEUSDT", None, "spot")):
        assert pw.charged_fee_bps(sym, cm, bps, prod) == pytest.approx(
            rp._resolve_commission_rate(sym, cm, bps, prod) * 10_000.0, rel=1e-15)
        assert pw.charged_fee_bps(sym, cm, bps, prod) == cost_helpers.resolve_fee_bps(
            sym, cm, bps, prod)
    assert pw.charged_fee_bps("BTCUSDT", cm) == pytest.approx(7.5)
    assert pw.charged_fee_bps("BTCUSDT", cm, product="perp") == pytest.approx(5.0)
    assert pw.charged_fee_bps("BTCUSDT", cm, commission_bps=10.0) == pytest.approx(10.0)
    assert pw.charged_fee_bps("BTCUSDT", cm) != 10  # the manifest's fee_bps
    with pytest.raises(ValueError, match="default rate"):
        pw.charged_fee_bps("BTCUSDT", None)
    with pytest.raises(ValueError, match="default rate"):
        pw.charged_fee_bps("ETHUSDT", {"fee_rate_bps": {"BTCUSDT": 7.5}})
    with pytest.raises(ValueError, match="commission_bps"):
        pw.charged_fee_bps("BTCUSDT", cm, commission_bps=float("nan"))


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
    with pytest.raises(ValueError, match="not hashable"):
        pw.slippage_bps_for_symbol(table, ["BTCUSDT"])


def test_window_close_bars_reader(tmp_path):
    eq = _bars(0, [1000.0, 1001.0, 1002.0])
    cl = _bars(0, [10.0, 11.0, 12.0])
    _write_states(tmp_path, "r1", eq, cl)
    p = tmp_path / "results" / "r1" / "portfolio_states.csv"
    got = pw.window_close_bars(p)
    assert got == cl  # warm-up row (close -1) dropped by the NOT_READY filter
    q = tmp_path / "noclose.csv"
    q.write_text("timestamp,regime,postRebalance_total_value\n2020-01-01 23:00:00,trend,1\n",
                 encoding="utf-8")
    with pytest.raises(ValueError, match="lacks column"):
        pw.window_close_bars(q)
    z = tmp_path / "zero.csv"
    z.write_text("timestamp,regime,close\n2020-01-01 23:00:00,trend,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="close 0.0"):
        pw.window_close_bars(z)
    dup = tmp_path / "dup.csv"
    dup.write_text("timestamp,regime,close\n2020-01-01 23:00:00,trend,5\n"
                   "2020-01-01 23:00:00,trend,6\n", encoding="utf-8")
    with pytest.raises(ValueError, match="two different closes"):
        pw.window_close_bars(dup)
    same = tmp_path / "same.csv"
    same.write_text("timestamp,regime,close\n2020-01-01 23:00:00,trend,5\n"
                    "2020-01-01 23:00:00,trend,5\n", encoding="utf-8")
    assert pw.window_close_bars(same) == {datetime(2020, 1, 1, 23): 5.0}


def test_window_close_bars_parses_exactly_like_window_equity_bars(tmp_path):
    """Code review finding 8: the copy must read the same rows. One CSV with
    NOT_READY rows before AND inside the window (a large-gap reset), mixed-case
    and padded regime labels, timezone-aware stamps (+00:00 and +02:00), rows
    out of order, and the engine's re-recorded final bar (same timestamp, same
    close, different equity): both readers return the same timestamps in the
    same order; the equity reader keeps the last equity, as it always did."""
    rows = [
        "timestamp,regime,postRebalance_total_value,close",
        "2019-12-31 22:00:00,NOT_READY,999.0,1.0",
        "2020-01-01 23:00:00,trend,100.0,10.0",
        "2020-01-02 01:00:00+00:00,range,101.0,10.5",
        "2020-01-02 03:00:00+02:00, not_ready ,555.0,99.0",
        "2020-01-03 23:00:00,Trend,103.0,11.0",
        "2020-01-02 23:00:00,trend,102.0,10.8",
        "2020-01-04 00:30:00+02:00,trend,104.0,11.2",
        "2020-01-04 23:00:00,trend,105.0,11.5",
        "2020-01-04 23:00:00,trend,104.5,11.5",
    ]
    p = tmp_path / "states.csv"
    p.write_text("\n".join(rows) + "\n", encoding="utf-8")
    closes = pw.window_close_bars(p)
    equity = pdv1.window_equity_bars(p)
    assert list(closes) == list(equity)
    assert list(closes) == [datetime(2020, 1, 1, 23), datetime(2020, 1, 2, 1),
                            datetime(2020, 1, 2, 23), datetime(2020, 1, 3, 22, 30),
                            datetime(2020, 1, 3, 23), datetime(2020, 1, 4, 23)]
    assert equity[datetime(2020, 1, 4, 23)] == 104.5
    assert closes[datetime(2020, 1, 4, 23)] == 11.5


# ---------------------------------------------------------------------------
# G7: pooled edge / cost ratio
# ---------------------------------------------------------------------------

def _trade(sym="BTCUSDT", win="w0", reason="signal_flip", rr=0.5, cost=15.0):
    return {"symbol": sym, "window": win, "exit_reason": reason, "realized_return": rr,
            "cost_paid": cost}


def test_edge_cost_ratio_on_non_forced_trades_with_the_floor():
    """100 signal trades, gross 0.33% = 33 bps each, cost 15 bps: 33/15 = 2.2
    (unrounded float), both ratios equal with no forced close."""
    recs = [_trade(rr=0.33) for _ in range(100)]
    got = pw.pooled_edge_to_cost_ratio(recs, min_trades=100)
    assert got["ratio"] == pytest.approx(2.2, rel=1e-12)
    assert got["ratio_all_trades"] == got["ratio_excluding_end_of_window"] == got["ratio"]
    assert got["n_trades"] == 100 and got["n_excluded_end_of_window"] == 0


def test_edge_cost_ratio_forced_close_gains_cannot_lift_it():
    """100 signal trades at 30 bps plus 50 forced closes at 300 bps: over all
    records (100x30 + 50x300)/150/15 = 8.0; without the forced closes 30/15 =
    2.0; the bar reads the lower, 2.0, over exactly 100 trades."""
    recs = ([_trade(rr=0.30) for _ in range(100)]
            + [_trade(reason="end_of_window", rr=3.0) for _ in range(50)])
    got = pw.pooled_edge_to_cost_ratio(recs, min_trades=100)
    assert got["ratio_all_trades"] == pytest.approx(8.0, rel=1e-12)
    assert got["ratio_excluding_end_of_window"] == pytest.approx(2.0, rel=1e-12)
    assert got["ratio"] == got["ratio_excluding_end_of_window"]
    assert got["n_trades"] == 100 and got["n_excluded_end_of_window"] == 50


def test_edge_cost_ratio_forced_close_losses_cannot_be_hidden_probe():
    """Second-round finding 2 probe: 100 signal trades at +33 bps and 50 forced
    closes at -300 bps, all at 15 bps cost. Non-forced only: 33/15 = 2.2 (would
    pass a `>= 2.2` reading); over all records (100x33 - 50x300)/150 = -78 bps
    -> -78/15 = -5.2. The bar reads min = -5.2: FAIL."""
    recs = ([_trade(rr=0.33) for _ in range(100)]
            + [_trade(reason="end_of_window", rr=-3.0) for _ in range(50)])
    got = pw.pooled_edge_to_cost_ratio(recs, min_trades=100)
    assert got["ratio_excluding_end_of_window"] == pytest.approx(2.2, rel=1e-12)
    assert got["ratio_all_trades"] == pytest.approx(-5.2, rel=1e-12)
    assert got["ratio"] == got["ratio_all_trades"]
    assert not got["ratio"] > 2.2


def test_always_long_two_coins_96_windows_is_not_evaluable_not_pass():
    """Code review finding 6: one forced close per (coin, window), 2 x 96 = 192
    records, each gross 5% against 15 bps -- pooled over all records the ratio
    is 33 with n = 192 >= 100 (a PASS). Without forced closes: 0 trades."""
    recs = [_trade(sym=s, win=f"w{k}", reason="end_of_window", rr=5.0)
            for s in ("BTCUSDT", "ETHUSDT") for k in range(96)]
    import cost_helpers
    assert cost_helpers.realized_edge_to_cost_ratio(recs) > 2.2  # the flattering number
    with pytest.raises(NE, match="0 trade.*192 end_of_window.*min_trades=100"):
        pw.pooled_edge_to_cost_ratio(recs, min_trades=100)


def test_edge_cost_ratio_is_unrounded_so_just_below_the_bar_stays_below():
    """Second-round finding 7: gross 32.9994 bps / 15 bps = 2.19996, which the
    descriptive summary rounds to 2.2. The bar value stays 2.19996 < 2.2 (FAIL
    under `> 2.2` and under `>= 2.2`)."""
    import cost_helpers
    recs = [_trade(rr=0.329994) for _ in range(100)]
    got = pw.pooled_edge_to_cost_ratio(recs, min_trades=100)["ratio"]
    assert cost_helpers.realized_edge_to_cost_ratio(recs) == 2.2
    assert got == pytest.approx(2.19996, rel=1e-9)
    assert got < 2.2 and not got >= 2.2


@pytest.mark.parametrize("recs,frag", [
    ([_trade() for _ in range(99)], "fewer than min_trades=100"),
    ([_trade() for _ in range(99)] + [_trade(cost=None)], "lack a measured cost"),
    ([_trade() for _ in range(100)] + [_trade(reason="end_of_window", cost=None)],
     "1 of 101 trade record"),
    ([_trade(cost=0.0) for _ in range(120)], "zero mean measured cost"),
    ([], "fewer than min_trades=100"),
])
def test_edge_cost_ratio_not_evaluable(recs, frag):
    with pytest.raises(NE, match=frag):
        pw.pooled_edge_to_cost_ratio(recs, min_trades=100)


def test_edge_cost_ratio_bad_inputs_raise_value_error():
    ok = [_trade() for _ in range(100)]
    for bad_min in (0, True, 1.5):
        with pytest.raises(ValueError, match="min_trades"):
            pw.pooled_edge_to_cost_ratio(ok, min_trades=bad_min)
    for bad in (_trade(rr=float("nan")), _trade(rr=None), _trade(cost=-1.0),
                _trade(cost=float("inf")), _trade(reason="take_profit"), _trade(sym=["X"]),
                _trade(reason="end_of_window", rr=None), {"symbol": "X"}, "not a record"):
        with pytest.raises(ValueError) as ei:
            pw.pooled_edge_to_cost_ratio(ok + [bad], min_trades=100)
        assert not isinstance(ei.value, NE)
    with pytest.raises(ValueError, match="trade_records must be a list"):
        pw.pooled_edge_to_cost_ratio({"trades": ok}, min_trades=100)


def test_edge_cost_ratio_is_the_shared_function_run_protocol_uses():
    """Same formula, one definition: on the same (non-forced) records the bar's
    unrounded value, rounded to 4 decimals, is run_protocol's summary figure."""
    import cost_helpers
    import run_protocol as rp
    recs = []
    for k in range(120):
        recs.append({"symbol": "BTCUSDT" if k % 2 else "ETHUSDT", "window": f"w{k % 4}",
                     "exit_reason": "signal_flip", "realized_return": 0.2 + 0.01 * (k % 7),
                     "cost_paid": 15.0, "net_portfolio_return_pct": 0.05, "holding_bars": 3,
                     "mae": 0.1, "mfe": 0.3, "profitable_net": True, "entry_efficiency": None,
                     "exit_efficiency": None})
    summary = rp._aggregate_trade_diagnostics(recs, [{"core": {"trade_count": 30}}] * 4)
    got = pw.pooled_edge_to_cost_ratio(recs, min_trades=100)
    assert got["ratio"] == cost_helpers.realized_edge_to_cost_ratio_unrounded(recs)
    assert round(got["ratio"], 4) == summary["realized_edge_to_cost_ratio"]
    assert got["n_trades"] == 120


# ---------------------------------------------------------------------------
# run_protocol cost_paid: the fee actually charged (second-round finding 6)
# ---------------------------------------------------------------------------

# _cost_paid_bps outputs with the DEFAULT flags, computed with the code at
# 946c9023 (before the change) on the real config/cost_model.yaml and edge
# cases; the new code must return exactly these.
_COST_PAID_DEFAULT_PINS = [
    ({"symbol": "BTCUSDT"}, "real", 15.0), ({"symbol": "ETHUSDT"}, "real", 15.0),
    ({"symbol": "SOLUSDT"}, "real", 15.0), ({"symbol": "AVAXUSDT"}, "real", 15.0),
    ({"symbol": "BNBUSDT"}, "real", 12.0), ({"symbol": "NOPEUSDT"}, "real", 15.0),
    ({"symbol": ""}, "real", 15.0), ({}, "real", 15.0),
    ({"symbol": "BTCUSDT"}, {"fee_rate_bps": {}}, 20.0),
    ({"symbol": "BTCUSDT", "total_commission_percent": 0.15}, None, 15.0),
    ({"symbol": "BTCUSDT"}, None, 0.0),
    ({"symbol": "BTCUSDT", "total_commission_percent": 0.2}, {}, 20.0),
    ({"symbol": "X"}, {"fee_rate_bps": {"X": 3.333}}, 6.67),
]


def test_cost_paid_default_flags_byte_identical():
    import run_protocol as rp
    cm = yaml.safe_load((SR_ROOT / "config" / "cost_model.yaml").read_text(encoding="utf-8"))
    for trade, model, expected in _COST_PAID_DEFAULT_PINS:
        got = rp._cost_paid_bps(dict(trade), cm if model == "real" else model)
        assert got == expected and type(got) is float, (trade, model, got)
        got2 = rp._cost_paid_bps(dict(trade), cm if model == "real" else model, None, "spot")
        assert got2 == expected


def test_cost_paid_follows_commission_bps_and_cost_product():
    """cost_paid = 2 x the one-way fee the engine charged, by the same lookup
    (charged_fee_bps / resolve_fee_bps): --commission-bps 10 -> 20 bps round
    trip (was 15, the spot table's); --cost-product perp -> 10 (was 15)."""
    import run_protocol as rp
    cm = yaml.safe_load((SR_ROOT / "config" / "cost_model.yaml").read_text(encoding="utf-8"))
    t = {"symbol": "BTCUSDT"}
    assert rp._cost_paid_bps(t, cm, 10.0, "spot") == 20.0
    assert rp._cost_paid_bps(t, cm, None, "perp") == 10.0
    assert rp._cost_paid_bps(t, None, 12.5, "spot") == 25.0
    for bps, prod in ((10.0, "spot"), (None, "perp"), (None, "spot"), (3.0, "perp")):
        assert rp._cost_paid_bps(t, cm, bps, prod) == round(
            2 * pw.charged_fee_bps("BTCUSDT", cm, bps, prod), 2)


def test_cost_paid_through_the_trade_records_with_commission_bps(tmp_path):
    """End to end through _compute_trade_records_for_window: a run made with
    --commission-bps 10 records cost_paid 20.0 (2 x 10), the fee the engine
    charged; the default call still records 15.0."""
    import csv
    import json
    import run_protocol as rp
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    stamps = [f"2020-01-0{d} 0{h}:00:00" for d in (1, 2, 3) for h in range(3)]
    with open(run_dir / "bars.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["timestamp", "open", "high", "low", "close"])
        w.writeheader()
        for i, ts in enumerate(stamps):
            w.writerow({"timestamp": ts, "open": 100.0 + i, "high": 101.0 + i,
                        "low": 99.0 + i, "close": 100.5 + i})
    trade = {"trade_id": "t1", "symbol": "BTCUSDT", "side": "LONG", "entry_price": 100.0,
             "exit_price": 101.0, "entry_time": "2020-01-01T01:00:00",
             "exit_time": "2020-01-02T01:00:00", "duration_minutes": 1440.0,
             "profit_loss_percent": 1.0, "net_portfolio_profit_loss_percent": 0.8,
             "profitable_net": True, "exit_forecast": -1.0, "total_commission_percent": 0.2}
    (run_dir / "trades.json").write_text(json.dumps([trade]), encoding="utf-8")
    cm = yaml.safe_load((SR_ROOT / "config" / "cost_model.yaml").read_text(encoding="utf-8"))
    (rec,) = rp._compute_trade_records_for_window(run_dir, "BTCUSDT", "w", "2020-01-04", cm,
                                                  commission_bps=10.0, cost_product="spot")
    assert rec["cost_paid"] == 20.0
    (rec,) = rp._compute_trade_records_for_window(run_dir, "BTCUSDT", "w", "2020-01-04", cm)
    assert rec["cost_paid"] == 15.0


def test_run_protocol_passes_the_runs_fee_flags_to_the_trade_records():
    """Static check of the one call site in main(): the run's own
    --commission-bps / --cost-product reach cost_paid."""
    src = (SR_ROOT / "tools" / "run_protocol.py").read_text(encoding="utf-8")
    assert src.count("_compute_trade_records_for_window(") == 2  # the def + one call
    assert src.count("= _compute_trade_records_for_window(\n") == 1
    assert "commission_bps=args.commission_bps, cost_product=args.cost_product," in src


def _pin_records(kind: str) -> list:
    recs = []
    for k in range(60):
        cost = 15.0 if k % 2 else 12.0
        if kind == "partial" and k % 5 == 0:
            cost = None
        if kind == "none":
            cost = None
        if kind == "zero":
            cost = 0.0
        recs.append({
            "symbol": "BTCUSDT" if k % 3 else "ETHUSDT", "window": f"w{k % 6}",
            "exit_reason": "end_of_window" if k % 7 == 0 else "signal_flip",
            "realized_return": ((k * 37) % 23 - 9) / 10.0, "cost_paid": cost,
            "net_portfolio_return_pct": ((k * 11) % 13 - 6) / 100.0, "holding_bars": 1 + k % 9,
            "mae": 0.1 * (k % 4), "mfe": 0.2 * (k % 5), "profitable_net": bool(k % 2),
            "entry_efficiency": 0.5, "exit_efficiency": None,
        })
    return recs


# run_protocol._aggregate_trade_diagnostics output on _pin_records, computed at
# the base commit (origin/master 21920594) BEFORE the ratio moved to
# cost_helpers: (realized_edge_to_cost_ratio, sha256 of the whole summary as
# json.dumps(sort_keys=True)). The refactor must reproduce both exactly.
_RP_SUMMARY_PINS = {
    "full": (1.3951, "d1afb4879085e77573a5577ca6276a713182b9475c5269cb1bdd77e28e6abfda"),
    "partial": (2.392, "7776b8b430a73e7d93267616b557ed1b093457ee506fe329df33cba1323f190d"),
    "none": (None, "5d2546a26ad7e6ee83dbe7ba85480b44c7504eb917c3d1cea3e11fd103249555"),
    "zero": (None, "51fefa58e5b380db33e24778a20a53e9fd18596f1a1f168be2b0f5de9e8f60e7"),
}


@pytest.mark.parametrize("kind", sorted(_RP_SUMMARY_PINS))
def test_run_protocol_trade_summary_byte_identical_after_the_refactor(kind):
    import json
    import run_protocol as rp
    s = rp._aggregate_trade_diagnostics(_pin_records(kind), [{"core": {"trade_count": 10}}] * 6)
    ratio, digest = _RP_SUMMARY_PINS[kind]
    assert s["realized_edge_to_cost_ratio"] == ratio
    assert hashlib.sha256(json.dumps(s, sort_keys=True, default=str).encode()).hexdigest() \
        == digest


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
