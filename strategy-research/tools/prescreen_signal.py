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

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Block size for autocorrelation-adjusted significance (24 bars for 1h).
_BLOCK_SIZE_1H = 24

# Significance threshold: p < 0.10 is informative.
_SIG_THRESHOLD = 0.10

# Forecast is "active" if abs(forecast) > this threshold.
# Exactly zero is the inactive state for regime-gated strategies.
_ACTIVE_THRESHOLD = 1e-6

# Default sigma_bar estimate in bps for 1h crypto.
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
# Spearman rank correlation (no scipy dependency)
# ---------------------------------------------------------------------------

def _spearman(x: list, y: list) -> float | None:
    """
    Compute Spearman rank correlation between x and y.
    Returns None when either series is constant (or fewer than 3 points).
    """
    n = len(x)
    if n < 3 or len(y) != n:
        return None

    def _rank(vals):
        sorted_i = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and vals[sorted_i[j + 1]] == vals[sorted_i[j]]:
                j += 1
            avg_r = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                ranks[sorted_i[k]] = avg_r
            i = j + 1
        return ranks

    rx = _rank(x)
    ry = _rank(y)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    cov = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n)) / n
    std_rx = math.sqrt(sum((r - mean_rx) ** 2 for r in rx) / n)
    std_ry = math.sqrt((sum((r - mean_ry) ** 2 for r in ry) / n))
    if std_rx < 1e-10 or std_ry < 1e-10:
        return None
    return cov / (std_rx * std_ry)


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
        }

    all_f  = [r["forecast"]        for r in records]
    all_r  = [r["next_return_bps"] for r in records]

    active_records = [r for r in records if r["active"]]
    act_f = [r["forecast"]        for r in active_records]
    act_r = [r["next_return_bps"] for r in active_records]

    ic_all   = _spearman(all_f, all_r)
    ic_active = _spearman(act_f, act_r) if act_f else None

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
    returns = [r["next_return_bps"] for r in records]
    if len(returns) < 5:
        return _DEFAULT_SIGMA_BAR_BPS
    return statistics.stdev(returns)


# ---------------------------------------------------------------------------
# Routing logic (A8.1)
# ---------------------------------------------------------------------------

def _determine_route(ic_sig: dict, cost: dict) -> tuple:
    """
    Returns (route, rationale, prescreen_kill_reason).

    Priority:
    1. IC not significant → kill_no_ic
    2. IC significant, NEGATIVE → refine_inverted_ic
    3. IC significant, positive, cost fails → refine_cost_hurdle (or kill_cost_hurdle)
    4. Both pass → proceed_to_backtest
    """
    sig       = ic_sig.get("significant", False)
    pooled_ic = ic_sig.get("pooled_ic") or 0.0
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
            f"Active-bar IC={pooled_ic:.4f}, p={p_value:.4f} >= {_SIG_THRESHOLD}. "
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
                f"Active-bar IC={pooled_ic:.4f} (negative, significant at p={p_value:.4f}). "
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
                    f"Active-bar IC={pooled_ic:.4f} (p={p_value:.4f}, marginal). "
                    f"Est. gross edge {edge_str} vs cost {cost_str} "
                    f"(ratio={ratio_str} < {safety}). Structural cost barrier."
                ),
                "cost_drag_structural",
            )
        else:
            return (
                "refine_cost_hurdle",
                (
                    f"Active-bar IC={pooled_ic:.4f} (significant, p={p_value:.4f}), but "
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
            f"Active-bar IC={pooled_ic:.4f} (p={p_value:.4f}, significant). "
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
    block_size = _BLOCK_SIZE_1H if timeframe in ("1h",) else max(_BLOCK_SIZE_1H // 4, 6)

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
    sigma_bar_bps = statistics.mean(sigma_estimates) if sigma_estimates else _DEFAULT_SIGMA_BAR_BPS

    ic_active      = ic_fields["ic_active_bars"]
    ic_all         = ic_fields["ic_all_bars"]
    active_n       = ic_fields["active_n_bars"]
    sparsity_pct   = ic_fields["forecast_sparsity_pct"]

    # Block-adjusted significance on ACTIVE-BAR n (A8.3)
    ic_values_for_sig = [ic_active] if ic_active is not None else []
    ic_sig_block24 = _block_adjusted_significance(ic_values_for_sig, active_n, block_size)
    ic_sig = ic_sig_block24
    significance_methodology_used = "block_24_fisher_z"
    ic_by_era = None

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

    # Turnover proxy: active bars per trade implies holding period
    total_active = sum(1 for r in all_records if r["active"])
    # Estimate trade count from sign changes in forecast (each flip = one round-trip)
    sign_changes = 0
    prev_sign = 0
    for r in all_records:
        curr_sign = 1 if r["forecast"] > _ACTIVE_THRESHOLD else (
                   -1 if r["forecast"] < -_ACTIVE_THRESHOLD else 0)
        if curr_sign != 0 and prev_sign != 0 and curr_sign != prev_sign:
            sign_changes += 1
        if curr_sign != 0:
            prev_sign = curr_sign

    # Implied trades ≈ sign_changes (each direction flip is one close+open).
    # Fallback: if no sign changes, use a trade every avg_holding_bars.
    implied_trades = max(sign_changes, 1)
    avg_holding_bars = total_active / implied_trades if implied_trades > 0 else None

    turnover_proxy = {
        "active_bars_total":           total_active,
        "implied_trades_estimated":    implied_trades,
        "avg_holding_bars":            round(avg_holding_bars, 2) if avg_holding_bars else None,
        "forecast_sparsity_pct":       sparsity_pct,
    }

    # Cost check uses ic_active_bars (A8.3 and A9.1)
    primary_symbol = symbols[0] if symbols else "default"
    cost = _cost_check(
        ic_active=ic_active,
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
