"""
Whale-footprint features from public trades (roadmap Phase 2.3).
================================================================

Three features, computed from message-level trade records and aggregated to the
bar the strategy consumes. Each is a plain function over a window of
:class:`~recorder.shard_reader.Trade` and is independently testable;
:func:`whale_bar_features` is only the driver that walks the bars and maintains
the trailing baseline.

This module BUILDS AN INSTRUMENT. It contains no forward return, no correlation
against price, no information coefficient and no backtest, and none belongs
here: whether these features predict anything is a separately gated question,
and answering it inside the construction step would produce an ungated verdict
on data that is registered deny-by-default
(`campaign_data_policy.yaml:kraken_ws_forward_recorder`).

SIZE IS MEASURED IN QUOTE NOTIONAL
----------------------------------
Every definition below uses ``notional = price x qty`` (USD), never base
quantity. A whale is defined by dollars committed, and base quantity is not
comparable across pairs (1 BTC and 1 DOGE are four orders of magnitude apart)
nor across time within a pair as its price moves. Using base quantity would
make a fixed threshold drift with price and make any cross-pair pooling
meaningless.

SIGN IS THE TAKER'S SIDE
------------------------
Kraken WS v2 publishes ``side`` as the AGGRESSOR's side, so ``+notional`` for a
buy and ``-notional`` for a sell measures liquidity DEMAND. See
`shard_reader.TAKER_SIDES`.

THE DEFINITIONS
---------------

**(a) Large-trade imbalance** ``whale_lt_imbalance``, in [-1, +1].

    Over bar B, with size threshold tau:

        L    = { t in B : notional(t) >= tau }
        LTI  = sum_{t in L} sign(t) * notional(t)
               ---------------------------------
                    sum_{t in L} notional(t)

    A ratio, not a level: it answers "of the whale money that moved this bar,
    what fraction was one-directional", which is scale-free and directly
    comparable across pairs and across volume regimes. The raw signed sum is
    already feature (b) and is not duplicated here.

    ``tau`` is a QUANTILE OF THAT PAIR'S OWN trailing trade-notional
    distribution — never an absolute figure. $50k is a whale in ONDO and noise
    in BTC, and it is a different thing in the same pair six months later. The
    baseline is STRICTLY TRAILING (see below).

    NaN when the bar contains no trade at or above ``tau``, or when ``tau``
    itself is undefined. Not 0.0: zero asserts that whale flow was balanced,
    which is a measurement, and there was none to measure. The companion
    ``whale_lt_count`` column carries |L| so a consumer can tell the two apart.

    KNOWN DEGENERACY, stated rather than silently patched. The comparison is
    ``>=``, so if ``tau`` lands exactly on a REPEATED trade size, every copy of
    that size qualifies. Crypto trade sizes are lumpy — round numbers and
    bot-standard clip sizes recur — so in a thin pair the top-1% threshold can
    sit on an atom and admit several percent of trades instead of one. The
    feature then dilutes toward the sign of feature (b) and stops being about
    whales specifically. Switching to ``>`` only moves the failure: if the
    largest prints are a bot's identical clips, ``>`` admits nothing and the
    feature is NaN whenever it would matter most. Neither is right in general,
    so the definition keeps the standard ``>=`` reading and the degeneracy is
    made VISIBLE instead: ``whale_lt_count`` far above ~1% of
    ``whale_trade_count`` is the diagnostic, and it is a column the consumer
    already has.

**(b) Cumulative volume delta** ``whale_cvd_delta``, quote units, unbounded.

        CVD_delta(B) = sum_{t in B} sign(t) * notional(t)

    Emitted as the PER-BAR delta, not as a running total, and that is a
    deliberate choice rather than a shortcut. The running cumulative is
    ``cumsum`` of this column, one line for anyone who wants it — but its LEVEL
    depends entirely on where the capture happens to have started, so it is not
    comparable across windows, across recorder restarts, or across pairs. Worse,
    a cumulative running across an unattested gap silently bridges it: the
    level after the gap inherits the level before it as though nothing were
    missing, which is precisely the interpolation this whole read path exists to
    refuse. The delta localises the damage to the bars actually affected, which
    are the bars that get marked.

**(c) Trade-size distribution shift** ``whale_size_shift``, log units, signed.

        S(B) = ln( median{ notional(t) : t in B }
                   / median{ notional(t) : t in baseline(B) } )

    Positive means this bar's trades are running larger than the pair's own
    recent norm. A log RATIO OF MEDIANS, for two reasons. Median, not mean:
    trade notional is extremely heavy-tailed, and a mean shift would be driven
    by the same handful of large prints that feature (a) already measures, so
    the two would be near-redundant. Log ratio, not a difference: it is
    unit-free and symmetric, so a doubling and a halving are +/- the same
    magnitude.

    This is a LOCATION statistic, and calling it "distribution shift" is
    therefore a slight over-claim which is worth stating plainly. A full
    shape statistic (two-sample KS on log-notional) was considered and rejected:
    it is UNSIGNED, and an unsigned number cannot be turned into a directional
    forecast by the pipeline that consumes this, so it would have to be paired
    with a sign from somewhere else to be usable at all.

THE TRAILING BASELINE IS STRICTLY BEFORE THE BAR
------------------------------------------------
Both ``tau`` and the (c) denominator come from trades in
``[bar_start - baseline_seconds, bar_start)`` — strictly before the bar being
scored. Including the bar's own trades would be self-referential in exactly the
wrong direction: the bar's own whale print would raise the threshold meant to
detect it. It is also the only version of the baseline that is causal, so no
column here can see past its own bar's close, which is the same availability the
bar's own ``close`` has.

PARAMETERS AND WHY THESE DEFAULTS
---------------------------------
Every arbitrary choice is a keyword argument. The defaults:

``bar_seconds = 3600``
    The pipeline's bar. Every price cache the campaign reads is 1h
    (``local_data/kraken_<BASE>USD_1h.csv``) and the strategy's ``update()``
    fires at 1h candle completion. This is not a tuning choice; it is the
    frequency the consumer already runs at.

    It also happens to be the frequency at which feature (a) is not degenerate,
    which is MEASURED, not assumed: over the 2026-07-26/27 baseline capture at
    ``bar_seconds=60``, 51% of scored bars (51 of 100, across BTC/ETH/XRP/SOL)
    contained exactly ONE trade above ``tau``, so the ratio collapses to
    ``sign()`` and the feature carries a single bit. An hourly bar accumulates
    enough qualifying prints for the ratio to mean something.

``large_quantile = 0.99``
    Top 1% of the pair's own recent trades. At the rates measured in the
    baseline capture this leaves single digits of qualifying prints per hourly
    bar per pair: sparse enough that "whale" means something, dense enough that
    the feature is not almost-always NaN. 0.999 was rejected as too sparse at
    an hourly bar for the thinner pairs; 0.95 admits ordinary retail flow.
    Genuinely a choice within a range, which is why it is a parameter.

``baseline_seconds = 86400``
    One diurnal cycle. Shorter and the threshold tracks the time of day rather
    than the pair — an Asian-session hour would be scored against a US-session
    threshold. Longer and it starts averaging across regime change, which is the
    thing the feature is supposed to react to.

``min_baseline_trades = 200``
    A 0.99 quantile estimated from fewer than ~200 samples is set by one or two
    observations and is not a quantile in any useful sense. Below this floor the
    bar is NOT scored — NaN and ``whale_attested`` unaffected — rather than
    scored against a threshold nobody should trust.

``min_bar_trades = 10``
    A median from under ~10 trades is noise. Same treatment: not scored.

GAPS ARE MARKED, NOT INTERPOLATED
---------------------------------
The driver consumes the ``Trade | Gap`` stream from
`shard_reader.ShardReader.iter_trades`. Any bar whose span intersects a
:class:`~recorder.shard_reader.Gap` gets ``whale_attested = 0.0`` and every
feature column set to NaN, however many trades were captured inside it. A bar
that is 90% captured is not 90% of a measurement — the missing 10% is where the
whale print would be, and a partially-captured bar that reports a number is
indistinguishable downstream from a fully-captured one. Attested-but-quiet is a
different thing and is scored normally (``whale_attested = 1.0``,
``whale_trade_count = 0``), which is the differential-guard property inherited
from ``base_fetcher._assert_no_new_gap``.

MEMORY
------
The driver materialises the requested window's trades. That is bounded work per
call because `BaseFetcher` already chunks by missing period, and a day of one
pair's trades is small; do not point it at twelve months in one call.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Deque, Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

if __package__ in (None, ""):  # allow direct execution
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.shard_reader import Gap, Trade, as_naive_utc  # type: ignore
else:
    from .shard_reader import Gap, Trade, as_naive_utc

DEFAULT_BAR_SECONDS = 3600
DEFAULT_LARGE_QUANTILE = 0.99
DEFAULT_BASELINE_SECONDS = 24 * 3600
DEFAULT_MIN_BASELINE_TRADES = 200
DEFAULT_MIN_BAR_TRADES = 10

#: The emitted columns, in order. One FEED_REGISTRY entry per column: the bot's
#: `_premerge_aux_feeds` (data_manager.py:622) attaches only the column whose
#: name equals the registered feed name, so a multi-column feed reaches the
#: strategy only if each column is registered under its own name.
FEATURE_COLUMNS = (
    "whale_lt_imbalance",
    "whale_lt_count",
    "whale_cvd_delta",
    "whale_size_shift",
    "whale_trade_count",
    "whale_attested",
)

#: Columns that are NaN-ed when a bar is not fully attested. `whale_attested`
#: and the count columns are excluded: they are the marking itself.
_VALUE_COLUMNS = ("whale_lt_imbalance", "whale_cvd_delta", "whale_size_shift")


# ---------------------------------------------------------------------------
# The three features, each a pure function over one window
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LargeTradeImbalance:
    """Result of :func:`large_trade_imbalance`."""

    value: float  # NaN when no trade qualified
    count: int
    gross_notional: float


def size_threshold(
    baseline_notionals: Sequence[float],
    quantile: float = DEFAULT_LARGE_QUANTILE,
    min_samples: int = DEFAULT_MIN_BASELINE_TRADES,
) -> float:
    """
    ``tau``: the `quantile`-th quantile of a pair's own trailing trade
    notionals.

    Returns NaN when there are fewer than `min_samples` — see the module
    docstring on ``min_baseline_trades``. Linear interpolation between order
    statistics (numpy's default) rather than a nearest-rank rule, so ``tau``
    moves continuously as the baseline rolls instead of stepping between
    individual observations.
    """
    if not 0.0 < quantile < 1.0:
        raise ValueError(f"quantile must be in (0, 1), got {quantile}")
    if len(baseline_notionals) < min_samples:
        return math.nan
    return float(np.quantile(np.asarray(baseline_notionals, dtype=float), quantile))


def large_trade_imbalance(
    trades: Iterable[Trade], threshold: float
) -> LargeTradeImbalance:
    """
    Feature (a). Signed share of the bar's LARGE-trade notional.

    ``sum(sign * notional) / sum(notional)`` over trades at or above
    `threshold`, in [-1, +1]. NaN when nothing qualified or `threshold` is NaN.
    """
    if threshold != threshold:  # NaN
        return LargeTradeImbalance(value=math.nan, count=0, gross_notional=0.0)
    signed = 0.0
    gross = 0.0
    count = 0
    for t in trades:
        n = t.notional
        if n >= threshold:
            signed += t.sign * n
            gross += n
            count += 1
    if count == 0 or gross <= 0.0:
        return LargeTradeImbalance(value=math.nan, count=count, gross_notional=gross)
    return LargeTradeImbalance(value=signed / gross, count=count, gross_notional=gross)


def cumulative_volume_delta(trades: Iterable[Trade]) -> float:
    """
    Feature (b). Signed notional over the window: taker buys minus taker sells.

    Per-bar delta. The running cumulative is this column's ``cumsum`` and is
    deliberately not what is emitted — see the module docstring.
    """
    return float(sum(t.signed_notional for t in trades))


def trade_size_shift(
    trades: Sequence[Trade],
    baseline_notionals: Sequence[float],
    min_bar_trades: int = DEFAULT_MIN_BAR_TRADES,
    min_baseline_trades: int = DEFAULT_MIN_BASELINE_TRADES,
) -> float:
    """
    Feature (c). ``ln(median bar notional / median baseline notional)``.

    NaN when either sample is under its floor, or when the baseline median is
    non-positive (which a positive-notional baseline cannot produce, but a
    caller-supplied one could).
    """
    if len(trades) < min_bar_trades or len(baseline_notionals) < min_baseline_trades:
        return math.nan
    bar_med = float(np.median([t.notional for t in trades]))
    base_med = float(np.median(np.asarray(baseline_notionals, dtype=float)))
    if bar_med <= 0.0 or base_med <= 0.0:
        return math.nan
    return math.log(bar_med / base_med)


# ---------------------------------------------------------------------------
# Driver: message-level -> bar-level
# ---------------------------------------------------------------------------


def bar_floor(ts: datetime, bar_seconds: int) -> datetime:
    """Open time of the bar containing `ts`, on the UTC epoch grid."""
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    n = int((ts.astimezone(timezone.utc) - epoch).total_seconds()) // bar_seconds
    return epoch + timedelta(seconds=n * bar_seconds)


def whale_bar_features(
    stream: Iterable[Union[Trade, Gap]],
    bar_seconds: int = DEFAULT_BAR_SECONDS,
    large_quantile: float = DEFAULT_LARGE_QUANTILE,
    baseline_seconds: int = DEFAULT_BASELINE_SECONDS,
    min_baseline_trades: int = DEFAULT_MIN_BASELINE_TRADES,
    min_bar_trades: int = DEFAULT_MIN_BAR_TRADES,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> pd.DataFrame:
    """
    Aggregate one symbol's ``Trade | Gap`` stream to a complete bar grid.

    Returns a DataFrame with a naive-UTC ``timestamp`` column (bar OPEN time,
    matching the OHLCV caches) plus :data:`FEATURE_COLUMNS`. EVERY bar in the
    covered range gets a row, including bars with no trades and bars that are
    not attested — a missing row would be indistinguishable from a bar the
    consumer never asked for, and `merge_asof(direction='backward')` would then
    carry a neighbouring bar's value across the hole.

    Trades are binned by VENUE EVENT TIME (``Trade.ts``), which is the economic
    clock. Gaps are wall-clock spans of the RECORDER's clock; a bar is marked
    unattested if its span intersects any gap.
    """
    if bar_seconds <= 0:
        raise ValueError("bar_seconds must be positive")

    trades: List[Trade] = []
    gaps: List[Gap] = []
    for item in stream:
        if isinstance(item, Gap):
            gaps.append(item)
        elif isinstance(item, Trade):
            trades.append(item)
        else:
            raise TypeError(
                f"stream yielded {type(item).__name__}; expected Trade or Gap. "
                "Pass ShardReader.iter_trades(...) directly rather than filtering "
                "the Gap markers out of it."
            )

    trades.sort(key=lambda t: (t.ts, t.trade_id))

    if start is None:
        candidates = [t.ts for t in trades] + [g.start for g in gaps]
        if not candidates:
            return pd.DataFrame(columns=["timestamp", *FEATURE_COLUMNS])
        start = min(candidates)
    if end is None:
        candidates = [t.ts for t in trades] + [g.end for g in gaps]
        if not candidates:
            return pd.DataFrame(columns=["timestamp", *FEATURE_COLUMNS])
        end = max(candidates)
    if end < start:
        raise ValueError("end precedes start")

    step = timedelta(seconds=bar_seconds)
    baseline_window = timedelta(seconds=baseline_seconds)

    # Trailing baseline: (ts, notional) for trades strictly before the current
    # bar's open, within `baseline_seconds`. Bounded by the window, not by count.
    baseline: Deque[Tuple[datetime, float]] = deque()
    cursor = 0  # index into `trades` of the first trade not yet in the baseline

    rows = []
    bar_start = bar_floor(start, bar_seconds)
    # [start, end] is INCLUSIVE at both ends, matching `journal.uncovered` and
    # `assert_covered`, so the bar CONTAINING `end` is always emitted. When
    # `end` lands exactly on a boundary that trailing bar is usually empty —
    # which is deliberate and not an off-by-one: `end` is defaulted from the
    # last trade's timestamp, and that trade lives in the bar starting at `end`.
    # Dropping it to avoid the empty case would drop a bar with data in it.
    last_start = bar_floor(end, bar_seconds)
    while bar_start <= last_start:
        bar_end = bar_start + step

        # Admit every trade that closed before this bar opened, then evict what
        # has rolled out of the baseline window. Done in this order so the
        # baseline is exactly [bar_start - baseline_seconds, bar_start).
        while cursor < len(trades) and trades[cursor].ts < bar_start:
            baseline.append((trades[cursor].ts, trades[cursor].notional))
            cursor += 1
        cutoff = bar_start - baseline_window
        while baseline and baseline[0][0] < cutoff:
            baseline.popleft()
        baseline_notionals = [n for _ts, n in baseline]

        # `cursor` is now the first trade at or after `bar_start`, so the bar's
        # slice starts there. Two pointers over a sorted list keeps the whole
        # walk O(trades + bars); re-scanning `trades` per bar would be O(n*m)
        # and is what makes a naive version unusable on a multi-month window.
        j = cursor
        while j < len(trades) and trades[j].ts < bar_end:
            j += 1
        in_bar = trades[cursor:j]
        attested = not any(g.start < bar_end and g.end > bar_start for g in gaps)

        tau = size_threshold(baseline_notionals, large_quantile, min_baseline_trades)
        lti = large_trade_imbalance(in_bar, tau)
        row = {
            "timestamp": as_naive_utc(bar_start),
            "whale_lt_imbalance": lti.value,
            "whale_lt_count": float(lti.count),
            "whale_cvd_delta": cumulative_volume_delta(in_bar),
            "whale_size_shift": trade_size_shift(
                in_bar, baseline_notionals, min_bar_trades, min_baseline_trades
            ),
            "whale_trade_count": float(len(in_bar)),
            "whale_attested": 1.0 if attested else 0.0,
        }
        if not attested:
            for col in _VALUE_COLUMNS:
                row[col] = math.nan
        rows.append(row)
        bar_start = bar_end

    return pd.DataFrame(rows, columns=["timestamp", *FEATURE_COLUMNS])
