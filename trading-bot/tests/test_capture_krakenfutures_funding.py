"""
Kraken Futures funding capture tool.

Mock-only: no live network fetch, no real data. A stub ccxt exchange serves a
synthetic hourly funding window (filtering by `since` client-side exactly as
ccxt's krakenfutures adapter does). Pins:

  (a) exchange_id="krakenfutures" resolves interval 3600 and cache slot
      krakenfutures_BTCUSD_funding_1h;
  (b) a second capture APPENDS/merges rather than overwrites (no data loss) —
      the ingest_kraken_archive.py overwrite trap must not recur;
  (c) the reused gap-guard passes a clean hourly append and FIRES on a
      discontinuous one (rolling-window-ignores-since shape);
  (d) main() exits cleanly (returns 0) with a mocked exchange.

All assertions are on SYNTHETIC values only.
"""
import datetime
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.base_fetcher import FetchGapError  # noqa: E402
from data.fetchers.funding_rate_fetcher import FundingRateFetcher  # noqa: E402
from tools import capture_krakenfutures_funding as cap  # noqa: E402

SYMBOL = "BTCUSD"
# Pre-seal synthetic base (before the 2026-01-01 holdout start). Test files are
# excluded from the seal scan, but staying pre-seal keeps the fixture honest.
BASE = datetime.datetime(2025, 9, 1)


def _epoch_ms(dt: datetime.datetime) -> int:
    """Naive datetime interpreted as UTC -> epoch milliseconds, so the
    fetcher's pd.to_datetime(unit='ms') round-trips back to `dt`."""
    return int(dt.replace(tzinfo=datetime.UTC).timestamp() * 1000)


def _hourly_records(start: datetime.datetime, count: int) -> list[dict]:
    """A contiguous hourly funding window, distinct per-row rates so a value
    assertion actually pins the row (not just its presence)."""
    return [
        {
            "timestamp": _epoch_ms(start + datetime.timedelta(hours=i)),
            "fundingRate": 2.0e-5 + i * 5.0e-7,
            "markPrice": 60000.0 + i,
        }
        for i in range(count)
    ]


class _FakeKrakenFuturesExchange:
    """Stub ccxt exchange: serves a fixed synthetic funding window, filtering by
    `since` client-side the way ccxt.krakenfutures does (filter_by_symbol_since_
    limit). No network. rateLimit=0 so _fetch_remote does not sleep."""

    rateLimit = 0

    def __init__(self, records: list[dict]):
        self._records = sorted(records, key=lambda r: r["timestamp"])

    def fetch_funding_rate_history(self, symbol, since=None, limit=None):
        recs = self._records
        if since is not None:
            recs = [r for r in recs if r["timestamp"] >= since]
        if limit is not None:
            recs = recs[:limit]
        return list(recs)


def _fetcher_with_mock(records, start, end, data_dir):
    fetcher = cap.build_fetcher(SYMBOL, start, end, str(data_dir))
    fetcher.exchange = _FakeKrakenFuturesExchange(records)
    return fetcher


def _read_cache(dest: str) -> pd.DataFrame:
    df = pd.read_csv(dest)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


# ---------------------------------------------------------------------------
# (a) venue -> interval + cache-name resolution
# ---------------------------------------------------------------------------

def test_krakenfutures_resolves_hourly_interval_and_cache_name(tmp_path):
    fetcher = cap.build_fetcher(SYMBOL, BASE, BASE + datetime.timedelta(days=1),
                                str(tmp_path))
    assert fetcher.exchange_id == "krakenfutures"
    assert fetcher.interval_seconds == 3600
    assert fetcher.cache_key(SYMBOL) == "krakenfutures_BTCUSD_funding_1h"


def test_build_fetcher_uses_local_storage(tmp_path):
    """localStorage must be on, else get_data never loads/merges/writes a cache
    and every 'capture' would silently no-op to disk."""
    fetcher = cap.build_fetcher(SYMBOL, BASE, BASE + datetime.timedelta(days=1),
                                str(tmp_path))
    assert fetcher.localStorage is True


# ---------------------------------------------------------------------------
# (b) first capture writes the slot; (c) a clean second capture APPENDS
# ---------------------------------------------------------------------------

def test_first_capture_writes_krakenfutures_slot(tmp_path):
    records = _hourly_records(BASE, 48)
    fetcher = _fetcher_with_mock(records, BASE, BASE + datetime.timedelta(days=1),
                                 tmp_path)

    summary = cap.capture(fetcher, SYMBOL)

    expected = tmp_path / "krakenfutures_BTCUSD_funding_1h.csv"
    assert Path(summary["dest"]) == expected
    assert expected.exists()
    assert summary["rows"] > 0
    disk = _read_cache(summary["dest"])
    assert len(disk) == summary["rows"]


def test_second_capture_appends_not_overwrites(tmp_path):
    # 60 hourly settlements: 09-01 00:00 .. 09-03 11:00.
    records = _hourly_records(BASE, 60)

    # Run 1: window ends 09-02 -> keeps 09-01 00:00 .. 09-02 23:00 (48 rows).
    f1 = _fetcher_with_mock(records, BASE, BASE + datetime.timedelta(days=1),
                            tmp_path)
    s1 = cap.capture(f1, SYMBOL)
    run1 = _read_cache(s1["dest"])

    # Run 2: window extends to 09-03 -> appends 09-03 00:00 .. 09-03 11:00.
    f2 = _fetcher_with_mock(records, BASE, BASE + datetime.timedelta(days=2),
                            tmp_path)
    s2 = cap.capture(f2, SYMBOL)
    run2 = _read_cache(s2["dest"])

    # Strictly grew -> new settlements were merged in.
    assert len(run2) > len(run1)

    # No data loss: every run-1 timestamp survives the second write.
    run1_ts = set(run1["timestamp"])
    run2_ts = set(run2["timestamp"])
    assert run1_ts.issubset(run2_ts)

    # And the original rows' VALUES are unchanged (overwrite would replace them).
    first_ts = run1["timestamp"].iloc[0]
    v1 = run1.loc[run1["timestamp"] == first_ts, "funding_rate"].iloc[0]
    v2 = run2.loc[run2["timestamp"] == first_ts, "funding_rate"].iloc[0]
    assert v2 == pytest.approx(v1)
    assert v1 == pytest.approx(2.0e-5)  # synthetic row 0

    # Clean hourly append leaves a continuous series (gap-guard did not fire).
    ts = np.sort(run2["timestamp"].to_numpy())
    deltas = np.diff(ts)
    assert (deltas == np.timedelta64(1, "h")).all()


# ---------------------------------------------------------------------------
# (c) the reused gap-guard FIRES on a discontinuous second capture
# ---------------------------------------------------------------------------

def test_discontinuous_second_capture_raises_fetch_gap_error(tmp_path):
    # Continuous 09-01 00:00 .. 09-02 23:00, then a 25h hole, then 09-04 00:00+.
    cont = _hourly_records(BASE, 48)
    resume = BASE + datetime.timedelta(hours=72)   # 09-04 00:00 (skips all 09-03)
    jump = _hourly_records(resume, 6)
    records = cont + jump

    # Run 1 (ends 09-02): only the continuous block lands.
    f1 = _fetcher_with_mock(records, BASE, BASE + datetime.timedelta(days=1),
                            tmp_path)
    cap.capture(f1, SYMBOL)
    before = _read_cache(f1._csv_path(SYMBOL))

    # Run 2 (ends 09-04): the append fetch returns the post-hole block, which
    # does not connect to the cache -> the reused _assert_no_new_gap must reject
    # it, leaving the cache untouched.
    f2 = _fetcher_with_mock(records, BASE, BASE + datetime.timedelta(days=3),
                            tmp_path)
    with pytest.raises(FetchGapError):
        cap.capture(f2, SYMBOL)

    after = _read_cache(f2._csv_path(SYMBOL))
    pd.testing.assert_frame_equal(before, after)


# ---------------------------------------------------------------------------
# (d) main() exits cleanly with a mocked exchange (no live fetch)
# ---------------------------------------------------------------------------

def _pin_tool_clock(monkeypatch, now: datetime.datetime) -> None:
    """Freeze the "now" that cap.main() reads to compute its lookback window.

    main() builds start = now - lookback_days (default 400). With a real clock
    the fixed-date fixture ages out of that window (a date time-bomb: from about
    2026-10-05 on, BASE + 48h sat before `start`, the fetch came back empty and
    capture() raised KeyError: 'timestamp'). datetime.datetime itself is
    immutable, so swap the tool module's `datetime` reference for a shim whose
    datetime.now() is fixed; timedelta/UTC pass through unchanged.
    """
    class _FrozenDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return now.replace(tzinfo=tz) if tz is not None else now

    real_timedelta, real_utc = datetime.timedelta, datetime.UTC

    class _Shim:
        datetime = _FrozenDateTime
        timedelta = real_timedelta
        UTC = real_utc

    monkeypatch.setattr(cap, "datetime", _Shim)


def test_main_returns_zero_and_writes_cache(tmp_path, monkeypatch):
    records = _hourly_records(BASE, 48)
    # Pin "now" two days after the fixture start so [now - 400d, now] always
    # contains every record, whatever the real date is.
    _pin_tool_clock(monkeypatch, BASE + datetime.timedelta(days=2))

    def fake_build(symbol, start, end, data_dir, exchange_id=cap.EXCHANGE_ID):
        fetcher = FundingRateFetcher(
            start_date=start, end_date=end, symbols=[symbol],
            exchange_id=exchange_id, localStorage=True, data_dir=data_dir,
        )
        fetcher.exchange = _FakeKrakenFuturesExchange(records)
        return fetcher

    monkeypatch.setattr(cap, "build_fetcher", fake_build)

    rc = cap.main(["--symbol", SYMBOL, "--data-dir", str(tmp_path)])

    assert rc == 0
    assert (tmp_path / "krakenfutures_BTCUSD_funding_1h.csv").exists()


def test_main_returns_one_when_exchange_uninitialised(tmp_path, monkeypatch):
    def fake_build(symbol, start, end, data_dir, exchange_id=cap.EXCHANGE_ID):
        fetcher = FundingRateFetcher(
            start_date=start, end_date=end, symbols=[symbol],
            exchange_id=exchange_id, localStorage=True, data_dir=data_dir,
        )
        fetcher.exchange = None
        return fetcher

    monkeypatch.setattr(cap, "build_fetcher", fake_build)

    rc = cap.main(["--symbol", SYMBOL, "--data-dir", str(tmp_path)])

    assert rc == 1
    assert not (tmp_path / "krakenfutures_BTCUSD_funding_1h.csv").exists()
