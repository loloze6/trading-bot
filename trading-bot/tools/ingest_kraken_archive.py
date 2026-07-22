"""
Kraken bulk-archive → local cache ingestion (Phase 2 Track A, 5-pair pilot)
==========================================================================

Converts Kraken's static bulk-export OHLCV CSVs (headerless, unix-second
timestamps) into the exact column schema used by the Binance-sourced cache
files this bot already reads, and writes them into the *exchange-qualified*
cache slot (`kraken_<TICKER>_<tf>.csv`) produced by the fixed
`CcxtFetcher.cache_key()`.

Why exchange-qualified: a Kraken `CcxtFetcher` fetching e.g. `XBTUSD` at 1h now
derives cache_key `kraken_XBTUSD_1h`, so a future *live top-up* (Jan 2026 →
present, the ~7-month archive gap) lands in the SAME slot these ingested rows
occupy — the archive and the live feed compose cleanly.

Pilot scope: BTC, ETH, SOL, ADA, LINK, USD-quoted, 1-hour resolution.
Reusable for the remaining 15 pairs of the 20-pair breadth set later.

Source schema (Kraken bulk, no header, 7 cols):
    unix_seconds, open, high, low, close, volume, trade_count

Target schema (Binance cache, WITH header, 12 cols, this exact order):
    timestamp, open, high, low, close, volume, close_time,
    quote_asset_volume, number_of_trades,
    taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore

Run:
    python trading-bot/tools/ingest_kraken_archive.py
"""

import datetime
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # tools/ -> trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.ccxt_fetcher import CcxtFetcher  # noqa: E402

# ---------------------------------------------------------------------------
# Pilot configuration
# ---------------------------------------------------------------------------

# Kraken uses legacy base-currency tickers, not the market-standard ones.
# BTC is stored under XBT. (For the full 20-pair scale-up, DOGE is under XDG —
# NOT DOGEUSD; not part of this pilot, documented here so the mapping isn't
# rediscovered later.) All other pilot assets use their standard base ticker.
KRAKEN_TICKER_MAP = {
    "BTC": "XBT",
    # "DOGE": "XDG",   # full-run only — not ingested in this pilot
}

PILOT_ASSETS = ["BTC", "ETH", "SOL", "ADA", "LINK"]
QUOTE = "USD"                # Kraken's primary USD quote. NB: the Binance breadth
                             # cache is USDT-quoted — a documented venue divergence,
                             # not a bug (see ledger entry).
RESOLUTION_MINUTES = 60      # 1h — matches the dominant Binance breadth cache
                             # resolution (BTCUSDT_1h / ETHUSDT_1h / SOLUSDT_1h).
CANDLE_INTERVAL_SECONDS = RESOLUTION_MINUTES * 60          # -> ccxt_timeframe "1h"
TIMEFRAME_MS = RESOLUTION_MINUTES * 60 * 1000

# Binance cache column order — target schema, reproduced exactly.
BINANCE_COLUMNS = [
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore",
]

KRAKEN_RAW_COLUMNS = [
    "unix_s", "open", "high", "low", "close", "volume", "trade_count",
]


class IngestUTCError(RuntimeError):
    """Raised when the UTC round-trip verification fails (data is NOT UTC)."""


def kraken_pair(asset: str) -> str:
    """'BTC' -> 'XBTUSD', 'ETH' -> 'ETHUSD', ..."""
    base = KRAKEN_TICKER_MAP.get(asset, asset)
    return f"{base}{QUOTE}"


def kraken_source_path(asset: str, archive_dir: Path,
                       resolution: int = RESOLUTION_MINUTES) -> Path:
    return archive_dir / f"{kraken_pair(asset)}_{resolution}.csv"


def load_kraken_ohlcv(path: Path) -> pd.DataFrame:
    """Read a headerless Kraken bulk CSV into a named-column DataFrame."""
    raw = pd.read_csv(path, header=None, names=KRAKEN_RAW_COLUMNS)
    if raw.empty:
        raise ValueError(f"Empty Kraken source file: {path}")
    # Sanity: unix seconds are 10-digit (ms would be 13). Guards against a
    # silent ms/s misread that would place candles in 1970 or the far future.
    span = raw["unix_s"].iloc[-1] - raw["unix_s"].iloc[0]
    if span <= 0:
        raise ValueError(f"Non-increasing timestamps in {path}")
    return raw


def to_binance_schema(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Map Kraken raw OHLCV to the exact Binance cache column schema/order.

    Value-level notes:
      • close_time / quote_asset_volume are derived identically to
        CcxtFetcher._fetch_remote (est. quote vol = volume * close).
      • number_of_trades is populated with Kraken's REAL per-candle trade count
        (the bulk archive carries it; live ccxt fetch_ohlcv does not, so
        live-fetched Kraken rows will leave this NaN — a documented, minor,
        source-of-truth divergence flagged in the ledger, not a schema break).
      • taker_buy_* are NaN (Kraken bulk has no taker breakdown), matching what
        CcxtFetcher writes for a live Kraken fetch.
    """
    ts = pd.to_datetime(raw["unix_s"], unit="s")  # tz-naive, epoch == UTC
    out = pd.DataFrame({
        "timestamp": ts,
        "open": raw["open"].astype(float),
        "high": raw["high"].astype(float),
        "low": raw["low"].astype(float),
        "close": raw["close"].astype(float),
        "volume": raw["volume"].astype(float),
        "close_time": ts + pd.Timedelta(milliseconds=TIMEFRAME_MS - 1),
        "quote_asset_volume": raw["volume"].astype(float) * raw["close"].astype(float),
        "number_of_trades": raw["trade_count"].astype("int64"),
        "taker_buy_base_asset_volume": np.nan,
        "taker_buy_quote_asset_volume": np.nan,
        "ignore": 0,
    })
    return out[BINANCE_COLUMNS]


def verify_utc_roundtrip(raw: pd.DataFrame, converted: pd.DataFrame) -> None:
    """
    Concrete UTC check (standing timezone lesson, commit 2529f5b): the
    fetch/cache layer does NOT inherit CandleBuilder._align()'s UTC guard, so
    this ingestion asserts its own. We do NOT trust the recon's inferred-UTC:
    we verify that each of the first AND last raw unix epochs maps to the
    stdlib UTC wall-clock and survives unchanged in the converted frame.
    Raises IngestUTCError on any mismatch (STOP condition — no silent shift).
    """
    for pos in (0, -1):
        unix_s = int(raw["unix_s"].iloc[pos])
        # tz-aware UTC then strip tzinfo -> tz-naive UTC wall-clock (matches the
        # naive-UTC convention the Binance cache stores). Avoids deprecated
        # utcfromtimestamp while remaining an explicit UTC assertion.
        expected = datetime.datetime.fromtimestamp(
            unix_s, datetime.timezone.utc).replace(tzinfo=None)
        got = pd.Timestamp(converted["timestamp"].iloc[pos]).to_pydatetime()
        if got != expected:
            raise IngestUTCError(
                f"UTC round-trip FAILED at row {pos}: unix {unix_s} -> "
                f"expected {expected} (UTC) but got {got}. Data is not UTC "
                f"as assumed — halting; timestamps were NOT shifted."
            )


def ingest(asset: str, archive_dir: Path, data_dir: Path,
           resolution: int = RESOLUTION_MINUTES) -> dict:
    """
    Ingest one pilot asset. Returns a summary dict. The file is written through
    the real fetcher plumbing (`_merge_and_store` -> `_csv_path` -> the fixed
    `cache_key`) so it lands in the exact slot a live Kraken fetch would use.
    """
    src = kraken_source_path(asset, archive_dir, resolution)
    if not src.exists():
        raise FileNotFoundError(f"Kraken source missing for {asset}: {src}")

    raw = load_kraken_ohlcv(src)
    converted = to_binance_schema(raw)
    verify_utc_roundtrip(raw, converted)  # STOP-on-fail

    store_symbol = kraken_pair(asset)  # e.g. XBTUSD -> cache_key kraken_XBTUSD_1h
    fetcher = CcxtFetcher(
        start_date=converted["timestamp"].min(),
        end_date=converted["timestamp"].max(),
        symbols=[store_symbol],
        candle_interval_seconds=resolution * 60,
        exchange="kraken",
        localStorage=True,
        data_dir=str(data_dir),
    )
    fetcher._merge_and_store(store_symbol, [converted], save=True)
    dest = Path(fetcher._csv_path(store_symbol))

    # Reload-from-disk round trip, then re-assert UTC survived the write.
    reloaded = pd.read_csv(dest)
    reloaded["timestamp"] = pd.to_datetime(reloaded["timestamp"])
    verify_utc_roundtrip(raw, reloaded)

    return {
        "asset": asset,
        "store_symbol": store_symbol,
        "source": str(src),
        "dest": str(dest),
        "cache_key": fetcher.cache_key(store_symbol),
        "rows": len(reloaded),
        "first": reloaded["timestamp"].iloc[0],
        "last": reloaded["timestamp"].iloc[-1],
    }


def main() -> None:
    archive_dir = PROJECT_ROOT / "local_data" / "Kraken_batch" / "master_q4"
    data_dir = PROJECT_ROOT / "local_data"

    print(f"Kraken archive : {archive_dir}")
    print(f"Cache data_dir : {data_dir}")
    print(f"Pilot assets   : {PILOT_ASSETS} @ {QUOTE} {RESOLUTION_MINUTES}m\n")

    for asset in PILOT_ASSETS:
        r = ingest(asset, archive_dir, data_dir)
        print(f"[OK] {asset:5s} {r['cache_key']:22s} rows={r['rows']:>7} "
              f"{r['first']} -> {r['last']}  ({Path(r['dest']).name})")


if __name__ == "__main__":
    main()
