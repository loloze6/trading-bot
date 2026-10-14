"""D-129: the whole-test drawdown is the worst drawdown within each contiguous stretch; the running
peak resets at each PLANNED protocol gap (a chain segment of kind "gap" with n_gap_days_before > 0).

Byte-identical on a chain with no planned gap (contiguous folds A and D, a single window, a
hand-made chain without segments). The cross-check on stored runs 081-083 (fold A) and 091 (fold D)
reads run artifacts that are not in git: it runs where they exist (D113_RUNS_ROOT, or this
checkout) and skips elsewhere.
"""
from __future__ import annotations

import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "workflow"))

import portfolio_whole_test as pw  # noqa: E402

D0 = date(2020, 1, 1)


def _day(i: int) -> date:
    return D0 + timedelta(days=i)


def _bars(first: int, closes: list) -> dict:
    return {datetime(*_day(first + k).timetuple()[:3], 23): v for k, v in enumerate(closes)}


def _reference_drawdown(bar_levels) -> float:
    """The pre-D-129 definition: one running peak over the whole chain."""
    peak, dd = None, 0.0
    for _ts, v in bar_levels:
        peak = v if peak is None or v > peak else peak
        dd = max(dd, 1.0 - v / peak)
    return dd * 100.0


def _two_windows(second_first_day: int):
    """One coin. w0 rises 10 days then falls; w1 (after a gap or right after) starts low and
    falls again. Equity is the coin's normalised close."""
    w0 = _bars(0, [1000.0, 1100.0, 1200.0, 1100.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0])
    w1 = _bars(second_first_day, [1000.0, 1000.0, 900.0, 900.0, 950.0, 950.0, 950.0, 950.0,
                                  950.0, 950.0])
    wins = {"w0": {"X": w0}, "w1": {"X": w1}}
    bounds = {"w0": (_day(0), _day(9)),
              "w1": (_day(second_first_day), _day(second_first_day + 9))}
    start = {"w0": {"X": 1000.0}, "w1": {"X": 1000.0}}
    return wins, bounds, start


def test_a_planned_gap_resets_the_peak():
    wins, bounds, start = _two_windows(20)
    chain = pw.chain_windows(wins, ["X"], bounds, start_values=start)
    assert [s["n_gap_days_before"] for s in chain["segments"]] == [0, 10]
    dd = pw.whole_test_max_drawdown(chain)
    # w0 alone: 1200 -> 1000 = 16.67%; w1 alone: 1000 -> 900 = 10%. The reset-free chain
    # carries w0's 1000-level into w1 and measures 1200 -> 900 = 25%.
    assert _reference_drawdown(chain["bar_levels"]) == pytest.approx(25.0, rel=1e-9)
    assert dd["max_drawdown_pct"] == pytest.approx(100 * (1 - 1000 / 1200), rel=1e-9)
    assert dd["n_stretches"] == 2


def test_the_gap_windows_own_day1_drop_stays_in():
    """The new stretch's peak is the capital carried in, so a fall from it on the gap
    window's first day is a drawdown, as for any later window before D-129."""
    w0 = _bars(0, [1000.0] * 10)
    w1 = _bars(20, [900.0] * 10)  # anchor close 10% below the starting value of 1000
    chain = pw.chain_windows({"w0": {"X": w0}, "w1": {"X": w1}}, ["X"],
                             {"w0": (_day(0), _day(9)), "w1": (_day(20), _day(29))},
                             start_values={"w0": {"X": 1000.0}, "w1": {"X": 1000.0}})
    assert pw.whole_test_max_drawdown(chain)["max_drawdown_pct"] == pytest.approx(10.0, rel=1e-9)


def test_windows_that_follow_each_other_do_not_reset():
    wins, bounds, start = _two_windows(10)
    chain = pw.chain_windows(wins, ["X"], bounds, start_values=start)
    assert chain["segments"][1]["kind"] == "gap" and chain["segments"][1]["n_gap_days_before"] == 0
    dd = pw.whole_test_max_drawdown(chain)
    assert dd["n_stretches"] == 1
    assert dd["max_drawdown_pct"] == _reference_drawdown(chain["bar_levels"])


def test_a_chain_without_segments_is_unchanged():
    chain = {"bar_levels": [(datetime(2020, 1, d), v) for d, v in
                            enumerate([1.0, 1.2, 0.9, 1.3, 1.0], start=1)]}
    dd = pw.whole_test_max_drawdown(chain)
    assert dd["max_drawdown_pct"] == _reference_drawdown(chain["bar_levels"])
    assert dd["n_stretches"] == 1 and dd["n_bars"] == 5


def test_peak_and_trough_timestamps_belong_to_the_worst_stretch():
    wins, bounds, start = _two_windows(20)
    chain = pw.chain_windows(wins, ["X"], bounds, start_values=start)
    dd = pw.whole_test_max_drawdown(chain)
    assert dd["peak_ts"].date() == _day(2) and dd["trough_ts"].date() == _day(4)


def test_three_stretches_take_the_worst():
    w = lambda first, lo: _bars(first, [1000.0, 1000.0, lo, lo, lo, lo, lo, lo, lo, lo])  # noqa: E731
    wins = {"a": {"X": w(0, 950.0)}, "b": {"X": w(20, 800.0)}, "c": {"X": w(40, 900.0)}}
    bounds = {k: (_day(s), _day(s + 9)) for k, s in (("a", 0), ("b", 20), ("c", 40))}
    start = {k: {"X": 1000.0} for k in wins}
    chain = pw.chain_windows(wins, ["X"], bounds, start_values=start)
    dd = pw.whole_test_max_drawdown(chain)
    assert dd["n_stretches"] == 3
    assert dd["max_drawdown_pct"] == pytest.approx(20.0, rel=1e-9)


_RUNS_ROOT = Path(os.environ.get("D113_RUNS_ROOT") or SR_ROOT)


@pytest.mark.parametrize("run_id", ["run_081", "run_082", "run_083", "run_091"])
def test_contiguous_stored_runs_recompute_to_the_pre_d129_number(run_id, monkeypatch):
    """Fold A (081-083) and fold D (091) are contiguous: no planned gap, one stretch, and the
    drawdown equals the single-peak definition on the same chain."""
    run_dir = _RUNS_ROOT / "runs" / run_id
    prp = run_dir / "artifacts" / "protocol_result.yaml"
    if not prp.is_file():
        pytest.skip(f"{run_id}'s artifacts are not in this checkout (set D113_RUNS_ROOT)")
    import run_phase1_research as rpr
    monkeypatch.setattr(rpr, "ROOT", _RUNS_ROOT)
    pr = yaml.safe_load(prp.read_text(encoding="utf-8"))
    chain, _coins = rpr._whole_test_chain(run_dir, pr)
    assert all(s["n_gap_days_before"] == 0 for s in chain["segments"])
    dd = pw.whole_test_max_drawdown(chain)
    assert dd["n_stretches"] == 1
    assert dd["max_drawdown_pct"] == _reference_drawdown(chain["bar_levels"])
    if run_id == "run_091":  # graded after D-116: its stored row is the same number, bit for bit
        ev = yaml.safe_load((run_dir / "artifacts" / "profit_bars_evaluation.yaml")
                            .read_text(encoding="utf-8"))
        stored = [b["actual"] for v in ev["variants"].values() for b in v["bars"]
                  if b.get("name") == "max_drawdown_pct_max"]
        assert stored == [dd["max_drawdown_pct"]]
    # runs 081-083 were graded before D-116's day-1 fix: their stored rows differ from any
    # recompute by that fix alone (27.95 vs 27.99, 22.48 vs 22.50, 17.31 vs 17.35), not by D-129.
