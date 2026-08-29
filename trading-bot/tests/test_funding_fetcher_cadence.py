"""
FundingRateFetcher settlement cadence.

Parametrizes the funding fetcher's interval so a non-8h venue (Kraken Futures,
hourly) works while the Binance 8h path stays byte-identical. Pins:
  - the per-exchange cadence default map (krakenfutures -> 3600, else 28800)
  - explicit interval_seconds overriding the map
  - the interval-derived cache_key suffix (28800 -> funding_8h, 3600 -> funding_1h)
  - THE STRIDE BUG: pagination advanced by the 8h constant thinned hourly data
    ~7 records per 1000-row page boundary. The fix uses self.interval_seconds;
    this file proves it with a page-boundary stub.

The existing binance/kraken-spot cache_key pins in test_aux_feed_venue.py stay
untouched and keep proving the default path is unchanged.
"""

import datetime
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.funding_rate_fetcher import FundingRateFetcher  # noqa: E402

# ---------------------------------------------------------------------------
# Cadence resolution + interval-derived cache_key
# ---------------------------------------------------------------------------


def test_krakenfutures_defaults_to_hourly_cadence():
    f = FundingRateFetcher(
        "2025-08-13", "2025-08-14", symbols=["BTCUSD"], exchange_id="krakenfutures"
    )
    assert f.interval_seconds == 3600
    assert f.cache_key("BTCUSD") == "krakenfutures_BTCUSD_funding_1h"


def test_binance_cadence_and_cache_key_unchanged():
    f = FundingRateFetcher(
        "2025-08-13", "2025-08-14", symbols=["BTCUSDT"], exchange_id="binance"
    )
    assert f.interval_seconds == 28800
    assert f.cache_key("BTCUSDT") == "BTCUSDT_funding_8h"


def test_kraken_spot_id_keeps_the_8h_default():
    # The cadence map keys on "krakenfutures", NOT "kraken" (spot): a bare
    # exchange_id="kraken" construction still resolves 8h -- this is why the
    # direct-construction pin in test_aux_feed_venue.py survives.
    f = FundingRateFetcher(
        "2025-08-13", "2025-08-14", symbols=["BTCUSD"], exchange_id="kraken"
    )
    assert f.interval_seconds == 28800
    assert f.cache_key("BTCUSD") == "kraken_BTCUSD_funding_8h"


def test_explicit_interval_overrides_the_exchange_default():
    # Explicit arg wins over the per-exchange map (krakenfutures would be 3600).
    f = FundingRateFetcher(
        "2025-08-13",
        "2025-08-14",
        symbols=["BTCUSD"],
        exchange_id="krakenfutures",
        interval_seconds=28800,
    )
    assert f.interval_seconds == 28800
    assert f.cache_key("BTCUSD") == "krakenfutures_BTCUSD_funding_8h"


# ---------------------------------------------------------------------------
# The stride bug -- pagination page-boundary thinning
# ---------------------------------------------------------------------------


class _RollingWindowStub:
    """Models krakenfutures: every call returns the FULL window filtered to
    `since` client-side (ccxt filter_by_symbol_since_limit), capped at `limit`.
    krakenfutures ignores `since` server-side and ccxt slices locally, so a
    stride that overshoots the true cadence skips whatever it steps over."""

    rateLimit = 0

    def __init__(self, grid_ms):
        self._grid = sorted(grid_ms)

    def fetch_funding_rate_history(self, symbol, since, limit):
        rows = [ts for ts in self._grid if ts >= since][:limit]
        return [
            {"timestamp": ts, "fundingRate": 1e-5, "markPrice": None} for ts in rows
        ]


def test_stride_uses_interval_no_page_boundary_thinning():
    """Regression for the pagination stride bug. With interval resolved to 3600
    the stride is one hour and every record survives the 1000-row page boundary.

    Asserts the EXACT sorted timestamp sequence -- chosen as strictly stronger
    than a bare set-equality check:
      - the 8h-constant defect drops 7 records per boundary -> missing
        timestamps -> RED.
      - a sign/sibling stride mutation re-fetches overlapping records ->
        duplicate timestamps whose SET still equals the grid (the duplicate
        superset collapses under set()), so set-equality would ACCEPT it;
        sequence-equality rejects the extra rows -> RED.
    (Both mutations above also change the row count, so a length check would
    catch these two; sequence-equality is the strictly-stronger choice because
    it rejects the set-surviving sign-flip and pins the actual timestamp
    values, catching a count-preserving shift a set or length check would not.)
    Only the correct one-hour stride reproduces the hourly grid exactly once.
    """
    start = datetime.datetime(2025, 8, 13, 8, 0, tzinfo=datetime.UTC)
    end = start + datetime.timedelta(hours=2000)  # well past the grid
    since_ms = int(start.timestamp() * 1000)
    n = 1500  # > one 1000-row page: forces a page boundary
    grid_ms = [since_ms + i * 3_600_000 for i in range(n)]  # hourly grid

    fetcher = FundingRateFetcher(
        start, end, symbols=["BTCUSD"], exchange_id="krakenfutures"
    )
    assert fetcher.interval_seconds == 3600  # precondition: hourly cadence resolved
    fetcher.exchange = _RollingWindowStub(grid_ms)

    df = fetcher._fetch_remote("BTCUSD", start, end)
    result_ms = [int(ts.value // 1_000_000) for ts in df["timestamp"]]

    assert result_ms == grid_ms
