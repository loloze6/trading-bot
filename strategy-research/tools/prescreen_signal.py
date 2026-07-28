"""
prescreen_signal.py — Signal prescreen tool (Improvements 08 + 09, with A8.3).

Cheap IC gate before full walk-forward backtest. Feeds OHLCV bars directly into
the strategy's signal layer (no portfolio simulation), computes per-bar forecasts,
then evaluates:
  - ic_all_bars:    Spearman(forecast, next_return) over ALL bars
  - ic_active_bars: Spearman(forecast, next_return) over bars where |forecast| > threshold
  - forecast_sparsity_pct: fraction of bars where forecast is inactive
  - block-adjusted significance on active-bar n
  - Layer 2 cost hurdle from config/cost_model.yaml

A8.1: 08 and 09 land together — proceed_to_backtest requires BOTH ic_significance
      AND cost_check.pass.

A8.3: ic_all_bars for sparse/gated strategies collapses toward zero due to tie mass
      at forecast=0. The IC gate evaluates ic_active_bars with significance computed
      on active-bar n. Dense signals: both ICs converge, behavior unchanged.

A9.1: Keltner config must not proceed to backtest. Empirical result: kill_no_ic
      (active-bar IC=-0.031786, p=0.83 — no significant directional content).
      The historical IC=0.2145 was a small-sample artifact: per-window n_active=5-35
      bars → Pearson IC SE≈0.18-0.58 → noise. Reliable pooled estimate (n=1125) is near
      zero. The two-stage rejection (IC passes, cost fails) is demonstrated in the
      boundary test section via a synthetic fixture.
      See _run_boundary_test() Section 2.

A2.3: ic_by_regime suspended until a trustworthy detector exists.

A6.4: forecast_hash computed from serialized forecast series for trial dedup.

CLI:
  python strategy-research/tools/prescreen_signal.py <config_path> <protocol_path>
  python strategy-research/tools/prescreen_signal.py <config_path> <protocol_path> --run-id run_041
"""

import sys
import os
import csv
import json
import math
import random
import argparse
import statistics
from datetime import datetime, timezone, date as _date, timedelta
from hashlib import sha256
from pathlib import Path

import pandas as pd
import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))   # strategy-research/tools/
_SR   = os.path.dirname(_HERE)                        # strategy-research/
_REPO = os.path.dirname(_SR)                          # repo root
_TBOT = os.path.join(_REPO, "trading-bot")            # trading-bot/

if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

from strategies.main_strategy import AdvancedStrategy
from performance.signal_statistics import spearman_correlation as _spearman

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Block size for autocorrelation-adjusted significance (24 bars for 1h).
_BLOCK_SIZE_1H = 24
# 2026-07-07: a daily bar IS already one calendar day -- no intra-day
# autocorrelation block to divide out (mirrors _BLOCK_SIZE_1H's own logic:
# bars-per-day == block_size, which is 1 bar-per-day at daily resolution).
_BLOCK_SIZE_1D = 1

# Significance threshold: p < 0.10 is informative.
_SIG_THRESHOLD = 0.10

# 2026-07-07 (P4_ts_trend shakedown finding): fallback significance test for signals
# whose active-bar forecast is a SINGLE constant magnitude (e.g. long-only, never
# shorts -- SmaTrendLongOnlyComponent). Spearman IC among active bars is
# mathematically undefined for a constant series (zero variance) regardless of
# sample size or true signal quality -- see _is_degenerate_active_forecast. This is
# a DIFFERENT question from _BLOCK_SIZE_1H/_BLOCK_SIZE_1D above (how many raw bars
# form one independent unit for n_eff): the bootstrap block size below answers "how
# many CONSECUTIVE bars must be resampled together to preserve serial dependence in
# daily returns/signal persistence." Set to ~1 trading month (20 bars), matching the
# "multi-week horizon" serial-correlation mechanism this campaign's brief documents
# for persistent_behavioral_bias edges -- long enough to preserve dependency
# structure, short enough to leave many resampling blocks per symbol (~2720/20=136
# for the full 2018-2025 daily range). This is a PRE-REGISTERED default, fixed
# before observing any run's actual IC value -- do not tune per-hypothesis.
_BOOTSTRAP_BLOCK_SIZE_1D = 20
_BOOTSTRAP_N_RESAMPLES = 1000
# Fixed seed for reproducibility -- a bootstrap significance test must give the same
# p-value on every re-run of the same data, not a different one each invocation.
_BOOTSTRAP_SEED = 20260707

# Forecast is "active" if abs(forecast) > this threshold.
# Exactly zero is the inactive state for regime-gated strategies.
_ACTIVE_THRESHOLD = 1e-6

# LAST-RESORT PLACEHOLDER. NOT A VOLATILITY ESTIMATE. DO NOT CITE THIS NUMBER.
#
# This is the value _sigma_from_records returns when a run has FEWER THAN FIVE
# records -- i.e. when there is not enough data to compute a standard deviation
# at all. It exists so that _cost_check has a finite number to divide by instead
# of crashing on a degenerate run. It was never measured from anything.
#
# Its previous comment read "Default sigma_bar estimate in bps for 1h crypto",
# which is how it came to be read as a campaign measurement of hourly crypto
# volatility and copied into a pre-registration as one. That produced dispatch
# W9's terminal "the whale-footprint family is economically untradeable"
# verdict, which stood until W10 traced it back here and withdrew it. See
# strategy-research/protocols/prereg_whale_footprint_v2.yaml:w10_correction.
#
# For scale: every real 1h measurement this campaign has taken is 48-160 bps
# (15 archived prescreen artifacts: 61.6-82.9; the 19 Kraken breadth pairs over
# 2024-12..2025-12: 48.6-159.2, pooled 106.9 -- tools/measure_bar_sigma.py).
# 15 bps/1h annualizes to ~14% vol, which is not a crypto number. This constant
# is roughly 4-7x too low as a volatility and using it as one BIASES REQUIRED-IC
# DERIVATIONS UPWARD BY THE SAME FACTOR.
#
# If you need a 1h sigma, measure it (tools/measure_bar_sigma.py) or take it
# from the run's own `sigma_bar_bps` output field. Never from here.
_DEFAULT_SIGMA_BAR_BPS = 15.0

# F5c (2026-07-04): component_error_count as a percentage of n_bars_total above which
# the run is routed to no_signal_artifact even when active_n_bars > 0 (pervasive but
# not total failure — still not a trustworthy result). active_n_bars == 0 always
# triggers no_signal_artifact regardless of this threshold.
_NO_SIGNAL_ARTIFACT_ERROR_PCT_THRESHOLD = 5.0

_LOCAL_DATA = os.path.join(_TBOT, "local_data")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _load_funding_rate(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Load 8h funding rate from local_data/{SYMBOL}_funding_8h.csv for [start, end).
    Returns DataFrame with columns: timestamp (pd.Timestamp), funding_rate (float).
    Empty DataFrame if file not found.
    """
    fpath = os.path.join(_LOCAL_DATA, f"{symbol}_funding_8h.csv")
    if not os.path.exists(fpath):
        print(f"    ⚠ Funding rate file not found: {fpath}")
        return pd.DataFrame(columns=["timestamp", "funding_rate"])
    df = pd.read_csv(fpath)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df[(df["timestamp"].dt.strftime("%Y-%m-%d") >= start) &
            (df["timestamp"].dt.strftime("%Y-%m-%d") < end)]
    return df[["timestamp", "funding_rate"]].sort_values("timestamp").reset_index(drop=True)


def _load_fear_greed(start: str, end: str) -> pd.DataFrame:
    """
    Load daily Fear & Greed from local_data/fear_greed_daily.csv for [start, end).
    A8.4 alignment fix: timestamps are shifted +1 day so that the value published
    on day D-1 is first visible on day D's 00:00 bar (eliminates same-day lookahead).
    Returns DataFrame with columns: timestamp (pd.Timestamp), fear_greed (float).
    """
    fpath = os.path.join(_LOCAL_DATA, "fear_greed_daily.csv")
    if not os.path.exists(fpath):
        print(f"    ⚠ Fear & Greed file not found: {fpath}")
        return pd.DataFrame(columns=["timestamp", "fear_greed"])
    df = pd.read_csv(fpath)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # A8.4 fix: +1 day shift so day D value is visible only from day D+1 onward
    df["timestamp"] = df["timestamp"] + pd.Timedelta(days=1)
    df = df[(df["timestamp"].dt.strftime("%Y-%m-%d") >= start) &
            (df["timestamp"].dt.strftime("%Y-%m-%d") < end)]
    return df[["timestamp", "fear_greed"]].sort_values("timestamp").reset_index(drop=True)


def _merge_aux_feeds(
    bars_df: pd.DataFrame,
    aux_feeds: list,
    symbol: str,
    start: str,
    end: str,
) -> pd.DataFrame:
    """
    Merge auxiliary feed columns into bars_df using merge_asof(direction='backward').
    Each feed value assigned to the bar whose open timestamp is >= the feed's timestamp —
    matching the data_manager.py _premerge_aux_feeds() logic exactly.

    Supported aux_feed names: "funding_rate", "fear_greed"
    """
    result = bars_df.copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"])

    if "funding_rate" in aux_feeds:
        fund_df = _load_funding_rate(symbol, start, end)
        if not fund_df.empty:
            result = pd.merge_asof(
                result.sort_values("timestamp"),
                fund_df.sort_values("timestamp"),
                on="timestamp",
                direction="backward",
            )
            n_active = (result["funding_rate"].abs() > 0).sum()
            print(f"    Merged funding_rate: {len(fund_df)} settlement records, "
                  f"{n_active} bars with non-zero rate")
        else:
            result["funding_rate"] = float("nan")
            print(f"    ⚠ No funding rate data for {symbol} — funding_rate set to NaN")

    if "fear_greed" in aux_feeds:
        fng_df = _load_fear_greed(start, end)
        if not fng_df.empty:
            result = pd.merge_asof(
                result.sort_values("timestamp"),
                fng_df.sort_values("timestamp"),
                on="timestamp",
                direction="backward",
            )
            n_extreme = ((result["fear_greed"] < 25) | (result["fear_greed"] > 75)).sum()
            print(f"    Merged fear_greed: {len(fng_df)} daily records (+1d shift applied), "
                  f"{n_extreme} bars in extreme zone (25/75 thresholds)")
        else:
            result["fear_greed"] = float("nan")
            print(f"    ⚠ No Fear & Greed data — fear_greed set to NaN")

    return result


def _load_ohlcv(symbol: str, start: str, end: str, timeframe: str = "1h") -> pd.DataFrame:
    """
    Load OHLCV bars from local_data/{SYMBOL}_{timeframe}.csv filtered to [start, end).

    Returns a DataFrame with columns: timestamp, open, high, low, close, volume.
    Rows are sorted by timestamp ascending.
    """
    fname = f"{symbol}_{timeframe}.csv"
    fpath = os.path.join(_LOCAL_DATA, fname)
    if not os.path.exists(fpath):
        raise FileNotFoundError(f"Local data file not found: {fpath}")

    rows = []
    with open(fpath, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row.get("timestamp", "")
            # Accept either "YYYY-MM-DD HH:MM:SS" or "YYYY-MM-DD"
            ts_date = ts[:10]
            if ts_date < start or ts_date >= end:
                continue
            try:
                rows.append({
                    "timestamp": ts,
                    "open":   float(row["open"]),
                    "high":   float(row["high"]),
                    "low":    float(row["low"]),
                    "close":  float(row["close"]),
                    "volume": float(row.get("volume", 0) or 0),
                })
            except (ValueError, KeyError):
                pass

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Spearman rank correlation -- see the import above: _spearman is
# performance.signal_statistics.spearman_correlation (shared, degenerate-safe
# implementation; deduplicated 2026-07-09 after the same logic was found
# independently hand-rolled a second time in run_artifact.py::build_core with
# a bug in its degenerate-case handling).
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Forecast extraction (signal layer only, no portfolio simulation)
# ---------------------------------------------------------------------------

def _extract_forecasts(config_path: str, bars_df: pd.DataFrame) -> tuple:
    """
    Instantiate AdvancedStrategy from config_path, feed bars sequentially,
    collect (forecast, next_return_bps) pairs for every bar where is_ready().

    next_return_bps: close-to-close return of the bar following the forecast bar,
    in basis points. The last bar in the window has no successor and is excluded.

    Returns (records, component_error_count, component_error_samples):
    - records: list of dicts {forecast, next_return_bps, active}
    - component_error_count: F5b — bars where AdvancedStrategy.update() swallowed a
      component exception. A signal that errors on every bar produces active_n=0
      identically to a signal that genuinely never fires — this count is what lets
      the caller (run_prescreen) tell the two apart (F5c: no_signal_artifact route).
    - component_error_samples: capped list of {bar_index, stage, error_type, error_message}
    """
    strategy = AdvancedStrategy(config_path=config_path)
    records = []
    closes = bars_df["close"].tolist()
    n = len(bars_df)

    for i in range(n):
        bar_row = bars_df.iloc[i : i + 1]
        strategy.update(bar_row)

        if not strategy.is_ready():
            continue

        # Skip the last bar — no successor to compute next_return
        if i >= n - 1:
            continue

        forecast, *_ = strategy.generate_forecast()
        next_ret_bps = (closes[i + 1] - closes[i]) / closes[i] * 10_000.0

        records.append({
            "forecast":       float(forecast),
            "next_return_bps": float(next_ret_bps),
            "active":          abs(forecast) > _ACTIVE_THRESHOLD,
            # A8.5.1a: timestamp carried through so episode_significance.py can
            # map bars to era boundaries. Additive field, does not affect any
            # existing consumer of this record shape.
            "timestamp":       bars_df["timestamp"].iloc[i],
        })

    return records, strategy.component_error_count, strategy.component_error_samples


# ---------------------------------------------------------------------------
# IC and sparsity computation
# ---------------------------------------------------------------------------

def _compute_ic_fields(records: list) -> dict:
    """
    Compute ic_all_bars, ic_active_bars, forecast_sparsity_pct, active_n_bars,
    and forecast_hash from the per-bar records list.
    """
    if not records:
        return {
            "ic_all_bars":          None,
            "ic_active_bars":       None,
            "forecast_sparsity_pct": 100.0,
            "active_n_bars":        0,
            "forecast_hash":        None,
            "active_forecast_distinct_count": 0,
        }

    all_f  = [r["forecast"]        for r in records]
    all_r  = [r["next_return_bps"] for r in records]

    active_records = [r for r in records if r["active"]]
    act_f = [r["forecast"]        for r in active_records]
    act_r = [r["next_return_bps"] for r in active_records]

    ic_all   = _spearman(all_f, all_r)
    ic_active = _spearman(act_f, act_r) if act_f else None
    # 2026-07-07: distinct forecast magnitudes among ACTIVE bars only. A long-only
    # constant-magnitude signal (e.g. always exactly +10.0 when active) has exactly
    # 1 here -- Spearman IC is undefined by construction (zero variance), not by a
    # small-sample or no-edge failure. See _is_degenerate_active_forecast.
    active_distinct_count = len({round(v, 10) for v in act_f})

    n_total  = len(records)
    n_active = len(active_records)
    sparsity = (1.0 - n_active / n_total) * 100.0 if n_total > 0 else 100.0

    # A6.4: forecast hash — deterministic fingerprint of the signal series
    forecast_str = ",".join(f"{v:.6f}" for v in all_f)
    f_hash = sha256(forecast_str.encode()).hexdigest()[:16]

    return {
        "ic_all_bars":          round(ic_all, 6)    if ic_all    is not None else None,
        "ic_active_bars":       round(ic_active, 6) if ic_active is not None else None,
        "forecast_sparsity_pct": round(sparsity, 2),
        "active_n_bars":        n_active,
        "forecast_hash":        f_hash,
        "active_forecast_distinct_count": active_distinct_count,
    }


# ---------------------------------------------------------------------------
# Block-adjusted significance (on active-bar n per A8.3)
# ---------------------------------------------------------------------------

def _block_adjusted_significance(
    ic_values: list,
    n_active_bars: int,
    block_size: int = _BLOCK_SIZE_1H,
) -> dict:
    """
    Block-adjusted z-significance.

    N_eff = n_active_bars / block_size (not total bars — A8.3 requires active-bar n).
    Fisher z-transformation: z = IC * sqrt(N_eff - 3).
    Two-tailed normal approximation.
    """
    if not ic_values:
        return {
            "pooled_ic": None, "z_stat": None, "p_value": 1.0,
            "n_eff": n_active_bars // max(block_size, 1),
            "block_size": block_size, "significant": False,
        }

    pooled_ic = statistics.mean([v for v in ic_values if v is not None])
    n_eff = max(n_active_bars // max(block_size, 1), len(ic_values))

    if abs(pooled_ic) >= 1.0:
        return {
            "pooled_ic": round(pooled_ic, 4), "z_stat": None,
            "p_value": 0.0, "n_eff": n_eff, "block_size": block_size,
            "significant": True,
        }

    # Fisher z: z = IC * sqrt(N_eff - 3)
    dof = max(n_eff - 3, 1)
    z_stat = pooled_ic * math.sqrt(dof)
    abs_z  = abs(z_stat)
    p_value = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs_z / math.sqrt(2.0))))

    return {
        "pooled_ic":   round(pooled_ic, 4),
        "z_stat":      round(z_stat, 4),
        "p_value":     round(p_value, 4),
        "n_eff":       n_eff,
        "block_size":  block_size,
        "significant": bool(p_value < _SIG_THRESHOLD),
    }


# ---------------------------------------------------------------------------
# Degenerate active-bar forecast fallback (2026-07-07)
# ---------------------------------------------------------------------------

def _is_degenerate_active_forecast(ic_active: float | None, active_n: int, active_distinct_count: int) -> bool:
    """
    True when ic_active_bars is undefined NOT because of a bug or an underpowered
    sample, but because the active-bar forecast has fewer than 2 distinct values --
    Spearman IC has zero variance to correlate against returns by construction.
    Structural detection (count of distinct values), never a magnitude threshold.
    """
    return ic_active is None and active_n > 0 and active_distinct_count < 2


def _stationary_block_bootstrap_ic_significance(
    records_by_symbol: dict,
    block_size: int = _BOOTSTRAP_BLOCK_SIZE_1D,
    n_resamples: int = _BOOTSTRAP_N_RESAMPLES,
    seed: int = _BOOTSTRAP_SEED,
) -> dict:
    """
    Pre-registered fallback significance test for the pooled ALL-BARS rank IC, used
    only when ic_active_bars is degenerate (_is_degenerate_active_forecast). All-bars
    IC has real variance to test here because inactive (forecast=0) and active
    (forecast=constant nonzero) bars are two distinct levels.

    Circular block bootstrap: resamples fixed-length blocks WITH replacement,
    independently per symbol (never crossing a symbol boundary, preserving each
    symbol's own time ordering and forecast/return pairing within a block), wrapping
    circularly at the end of each symbol's series. Pools resampled bars across
    symbols exactly as the real statistic does, recomputing Spearman IC on each of
    n_resamples replicates.

    Significance: two-sided bootstrap p-value via the percentile method --
    p = 2 * min(frac(boot_ic <= 0), frac(boot_ic >= 0)), i.e. how much of the
    bootstrap distribution's mass sits on the opposite side of zero from the
    observed IC. Reproducible: fixed seed, not re-randomized per call.
    """
    symbol_arrays = {}
    observed_all_f, observed_all_r = [], []
    for sym, recs in records_by_symbol.items():
        f   = [r["forecast"]        for r in recs]
        ret = [r["next_return_bps"] for r in recs]
        symbol_arrays[sym] = (f, ret)
        observed_all_f.extend(f)
        observed_all_r.extend(ret)

    observed_ic = _spearman(observed_all_f, observed_all_r)
    result_base = {
        "method":       "block_bootstrap_all_bars_v1",
        "block_size":   block_size,
        "n_resamples":  n_resamples,
    }
    if observed_ic is None:
        return {**result_base, "pooled_ic": None, "p_value": 1.0,
                "significant": False, "n_bootstrap_valid": 0}

    rng = random.Random(seed)
    boot_ics = []
    for _ in range(n_resamples):
        rf, rr = [], []
        for f, ret in symbol_arrays.values():
            n = len(f)
            if n == 0:
                continue
            n_blocks_needed = (n + block_size - 1) // block_size
            for _b in range(n_blocks_needed):
                start = rng.randrange(0, n)
                for k in range(block_size):
                    idx = (start + k) % n  # circular wrap -- Politis & Romano (1994)
                    rf.append(f[idx])
                    rr.append(ret[idx])
        ic = _spearman(rf, rr)
        if ic is not None:
            boot_ics.append(ic)

    if not boot_ics:
        return {**result_base, "pooled_ic": round(observed_ic, 6), "p_value": 1.0,
                "significant": False, "n_bootstrap_valid": 0}

    frac_le_0 = sum(1 for v in boot_ics if v <= 0) / len(boot_ics)
    frac_ge_0 = sum(1 for v in boot_ics if v >= 0) / len(boot_ics)
    p_value = min(1.0, 2.0 * min(frac_le_0, frac_ge_0))

    return {
        **result_base,
        "pooled_ic":         round(observed_ic, 6),
        "p_value":           round(p_value, 4),
        "significant":       bool(p_value < _SIG_THRESHOLD),
        "n_bootstrap_valid":  len(boot_ics),
    }


# ---------------------------------------------------------------------------
# Turnover proxy (2026-07-07 redefinition -- see run_prescreen's call site)
# ---------------------------------------------------------------------------

def _compute_turnover_proxy(records_by_symbol: dict) -> dict:
    """
    Trade boundary = an ACTIVITY transition, not a sign transition:
    inactive -> active OPENS a trade; active -> inactive CLOSES it; a direct
    sign flip (long -> short with no flat bar between) closes the old side and
    opens the new one in the same bar (counted as one open here, since exactly
    one new episode begins).

    Superseded the prior sign-flip-only counter (tracked "last NONZERO sign"
    across flat gaps), which silently merged every long-only or short-only
    signal's separate episodes into a SINGLE trade whenever the signal never
    flipped sign -- flat gaps were invisible to it. See the P4_ts_trend
    SmaTrendLongOnlyComponent shakedown finding: that bug inflated
    avg_holding_bars from a ~193-bar estimate to 3058 (the entire pooled
    active-bar count treated as one trade) and the cost ratio to 44.9x.

    Computed per-symbol (never crossing a symbol boundary) then summed:
    pooling the flat records list across symbols would let one symbol's
    trailing sign leak into the next symbol's opening bar as a spurious
    "no transition" read.
    """
    total_active = 0
    total_opens = 0
    for recs in records_by_symbol.values():
        prev_sign = 0  # 0 = flat; tracks the actual PRIOR bar's state, flat included
        for r in recs:
            curr_sign = 1 if r["forecast"] > _ACTIVE_THRESHOLD else (
                       -1 if r["forecast"] < -_ACTIVE_THRESHOLD else 0)
            if curr_sign != 0:
                total_active += 1
                if curr_sign != prev_sign:
                    total_opens += 1
            prev_sign = curr_sign

    implied_trades = max(total_opens, 1)
    avg_holding_bars = total_active / implied_trades if implied_trades > 0 else None
    return {
        "active_bars_total":        total_active,
        "implied_trades_estimated": implied_trades,
        "avg_holding_bars":         avg_holding_bars,
    }


# ---------------------------------------------------------------------------
# Cost check (Layer 2, Improvement 09)
# ---------------------------------------------------------------------------

def _load_cost_model() -> dict:
    p = Path(_SR) / "config" / "cost_model.yaml"
    if not p.exists():
        return {
            "fee_rate_bps":        {"default": 7.5},
            "round_trip_cost_bps": {"default": 18.5},
            "safety_factor":       2.0,
        }
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_campaign_data_policy() -> dict:
    p = Path(_SR) / "config" / "campaign_data_policy.yaml"
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _era_id_for_timestamp(ts, eras: list) -> str:
    """A8.5.1a: map a bar timestamp to its era_id per campaign_data_policy.yaml's
    `eras` list. Returns 'era_unmapped' if the timestamp falls outside every
    declared era (should not happen for in-policy data, but must not crash)."""
    d = pd.Timestamp(ts).strftime("%Y-%m-%d")
    for era in eras:
        lo, hi = era["range"]
        if lo <= d <= hi:
            return era["era_id"]
    return "era_unmapped"


def _round_trip_cost(symbol: str, cost_model: dict) -> float:
    rtc = cost_model.get("round_trip_cost_bps", {})
    return float(rtc.get(symbol) or rtc.get("default", 18.5))


def _cost_check(
    ic_active: float | None,
    sigma_bar_bps: float,
    avg_holding_bars: float | None,
    symbol: str,
    cost_model: dict,
) -> dict:
    """
    Layer 2 cost hurdle.

    estimated_gross_edge_bps_per_trade = abs(ic_active) * sigma_bar_bps * sqrt(avg_holding_bars)
    edge_to_cost_ratio = gross_edge / round_trip_cost_bps
    pass = (ratio >= safety_factor)

    Uses ic_active_bars per A8.3 — the IC that reflects actual signal quality.
    """
    rtc_bps = _round_trip_cost(symbol, cost_model)
    safety  = float(cost_model.get("safety_factor", 2.0))

    if ic_active is None or avg_holding_bars is None or avg_holding_bars <= 0:
        return {
            "symbol":                              symbol,
            "implied_trades_per_window":           None,
            "estimated_gross_edge_bps_per_trade":  None,
            "cost_bps_per_trade":                  rtc_bps,
            "edge_to_cost_ratio":                  None,
            "safety_factor_required":              safety,
            "pass":                                False,
            "ic_used":                             "ic_active_bars",
        }

    gross_edge = abs(ic_active) * sigma_bar_bps * math.sqrt(max(avg_holding_bars, 1.0))
    ratio      = gross_edge / rtc_bps if rtc_bps > 0 else 0.0

    return {
        "symbol":                              symbol,
        "implied_trades_per_window":           None,  # set by caller
        "estimated_gross_edge_bps_per_trade":  round(gross_edge, 4),
        "cost_bps_per_trade":                  rtc_bps,
        "edge_to_cost_ratio":                  round(ratio, 4),
        "safety_factor_required":              safety,
        "pass":                                bool(ratio >= safety),
        "ic_used":                             "ic_active_bars",
    }


# ---------------------------------------------------------------------------
# Sigma estimation from returns
# ---------------------------------------------------------------------------

def _sigma_from_records(records: list) -> float:
    """
    Per-bar return volatility in bps, or the placeholder when it cannot be
    computed.

    The fallback branch is LOUD BY DESIGN. Its silence is what let
    _DEFAULT_SIGMA_BAR_BPS travel out of this function and into a
    pre-registration as though it were a measurement (see the constant's own
    comment). A cost check running on a placeholder sigma is not a cost check,
    and the run artifact should not be the first place anyone finds out.
    """
    returns = [r["next_return_bps"] for r in records]
    if len(returns) < 5:
        print(
            f"    ⚠ SIGMA FALLBACK FIRED: only {len(returns)} record(s) (<5), cannot "
            f"compute stdev. Substituting _DEFAULT_SIGMA_BAR_BPS={_DEFAULT_SIGMA_BAR_BPS} "
            f"— a PLACEHOLDER, not a measurement. Any cost check or required-IC "
            f"derivation resting on this value is invalid; do not cite it."
        )
        return _DEFAULT_SIGMA_BAR_BPS
    return statistics.stdev(returns)


# ---------------------------------------------------------------------------
# Routing logic (A8.1)
# ---------------------------------------------------------------------------

def _fmt_ic(ic: float | None) -> str:
    """Render an IC value for a rationale string. None means undefined (e.g. a
    degenerate constant-magnitude active-bar forecast, see
    _is_degenerate_active_forecast) -- must never print as "0.0000", which would
    claim a measured null result where none exists."""
    return f"{ic:.4f}" if ic is not None else "undefined (degenerate active-bar forecast)"


def _determine_route(ic_sig: dict, cost: dict) -> tuple:
    """
    Returns (route, rationale, prescreen_kill_reason).

    Priority:
    1. IC not significant → kill_no_ic
    2. IC significant, NEGATIVE → refine_inverted_ic
    3. IC significant, positive, cost fails → refine_cost_hurdle (or kill_cost_hurdle)
    4. Both pass → proceed_to_backtest
    """
    sig          = ic_sig.get("significant", False)
    pooled_ic_raw = ic_sig.get("pooled_ic")
    # 2026-07-07: pooled_ic=None means UNDEFINED (e.g. degenerate constant-magnitude
    # active-bar forecast -- see _is_degenerate_active_forecast), not a measured
    # zero. Rendering None as "0.0000" claims a result was measured when it wasn't;
    # _fmt_ic keeps the two cases visually distinct in every rationale string below.
    pooled_ic = pooled_ic_raw if pooled_ic_raw is not None else 0.0
    ic_str    = _fmt_ic(pooled_ic_raw)
    p_value   = ic_sig.get("p_value")
    p_value   = p_value if p_value is not None else 1.0
    ratio     = cost.get("edge_to_cost_ratio")
    cost_pass = cost.get("pass", False)

    if not sig:
        disposition_note = ic_sig.get("disposition_note")
        kill_reason = (
            "insufficient_episodes_a851a" if disposition_note == "insufficient_sample_inconclusive"
            else "no_informational_content_this_venue"
        )
        rationale = (
            f"Active-bar IC={ic_str}, p={p_value:.4f} >= {_SIG_THRESHOLD}. "
            f"Signal has no detectable directional content on this venue/timeframe."
        )
        if disposition_note:
            rationale = (
                f"A8.5.1a: n_episodes={ic_sig.get('n_episodes')} below the "
                f"min_n_episodes floor — descriptive only (pooled_ic={pooled_ic:.4f}), "
                f"no significance claim made. {disposition_note}."
            )
        return ("kill_no_ic", rationale, kill_reason)

    if pooled_ic < 0:
        return (
            "refine_inverted_ic",
            (
                f"Active-bar IC={ic_str} (negative, significant at p={p_value:.4f}). "
                f"Signal direction is inverted — flip polarity before backtest."
            ),
            None,
        )

    # IC positive and significant
    if not cost_pass:
        ratio_str = f"{ratio:.4f}" if ratio is not None else "N/A"
        edge_str  = (
            f"{cost.get('estimated_gross_edge_bps_per_trade', 'N/A'):.1f} bps"
            if cost.get("estimated_gross_edge_bps_per_trade") is not None else "N/A"
        )
        cost_str  = f"{cost.get('cost_bps_per_trade', 'N/A')} bps"
        safety    = cost.get("safety_factor_required", 2.0)
        if p_value > 0.05 or (ratio is not None and ratio < 0.5):
            return (
                "kill_cost_hurdle",
                (
                    f"Active-bar IC={ic_str} (p={p_value:.4f}, marginal). "
                    f"Est. gross edge {edge_str} vs cost {cost_str} "
                    f"(ratio={ratio_str} < {safety}). Structural cost barrier."
                ),
                "cost_drag_structural",
            )
        else:
            return (
                "refine_cost_hurdle",
                (
                    f"Active-bar IC={ic_str} (significant, p={p_value:.4f}), but "
                    f"est. gross edge {edge_str} vs cost {cost_str} "
                    f"(ratio={ratio_str} < required {safety}). "
                    f"Fix: wider threshold or longer holding."
                ),
                None,
            )

    ratio_str = f"{ratio:.4f}" if ratio is not None else "N/A"
    return (
        "proceed_to_backtest",
        (
            f"Active-bar IC={ic_str} (p={p_value:.4f}, significant). "
            f"Edge-to-cost ratio={ratio_str} >= {cost.get('safety_factor_required', 2.0)}. "
            f"Signal passes both IC and cost gates."
        ),
        None,
    )


# ---------------------------------------------------------------------------
# Config fingerprint
# ---------------------------------------------------------------------------

def _config_sha(config_path: str) -> tuple:
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"))
    digest = sha256(canonical.encode()).hexdigest()
    return digest, digest[:8]


# ---------------------------------------------------------------------------
# run_039 ungated_escape write-back (A9.1 side effect)
# ---------------------------------------------------------------------------

def _resolve_ungated_escape(
    run_id: str | None,
    ic_all: float | None,
    n_total_bars: int,
    ic_active: float | None,
    block_size: int = _BLOCK_SIZE_1H,
) -> None:
    """
    A9.1 side effect: resolve ungated_escape_eligible = 'indeterminate' using
    ic_all_bars — the ALL-BARS IC, which is the only admissible metric for A2.1.

    A2.3 rule 5: "The ungated-escape criterion in A2.1 requires IC computed over ALL
    bars; an IC computed on detector-gated bars is not admissible for or against the
    escape." For the Keltner config, ic_active_bars = IC on TRENDING-labeled bars only.
    ic_all_bars = IC on all bars (no regime filter) = the admissible ungated metric.

    Resolution rule (A2.1):
    - If ic_all is near zero (|IC| < 2*SE, i.e. p > 0.05):
      ungated_escape_eligible = True.
      Verdict may conclude signal_bad_everywhere regardless of detector confidence.
    - Otherwise: ungated_escape_eligible = False.
    """
    if not run_id:
        return

    runs_root = Path(_SR) / "runs"
    artifact_path = runs_root / run_id / "artifacts" / "regime_audit_decision.yaml"
    if not artifact_path.exists():
        return

    with open(artifact_path, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}

    current = doc.get("ungated_escape_eligible")
    resolved_by = doc.get("ungated_escape_resolved_by", "")
    # Allow re-resolution if: still indeterminate, OR previously resolved by
    # the old (incorrect) active-bar method.
    if current != "indeterminate" and resolved_by == "prescreen_ic_all_bars":
        return  # Already resolved correctly by this method; no re-write needed.

    if ic_all is None:
        return  # Cannot resolve without all-bars IC

    # Approximate SE and CI using block-adjusted n_eff
    n_eff = max(n_total_bars // block_size, 3)
    se_ic = 1.0 / math.sqrt(max(n_eff - 3, 1))
    z_all = ic_all * math.sqrt(max(n_eff - 3, 1))
    p_all = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z_all) / math.sqrt(2.0))))
    ci_lo = round(ic_all - 1.96 * se_ic, 4)
    ci_hi = round(ic_all + 1.96 * se_ic, 4)

    # "Near zero" = within 2 SE of zero (p > 0.05 two-tailed)
    near_zero = abs(ic_all) < 2.0 * se_ic

    if near_zero:
        new_status = True
        rationale = (
            f"Resolved using prescreen ic_all_bars (all-bars, ungated — admissible per A2.3 rule 5). "
            f"ic_all_bars={ic_all:.4f}, p={p_all:.4f}, 95% CI=[{ci_lo:.4f}, {ci_hi:.4f}], "
            f"n_eff={n_eff} (n_total={n_total_bars} / block_size={block_size}). "
            f"IC is within 2 SE of zero — consistent with no edge over all bars. "
            f"Per A2.1: 'signal_bad_everywhere' may be concluded. "
            f"ungated_escape_eligible set to true. "
            f"Separate diagnostic: ic_active_bars={ic_active if ic_active is not None else 'N/A'} "
            f"(not admissible for this criterion — equals gated/TRENDING-bar IC for this config)."
        )
    else:
        new_status = False
        rationale = (
            f"Resolved using prescreen ic_all_bars (all-bars, ungated — admissible per A2.3 rule 5). "
            f"ic_all_bars={ic_all:.4f}, p={p_all:.4f}, 95% CI=[{ci_lo:.4f}, {ci_hi:.4f}], "
            f"n_eff={n_eff}. |IC| >= 2 SE — cannot apply A2.1 ungated escape. "
            f"ungated_escape_eligible set to false."
        )

    doc["ungated_escape_eligible"] = new_status
    doc["ungated_escape_rationale"] = rationale
    doc["ungated_escape_resolved_by"] = "prescreen_ic_all_bars"
    doc["ungated_escape_resolved_at"] = datetime.now(timezone.utc).isoformat()
    doc["prescreen_ic_all_bars"] = ic_all
    doc["prescreen_ic_active_bars"] = ic_active
    doc["prescreen_ic_all_bars_ci_95"] = [ci_lo, ci_hi]

    with open(artifact_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True)

    print(f"  [prescreen] Resolved ungated_escape_eligible={new_status} in {artifact_path}")


# ---------------------------------------------------------------------------
# Main prescreen function
# ---------------------------------------------------------------------------

def run_prescreen(
    config_path: str,
    protocol_path: str,
    run_id: str | None = None,
    out_dir: Path | None = None,
) -> dict:
    """
    Run signal prescreen over the FULL protocol walk-forward range.

    Signal layer only — no portfolio simulation, no full backtest invocation.
    Computes ic_all_bars and ic_active_bars separately per A8.3.
    """
    with open(config_path, encoding="utf-8") as f:
        config_raw = json.load(f)
    with open(protocol_path, encoding="utf-8") as f:
        protocol = json.load(f)

    aux_feeds      = config_raw.get("aux_feeds", [])
    cost_model     = _load_cost_model()
    config_sha256, config_sha8 = _config_sha(config_path)

    symbols   = protocol["symbols"]
    windows   = protocol["windows"]
    timeframe = protocol.get("timeframe", "1h")
    # 2026-07-07: added explicit "1d" case (block_size=1 -- each daily bar IS
    # already one calendar day, so there is no intra-day autocorrelation block
    # to divide out, matching how "1h" itself is treated: bars-per-day ==
    # block_size). The pre-existing generic fallback for every OTHER non-1h
    # timeframe (4h, 15m, etc.) is untouched.
    if timeframe == "1h":
        block_size = _BLOCK_SIZE_1H
    elif timeframe == "1d":
        block_size = _BLOCK_SIZE_1D
    else:
        block_size = max(_BLOCK_SIZE_1H // 4, 6)

    if out_dir is None:
        out_dir = Path(_SR) / "results" / "prescreens"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect per-symbol results over the full range
    all_records_by_symbol: dict = {}
    n_bars_total = 0
    sigma_estimates: list = []
    total_component_error_count = 0
    component_error_sample: list = []  # capped across all symbols, see below
    _MAX_ERROR_SAMPLE = 5

    for symbol in symbols:
        # Determine full protocol range: earliest start to latest end across all windows
        all_starts = [w["test"]["start"] for w in windows]
        all_ends   = [w["test"]["end"]   for w in windows]
        range_start = min(all_starts)
        range_end   = max(all_ends)

        print(f"  [prescreen] {symbol}  full range {range_start} to {range_end} ...")

        try:
            bars_df = _load_ohlcv(symbol, range_start, range_end, timeframe)
        except FileNotFoundError as e:
            print(f"    ⚠ {e} — skipping {symbol}")
            continue

        if bars_df.empty:
            print(f"    ⚠ No bars for {symbol} in [{range_start}, {range_end}) — skipping")
            continue

        print(f"    Loaded {len(bars_df)} bars — running signal extraction ...")
        if aux_feeds:
            bars_df = _merge_aux_feeds(bars_df, aux_feeds, symbol, range_start, range_end)
        records, error_count, error_samples = _extract_forecasts(config_path, bars_df)
        for r in records:
            r["symbol"] = symbol  # A8.5.1a: needed to keep episodes symbol-bounded when pooled
        print(f"    {len(records)} forecast records; active={sum(1 for r in records if r['active'])}")
        if error_count:
            print(f"    ⚠ {error_count} bar(s) raised a swallowed component exception "
                  f"during update() — see component_error_count/component_error_sample")
            total_component_error_count += error_count
            for s in error_samples:
                if len(component_error_sample) < _MAX_ERROR_SAMPLE:
                    component_error_sample.append({"symbol": symbol, **s})

        all_records_by_symbol[symbol] = records
        n_bars_total += len(records)

        sig_est = _sigma_from_records(records)
        if sig_est > 0:
            sigma_estimates.append(sig_est)

    # Pool records across symbols
    all_records = []
    for recs in all_records_by_symbol.values():
        all_records.extend(recs)

    ic_fields = _compute_ic_fields(all_records)
    # Second, independent path to the placeholder: every symbol failed to produce
    # an estimate. Flagged the same way and for the same reason as the branch in
    # _sigma_from_records -- `sigma_is_placeholder` is carried into the artifact
    # below so a downstream reader sees it without having to have watched stdout.
    sigma_is_placeholder = not sigma_estimates
    if sigma_is_placeholder:
        print(
            f"    ⚠ SIGMA FALLBACK FIRED: no symbol yielded a sigma estimate. "
            f"Substituting _DEFAULT_SIGMA_BAR_BPS={_DEFAULT_SIGMA_BAR_BPS} — a "
            f"PLACEHOLDER, not a measurement. The cost check below is not valid."
        )
    sigma_bar_bps = statistics.mean(sigma_estimates) if sigma_estimates else _DEFAULT_SIGMA_BAR_BPS

    ic_active      = ic_fields["ic_active_bars"]
    ic_all         = ic_fields["ic_all_bars"]
    active_n       = ic_fields["active_n_bars"]
    sparsity_pct   = ic_fields["forecast_sparsity_pct"]
    active_distinct = ic_fields["active_forecast_distinct_count"]

    # Block-adjusted significance on ACTIVE-BAR n (A8.3)
    ic_values_for_sig = [ic_active] if ic_active is not None else []
    ic_sig_block24 = _block_adjusted_significance(ic_values_for_sig, active_n, block_size)
    ic_sig = ic_sig_block24
    significance_methodology_used = "block_24_fisher_z"
    ic_by_era = None
    # Value used for the cost gate's gross-edge estimate (A8.3/A9.1 default: ic_active).
    # Overridden below when ic_active is degenerate (see _is_degenerate_active_forecast).
    ic_for_cost = ic_active

    # 2026-07-07: degenerate active-bar forecast (e.g. a long-only, single-constant-
    # magnitude signal -- SmaTrendLongOnlyComponent). ic_active_bars is undefined by
    # construction here (zero variance among active-bar forecasts), NOT a real
    # no-edge result -- see the P4_ts_trend shakedown finding. Only structural
    # (component ALWAYS produces one magnitude when active) triggers this, checked
    # below; a merely-small active-bar sample from a sign-based signal (e.g. few
    # extreme-funding episodes that happen to share a sign in a narrow window) is a
    # POWER problem, not a structural one -- that case is already handled by the
    # a851a opt-in's own insufficient-episode disposition below, which must run
    # first and is left untouched. This structural fallback only applies to the
    # DEFAULT (non-a851a) path.
    degenerate_active_forecast = _is_degenerate_active_forecast(ic_active, active_n, active_distinct)

    # A8.5.1a (opt-in): candidate_strategy_config.json may request the episode-
    # blocked significance method for hypotheses evaluated over multi-era
    # backward-extension data (see docs/plan/AMENDMENTS_01-06.md "A8.5.1a-spec").
    # Default behavior (flag absent) is UNCHANGED — every prior run's recorded
    # result stays reproducible under the original block_24_fisher_z method.
    if config_raw.get("significance_methodology") == "episode_blocked_a851a":
        import episode_significance as _es
        policy = _load_campaign_data_policy()
        eras = policy.get("eras", [])
        es_cfg = policy.get("episode_significance", {})

        def _era_of(i, _records=all_records, _eras=eras):
            return (_records[i]["symbol"], _era_id_for_timestamp(_records[i]["timestamp"], _eras))

        a851a_result = _es.compute_a851a_significance(
            all_records,
            era_of=_era_of if eras else None,
            gap_bars=es_cfg.get("gap_bars", _es._DEFAULT_GAP_BARS),
            density_fallback_pct=es_cfg.get("density_fallback_pct", _es._DEFAULT_DENSITY_FALLBACK_PCT),
            min_n_episodes=es_cfg.get("min_n_episodes", _es._MIN_N_EPISODES),
            block_size=block_size,
            n_resamples=es_cfg.get("n_resamples", _es._DEFAULT_N_RESAMPLES),
        )
        ic_sig = a851a_result
        significance_methodology_used = a851a_result["method"]
        if eras:
            ic_by_era = _es.per_era_report(all_records, _era_of)
        print(f"    A8.5.1a significance: method={a851a_result['method']} "
              f"n_episodes={a851a_result.get('n_episodes')} "
              f"pooled_ic={a851a_result.get('pooled_ic')} "
              f"p_value={a851a_result.get('p_value')} "
              f"significant={a851a_result.get('significant')}")
    elif degenerate_active_forecast:
        bootstrap_result = _stationary_block_bootstrap_ic_significance(all_records_by_symbol)
        ic_sig = bootstrap_result
        significance_methodology_used = bootstrap_result["method"]
        ic_for_cost = bootstrap_result["pooled_ic"]
        print(f"    Degenerate active-bar forecast (active_forecast_distinct_count="
              f"{active_distinct}) -- ic_active_bars is undefined by construction, "
              f"not a no-edge result. Falling back to {bootstrap_result['method']}: "
              f"pooled_ic={bootstrap_result['pooled_ic']} p_value={bootstrap_result['p_value']} "
              f"significant={bootstrap_result['significant']}")

    # Turnover proxy: active bars per trade implies holding period. See
    # _compute_turnover_proxy's docstring for the 2026-07-07 activity-transition
    # redefinition (supersedes the prior sign-flip-only counter, which silently
    # merged long-only/short-only episodes across flat gaps into one trade).
    _turnover = _compute_turnover_proxy(all_records_by_symbol)
    total_active     = _turnover["active_bars_total"]
    implied_trades   = _turnover["implied_trades_estimated"]
    avg_holding_bars = _turnover["avg_holding_bars"]

    turnover_proxy = {
        "active_bars_total":           total_active,
        "implied_trades_estimated":    implied_trades,
        "avg_holding_bars":            round(avg_holding_bars, 2) if avg_holding_bars else None,
        "forecast_sparsity_pct":       sparsity_pct,
    }

    # Cost check uses ic_active_bars (A8.3 and A9.1), or ic_for_cost's block-bootstrap
    # fallback when ic_active is degenerate (see above) -- otherwise the cost gate
    # would unconditionally fail (ic=None) regardless of the signal's true cost profile.
    primary_symbol = symbols[0] if symbols else "default"
    cost = _cost_check(
        ic_active=ic_for_cost,
        sigma_bar_bps=sigma_bar_bps,
        avg_holding_bars=avg_holding_bars,
        symbol=primary_symbol,
        cost_model=cost_model,
    )
    cost["implied_trades_per_window"] = implied_trades

    # Route decision
    route, rationale, kill_reason = _determine_route(ic_sig, cost)

    # F5c (2026-07-04): zero-signal-artifact check takes priority over every other
    # route. active_n_bars==0 or a pervasive component-error rate means the signal
    # was never actually evaluated — a bug/config problem, not a scientific "no edge"
    # result. This MUST NOT be scored as kill_no_ic (that says "tested, found nothing");
    # the hypothesis here is untested. See run_044 (2026-07-04): FundingRateMeanReversion
    # Component's threshold=0 divide-by-zero produced active_n_bars=0, which read as a
    # real kill_no_ic verdict and nearly closed an otherwise-untested hypothesis family.
    error_pct = (total_component_error_count / n_bars_total * 100.0) if n_bars_total > 0 else 0.0
    if active_n == 0 or error_pct > _NO_SIGNAL_ARTIFACT_ERROR_PCT_THRESHOLD:
        route = "no_signal_artifact"
        if total_component_error_count > 0:
            kill_reason = "component_error"
            rationale = (
                f"F5c: {total_component_error_count} bar(s) ({error_pct:.1f}% of "
                f"{n_bars_total} processed) raised a swallowed component exception during "
                f"update() (see component_error_sample). active_n_bars={active_n} cannot be "
                f"trusted as a genuine result — this is an engineering failure, not evidence "
                f"about the hypothesis. Fix the component/config, then re-run fresh."
            )
        else:
            kill_reason = "zero_activation"
            rationale = (
                f"F5c: active_n_bars=0 with zero swallowed component errors — the signal "
                f"genuinely never activated on this data (e.g. its firing condition was "
                f"never satisfied in this window). Still routed as no_signal_artifact, not "
                f"kill_no_ic: a component that never fires has not been tested for "
                f"directional content, only for activation. Investigate the activation "
                f"condition/data before concluding anything about the mechanism."
            )
        print(f"  ⚠ [prescreen] no_signal_artifact: {rationale}")

    # ic_by_regime: suspended per A2.3
    ic_by_regime = {
        "suspended": True,
        "reason": (
            "A2.3: ic_by_regime suspended until a trustworthy detector exists. "
            "Only ungated IC is used for prescreen decisions."
        ),
    }

    # Windows actually processed (full range = all windows)
    windows_used = [w["label"] for w in windows]

    result = {
        "run_id":                   run_id or "unknown",
        "config_sha8":              config_sha8,
        "computed_at":              datetime.now(timezone.utc).isoformat(),
        "protocol_version":         protocol.get("_version", protocol_path),
        "symbols":                  symbols,
        "prescreen_windows_used":   windows_used,
        "n_bars_total":             n_bars_total,
        # A8.3 fields
        "ic_all_bars":              ic_all,
        "ic_active_bars":           ic_active,
        "forecast_sparsity_pct":    sparsity_pct,
        "active_n_bars":            active_n,
        "forecast_hash":            ic_fields["forecast_hash"],
        # 2026-07-07: structural flag, not a threshold -- see _is_degenerate_active_forecast.
        "active_forecast_distinct_count": active_distinct,
        "degenerate_active_forecast":     degenerate_active_forecast,
        # Legacy pooled field (= ic_active_bars for backward compat)
        "ic_spearman_pooled":       ic_active,
        "ic_by_regime":             ic_by_regime,
        "ic_significance":          ic_sig,
        # A8.5.1a: always compute+report the original block_24 method for
        # continuity/comparison, and which method actually decided `route` above.
        "ic_significance_block24":  ic_sig_block24,
        "significance_methodology_used": significance_methodology_used,
        "ic_by_era":                ic_by_era,
        "turnover_proxy":           turnover_proxy,
        "sigma_bar_bps":            round(sigma_bar_bps, 4),
        # True when sigma_bar_bps above is _DEFAULT_SIGMA_BAR_BPS rather than a
        # measurement. Any cost_check or required-IC figure in this artifact is
        # invalid when this is true -- see the constant's comment.
        "sigma_is_placeholder":     sigma_is_placeholder,
        "cost_check":               cost,
        "route":                    route,
        "route_rationale":          rationale,
        "prescreen_kill_reason":    kill_reason,
        # F5b/F5c
        "component_error_count":    total_component_error_count,
        "component_error_sample":   component_error_sample,
    }

    # A9.1 side effect: resolve ungated_escape_eligible using ic_all_bars (A2.1 admissible metric)
    resolve_id = run_id or "run_039"
    _resolve_ungated_escape(resolve_id, ic_all, n_bars_total, ic_active, block_size)

    # Write prescreen_result.yaml
    out_path = out_dir / "prescreen_result.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(result, f, sort_keys=False, allow_unicode=True)

    print(
        f"  [prescreen] Route={route} | "
        f"ic_active={ic_active} ic_all={ic_all} "
        f"sparsity={sparsity_pct:.1f}% active_n={active_n} "
        f"p={ic_sig.get('p_value')} | "
        f"cost_pass={cost['pass']} ratio={cost.get('edge_to_cost_ratio')}"
    )
    print(f"  [prescreen] Written to {out_path}")

    return result


# ---------------------------------------------------------------------------
# Synthetic boundary-case unit test (A8.3 acceptance criterion 3)
# ---------------------------------------------------------------------------

def _run_boundary_test() -> None:
    """
    Verify cost_check threshold logic at ratio ≈ 2.0, and demonstrate the A9.1
    two-stage rejection (IC gate passes, cost gate fails).

    Section 1 — Boundary cases near ratio=2.0:
      just_below: IC=0.25, hold=80 bars → ratio=1.973 → FAIL
      just_above: IC=0.25, hold=84 bars → ratio=2.022 → PASS

    Section 2 — Synthetic A9.1 two-stage rejection:
      Simulates a strategy with IC=0.20 (significant, passes IC gate) but very short
      avg_holding_bars=4 (high turnover → low gross edge → fails cost gate).
      This exercises the code path that A8.3 requires: IC gate passes, cost gate fails.

    Note on Keltner fixture (keltner_163): the actual pooled prescreen ic_active_bars
    for the Keltner config is -0.031786 (p=0.83, n_active=1125), which kills at the IC
    gate (kill_no_ic), not the cost gate. The historical IC=0.2145 was a small-sample
    artifact: per-window active_n was only 5-35 bars per window, giving Pearson IC SE
    of 0.18-0.58. The reliable pooled estimate shows no significant directional content.
    The synthetic fixture below demonstrates the intended two-stage path.
    """
    cost_model = _load_cost_model()
    sigma = 15.0
    all_pass = True

    # Section 1: boundary cases near ratio=2.0
    # IC=0.25, sigma=15, rtc=17: ratio=2.0 when hold=82.2 bars
    print("\n[boundary test] Section 1: cost_check threshold at ratio ~2.0")
    boundary_cases = [
        ("just_below_2.0", 0.25, 80.0, False),
        ("just_above_2.0", 0.25, 84.0, True),
    ]
    for label, ic, hold, expected_pass in boundary_cases:
        c = _cost_check(ic, sigma, hold, "BTCUSDT", cost_model)
        ratio = c["edge_to_cost_ratio"]
        ok = c["pass"] == expected_pass
        status = "OK" if ok else "FAIL"
        print(
            f"  [{status}] {label}: IC={ic} hold={hold} => "
            f"gross={c['estimated_gross_edge_bps_per_trade']:.2f} bps "
            f"ratio={ratio:.4f} "
            f"pass={c['pass']} (expected {expected_pass})"
        )
        if not ok:
            all_pass = False

    # Section 2: synthetic A9.1 two-stage rejection
    # IC=0.20, sigma=15, hold=4 bars (high-turnover strategy):
    #   gross_edge = 0.20 * 15 * sqrt(4) = 0.20 * 15 * 2 = 6.0 bps
    #   ratio = 6.0 / 17 = 0.353 < 2.0 → cost FAILS
    # Route: IC significant (mocked) → cost fails → refine_cost_hurdle
    print("\n[boundary test] Section 2: A9.1 two-stage rejection (IC passes, cost fails)")
    ic_a91 = 0.20
    hold_a91 = 4.0
    c_a91 = _cost_check(ic_a91, sigma, hold_a91, "BTCUSDT", cost_model)

    # Mock a significant IC result (p=0.04, significant=True)
    ic_sig_mock = {
        "pooled_ic":   ic_a91,
        "z_stat":      2.05,
        "p_value":     0.04,
        "n_eff":       420,  # 10080 active bars / 24 block
        "block_size":  24,
        "significant": True,
    }
    route, rationale, kill_reason = _determine_route(ic_sig_mock, c_a91)

    expected_route_prefix = "refine_cost_hurdle"  # or kill_cost_hurdle depending on p_value
    # p=0.04 < 0.05 and ratio=0.35 < 0.5 → kill_cost_hurdle
    expected_route = "kill_cost_hurdle"
    ok_route = route == expected_route
    ok_cost_fail = not c_a91["pass"]
    ok_ic_pass   = ic_sig_mock["significant"] and ic_a91 > 0

    print(f"  IC gate:   pooled_ic={ic_a91:.2f} p={ic_sig_mock['p_value']:.2f} significant={ic_sig_mock['significant']} => {'PASS' if ok_ic_pass else 'FAIL'}")
    print(f"  Cost gate: gross={c_a91['estimated_gross_edge_bps_per_trade']:.1f} bps ratio={c_a91['edge_to_cost_ratio']:.4f} pass={c_a91['pass']} => {'FAIL (expected)' if ok_cost_fail else 'UNEXPECTED PASS'}")
    print(f"  Route:     {route} => {'OK' if ok_route else f'FAIL (expected {expected_route})'}")
    print(f"  Rationale: {rationale[:120]}...")

    if not (ok_ic_pass and ok_cost_fail and ok_route):
        all_pass = False

    if all_pass:
        print("\n[boundary test] PASSED — threshold and two-stage rejection behave correctly.\n")
    else:
        print("\n[boundary test] FAILED — check logic.\n")
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    # Handle --boundary-test early before positional args are required.
    if "--boundary-test" in sys.argv:
        _run_boundary_test()
        return

    parser = argparse.ArgumentParser(
        description="Signal prescreen — cheap IC+cost gate before full walk-forward."
    )
    parser.add_argument("config_path",    help="Path to candidate_strategy_config.json")
    parser.add_argument("protocol_path",  help="Path to protocol JSON spec")
    parser.add_argument("--run-id",       default=None, help="Run ID for artifact labelling")
    parser.add_argument("--out-dir",      default=None, help="Output directory override")
    args = parser.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else None
    result  = run_prescreen(
        args.config_path, args.protocol_path,
        run_id=args.run_id, out_dir=out_dir,
    )
    print(f"\nPrescreen complete. Route: {result['route']}")
    print(f"Rationale: {result['route_rationale']}")


if __name__ == "__main__":
    main()
