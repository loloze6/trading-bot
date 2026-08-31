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

Scope: the 20-pair USD-quoted breadth set — 1-hour by default, or any exactly
mapped ccxt resolution via `--resolution` (60 = 1h, 1440 = 1d). HYPE is absent
from the bulk archive (no `HYPEUSD_<res>.csv`) and is skipped — it needs a
separate live-fetch path (ledger G1 carry-forward 1). 19 of 20 ingest here.

Source schema (Kraken bulk, no header, 7 cols):
    unix_seconds, open, high, low, close, volume, trade_count

Target schema (Binance cache, WITH header, 12 cols, this exact order):
    timestamp, open, high, low, close, volume, close_time,
    quote_asset_volume, number_of_trades,
    taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore

Run:
    python trading-bot/tools/ingest_kraken_archive.py                    # 1h
    python trading-bot/tools/ingest_kraken_archive.py --resolution 1440  # 1d
"""

import argparse
import datetime
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # tools/ -> trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.ccxt_fetcher import CcxtFetcher  # noqa: E402

#: `strategy-research/config/campaign_data_policy.yaml:holdout_range`. Read, never
#: assumed — the seal moves with the policy, the same rule
#: `tests/test_no_sealed_date_literals.py` states and follows.
_POLICY_PATH = PROJECT_ROOT.parent / "strategy-research" / "config" / "campaign_data_policy.yaml"


def _holdout_bounds() -> tuple:
    """(first sealed instant, first instant AFTER the seal), from the policy.

    BOTH ends. holdout_range is a closed window and the policy declares data
    usable again after it (`era_2026_h2_forward_recorded`), so keying on the
    start alone would reject a legitimate 2026-Q3 tranche wholesale rather than
    just the sealed part. The upper end is INCLUSIVE in the policy, hence the
    returned bound is the following midnight and the comparison is strict.

    Deny-by-default on every failure to read, INCLUDING an unavailable yaml —
    hence the import inside the try. An ingest that cannot prove where the seal
    is must not write. This mirrors `holdout_date_gate.sh`'s stance that silence
    is never success, and it matters more here than in a scanner because this
    path WRITES into tracked caches.
    """
    try:
        import yaml  # local: keeps the module importable where yaml is absent
        with open(_POLICY_PATH, encoding="utf-8") as fh:
            lo, hi = yaml.safe_load(fh)["holdout_range"][:2]
        return pd.Timestamp(lo), pd.Timestamp(hi).normalize() + pd.Timedelta(days=1)
    except Exception as exc:                                  # noqa: BLE001
        raise RuntimeError(
            f"Cannot read holdout_range from {_POLICY_PATH}: {exc}. Refusing to "
            f"ingest — an ingest that cannot locate the seal cannot prove it is "
            f"not writing sealed rows into a tracked cache. NOTHING was written."
        ) from exc

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
    # STRICTLY increasing — not just first-vs-last, and not merely
    # non-decreasing. An interior row out of order clears the span check above
    # and is invisible to the span-scoped verification in ingest() (which
    # compares only the two boundary rows). A REPEATED timestamp is just as
    # malformed and less visible still: drop_duplicates downstream keeps
    # whichever copy sorts first and discards the conflicting value with
    # nothing reported. Sorting or de-duplicating here would paper either one
    # over — name it and stop instead.
    if not (raw["unix_s"].diff().iloc[1:] > 0).all():
        raise ValueError(
            f"Out-of-order timestamps in {path}: the bulk export is assumed "
            f"strictly chronological, and a duplicate or out-of-order row means "
            f"a malformed archive. Sorting or de-duplicating it here would "
            f"silently paper that over — inspect the source instead."
        )
    return raw


def to_binance_schema(raw: pd.DataFrame,
                      resolution_minutes: int = RESOLUTION_MINUTES) -> pd.DataFrame:
    """
    Map Kraken raw OHLCV to the exact Binance cache column schema/order.

    Value-level notes:
      • close_time spans one candle less a millisecond, derived from the
        REQUESTED resolution (default RESOLUTION_MINUTES = 1h). A daily
        (1440-minute) tranche must not inherit a 1h close_time.
      • quote_asset_volume is derived identically to
        CcxtFetcher._fetch_remote (est. quote vol = volume * close).
      • number_of_trades is populated with Kraken's REAL per-candle trade count
        (the bulk archive carries it; live ccxt fetch_ohlcv does not, so
        live-fetched Kraken rows will leave this NaN — a documented, minor,
        source-of-truth divergence flagged in the ledger, not a schema break).
      • taker_buy_* are NaN (Kraken bulk has no taker breakdown), matching what
        CcxtFetcher writes for a live Kraken fetch.
    """
    ts = pd.to_datetime(raw["unix_s"], unit="s")  # tz-naive, epoch == UTC
    close_time_ms = resolution_minutes * 60 * 1000
    out = pd.DataFrame({
        "timestamp": ts,
        "open": raw["open"].astype(float),
        "high": raw["high"].astype(float),
        "low": raw["low"].astype(float),
        "close": raw["close"].astype(float),
        "volume": raw["volume"].astype(float),
        "close_time": ts + pd.Timedelta(milliseconds=close_time_ms - 1),
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


def verify_boundary_values(converted: pd.DataFrame, archive_span: pd.DataFrame,
                           dest: Path) -> None:
    """
    Value-level companion to verify_utc_roundtrip's timestamp comparison, and
    the half that stays live on a top-up.

    The timestamp check alone is geometrically inert once a cache exists: the
    span mask is built from `converted`'s OWN bounds, so archive_span's first
    and last rows carry exactly those timestamps by construction whenever the
    cache already covers them. A neighbouring CACHE row then satisfies the
    comparison no matter what the write did, and a whole-file shift lands
    silently.

    Values close that. The archive wins duplicate timestamps, so on a healthy
    write the row sitting at each boundary is the archive's own; a shifted or
    reordered write puts a different row there. Tolerance rather than equality
    because the CSV float round-trip is not bit-exact.
    """
    for pos in (0, -1):
        for col in ("open", "high", "low", "close", "volume"):
            expected = converted[col].iloc[pos]
            got = archive_span[col].iloc[pos]
            # NaN on both sides is left alone: this check exists to catch a
            # displaced write, not to become a NaN rejector by side effect.
            if pd.isna(expected) and pd.isna(got):
                continue
            if not abs(got - expected) <= max(abs(expected) * 1e-9, 1e-12):
                raise IngestUTCError(
                    f"Post-write boundary-row mismatch in {dest}: at archive "
                    f"row {pos}, column '{col}' is {got} on disk but the "
                    f"archive says {expected}. The row occupying the archive's "
                    f"own boundary timestamp is not the archive's row — the "
                    f"write displaced or reordered it. Halting."
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
    # STOP on a resolution that has no EXACT ccxt timeframe. CcxtFetcher snaps
    # candle_interval to the NEAREST timeframe, so 720m (12h) would land in the
    # 4h slot and MERGE 12h bars into a legitimate 4h cache; 0 and negatives
    # produce degenerate close_time spans. The store slot (cache_key) is derived
    # from the SAME snap, so a mismatch here IS a mis-file. Refuse before any
    # read or write — this covers programmatic callers, not only the CLI.
    interval_s = resolution * 60
    snapped = CcxtFetcher._seconds_to_ccxt_timeframe(interval_s)
    if CcxtFetcher._timeframe_to_ms(snapped) != interval_s * 1000:
        raise ValueError(
            f"Resolution {resolution}m ({interval_s}s) has no exact ccxt "
            f"timeframe: it snaps to '{snapped}' "
            f"({CcxtFetcher._timeframe_to_ms(snapped) // 1000}s) and would be "
            f"written into the '{snapped}' cache slot, silently mixing a "
            f"different bar size into it. Refusing; NOTHING was written. Use an "
            f"exactly-mapped resolution (1, 5, 15, 30, 60, 240, or 1440 minutes)."
        )

    src = kraken_source_path(asset, archive_dir, resolution)
    if not src.exists():
        raise FileNotFoundError(f"Kraken source missing for {asset}: {src}")

    raw = load_kraken_ohlcv(src)
    converted = to_binance_schema(raw, resolution)
    verify_utc_roundtrip(raw, converted)  # STOP-on-fail

    # Seal guard. Checked HERE — after conversion, before the fetcher is even
    # constructed — so a violating tranche cannot touch the store at all.
    #
    # Today's archive is holdout-clean by inspection (12,027 files ending
    # 2025-12-31), which is exactly why this is worth pinning: the guard is for
    # the NEXT bulk tranche, whose extra rows would otherwise be written into a
    # tracked cache with nothing objecting. Every other seal control in the tree
    # guards reading or committing; this path writes, which is the one direction
    # none of them cover.
    _lo, _hi = _holdout_bounds()
    sealed = converted[(converted["timestamp"] >= _lo) & (converted["timestamp"] < _hi)]
    if not sealed.empty:
        first, last = sealed["timestamp"].min(), sealed["timestamp"].max()
        raise ValueError(
            f"{asset}: archive carries {len(sealed)} row(s) inside the holdout "
            f"seal [{_lo:%Y-%m-%d}, {_hi - pd.Timedelta(days=1):%Y-%m-%d}] — "
            f"first {first}, last {last}. "
            f"Ingesting would write sealed candles into the tracked cache "
            f"{cache_symbol(asset)}. NOTHING was written. Trim the source tranche "
            f"to pre-seal rows, or quarantine it; do not widen this guard."
        )

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
    existing = fetcher._load_local(store_symbol)
    dest = Path(fetcher._csv_path(store_symbol))

    # A cache file that EXISTS but parses to nothing is not a fresh slot.
    # `_load_local` swallows every read error and returns an empty frame, and an
    # empty `existing` switches off BOTH protections below at once: the union
    # degenerates to the archive alone and `_assert_no_new_gap` short-circuits.
    # That is exactly the state where a cache most needs them, so refuse rather
    # than replace. A cache truncated MID-FILE still parses non-empty and is
    # indistinguishable from truth here — this catches unreadable, not partial.
    if existing.empty and dest.exists():
        raise ValueError(
            f"Existing cache {dest} is present but parsed to zero rows — it is "
            f"either unreadable (ragged, truncated, or renamed columns) or "
            f"contentless. Refusing to treat it as a fresh slot, which would "
            f"replace it with this archive alone. NOTHING was written; inspect "
            f"or quarantine the file."
        )

    # MERGE, don't overwrite. Passing `[converted]` alone with no `existing=`
    # has two consequences:
    #   1. the on-disk cache is REPLACED — re-ingesting a 3-month quarterly
    #      bundle over the 2013-2025 master_q4 cache destroys twelve years of
    #      rows, and both occupy this same slot;
    #   2. `_assert_no_new_gap` short-circuits when `existing` is None, so the
    #      continuity guard is dead at this call site.
    # `converted` is placed FIRST so the archive wins on duplicate timestamps
    # (drop_duplicates keeps the first occurrence): a re-ingest must be able to
    # correct a bad cached row, not be a no-op for every timestamp it already
    # has. `existing` is an empty frame on a fresh slot; pd.concat handles it.
    fetcher._merge_and_store(store_symbol, [converted, existing],
                             save=True, existing=existing)

    # Reload-from-disk round trip, then re-assert UTC survived the write.
    reloaded = pd.read_csv(dest)
    reloaded["timestamp"] = pd.to_datetime(reloaded["timestamp"])

    # Scoped to the ARCHIVE's own span, not the whole file. verify_utc_roundtrip
    # compares `raw`'s FIRST and LAST rows against its second argument's, and the
    # merge above is a real union, so the file's bounds are the CACHE's whenever
    # the cache is wider — comparing wholesale raises a spurious IngestUTCError
    # on every top-up of an existing slot.
    # .min()/.max() so the mask and the fetcher's own window (built above from
    # the same two values) are derived identically.
    archive_span = reloaded.loc[
        (reloaded["timestamp"] >= converted["timestamp"].min()) &
        (reloaded["timestamp"] <= converted["timestamp"].max())
    ]
    verify_utc_roundtrip(raw, archive_span)
    # Timestamps alone go blind once a cache brackets the archive's span.
    verify_boundary_values(converted, archive_span, dest)

    # rows/first/last/gaps describe the WHOLE merged cache on disk, not the
    # tranche this call ingested. That is what the coverage table and the
    # "2017+ benchmark" comparison in main() want.
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


def run_all(assets: list, archive_dir: Path, data_dir: Path,
            resolution: int = RESOLUTION_MINUTES) -> tuple:
    """
    Ingest every asset, isolating failures. Returns (done, skipped, failures).

    One asset raising must NOT abort the rest — a single malformed archive or a
    continuity-guard trip would otherwise silently drop every asset after it.
    Each ingest is caught, recorded as (asset, exception), and reported loudly
    at failure time; the run continues. The [SKIP]-on-absent-source path is a
    deliberate no-op, kept separate from failures — absence is expected (HYPE),
    a raise is not.
    """
    done, skipped, failures = [], [], []
    for asset in assets:
        src = kraken_source_path(asset, archive_dir, resolution)
        if not src.exists():
            skipped.append(asset)
            print(f"[SKIP] {asset:5s} source absent ({src.name})")
            continue
        try:
            r = ingest(asset, archive_dir, data_dir, resolution)
        except Exception as exc:
            failures.append((asset, exc))
            print(f"[FAIL] {asset:5s} {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            continue
        done.append(r)
        print(f"[OK] {asset:5s} {r['cache_key']:20s} rows={r['rows']:>7} "
              f"{r['first']} -> {r['last']}")
    return done, skipped, failures


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest Kraken bulk-archive OHLCV CSVs into local cache slots."
    )
    parser.add_argument(
        "--resolution", type=int, default=RESOLUTION_MINUTES,
        help="Candle resolution in MINUTES (60 = 1h, 1440 = 1d). "
             "Selects the source-file suffix (_60 / _1440) and the cache "
             f"timeframe. Default {RESOLUTION_MINUTES}.",
    )
    args = parser.parse_args()
    resolution = args.resolution

    archive_dir = PROJECT_ROOT / "local_data" / "Kraken_batch" / "master_q4"
    data_dir = PROJECT_ROOT / "local_data"

    print(f"Kraken archive : {archive_dir}")
    print(f"Cache data_dir : {data_dir}")
    print(f"Breadth assets : {len(BREADTH_ASSETS)} @ {QUOTE} {resolution}m\n")

    done, skipped, failures = run_all(BREADTH_ASSETS, archive_dir, data_dir,
                                      resolution)

    # Coverage table
    print(f"\n{'asset':6}{'cache_key':22}{'rows':>8}  {'first':16} {'last':16}"
          f"{'miss':>7}{'full%':>8}{'2017+%':>9}")
    for r in done:
        g = r["gaps"]
        f, p = g["full"], g["post"]
        print(f"{r['asset']:6}{r['cache_key']:22}{r['rows']:>8}  "
              f"{str(r['first'])[:16]:16} {str(r['last'])[:16]:16}"
              f"{f['missing']:>7}{f['pct']:>7.2f}%{p['pct']:>8.2f}%")

    # Failures table — loud, on stderr (stdout stays the [OK]/coverage channel).
    if failures:
        print(f"\n{'asset':6}error", file=sys.stderr)
        for asset, exc in failures:
            print(f"{asset:6}{type(exc).__name__}: {exc}", file=sys.stderr)

    print(f"\nIngested {len(done)}/{len(BREADTH_ASSETS)}; skipped "
          f"{skipped or 'none'}; failed {[a for a, _ in failures] or 'none'}. "
          f"Pilot 2017+ BTC benchmark = 0.11%.")

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
