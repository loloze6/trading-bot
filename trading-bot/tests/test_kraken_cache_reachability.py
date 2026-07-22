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
      path down to kraken_XBTUSD_1h.csv and get real rows back.
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
KRAKEN_BTC_CACHE = REAL_LOCAL_DATA / "kraken_XBTUSD_1h.csv"

# Ratified audit figures (docs/session_reports/20260721_breadth_download_recon.md
# and the Kraken 5-pair pilot ingestion) that step 4 of this dispatch must
# reproduce via the public DataManager path, not just by re-reading the CSV.
EXPECTED_ROWS = 96381
EXPECTED_FIRST = pd.Timestamp("2013-10-06 21:00:00")
EXPECTED_LAST = pd.Timestamp("2025-12-31 23:00:00")


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
    Load kraken_XBTUSD_1h.csv end-to-end through the public
    DataManager.fetch_historical_data() path with the new `exchange` kwarg,
    reading the REAL on-disk local_data/ cache (not an isolated tmp_path) so
    this is a genuine reachability proof, not a synthetic round-trip.
    """
    dm = DataManager(symbols=["XBTUSD"], interval_seconds=3600, mode="backtest")

    df = dm.fetch_historical_data(
        "XBTUSD", "2013-01-01", "2025-12-31", exchange="kraken"
    )

    assert not df.empty
    assert len(df) == EXPECTED_ROWS, len(df)
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert df["timestamp"].dt.tz is None
    assert df["timestamp"].iloc[0] == EXPECTED_FIRST
    assert df["timestamp"].iloc[-1] == EXPECTED_LAST


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
