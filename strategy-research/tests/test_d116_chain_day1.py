"""D-116 (CUL-431's day-1 anchor defect): the whole-test chain counts each window's
first-day return, from its starting capital (total_portfolio_value on the first recorded
bar, before that bar's rebalance) to its anchor close. A declared change in output of
every v2 chain number; without start values the chain is exactly as before.

The cross-check on runs 084 / 088 / 089 (D-114's offline "with day-1" Sharpes) reads run
artifacts that are not in git: it runs where they exist (D113_RUNS_ROOT, or this checkout)
and skips elsewhere.
"""
from __future__ import annotations

import math
import os
import statistics
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

D0 = date(2020, 1, 1)


def _day(i: int) -> date:
    return D0 + timedelta(days=i)


def _bars(first: int, closes: list) -> dict:
    return {datetime(*_day(first + k).timetuple()[:3], 23): v for k, v in enumerate(closes)}


def _layout():
    """Two coins, w0 days 0..9 and w1 days 20..29 (a planned gap); the anchor closes are
    after a day-1 fill: X pays 0.4% on w0 and nothing on w1, Y pays 0.2% on both."""
    wins = {"w0": {"X": _bars(0, [996.0 * (1.001 ** k) for k in range(10)]),
                   "Y": _bars(0, [998.0 * (0.999 ** k) for k in range(10)])},
            "w1": {"X": _bars(20, [1000.0 * (1.002 ** k) for k in range(10)]),
                   "Y": _bars(20, [998.0 * (1.0005 ** k) for k in range(10)])}}
    bounds = {"w0": (_day(0), _day(9)), "w1": (_day(20), _day(29))}
    start = {"w0": {"X": 1000.0, "Y": 1000.0}, "w1": {"X": 1000.0, "Y": 1000.0}}
    return wins, bounds, start


def test_each_window_gets_its_day1_return_on_its_anchor_day():
    wins, bounds, start = _layout()
    old = pw.chain_windows(wins, ["X", "Y"], bounds)
    new = pw.chain_windows(wins, ["X", "Y"], bounds, start_values=start)
    r0 = ((996.0 / 1000.0) + (998.0 / 1000.0)) / 2 - 1   # -0.003
    r1 = ((1000.0 / 1000.0) + (998.0 / 1000.0)) / 2 - 1  # -0.001
    got = dict(new["daily_returns"])
    assert got[_day(0)] == pytest.approx(r0, abs=1e-15)
    assert got[_day(20)] == pytest.approx(r1, abs=1e-15)
    assert _day(0) not in dict(old["daily_returns"]) and _day(20) not in dict(old["daily_returns"])
    # every other return is unchanged
    assert [x for x in new["daily_returns"] if x[0] not in (_day(0), _day(20))] == old["daily_returns"]
    assert new["n_day1_returns"] == 2 and new["start_level"] == 1.0
    assert "start_level" not in old and "n_day1_returns" not in old
    # levels scaled: the chain's final level carries both day-1 returns
    assert new["daily_levels"][-1][1] == pytest.approx(
        old["daily_levels"][-1][1] * (1 + r0) * (1 + r1), rel=1e-12)
    # coverage: 20 counted days, 18 + 2 returns, no "+1"
    assert new["coverage"] == 20 / 20 and old["coverage"] == 19 / 20


def test_no_day1_fill_gives_an_exact_zero_return():
    wins, bounds, _ = _layout()
    start = {w: {c: min(wins[w][c].items())[1] for c in ("X", "Y")} for w in wins}
    new = pw.chain_windows(wins, ["X", "Y"], bounds, start_values=start)
    got = dict(new["daily_returns"])
    assert got[_day(0)] == 0.0 and got[_day(20)] == 0.0


def test_without_start_values_the_chain_is_exactly_as_before():
    wins, bounds, _ = _layout()
    a = pw.chain_windows(wins, ["X", "Y"], bounds)
    b = pw.chain_windows(wins, ["X", "Y"], bounds, start_values=None)
    assert a == b


def test_the_strategy_total_return_counts_the_first_windows_day1_cost():
    wins, bounds, start = _layout()
    chain = pw.chain_windows(wins, ["X", "Y"], bounds, start_values=start)
    closes = {w: {c: {t: 100.0 for t in wins[w][c]} for c in ("X", "Y")} for w in wins}
    bh = pw.chained_buy_and_hold(chain, closes, {"X": 0, "Y": 0}, {"X": 0, "Y": 0})
    assert bh["strategy_total_return"] == pytest.approx(chain["daily_levels"][-1][1] - 1.0, abs=1e-15)


def test_a_junction_window_gets_no_day1_return():
    """w1 starts on w0's last day (a shared junction day): its first day belongs to w0."""
    wins = {"w0": {"X": _bars(0, [1000.0 + k for k in range(10)])},
            "w1": {"X": _bars(9, [990.0 + k for k in range(10)])}}
    bounds = {"w0": (_day(0), _day(9)), "w1": (_day(9), _day(18))}
    start = {"w0": {"X": 1005.0}, "w1": {"X": 1000.0}}
    ch = pw.chain_windows(wins, ["X"], bounds, start_values=start)
    assert [s["kind"] for s in ch["segments"]] == ["first", "junction"]
    assert ch["n_day1_returns"] == 1
    assert dict(ch["daily_returns"])[_day(0)] == pytest.approx(1000.0 / 1005.0 - 1, abs=1e-15)
    days = [d for d, _r in ch["daily_returns"]]
    assert len(days) == 1 + 9 + 9 and len(set(days)) == len(days)  # w0's day 1, 9 + 9 steps
    pw._check_daily_returns(ch["daily_returns"])  # strictly increasing days: no extra on day 9


@pytest.mark.parametrize("bad", [
    {"w0": {"X": 1000.0}},                                        # a window missing
    {"w0": {"X": 1000.0, "Y": 1000.0}, "w1": {"X": 1000.0}},      # a coin missing
    {"w0": {"X": 1000.0, "Y": 0.0}, "w1": {"X": 1000.0, "Y": 1.0}},  # not positive
])
def test_malformed_start_values_raise(bad):
    wins, bounds, _ = _layout()
    with pytest.raises(ValueError):
        pw.chain_windows(wins, ["X", "Y"], bounds, start_values=bad)


def test_window_start_value_reads_the_first_recorded_bar(tmp_path):
    p = tmp_path / "portfolio_states.csv"
    p.write_text("timestamp,regime,total_portfolio_value,postRebalance_total_value\n"
                 "2020-01-01,NOT_READY,1000.0,1000.0\n"
                 "2020-01-02,trend,1000.0,999.5\n"
                 "2020-01-03,trend,1001.0,1001.0\n", encoding="utf-8")
    assert pw.window_start_value(p) == 1000.0
    p.write_text("timestamp,regime,postRebalance_total_value\n2020-01-02,trend,999.5\n",
                 encoding="utf-8")
    with pytest.raises(ValueError, match="total_portfolio_value"):
        pw.window_start_value(p)
    p.write_text("timestamp,regime,total_portfolio_value\n2020-01-01,NOT_READY,1000.0\n",
                 encoding="utf-8")
    with pytest.raises(ValueError, match="no recorded bar"):
        pw.window_start_value(p)


# ---------------------------------------------------------------------------
# Cross-check: D-114's offline "with day-1" Sharpes, now the pipeline's own
# ---------------------------------------------------------------------------

_RUNS_ROOT = Path(os.environ.get("D113_RUNS_ROOT") or SR_ROOT)
D114_WITH_DAY1 = {"run_089": 0.992612, "run_084": 1.407447, "run_088": 1.295332}


@pytest.mark.parametrize("run_id", sorted(D114_WITH_DAY1))
def test_the_pipeline_chain_reproduces_d114s_with_day1_sharpe(run_id, monkeypatch):
    run_dir = _RUNS_ROOT / "runs" / run_id
    prp = run_dir / "artifacts" / "protocol_result.yaml"
    if not prp.is_file():
        pytest.skip(f"{run_id}'s artifacts are not in this checkout (set D113_RUNS_ROOT)")
    import run_phase1_research as rpr
    monkeypatch.setattr(rpr, "ROOT", _RUNS_ROOT)
    pr = yaml.safe_load(prp.read_text(encoding="utf-8"))
    chain, _coins = rpr._whole_test_chain(run_dir, pr)
    assert len(chain["daily_returns"]) == 730 and chain["n_day1_returns"] == 6
    sr = pw.whole_test_sharpe(chain["daily_returns"])
    rets = [r for _d, r in chain["daily_returns"]]
    assert sr == pytest.approx(statistics.mean(rets) / statistics.stdev(rets) * math.sqrt(365),
                               rel=1e-12)
    assert sr == pytest.approx(D114_WITH_DAY1[run_id], abs=5e-7)


# ---------------------------------------------------------------------------
# Review of #406: buy-and-hold alignment, drawdown, overlap, messages, reader edges
# ---------------------------------------------------------------------------

def _intraday(first: int, n_days: int, start: float, step: float, *, day1_mid: float):
    """Two bars a day (11:00, 23:00); the first day's 11:00 bar is the first recorded bar."""
    out, v = {}, start
    for k in range(n_days):
        d = _day(first + k)
        out[datetime(d.year, d.month, d.day, 11)] = day1_mid if k == 0 else v
        if k > 0:
            v *= step
        out[datetime(d.year, d.month, d.day, 23)] = v
    return out


def test_buy_and_hold_starts_at_the_first_recorded_bar_on_intraday_bars():
    """The strategy's day-1 return runs from its first bar to the anchor close, so does
    buy-and-hold: on intraday bars its growth gains close(anchor) / close(first bar)."""
    eq = {"w0": {"X": _intraday(0, 10, 1000.0, 1.001, day1_mid=1000.0)}}
    px = {"w0": {"X": _intraday(0, 10, 110.0, 1.002, day1_mid=100.0)}}
    bounds = {"w0": (_day(0), _day(9))}
    with_d1 = pw.chain_windows(eq, ["X"], bounds, start_values={"w0": {"X": 1000.0}})
    without = pw.chain_windows(eq, ["X"], bounds)
    a = pw.chained_buy_and_hold(with_d1, px, {"X": 0}, {"X": 0})
    b = pw.chained_buy_and_hold(without, px, {"X": 0}, {"X": 0})
    assert 1 + a["buy_and_hold_gross_return"] == pytest.approx(
        (1 + b["buy_and_hold_gross_return"]) * (110.0 / 100.0), rel=1e-12)


def test_buy_and_hold_is_unchanged_on_daily_bars():
    wins, bounds, start = _layout()
    px = {w: {c: {t: 100.0 + i for i, t in enumerate(sorted(wins[w][c]))} for c in ("X", "Y")}
          for w in wins}
    a = pw.chained_buy_and_hold(pw.chain_windows(wins, ["X", "Y"], bounds, start_values=start),
                                px, {"X": 0, "Y": 0}, {"X": 0, "Y": 0})
    b = pw.chained_buy_and_hold(pw.chain_windows(wins, ["X", "Y"], bounds),
                                px, {"X": 0, "Y": 0}, {"X": 0, "Y": 0})
    assert a["buy_and_hold_gross_return"] == b["buy_and_hold_gross_return"]


def test_a_later_windows_day1_drop_is_in_the_drawdown():
    """Flat equity, a 1% day-1 cost on the gap window: the drawdown is that 1%."""
    wins = {"w0": {"X": _bars(0, [1000.0] * 10)}, "w1": {"X": _bars(20, [990.0] * 10)}}
    bounds = {"w0": (_day(0), _day(9)), "w1": (_day(20), _day(29))}
    start = {"w0": {"X": 1000.0}, "w1": {"X": 1000.0}}
    dd = pw.whole_test_max_drawdown(pw.chain_windows(wins, ["X"], bounds, start_values=start))
    assert dd["max_drawdown_pct"] == pytest.approx(1.0, rel=1e-12)
    assert pw.whole_test_max_drawdown(pw.chain_windows(wins, ["X"], bounds))["max_drawdown_pct"] == 0.0


def test_an_overlap_window_gets_no_day1_return():
    wins = {"w0": {"X": _bars(0, [1000.0 + k for k in range(11)])},
            "w1": {"X": _bars(7, [990.0 + k for k in range(14)])}}
    bounds = {"w0": (_day(0), _day(10)), "w1": (_day(7), _day(20))}
    ch = pw.chain_windows(wins, ["X"], bounds, start_values={"w0": {"X": 1000.0}, "w1": {"X": 1000.0}})
    assert [s["kind"] for s in ch["segments"]] == ["first", "overlap"]
    assert ch["n_day1_returns"] == 1
    pw._check_daily_returns(ch["daily_returns"])


def test_a_multi_day_step_with_start_values_and_the_coverage_message():
    """One day missing inside w0 (both coins): two returns lost, the day-1 return kept;
    below the floor the message says '+ 0'."""
    wins, bounds, start = _layout()
    for c in ("X", "Y"):
        wins["w0"][c] = {t: v for t, v in wins["w0"][c].items() if t.date() != _day(5)}
    ch = pw.chain_windows(wins, ["X", "Y"], bounds, start_values=start)
    assert ch["n_multi_day_steps"] == 1 and len(ch["daily_returns"]) == 18 - 2 + 2
    for c in ("X", "Y"):
        wins["w1"][c] = {t: v for t, v in wins["w1"][c].items() if t.date().day % 2}
    with pytest.raises(pdv1.PortfolioNotEvaluable, match=r"daily return\(s\) \+ 0 cover"):
        pw.chain_windows(wins, ["X", "Y"], bounds, start_values=start)


@pytest.mark.parametrize("rows, match", [
    ("2020-01-02,trend,abc\n", "non-numeric"),
    ("2020-01-02,trend,0\n", "finite positive"),
    ("2020-01-01,not_ready,5.0\n2020-01-02,trend,7.0\n", None),
])
def test_window_start_value_edges(tmp_path, rows, match):
    p = tmp_path / "portfolio_states.csv"
    p.write_text("timestamp,regime,total_portfolio_value\n" + rows, encoding="utf-8")
    if match:
        with pytest.raises(ValueError, match=match):
            pw.window_start_value(p)
    else:
        assert pw.window_start_value(p) == 7.0  # lower-case not_ready is skipped too
