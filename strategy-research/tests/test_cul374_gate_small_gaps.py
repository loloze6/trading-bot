"""
CUL-374: the data gate does not pause a run over gaps the engine ignores.

Before: any missing bar in a window made it `refine`, which pauses the run
for a human (or marks a variant not_tested). The engine's own gap rule
(trading-bot core/launcher.py DEFAULT_GAP_POLICY) treats a stretch of up to
`ignore_max_bars` (3) missing bars as nothing -- on Kraken 1h these are mostly
hours with no trades, where the exchange writes no candle. Measured
2026-10-02: Kraken BTCUSD/ETHUSD 1h miss exactly one bar each in 2022-2023.

Now: a window within the tolerance whose every gap is <= that limit is
`validate`, with the gaps recorded. Longer gaps, or more than the tolerance
in total, are judged exactly as before.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "tools"))

import data_availability_gate as dag  # noqa: E402

START, END = "2022-01-01", "2022-04-30"  # one 4-month window, 2,880 hourly bars


class _FakeDM:
    df = None

    def __init__(self, *a, **kw):
        self.fetch_interval_seconds = 3600

    def fetch_historical_data(self, *a, **kw):
        return self.df


def _check(monkeypatch, drop_hours):
    full = pd.date_range(f"{START} 00:00", f"{END} 23:00", freq="h")
    _FakeDM.df = pd.DataFrame({"timestamp": full.delete(sorted(drop_hours))})
    monkeypatch.setattr(dag, "DataManager", _FakeDM)
    return dag.check_price_window("BTCUSD", "kraken", "1h", START, END, fetch_interval_seconds=None)


def test_a_complete_window_is_unchanged(monkeypatch):
    res = _check(monkeypatch, [])
    assert res["outcome"] == "validate" and res["reason"] == "fully available"
    assert "small_gaps" not in res


@pytest.mark.parametrize("drop", [[100], [100, 101, 102], [100, 101, 102, 500, 501, 502]])
def test_gaps_the_engine_ignores_validate_and_are_recorded(monkeypatch, drop):
    res = _check(monkeypatch, drop)
    assert res["outcome"] == "validate", res
    assert res["missing_fraction"] > 0
    assert sum(g["bars"] for g in res["small_gaps"]) == len(drop)
    assert "ignore_max_bars=3" in res["reason"]


def test_a_four_bar_gap_is_judged_as_before(monkeypatch):
    res = _check(monkeypatch, [100, 101, 102, 103])
    assert res["outcome"] == "refine" and "small_gaps" not in res


@pytest.mark.parametrize("drop", [[0, 1], [2878, 2879]])  # at the window's start / end
def test_short_edge_gaps_count_as_small(monkeypatch, drop):
    res = _check(monkeypatch, drop)
    assert res["outcome"] == "validate", res
    assert [g["bars"] for g in res["small_gaps"]] == [2.0]


def test_many_small_gaps_over_the_tolerance_still_decline(monkeypatch):
    """Every other hour missing: each gap is one bar, but half the data is
    gone -- a quality problem, never waved through."""
    res = _check(monkeypatch, list(range(1, 2880, 2)))
    assert res["outcome"] == "decline"


def test_the_limit_is_read_from_the_engine(monkeypatch):
    import core.launcher as launcher
    monkeypatch.setitem(launcher.DEFAULT_GAP_POLICY, "ignore_max_bars", 0)
    assert _check(monkeypatch, [100])["outcome"] == "refine"
