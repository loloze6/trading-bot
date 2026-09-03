"""
Timezone anchoring of the CCXT `since`/`until` epoch bounds (CUL-248).

`CcxtFetcher._fetch_remote` (and its funding sibling) computed the paginated
fetch bounds as `int(start.timestamp() * 1000)`. `start`/`end` arrive tz-naive
but denote UTC instants: `base_fetcher.py:107` seeds them via `pd.to_datetime`,
and `_identify_missing_periods` emits plain `datetime.datetime` for gap types
1-3 (the common incremental-top-up path). `datetime.datetime.timestamp()` on a
naive value interprets it in the host's LOCAL zone, so on any non-UTC host the
absolute epoch handed to the exchange is shifted by the host's UTC offset
(1h CET / 2h CEST on Jeremy's Europe/Paris machine) — a silently mis-placed
fetch window. The fix anchors both bounds to UTC explicitly.

The ground-truth reference is `pd.Timestamp(dt, tz="UTC").value // 1_000_000`
(nanoseconds-since-UTC-epoch → ms), an implementation independent of the
production `.timestamp()` path, so these assertions are not tautological.

Coverage split by host:
  * The biting non-UTC proof (host TZ forced to Europe/Paris) runs ONLY where
    `time.tzset` exists — this CEST Mac, and the Linux CI leg if TZ is settable.
    Those cases skip on Windows (no `tzset`).
  * `_utc_epoch_ms` is unit-tested directly against `calendar.timegm` — a
    host-TZ-independent reference, so the assertion is a valid invariant on
    every host and needs no `tzset`. It CATCHES the bug on any non-UTC host
    (this CEST Mac; a non-UTC CI leg); on a UTC host the bug does not manifest
    at all, so nothing there can catch it — that is a property of the bug, not
    a coverage gap. The Windows leg runs only this helper test plus the
    current-host cases; we claim no more than that.
"""

import calendar
import datetime
import os
import sys
import time
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.base_fetcher import _utc_epoch_ms  # noqa: E402
from data.fetchers.ccxt_fetcher import CcxtFetcher  # noqa: E402
from data.fetchers.funding_rate_fetcher import FundingRateFetcher  # noqa: E402

_HAS_TZSET = hasattr(time, "tzset")


def _utc_ms(dt) -> int:
    """Ground-truth UTC epoch-ms for a naive-UTC datetime/Timestamp."""
    return pd.Timestamp(dt, tz="UTC").value // 1_000_000


def _timegm_ms(dt: datetime.datetime) -> int:
    """Host-TZ-independent UTC epoch-ms via calendar.timegm (millisecond-precise)."""
    return calendar.timegm(dt.utctimetuple()) * 1000 + dt.microsecond // 1000


# ---------------------------------------------------------------------------
# _utc_epoch_ms unit tests — tz-independent, so they run on Windows CI too and
# are the only leg that pins the arithmetic where time.tzset is absent.
# ---------------------------------------------------------------------------

_HELPER_DATES = [
    datetime.datetime(2024, 1, 15, 0, 0, 0),  # CET wall-clock date
    datetime.datetime(2024, 7, 15, 0, 0, 0),  # CEST wall-clock date
    datetime.datetime(2024, 1, 15, 0, 0, 0) - datetime.timedelta(milliseconds=1),  # sub-second
]


@pytest.mark.parametrize("dt", _HELPER_DATES, ids=["jan", "jul", "minus1ms"])
def test_utc_epoch_ms_matches_timegm(dt):
    assert _utc_epoch_ms(dt) == _timegm_ms(dt)


def test_utc_epoch_ms_aware_uses_real_offset_not_relabel():
    """An aware value is converted on its own offset, never re-labelled as UTC."""
    aware = datetime.datetime(2024, 7, 15, 2, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=2)))
    correct = pd.Timestamp(aware).value // 1_000_000  # ground truth: 02:00+02:00 == 00:00 UTC
    relabelled = _timegm_ms(aware.replace(tzinfo=None))  # the bug: wall-clock read as UTC
    assert _utc_epoch_ms(aware) == correct
    assert _utc_epoch_ms(aware) != relabelled


class _CapturingExchange:
    """Records the `since` epoch handed to CCXT, then breaks the fetch loop."""

    rateLimit = 0

    def __init__(self):
        self.since_calls: list[int] = []

    def fetch_ohlcv(self, symbol, timeframe, since, limit):
        self.since_calls.append(since)
        return []

    def fetch_funding_rate_history(self, symbol, since, limit):
        self.since_calls.append(since)
        return []


@pytest.fixture
def paris_tz():
    """Run the body under Europe/Paris host time, then restore."""
    if not _HAS_TZSET:
        pytest.skip("time.tzset unavailable (Windows)")
    prev = os.environ.get("TZ")
    os.environ["TZ"] = "Europe/Paris"
    time.tzset()
    try:
        yield
    finally:
        if prev is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = prev
        time.tzset()


def _ccxt(tmp_path) -> tuple[CcxtFetcher, _CapturingExchange]:
    f = CcxtFetcher(
        start_date="2024-01-01",
        end_date="2024-02-01",
        symbols=["BTCUSDT"],
        candle_interval_seconds=3600,
        localStorage=False,
        data_dir=str(tmp_path),
    )
    ex = _CapturingExchange()
    f.exchange = ex
    return f, ex


def _funding(tmp_path) -> tuple[FundingRateFetcher, _CapturingExchange]:
    f = FundingRateFetcher(
        start_date="2024-01-01",
        end_date="2024-02-01",
        symbols=["BTCUSDT"],
        localStorage=False,
        data_dir=str(tmp_path),
    )
    ex = _CapturingExchange()
    f.exchange = ex
    return f, ex


# ---------------------------------------------------------------------------
# `since` is the absolute epoch sent to the exchange — it must be UTC-correct
# regardless of host TZ. `until` uses the byte-identical expression on the same
# line pair; each date below is exercised through the `since`-position argument.
# ---------------------------------------------------------------------------

# 2024-01-15 → CET (UTC+1); 2024-07-15 → CEST (UTC+2): two distinct DST offsets.
_DST_DATES = [
    datetime.datetime(2024, 1, 15, 0, 0, 0),
    datetime.datetime(2024, 7, 15, 0, 0, 0),
]


@pytest.mark.parametrize("start", _DST_DATES, ids=["CET-winter", "CEST-summer"])
def test_ccxt_since_utc_anchored_under_paris(tmp_path, paris_tz, start):
    end = start + datetime.timedelta(hours=1)
    f, ex = _ccxt(tmp_path)
    f._fetch_remote("BTCUSDT", start, end)
    assert ex.since_calls == [_utc_ms(start)]


@pytest.mark.parametrize("start", _DST_DATES, ids=["CET-winter", "CEST-summer"])
def test_funding_since_utc_anchored_under_paris(tmp_path, paris_tz, start):
    end = start + datetime.timedelta(hours=8)
    f, ex = _funding(tmp_path)
    f._fetch_remote("BTCUSDT", start, end)
    assert ex.since_calls == [_utc_ms(start)]


def test_ccxt_since_utc_anchored_on_current_host(tmp_path):
    """Whatever the host TZ, the emitted `since` matches the UTC reference (bites on this CEST Mac)."""
    start = datetime.datetime(2024, 3, 1, 0, 0, 0)
    f, ex = _ccxt(tmp_path)
    f._fetch_remote("BTCUSDT", start, start + datetime.timedelta(hours=1))
    assert ex.since_calls == [_utc_ms(start)]


def test_funding_since_utc_anchored_on_current_host(tmp_path):
    """Funding-fetcher parity for the current-host guard."""
    start = datetime.datetime(2024, 3, 1, 0, 0, 0)
    f, ex = _funding(tmp_path)
    f._fetch_remote("BTCUSDT", start, start + datetime.timedelta(hours=8))
    assert ex.since_calls == [_utc_ms(start)]


# ---------------------------------------------------------------------------
# Gap-type input shapes: types 1/2 emit plain datetime with a ±1ms offset;
# type 3 emits datetime.replace(tzinfo=None); empty-cache emits pd.Timestamp.
# Every shape must convert to the same UTC epoch under a non-UTC host.
# ---------------------------------------------------------------------------

_SHAPES = [
    datetime.datetime(2024, 1, 15, 0, 0, 0),  # plain (types 1/2)
    datetime.datetime(2024, 1, 15, 0, 0, 0) - datetime.timedelta(milliseconds=1),  # type-1 end (-1ms)
    datetime.datetime(2024, 1, 15, 0, 0, 0, 1000).replace(tzinfo=None),  # type-3 naive
    pd.Timestamp("2024-01-15 00:00:00"),  # empty-cache
]


@pytest.mark.parametrize("start", _SHAPES, ids=["plain", "minus1ms", "type3", "pdTimestamp"])
def test_ccxt_since_all_gap_shapes_under_paris(tmp_path, paris_tz, start):
    f, ex = _ccxt(tmp_path)
    f._fetch_remote("BTCUSDT", start, start + datetime.timedelta(hours=1))
    assert ex.since_calls == [_utc_ms(start)]


# ---------------------------------------------------------------------------
# End-to-end through the real _identify_missing_periods: the plain datetimes it
# produces for gap types 1, 2 and 3 must yield UTC-correct `since` under Paris.
# ---------------------------------------------------------------------------


def _existing(ts_start: str, periods: int) -> pd.DataFrame:
    ts = pd.date_range(start=ts_start, periods=periods, freq="1h")
    return pd.DataFrame({"timestamp": ts, "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0})


def test_identify_missing_type1_since_utc_under_paris(tmp_path, paris_tz):
    """Gap before earliest stored row → plain datetime start (type 1)."""
    f, ex = _ccxt(tmp_path)
    existing = _existing("2024-01-15 00:00", 24)  # cache starts 01-15
    periods = f._identify_missing_periods(existing, datetime.datetime(2024, 1, 10), datetime.datetime(2024, 1, 16))
    assert periods, "expected a type-1 gap"
    ps, _ = periods[0]
    f._fetch_remote("BTCUSDT", ps, ps + datetime.timedelta(hours=1))
    assert ex.since_calls == [_utc_ms(ps)]


def test_identify_missing_type2_since_utc_under_paris(tmp_path, paris_tz):
    """Gap after latest stored row → plain datetime start (type 2)."""
    f, ex = _ccxt(tmp_path)
    existing = _existing("2024-01-10 00:00", 24)  # cache ends 01-10 23:00
    periods = f._identify_missing_periods(existing, datetime.datetime(2024, 1, 10), datetime.datetime(2024, 1, 20))
    assert periods, "expected a type-2 gap"
    ps, _ = periods[-1]
    f._fetch_remote("BTCUSDT", ps, ps + datetime.timedelta(hours=1))
    assert ex.since_calls == [_utc_ms(ps)]


def test_identify_missing_type3_since_utc_under_paris(tmp_path, paris_tz):
    """Internal gap → datetime.replace(tzinfo=None) start (type 3)."""
    f, ex = _ccxt(tmp_path)
    head = _existing("2024-01-10 00:00", 10)
    tail = _existing("2024-01-12 00:00", 10)  # 38h internal gap
    existing = pd.concat([head, tail], ignore_index=True)
    periods = f._identify_missing_periods(existing, datetime.datetime(2024, 1, 10), datetime.datetime(2024, 1, 13))
    # locate the interior gap period (starts after the head, before the tail)
    interior = [
        p for p in periods if p[0] >= datetime.datetime(2024, 1, 10, 10) and p[1] <= datetime.datetime(2024, 1, 12)
    ]
    assert interior, f"expected a type-3 interior gap, got {periods}"
    ps, _ = interior[0]
    f._fetch_remote("BTCUSDT", ps, ps + datetime.timedelta(hours=1))
    assert ex.since_calls == [_utc_ms(ps)]
