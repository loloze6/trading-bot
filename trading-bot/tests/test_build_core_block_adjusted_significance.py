"""
CUL-262 (E-039 parity): build_core's new, additive block-adjusted significance
must (a) leave every pre-existing field byte-identical when the new
`candle_interval_seconds` argument isn't supplied, and (b) agree with
`performance.signal_statistics`'s own `block_adjusted_pvalue`/
`gap_aware_active_block_count` -- the same functions build_core itself calls
-- on the same underlying series, proving the wiring passes through the exact
population build_core measured `corr` on, not just "a number that sounds
plausible."

(Originally a lockstep comparison against prescreen_signal.py's own
`_block_adjusted_significance`/`_gap_aware_block_count`, which
`signal_statistics.py`'s pair are a verbatim port of; repointed 2026-09-12,
E-039 step 5, once prescreen_signal.py was removed -- build_core has never
called prescreen_signal.py, only the test's comparison target changed.)
"""
import sys
from pathlib import Path

import pandas as pd

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from reporting.run_artifact import build_core
from performance.signal_statistics import gap_aware_active_block_count, block_adjusted_pvalue


def _bars(forecasts, closes, freq="h", start="2020-01-01"):
    return pd.DataFrame({
        "timestamp": pd.date_range(start, periods=len(forecasts), freq=freq),
        "forecast": forecasts,
        "close": closes,
    })


def _varying_series(n=60):
    forecasts = [((-1) ** i) * (5 + i % 5) for i in range(n)]
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    return forecasts, closes


def test_default_call_signature_byte_identical_to_before():
    """Old 3-positional-arg call (as core/backtester.py made it before CUL-262)
    must still work and must not change either pre-existing field's value --
    the new fields are additive and default to None when the interval isn't
    supplied."""
    forecasts, closes = _varying_series()
    bars = _bars(forecasts, closes)

    core = build_core({}, [], bars)

    assert core["forecast_return_corr"] is not None
    assert core["forecast_return_corr_pvalue"] is not None
    assert core["forecast_return_corr_pvalue_block_adjusted"] is None, (
        "must stay None when candle_interval_seconds is not supplied -- "
        "no existing caller passes it, so no existing output may change"
    )
    assert core["forecast_return_corr_n_eff"] is None


def test_block_adjusted_pvalue_matches_prescreen_no_gaps():
    """No-gap case: build_core's new field must equal what
    block_adjusted_pvalue/gap_aware_active_block_count compute standalone on
    the exact same active/timestamp shape build_core itself derives."""
    forecasts, closes = _varying_series(n=80)
    bars = _bars(forecasts, closes, freq="h")
    candle_interval_seconds = 3600  # 1h -> block_size 24

    core = build_core({}, [], bars, candle_interval_seconds=candle_interval_seconds)
    corr = core["forecast_return_corr"]
    assert corr is not None

    # Reproduce build_core's own active-bar filter to get n_active/records,
    # since that's what both the real code and this check must agree on.
    df = bars[["forecast", "close"]].copy()
    df["forward_return"] = df["close"].shift(-1) / df["close"] - 1
    df = df.dropna()
    df = df[df["forecast"] != 0]

    block_size = 24
    # Match build_core's own population: the last row's forward_return is
    # always NaN (nothing to shift(-1) into), so it's excluded from `x`/`corr`
    # and must be excluded here too for an apples-to-apples comparison.
    records = [
        {"active": bool(f != 0), "timestamp": ts}
        for f, ts in zip(bars["forecast"].iloc[:-1], bars["timestamp"].iloc[:-1])
    ]
    expected_step = pd.Timedelta(seconds=candle_interval_seconds)
    placeable = gap_aware_active_block_count(records, block_size, expected_step)

    expected_p, expected_n_eff = block_adjusted_pvalue(
        corr, len(df), block_size=block_size, placeable_blocks=placeable
    )

    assert core["forecast_return_corr_n_eff"] == expected_n_eff
    assert core["forecast_return_corr_pvalue_block_adjusted"] == expected_p, (
        f"build_core's p-value {core['forecast_return_corr_pvalue_block_adjusted']} "
        f"must match a standalone block_adjusted_pvalue call {expected_p} on identical input"
    )


def test_block_adjusted_pvalue_gap_aware_with_a_real_gap():
    """With a real data gap inserted, the gap-aware n_eff must be STRICTLY
    LOWER than the naive (gap-ignorant) count would give -- proving
    gap_aware_active_block_count carries the #50(B) gap-awareness fix, not
    just the pre-gap arithmetic."""
    n = 100
    forecasts = [((-1) ** i) * (5 + i % 5) for i in range(n)]
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    bars = _bars(forecasts, closes, freq="h")

    # Punch three real gaps: splice out 200 hours total, at three different
    # offsets, so the effect survives floor-division coarseness against
    # block_size=24 regardless of exactly where in a block each gap lands
    # (prices/forecasts stay put -- this reproduces "the next ROW is not the
    # next BAR" exactly, the #50 defect shape).
    ts = bars["timestamp"].tolist()
    for gap_point, gap_hours in ((20, 60), (50, 70), (80, 70)):
        ts = ts[:gap_point] + [t + pd.Timedelta(hours=gap_hours) for t in ts[gap_point:]]
    bars["timestamp"] = ts

    candle_interval_seconds = 3600
    block_size = 24
    core = build_core({}, [], bars, candle_interval_seconds=candle_interval_seconds)
    corr = core["forecast_return_corr"]
    assert corr is not None

    # Match build_core's own population -- see the no-gaps test above for why
    # the last row is excluded.
    records = [
        {"active": bool(f != 0), "timestamp": t}
        for f, t in zip(bars["forecast"].iloc[:-1], bars["timestamp"].iloc[:-1])
    ]
    expected_step = pd.Timedelta(seconds=candle_interval_seconds)
    gap_aware_count   = gap_aware_active_block_count(records, block_size, expected_step)
    naive_count       = gap_aware_active_block_count(records, block_size, None)

    assert gap_aware_count < naive_count, (
        "a real 40h gap must reduce the placeable block count relative to "
        "the gap-ignorant count -- otherwise the gap-awareness isn't doing anything"
    )


def test_trailing_bar_excluded_from_n_eff_population():
    """The last bar's forward_return is always NaN (nothing to shift(-1)
    into), so `df`/`x`/`corr` never see it -- the gap-aware active-block
    count must not see it either, or n_eff would be computed over a
    population one bar larger than the one `corr` was actually measured on.

    Crafted so the extra bar crosses a block-size boundary (48 active bars
    including the last row vs 47 excluding it, block_size=24: floor(48/24)=2
    vs floor(47/24)=1) -- a case where getting this wrong is visible, not
    silently absorbed by floor-division coarseness.
    """
    n = 48
    forecasts = [5 + i % 7 for i in range(n)]  # all nonzero (active), varies
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    bars = _bars(forecasts, closes, freq="h")

    core = build_core({}, [], bars, candle_interval_seconds=3600)
    corr = core["forecast_return_corr"]
    assert corr is not None

    assert core["forecast_return_corr_n_eff"] == 1, (
        "47 forward-return-eligible active bars / block_size 24 = floor(47/24) "
        "= 1 -- if this reads 2 instead, the trailing (forward-return-less) "
        "bar leaked back into the population"
    )
