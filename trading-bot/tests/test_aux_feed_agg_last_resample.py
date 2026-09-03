"""
CUL-250 follow-up: aux feeds registered with agg='last' (every real feed in
this codebase -- core/backtester.py hardcodes it) must pick up the FRESHEST
reading within a candle's own span once fetch_interval_seconds (CUL-250)
lets OHLCV be fetched finer than the candle -- not silently anchor to
whatever value was current when the candle OPENED.

Before this fix, data_manager.py's _premerge_aux_feeds() only resampled
feed data to interval_seconds buckets for agg != 'last'; agg='last' feeds
went straight into merge_asof against the raw (possibly finer-than-candle)
price rows. That was invisible for every existing caller because OHLCV was
always fetched at candle resolution, so at most one raw aux reading could
ever land inside a candle -- "anchored to candle open" and "anchored to
candle close" were the same instant. fetch_interval_seconds breaks that
coincidence: now multiple raw aux readings can land inside one candle span,
and the fix makes 'last' resample exactly like every other agg function
already did, picking the freshest reading before the candle closes.
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


class _StubFetcher:
    """Serves a fixed aux DataFrame; no network, no caching."""

    def __init__(self, df: pd.DataFrame, column: str):
        self._df = df
        self._column = column
        self.exchange_id = "binance"

    def get_data(self, symbol=None):
        return self._df

    def cache_key(self, symbol):
        return "stub"


def _hourly_price(n: int) -> pd.DataFrame:
    ts = pd.date_range("2024-01-01", periods=n, freq="1h")
    return pd.DataFrame({
        "timestamp": ts,
        "open": [100.0] * n, "high": [100.0] * n, "low": [100.0] * n,
        "close": [100.0] * n, "volume": [1.0] * n,
    })


def test_agg_last_feed_picks_the_freshest_reading_before_candle_close():
    """4h candles built from 1h OHLCV (fetch_interval_seconds=3600); an
    agg='last' aux feed updates every hour. The candle covering hours 0-3
    must carry the value from hour 3 (freshest known before the candle
    closes), not the value from hour 0 (stale, candle-open anchor)."""
    price = _hourly_price(8)
    aux = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=8, freq="1h"),
        "aux_val": [10, 20, 30, 40, 50, 60, 70, 80],
    })

    dm = DataManager(
        symbols=[SYMBOL], interval_seconds=4 * 3600, mode="backtest",
        fetch_interval_seconds=3600,
    )
    dm.register_feed(name="aux_val", fetcher=_StubFetcher(aux, "aux_val"),
                      window_seconds=0, agg="last")
    dm.historical_data[SYMBOL] = price
    dm.initialize()

    enriched = dm._enrichment_data[SYMBOL]
    candle_1 = enriched[enriched["timestamp"] == pd.Timestamp("2024-01-01 00:00:00")]
    candle_2 = enriched[enriched["timestamp"] == pd.Timestamp("2024-01-01 04:00:00")]

    assert candle_1.iloc[0]["aux_val"] == 40, (
        "candle 1 (hours 0-3) must carry the freshest reading (hour 3's "
        "value, 40), not the candle-open value (hour 0's, 10)"
    )
    assert candle_2.iloc[0]["aux_val"] == 80


def test_agg_last_feed_forward_fills_when_no_reading_falls_in_the_candle():
    """No new aux reading inside a candle's span -> carry the previous
    bucket's value forward (still via the causality guard's own merge_asof,
    unchanged) -- the resample step must not turn missing readings into
    NaN gaps."""
    price = _hourly_price(8)
    aux = pd.DataFrame({
        # Only one reading, in the middle of candle 1's span.
        "timestamp": pd.to_datetime(["2024-01-01 01:00:00"]),
        "aux_val": [99],
    })

    dm = DataManager(
        symbols=[SYMBOL], interval_seconds=4 * 3600, mode="backtest",
        fetch_interval_seconds=3600,
    )
    dm.register_feed(name="aux_val", fetcher=_StubFetcher(aux, "aux_val"),
                      window_seconds=0, agg="last")
    dm.historical_data[SYMBOL] = price
    dm.initialize()

    enriched = dm._enrichment_data[SYMBOL]
    candle_1 = enriched[enriched["timestamp"] == pd.Timestamp("2024-01-01 00:00:00")]
    candle_2 = enriched[enriched["timestamp"] == pd.Timestamp("2024-01-01 04:00:00")]

    assert candle_1.iloc[0]["aux_val"] == 99
    assert candle_2.iloc[0]["aux_val"] == 99, "candle 2 has no new reading -- must carry candle 1's forward"


def test_agg_last_feed_is_byte_identical_when_fetch_interval_matches_interval():
    """The universal current-production case (fetch_interval_seconds unset,
    one raw price row per candle): resampling to interval_seconds buckets
    with agg='last' must be a no-op, reproducing the pre-fix values exactly.
    This is the bit-identity guarantee -- every existing run must be
    unaffected by this change."""
    n = 4
    price = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="4h"),
        "open": [100.0] * n, "high": [100.0] * n, "low": [100.0] * n,
        "close": [100.0] * n, "volume": [1.0] * n,
    })
    aux = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="4h"),
        "aux_val": [11, 22, 33, 44],
    })

    dm = DataManager(symbols=[SYMBOL], interval_seconds=4 * 3600, mode="backtest")
    dm.register_feed(name="aux_val", fetcher=_StubFetcher(aux, "aux_val"),
                      window_seconds=0, agg="last")
    dm.historical_data[SYMBOL] = price
    dm.initialize()

    enriched = dm._enrichment_data[SYMBOL]
    assert list(enriched["aux_val"]) == [11, 22, 33, 44]
    assert list(enriched["timestamp"]) == list(price["timestamp"])
