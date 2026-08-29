"""
Write-boundary END guard (2026-07-28).

Defect, measured not theoretical: `CcxtFetcher` overshoots its own `end_date`.
`ccxt_fetcher.py:149-174` loops `while current_since < until`, so the bound
governs where a page *starts*, never where the data *ends*; each page returns up
to 1000 candles and the frame is never trimmed. A fetch of `BTCUSDT_1d` bounded
at 2025-12-31 wrote daily bars through 2026-03-19 — straight across the sealed
holdout. Bounding a request is not a bound on the response.

`_load_all` already trims the IN-MEMORY frame to the requested window, which is
why the defect was invisible for so long: every consumer saw correct data while
the CSV on disk carried the overshoot, and the next process to read that cache
inherited it.

The fix belongs in `BaseFetcher._load_all`, not in `CcxtFetcher`: the contract is
that a fetcher MAY return more than it was asked for, and the orchestrator trims
each chunk to its requested period before merging. One edit covers every fetcher.

These tests use FIXTURES, never a live call — the overshoot is reproduced by a
stub whose `_fetch_remote` ignores `end`, exactly as the real one does.
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.base_fetcher import BaseFetcher  # noqa: E402

HOUR = 3600


def _bars(start, periods: int, freq: str = "1h") -> pd.DataFrame:
    """OHLCV-shaped frame; only `timestamp` matters to the guard."""
    ts = pd.date_range(start=start, periods=periods, freq=freq)
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": 1.0,
            "high": 1.0,
            "low": 1.0,
            "close": 1.0,
            "volume": 1.0,
        }
    )


class _OvershootingFetcher(BaseFetcher):
    """
    CcxtFetcher's real shape: `_fetch_remote` honours `start` and ignores `end`,
    returning a whole page. `page` is 1000 to match the exchange page size that
    produced the measured 2026-03-19 overshoot.
    """

    def __init__(self, tmp_dir, start, end, page: int = 1000, interval_seconds=HOUR):
        super().__init__(
            start_date=start,
            end_date=end,
            symbols=["BTCUSDT"],
            interval_seconds=interval_seconds,
            localStorage=True,
            data_dir=str(tmp_dir),
        )
        self.page = page
        self.requested_periods = []

    def _fetch_remote(self, symbol, start, end):
        self.requested_periods.append((start, end))
        return _bars(start, self.page)

    def cache_key(self, symbol):
        return f"{symbol}_1h"


def _written(tmp_path) -> pd.DataFrame:
    df = pd.read_csv(tmp_path / "BTCUSDT_1h.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


# ---------------------------------------------------------------------------
# The real failure shape
# ---------------------------------------------------------------------------


def test_overshooting_chunk_is_not_written_past_the_requested_end(tmp_path):
    """
    The measured defect, to scale. A 1000-bar page opened at 2025-12-01 runs to
    2026-01-11 15:00 — 259 hourly bars inside the sealed holdout. The CSV must
    stop at the requested end, not at wherever the page happened to land.
    """
    f = _OvershootingFetcher(tmp_path, "2025-12-01", "2025-12-31")
    f.get_data()

    written = _written(tmp_path)
    assert written["timestamp"].max() == pd.Timestamp("2025-12-31 23:00")
    assert not (written["timestamp"] >= pd.Timestamp("2026-01-01")).any(), "holdout rows reached disk"


def test_in_memory_frame_matches_what_was_written(tmp_path):
    """
    The defect hid because memory and disk disagreed: `_load_all` trimmed the
    frame it returned while `_merge_and_store` wrote the untrimmed one. They must
    agree, or the next process to read the cache inherits what this one rejected.
    """
    f = _OvershootingFetcher(tmp_path, "2025-12-01", "2025-12-31")
    got = f.get_data("BTCUSDT")

    assert got["timestamp"].max() == _written(tmp_path)["timestamp"].max()


# ---------------------------------------------------------------------------
# The `+1 day` window filter — same bug class, a different line
# ---------------------------------------------------------------------------


def test_end_date_carrying_a_time_does_not_admit_the_following_day(tmp_path):
    """
    `_load_all`'s in-memory filter is `timestamp < end_date + 1 day`. That is
    correct for a date-only end (inclusive of the whole day) but for an end of
    2025-12-31 23:00 it admits bars through 2026-01-01 22:00 — 23 sealed bars,
    in memory, past a bound the caller stated explicitly.
    """
    f = _OvershootingFetcher(tmp_path, "2025-12-01 00:00", "2025-12-31 23:00")
    got = f.get_data("BTCUSDT")

    assert got["timestamp"].max() == pd.Timestamp("2025-12-31 23:00")
    assert _written(tmp_path)["timestamp"].max() == pd.Timestamp("2025-12-31 23:00")


def test_a_complete_cache_is_still_bounded_by_the_window(tmp_path):
    """
    The path where `_inclusive_end` is the ONLY thing acting: the cache already
    covers the window, so `missing == []`, no chunk is fetched and no trim runs.
    Red-team B1 — without this, reverting the window filter to
    `< end_date + 1 day` leaves every test in this file green while the returned
    frame runs a full day past the bound the caller stated.
    """
    seed = _bars("2025-06-01", 40 * 24)  # -> 2025-07-10 23:00
    seed.to_csv(tmp_path / "BTCUSDT_1h.csv", index=False)

    f = _OvershootingFetcher(tmp_path, "2025-06-01", "2025-06-30 23:00")
    got = f.get_data("BTCUSDT")

    assert f.requested_periods == [], "cache was complete; nothing should be fetched"
    assert got["timestamp"].max() == pd.Timestamp("2025-06-30 23:00")


def test_a_computed_period_end_on_midnight_is_not_widened_by_a_day(tmp_path):
    """
    Red-team C1. `_identify_missing_periods` computes gap ends as `ts - 1ms`
    (base_fetcher.py), so a cached row at HH:00:00.001 yields a period end at
    exactly midnight. Treating that computed end as "date-only" and extending it
    to 23:59:59.999 widens the fetch by a full day.

    The trigger shape is live in shipped data: BTCUSDT_funding_8h.csv carries 244
    rows at 00:00:00.001. Only the CALLER's end_date means "through that whole
    day"; an end the code derived means exactly what it says.
    """
    eight_h = 8 * 3600
    seed = _bars("2025-03-05 00:00:00.001", 3, freq="8h")
    seed.to_csv(tmp_path / "BTCUSDT_1h.csv", index=False)

    f = _OvershootingFetcher(tmp_path, "2025-03-01", "2025-03-05", page=40, interval_seconds=eight_h)
    f._fetch_remote = lambda symbol, start, end: f.requested_periods.append((start, end)) or _bars(start, 40, freq="8h")
    f.get_data()

    written = set(_written(tmp_path)["timestamp"])
    # Exactly the prepend gap — the sub-interval remainder after the last
    # cached bar (16:00:00.001 -> 23:59:59.999, no whole 8h bar fits) must not
    # be scheduled as a second, phantom period.
    assert len(f.requested_periods) == 1
    _, pe = f.requested_periods[0]
    assert pd.Timestamp(pe) == pd.Timestamp("2025-03-05 00:00:00")

    assert pd.Timestamp("2025-03-05 08:00:00") not in written, (
        "chunk kept rows past its computed period end — bound widened to end-of-day"
    )


def test_date_only_end_stays_inclusive_of_that_whole_day(tmp_path):
    """
    STOP condition on the fix above: `end_date='2025-12-31'` must keep meaning
    "through 2025-12-31 23:00", as it does today and as every caller in the repo
    relies on (launcher passes date-only strings; the Kraken caches all end
    2025-12-31 23:00). Tightening to midnight would silently drop 23 bars from
    every window in the codebase.
    """
    f = _OvershootingFetcher(tmp_path, "2025-12-01", "2025-12-31")
    got = f.get_data("BTCUSDT")

    assert got["timestamp"].max() == pd.Timestamp("2025-12-31 23:00")
    assert len(got) == 31 * 24


def test_a_cache_covering_the_window_is_left_alone(tmp_path):
    """
    Review finding: passing the inclusive `window_end` into
    `_identify_missing_periods` made the type-2 completeness check see the
    sub-bar remainder after the last bar of every complete cache — a phantom
    trailing period, a network call, and a cache-file rewrite on every run,
    with the top-up's first page opening past the requested end (measured
    reaching the sealed span before the trim discarded it). A cache whose
    last bar is the final bar of the window must produce zero fetches and a
    byte-untouched file.
    """
    seed = _bars("2025-12-01", 31 * 24)  # -> 2025-12-31 23:00
    seed.to_csv(tmp_path / "BTCUSDT_1h.csv", index=False)
    before = (tmp_path / "BTCUSDT_1h.csv").read_bytes()

    f = _OvershootingFetcher(tmp_path, "2025-12-01", "2025-12-31")
    got = f.get_data("BTCUSDT")

    assert f.requested_periods == [], "complete cache scheduled a phantom top-up fetch"
    assert (tmp_path / "BTCUSDT_1h.csv").read_bytes() == before, "cache rewritten with no new data"
    assert got["timestamp"].max() == pd.Timestamp("2025-12-31 23:00")


def test_a_genuinely_missing_final_bar_is_still_fetched(tmp_path):
    """
    Companion bound to the complete-cache test: the whole-interval condition
    must not under-fetch. Verifier finding — disabling type-2 detection
    outright survived every other test in the suite, and that regression is
    silent: the fetcher logs "complete" and hands stale data to every
    consumer. A cache one bar short must schedule exactly one trailing period
    and land the missing bar on disk.
    """
    seed = _bars("2025-12-01", 31 * 24 - 1)  # -> 2025-12-31 22:00
    seed.to_csv(tmp_path / "BTCUSDT_1h.csv", index=False)

    f = _OvershootingFetcher(tmp_path, "2025-12-01", "2025-12-31")
    # Snap to the venue grid, as real endpoints do (openTime >= since); the
    # default stub echoes the off-grid `latest + 1ms` period start.
    f._fetch_remote = lambda symbol, start, end: (
        f.requested_periods.append((start, end)) or _bars(pd.Timestamp(start).ceil("h"), f.page)
    )
    got = f.get_data("BTCUSDT")

    assert len(f.requested_periods) == 1, "missing final bar was not scheduled"
    assert got["timestamp"].max() == pd.Timestamp("2025-12-31 23:00")
    assert _written(tmp_path)["timestamp"].max() == pd.Timestamp("2025-12-31 23:00")


def test_fear_greed_fetch_respects_a_literal_end(monkeypatch):
    """
    FearGreedFetcher._fetch_remote filtered `< end + 1 day` — the same
    widening removed from _load_all — and it now receives already-literal
    period ends, so it must filter `<= end`. The stub payload spans the seal
    to prove rows past the bound never leave the subclass.
    """
    from data.fetchers import fear_greed_fetcher as fg_mod

    payload = {
        "data": [
            {"timestamp": str(int(pd.Timestamp(d).timestamp())), "value": "50", "value_classification": "Neutral"}
            for d in pd.date_range("2025-12-28", "2026-01-03")
        ]
    }

    class _Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return payload

    monkeypatch.setattr(fg_mod.requests, "get", lambda *a, **k: _Resp())

    f = fg_mod.FearGreedFetcher("2025-12-28", "2025-12-31")
    got = f._fetch_remote("fear_greed", pd.Timestamp("2025-12-28"), pd.Timestamp("2025-12-31 23:59:59.999"))

    assert got["timestamp"].max() == pd.Timestamp("2025-12-31")
    assert not (got["timestamp"] >= pd.Timestamp("2026-01-01")).any(), (
        "rows past the literal period end left _fetch_remote"
    )


# ---------------------------------------------------------------------------
# The case the fix must NOT break
# ---------------------------------------------------------------------------


def test_a_narrow_request_does_not_truncate_a_wider_existing_cache(tmp_path):
    """
    STOP condition, and the reason the clamp lives in `_load_all` rather than in
    `_merge_and_store`: `_merge_and_store` concatenates `existing` + new chunks,
    so clamping there would DELETE cached rows beyond the current request's end
    whenever anyone fetches a narrower window than the cache already holds. That
    turns a leak into data loss.

    Here the cache runs to 2025-06-30 23:00, the request ends 2025-06-20, and a
    backfill of earlier bars triggers a write. Every existing row must survive it.
    """
    seed = _bars("2025-06-10", 21 * 24)  # -> 2025-06-30 23:00
    seed.to_csv(tmp_path / "BTCUSDT_1h.csv", index=False)

    f = _OvershootingFetcher(tmp_path, "2025-06-01", "2025-06-20")
    got = f.get_data("BTCUSDT")

    written = _written(tmp_path)
    assert written["timestamp"].max() == pd.Timestamp("2025-06-30 23:00"), (
        "existing rows beyond the requested end were destroyed"
    )
    assert written["timestamp"].min() == pd.Timestamp("2025-06-01 00:00")

    # The returned frame is still trimmed to the requested window — that part of
    # the contract is unchanged.
    assert got["timestamp"].max() == pd.Timestamp("2025-06-20 23:00")
