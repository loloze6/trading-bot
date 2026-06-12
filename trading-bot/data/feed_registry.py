"""
feed_registry.py
================
Single registry mapping feed names to their fetcher factories.
 
To add a new feed:
  1. Import its fetcher class
  2. Add one entry to FEED_REGISTRY
 
Nothing else needs to change in backtester.py or launcher.py.
"""
 
from data.fetchers import FundingRateFetcher, FearGreedFetcher
 
# feed name → lambda(symbols, start, end) → BaseFetcher instance
FEED_REGISTRY = {
    'funding_rate': lambda symbols, start, end, data_dir: FundingRateFetcher(
        start, end, symbols=symbols, localStorage=True, data_dir=data_dir
    ),
    'fear_greed': lambda symbols, start, end, data_dir: FearGreedFetcher(
        start, end, localStorage=True, data_dir=data_dir
    ),
}