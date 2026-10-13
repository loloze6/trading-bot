"""D-113: the whole-test chain's coverage denominator excludes planned protocol
gap days (days inside no window's nominal span); a day missing inside a window
still counts. No flag: a declared output change for protocols with gaps,
byte-identical for contiguous protocols.

The fold-A recompute (runs 081-083, contiguous) reads run artifacts that are not
in git: it runs where they exist (the operator's checkout, or D113_RUNS_ROOT =
a strategy-research directory holding runs/ and protocols/) and skips elsewhere.
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

import portfolio_daily as pdv1  # noqa: E402
import portfolio_whole_test as pw  # noqa: E402

NE = pdv1.PortfolioNotEvaluable
D0 = date(2020, 1, 1)


def _day(i: int) -> date:
    return D0 + timedelta(days=i)


def _bars(first: int, closes: list, skip: set = frozenset()) -> dict:
    """{datetime: value}: day `first + k` gets a 23:00 bar carrying closes[k],
    except the day indices in `skip` (absolute)."""
    return {datetime(*_day(first + k).timetuple()[:3], 23): v
            for k, v in enumerate(closes) if first + k not in skip}


def _closes(n: int, seed: int) -> list:
    return [100.0 * (1.0 + 0.01 * (((k * 7 + seed) % 11) - 5) / 5) * (1.001 ** k)
            for k in range(n)]


# three 30-day windows with 30-day planned gaps between them: the fold-B shape
INTERLEAVED = {"w0": (0, 29), "w1": (60, 89), "w2": (120, 149)}


def _interleaved(skip: set = frozenset(), coins=("X", "Y")) -> tuple:
    wins = {w: {c: _bars(a, _closes(b - a + 1, i + j), skip) for j, c in enumerate(coins)}
            for i, (w, (a, b)) in enumerate(INTERLEAVED.items())}
    bounds = {w: (_day(a), _day(b)) for w, (a, b) in INTERLEAVED.items()}
    return wins, list(coins), bounds


def test_interleaved_protocol_becomes_evaluable():
    """87 returns + 1 = 88. Before D-113: 88 / 150 days (0.587) < 0.9,
    NOT_EVALUABLE. Now 60 gap days are not counted: 88 / 90 = 0.978."""
    wins, coins, bounds = _interleaved()
    ch = pw.chain_windows(wins, coins, bounds)
    assert len(ch["daily_returns"]) == 87
    assert ch["n_gap_days"] == 60 and ch["n_gap_links"] == 2
    assert ch["n_calendar_days"] == 150          # stays the whole nominal span
    assert ch["n_counted_calendar_days"] == 90   # D-113
    assert ch["coverage"] == 88 / 90
    sr = pw.whole_test_sharpe(ch["daily_returns"])
    assert isinstance(sr, float)
    stats = pw.whole_test_sharpe_stats(ch["daily_returns"])
    assert stats["T"] == 87


def test_missing_days_inside_windows_still_fail_the_floor():
    """Three non-adjacent days missing inside each window (both coins): each
    window keeps 27 of 30 days, so the per-window floor passes, but each missing
    day costs two returns: 3 x (29 - 6) = 69 returns, (69 + 1) / 90 = 0.778 <
    0.9 -> NOT_EVALUABLE. The missing days stay in the denominator."""
    skip = {a + k for a, _b in INTERLEAVED.values() for k in (5, 12, 20)}
    wins, coins, bounds = _interleaved(skip)
    with pytest.raises(NE, match="WHOLE_TEST_MIN_COVERAGE") as exc:
        pw.chain_windows(wins, coins, bounds)
    msg = str(exc.value)
    assert "69 daily return(s) + 1 cover 77.8% of the 90 counted calendar day(s)" in msg
    assert "minus 60 protocol gap day(s) over 2 gap link(s)" in msg and "D-113" in msg


def test_one_missing_day_per_window_passes_and_is_counted():
    """One day missing inside each window: 3 x 27 = 81 returns, (81 + 1) / 90:
    the denominator keeps the missing days (90, not 87)."""
    skip = {a + 10 for a, _b in INTERLEAVED.values()}
    wins, coins, bounds = _interleaved(skip)
    ch = pw.chain_windows(wins, coins, bounds)
    assert len(ch["daily_returns"]) == 81
    assert ch["n_counted_calendar_days"] == 90 and ch["coverage"] == 82 / 90


def _contiguous(skip=frozenset()):
    spans = {"w0": (0, 29), "w1": (30, 59), "w2": (60, 89)}
    wins = {w: {"X": _bars(a, _closes(b - a + 1, i), skip)} for i, (w, (a, b)) in enumerate(spans.items())}
    return wins, {w: (_day(a), _day(b)) for w, (a, b) in spans.items()}


def test_contiguous_protocol_unchanged():
    """A contiguous protocol (fold A's shape): the union of the windows is the
    whole span, so the denominator is the pre-D-113 one, nominal span minus the
    engine days."""
    wins, bounds = _contiguous()
    ch = pw.chain_windows(wins, ["X"], bounds)
    assert ch["n_gap_days"] == 0
    assert ch["n_counted_calendar_days"] == ch["n_calendar_days"] - len(ch["engine_gap_days_excluded"])
    assert ch["coverage"] == (len(ch["daily_returns"]) + 1) / 90


def test_contiguous_not_evaluable_text_is_the_pre_d113_text():
    """A contiguous protocol below the floor keeps the old reason, byte for byte
    (a stored NOT_EVALUABLE reason must not change)."""
    skip = {a + k for a in (0, 30, 60) for k in (4, 9, 14, 19, 24)}
    wins, bounds = _contiguous(skip)
    with pytest.raises(NE) as exc:
        pw.chain_windows(wins, ["X"], bounds)
    n_ret = 3 * (29 - 10)
    assert str(exc.value) == (
        f"whole test: {n_ret} daily return(s) + 1 cover {(n_ret + 1) / 90:.1%} of the 90 "
        f"counted calendar day(s) (nominal span {_day(0)} to {_day(89)} = 90 day(s), minus 0 "
        f"engine tail/head day(s); 0 protocol gap day(s) over 2 gap link(s) stay counted), "
        f"below WHOLE_TEST_MIN_COVERAGE={pw.WHOLE_TEST_MIN_COVERAGE}")


def test_engine_days_next_to_a_planned_gap_are_not_subtracted_twice():
    """w0 nominal 0..29 recorded 0..27 (2 engine tail days), w1 nominal 60..89
    recorded 62..89 (2 engine head days), a 30-day planned gap between: counted
    = 60 days inside the windows - 4 engine days = 56; returns 27 + 27 = 54."""
    wins = {"w0": {"X": _bars(0, _closes(28, 0))}, "w1": {"X": _bars(62, _closes(28, 1))}}
    bounds = {"w0": (_day(0), _day(29)), "w1": (_day(60), _day(89))}
    ch = pw.chain_windows(wins, ["X"], bounds)
    assert ch["n_engine_tail_days"] == 2 and ch["n_engine_head_days"] == 2
    assert ch["n_gap_days"] == 30 and ch["n_calendar_days"] == 90
    assert ch["n_counted_calendar_days"] == 56 and ch["coverage"] == 55 / 56


def test_overlap_and_order_do_not_change_the_counted_days():
    """w0 0..29 and w1 25..49 overlap (union 0..49), w2 70..99 after a 20-day
    gap: counted 80; the same windows given out of order chain identically."""
    spans = {"w0": (0, 29), "w1": (25, 49), "w2": (70, 99)}
    wins = {w: {"X": _bars(a, _closes(b - a + 1, i))} for i, (w, (a, b)) in enumerate(spans.items())}
    bounds = {w: (_day(a), _day(b)) for w, (a, b) in spans.items()}
    ch = pw.chain_windows(wins, ["X"], bounds)
    assert ch["n_gap_days"] == 20 and ch["n_counted_calendar_days"] == 80
    rev = {w: wins[w] for w in reversed(list(wins))}
    ch2 = pw.chain_windows(rev, ["X"], bounds)
    assert ch2["daily_returns"] == ch["daily_returns"] and ch2["coverage"] == ch["coverage"]


# ---------------------------------------------------------------------------
# Fold A (contiguous): runs 081-083's stored v2 chain rows recomputed with this code
# ---------------------------------------------------------------------------

_RUNS_ROOT = Path(os.environ.get("D113_RUNS_ROOT") or SR_ROOT)
# D-120 replaced the stored buy_and_hold_excess_return_min row by a Sharpe comparison under a
# new name, so the stored row has no recomputed twin: three chain rows are compared.
_CHAIN_ROWS = ("sharpe_min", "max_drawdown_pct_max", "avg_daily_return_min")


@pytest.mark.parametrize("run_id", ["run_081", "run_082", "run_083"])
def test_fold_a_stored_chain_rows_recompute_equal(run_id, monkeypatch):
    run_dir = _RUNS_ROOT / "runs" / run_id
    pb_path = run_dir / "artifacts" / "profit_bars_evaluation.yaml"
    if not pb_path.is_file():
        pytest.skip(f"{run_id}'s artifacts are not in this checkout (set D113_RUNS_ROOT)")
    import run_phase1_research as rpr
    monkeypatch.setattr(rpr, "ROOT", _RUNS_ROOT)  # the protocol file is relative to it
    pr = yaml.safe_load((run_dir / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
    stored = yaml.safe_load(pb_path.read_text(encoding="utf-8"))
    rows = [r for v in stored["variants"].values() for r in v["bars"]]
    stored_rows = {r["name"]: r for r in rows if r["name"] in _CHAIN_ROWS}
    assert set(stored_rows) == set(_CHAIN_ROWS)
    bars = {"cost_edge_min_trades": 100}
    # D-116 adds each window's day-1 return to the chain (a declared change); this test pins
    # D-113's own claim, so it reads the chain as it was before D-116 (no start values).
    real_chain = pw.chain_windows
    monkeypatch.setattr(pw, "chain_windows",
                        lambda *a, start_values=None, **k: real_chain(*a, **k))
    got = rpr._whole_test_profit_metrics(run_dir, pr, bars)
    for name in _CHAIN_ROWS:
        assert got[name]["actual"] == stored_rows[name]["actual"], name
        assert got[name]["note"] == stored_rows[name]["note"], name
        for k in ("n_counted_calendar_days", "coverage", "n_daily_returns"):
            assert got[name]["detail"][k] == stored_rows[name]["detail"][k], (name, k)
