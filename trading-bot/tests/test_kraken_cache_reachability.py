"""
Phase 2 Track A — Kraken cache reachability.

Two groups:
  (a) BaseFetcher._load_local's tz-naive convention guard: must raise when a
      cached CSV's 'timestamp' column parses as tz-aware (an offset-carrying
      writer would otherwise silently produce a dtype every naive comparison
      in the codebase chokes on downstream, far from the actual cause).
  (b) End-to-end reachability of an ingested Kraken pair through
      DataManager.fetch_historical_data()'s new `exchange` parameter — the
      parameter is only meaningful if a caller can actually walk the public
      path down to kraken_BTCUSD_1h.csv and get real rows back.

Read-only-rule note (ledger G1 pipeline defect): DataManager.fetch_historical_
data() → get_data() → _load_all() gap-fills, and when the requested window has
an internal gap it attempts a remote fetch and re-saves the cache even on a
pure read. Under the settled convention the store symbol BTCUSD normalizes to
the VALID ccxt symbol BTC/USD, so such a fetch would now hit the live network
and mutate the archive cache. This test therefore reads a deliberately
gap-free window (BTC 2022 — audited 0 missing bars), which yields zero missing
periods, hence zero remote fetch and zero re-save. Full-history reachability
(96,381 rows) is verified by the ingestion script's own reload round-trip.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.ccxt_fetcher import CcxtFetcher   # noqa: E402
from data.data_manager import DataManager            # noqa: E402

REAL_LOCAL_DATA = PROJECT_ROOT / "local_data"
KRAKEN_BTC_CACHE = REAL_LOCAL_DATA / "kraken_BTCUSD_1h.csv"

# Gap-free reachability window (BTC 2022 — audited 0 missing bars). Chosen so
# the public DataManager path finds NO missing period and performs no remote
# fetch / cache re-save (see module docstring's read-only-rule note).
WINDOW_START = "2022-01-01"
WINDOW_END = "2022-12-31"
EXPECTED_WINDOW_ROWS = 8760
WINDOW_FIRST = pd.Timestamp("2022-01-01 00:00:00")
WINDOW_LAST = pd.Timestamp("2022-12-31 23:00:00")


# ---------------------------------------------------------------------------
# (a) tz-naive convention guard
# ---------------------------------------------------------------------------

def test_load_local_raises_on_tz_aware_cache(tmp_path):
    """
    Inject a cache CSV whose timestamp column carries an explicit UTC offset
    (e.g. a future writer that parsed with utc=True). _load_local must raise
    rather than silently hand back a tz-aware DataFrame that downstream naive
    comparisons (base_fetcher start/end filtering, fear_greed_fetcher.py,
    data_manager.py, launcher.py) would choke on far from the real cause.
    """
    fetcher = CcxtFetcher(
        start_date="2020-01-01",
        end_date="2020-01-02",
        symbols=["BTCUSDT"],
        candle_interval_seconds=3600,
        exchange="binance",
        localStorage=False,
        data_dir=str(tmp_path),
    )
    bad_path = Path(fetcher._csv_path("BTCUSDT"))
    bad_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2020-01-01T00:00:00+00:00,1,1,1,1,1\n"
        "2020-01-01T01:00:00+00:00,1,1,1,1,1\n"
    )

    with pytest.raises(ValueError, match="tz-aware"):
        fetcher._load_local("BTCUSDT")


def test_load_local_accepts_naive_cache(tmp_path):
    """Control: an ordinary naive-UTC cache (the actual convention) still loads fine."""
    fetcher = CcxtFetcher(
        start_date="2020-01-01",
        end_date="2020-01-02",
        symbols=["BTCUSDT"],
        candle_interval_seconds=3600,
        exchange="binance",
        localStorage=False,
        data_dir=str(tmp_path),
    )
    good_path = Path(fetcher._csv_path("BTCUSDT"))
    good_path.write_text(
        "timestamp,open,high,low,close,volume\n"
        "2020-01-01 00:00:00,1,1,1,1,1\n"
        "2020-01-01 01:00:00,1,1,1,1,1\n"
    )

    df = fetcher._load_local("BTCUSDT")
    assert not df.empty
    assert df["timestamp"].dt.tz is None


# ---------------------------------------------------------------------------
# (b) End-to-end reachability via DataManager.fetch_historical_data(exchange=...)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(
    not KRAKEN_BTC_CACHE.exists(),
    reason=f"Kraken BTC cache not present: {KRAKEN_BTC_CACHE}",
)
def test_kraken_cache_reachable_via_data_manager_exchange_param():
    """
    Load kraken_BTCUSD_1h.csv end-to-end through the public
    DataManager.fetch_historical_data() path with the new `exchange` kwarg,
    reading the REAL on-disk local_data/ cache (not an isolated tmp_path) so
    this is a genuine reachability proof, not a synthetic round-trip.

    Uses the settled STANDARD-base store symbol BTCUSD (not the old XBTUSD),
    over a gap-free window so the read triggers no remote fetch / re-save.
    """
    dm = DataManager(symbols=["BTCUSD"], interval_seconds=3600, mode="backtest")

    df = dm.fetch_historical_data(
        "BTCUSD", WINDOW_START, WINDOW_END, exchange="kraken"
    )

    assert not df.empty
    assert len(df) == EXPECTED_WINDOW_ROWS, len(df)
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert df["timestamp"].dt.tz is None
    assert df["timestamp"].iloc[0] == WINDOW_FIRST
    assert df["timestamp"].iloc[-1] == WINDOW_LAST


BINANCE_BTC_CACHE = REAL_LOCAL_DATA / "BTCUSDT_1h.csv"


@pytest.mark.skipif(
    not BINANCE_BTC_CACHE.exists(),
    reason=f"Binance BTC cache not present: {BINANCE_BTC_CACHE}",
)
def test_default_exchange_still_binance_unqualified():
    """
    Existing call sites that don't pass `exchange` must keep resolving to the
    original unqualified Binance filename — the additive-parameter guarantee
    from this dispatch. Reads the REAL local_data/ cache (no exchange kwarg,
    exactly like every pre-existing call site) and confirms it still returns
    real rows without ever touching a qualified 'binance_BTCUSDT_1h.csv'.
    """
    qualified_variant = REAL_LOCAL_DATA / "binance_BTCUSDT_1h.csv"
    assert not qualified_variant.exists()

    dm = DataManager(symbols=["BTCUSDT"], interval_seconds=3600, mode="backtest")
    df = dm.fetch_historical_data("BTCUSDT", "2018-01-01", "2018-01-02")  # no exchange kwarg

    assert not df.empty
    assert BINANCE_BTC_CACHE.exists()
    # Untouched: no qualified variant ever created alongside the original.
    assert not qualified_variant.exists()
