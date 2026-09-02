"""
CUL-43 — `close_time` dtype must survive a load+merge.

`BaseFetcher._load_local` re-parses only `timestamp`, so `close_time` came back
from `read_csv` as object (string). Concatenating that against a CcxtFetcher
chunk's real datetime64 `close_time` in `_merge_and_store` silently degraded the
merged column to object, and `to_csv` then wrote `…:59.999000` where a fresh
write produces `…:59.999`. The fix re-parses `close_time` in `_load_local` once,
for every caller.

No network: these tests only exercise `_load_local` / `_merge_and_store` against
CSVs under tmp_path — no fetcher remote method is ever reached.
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.ccxt_fetcher import CcxtFetcher  # noqa: E402

H = 3600
T0 = pd.Timestamp("2020-01-01 00:00:00")
SYMBOL = "BTCUSDT"


def _ohlcv(start, periods: int) -> pd.DataFrame:
    """A Binance-schema frame with a real datetime64 `close_time` column."""
    ts = pd.date_range(start=start, periods=periods, freq="h")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": 1.0,
            "high": 1.0,
            "low": 1.0,
            "close": 1.0,
            "volume": 1.0,
            "close_time": ts + pd.Timedelta(H * 1000 - 1, unit="ms"),
            "quote_asset_volume": 1.0,
            "number_of_trades": 1,
            "taker_buy_base_asset_volume": float("nan"),
            "taker_buy_quote_asset_volume": float("nan"),
            "ignore": 0,
        }
    )


def _fetcher(tmp_path) -> CcxtFetcher:
    return CcxtFetcher(
        start_date=T0,
        end_date=T0 + pd.Timedelta(8, unit="h"),
        symbols=[SYMBOL],
        candle_interval_seconds=H,
        exchange="binance",
        localStorage=False,
        data_dir=str(tmp_path),
    )


def test_merge_keeps_close_time_datetime64(tmp_path):
    """
    An existing cache (close_time round-tripped as strings via read_csv) merged
    with a fresh datetime64 top-up must keep the merged close_time as
    datetime64 — the degradation to object is what the fix prevents.

    Mutation: revert the _load_local close_time re-parse and the loaded
    `existing` carries object strings; the concat degrades to object and this
    assertion goes red.
    """
    fetcher = _fetcher(tmp_path)
    path = Path(fetcher._csv_path(SYMBOL))
    _ohlcv(T0, 3).to_csv(path, index=False)  # hours 0,1,2 -> close_time as string on disk

    existing = fetcher._load_local(SYMBOL)
    chunk = _ohlcv(T0 + pd.Timedelta(3, unit="h"), 3)  # hours 3,4,5 — contiguous top-up

    fetcher._merge_and_store(SYMBOL, [chunk, existing], save=False, existing=existing)
    combined = fetcher.data_cache[SYMBOL]

    assert combined["close_time"].dtype == "datetime64[ns]", combined["close_time"].dtype
    assert len(combined) == 6


def test_clean_cache_reload_rewrite_is_byte_identical(tmp_path):
    """
    Idempotency guardrail (rule-4 support): reloading and rewriting a cache that
    already stores clean `…:59.999` close_time bytes is byte-identical — the
    re-parse does not reformat an already-clean file.
    """
    fetcher = _fetcher(tmp_path)
    path = Path(fetcher._csv_path(SYMBOL))
    _ohlcv(T0, 5).to_csv(path, index=False)
    first = path.read_bytes()

    reloaded = fetcher._load_local(SYMBOL)
    reloaded.to_csv(path, index=False)

    assert path.read_bytes() == first, "reload+rewrite of a clean cache changed its bytes"
