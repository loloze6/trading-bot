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

from data.fetchers import FundingRateFetcher, FearGreedFetcher, WhaleFootprintFetcher

# feed name → lambda(symbols, start, end) → BaseFetcher instance
FEED_REGISTRY = {
    'funding_rate': lambda symbols, start, end, data_dir: FundingRateFetcher(
        start, end, symbols=symbols, localStorage=True, data_dir=data_dir
    ),
    'fear_greed': lambda symbols, start, end, data_dir: FearGreedFetcher(
        start, end, localStorage=True, data_dir=data_dir
    ),
}

# ---------------------------------------------------------------------------
# RESERVED FEEDS — a SECOND registry, deliberately not merged into the first.
#
# `FEED_REGISTRY` is not an opt-in menu. `launcher.py:290` and `launcher.py:596`
# both pass the WHOLE dict as `extra_feeds`, so every name in it is constructed
# and loaded on every backtest. That makes it precisely the wrong home for a
# dataset that must not be read by default: adding a deny-by-default feed there
# would either break every run or, worse, quietly load reserved data into all of
# them. The split below is what deny-by-default means at the wiring level —
# membership of FEED_REGISTRY IS the release decision, so a reserved feed must
# not be a member.
#
# A caller opts in BY NAME, and even then the gate decides:
#
#     from data.feed_registry import RESERVED_FEED_REGISTRY
#     bot.load_data(start, end, extra_feeds={
#         k: RESERVED_FEED_REGISTRY[k] for k in ['whale_cvd_delta']
#     })
#
# ...which raises ReservedDataError unless campaign_data_policy.yaml carries a
# committed designation covering the window. Being listed here is not a release;
# it is only the wiring.
#
# ONE ENTRY PER COLUMN, all backed by the same fetcher and the same cache_key.
# DataManager._premerge_aux_feeds attaches only the column whose name equals the
# registered feed name (data_manager.py:622), so a six-column feed needs six
# names; sharing the cache_key means the CSV is still computed once.
# ---------------------------------------------------------------------------
WHALE_FOOTPRINT_FEEDS = (
    'whale_lt_imbalance',
    'whale_lt_count',
    'whale_cvd_delta',
    'whale_size_shift',
    'whale_trade_count',
    'whale_attested',
)

RESERVED_FEED_REGISTRY = {
    name: (lambda symbols, start, end, data_dir: WhaleFootprintFetcher(
        start, end, symbols=symbols, localStorage=True, data_dir=data_dir
    ))
    for name in WHALE_FOOTPRINT_FEEDS
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