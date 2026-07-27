"""
data.fetchers
=============
All data fetchers.  Import from here for convenience.

Price data (OHLCV):
    from data.fetchers import CcxtFetcher
    from data.fetchers import CcxtFetcher as HistoricalDataFetcher  # backward compat

Auxiliary / enrichment feeds:
    from data.fetchers import FearGreedFetcher
    from data.fetchers import FundingRateFetcher

Base class (for writing new fetchers):
    from data.fetchers import BaseFetcher
"""

from data.fetchers.base_fetcher        import BaseFetcher
from data.fetchers.ccxt_fetcher        import CcxtFetcher, HistoricalDataFetcher
from data.fetchers.fear_greed_fetcher  import FearGreedFetcher
from data.fetchers.funding_rate_fetcher import FundingRateFetcher
from data.fetchers.whale_footprint_fetcher import (
    ReservedDataError,
    WhaleFootprintFetcher,
)

__all__ = [
    "BaseFetcher",
    "CcxtFetcher",
    "HistoricalDataFetcher",   # backward-compatibility alias
    "FearGreedFetcher",
    "FundingRateFetcher",
    "WhaleFootprintFetcher",
    "ReservedDataError",
]
