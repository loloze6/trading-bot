"""
Residual IC -- does a candidate block hold information the current composite
does not? (E-060 S2, delivery_plan_v26.md slice 7 item 7.1; spec:
engineering/roadmap/E-060/S1_FINDINGS.md §3, guesses 4, 6, 7, 8 and the
operator decision of 2026-09-26.)

Method (guess 8, with the no-lookahead refinement below):
  1. per symbol, inner-join the candidate's and the composite's per-bar
     records on timestamp (a bar missing on either side is dropped and
     counted, never filled);
  2. per symbol, least-squares fit WITH intercept of the candidate forecast on
     the composite forecast, f_cand = a + b * f_comp + e, and keep e;
  3. residual_ic = Spearman rank correlation of e with the next-bar return,
     pooled over every bar of every symbol (all bars, not only bars where the
     block speaks);
  4. n_eff = sum over symbols of the gap-aware one-day block count over those
     bars (performance.signal_statistics.gap_aware_active_block_count with
     every bar marked active, the same way reporting/run_artifact.py counts
     its all-bars IC); p from block_adjusted_pvalue on that n_eff.

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
    """Inner join on timestamp, candidate order. Returns (pairs, only_cand,
    only_comp) where pairs = [(cand_rec, comp_forecast)]."""
    comp_by_ts = {}
    for r in comp_records:
        ts = r["timestamp"]
        if ts in comp_by_ts:
            raise ValueError(f"composite has a duplicate bar at {ts!r}")
        comp_by_ts[ts] = float(r["forecast"])
    seen = set()
    pairs = []
    only_cand = 0
    for r in cand_records:
        ts = r["timestamp"]
        if ts in seen:
            raise ValueError(f"candidate has a duplicate bar at {ts!r}")
        seen.add(ts)
        if ts in comp_by_ts:
            pairs.append((r, comp_by_ts[ts]))
        else:
            only_cand += 1
    only_comp = sum(1 for ts in comp_by_ts if ts not in seen)
    return pairs, only_cand, only_comp


def compute_residual_ic(candidate_by_symbol: dict, composite_by_symbol: dict | None, *,
                        block_size: int, expected_step_by_symbol: dict | None = None,
                        composite_label: str = COMPOSITE_NONE) -> dict:
    """The residual-IC diagnostic, injected as
    protocol_result.hypothesis_verdict.diagnostics.residual_ic for the grid.

    `candidate_by_symbol` / `composite_by_symbol`: {symbol: [record]}, each
    record {timestamp, forecast, next_return_bps} in bar order (the shape of
    run_protocol._assemble_pooled_symbol_records). `composite_by_symbol` None
    means there is no composite (`composite_label` must then be "none").
    `expected_step_by_symbol`: {symbol: bar step} for the gap-aware n_eff;
    a symbol without one is counted as contiguous.
    `block_size`: bars per day (tools/timeframe.bars_per_day)."""
    if block_size < 1:
        raise ValueError(f"block_size must be >= 1, got {block_size!r}")
    if composite_by_symbol is None and composite_label != COMPOSITE_NONE:
        raise ValueError(f"no composite series given but composite_label={composite_label!r}")
    steps = expected_step_by_symbol or {}
    cand_all, comp_all, resid_all, ret_all = [], [], [], []
    n_eff = 0
    dropped_cand = dropped_comp = 0
    for symbol in sorted(candidate_by_symbol):
        c_recs = candidate_by_symbol[symbol] or []
        if composite_by_symbol is None:
            joined = [(r, None) for r in c_recs]
        else:
            joined, oc, op = _join(c_recs, composite_by_symbol.get(symbol) or [])
            dropped_cand += oc
            dropped_comp += op
        if not joined:
            continue
        f_cand = [float(r["forecast"]) for r, _ in joined]
        rets = [float(r["next_return_bps"]) for r, _ in joined]
        if composite_by_symbol is None:
            resid = f_cand
        else:
            f_comp = [c for _, c in joined]
            resid = expanding_ols_residuals(f_cand, f_comp)
            comp_all.extend(f_comp)
        cand_all.extend(f_cand)
        resid_all.extend(resid)
        ret_all.extend(rets)
        step = steps.get(symbol)
        recs = [{"active": True, "timestamp": r.get("timestamp")} for r, _ in joined]
        n_eff += gap_aware_active_block_count(recs, block_size, step)

    out = {
        "value": None,
        "n_eff": n_eff,
        "p_value": None,
        "n_bars": len(cand_all),
        "n_dropped_candidate_only": dropped_cand,
        "n_dropped_composite_only": dropped_comp,
        "fully_explained": False,
        "correlation_to_composite": None,
        "composite": composite_label,
        "method": METHOD,
        "reason": None,
    }
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
    p, _ = block_adjusted_pvalue(ic, len(resid_all), block_size, placeable_blocks=n_eff)
    out["p_value"] = p
    return out


def stale_residual_ic(reason: str) -> dict:
    """The diagnostic when the composite for this registry revision has not
    been computed yet (guess 4): INCONCLUSIVE, never a number."""
    return {"value": None, "n_eff": None, "p_value": None, "n_bars": 0,
            "n_dropped_candidate_only": 0, "n_dropped_composite_only": 0,
            "fully_explained": False, "correlation_to_composite": None,
            "composite": COMPOSITE_STALE, "method": METHOD, "reason": reason}


def symbol_records_from_protocol_result(protocol_result: dict, results_dir) -> tuple:
    """({symbol: records}, {symbol: expected_step}) from a protocol run's
    per-window bars.csv files (<out_dir>/results/<window_run_id>/bars.csv),
    via run_protocol._assemble_pooled_symbol_records -- the one record builder
    the pooled IC and the episode test already share (no third builder).
    Records need a timestamp to be joined: a window without one raises."""
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
        records[symbol] = recs
        steps[symbol] = step
    return records, steps
