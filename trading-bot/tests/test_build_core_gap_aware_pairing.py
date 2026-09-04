"""
CUL-266 (#50(A) on the PRIMARY backtest corr path): build_core must not pair a
forecast with a close that is not exactly one bar later.

`build_core` computes `forward_return = close.shift(-1)/close - 1`, which takes
the next ROW. Across a real hole in the cache that makes a multi-hour move wear
a one-bar label, and it flows into BOTH the correlation and `sigma_bar_bps`
(and therefore into CUL-264's cost hurdle, which consumes sigma).

These tests pin four things:
  1. No `candle_interval_seconds` -> byte-identical to before, new fields None.
  2. The suppression actually changes the correlation when a gap-adjacent bar
     is ACTIVE -- the case the fix exists for.
  3. It changes sigma even when the gap-adjacent bar is INACTIVE, because sigma
     spans all bars while the correlation is active-only. (This is the shape
     the real BTCUSDT data happens to have -- see the real-cache test below.)
  4. Skipped pairs are COUNTED, with `gap_skipped_pct` denominated in PAIRS
     REACHED (kept + skipped), matching prescreen's own `pairs_reached`.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from reporting.run_artifact import build_core  # noqa: E402


def _bars(forecasts, closes, timestamps):
    return pd.DataFrame(
        {"timestamp": pd.to_datetime(timestamps), "forecast": forecasts, "close": closes}
    )


def _hourly(n, start="2020-01-01"):
    return list(pd.date_range(start, periods=n, freq="h"))


# ---------------------------------------------------------------------------
# 1. Byte-identity when no interval is supplied
# ---------------------------------------------------------------------------

def test_no_candle_interval_is_byte_identical_and_reports_nothing():
    """Every existing caller passes no interval. Those callers must see exactly
    what they saw before, and must not be told "0 gaps" -- a measurement that
    was never taken."""
    n = 60
    forecasts = [((-1) ** i) * (5 + i % 5) for i in range(n)]
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    ts = _hourly(n)
    # A real hole: drop the 30th bar so the 29th's successor is 2h later.
    keep = [i for i in range(n) if i != 30]
    bars = _bars([forecasts[i] for i in keep], [closes[i] for i in keep],
                 [ts[i] for i in keep])

    core = build_core({}, [], bars)

    assert core["gap_skipped_pairs"] is None, (
        "no interval supplied means no gap check ran -- reporting 0 would claim "
        "a measurement that never happened"
    )
    assert core["gap_skipped_pct"] is None
    # The pre-existing fields still compute exactly as before.
    assert core["forecast_return_corr"] is not None
    assert core["sigma_bar_bps"] is not None


# ---------------------------------------------------------------------------
# 2. The correlation actually moves when a gap-adjacent bar is ACTIVE
# ---------------------------------------------------------------------------

def test_correlation_changes_when_gap_adjacent_bar_is_active():
    """The defect's whole point. A gap-spanning pair carries a multi-bar move
    labelled as one bar; if that bar is active it lands in the correlation.
    Constructed so the gap-spanning pair is a large, sign-flipping outlier, so
    its removal is unmistakable rather than a rounding difference."""
    n = 40
    ts = _hourly(n)
    forecasts = [5.0 if i % 2 == 0 else -5.0 for i in range(n)]   # every bar active
    closes = [100.0 + (1.0 if i % 2 == 0 else -1.0) for i in range(n)]

    # Drop bar 20 -> bar 19's successor is 2h later. Make that spanning move
    # huge and against the forecast's sign, so including it drags the corr.
    keep = [i for i in range(n) if i != 20]
    f = [forecasts[i] for i in keep]
    c = [closes[i] for i in keep]
    t = [ts[i] for i in keep]
    gap_row = t.index(ts[19])
    c[gap_row + 1] = c[gap_row] * 2.0            # +100% "one-bar" move
    f[gap_row] = 5.0                              # active, positive forecast

    bars = _bars(f, c, t)

    naive = build_core({}, [], bars)
    fixed = build_core({}, [], bars, candle_interval_seconds=3600)

    assert fixed["gap_skipped_pairs"] == 1
    assert naive["forecast_return_corr"] != fixed["forecast_return_corr"], (
        "the gap-spanning pair was active and outsized -- suppressing it MUST "
        "move the correlation, or the fix is not reaching the corr population"
    )


# ---------------------------------------------------------------------------
# 3. Sigma moves even when the gap-adjacent bar is inactive
# ---------------------------------------------------------------------------

def test_sigma_changes_even_when_gap_adjacent_bar_is_inactive():
    """sigma_bar_bps spans ALL bars; the correlation is active-only. So an
    inactive gap-adjacent bar is invisible to the correlation but still
    inflates sigma -- and sigma feeds CUL-264's cost hurdle. This is the shape
    the real BTCUSDT window actually has."""
    n = 40
    ts = _hourly(n)
    forecasts = [5.0 if i % 2 == 0 else -5.0 for i in range(n)]
    closes = [100.0 + (1.0 if i % 2 == 0 else -1.0) for i in range(n)]

    keep = [i for i in range(n) if i != 20]
    f = [forecasts[i] for i in keep]
    c = [closes[i] for i in keep]
    t = [ts[i] for i in keep]
    gap_row = t.index(ts[19])
    c[gap_row + 1] = c[gap_row] * 2.0            # huge spanning move
    f[gap_row] = 0.0                              # INACTIVE -> corr never sees it

    bars = _bars(f, c, t)

    naive = build_core({}, [], bars)
    fixed = build_core({}, [], bars, candle_interval_seconds=3600)

    assert fixed["gap_skipped_pairs"] == 1
    assert naive["forecast_return_corr"] == fixed["forecast_return_corr"], (
        "the gap bar is inactive, so the active-only correlation cannot see it"
    )
    assert naive["sigma_bar_bps"] != fixed["sigma_bar_bps"], (
        "sigma spans all bars, so the gap-inflated 'one-bar' move MUST be "
        "excluded -- otherwise the cost hurdle rests on a fabricated volatility"
    )
    assert fixed["sigma_bar_bps"] < naive["sigma_bar_bps"]


# ---------------------------------------------------------------------------
# 4. Counting and the denominator
# ---------------------------------------------------------------------------

def test_gap_skipped_pct_denominator_is_pairs_reached():
    """prescreen denominates gap_skipped_pct in PAIRS REACHED (kept + skipped),
    not total bars (prescreen_signal.py::run_prescreen). Same contract here."""
    n = 30
    ts = _hourly(n)
    forecasts = [((-1) ** i) * 5.0 for i in range(n)]
    closes = [100.0 + i * 0.5 for i in range(n)]

    keep = [i for i in range(n) if i not in (10, 20)]   # two holes
    bars = _bars([forecasts[i] for i in keep], [closes[i] for i in keep],
                 [ts[i] for i in keep])

    core = build_core({}, [], bars, candle_interval_seconds=3600)

    kept_plus_skipped = len(bars) - 1        # every row but the trailing one is a reachable pair
    assert core["gap_skipped_pairs"] == 2
    expected_pct = round(2 / kept_plus_skipped * 100.0, 4)
    assert core["gap_skipped_pct"] == expected_pct, (
        f"denominator must be pairs reached ({kept_plus_skipped}), not total bars"
    )


def test_trailing_bar_is_not_counted_as_a_gap_skip():
    """The last bar has no successor at all. That is 'no pair', not 'a pair
    suppressed for spanning a gap' -- counting it would inflate the reported
    contamination of every clean run by one."""
    n = 20
    bars = _bars([((-1) ** i) * 5.0 for i in range(n)],
                 [100.0 + i for i in range(n)], _hourly(n))

    core = build_core({}, [], bars, candle_interval_seconds=3600)

    assert core["gap_skipped_pairs"] == 0, "a contiguous series has zero gap skips"
    assert core["gap_skipped_pct"] == 0.0


# ---------------------------------------------------------------------------
# 5. The real cache, real gaps
# ---------------------------------------------------------------------------

from _cache_guard import cache_skip_reason  # noqa: E402

_REAL_START, _REAL_END = "2018-01-01", "2018-03-01"
_CACHE_SKIP = cache_skip_reason(
    TRADING_BOT_ROOT / "local_data", ("BTCUSDT_1h.csv",), _REAL_START, _REAL_END
)


@pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "cache usable")
def test_real_btcusdt_gaps_are_detected_and_counted():
    """The two real holes in BTCUSDT_1h.csv's 2018-01→03 window (2018-01-04
    03:00→05:00, and the 34h 2018-02-08 00:00→2018-02-09 10:00) must be found
    and counted -- proving this works on the actual cache, not only fixtures."""
    raw = pd.read_csv(TRADING_BOT_ROOT / "local_data" / "BTCUSDT_1h.csv")
    raw["timestamp"] = pd.to_datetime(raw["timestamp"])
    w = raw[(raw["timestamp"] >= _REAL_START) & (raw["timestamp"] < _REAL_END)].copy()
    # Deterministic synthetic forecast: this test is about the gap filter, not
    # about any particular strategy's signal.
    w["forecast"] = [((-1) ** i) * 5.0 for i in range(len(w))]

    core = build_core({}, [], w[["timestamp", "forecast", "close"]],
                      candle_interval_seconds=3600)

    assert core["gap_skipped_pairs"] == 2, (
        "the 2018-01-04 and 2018-02-08 holes in the real cache must both be "
        f"suppressed; got {core['gap_skipped_pairs']}"
    )
    assert core["gap_skipped_pct"] > 0
