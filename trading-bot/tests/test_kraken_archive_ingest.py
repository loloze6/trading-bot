"""
Phase 2 Track A — tests for the exchange-qualified cache key and the Kraken
bulk-archive 5-pair pilot ingestion.

Two groups:
  (a) cache_key() behaviour: Binance key reproduced exactly (backward compat),
      Kraken key exchange-qualified, and NO collision between the two for the
      same symbol/timeframe.
  (b) Round-trip integrity of an ingested pilot file: row count, first/last
      timestamps, and column values spot-checked against directly re-reading
      the source Kraken CSV.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.ccxt_fetcher import CcxtFetcher  # noqa: E402
from tools import ingest_kraken_archive as ing       # noqa: E402

ARCHIVE_DIR = PROJECT_ROOT / "local_data" / "Kraken_batch" / "master_q4"

# One representative pilot pair for the round-trip test.
PILOT_ASSET = "BTC"
PILOT_SOURCE = ing.kraken_source_path(PILOT_ASSET, ARCHIVE_DIR)


def _fetcher(exchange: str, data_dir: str) -> CcxtFetcher:
    return CcxtFetcher(
        start_date="2020-01-01",
        end_date="2020-01-02",
        symbols=["BTCUSDT"],
        candle_interval_seconds=3600,   # -> "1h"
        exchange=exchange,
        localStorage=False,
        data_dir=data_dir,
    )


# ---------------------------------------------------------------------------
# (a) cache_key behaviour
# ---------------------------------------------------------------------------

def test_binance_cache_key_unprefixed_backward_compatible(tmp_path):
    """Binance keeps its historical UN-prefixed key — no migration needed."""
    f = _fetcher("binance", str(tmp_path))
    assert f.cache_key("BTCUSDT") == "BTCUSDT_1h"
    # And the derived filename matches existing on-disk convention exactly.
    assert Path(f._csv_path("BTCUSDT")).name == "BTCUSDT_1h.csv"


def test_kraken_cache_key_is_exchange_qualified(tmp_path):
    f = _fetcher("kraken", str(tmp_path))
    assert f.cache_key("XBTUSD") == "kraken_XBTUSD_1h"
    assert Path(f._csv_path("XBTUSD")).name == "kraken_XBTUSD_1h.csv"


def test_no_collision_same_symbol_timeframe(tmp_path):
    """
    The whole point of the fix: a Kraken instance fetching the SAME compact
    symbol/timeframe as Binance must not resolve to the same cache file.
    """
    binance = _fetcher("binance", str(tmp_path))
    kraken = _fetcher("kraken", str(tmp_path))
    assert binance.cache_key("BTCUSDT") != kraken.cache_key("BTCUSDT")
    assert binance._csv_path("BTCUSDT") != kraken._csv_path("BTCUSDT")


def test_nonbinance_exchanges_all_prefixed(tmp_path):
    """Only binance is unprefixed; every other venue is qualified."""
    for ex in ("kraken", "coinbase", "bybit"):
        f = _fetcher(ex, str(tmp_path))
        assert f.cache_key("BTCUSDT") == f"{ex}_BTCUSDT_1h"


# ---------------------------------------------------------------------------
# (b) Round-trip integrity of an ingested pilot file
# ---------------------------------------------------------------------------

@pytest.mark.skipif(
    not PILOT_SOURCE.exists(),
    reason=f"Kraken pilot archive not present: {PILOT_SOURCE}",
)
def test_ingest_roundtrip_integrity(tmp_path):
    # Ingest into an isolated temp cache dir (does not touch real local_data/).
    summary = ing.ingest(PILOT_ASSET, ARCHIVE_DIR, tmp_path)

    # Cache slot is exchange-qualified.
    assert summary["cache_key"] == "kraken_XBTUSD_1h"
    dest = Path(summary["dest"])
    assert dest.name == "kraken_XBTUSD_1h.csv"
    assert dest.exists()

    # --- Directly re-read the SOURCE Kraken CSV (ground truth) ---
    raw = pd.read_csv(PILOT_SOURCE, header=None, names=ing.KRAKEN_RAW_COLUMNS)
    # --- Re-read the INGESTED cache file ---
    got = pd.read_csv(dest)
    got["timestamp"] = pd.to_datetime(got["timestamp"])

    # Schema: exact Binance column order.
    assert list(got.columns) == ing.BINANCE_COLUMNS

    # Row count preserved (source has no duplicate timestamps).
    assert len(got) == len(raw), (len(got), len(raw))

    # First/last timestamps match stdlib UTC conversion of raw unix seconds.
    import datetime as _dt
    _utc = _dt.timezone.utc
    exp_first = _dt.datetime.fromtimestamp(int(raw["unix_s"].iloc[0]), _utc).replace(tzinfo=None)
    exp_last = _dt.datetime.fromtimestamp(int(raw["unix_s"].iloc[-1]), _utc).replace(tzinfo=None)
    assert got["timestamp"].iloc[0].to_pydatetime() == exp_first
    assert got["timestamp"].iloc[-1].to_pydatetime() == exp_last

    # Column-value spot checks against the source (first and last rows).
    for pos in (0, -1):
        for col in ("open", "high", "low", "close", "volume"):
            assert got[col].iloc[pos] == pytest.approx(raw[col].iloc[pos]), (col, pos)
        # number_of_trades carries Kraken's real per-candle count.
        assert int(got["number_of_trades"].iloc[pos]) == int(raw["trade_count"].iloc[pos])
        # Derived quote volume = volume * close (estimated), matches CcxtFetcher.
        assert got["quote_asset_volume"].iloc[pos] == pytest.approx(
            raw["volume"].iloc[pos] * raw["close"].iloc[pos]
        )
        # ignore constant, taker_* absent.
        assert got["ignore"].iloc[pos] == 0
        assert pd.isna(got["taker_buy_base_asset_volume"].iloc[pos])
        assert pd.isna(got["taker_buy_quote_asset_volume"].iloc[pos])

    # close_time = timestamp + (1h - 1ms).
    delta = got["close_time"].apply(pd.Timestamp) - got["timestamp"]
    assert (delta == pd.Timedelta(milliseconds=ing.TIMEFRAME_MS - 1)).all()


@pytest.mark.skipif(
    not PILOT_SOURCE.exists(),
    reason=f"Kraken pilot archive not present: {PILOT_SOURCE}",
)
def test_utc_roundtrip_guard_raises_on_shift():
    """The UTC guard must actually fire when timestamps don't match UTC."""
    raw = pd.read_csv(PILOT_SOURCE, header=None,
                      names=ing.KRAKEN_RAW_COLUMNS).head(10)
    converted = ing.to_binance_schema(raw)
    # Corrupt the converted timestamps by a +1h shift -> guard must raise.
    bad = converted.copy()
    bad["timestamp"] = bad["timestamp"] + pd.Timedelta(hours=1)
    with pytest.raises(ing.IngestUTCError):
        ing.verify_utc_roundtrip(raw, bad)
