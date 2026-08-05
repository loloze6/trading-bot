"""
Phase 2 Track A — tests for the exchange-qualified cache key and the Kraken
bulk-archive breadth ingestion.

Groups:
  (a) cache_key() behaviour: Binance key reproduced exactly (backward compat),
      Kraken key exchange-qualified, and NO collision between the two for the
      same symbol/timeframe.
  (b) Round-trip integrity of an ingested file: row count, first/last
      timestamps, and column values spot-checked against directly re-reading
      the source Kraken CSV.
  (c) Symbol convention (settled 2026-07-22): the STORE symbol is standard-base
      (`BTCUSD`, not Kraken's altname `XBTUSD`) so a live top-up (i) lands in
      the same cache slot and (ii) normalizes to ccxt's unified `BTC/USD`; the
      SOURCE file is still located via Kraken's altname base.
  (d) Gap-stat arithmetic.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.base_fetcher import FetchGapError  # noqa: E402
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
    assert f.cache_key("BTCUSD") == "kraken_BTCUSD_1h"
    assert Path(f._csv_path("BTCUSD")).name == "kraken_BTCUSD_1h.csv"


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

    # Cache slot is exchange-qualified AND standard-base (BTC, not XBT).
    assert summary["cache_key"] == "kraken_BTCUSD_1h"
    dest = Path(summary["dest"])
    assert dest.name == "kraken_BTCUSD_1h.csv"
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


# ---------------------------------------------------------------------------
# (c) Symbol convention: store standard-base, source Kraken-altname
# ---------------------------------------------------------------------------

def test_store_symbol_is_standard_base_not_kraken_altname():
    """The cache key must use the standard base (BTC/DOGE), never Kraken's
    legacy altname (XBT/XDG) — the load-bearing correction to the pilot."""
    assert ing.cache_symbol("BTC") == "BTCUSD"
    assert ing.cache_symbol("DOGE") == "DOGEUSD"
    assert ing.cache_symbol("ETH") == "ETHUSD"      # unaffected pair unchanged


def test_source_pair_uses_kraken_altname_base():
    """The archive file is located by Kraken's altname base."""
    assert ing.kraken_source_pair("BTC") == "XBTUSD"
    assert ing.kraken_source_pair("DOGE") == "XDGUSD"
    assert ing.kraken_source_pair("ETH") == "ETHUSD"


def _normalize_like_fetch_remote(symbol: str) -> str:
    """Reproduce CcxtFetcher._fetch_remote's compact -> 'BASE/QUOTE' step."""
    if "/" not in symbol and len(symbol) > 3:
        for q in ("USDT", "USD", "BUSD", "USDC", "ETH", "BTC"):
            if symbol.endswith(q):
                return f"{symbol[:-len(q)]}/{q}"
    return symbol


@pytest.mark.parametrize("asset,unified", [
    ("BTC", "BTC/USD"),    # NOT XBT/USD — ccxt would reject the altname form
    ("DOGE", "DOGE/USD"),  # NOT XDG/USD
    ("ETH", "ETH/USD"),
    ("SOL", "SOL/USD"),
])
def test_store_symbol_normalizes_to_ccxt_unified(asset, unified):
    """Top-up composability invariant: the stored symbol, run through the
    fetcher's own normalization, yields ccxt's unified 'BASE/USD' (the only
    form Kraken's adapter accepts) — never a legacy-ticker slash form."""
    assert _normalize_like_fetch_remote(ing.cache_symbol(asset)) == unified


def test_topup_key_matches_archive_slot(tmp_path):
    """A live top-up passing the store symbol resolves to the SAME cache slot
    the archive rows occupy — proved by key derivation, no fetch performed."""
    archive = _fetcher("kraken", str(tmp_path)).cache_key(ing.cache_symbol("BTC"))
    topup = CcxtFetcher(
        start_date="2026-01-01", end_date="2026-07-22",
        symbols=[ing.cache_symbol("BTC")], candle_interval_seconds=3600,
        exchange="kraken", localStorage=True, data_dir=str(tmp_path),
    ).cache_key("BTCUSD")
    assert archive == topup == "kraken_BTCUSD_1h"


# ---------------------------------------------------------------------------
# (e) Merge semantics against an EXISTING cache
#
# `ingest` must hand `_merge_and_store` BOTH frames and pass `existing=`.
# Passing `[converted]` alone with no `existing=` has two consequences, both
# reproduced below:
#   1. the on-disk cache is OVERWRITTEN, not merged, so re-ingesting a narrow
#      tranche over a wide cache destroys rows silently;
#   2. `_assert_no_new_gap` short-circuits when `existing` is None, so the
#      continuity guard is dead at this call site.
# ---------------------------------------------------------------------------

H = 3600
T0 = 1577836800          # 2020-01-01 00:00:00 UTC


def _write_source(archive_dir: Path, asset: str, start_unix: int, periods: int,
                  close: float = 100.0, resolution: int = 60) -> Path:
    """Headerless Kraken bulk CSV: unix_s,open,high,low,close,volume,count."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    path = ing.kraken_source_path(asset, archive_dir, resolution)
    step = resolution * 60
    rows = [f"{start_unix + i * step},{close},{close},{close},{close},1.0,1"
            for i in range(periods)]
    path.write_text("\n".join(rows) + "\n")
    return path


def _seed_cache(data_dir: Path, asset: str, start_unix: int, periods: int,
                close: float = 999.0) -> Path:
    """
    Pre-existing cache in the exact slot `ingest` writes to, built through the
    real schema converter so the columns match byte-for-byte.
    """
    staging = data_dir / "_staging"
    src = _write_source(staging, asset, start_unix, periods, close=close)
    frame = ing.to_binance_schema(ing.load_kraken_ohlcv(src))
    dest = data_dir / f"kraken_{ing.cache_symbol(asset)}_1h.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(dest, index=False)
    return dest


def test_ingest_does_not_truncate_a_wider_existing_cache(tmp_path):
    """
    THE DATA-LOSS BUG. A cache holding 500 hourly bars, re-ingested from a
    10-bar tranche, ended up with 10 rows. The 26 GB master_q4 archive and the
    3-month quarterly bundles occupy the same cache slot, so this is reachable
    by ingesting the wrong bundle once.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _seed_cache(data_dir, "TEST", T0, 500)
    _write_source(archive, "TEST", T0, 10)          # narrow, overlapping tranche

    ing.ingest("TEST", archive, data_dir)

    written = pd.read_csv(data_dir / "kraken_TESTUSD_1h.csv")
    assert len(written) == 500, "pre-existing rows were destroyed by the ingest"


def test_archive_values_win_over_stale_cached_values(tmp_path):
    """
    Ordering pin AND merge-precedence proof. The archive frame goes ahead of
    `existing` in `pieces` (drop_duplicates keeps the first occurrence), so a
    re-ingest can CORRECT a bad cached row; the reverse ordering makes it a
    no-op for every timestamp already cached, which is worse than the overwrite
    it replaces.

    The cache is deliberately WIDER than the archive. Seeding both with the same
    20 timestamps would make the assertion hold identically under plain
    overwrite — it could not tell merge from replace.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _seed_cache(data_dir, "TEST", T0, 100, close=999.0)              # stale, wide
    _write_source(archive, "TEST", T0 + 50 * H, 20, close=111.0)     # authoritative, inside

    ing.ingest("TEST", archive, data_dir)

    written = pd.read_csv(data_dir / "kraken_TESTUSD_1h.csv")
    assert len(written) == 100, "merge lost rows"

    overlap = written.iloc[50:70]["close"]
    rest = pd.concat([written.iloc[:50]["close"], written.iloc[70:]["close"]])
    assert set(overlap) == {111.0}, "archive did not win on the overlapping span"
    assert set(rest) == {999.0}, "non-overlapping cached rows were altered"


def test_ingest_refuses_to_open_a_new_hole_in_a_continuous_cache(tmp_path):
    """
    The continuity guard is DEAD unless `existing=` is passed:
    `_assert_no_new_gap` returns immediately when `existing` is None. Ingesting
    a disjoint tranche over a continuous cache must raise and write nothing.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    dest = _seed_cache(data_dir, "TEST", T0, 100)        # continuous
    before = dest.read_bytes()
    _write_source(archive, "TEST", T0 + 500 * H, 50)     # far-later, disjoint

    with pytest.raises(FetchGapError):
        ing.ingest("TEST", archive, data_dir)

    assert dest.read_bytes() == before, "cache was modified despite the gap guard"


def test_an_out_of_order_source_is_rejected_by_name(tmp_path):
    """
    An interior row out of order clears the first-vs-last span check and is
    invisible to the span-scoped UTC round-trip, so without an explicit
    monotonicity assertion a malformed export ingests silently.
    """
    archive = tmp_path / "archive"
    src = _write_source(archive, "TEST", T0, 10)
    rows = src.read_text().strip().split("\n")
    rows[3], rows[7] = rows[7], rows[3]                  # interior swap
    src.write_text("\n".join(rows) + "\n")

    with pytest.raises(ValueError, match="Out-of-order"):
        ing.load_kraken_ohlcv(src)

    # And through the public entry: the guard is WIRED into ingest(), not
    # merely reachable in the helper.
    with pytest.raises(ValueError, match="Out-of-order"):
        ing.ingest("TEST", archive, tmp_path / "cache")


def test_a_duplicate_timestamp_is_rejected(tmp_path):
    """
    `is_monotonic_increasing` is NON-strict, so a repeated timestamp cleared the
    guard and `drop_duplicates` then kept whichever copy happened to sort first,
    discarding a conflicting value with nothing reported. Two rows claiming the
    same hour with different prices is a malformed export, not a merge decision.
    """
    archive = tmp_path / "archive"
    src = _write_source(archive, "TEST", T0, 4)
    rows = src.read_text().strip().split("\n")
    rows[2] = rows[1].replace("100.0", "555.0")          # same timestamp, other prices
    src.write_text("\n".join(rows) + "\n")

    with pytest.raises(ValueError, match="strictly chronological"):
        ing.load_kraken_ohlcv(src)


def test_reingesting_the_same_archive_is_byte_identical(tmp_path):
    """
    Public-entry idempotency. `_load_local` re-parses only `timestamp`, so
    `close_time` comes back as strings; concatenating that with `converted`'s
    datetime64 column degrades the merged column to object and `to_csv` then
    writes `…:59.999000` where the first write produced `…:59.999`. Re-running
    the ingest would rewrite every archive row of every tracked cache for a
    formatting difference alone.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source(archive, "TEST", T0, 48)
    dest = data_dir / "kraken_TESTUSD_1h.csv"

    ing.ingest("TEST", archive, data_dir)
    first = dest.read_bytes()
    ing.ingest("TEST", archive, data_dir)

    assert dest.read_bytes() == first, "re-ingesting an unchanged archive rewrote the file"


def test_a_cache_that_exists_but_parses_empty_is_refused(tmp_path):
    """
    `_load_local` swallows every read error and returns an empty frame, so an
    unreadable cache is indistinguishable from a fresh slot at this call site —
    and an empty `existing` switches BOTH protections off at once: the union
    degenerates to the archive alone and `_assert_no_new_gap` short-circuits.
    That is precisely the state where a cache most needs them.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    dest = _seed_cache(data_dir, "TEST", T0, 500)
    dest.write_text(dest.read_text() + ",".join(str(i) for i in range(26)) + "\n")
    before = dest.read_bytes()
    _write_source(archive, "TEST", T0, 10)

    with pytest.raises(ValueError, match="parsed to zero rows"):
        ing.ingest("TEST", archive, data_dir)

    assert dest.read_bytes() == before, "the unreadable cache was modified"


def test_first_ingest_with_no_existing_cache_is_unchanged(tmp_path):
    """
    STOP condition: the overwhelmingly common path — a fresh slot — must behave
    exactly as before, including the returned summary.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source(archive, "TEST", T0, 48)

    summary = ing.ingest("TEST", archive, data_dir)

    assert summary["rows"] == 48
    assert summary["first"] == pd.Timestamp("2020-01-01 00:00:00")
    assert summary["last"] == pd.Timestamp("2020-01-02 23:00:00")


def test_utc_roundtrip_survives_a_union_with_a_wider_cache(tmp_path):
    """
    Second-order hazard of the fix: the post-write check re-verifies the ARCHIVE
    against what landed on disk. Once the merge is a real union, the file's
    first/last rows are the CACHE's, not the archive's, so comparing them
    wholesale raises a spurious IngestUTCError. The check must be scoped to the
    archive's own span.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _seed_cache(data_dir, "TEST", T0, 300)
    _write_source(archive, "TEST", T0 + 50 * H, 20)     # strictly inside the cache

    summary = ing.ingest("TEST", archive, data_dir)     # must not raise

    assert summary["rows"] == 300
    # gaps describe the WHOLE merged cache, not the ingested tranche.
    assert summary["gaps"]["full"]["rows"] == 300


def _shift_the_write(monkeypatch, hours: int = 1) -> None:
    """
    Corrupt what actually lands on disk: every frame written through
    `DataFrame.to_csv` gets its timestamps shifted. This models "UTC did not
    survive the write" — the precise defect verify_utc_roundtrip's docstring
    names as its STOP condition — without touching the code under test.
    """
    original = pd.DataFrame.to_csv

    def patched(self, *args, **kwargs):
        if "timestamp" in getattr(self, "columns", []):
            shifted = self.copy()
            shifted["timestamp"] = (pd.to_datetime(shifted["timestamp"])
                                    + pd.Timedelta(hours=hours))
            return original(shifted, *args, **kwargs)
        return original(self, *args, **kwargs)

    monkeypatch.setattr(pd.DataFrame, "to_csv", patched)


def test_a_shifted_write_is_caught_at_the_archive_boundary(tmp_path, monkeypatch):
    """
    The timestamp round-trip alone is geometrically INERT in this geometry. The
    span mask is built from `converted`'s own bounds, so archive_span's boundary
    rows carry those two timestamps by construction whenever the cache already
    covers them — a neighbouring CACHE row satisfies the comparison no matter
    what the write did, and a whole-cache shift lands silently.

    Comparing the boundary rows' VALUES is what makes the check live: the
    archive wins duplicate timestamps, so on a healthy write the row sitting at
    each boundary is the archive's own. Per-row-distinct closes so a shift by
    one bar cannot coincidentally match.
    """
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _seed_cache(data_dir, "TEST", T0, 300, close=999.0)      # brackets the archive
    archive.mkdir(parents=True, exist_ok=True)
    ing.kraken_source_path("TEST", archive, 60).write_text("\n".join(
        f"{T0 + (50 + i) * H},{111.0 + i},{111.0 + i},{111.0 + i},{111.0 + i},1.0,1"
        for i in range(20)) + "\n")

    _shift_the_write(monkeypatch, hours=1)

    with pytest.raises(ing.IngestUTCError, match="boundary"):
        ing.ingest("TEST", archive, data_dir)


# ---------------------------------------------------------------------------
# (d) Gap-stat arithmetic
# ---------------------------------------------------------------------------

def test_compute_gap_stats_counts_missing_hours():
    """Deterministic series with a known hole -> exact missing count/%."""
    # 10 contiguous hourly bars, then drop 3 (a 3-hour gap), keep 10 after.
    full = pd.date_range("2020-01-01", periods=23, freq="h")
    kept = full.delete([10, 11, 12])                 # remove 3 interior bars
    stats = ing.compute_gap_stats(pd.Series(kept), resolution=60)
    assert stats["full"]["rows"] == 20
    assert stats["full"]["expected"] == 23           # span 22h /1h + 1
    assert stats["full"]["missing"] == 3
    assert stats["full"]["pct"] == pytest.approx(100 * 3 / 23)


def test_compute_gap_stats_perfect_series_zero_missing():
    ts = pd.Series(pd.date_range("2021-06-01", periods=500, freq="h"))
    stats = ing.compute_gap_stats(ts, resolution=60)
    assert stats["full"]["missing"] == 0
    assert stats["full"]["pct"] == 0.0
