"""
CUL-250: DataManager.fetch_interval_seconds -- fetch OHLCV at a finer
resolution than the candle target, let CandleBuilder aggregate it up during
replay.

This capability existed in a version of this codebase that predates the
repo's own git history (confirmed from historical source Jeremy supplied
2026-09-03: main.py/data_manager.py/backtester.py of that era fed
HistoricalDataFetcher from a SEPARATE `check_interval_seconds`-derived value
while HistoricalDataManager aggregated to `interval`), then was lost in a
one-line regression during a later consolidation refactor (the fetch call
site changed to use the SAME interval as the candle target). This restores
the capability as a new, explicit, off-by-default parameter rather than
reverting the consolidation -- CandleBuilder's own aggregation math is
unchanged and already proven by test_candle_builder_aggregation.py; this
file covers the layer above it (DataManager wiring + validation).
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import DataManager  # noqa: E402

SYMBOL = "BTCUSDT"


# ---------------------------------------------------------------------------
# Constructor validation
# ---------------------------------------------------------------------------

def test_unset_fetch_interval_defaults_to_interval_seconds():
    dm = DataManager(symbols=[SYMBOL], interval_seconds=14400, mode="backtest")
    assert dm.fetch_interval_seconds == 14400


def test_explicit_fetch_interval_equal_to_interval_is_accepted():
    dm = DataManager(
        symbols=[SYMBOL], interval_seconds=3600, mode="backtest", fetch_interval_seconds=3600,
    )
    assert dm.fetch_interval_seconds == 3600


def test_fetch_interval_coarser_than_interval_raises():
    with pytest.raises(ValueError, match="must be <="):
        DataManager(
            symbols=[SYMBOL], interval_seconds=3600, mode="backtest", fetch_interval_seconds=14400,
        )


def test_fetch_interval_that_does_not_evenly_divide_interval_raises():
    with pytest.raises(ValueError, match="evenly divisible"):
        DataManager(
            symbols=[SYMBOL], interval_seconds=14400, mode="backtest", fetch_interval_seconds=1000,
        )


def test_fetch_interval_evenly_dividing_interval_is_accepted():
    dm = DataManager(
        symbols=[SYMBOL], interval_seconds=14400, mode="backtest", fetch_interval_seconds=3600,
    )
    assert dm.fetch_interval_seconds == 3600
    assert dm.interval_seconds == 14400


# ---------------------------------------------------------------------------
# fetch_historical_data() wiring -- no network, HistoricalDataFetcher stubbed
# ---------------------------------------------------------------------------

class _RecordingFetcher:
    """Captures the interval it was asked to fetch at; serves nothing (the
    wiring test only needs to see what DataManager constructs it with)."""

    captured_candle_interval_seconds = None

    def __init__(self, start_date, end_date, symbols, candle_interval_seconds,
                 exchange="binance", localStorage=True, data_dir=None):
        type(self).captured_candle_interval_seconds = candle_interval_seconds
        self.tolerate_fill_failure = False

    def get_data(self):
        return {}

    def validate_data_continuity(self, symbol):
        return True, []


def test_fetch_historical_data_uses_fetch_interval_not_interval_seconds(monkeypatch):
    import data.data_manager as dm_mod

    monkeypatch.setattr(dm_mod, "HistoricalDataFetcher", _RecordingFetcher)
    dm = DataManager(
        symbols=[SYMBOL], interval_seconds=14400, mode="backtest", fetch_interval_seconds=3600,
    )
    dm.fetch_historical_data(SYMBOL, "2024-01-01", "2024-01-02")
    assert _RecordingFetcher.captured_candle_interval_seconds == 3600


def test_fetch_historical_data_without_fetch_interval_matches_prior_behaviour(monkeypatch):
    """Byte-identity: every existing caller (fetch_interval_seconds unset)
    must still ask the fetcher for interval_seconds, exactly as before this
    parameter existed."""
    import data.data_manager as dm_mod

    monkeypatch.setattr(dm_mod, "HistoricalDataFetcher", _RecordingFetcher)
    dm = DataManager(symbols=[SYMBOL], interval_seconds=14400, mode="backtest")
    dm.fetch_historical_data(SYMBOL, "2024-01-01", "2024-01-02")
    assert _RecordingFetcher.captured_candle_interval_seconds == 14400


# ---------------------------------------------------------------------------
# End-to-end replay: finer historical_data rows aggregated to the coarser
# candle target through the real process_next_tick()/advance() loop -- not
# just a direct CandleBuilder.add_row() call, proving DataManager's own
# plumbing (cursor, has_more_data) is agnostic to the row/candle ratio.
# ---------------------------------------------------------------------------

def _hourly_frame(n: int, start: str = "2020-01-01 00:00:00") -> pd.DataFrame:
    ts = pd.date_range(start, periods=n, freq="1h")
    return pd.DataFrame({
        "timestamp": ts,
        "open":   [100.0 + i for i in range(n)],
        "high":   [100.5 + i for i in range(n)],
        "low":    [99.5 + i for i in range(n)],
        "close":  [100.2 + i for i in range(n)],
        "volume": [10.0 * (i + 1) for i in range(n)],
    })


def _replay_all(dm: DataManager, symbol: str, n_rows: int):
    cap = max(3 * n_rows, 3)
    feeds = 0
    while dm.has_more_data(symbol):
        feeds += 1
        assert feeds <= cap, "has_more_data never went False -- cursor stuck"
        dm.process_next_tick(symbol)
        dm.advance(symbol)
    # Flush the final partial-or-complete candle, matching main.py's own
    # end-of-backtest handling (BacktestEngine reads get_final_candle()).
    dm.flush_final_candle(symbol)


def test_replay_aggregates_hourly_rows_into_4h_candles_matching_a_resample_oracle():
    """16 hourly rows -> 4 four-hour candles. Cross-checked against pandas'
    own resample as an independent oracle (same convention as
    test_candle_builder_aggregation.py's test_matches_a_straight_ohlc_resample)."""
    n_rows = 16
    frame = _hourly_frame(n_rows)

    dm = DataManager(
        symbols=[SYMBOL], interval_seconds=4 * 3600, mode="backtest", fetch_interval_seconds=3600,
    )
    dm.historical_data[SYMBOL] = frame
    dm.initialize()

    _replay_all(dm, SYMBOL, n_rows)

    got = dm.candle_builder.get_candle_history(SYMBOL, count=100)
    assert len(got) == 4, f"expected 4 four-hour candles from 16 hourly rows, got {len(got)}"

    oracle = (
        frame.set_index("timestamp")
        .resample("14400s", closed="left", label="left")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
        .reset_index()
    )
    for col in ("open", "high", "low", "close", "volume"):
        assert list(got[col]) == list(oracle[col]), f"{col} mismatch vs resample oracle"


def test_replay_with_unset_fetch_interval_is_unchanged_one_row_per_candle():
    """Byte-identity check the other direction: fetch_interval_seconds unset
    with hourly historical_data AND an hourly interval_seconds must still
    produce one candle per row, exactly as every existing baseline does."""
    n_rows = 5
    frame = _hourly_frame(n_rows)

    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    dm.historical_data[SYMBOL] = frame
    dm.initialize()

    _replay_all(dm, SYMBOL, n_rows)

    got = dm.candle_builder.get_candle_history(SYMBOL, count=100)
    assert len(got) == n_rows
    for col in ("open", "high", "low", "close", "volume"):
        assert list(got[col]) == list(frame[col])
