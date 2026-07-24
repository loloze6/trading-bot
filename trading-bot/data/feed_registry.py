"""
feed_registry.py
================
Single registry mapping feed names to their fetcher factories.

To add a new feed:
  1. Import its fetcher class
  2. Add one entry to FEED_REGISTRY

Nothing else needs to change in backtester.py or launcher.py.
"""

import os

import pandas as pd

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


def build_daily_funding_series(symbols, data_dir):
    """
    Build a per-symbol DAILY funding COST series from the Binance 8h funding CSVs
    already on disk (``{symbol}_funding_8h.csv``, cols ``timestamp,funding_rate,
    mark_price``; see FundingRateFetcher).

    ``f_daily[day] = SUM of that day's settlements`` (the 00:00/08:00/16:00 UTC
    settlements *dated to that calendar day*). Partial days (feed inception,
    maintenance gaps) sum whatever settlements exist — no imputation of a missing
    settlement. Days with no settlement are simply absent from the series.

    This is a NEW cost series, kept DISTINCT from the forward-filled ``funding_rate``
    SIGNAL feed the FundingRateMeanReversionComponent reads (that feed is produced by
    FundingRateFetcher + merge_asof and is left byte-identical — this function never
    touches it). The daily-summed series is what a funding CASH-FLOW model needs: a
    position held across a full daily bar accrues all of that day's settlements, not
    just the single most-recently-published rate.

    The series is indexed by DATE (each key is the day normalized to 00:00), so a
    backtest window naturally bounds it and a bar reads only settlements dated to that
    bar's day — never a settlement dated after it (no look-ahead).

    Returns
    -------
    dict[str, dict[pandas.Timestamp, float]]
        ``{symbol: {normalized-day-Timestamp: summed_funding_rate}}``. Symbols whose
        CSV is absent are omitted.
    """
    out = {}
    for symbol in symbols:
        path = os.path.join(data_dir, f"{symbol}_funding_8h.csv")
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path, usecols=["timestamp", "funding_rate"])
        if df.empty:
            out[symbol] = {}
            continue
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["day"] = df["timestamp"].dt.normalize()
        daily = df.groupby("day")["funding_rate"].sum()
        out[symbol] = {day: float(val) for day, val in daily.items()}
    return out