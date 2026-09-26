"""
Residual IC -- does a candidate block hold information the current composite
does not? (E-060 S2, delivery_plan_v26.md slice 7 item 7.1; spec:
engineering/roadmap/E-060/S1_FINDINGS.md §3, guesses 4, 6, 7, 8 and the
operator decisions.)

Method (guess 8, with the no-lookahead refinement below):
  1. per symbol, inner-join the candidate's and the composite's per-bar
     records on the (UTC-normalised) timestamp -- a bar missing on either side
     is dropped and counted, never filled; a symbol where fewer than
     MIN_COMPOSITE_COVERAGE of the candidate's bars are matched makes the whole
     result INCONCLUSIVE (`reason: composite_coverage`);
  2. per symbol, least-squares fit WITH intercept of the candidate forecast on
     the composite forecast, f_cand = a + b * f_comp + e, and keep e;
  3. residual_ic = Spearman rank correlation of e with the next-bar return,
     pooled over every bar of every symbol (all bars, not only bars where the
     block speaks);
  4. n_eff = sum over symbols of the gap-aware one-day block count over those
     bars (performance.signal_statistics.gap_aware_active_block_count with
     every bar marked active, the same way reporting/run_artifact.py counts
     its all-bars IC); p from block_adjusted_pvalue on that n_eff, plus the
     one-sided p for "residual IC > 0" that the grid's significance gate reads.

No composite (no forecast block registered on this timeframe yet): step 2 is
skipped and residual_ic is the candidate's own all-bar rank IC
(`composite: none`, guess 4).

WHY THIS CANNOT LEAK (hard rule 3):
  * The fit in step 2 is EXPANDING, not whole-sample: e_t uses a_t, b_t fitted
    on the candidate/composite forecast pairs at bars <= t only. A forecast at
    bar t is itself computed by the engine from data up to t's close, so e_t is
    known at t's close; appending later bars never changes an earlier e_t
    (pinned by tests/test_e060_s2_residual_ic.py). A whole-sample fit would let
    bar t's residual depend on forecasts from after t -- the same objection the
    operator raised against a computed-once scale factor (decision 1).
    Records must be in strictly increasing time order per symbol (checked;
    raises otherwise) so "bars <= t" means earlier in time, not earlier in a
    file or window-label order.
  * The fit uses forecasts only; the next-bar return enters only as the thing
    the residual is ranked against in step 3 -- exactly as in any IC. It is
    never an input of e.
  * The composite forecast series is the output of the same engine on the same
    bars (tools/composite_cache.py), so it carries the engine's own
    past-only guarantee; this module never shifts or aligns it by anything but
    equal timestamps.

Scale-free (operator decision 1 puts standardisation in S3, composition
assembly): multiplying the candidate by a positive constant multiplies e by
the same constant, and multiplying the composite by any non-zero constant only
rescales b -- the ranks of e, and therefore the IC, do not move. S2 does not
depend on any standardisation op.

Degenerate inputs (the signal_statistics HARD RULE -- undefined is never 0.0):
  * a non-finite forecast, composite forecast, return or residual -> value
    None, INCONCLUSIVE (`reason: non_finite`); NaN never reaches spearman;
  * candidate constant over the joined bars -> value None, INCONCLUSIVE
    (`reason: candidate_constant`);
  * candidate varies but the residual has (numerically) no variance -> the
    composite explains it entirely: value None, `fully_explained: true`, which
    the grid maps to FAIL (guess 7). No fake 0.0 is written.
  * composite constant so far at a bar -> b = 0 at that bar (the residual is
    the candidate minus its running mean), well defined.

Pure: no file I/O except symbol_records_from_protocol_result, which reads the
per-window bars.csv files a protocol run already wrote.
"""
from __future__ import annotations

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))           # strategy-research/tools/
_TBOT = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "trading-bot")
for _p in (_HERE, _TBOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from performance.signal_statistics import (  # noqa: E402
    block_adjusted_pvalue,
    gap_aware_active_block_count,
    pearson_correlation,
    spearman_correlation,
)

METHOD = "expanding_ols_residual_rank_ic_v1"
COMPOSITE_NONE = "none"
COMPOSITE_STALE = "STALE"
# Residual variance at or below this fraction of the candidate's variance is
# "no variance left" (guess 7). Floating-point residue of an exact or scaled
# duplicate sits ~1e-30 relative; any genuinely independent component is many
# orders of magnitude above it.
FULLY_EXPLAINED_REL_VAR = 1e-12
# Per symbol, at least this fraction of the CANDIDATE's bars must have a
# composite bar at the same timestamp, else the residual IC is INCONCLUSIVE:
# a composite that covers only part of the candidate would grade the block on
# a thinned-out, possibly unrepresentative sample. Same 0.9 as the portfolio
# common-day coverage floor (run_phase1_research.PORTFOLIO_MIN_COMMON_DAY_COVERAGE).
MIN_COMPOSITE_COVERAGE = 0.9


class RecordOrderError(ValueError):
    """A symbol's records are not in strictly increasing time order."""


def normalize_timestamp(ts):
    """UTC-normalised join key. Numbers (synthetic test clocks) pass through;
    anything else becomes a tz-aware UTC pandas Timestamp (a tz-naive value is
    taken to be UTC, which is what the engine writes)."""
    if isinstance(ts, (int, float)) and not isinstance(ts, bool):
        return ts
    import pandas as pd
    t = pd.Timestamp(ts)
    return t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")


def _normalized(records: list, who: str) -> list:
    out = [{**r, "timestamp": normalize_timestamp(r["timestamp"])} for r in records]
    for i in range(1, len(out)):
        if not out[i]["timestamp"] > out[i - 1]["timestamp"]:
            raise RecordOrderError(
                f"{who}: timestamps not strictly increasing at index {i} "
                f"({out[i - 1]['timestamp']!r} then {out[i]['timestamp']!r}) -- the expanding "
                f"fit needs bars in time order")
    return out


def _finite(x) -> bool:
    try:
        return math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def _variance(values) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    m = sum(values) / n
    return sum((v - m) ** 2 for v in values) / n


def expanding_ols_residuals(cand: list, comp: list) -> list:
    """e_t = cand_t - (a_t + b_t * comp_t), with (a_t, b_t) the least-squares
    fit on pairs 0..t INCLUSIVE (Welford-style running moments, numerically
    stable). b_t = 0 while the composite has no variance yet. Past-only: e_t
    reads nothing after index t."""
    if len(cand) != len(comp):
        raise ValueError(f"candidate and composite differ in length ({len(cand)} vs {len(comp)})")
    out = []
    n = 0
    mean_x = mean_y = 0.0
    sxx = sxy = 0.0
    sum_x2 = 0.0
    for x, y in zip(comp, cand):
        n += 1
        dx = x - mean_x
        mean_x += dx / n
        mean_y += (y - mean_y) / n
        # co-moments about the updated means (Welford)
        sxx += dx * (x - mean_x)
        sxy += dx * (y - mean_y)
        sum_x2 += x * x
        # Scale-free tolerance: centred vs raw sum of squares of the composite.
        if sxx > 1e-12 * sum_x2:
            b = sxy / sxx
        else:
            b = 0.0
        a = mean_y - b * mean_x
        out.append(y - (a + b * x))
    return out


def _join(cand_records: list, comp_records: list) -> tuple:
    """Inner join on (already normalised) timestamp, candidate order. Returns
    (pairs, only_cand, only_comp) where pairs = [(cand_rec, comp_forecast)]."""
    comp_by_ts = {r["timestamp"]: r["forecast"] for r in comp_records}
    seen = set()
    pairs = []
    only_cand = 0
    for r in cand_records:
        ts = r["timestamp"]
        seen.add(ts)
        if ts in comp_by_ts:
            pairs.append((r, comp_by_ts[ts]))
        else:
            only_cand += 1
    only_comp = sum(1 for ts in comp_by_ts if ts not in seen)
    return pairs, only_cand, only_comp


def one_sided_p(ic: float, p_two_sided):
    """P(IC this large | no information) for H1: IC > 0, from the symmetric
    two-sided normal-approximation p of block_adjusted_pvalue."""
    if p_two_sided is None:
        return None
    return round(p_two_sided / 2.0 if ic > 0 else 1.0 - p_two_sided / 2.0, 6)


def compute_residual_ic(candidate_by_symbol: dict, composite_by_symbol: dict | None, *,
                        block_size: int, expected_step_by_symbol: dict | None = None,
                        composite_label: str = COMPOSITE_NONE) -> dict:
    """The residual-IC diagnostic, injected as
    protocol_result.hypothesis_verdict.diagnostics.residual_ic for the grid.

    `candidate_by_symbol` / `composite_by_symbol`: {symbol: [record]}, each
    record {timestamp, forecast, next_return_bps}, strictly increasing in time
    per symbol (raises RecordOrderError otherwise). `composite_by_symbol` None
    means there is no composite (`composite_label` must then be "none").
    `expected_step_by_symbol`: {symbol: bar step} for the gap-aware n_eff;
    a symbol without one is counted as contiguous.
    `block_size`: bars per day (tools/timeframe.bars_per_day)."""
    if block_size < 1:
        raise ValueError(f"block_size must be >= 1, got {block_size!r}")
    if composite_by_symbol is None and composite_label != COMPOSITE_NONE:
        raise ValueError(f"no composite series given but composite_label={composite_label!r}")
    steps = expected_step_by_symbol or {}
    out = {
        "value": None, "n_eff": 0, "p_value": None, "p_value_one_sided": None, "n_bars": 0,
        "n_dropped_candidate_only": 0, "n_dropped_composite_only": 0,
        "coverage_by_symbol": None if composite_by_symbol is None else {},
        "fully_explained": False, "correlation_to_composite": None,
        "composite": composite_label, "method": METHOD, "reason": None,
    }
    cand_all, comp_all, resid_all, ret_all = [], [], [], []
    non_finite, low_coverage = [], []
    for symbol in sorted(candidate_by_symbol):
        c_recs = _normalized(candidate_by_symbol[symbol] or [], f"candidate {symbol}")
        bad = [i for i, r in enumerate(c_recs)
               if not (_finite(r["forecast"]) and _finite(r["next_return_bps"]))]
        if bad:
            non_finite.append(f"candidate {symbol}: {len(bad)} bar(s) (first index {bad[0]})")
            continue
        if composite_by_symbol is None:
            joined = [(r, None) for r in c_recs]
        else:
            p_recs = _normalized(composite_by_symbol.get(symbol) or [], f"composite {symbol}")
            badc = [i for i, r in enumerate(p_recs) if not _finite(r["forecast"])]
            if badc:
                non_finite.append(f"composite {symbol}: {len(badc)} bar(s) (first index {badc[0]})")
                continue
            joined, oc, op = _join(c_recs, p_recs)
            out["n_dropped_candidate_only"] += oc
            out["n_dropped_composite_only"] += op
            cov = (len(joined) / len(c_recs)) if c_recs else 0.0
            out["coverage_by_symbol"][symbol] = round(cov, 6)
            if cov < MIN_COMPOSITE_COVERAGE:
                low_coverage.append(f"{symbol} {cov:.1%}")
                continue
        if not joined:
            continue
        f_cand = [float(r["forecast"]) for r, _ in joined]
        rets = [float(r["next_return_bps"]) for r, _ in joined]
        if composite_by_symbol is None:
            resid = f_cand
        else:
            f_comp = [float(c) for _, c in joined]
            resid = expanding_ols_residuals(f_cand, f_comp)
            if not all(math.isfinite(e) for e in resid):
                non_finite.append(f"residual {symbol}")
                continue
            comp_all.extend(f_comp)
        cand_all.extend(f_cand)
        resid_all.extend(resid)
        ret_all.extend(rets)
        recs = [{"active": True, "timestamp": r["timestamp"]} for r, _ in joined]
        out["n_eff"] += gap_aware_active_block_count(recs, block_size, steps.get(symbol))
    out["n_bars"] = len(cand_all)

    if non_finite:
        out["reason"] = f"non_finite: non-finite values in {non_finite} -- IC not computed"
        return out
    if low_coverage:
        out["reason"] = (f"composite_coverage: the composite matches fewer than "
                         f"{MIN_COMPOSITE_COVERAGE:.0%} of the candidate's bars on {low_coverage}")
        return out
    if composite_by_symbol is not None and cand_all:
        corr = pearson_correlation(cand_all, comp_all)
        out["correlation_to_composite"] = None if corr is None else round(corr, 6)
    var_cand = _variance(cand_all)
    if var_cand <= 0.0 or not math.isfinite(var_cand):
        out["reason"] = "candidate_constant: the candidate forecast has no variance -- IC undefined"
        return out
    if composite_by_symbol is not None and _variance(resid_all) <= FULLY_EXPLAINED_REL_VAR * var_cand:
        out["fully_explained"] = True
        out["reason"] = ("fully_explained: the composite explains the candidate entirely "
                         "(residual has no variance) -- the block adds nothing")
        return out
    ic = spearman_correlation(resid_all, ret_all)
    if ic is None:
        out["reason"] = "rank IC undefined (fewer than 3 bars, or a rank-constant series)"
        return out
    out["value"] = round(ic, 6)
    p, _ = block_adjusted_pvalue(ic, len(resid_all), block_size, placeable_blocks=out["n_eff"])
    out["p_value"] = p
    out["p_value_one_sided"] = one_sided_p(ic, p)
    return out


def stale_residual_ic(reason: str) -> dict:
    """The diagnostic when the composite for this registry revision has not
    been computed yet (guess 4): INCONCLUSIVE, never a number."""
    return {"value": None, "n_eff": None, "p_value": None, "p_value_one_sided": None,
            "n_bars": 0, "n_dropped_candidate_only": 0, "n_dropped_composite_only": 0,
            "coverage_by_symbol": None, "fully_explained": False,
            "correlation_to_composite": None, "composite": COMPOSITE_STALE, "method": METHOD,
            "reason": reason}


def symbol_records_from_protocol_result(protocol_result: dict, results_dir) -> tuple:
    """({symbol: records}, {symbol: expected_step}) from a protocol run's
    per-window bars.csv files (<out_dir>/results/<window_run_id>/bars.csv),
    via run_protocol._assemble_pooled_symbol_records -- the one record builder
    the pooled IC and the episode test already share (no third builder).
    That builder orders windows by their LABEL; the records are re-sorted here
    by (UTC-normalised) timestamp, and compute_residual_ic refuses any
    remaining non-increasing timestamp. Records need a timestamp to be joined:
    a window without one raises."""
    import run_protocol as _rp  # lazy: pulls trading-bot's launcher
    by_symbol: dict = {}
    for entry in protocol_result.get("results") or []:
        if isinstance(entry, dict) and entry.get("symbol") and entry.get("run_id"):
            by_symbol.setdefault(entry["symbol"], []).append(entry)
    records, steps = {}, {}
    for symbol, rows in sorted(by_symbol.items()):
        recs, step, all_ts = _rp._assemble_pooled_symbol_records(rows, results_dir)
        if recs and not all_ts:
            raise ValueError(f"{symbol}: a window's bars.csv has no timestamp column -- the "
                             f"residual IC joins candidate and composite by timestamp")
        recs = [{**r, "timestamp": normalize_timestamp(r["timestamp"])} for r in recs]
        records[symbol] = sorted(recs, key=lambda r: r["timestamp"])
        steps[symbol] = step
    return records, steps


def window_bars_paths(protocol_result: dict, results_dir) -> list:
    """Every window's bars.csv path a protocol result refers to."""
    from pathlib import Path
    return [Path(results_dir) / e["run_id"] / "bars.csv"
            for e in protocol_result.get("results") or []
            if isinstance(e, dict) and e.get("run_id")]
