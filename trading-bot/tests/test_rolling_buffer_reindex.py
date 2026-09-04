"""
CUL-273 Task A part 4: RollingBuffer.get_df() timestamp reindex -- the actual
time-axis fix the count-indexed audit called for. Before this, RollingBuffer
was purely count-indexed (deque(maxlen=N), no timestamp reindex at all), so a
skipped bar let .rolling()/.ewm() silently compute over a wider real time span
using the same row-count -- the original defect CUL-271's detection/reset work
did not touch.

NOT wired into the real live/backtest path yet (core/launcher.py's
AdvancedStrategy(...) call sites still construct it with no interval/policy) --
this tests the mechanism in isolation, which is what a future wiring change
would rely on.
"""
import math

import numpy as np
import pandas as pd
import pytest

from strategies.strategy_base import RollingBuffer


def _push(buf, timestamps, closes, extra=None):
    for i, (ts, c) in enumerate(zip(timestamps, closes)):
        row = {"timestamp": ts, "open": c, "high": c, "low": c, "close": c, "volume": 1.0}
        if extra:
            row.update(extra[i])
        buf.add_data(row)


def test_default_construction_is_byte_identical_no_reindex_attempted():
    """Both params absent (every existing call site) -- get_df() must not even
    look at timestamp spacing."""
    buf = RollingBuffer(500)
    ts = list(pd.date_range("2024-01-01", periods=5, freq="h"))
    ts[3] = ts[3] + pd.Timedelta(hours=10)   # a real, large gap
    _push(buf, ts, [100.0] * 5)
    df = buf.get_df()
    assert len(df) == 5, "no rows may be inserted when the mechanism is off"
    assert list(df["timestamp"]) == ts, "existing bars must be untouched, in original order"


def test_one_param_alone_is_also_inert():
    """Requires BOTH candle_interval_seconds and ignore_max_bars -- a step
    with no tolerance, or a tolerance with no step, cannot classify a gap, so
    neither alone may activate reindexing."""
    buf_a = RollingBuffer(500, candle_interval_seconds=3600)
    buf_b = RollingBuffer(500, ignore_max_bars=2)
    ts = list(pd.date_range("2024-01-01", periods=5, freq="h"))
    ts[3] = ts[3] + pd.Timedelta(hours=10)
    for buf in (buf_a, buf_b):
        _push(buf, ts, [100.0] * 5)
        assert len(buf.get_df()) == 5


def test_small_gap_forward_fills_close_and_zeros_volume():
    """A gap smaller than ignore_max_bars gets synthetic flat-close,
    zero-volume rows inserted -- CUL-271's already-agreed 'small gaps don't
    matter' policy, applied here so a short hole doesn't put an artificial gap
    in an otherwise-continuous rolling window."""
    buf = RollingBuffer(500, candle_interval_seconds=3600, ignore_max_bars=3)
    ts = list(pd.date_range("2024-01-01 00:00", periods=3, freq="h"))
    ts_after = ts[-1] + pd.Timedelta(hours=3)   # 2 bars missing (01:00, 02:00), < ignore_max_bars=3
    _push(buf, ts + [ts_after], [100.0, 105.0, 110.0, 120.0])
    df = buf.get_df()
    assert len(df) == 6, "2 missing bars must be inserted -> 4 real + 2 synthetic = 6"
    inserted = df.iloc[3:5]
    assert (inserted["close"] == 110.0).all(), "forward-filled close must carry the last real close (flat, no invented trend)"
    assert (inserted["volume"] == 0.0).all()
    assert not inserted["close"].isna().any()


def test_large_gap_inserts_nan_not_a_fabricated_value():
    """A gap at or above ignore_max_bars must be NaN on every OHLCV column --
    the row a .rolling()/.ewm() window must see as genuinely missing, not
    silently forward-filled."""
    buf = RollingBuffer(500, candle_interval_seconds=3600, ignore_max_bars=2)
    ts = list(pd.date_range("2024-01-01 00:00", periods=3, freq="h"))
    ts_after = ts[-1] + pd.Timedelta(hours=5)   # 4 bars missing, >= ignore_max_bars=2
    _push(buf, ts + [ts_after], [100.0, 105.0, 110.0, 120.0])
    df = buf.get_df()
    assert len(df) == 8, "4 real bars + 4 missing inserted = 8"
    gap_rows = df[df["timestamp"].isin(
        [ts[-1] + pd.Timedelta(hours=h) for h in (1, 2, 3, 4)]
    )]
    assert len(gap_rows) == 4
    assert gap_rows["close"].isna().all(), "a large gap must be NaN, never a fabricated numeric value"
    assert gap_rows["volume"].isna().all()


def test_rolling_window_correctly_shrinks_across_an_unfilled_large_gap():
    """The actual point of this fix: a rolling mean computed AFTER reindexing
    must have fewer valid observations across a real hole, via min_periods --
    not silently average over row-count as if time were continuous."""
    buf = RollingBuffer(500, candle_interval_seconds=3600, ignore_max_bars=2)
    ts = list(pd.date_range("2024-01-01 00:00", periods=3, freq="h"))
    ts_after = ts[-1] + pd.Timedelta(hours=10)  # 9 bars missing, a real large gap
    post_gap_ts = list(pd.date_range(ts_after, periods=8, freq="h"))
    _push(buf, ts + post_gap_ts, [100.0] * (3 + 8))
    df = buf.get_df()
    window = 5
    rolling_mean = df["close"].rolling(window, min_periods=window).mean()

    gap_row_positions = [df.index[df["timestamp"] == ts[-1] + pd.Timedelta(hours=h)][0] for h in range(1, 10)]
    assert (rolling_mean.iloc[gap_row_positions].isna()).all(), (
        "a rolling mean spanning gap rows must be NaN -- if it isn't, the gap "
        "rows are being silently treated as real, present observations"
    )

    first_valid = rolling_mean.first_valid_index()
    assert first_valid is not None, "the window must eventually become valid once enough real post-gap bars accumulate"
    last_gap_row_position = gap_row_positions[-1]
    assert first_valid > last_gap_row_position, (
        "the window may only become valid AFTER it has fully cleared the gap "
        "rows (min_periods real observations, none of them NaN placeholders)"
    )
    assert first_valid - last_gap_row_position >= window, (
        "must require a full `window` of genuinely real post-gap bars, not "
        "just any bar past the gap"
    )


def test_no_gap_present_matches_unreindexed_output():
    """When the real data has no gap at all, reindexing must be a no-op --
    proves the mechanism doesn't distort clean data."""
    buf_on = RollingBuffer(500, candle_interval_seconds=3600, ignore_max_bars=2)
    buf_off = RollingBuffer(500)
    ts = list(pd.date_range("2024-01-01", periods=10, freq="h"))
    closes = list(np.linspace(100.0, 110.0, 10))
    _push(buf_on, ts, closes)
    _push(buf_off, ts, closes)
    df_on = buf_on.get_df()
    df_off = buf_off.get_df()
    assert len(df_on) == len(df_off) == 10
    assert list(df_on["close"]) == list(df_off["close"])
