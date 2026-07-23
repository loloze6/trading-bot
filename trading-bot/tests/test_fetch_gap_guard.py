"""
Write-boundary gap guard (2026-07-23).

Defect: Kraken's public OHLC endpoint serves a fixed rolling ~720-candle window
and ignores `since`. Requesting 2026-01-01 onward against a cache ending
2025-12-31 23:00 returns only 2026-06-22 23:00 -> 2026-07-22 23:00.
`_fetch_remote`'s `if not candles: break` exits cleanly, the merge is written,
and the run logs success — leaving a 4,151-bar hole nothing reports.

These tests use FIXTURES, never a live call: the failure shape is reproduced by
handing the fetcher a chunk that starts after the requested `since`.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.base_fetcher import BaseFetcher, FetchGapError  # noqa: E402

HOUR = 3600


def _bars(start: str, periods: int, freq: str = "1h") -> pd.DataFrame:
    """OHLCV-shaped frame; only `timestamp` matters to the guard."""
    ts = pd.date_range(start=start, periods=periods, freq=freq)
    return pd.DataFrame({
        "timestamp": ts,
        "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0,
    })


class _StubFetcher(BaseFetcher):
    """Minimal concrete BaseFetcher. _fetch_remote is never called by these
    tests — the guard is exercised through _merge_and_store directly, which is
    the write boundary the fix lives at."""

    def __init__(self, tmp_dir, interval_seconds=HOUR):
        super().__init__(
            start_date="2025-01-01", end_date="2026-12-31",
            symbols=["BTCUSD"], interval_seconds=interval_seconds,
            localStorage=True, data_dir=str(tmp_dir),
        )

    def _fetch_remote(self, symbol, start, end):  # pragma: no cover
        raise AssertionError("no live fetch in these tests")

    def cache_key(self, symbol):
        return f"kraken_{symbol}_1h"


# ---------------------------------------------------------------------------
# The real failure shape
# ---------------------------------------------------------------------------

def test_rolling_window_fetch_raises_and_writes_nothing(tmp_path):
    """The Kraken shape, to scale: archive ends 2025-12-31 23:00, the endpoint
    returns a window opening 2026-06-22 23:00. Must raise, not write."""
    f = _StubFetcher(tmp_path)
    existing = _bars("2025-12-01 00:00", 744)          # ... -> 2025-12-31 23:00
    chunk = _bars("2026-06-22 23:00", 721)             # the rolling window

    assert existing["timestamp"].iloc[-1] == pd.Timestamp("2025-12-31 23:00")

    with pytest.raises(FetchGapError) as exc:
        f._merge_and_store("BTCUSD", [existing, chunk], save=True, existing=existing)

    msg = str(exc.value)
    assert "2026-01-01 00:00:00" in msg      # names the missing span
    assert "2026-06-22 22:00:00" in msg
    assert "4151 bars" in msg                 # and its size
    assert "NOTHING was written" in msg

    # No trace in memory or on disk.
    assert not (tmp_path / "kraken_BTCUSD_1h.csv").exists()
    assert f.data_cache.get("BTCUSD") is None or f.data_cache["BTCUSD"].empty


def test_gap_size_reported_matches_the_measured_seam(tmp_path):
    """4,151 bars is the figure recorded in ledger G1 item 2; the guard must
    derive it independently rather than restate a constant."""
    f = _StubFetcher(tmp_path)
    existing = _bars("2025-12-31 23:00", 1)
    chunk = _bars("2026-06-22 23:00", 1)
    gaps = f._gap_intervals(pd.concat([existing, chunk])["timestamp"])
    assert len(gaps) == 1
    start, end = gaps[0]
    assert start == pd.Timestamp("2026-01-01 00:00")
    assert end == pd.Timestamp("2026-06-22 22:00")
    assert int((end - start) / pd.Timedelta(hours=1)) + 1 == 4151


# ---------------------------------------------------------------------------
# The case the guard must NOT block
# ---------------------------------------------------------------------------

def test_contiguous_top_up_still_writes(tmp_path):
    """STOP condition: the guard must not block a legitimate contiguous
    top-up — the case it exists to protect."""
    f = _StubFetcher(tmp_path)
    existing = _bars("2026-01-01 00:00", 100)          # ... -> 2026-01-05 03:00
    chunk = _bars("2026-01-05 04:00", 50)              # picks up exactly next bar

    f._merge_and_store("BTCUSD", [existing, chunk], save=True, existing=existing)

    path = tmp_path / "kraken_BTCUSD_1h.csv"
    assert path.exists()
    written = pd.read_csv(path)
    assert len(written) == 150
    assert pd.to_datetime(written["timestamp"]).is_monotonic_increasing


def test_preexisting_natural_gaps_do_not_block_a_write(tmp_path):
    """Archive caches carry real missing bars (INJ ~5.7%, DOGE ~5.1%). An
    absolute no-gaps rule would reject every cache the campaign depends on —
    the guard is differential, so these must pass through untouched."""
    f = _StubFetcher(tmp_path)
    head = _bars("2026-01-01 00:00", 50)
    tail = _bars("2026-01-10 00:00", 50)               # a large pre-existing hole
    existing = pd.concat([head, tail], ignore_index=True)
    chunk = _bars("2026-01-12 02:00", 24)              # contiguous with tail's end

    f._merge_and_store("BTCUSD", [existing, chunk], save=True, existing=existing)
    assert (tmp_path / "kraken_BTCUSD_1h.csv").exists()


def test_partially_filling_an_existing_gap_is_allowed(tmp_path):
    """A fetch that shrinks a pre-existing hole is an improvement. Containment,
    not equality, is why this passes."""
    f = _StubFetcher(tmp_path)
    head = _bars("2026-01-01 00:00", 24)               # -> 2026-01-01 23:00
    tail = _bars("2026-01-05 00:00", 24)
    existing = pd.concat([head, tail], ignore_index=True)
    fill = _bars("2026-01-02 00:00", 24)               # fills one day of the hole

    f._merge_and_store("BTCUSD", [existing, fill], save=True, existing=existing)
    assert (tmp_path / "kraken_BTCUSD_1h.csv").exists()


def test_first_fetch_with_no_existing_cache_is_not_guarded(tmp_path):
    """A late-listed asset legitimately returns data starting partway into the
    requested window. With no prior data there is no continuity to break."""
    f = _StubFetcher(tmp_path)
    chunk = _bars("2026-03-01 00:00", 100)
    f._merge_and_store("BTCUSD", [chunk], save=True, existing=pd.DataFrame())
    assert (tmp_path / "kraken_BTCUSD_1h.csv").exists()


# ---------------------------------------------------------------------------
# Existing caches must remain loadable and byte-identical
# ---------------------------------------------------------------------------

def test_real_archive_cache_still_loads_unchanged(tmp_path):
    """STOP condition: no archive-ingested cache may change. Loads a real
    on-disk Kraken cache read-only and confirms the guard does not reject it.
    Coverage metadata only — no prices or returns are computed."""
    cache = PROJECT_ROOT / "local_data" / "kraken_BTCUSD_1h.csv"
    if not cache.exists():
        pytest.skip("kraken_BTCUSD_1h.csv not present")

    before = cache.read_bytes()
    df = pd.read_csv(cache)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    f = _StubFetcher(tmp_path)
    # Re-storing the archive against itself introduces no NEW gap, however many
    # natural ones it already contains.
    f._merge_and_store("BTCUSD", [df], save=False, existing=df)
    assert len(f.data_cache["BTCUSD"]) == len(df)

    assert cache.read_bytes() == before, "archive cache was modified"
