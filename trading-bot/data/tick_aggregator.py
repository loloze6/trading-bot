"""
tick_aggregator.py
===================
Volume-weighted OHLCV construction from individual (raw) trade ticks.

E-008 (q1_26 tick archive aggregation) S1/S2. This is a DIFFERENT operation
from the `.resample()` seam already used in `data_manager.py` (around the
aux-feed pre-merge, see `_enrich_and_notify`): that seam takes an already
built time series and applies ONE aggregation function per column (e.g.
`agg='last'` for a funding-rate reading) to fold multiple *readings* that
land inside one candle's span into a single re-sampled row of an AUXILIARY
feed being merged onto pre-existing price candles.

Raw trade-tick aggregation is not that:
  * every bucket needs FOUR DIFFERENT aggregations over the same 'price'
    column simultaneously (first/max/min/last) plus a fifth ('sum') over a
    second 'volume' column — `.resample().agg(single_fn)` doesn't express
    this, `.resample().agg({col: [fn, ...]})` could, but see below;
  * the input is the PRIMARY price series itself at a finer resolution
    (individual trades), not an auxiliary column being merged onto an
    existing candle grid — there is no pre-existing candle DataFrame to
    merge onto yet; building it is the whole point;
  * the aux-feed seam is wired into DataManager's registered-feed causality
    guard / merge_asof pipeline (`register_feed`, `AuxFeedCausalityError`),
    which assumes a scalar reading per timestamp, not raw trades.
Conclusion (S1): extending that seam is not a fit. This module is a small,
standalone, dependency-free function instead — additive, not invasive.

Bucket alignment matches `CandleBuilder._align()` (data_manager.py) exactly:
Unix-epoch integer floor division, NOT pandas' resample default
`origin='start_day'`. This keeps archive-derived bars on the identical grid
boundaries live/backtest candles already use (same rationale as the
aux-feed seam's `origin='epoch'`, data_manager.py:1065).
"""

import datetime
import logging
from typing import Dict

import pandas as pd

logger = logging.getLogger("trading_bot")

# Kraken's public historical-trades CSV export: no header row, three columns
# in this order. This is Kraken's documented public trade-export format
# (general public knowledge — https://support.kraken.com/ "Downloadable
# historical market data"), independent of any particular archive file.
#   price:  trade price (float)
#   volume: trade size, in base currency (float)
#   time:   unix timestamp, seconds (int or float — Kraken emits fractional
#           seconds for sub-second trade precision)
KRAKEN_TRADE_COLUMNS = ["price", "volume", "time"]

# Minute-suffix convention already used by local_data/Kraken_batch/master_q4/
# (file suffixes _1, _60, _240, _720, _1440 = minutes) mapped to seconds, so
# callers can request a bucket width the same way that directory names one.
SUPPORTED_BUCKET_MINUTES: Dict[int, int] = {
    1: 60,
    60: 3600,
    240: 14400,
    720: 43200,
    1440: 86400,
}

OHLCV_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def bucket_seconds_from_minutes(minutes: int) -> int:
    """
    Convert a minute-based bucket width to seconds, restricted to the exact
    set already used by `local_data/Kraken_batch/master_q4/` (1, 60, 240,
    720, 1440). Rejecting anything else here is deliberate: those files are
    the only minute-suffix convention this repo has actually standardized
    on, and an unmapped value (e.g. 720's neighbours) would silently invite
    a bucket width nothing downstream expects.
    """
    if minutes not in SUPPORTED_BUCKET_MINUTES:
        raise ValueError(
            f"Unsupported bucket width: {minutes} minutes. Supported: "
            f"{sorted(SUPPORTED_BUCKET_MINUTES)} (matching the "
            f"Kraken_batch/master_q4 filename-suffix convention)."
        )
    return SUPPORTED_BUCKET_MINUTES[minutes]


def load_kraken_trades_csv(path: str) -> pd.DataFrame:
    """
    Load Kraken's public historical-trades CSV export (headerless: price,
    volume, time) and normalize it to this module's trade-frame convention
    (a 'timestamp' column of naive-UTC datetimes, plus 'price'/'volume').

    Does not touch any cache, does not write anything, does not assume the
    file lives anywhere in particular — pure read + normalize.
    """
    df = pd.read_csv(path, header=None, names=KRAKEN_TRADE_COLUMNS)
    return _normalize_trades(df)


def _normalize_trades(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize a raw Kraken-schema trade frame (price, volume, time-in-
    seconds) into this module's convention: a 'timestamp' column of
    naive-UTC datetimes replacing 'time'.

    `unit='s'` on `pd.to_datetime` interprets the numeric value as an
    offset from the Unix epoch in UTC and returns a tz-NAIVE Timestamp for
    it — exactly the "naive datetimes that represent UTC instants"
    convention the rest of this codebase uses (see
    `data_manager.py:CandleBuilder._align` and `base_fetcher.py:_load_local`).
    """
    missing = {"price", "volume", "time"} - set(df.columns)
    if missing:
        raise ValueError(
            f"Raw trade frame missing required column(s): {sorted(missing)}"
        )
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["time"], unit="s")
    return out.drop(columns=["time"])


def aggregate_trades_to_ohlcv(
    trades: pd.DataFrame, bucket_seconds: int = 3600
) -> pd.DataFrame:
    """
    Bucket individual trades into volume-weighted OHLCV bars.

    Args:
        trades: DataFrame with either
                  - a 'timestamp' column (naive-UTC datetime-like) plus
                    'price' and 'volume', or
                  - Kraken's raw schema ('time' unix-seconds instead of
                    'timestamp'), auto-normalized via `_normalize_trades`.
        bucket_seconds: bucket width in seconds. Must be > 0. Use
                        `bucket_seconds_from_minutes()` to derive this from
                        the Kraken_batch minute-suffix convention.

    Returns:
        DataFrame with columns `OHLCV_COLUMNS`
        (timestamp, open, high, low, close, volume), one row per bucket
        that contains at least one trade, sorted chronologically by
        `timestamp`. Buckets with zero trades are NOT emitted — that is a
        replay-time concern (forward-fill / gap handling belongs to
        `CandleBuilder`/`gap_policy`), not this pure aggregation function's.

        open  = first trade's price in the bucket
        high  = max trade price in the bucket
        low   = min trade price in the bucket
        close = last trade's price in the bucket
        volume = sum of trade sizes in the bucket

    Bucket boundary: floor(`timestamp`) to the nearest `bucket_seconds`
    multiple via Unix-epoch integer division — the identical scheme
    `CandleBuilder._align()` uses, so archive-derived bars land on the same
    grid boundaries live/backtest candles already occupy.

    Raises:
        ValueError: bucket_seconds <= 0, a required column is missing, or
                    'timestamp' is tz-aware (this codebase's convention is
                    naive-UTC throughout; see base_fetcher.py:_load_local's
                    identical guard).
    """
    if bucket_seconds <= 0:
        raise ValueError(f"bucket_seconds must be positive, got {bucket_seconds}")

    if trades.empty:
        return pd.DataFrame(columns=OHLCV_COLUMNS)

    if "timestamp" not in trades.columns:
        trades = _normalize_trades(trades)

    required = {"timestamp", "price", "volume"}
    missing = required - set(trades.columns)
    if missing:
        raise ValueError(
            f"trades frame missing required column(s): {sorted(missing)}"
        )

    df = trades[["timestamp", "price", "volume"]].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if isinstance(df["timestamp"].dtype, pd.DatetimeTZDtype):
        raise ValueError(
            "'timestamp' column is tz-aware. This codebase's convention is "
            "naive-UTC throughout — fix the caller producing this frame "
            "rather than accepting tz-aware input here."
        )

    # Stable sort: preserves each bucket's real trade order, which the
    # 'first'/'last' aggregations below depend on for open/close.
    df = df.sort_values("timestamp", kind="mergesort")

    # Epoch-second floor division — the same alignment scheme
    # CandleBuilder._align() uses (ts // interval_seconds * interval_seconds),
    # not pandas' resample default (`origin='start_day'`, anchored to the
    # data's OWN first timestamp rather than a fixed epoch reference).
    #
    # datetime.timedelta, NOT pd.Timedelta: `pd.Timedelta(seconds=...)`
    # construction emits a numpy generic-unit DeprecationWarning on this
    # numpy/pandas pin (see tests/test_no_generic_timedelta_warning.py,
    # which statically bans pd.Timedelta(...) construction anywhere under
    # data/) and is scheduled to become a hard error on a future numpy major.
    epoch_seconds = (
        df["timestamp"] - pd.Timestamp("1970-01-01")
    ) // datetime.timedelta(seconds=1)
    bucket_start_epoch = (epoch_seconds // bucket_seconds) * bucket_seconds
    df["bucket"] = pd.to_datetime(bucket_start_epoch, unit="s")

    ohlcv = (
        df.groupby("bucket", sort=True)
        .agg(
            open=("price", "first"),
            high=("price", "max"),
            low=("price", "min"),
            close=("price", "last"),
            volume=("volume", "sum"),
        )
        .reset_index()
        .rename(columns={"bucket": "timestamp"})
    )

    return ohlcv[OHLCV_COLUMNS]
