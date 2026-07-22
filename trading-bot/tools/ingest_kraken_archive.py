"""
Kraken bulk-archive → local cache ingestion (Phase 2 Track A, 20-pair breadth)
=============================================================================

Converts Kraken's static bulk-export OHLCV CSVs (headerless, unix-second
timestamps) into the exact column schema used by the Binance-sourced cache
files this bot already reads, and writes them into the *exchange-qualified*
cache slot (`kraken_<STORE_SYMBOL>_<tf>.csv`) produced by the fixed
`CcxtFetcher.cache_key()`.

Two distinct symbol spaces, deliberately separated (settled 2026-07-22 on
ccxt `load_markets()` evidence — see ledger G2):

  • SOURCE symbol — how the *archive file* is named. Kraken's bulk export uses
    its own legacy altname base: BTC → `XBTUSD_60.csv`, DOGE → `XDGUSD_60.csv`.
    Used ONLY to locate the CSV on disk (`KRAKEN_SOURCE_BASE`).

  • STORE symbol — the string handed to `CcxtFetcher`, hence the cache_key.
    This is the **standard-base compact** form `<BASE>USD` (BTC, DOGE — NOT
    XBT, XDG): e.g. `BTCUSD` → cache_key `kraken_BTCUSD_1h`.

Why the STORE symbol is standard-base, not Kraken's altname (the load-bearing
correction to the pilot): a live top-up must (i) land in the SAME cache slot
as these rows and (ii) actually fetch. `_fetch_remote` normalizes a compact
symbol to `BASE/QUOTE` before calling ccxt. ccxt's Kraken adapter only accepts
its UNIFIED symbol `BTC/USD` (verified: `market('BTC/USD')` → id `XXBTZUSD`);
it rejects both `XBTUSD` and `XBT/USD` with `BadSymbol`. So a top-up keyed on
the old `XBTUSD` could never fetch — `XBTUSD` → `XBT/USD` → BadSymbol. Keyed on
`BTCUSD`, the same string yields cache_key `kraken_BTCUSD_1h` AND normalizes to
`BTC/USD`, which ccxt fetches. Pairs whose standard base already equals Kraken's
altname base (ETH, SOL, ADA, LINK, …) were unaffected and keep their names;
only the legacy-ticker pairs (BTC=XBT, DOGE=XDG) diverged and are corrected.
The unified `BTC/USD` itself cannot be the cache key — the `/` is a path
separator (filesystem constraint). None of this touches `cache_key()`, which
keeps Binance UN-prefixed (ratified decision (a)); it is purely the choice of
the `symbol` string this script and any future top-up hand to the fetcher.

Scope: the 20-pair USD-quoted breadth set at 1-hour resolution. HYPE is absent
from the bulk archive (no `HYPEUSD_60.csv`) and is skipped — it needs a
separate live-fetch path (ledger G1 carry-forward 1). 19 of 20 ingest here.

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
# Breadth configuration
# ---------------------------------------------------------------------------

# SOURCE-file naming only: Kraken's bulk export uses legacy base tickers, not
# the market-standard ones. BTC's archive file is XBTUSD_60.csv, DOGE's is
# XDGUSD_60.csv. This map is consulted ONLY to locate the CSV on disk; the
# STORE symbol (cache key) uses the standard base — see cache_symbol().
KRAKEN_SOURCE_BASE = {
    "BTC": "XBT",
    "DOGE": "XDG",
}

# 20-pair USD breadth set (standard base tickers). Order = the recon's volume
# ranking source list. HYPE has no bulk-archive file and is skipped at runtime.
BREADTH_ASSETS = [
    "BTC", "ETH", "XRP", "SOL", "ADA", "SUI", "ZEC", "DOGE", "HYPE", "XMR",
    "LTC", "ONDO", "NEAR", "LINK", "TAO", "AVAX", "TRX", "AAVE", "INJ", "UNI",
]
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


def kraken_source_pair(asset: str) -> str:
    """SOURCE-file pair (Kraken altname base): 'BTC' -> 'XBTUSD',
    'DOGE' -> 'XDGUSD', 'ETH' -> 'ETHUSD', ..."""
    base = KRAKEN_SOURCE_BASE.get(asset, asset)
    return f"{base}{QUOTE}"


def cache_symbol(asset: str) -> str:
    """STORE symbol = cache-key input (standard base, never the Kraken altname):
    'BTC' -> 'BTCUSD', 'DOGE' -> 'DOGEUSD', 'ETH' -> 'ETHUSD', ...

    Chosen so a future live top-up passing this same string (i) lands in the
    identical cache slot via cache_key() and (ii) survives _fetch_remote's
    compact->'BASE/QUOTE' normalization into ccxt's unified symbol 'BASE/USD'
    (the only form Kraken's ccxt adapter accepts). See module docstring."""
    return f"{asset}{QUOTE}"


def kraken_source_path(asset: str, archive_dir: Path,
                       resolution: int = RESOLUTION_MINUTES) -> Path:
    return archive_dir / f"{kraken_source_pair(asset)}_{resolution}.csv"


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


def compute_gap_stats(ts: pd.Series, resolution: int = RESOLUTION_MINUTES,
                      since_year: int = 2017) -> dict:
    """
    Coverage stats over a timestamp column, matching the audit's methodology
    (expected = span/interval + 1 inclusive; missing = expected - actual).

    Returns full-history and post-`since_year` figures. The post-cutoff figure
    is the breadth-viability signal — the pilot's 2017+ BTC benchmark is 0.11%.
    """
    ts = pd.to_datetime(ts).sort_values().reset_index(drop=True)
    step_h = resolution / 60.0

    def _rate(series: pd.Series) -> dict:
        if len(series) < 2:
            return {"rows": len(series), "expected": len(series),
                    "missing": 0, "pct": 0.0}
        span_h = (series.iloc[-1] - series.iloc[0]).total_seconds() / 3600.0
        expected = int(round(span_h / step_h)) + 1
        missing = expected - len(series)
        pct = 100.0 * missing / expected if expected else 0.0
        return {"rows": len(series), "expected": expected,
                "missing": missing, "pct": pct}

    full = _rate(ts)
    post = _rate(ts[ts >= pd.Timestamp(year=since_year, month=1, day=1)]
                 .reset_index(drop=True))
    return {"full": full, "post": post, "since_year": since_year}


def ingest(asset: str, archive_dir: Path, data_dir: Path,
           resolution: int = RESOLUTION_MINUTES) -> dict:
    """
    Ingest one breadth asset. Returns a summary dict. The file is written
    through the real fetcher plumbing (`_merge_and_store` -> `_csv_path` -> the
    fixed `cache_key`) so it lands in the exact slot a live Kraken fetch would
    use — under the STANDARD-base store symbol (BTCUSD, not XBTUSD).
    """
    src = kraken_source_path(asset, archive_dir, resolution)
    if not src.exists():
        raise FileNotFoundError(f"Kraken source missing for {asset}: {src}")

    raw = load_kraken_ohlcv(src)
    converted = to_binance_schema(raw)
    verify_utc_roundtrip(raw, converted)  # STOP-on-fail

    store_symbol = cache_symbol(asset)  # e.g. BTCUSD -> cache_key kraken_BTCUSD_1h
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

    gaps = compute_gap_stats(reloaded["timestamp"], resolution)
    return {
        "asset": asset,
        "store_symbol": store_symbol,
        "source": str(src),
        "dest": str(dest),
        "cache_key": fetcher.cache_key(store_symbol),
        "rows": len(reloaded),
        "first": reloaded["timestamp"].iloc[0],
        "last": reloaded["timestamp"].iloc[-1],
        "gaps": gaps,
    }


def main() -> None:
    archive_dir = PROJECT_ROOT / "local_data" / "Kraken_batch" / "master_q4"
    data_dir = PROJECT_ROOT / "local_data"

    print(f"Kraken archive : {archive_dir}")
    print(f"Cache data_dir : {data_dir}")
    print(f"Breadth assets : {len(BREADTH_ASSETS)} @ {QUOTE} {RESOLUTION_MINUTES}m\n")

    done, skipped = [], []
    for asset in BREADTH_ASSETS:
        src = kraken_source_path(asset, archive_dir)
        if not src.exists():
            skipped.append(asset)
            print(f"[SKIP] {asset:5s} source absent ({src.name})")
            continue
        r = ingest(asset, archive_dir, data_dir)
        done.append(r)
        print(f"[OK] {asset:5s} {r['cache_key']:20s} rows={r['rows']:>7} "
              f"{r['first']} -> {r['last']}")

    # Coverage table
    print(f"\n{'asset':6}{'cache_key':22}{'rows':>8}  {'first':16} {'last':16}"
          f"{'miss':>7}{'full%':>8}{'2017+%':>9}")
    for r in done:
        g = r["gaps"]
        f, p = g["full"], g["post"]
        print(f"{r['asset']:6}{r['cache_key']:22}{r['rows']:>8}  "
              f"{str(r['first'])[:16]:16} {str(r['last'])[:16]:16}"
              f"{f['missing']:>7}{f['pct']:>7.2f}%{p['pct']:>8.2f}%")

    print(f"\nIngested {len(done)}/{len(BREADTH_ASSETS)}; skipped "
          f"{skipped or 'none'}. Pilot 2017+ BTC benchmark = 0.11%.")


if __name__ == "__main__":
    main()
