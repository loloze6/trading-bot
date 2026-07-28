"""
FearGreedFetcher
================
Fetches the daily Crypto Fear & Greed Index from the Alternative.me API
and stores it locally as CSV.

This is a concrete example of how any macro / sentiment data source plugs
into the pipeline.  The only code specific to this source is _fetch_remote()
and cache_key() — all storage, gap detection, and merging is inherited from
BaseFetcher.

Output column added to the candle DataFrame:  'fear_greed'  (0–100 integer)

The Fear & Greed index is published once per day, so:
  • expected_gap_tolerance is raised to 2.0 to tolerate the natural 24-hour
    cadence without false gap alerts.
  • During candle-level enrichment in DataManager, the value is forward-filled
    (merge_asof) so every intra-day candle inherits the most recent daily reading.

Usage:
    fetcher = FearGreedFetcher('2024-01-01', '2024-12-31',
                               localStorage=True)
    data = fetcher.get_data()      # {'fear_greed': DataFrame}
    # DataFrame has columns: timestamp, value (0-100), classification (text)

    # Register with DataManager:
    data_manager.register_feed(
        name='fear_greed',
        fetcher=FearGreedFetcher(...),
        window_seconds=0,     # published instantaneously — no forward window
        agg='last',           # take the last reading within each candle window
    )
"""

import datetime
import logging
from typing import Optional

import pandas as pd

try:
    import requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

from data.fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger("trading_bot")

_API_URL = "https://api.alternative.me/fng/"
_FEAR_GREED_INTERVAL_SECONDS = 24 * 3600   # 24 hours in seconds


class FearGreedFetcher(BaseFetcher):
    """
    Daily Crypto Fear & Greed Index from Alternative.me.

    The API returns up to 'limit' days of history in a single call, so no
    pagination loop is needed.  We request the full window in one shot and
    rely on BaseFetcher for local caching and gap-fill logic. 
    """

    # Daily data — tolerate gaps up to 2× the 86400s interval before alerting.
    # This prevents false positives on weekends / API downtime.
    expected_gap_tolerance: float = 2.0

    def __init__(
        self,
        start_date,
        end_date,
        localStorage: bool = False,
        data_dir: str = "data",
    ):
        """
        Note: no `symbols` parameter — Fear & Greed is a single global index.
        We pass ['fear_greed'] as the symbols list to fit BaseFetcher's API.
        """
        super().__init__(
            start_date=start_date,
            end_date=end_date,
            symbols=["fear_greed"],       # single global feed, keyed by name
            interval_seconds=_FEAR_GREED_INTERVAL_SECONDS,       # published daily
            localStorage=localStorage,
            data_dir=data_dir,
        )

    # -----------------------------------------------------------------------
    # BaseFetcher interface
    # -----------------------------------------------------------------------

    def cache_key(self, symbol: str) -> str:
        """'fear_greed_daily' — clearly namespaced, won't collide with price CSVs."""
        return "fear_greed_daily"

    def _fetch_remote(
        self,
        symbol: str,
        start: datetime.datetime,
        end: datetime.datetime,
    ) -> pd.DataFrame:
        """
        Fetch Fear & Greed history from Alternative.me in a single API call.

        The API does not support 'since' filtering directly — we request
        `limit` days (the full window length) and then filter to [start, end]
        locally.  This is fine for a daily feed; the entire history is small.
        """
        if not _REQUESTS_AVAILABLE:
            logger.error("FearGreedFetcher: 'requests' library not installed")
            return pd.DataFrame()

        # Request enough days to cover the window plus a small buffer
        days_needed = int((datetime.datetime.utcnow() - start).days) + 10

        try:
            resp = requests.get(
                _API_URL,
                params={"limit": days_needed, "format": "json"},
                timeout=10,
            )
            resp.raise_for_status()
            payload = resp.json()

            if "data" not in payload or not payload["data"]:
                logger.warning("FearGreedFetcher: empty response from API")
                return pd.DataFrame()

            records = [
                {
                    "timestamp": pd.Timestamp(datetime.datetime.utcfromtimestamp(int(entry["timestamp"]))).floor("D"),
                    "fear_greed": int(entry["value"]),
                    "classification": entry.get("value_classification", ""),
                }
                for entry in payload["data"]
            ]

            df = pd.DataFrame(records).sort_values("timestamp").reset_index(drop=True)

            # Filter to the requested window — the API always returns the most recent
            # N days from today regardless of start/end, so we trim here.
            df = df[(df["timestamp"] >= start) & (df["timestamp"] < end + datetime.timedelta(days=1))]

            logger.info(f"FearGreedFetcher: fetched {len(df)} daily readings in window")
            return df.reset_index(drop=True)

        except Exception as e:
            logger.error(f"FearGreedFetcher: fetch failed: {e}")
            return pd.DataFrame()