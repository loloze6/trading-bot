"""
Sign persistence of the whale-footprint features (dispatch W11 step 1).
=======================================================================

    python -m recorder.whale_persistence [--root DIR] [--start ISO8601] ...

Answers ONE question: how many bars does each whale feature's own SIGN persist
for, measured with the campaign's own operational definition of
``avg_holding_bars``.

WHY THIS FILE EXISTS
--------------------
`prereg_whale_footprint_v2.yaml` gates on an economic required-IC computed as

    IC_required = safety_factor * round_trip_cost_bps / (sigma_bar_bps * sqrt(H))

and until dispatch W11 the ``H`` in that expression was 5.74 — a figure
BORROWED from archived Keltner/MACD runs on BTC/AVAX (dispatch W10 step 2). It
was a defensible stand-in when nothing better existed, but it is a property of
those strategies' forecasts, not of these features. A gate whose threshold is
set by a different signal's turnover is not measuring this one. This module
measures it from the capture the pre-registration actually names.

WHAT THIS DELIBERATELY DOES NOT COMPUTE
---------------------------------------
No price. No return. No correlation. No information coefficient. Not as a
matter of restraint but as a matter of CONSTRUCTION: this module imports no
price loader, opens no OHLCV cache, and reads only the `trades` stream through
`ShardReader`. There is no code path here that could relate a feature to a
return, which is what makes it safe to run against a registered
deny-by-default capture (`campaign_data_policy.yaml:kraken_ws_forward_recorder`)
BEFORE the pre-registration fires. A number derived here cannot encode a peek at
the hypothesis, because the hypothesis is about feature-vs-return and this file
cannot see a return.

The companion measurement — per-bar return volatility, `sigma_bar_bps` — lives
in `strategy-research/tools/measure_bar_sigma.py` and reads ONLY prices, never
whale features. The two inputs to the required-IC derivation are measured by two
programs that share no data, which is the structural form of "this amendment is
not a peek".

THE DEFINITION, AND WHY IT IS THE CAMPAIGN'S AND NOT A NEW ONE
--------------------------------------------------------------
Transcribed from `tools/prescreen_signal.py:505-545` (`_compute_turnover_proxy`),
which every Layer-2 cost decision in this campaign already uses:

    a trade boundary is an ACTIVITY transition, not a sign transition.
    inactive -> active OPENS a trade; active -> inactive CLOSES it; a direct
    sign flip (long -> short with no flat bar between) closes the old side and
    opens the new one in the same bar, counted as ONE open.

    avg_holding_bars = active_bars_total / max(opens, 1)

Applied here to each feature's own value in place of ``r["forecast"]``, with the
same ``_ACTIVE_THRESHOLD`` of 1e-6. That substitution is the whole adaptation:
a forecast is a signed number per bar and so is a whale feature, and the
quantity the cost model wants — how long one directional exposure lasts before
it is closed — is the same quantity in both cases.

TWO PLACES WHERE THE ANALOGY NEEDS A DECISION, BOTH MADE EXPLICIT
------------------------------------------------------------------
**NaN is FLAT, not missing.** `prescreen_signal` records a bar once the strategy
`is_ready()`, and a bar the strategy declines to trade appears as forecast 0.0 —
an inactive bar that ends an episode. A whale feature is NaN for the exactly
analogous reason (`whale_features` docstring: no trade cleared ``tau``, or the
bar was too thin to score), so NaN maps to sign 0. Treating NaN as "skip this
bar" instead would BRIDGE quiet bars and inflate H, which is the same failure
mode the sign-flip-only counter had before 2026-07-07 (see
`_compute_turnover_proxy`'s own docstring on the P4_ts_trend finding). The
alternative is reported anyway, as `avg_holding_bars_nan_bridged`, so the
choice is visible rather than buried: if the two diverge a lot, that IS the
finding.

**Episodes do not cross an unattested gap.** Bars with ``whale_attested == 0``
are dropped and the surrounding attested bars are NOT joined into one episode —
each attested run is walked as its own record list, exactly as
`_compute_turnover_proxy` refuses to pool across a symbol boundary and for the
same reason: a value on either side of a hole says nothing about what the sign
did inside it, and stitching them asserts a persistence that was never observed.

STABILITY
---------
``avg_holding_bars`` is a ratio whose denominator is a small count of episodes.
Its relative standard error is approximately ``1/sqrt(opens)``, so an estimate
resting on a handful of episodes is not an estimate. :func:`stability_verdict`
turns that into an explicit pass/fail against `MIN_OPENS_FOR_STABLE_H` rather
than letting a caller read a number that happens to be printed. A capture too
short to support the estimate must say so — reporting an unstable H as though it
were measured is precisely how the borrowed 5.74 became load-bearing in the
first place.
"""

from __future__ import annotations

import argparse
import math
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

if __package__ in (None, ""):  # allow direct execution
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.shard_reader import ShardReader  # type: ignore
    from recorder.whale_features import (  # type: ignore
        DEFAULT_BAR_SECONDS,
        DEFAULT_BASELINE_SECONDS,
        DEFAULT_LARGE_QUANTILE,
        DEFAULT_MIN_BAR_TRADES,
        DEFAULT_MIN_BASELINE_TRADES,
        whale_bar_features,
    )
else:
    from .shard_reader import ShardReader
    from .whale_features import (
        DEFAULT_BAR_SECONDS,
        DEFAULT_BASELINE_SECONDS,
        DEFAULT_LARGE_QUANTILE,
        DEFAULT_MIN_BAR_TRADES,
        DEFAULT_MIN_BASELINE_TRADES,
        whale_bar_features,
    )

DEFAULT_ROOT = (
    Path(__file__).resolve().parents[3]
    / "trading-bot"
    / "local_data"
    / "recorded_reserved"
    / "kraken_ws_v2"
)

#: The three features the pre-registration names. `whale_lt_count`,
#: `whale_trade_count` and `whale_attested` are bookkeeping columns, not signals,
#: and have no sign to persist.
SIGNAL_COLUMNS = ("whale_lt_imbalance", "whale_cvd_delta", "whale_size_shift")

#: Verbatim from prescreen_signal.py:99. Kept as a separate constant rather than
#: imported so this module has no dependency on the backtest-facing tool tree.
ACTIVE_THRESHOLD = 1e-6

#: Minimum number of OPENS (episodes) before an avg_holding_bars estimate is
#: PRECISE enough to use. At `opens` episodes the ratio's relative standard error
#: is ~1/sqrt(opens); 30 gives ~18%, which is the loosest precision at which the
#: sqrt(H) term in the required-IC formula moves that IC by less than ~10%.
#: Pre-registered here, not tuned to whatever the capture happens to contain.
MIN_OPENS_FOR_STABLE_H = 30

#: Maximum fraction of episodes that may be RIGHT-CENSORED before
#: `avg_holding_bars` stops being an estimate of H and becomes a lower bound on
#: it. An episode is right-censored when it is still active at the last bar of
#: its attested segment: the capture ends the episode, not the signal, so its
#: true length is unknown and only known to be AT LEAST what was observed.
#:
#: This is a SEPARATE failure mode from imprecision and it is the one that bites
#: a short or gap-riddled capture. Precision improves with more episodes;
#: censoring does not improve with more episodes at all — it improves only with
#: LONGER UNBROKEN attested runs. A capture chopped into 1.5-bar segments can
#: accumulate thousands of episodes and still be unable to distinguish H=2 from
#: H=50, because no episode in it is allowed to last longer than its segment.
#: Reporting the censored mean as "measured H" in that situation understates H
#: without bound, and since IC_required scales as 1/sqrt(H) it would OVERSTATE
#: the required IC — the exact direction of the error dispatch W10 withdrew.
#: 0.20 is the conventional threshold above which a naive (censoring-ignoring)
#: mean is not reported as a point estimate in survival analysis.
MAX_CENSORED_FRACTION = 0.20


@dataclass
class PersistenceResult:
    """One (symbol, feature) measurement, or a pooled one when `symbol` is None."""

    symbol: Optional[str]
    feature: str
    bars_total: int = 0
    bars_attested: int = 0
    active_bars: int = 0
    opens: int = 0
    segments: int = 0
    #: Episodes still active at the last bar of their attested segment — the
    #: capture cut them off, so their observed length is a lower bound.
    censored_episodes: int = 0
    #: Lengths of every attested run, in bars. The ceiling on any episode.
    segment_lengths: List[int] = field(default_factory=list)
    #: Primary estimate: NaN counted as flat, episodes broken at unattested gaps.
    avg_holding_bars: Optional[float] = None
    #: Sensitivity: NaN bars dropped so an episode bridges quiet bars.
    avg_holding_bars_nan_bridged: Optional[float] = None
    #: Numerator/denominator of the bridged variant, carried separately so
    #: `pool` can add them instead of averaging the per-symbol ratios.
    bridged_active_bars: int = 0
    bridged_opens: int = 0
    episode_lengths: List[int] = field(default_factory=list)

    @property
    def precise(self) -> bool:
        """Enough episodes for the ratio's sampling error to be tolerable."""
        return self.opens >= MIN_OPENS_FOR_STABLE_H

    @property
    def censored_fraction(self) -> Optional[float]:
        n = len(self.episode_lengths)
        return (self.censored_episodes / n) if n else None

    @property
    def uncensored(self) -> bool:
        """Few enough truncated episodes that the mean is an estimate, not a bound."""
        cf = self.censored_fraction
        return cf is not None and cf <= MAX_CENSORED_FRACTION

    @property
    def stable(self) -> bool:
        """Usable as a measured input: BOTH precise and materially uncensored."""
        return self.precise and self.uncensored

    @property
    def relative_se(self) -> Optional[float]:
        """Approximate relative standard error of `avg_holding_bars`."""
        return 1.0 / math.sqrt(self.opens) if self.opens > 0 else None

    @property
    def max_observable_h(self) -> Optional[float]:
        """
        The largest H this capture's segment structure could ever have produced.

        An episode cannot outlive its segment, so the longest attested run is a
        hard ceiling on any measured holding period. When `avg_holding_bars` sits
        near this ceiling, the number is describing the CAPTURE, not the signal.
        """
        return float(max(self.segment_lengths)) if self.segment_lengths else None


def _signs(values: Sequence[float], nan_is_flat: bool = True) -> List[int]:
    """
    Map a feature's values to the tri-state sign series `_compute_turnover_proxy`
    walks. NaN -> 0 (flat) under the primary convention; dropped entirely under
    the bridged sensitivity.
    """
    out: List[int] = []
    for v in values:
        if v is None or (isinstance(v, float) and math.isnan(v)):
            if nan_is_flat:
                out.append(0)
            continue
        if v > ACTIVE_THRESHOLD:
            out.append(1)
        elif v < -ACTIVE_THRESHOLD:
            out.append(-1)
        else:
            out.append(0)
    return out


def turnover_from_sign_segments(segments: Sequence[Sequence[int]]) -> Dict[str, object]:
    """
    `_compute_turnover_proxy` (prescreen_signal.py:505-545) over pre-computed sign
    series, one series per segment.

    A segment plays the role a SYMBOL plays there: `prev_sign` resets at every
    segment boundary, so no episode is counted as continuing across one. Here a
    segment is an attested run within one symbol, for the reason in the module
    docstring.
    """
    total_active = 0
    total_opens = 0
    censored = 0
    lengths: List[int] = []
    for signs in segments:
        prev_sign = 0
        run = 0
        for curr_sign in signs:
            if curr_sign != 0:
                total_active += 1
                if curr_sign != prev_sign:
                    total_opens += 1
                    if run:
                        lengths.append(run)
                    run = 1
                else:
                    run += 1
            elif run:
                lengths.append(run)
                run = 0
            prev_sign = curr_sign
        if run:
            # Still active when the segment ran out. The episode was ended by
            # the edge of the capture, not by the signal going flat or flipping,
            # so `run` is a lower bound on its true length. Counted so the caller
            # can tell an estimate from a censored bound.
            lengths.append(run)
            censored += 1
    implied = max(total_opens, 1)
    return {
        "active_bars_total": total_active,
        "implied_trades_estimated": implied,
        "avg_holding_bars": (total_active / implied) if total_active else None,
        "opens": total_opens,
        "censored_episodes": censored,
        "episode_lengths": lengths,
    }


def _attested_segments(df: pd.DataFrame, column: str) -> List[List[float]]:
    """Split one feature column into runs of consecutive ATTESTED bars."""
    segments: List[List[float]] = []
    current: List[float] = []
    for attested, value in zip(df["whale_attested"].tolist(), df[column].tolist()):
        if attested >= 1.0:
            current.append(value)
        elif current:
            segments.append(current)
            current = []
    if current:
        segments.append(current)
    return segments


def measure_symbol(df: pd.DataFrame, symbol: str) -> Dict[str, PersistenceResult]:
    """Every feature's persistence for one symbol's bar frame."""
    results: Dict[str, PersistenceResult] = {}
    n_att = int(df["whale_attested"].sum()) if len(df) else 0
    for col in SIGNAL_COLUMNS:
        segs = _attested_segments(df, col) if len(df) else []
        primary = turnover_from_sign_segments([_signs(s, True) for s in segs])
        bridged = turnover_from_sign_segments([_signs(s, False) for s in segs])
        results[col] = PersistenceResult(
            symbol=symbol,
            feature=col,
            bars_total=len(df),
            bars_attested=n_att,
            active_bars=int(primary["active_bars_total"]),
            opens=int(primary["opens"]),
            segments=len(segs),
            censored_episodes=int(primary["censored_episodes"]),
            segment_lengths=[len(s) for s in segs],
            avg_holding_bars=primary["avg_holding_bars"],  # type: ignore[arg-type]
            avg_holding_bars_nan_bridged=bridged["avg_holding_bars"],  # type: ignore[arg-type]
            bridged_active_bars=int(bridged["active_bars_total"]),
            bridged_opens=int(bridged["opens"]),
            episode_lengths=list(primary["episode_lengths"]),  # type: ignore[arg-type]
        )
    return results


def pool(results: Sequence[PersistenceResult], feature: str) -> PersistenceResult:
    """
    Pool one feature across symbols the way `_compute_turnover_proxy` does: sum
    the numerators and the denominators, never average the per-symbol ratios. A
    mean of ratios would weight a pair with two episodes the same as one with
    two hundred.
    """
    pooled = PersistenceResult(symbol=None, feature=feature)
    for r in results:
        if r.feature != feature:
            continue
        pooled.bars_total += r.bars_total
        pooled.bars_attested += r.bars_attested
        pooled.active_bars += r.active_bars
        pooled.opens += r.opens
        pooled.segments += r.segments
        pooled.censored_episodes += r.censored_episodes
        pooled.bridged_active_bars += r.bridged_active_bars
        pooled.bridged_opens += r.bridged_opens
        pooled.segment_lengths.extend(r.segment_lengths)
        pooled.episode_lengths.extend(r.episode_lengths)
    if pooled.active_bars:
        pooled.avg_holding_bars = pooled.active_bars / max(pooled.opens, 1)
    if pooled.bridged_active_bars:
        pooled.avg_holding_bars_nan_bridged = pooled.bridged_active_bars / max(
            pooled.bridged_opens, 1
        )
    return pooled


def stability_verdict(
    pooled: Sequence[PersistenceResult],
    n_pairs: int = 19,
    target_h: float = 5.74,
) -> Dict[str, object]:
    """
    Whether the capture supports a usable H, and if not, what capture would.

    TWO independent conditions, reported separately because they fail for
    different reasons and are fixed by different things:

    **Precision** — enough episodes for the ratio to have a tolerable standard
    error. Fixed by MORE CAPTURE TIME; the shortfall is quoted as the extra
    attested bars per pair needed at the observed opens-per-attested-bar rate.

    **Censoring** — episodes long enough to be observed ending. Fixed ONLY by
    LONGER UNBROKEN ATTESTED RUNS, and NOT by more capture time: chopping twice
    as much data into segments of the same length yields twice as many episodes
    that are all still truncated at the same ceiling. The shortfall is therefore
    quoted as a required segment length, and separately as the per-bar
    interruption rate that would produce it, since the segment length is set by
    how often the capture is interrupted and not by how long it runs.

    `target_h` is the H the estimate must be able to RESOLVE — defaulting to the
    5.74 currently registered in `prereg_whale_footprint_v2.yaml`, since the
    question this tool exists to answer is whether the capture can confirm or
    refute that specific figure. A capture whose segments cannot hold a 5.74-bar
    episode cannot refute 5.74 no matter what mean it prints.
    """
    worst_precision = min(pooled, key=lambda r: r.opens)
    worst_censor = max(
        pooled,
        key=lambda r: r.censored_fraction if r.censored_fraction is not None else 0.0,
    )

    rate = (
        (worst_precision.opens / worst_precision.bars_attested)
        if worst_precision.bars_attested
        else 0.0
    )
    needed_pooled_bars = math.ceil(MIN_OPENS_FOR_STABLE_H / rate) if rate > 0 else None
    extra_bars_per_pair = None
    if needed_pooled_bars is not None:
        shortfall = max(needed_pooled_bars - worst_precision.bars_attested, 0)
        extra_bars_per_pair = math.ceil(shortfall / n_pairs)

    seg_lengths = [n for r in pooled for n in r.segment_lengths]
    mean_seg = (sum(seg_lengths) / len(seg_lengths)) if seg_lengths else 0.0
    max_seg = max(seg_lengths) if seg_lengths else 0

    # To keep censoring under MAX_CENSORED_FRACTION for episodes of mean length
    # `target_h`, a segment must fit several episodes end to end: with episodes
    # arriving in a segment of length S, roughly S/target_h of them fit and the
    # last one is the censored one, so censored_fraction ~ target_h / S. Solving
    # S >= target_h / MAX_CENSORED_FRACTION.
    required_segment_bars = math.ceil(target_h / MAX_CENSORED_FRACTION)
    # A segment ends at every interruption, so the mean segment length is ~the
    # reciprocal of the per-bar interruption rate. Inverting gives the rate the
    # recorder would have to achieve.
    observed_interrupt_rate = (1.0 / mean_seg) if mean_seg > 0 else None
    required_interrupt_rate = 1.0 / required_segment_bars

    return {
        "precise": all(r.precise for r in pooled),
        "uncensored": all(r.uncensored for r in pooled),
        "stable": all(r.stable for r in pooled),
        # precision
        "limiting_precision_feature": worst_precision.feature,
        "limiting_opens": worst_precision.opens,
        "min_opens_required": MIN_OPENS_FOR_STABLE_H,
        "opens_per_attested_bar": round(rate, 4) if rate else None,
        "observed_attested_bars_pooled": worst_precision.bars_attested,
        "pooled_attested_bars_needed": needed_pooled_bars,
        "extra_attested_bars_per_pair": extra_bars_per_pair,
        # censoring
        "limiting_censor_feature": worst_censor.feature,
        "worst_censored_fraction": (
            round(worst_censor.censored_fraction, 4)
            if worst_censor.censored_fraction is not None
            else None
        ),
        "max_censored_fraction_allowed": MAX_CENSORED_FRACTION,
        "mean_attested_segment_bars": round(mean_seg, 3),
        "max_attested_segment_bars": max_seg,
        "target_h_to_resolve": target_h,
        "required_segment_bars": required_segment_bars,
        "observed_interruptions_per_bar": (
            round(observed_interrupt_rate, 4) if observed_interrupt_rate else None
        ),
        "required_interruptions_per_bar": round(required_interrupt_rate, 4),
    }


def report(
    root: Path,
    symbols: Optional[Sequence[str]] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    bar_seconds: int = DEFAULT_BAR_SECONDS,
    large_quantile: float = DEFAULT_LARGE_QUANTILE,
    baseline_seconds: int = DEFAULT_BASELINE_SECONDS,
    min_baseline_trades: int = DEFAULT_MIN_BASELINE_TRADES,
    min_bar_trades: int = DEFAULT_MIN_BAR_TRADES,
) -> str:
    reader = ShardReader(root)
    man = reader.manifest()
    syms = list(symbols) if symbols else man.streams.get("trades", [])
    t0 = pd.Timestamp(start).to_pydatetime() if start else None
    t1 = pd.Timestamp(end).to_pydatetime() if end else None

    out: List[str] = [
        "=" * 96,
        "WHALE FEATURE SIGN PERSISTENCE  (no price, no return, no IC — see module docstring)",
        "=" * 96,
        f"root            {root}",
        f"window          {start or '(journal start)'} .. {end or '(journal end)'}",
        f"definition      prescreen_signal.py:505-545 _compute_turnover_proxy, "
        f"active_threshold={ACTIVE_THRESHOLD}",
        f"params          bar_seconds={bar_seconds} large_quantile={large_quantile} "
        f"baseline_seconds={baseline_seconds}",
        f"                min_baseline_trades={min_baseline_trades} min_bar_trades={min_bar_trades}",
        "",
    ]

    all_results: List[PersistenceResult] = []
    header = (
        f"{'pair':<9}{'bars':>6}{'att':>5}{'seg':>5}  {'feature':<20}"
        f"{'active':>8}{'opens':>7}{'H':>9}{'H_brdg':>9}{'relSE':>8}"
    )
    out += [header, "-" * len(header)]
    for sym in syms:
        stream = reader.iter_trades(symbols=[sym], start=t0, end=t1, emit_gaps=True)
        df = whale_bar_features(
            stream,
            bar_seconds=bar_seconds,
            large_quantile=large_quantile,
            baseline_seconds=baseline_seconds,
            min_baseline_trades=min_baseline_trades,
            min_bar_trades=min_bar_trades,
        )
        per_feature = measure_symbol(df, sym)
        for col in SIGNAL_COLUMNS:
            r = per_feature[col]
            all_results.append(r)
            out.append(
                f"{sym if col == SIGNAL_COLUMNS[0] else '':<9}"
                f"{r.bars_total if col == SIGNAL_COLUMNS[0] else '':>6}"
                f"{r.bars_attested if col == SIGNAL_COLUMNS[0] else '':>5}"
                f"{r.segments if col == SIGNAL_COLUMNS[0] else '':>5}  {col:<20}"
                f"{r.active_bars:>8}{r.opens:>7}"
                f"{_num(r.avg_holding_bars):>9}{_num(r.avg_holding_bars_nan_bridged):>9}"
                f"{_num(r.relative_se, 3):>8}"
            )

    pooled = [pool(all_results, c) for c in SIGNAL_COLUMNS]

    att = sum(r.bars_attested for r in all_results if r.feature == SIGNAL_COLUMNS[0])
    tot = sum(r.bars_total for r in all_results if r.feature == SIGNAL_COLUMNS[0])
    out += [
        "-" * len(header),
        "",
        f"ATTESTED-BAR FRACTION  {att}/{tot} = {att / tot:.4f}"
        if tot
        else "ATTESTED-BAR FRACTION  (no bars)",
        "  NB this is a BAR fraction, not the journal's TIME-coverage fraction. A bar is",
        "  attested only if NO gap of any length touches it, so a 2-second reconnect",
        "  costs a whole 1h bar. The two figures are not interchangeable.",
        "",
        "POOLED ACROSS PAIRS  (sum of numerators / sum of denominators)",
    ]
    ph = (
        f"{'feature':<20}{'active':>8}{'opens':>7}{'H':>9}{'H_brdg':>9}"
        f"{'relSE':>8}{'ep_med':>8}{'ep_p90':>8}{'ep_max':>8}{'cens%':>8}  verdict"
    )
    out += [ph, "-" * len(ph)]
    for r in pooled:
        eps = r.episode_lengths
        why = "OK" if r.stable else ("CENSORED" if not r.uncensored else "IMPRECISE")
        out.append(
            f"{r.feature:<20}{r.active_bars:>8}{r.opens:>7}"
            f"{_num(r.avg_holding_bars):>9}{_num(r.avg_holding_bars_nan_bridged):>9}"
            f"{_num(r.relative_se, 3):>8}"
            f"{(f'{statistics.median(eps):.1f}' if eps else '-'):>8}"
            f"{(f'{np.percentile(eps, 90):.1f}' if eps else '-'):>8}"
            f"{(str(max(eps)) if eps else '-'):>8}"
            f"{_num(r.censored_fraction, 3):>8}  {why}"
        )

    per_pair_H = {
        c: [
            r.avg_holding_bars
            for r in all_results
            if r.feature == c and r.avg_holding_bars is not None
        ]
        for c in SIGNAL_COLUMNS
    }
    out += ["", "DISPERSION OF PER-PAIR H  (pairs with a defined H only)"]
    dh = f"{'feature':<20}{'n_pairs':>9}{'min':>9}{'median':>9}{'max':>9}{'stdev':>9}"
    out += [dh, "-" * len(dh)]
    for c in SIGNAL_COLUMNS:
        vals = per_pair_H[c]
        out.append(
            f"{c:<20}{len(vals):>9}"
            f"{(f'{min(vals):.4f}' if vals else '-'):>9}"
            f"{(f'{statistics.median(vals):.4f}' if vals else '-'):>9}"
            f"{(f'{max(vals):.4f}' if vals else '-'):>9}"
            f"{(f'{statistics.stdev(vals):.4f}' if len(vals) > 1 else '-'):>9}"
        )

    seg_all = [n for r in pooled for n in r.segment_lengths]
    out += [
        "",
        "ATTESTED SEGMENT LENGTHS  (the hard ceiling on any episode)",
        f"  segments {len(seg_all)}   mean {sum(seg_all) / len(seg_all):.3f} bars   "
        f"median {statistics.median(seg_all):.1f}   max {max(seg_all)} bars"
        if seg_all
        else "  (none)",
    ]

    v = stability_verdict(pooled)
    out += ["", "=" * 96, "STABILITY VERDICT", "=" * 96]
    if v["stable"]:
        out += [
            f"STABLE. Every feature clears both conditions ({MIN_OPENS_FOR_STABLE_H}+ pooled "
            f"opens, censoring <= {MAX_CENSORED_FRACTION:.0%}); the H figures above may be "
            f"used as a measured input.",
        ]
    else:
        out += [
            "NOT STABLE — the H figures above are NOT a usable measured input.",
            "",
            f"  PRECISION  {'PASS' if v['precise'] else 'FAIL'}",
            f"    limiting feature      {v['limiting_precision_feature']} at "
            f"{v['limiting_opens']} pooled opens (need {v['min_opens_required']})",
            f"    observed rate         {v['opens_per_attested_bar']} opens per attested bar",
            f"    pooled attested bars  {v['observed_attested_bars_pooled']} now; "
            f"~{v['pooled_attested_bars_needed']} needed at that rate",
            f"    shortfall             ~{v['extra_attested_bars_per_pair']} more attested "
            f"bars per pair across {19} pairs",
            "",
            f"  CENSORING  {'PASS' if v['uncensored'] else 'FAIL'}",
            f"    worst feature         {v['limiting_censor_feature']} at "
            f"{v['worst_censored_fraction']} of episodes truncated by the capture "
            f"(allowed {v['max_censored_fraction_allowed']})",
            f"    attested segments     mean {v['mean_attested_segment_bars']} bars, "
            f"max {v['max_attested_segment_bars']} bars",
            f"    to resolve H={v['target_h_to_resolve']}   segments of >= "
            f"{v['required_segment_bars']} unbroken attested bars are required",
            f"    interruption rate     {v['observed_interruptions_per_bar']} per bar observed; "
            f"<= {v['required_interruptions_per_bar']} per bar required",
            "",
            "  MORE CAPTURE TIME FIXES PRECISION AND DOES NOT FIX CENSORING. Segment length",
            "  is set by how often capture is interrupted, not by how long it runs: at the",
            "  observed interruption rate the segments stay the same length however many of",
            "  them accumulate, and no episode can ever be observed outlasting one.",
        ]
    return "\n".join(out)


def _num(x: Optional[float], nd: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "-"
    return f"{x:.{nd}f}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--symbols", nargs="*", default=None)
    ap.add_argument("--start", default=None, help="ISO8601; excludes earlier shards")
    ap.add_argument("--end", default=None)
    ap.add_argument("--bar-seconds", type=int, default=DEFAULT_BAR_SECONDS)
    ap.add_argument("--large-quantile", type=float, default=DEFAULT_LARGE_QUANTILE)
    ap.add_argument("--baseline-seconds", type=int, default=DEFAULT_BASELINE_SECONDS)
    ap.add_argument(
        "--min-baseline-trades", type=int, default=DEFAULT_MIN_BASELINE_TRADES
    )
    ap.add_argument("--min-bar-trades", type=int, default=DEFAULT_MIN_BAR_TRADES)
    args = ap.parse_args(argv)
    print(
        report(
            root=args.root,
            symbols=args.symbols,
            start=args.start,
            end=args.end,
            bar_seconds=args.bar_seconds,
            large_quantile=args.large_quantile,
            baseline_seconds=args.baseline_seconds,
            min_baseline_trades=args.min_baseline_trades,
            min_bar_trades=args.min_bar_trades,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
