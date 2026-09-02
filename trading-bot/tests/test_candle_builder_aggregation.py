"""
CandleBuilder must keep intra-bar extremes when AGGREGATING several rows
into one candle.

Bug found 2026-08-28 while wiring the strategy-research prescreen onto
CandleBuilder (so that a prescreen bar and a backtest bar are the same bar by
construction). `_ingest`'s update branch called

    self._update_candle(current, price, volume)

dropping the `high` and `low` it had just received from `add_row`, even though
`_update_candle` declares both parameters. Its fallback is
`high if high is not None else price`, so every row after the FIRST in a
candle contributed only its CLOSE. An aggregated candle's high was therefore

    max(first_row_high, close of rows 2..n)

instead of max of all rows' highs -- systematically understating highs and
overstating lows. Measured on a synthetic 4h-from-1h bar: high 150 instead of
180, low 90 instead of 60.

WHY IT SURVIVED: it only bites when a candle spans MULTIPLE rows. A 1h run over
1h data opens a new candle on every row and so goes through `_open_candle`,
which does honour high/low. Only derived timeframes -- the documented "a 4h
backtest runs off BTCUSDT_1h.csv" path -- aggregate, and no 4h run had ever
been launched. The whole fast suite (383 tests) passed both before and after
the fix.

NOTE (2026-09-03, CUL-250): this file tests CandleBuilder's own aggregation
math in isolation (feeding it finer rows directly via add_row), and that math
is correct. It does NOT prove the "documented" path above is real end to end
-- checked separately and it is not. Nothing in the real fetch/backtest
pipeline ever decides to feed CandleBuilder rows finer than its own configured
interval; CcxtFetcher fetches and cache-keys at the exact requested timeframe
with no finer-cache fallback. Reproduced live re-running run_060 (4h) after
the CUL-230 fetch fix shipped: it still crashed, because the 4h cache was
incomplete and nothing tried the fully-available 1h cache instead. See
CUL-250 for the full trace and proposed fix.
"""
import datetime

import pandas as pd
import pytest

from data.data_manager import CandleBuilder


def _rows(specs):
    df = pd.DataFrame(specs, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def _build(rows, interval_seconds, symbol="X"):
    cb = CandleBuilder(interval_seconds=interval_seconds)
    for _, row in rows.iterrows():
        cb.add_row(row, symbol)
    cb.flush_final_candle(symbol)
    return cb.get_candle_history(symbol, count=len(rows))


FOUR_1H_ROWS = _rows([
    # extremes deliberately invisible in any close price
    ("2020-01-01 00:00:00", 100, 150, 90, 110, 1),
    ("2020-01-01 01:00:00", 110, 160, 80, 120, 1),
    ("2020-01-01 02:00:00", 120, 170, 70, 130, 1),
    ("2020-01-01 03:00:00", 130, 180, 60, 140, 1),
])


def test_aggregated_candle_keeps_the_true_high_and_low():
    """The regression itself. Before the fix: high=150, low=90."""
    out = _build(FOUR_1H_ROWS, 4 * 3600)
    assert len(out) == 1
    bar = out.iloc[0]
    assert bar["high"] == 180, "high must be the max across ALL rows, not just the first"
    assert bar["low"] == 60, "low must be the min across ALL rows, not just the first"


def test_aggregated_candle_keeps_open_close_and_volume():
    """The fields that were already correct must stay correct."""
    bar = _build(FOUR_1H_ROWS, 4 * 3600).iloc[0]
    assert bar["open"] == 100      # first row's open
    assert bar["close"] == 140     # last row's close
    assert bar["volume"] == 4      # sum
    assert bar["timestamp"] == datetime.datetime(2020, 1, 1, 0, 0)


def test_one_row_per_candle_is_unchanged():
    """Bit-identity for every existing baseline: when the candle interval
    matches the data resolution each row opens its own candle via
    _open_candle, which always honoured high/low. This path must not move."""
    out = _build(FOUR_1H_ROWS, 3600)
    assert len(out) == 4
    for i, expected in enumerate([(150, 90), (160, 80), (170, 70), (180, 60)]):
        assert (out.iloc[i]["high"], out.iloc[i]["low"]) == expected


def test_matches_a_straight_ohlc_resample():
    """Independent oracle: pandas resample with the engine's own convention
    (closed/label='left'), as used at core/backtester.py:296."""
    ref = (FOUR_1H_ROWS.set_index("timestamp")
           .resample("14400s", closed="left", label="left")
           .agg({"open": "first", "high": "max", "low": "min",
                 "close": "last", "volume": "sum"})
           .reset_index())
    got = _build(FOUR_1H_ROWS, 4 * 3600)
    for col in ["open", "high", "low", "close", "volume"]:
        assert float(got.iloc[0][col]) == float(ref.iloc[0][col]), col


@pytest.mark.parametrize("interval_hours,expected_bars", [(2, 2), (4, 1)])
def test_holds_across_aggregation_ratios(interval_hours, expected_bars):
    out = _build(FOUR_1H_ROWS, interval_hours * 3600)
    assert len(out) == expected_bars
    assert out["high"].max() == 180
    assert out["low"].min() == 60


def test_extremes_survive_when_the_open_row_is_the_calmest():
    """Directional check: the first row having the NARROWEST range is exactly
    the case the old code got wrong, because it seeded high/low from that row
    and then only ever saw later closes."""
    rows = _rows([
        ("2020-01-01 00:00:00", 100, 101, 99, 100, 1),   # calm opener
        ("2020-01-01 01:00:00", 100, 500, 10, 100, 1),   # the real extremes
        ("2020-01-01 02:00:00", 100, 102, 98, 100, 1),
        ("2020-01-01 03:00:00", 100, 103, 97, 100, 1),
    ])
    bar = _build(rows, 4 * 3600).iloc[0]
    assert bar["high"] == 500
    assert bar["low"] == 10
