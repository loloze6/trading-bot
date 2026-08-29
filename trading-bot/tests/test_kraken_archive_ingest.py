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

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.base_fetcher import FetchGapError  # noqa: E402
from data.fetchers.ccxt_fetcher import CcxtFetcher  # noqa: E402
from tools import ingest_kraken_archive as ing  # noqa: E402

ARCHIVE_DIR = PROJECT_ROOT / "local_data" / "Kraken_batch" / "master_q4"

# One representative pilot pair for the round-trip test.
PILOT_ASSET = "BTC"
PILOT_SOURCE = ing.kraken_source_path(PILOT_ASSET, ARCHIVE_DIR)


def _fetcher(exchange: str, data_dir: str) -> CcxtFetcher:
    return CcxtFetcher(
        start_date="2020-01-01",
        end_date="2020-01-02",
        symbols=["BTCUSDT"],
        candle_interval_seconds=3600,  # -> "1h"
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
    exp_first = _dt.datetime.fromtimestamp(int(raw["unix_s"].iloc[0]), _utc).replace(
        tzinfo=None
    )
    exp_last = _dt.datetime.fromtimestamp(int(raw["unix_s"].iloc[-1]), _utc).replace(
        tzinfo=None
    )
    assert got["timestamp"].iloc[0].to_pydatetime() == exp_first
    assert got["timestamp"].iloc[-1].to_pydatetime() == exp_last

    # Column-value spot checks against the source (first and last rows).
    for pos in (0, -1):
        for col in ("open", "high", "low", "close", "volume"):
            assert got[col].iloc[pos] == pytest.approx(raw[col].iloc[pos]), (col, pos)
        # number_of_trades carries Kraken's real per-candle count.
        assert int(got["number_of_trades"].iloc[pos]) == int(
            raw["trade_count"].iloc[pos]
        )
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
    raw = pd.read_csv(PILOT_SOURCE, header=None, names=ing.KRAKEN_RAW_COLUMNS).head(10)
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
    assert ing.cache_symbol("ETH") == "ETHUSD"  # unaffected pair unchanged


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
                return f"{symbol[: -len(q)]}/{q}"
    return symbol


@pytest.mark.parametrize(
    "asset,unified",
    [
        ("BTC", "BTC/USD"),  # NOT XBT/USD — ccxt would reject the altname form
        ("DOGE", "DOGE/USD"),  # NOT XDG/USD
        ("ETH", "ETH/USD"),
        ("SOL", "SOL/USD"),
    ],
)
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
        start_date="2026-01-01",
        end_date="2026-07-22",
        symbols=[ing.cache_symbol("BTC")],
        candle_interval_seconds=3600,
        exchange="kraken",
        localStorage=True,
        data_dir=str(tmp_path),
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
T0 = 1577836800  # 2020-01-01 00:00:00 UTC


def _write_source(
    archive_dir: Path,
    asset: str,
    start_unix: int,
    periods: int,
    close: float = 100.0,
    resolution: int = 60,
) -> Path:
    """Headerless Kraken bulk CSV: unix_s,open,high,low,close,volume,count."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    path = ing.kraken_source_path(asset, archive_dir, resolution)
    step = resolution * 60
    rows = [
        f"{start_unix + i * step},{close},{close},{close},{close},1.0,1"
        for i in range(periods)
    ]
    path.write_text("\n".join(rows) + "\n")
    return path


def _seed_cache(
    data_dir: Path, asset: str, start_unix: int, periods: int, close: float = 999.0
) -> Path:
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
    _write_source(archive, "TEST", T0, 10)  # narrow, overlapping tranche

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
    _seed_cache(data_dir, "TEST", T0, 100, close=999.0)  # stale, wide
    _write_source(
        archive, "TEST", T0 + 50 * H, 20, close=111.0
    )  # authoritative, inside

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
    dest = _seed_cache(data_dir, "TEST", T0, 100)  # continuous
    before = dest.read_bytes()
    _write_source(archive, "TEST", T0 + 500 * H, 50)  # far-later, disjoint

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
    rows[3], rows[7] = rows[7], rows[3]  # interior swap
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
    rows[2] = rows[1].replace("100.0", "555.0")  # same timestamp, other prices
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

    assert dest.read_bytes() == first, (
        "re-ingesting an unchanged archive rewrote the file"
    )


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
    _write_source(archive, "TEST", T0 + 50 * H, 20)  # strictly inside the cache

    summary = ing.ingest("TEST", archive, data_dir)  # must not raise

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
            shifted["timestamp"] = pd.to_datetime(shifted["timestamp"]) + pd.Timedelta(
                hours=hours
            )
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
    _seed_cache(data_dir, "TEST", T0, 300, close=999.0)  # brackets the archive
    archive.mkdir(parents=True, exist_ok=True)
    ing.kraken_source_path("TEST", archive, 60).write_text(
        "\n".join(
            f"{T0 + (50 + i) * H},{111.0 + i},{111.0 + i},{111.0 + i},{111.0 + i},1.0,1"
            for i in range(20)
        )
        + "\n"
    )

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
    kept = full.delete([10, 11, 12])  # remove 3 interior bars
    stats = ing.compute_gap_stats(pd.Series(kept), resolution=60)
    assert stats["full"]["rows"] == 20
    assert stats["full"]["expected"] == 23  # span 22h /1h + 1
    assert stats["full"]["missing"] == 3
    assert stats["full"]["pct"] == pytest.approx(100 * 3 / 23)


def test_compute_gap_stats_perfect_series_zero_missing():
    ts = pd.Series(pd.date_range("2021-06-01", periods=500, freq="h"))
    stats = ing.compute_gap_stats(ts, resolution=60)
    assert stats["full"]["missing"] == 0
    assert stats["full"]["pct"] == 0.0


# ---------------------------------------------------------------------------
# (f) Daily (1440-minute) resolution
#
# to_binance_schema derived close_time from the module-level 1h TIMEFRAME_MS
# regardless of the requested resolution, so a daily tranche was written with
# 1-HOUR close_times, silently. close_time now follows the passed resolution.
# ---------------------------------------------------------------------------


def test_to_binance_schema_daily_close_time_geometry(tmp_path):
    """A daily (1440-minute) tranche carries a full-day close_time:
    timestamp + 86,399,999 ms (= 1440*60*1000 - 1), not the 1h default."""
    src = _write_source(tmp_path, "TEST", T0, 5, resolution=1440)
    raw = ing.load_kraken_ohlcv(src)
    got = ing.to_binance_schema(raw, 1440)
    delta = got["close_time"].apply(pd.Timestamp) - got["timestamp"]
    assert (delta == pd.Timedelta(milliseconds=86_399_999)).all()


def test_to_binance_schema_default_resolution_stays_hourly(tmp_path):
    """Byte-identity pin: a no-arg call keeps the 1h close_time geometry —
    timestamp + 3,599,999 ms. Guards the default against a silent flip."""
    src = _write_source(tmp_path, "TEST", T0, 5, resolution=60)
    raw = ing.load_kraken_ohlcv(src)
    got = ing.to_binance_schema(raw)
    delta = got["close_time"].apply(pd.Timestamp) - got["timestamp"]
    assert (delta == pd.Timedelta(milliseconds=3_599_999)).all()


def test_ingest_at_daily_resolution_writes_1d_cache_and_is_idempotent(tmp_path):
    """End-to-end daily ingest through the real cache_key: the file lands in the
    1d slot, carries full-day close_times on disk, and re-running is a
    byte-identical no-op (the same idempotency the 1h path guarantees)."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source(archive, "TEST", T0, 30, resolution=1440)

    summary = ing.ingest("TEST", archive, data_dir, 1440)

    assert summary["cache_key"] == "kraken_TESTUSD_1d"
    dest = Path(summary["dest"])
    assert dest.name == "kraken_TESTUSD_1d.csv"

    got = pd.read_csv(dest)
    got["timestamp"] = pd.to_datetime(got["timestamp"])
    delta = got["close_time"].apply(pd.Timestamp) - got["timestamp"]
    assert (delta == pd.Timedelta(milliseconds=86_399_999)).all()

    first = dest.read_bytes()
    ing.ingest("TEST", archive, data_dir, 1440)
    assert dest.read_bytes() == first, (
        "re-ingesting an unchanged daily archive rewrote the file"
    )


# ---------------------------------------------------------------------------
# (g) Per-asset isolation
#
# One raising asset used to abort every asset after it. run_all now catches per
# asset, records (asset, error), continues, and reports a non-empty failures
# list that main() turns into a non-zero exit.
# ---------------------------------------------------------------------------


def test_run_all_isolates_a_failing_asset_and_continues(tmp_path, capsys):
    """A raising asset does not abort the rest, AND the failure is attributed to
    the failing asset — not to assets[0]. BAD sits BETWEEN two healthy assets so
    both invariants are load-bearing: 'continued past the failure' (GOOD2 after
    BAD) and 'recorded the failing asset, not the first' (assets[0] is GOOD1).
    The [SKIP]-on-absent path is separate and covered by its own test."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"

    _write_source(archive, "GOOD1", T0, 48)

    # BAD: interior out-of-order row -> load_kraken_ohlcv raises inside ingest.
    bad = _write_source(archive, "BAD", T0, 10)
    rows = bad.read_text().strip().split("\n")
    rows[3], rows[7] = rows[7], rows[3]
    bad.write_text("\n".join(rows) + "\n")

    _write_source(archive, "GOOD2", T0, 48)

    done, skipped, failures = ing.run_all(["GOOD1", "BAD", "GOOD2"], archive, data_dir)

    assert [r["asset"] for r in done] == ["GOOD1", "GOOD2"]  # continued past BAD
    assert skipped == []
    assert len(failures) == 1
    assert failures[0][0] == "BAD"  # attributed to BAD, not GOOD1
    assert isinstance(failures[0][1], ValueError)  # the REAL exception is kept
    assert (data_dir / "kraken_GOOD1USD_1h.csv").exists()
    assert (data_dir / "kraken_GOOD2USD_1h.csv").exists()

    # Loud on STDERR, and it names the failing asset (not the first one).
    err = capsys.readouterr().err
    assert "[FAIL] BAD" in err
    assert "[FAIL] GOOD1" not in err


def test_run_all_skips_absent_source_without_recording_failure(tmp_path):
    """The [SKIP]-on-absent-source branch (never hit by the isolation test,
    whose files all exist): an absent source is skipped, NOT recorded as a
    failure. Absence is expected (HYPE); a raise is not."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source(archive, "GOOD", T0, 48)  # MISSING has no source file

    done, skipped, failures = ing.run_all(["MISSING", "GOOD"], archive, data_dir)

    assert skipped == ["MISSING"]
    assert [r["asset"] for r in done] == ["GOOD"]
    assert failures == []  # absence is not a failure


def test_run_all_source_lookup_follows_the_requested_resolution(tmp_path):
    """run_all must locate the source at the REQUESTED resolution: an archive
    holding only a _1440 file is ingested at 1440, not skipped as absent (which
    is what dropping `resolution` from the source lookup would cause)."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source(archive, "TEST", T0, 30, resolution=1440)  # only _1440 exists

    done, skipped, failures = ing.run_all(["TEST"], archive, data_dir, 1440)

    assert [r["asset"] for r in done] == ["TEST"]
    assert skipped == []
    assert failures == []
    assert (data_dir / "kraken_TESTUSD_1d.csv").exists()


def test_main_exits_nonzero_when_any_asset_failed(monkeypatch, capsys):
    """A recorded failure makes the whole run exit non-zero AND the FAILURES
    table names the failing asset on STDERR. run_all is stubbed so no real
    local_data is read or written."""
    monkeypatch.setattr(sys, "argv", ["ingest_kraken_archive.py"])
    monkeypatch.setattr(
        ing,
        "run_all",
        lambda *a, **k: ([], [], [("BAD", RuntimeError("boom"))]),
    )
    with pytest.raises(SystemExit) as excinfo:
        ing.main()
    assert excinfo.value.code == 1
    err = capsys.readouterr().err
    assert "BAD" in err  # the FAILURES table names it


# ---------------------------------------------------------------------------
# (h) Resolution validation — an unmapped resolution is a STOP, not a mis-file
#
# CcxtFetcher snaps candle_interval to the NEAREST ccxt timeframe, so 720m (12h)
# would land in the 4h slot and merge 12h bars into a legitimate 4h cache; 0 and
# negatives produce degenerate close_time spans. ingest() refuses before any
# read or write.
# ---------------------------------------------------------------------------


def _write_source_at_suffix(
    archive: Path,
    asset: str,
    suffix: int,
    start_unix: int,
    periods: int,
    step_seconds: int = H,
) -> Path:
    """A monotonic (step_seconds-spaced) source written under an ARBITRARY file
    suffix, decoupling the on-disk spacing from the resolution ingest() is told.
    Lets a degenerate resolution reach the value-level code pre-fix instead of
    tripping the missing-file guard."""
    archive.mkdir(parents=True, exist_ok=True)
    path = ing.kraken_source_path(asset, archive, suffix)
    rows = [
        f"{start_unix + i * step_seconds},100.0,100.0,100.0,100.0,1.0,1"
        for i in range(periods)
    ]
    path.write_text("\n".join(rows) + "\n")
    return path


def test_ingest_720_snaps_to_the_4h_slot_and_is_rejected(tmp_path):
    """720m (12h) has no exact ccxt timeframe — it snaps to 4h. A _720 source is
    present, so pre-guard this silently wrote 12h bars into kraken_TESTUSD_4h.
    ingest() now refuses, naming the 4h slot, and writes nothing."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source(archive, "TEST", T0, 10, resolution=720)  # _720 source exists

    with pytest.raises(ValueError, match="4h"):
        ing.ingest("TEST", archive, data_dir, 720)

    assert not data_dir.exists()  # nothing written


def test_ingest_rejects_zero_resolution(tmp_path):
    """0 snaps to 1m and (pre-guard) divided by a zero step in the gap stats
    AFTER writing. The guard stops it before any write."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source_at_suffix(archive, "TEST", 0, T0, 10)  # monotonic _0 source

    with pytest.raises(ValueError):
        ing.ingest("TEST", archive, data_dir, 0)

    assert not data_dir.exists()


def test_ingest_rejects_negative_resolution(tmp_path):
    """-60 snaps to 1m and (pre-guard) wrote a NEGATIVE close_time span silently.
    The guard stops it before any write."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source_at_suffix(archive, "TEST", -60, T0, 10)  # monotonic _-60 source

    with pytest.raises(ValueError):
        ing.ingest("TEST", archive, data_dir, -60)

    assert not data_dir.exists()


def test_ingest_accepts_an_exactly_mapped_4h_resolution(tmp_path):
    """240m maps EXACTLY to 4h and must NOT be rejected by the guard — it lands
    in the legitimate kraken_TESTUSD_4h slot."""
    data_dir = tmp_path / "cache"
    archive = tmp_path / "archive"
    _write_source(archive, "TEST", T0, 30, resolution=240)

    summary = ing.ingest("TEST", archive, data_dir, 240)

    assert summary["cache_key"] == "kraken_TESTUSD_4h"


def test_to_binance_schema_4h_close_time_geometry(tmp_path):
    """A third geometry point (240-minute / 4h) so a close_time hardcoded to the
    {60, 1440} test set cannot survive: +14,399,999 ms (= 240*60*1000 - 1)."""
    src = _write_source(tmp_path, "TEST", T0, 5, resolution=240)
    raw = ing.load_kraken_ohlcv(src)
    got = ing.to_binance_schema(raw, 240)
    delta = got["close_time"].apply(pd.Timestamp) - got["timestamp"]
    assert (delta == pd.Timedelta(milliseconds=14_399_999)).all()


# ---------------------------------------------------------------------------
# Seal guard on the WRITE path (2026-08-19)
# ---------------------------------------------------------------------------
# Every other holdout control in the tree guards reading or committing. This
# path writes into a tracked cache, which is the one direction none of them
# cover: a future bulk tranche extending past 2025-12-31 would have landed
# sealed candles in the store with nothing objecting.

_SEAL = int(pd.Timestamp("2026-01-01").timestamp())


def test_ingest_refuses_a_tranche_carrying_sealed_rows(tmp_path):
    archive, data = tmp_path / "arch", tmp_path / "data"
    # Straddles the seal: 2 bars before, 2 at/after.
    _write_source(archive, "TEST", _SEAL - 2 * 3600, 4)

    with pytest.raises(ValueError, match="holdout seal"):
        ing.ingest("TEST", archive, data)


def test_a_refused_tranche_writes_nothing(tmp_path):
    """'NOTHING was written' has to be literally true.

    A guard that raises after the store has been touched leaves sealed rows on
    disk and only *reports* refusing -- worse than no guard, because the
    message says the opposite of what happened.
    """
    archive, data = tmp_path / "arch", tmp_path / "data"
    _write_source(archive, "TEST", _SEAL - 2 * 3600, 4)

    with pytest.raises(ValueError, match="holdout seal"):
        ing.ingest("TEST", archive, data)

    written = list(data.rglob("*.csv")) if data.exists() else []
    assert written == [], f"refused ingest still wrote {written}"


def test_ingest_still_accepts_a_wholly_pre_seal_tranche(tmp_path):
    """Control: the guard must not block legitimate history.

    Without this, a guard that simply refused everything would pass the two
    tests above.
    """
    archive, data = tmp_path / "arch", tmp_path / "data"
    _write_source(archive, "TEST", _SEAL - 10 * 3600, 5)  # all pre-seal

    summary = ing.ingest("TEST", archive, data)

    # `ingest()` returns "rows" -- the first version of this asserted on
    # "rows_written" behind an `if key in summary` guard, which made the whole
    # line `assert True`.
    assert summary["rows"] > 0
    assert list(data.rglob("*.csv")), "a legitimate pre-seal tranche was not written"


def test_seal_boundary_is_read_from_policy_not_hardcoded(tmp_path, monkeypatch):
    """The seal must move with campaign_data_policy.yaml.

    Pinned because a hardcoded 2026-01-01 would keep passing every test above
    while silently ignoring a policy change -- the exact 'correct-looking banner
    over a stale check' shape flagged for holdout_date_gate.sh's PATTERN.
    """
    policy = tmp_path / "campaign_data_policy.yaml"
    policy.write_text("holdout_range: ['2025-06-01', '2025-12-31']\n", encoding="utf-8")
    monkeypatch.setattr(ing, "_POLICY_PATH", policy)

    assert ing._holdout_bounds()[0] == pd.Timestamp("2025-06-01")

    archive, data = tmp_path / "arch", tmp_path / "data"
    # Pre-2026 but past the RELOCATED seal -> must now be refused.
    _write_source(archive, "TEST", int(pd.Timestamp("2025-06-02").timestamp()), 3)
    with pytest.raises(ValueError, match="holdout seal"):
        ing.ingest("TEST", archive, data)


def test_unreadable_policy_refuses_rather_than_defaulting(tmp_path, monkeypatch):
    """Deny by default: an ingest that cannot locate the seal must not write."""
    monkeypatch.setattr(ing, "_POLICY_PATH", tmp_path / "does_not_exist.yaml")

    archive, data = tmp_path / "arch", tmp_path / "data"
    _write_source(archive, "TEST", _SEAL - 10 * 3600, 5)  # otherwise legitimate

    with pytest.raises(RuntimeError, match="Cannot read holdout_range"):
        ing.ingest("TEST", archive, data)
