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
