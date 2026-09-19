"""
Run Artifact
============
Creates a versioned, self-contained run directory for each backtest.
Every run gets: manifest.json, metrics.json, trades.json, bars.csv,
forecast_distribution.csv, and tradesxl.xlsx.
"""

import json
import subprocess
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from performance.signal_statistics import (
    pearson_correlation, t_test_pvalue,
    gap_aware_active_block_count, block_adjusted_pvalue,
    sigma_bar_bps_from_returns, cost_check, determine_route,
)

# CUL-264 (E-039 parity): cost_model.yaml is the single source of truth for
# round_trip_cost_bps/safety_factor -- prescreen_signal.py reads it the same
# way. This is a data-file read across the repo's package boundary, not a
# Python import, so it does not invert the "trading-bot never imports from
# strategy-research" rule the block-adjusted significance port (CUL-262) is
# built around. Falls back to prescreen's own hardcoded defaults if the file
# is missing (e.g. a vendored/deployed trading-bot without the sibling repo).
_COST_MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "strategy-research" / "config" / "cost_model.yaml"


def _load_cost_model() -> dict:
    if not _COST_MODEL_PATH.exists():
        return {"round_trip_cost_bps": {"default": 18.5}, "safety_factor": 2.0}
    import yaml
    with open(_COST_MODEL_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _round_trip_cost_bps(symbol: Optional[str], cost_model: dict) -> float:
    rtc = cost_model.get("round_trip_cost_bps", {})
    if symbol is not None and symbol in rtc:
        return float(rtc[symbol])
    return float(rtc.get("default", 18.5))


# ---------------------------------------------------------------------------
# Directory creation
# ---------------------------------------------------------------------------

def new_run_dir(results_root: str, config: dict, *, runs_dir: str = None) -> Path:
    canonical = json.dumps(config, sort_keys=True, separators=(",", ":"))
    config_hash = sha256(canonical.encode()).hexdigest()[:8]
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + config_hash
    base = Path(runs_dir) if runs_dir else Path(results_root) / "runs"
    run_dir = base / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def data_sha256(df: pd.DataFrame) -> str:
    hash_bytes = pd.util.hash_pandas_object(
        df[["timestamp", "open", "high", "low", "close", "volume"]], index=False
    ).values.tobytes()
    return sha256(hash_bytes).hexdigest()


def _get_git_sha() -> str:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        # --untracked-files=no is deliberate: this repo permanently carries untracked
        # results/runs/ evidence dirs, so an untracked-inclusive check would stamp every
        # run dirty and the marker would stop discriminating. A modified TRACKED file is
        # the signal that the tree differs from the commit this manifest names.
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"]
        ).decode().strip()
        return f"{sha}-dirty" if dirty else sha
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def write_manifest(
    run_dir: Path,
    config: dict,
    data_df: pd.DataFrame,
    symbols: list,
    timeframe: str,
    git_sha: str,
    lookback: int,
    warmup: int,
    feeds: dict | None = None,
) -> None:
    canonical = json.dumps(config, sort_keys=True, separators=(",", ":"))
    manifest = {
        "run_id": run_dir.name,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "config": config,
        "config_sha256": sha256(canonical.encode()).hexdigest(),
        "data": {
            "symbols": symbols,
            "timeframe": timeframe,
            "start": str(data_df["timestamp"].min()),
            "end": str(data_df["timestamp"].max()),
            "bar_count": len(data_df),
            "data_sha256": data_sha256(data_df),
        },
        "git_sha": git_sha,
        "engine": {
            "lookback": lookback,
            "warmup": warmup,
        },
    }
    if feeds is not None:
        manifest["feeds"] = feeds
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))


# ---------------------------------------------------------------------------
# Trades
# ---------------------------------------------------------------------------

def write_trades_json(run_dir: Path, completed_trades: list) -> None:
    records = []
    for t in completed_trades:
        d = t.to_dict()
        d["profitable_absolute"] = bool(d["profitable_absolute"])
        d["profitable_net"] = bool(d["profitable_net"])
        records.append(d)
    (run_dir / "trades.json").write_text(json.dumps(records, indent=2, default=str))


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def write_metrics_json(
    run_dir: Path,
    core: dict,
    per_regime: dict,
    forecast_bins: dict,
    dynamic: dict,
    regime_validity: Optional[dict] = None,
    bar_equity: Optional[dict] = None,
    risk_controls: Optional[dict] = None,
) -> None:
    payload = {
        "core": {
            **core,
            "sharpe_annualization": "sqrt(365) for daily Sharpe (crypto, 365 days/year)",
        },
        "per_regime": per_regime,
        "forecast_bins": forecast_bins,
        "dynamic": dynamic,
    }
    if regime_validity is not None:
        payload["regime_validity"] = regime_validity
    if bar_equity is not None:
        payload["bar_equity"] = bar_equity
    if risk_controls is not None:
        payload["risk_controls"] = risk_controls
    (run_dir / "metrics.json").write_text(json.dumps(payload, indent=2, default=str))


# ---------------------------------------------------------------------------
# Bars CSV
# ---------------------------------------------------------------------------

def write_bars_csv(run_dir: Path, state_df: pd.DataFrame) -> None:
    state_df.round(6).to_csv(run_dir / "bars.csv", index=False)


# ---------------------------------------------------------------------------
# Forecast distribution
# ---------------------------------------------------------------------------

def write_forecast_distribution(run_dir: Path, bars_df: pd.DataFrame) -> None:
    if "forecast" not in bars_df.columns or "regime" not in bars_df.columns:
        return
    bins = [-np.inf, -15, -10, -5, 0, 5, 10, 15, np.inf]
    bin_labels = ["lt_-15", "-15_-10", "-10_-5", "-5_0", "0_5", "5_10", "10_15", "gt_15"]
    records = []
    for regime, group in bars_df.groupby("regime"):
        counts = pd.cut(group["forecast"], bins=bins, labels=bin_labels).value_counts()
        for bl in bin_labels:
            records.append({
                "regime": regime,
                "bin": bl,
                "count_final_forecast": int(counts.get(bl, 0)),
            })
    pd.DataFrame(records).to_csv(run_dir / "forecast_distribution.csv", index=False)


# ---------------------------------------------------------------------------
# Metrics section builders
# ---------------------------------------------------------------------------

def build_core(
    metrics_dict: dict,
    completed_trades: list,
    bars_df: Optional[pd.DataFrame] = None,
    candle_interval_seconds: Optional[int] = None,
    symbol: Optional[str] = None,
) -> dict:
    overall = metrics_dict.get("overall_metrics", {})
    n = len(completed_trades)
    avg_net_pnl = (
        sum(t.net_profit_loss_absolute for t in completed_trades) / n if n > 0 else 0.0
    )
    fees_paid = sum(t.total_commission for t in completed_trades)

    # A1: gross/net PnL + cost drag
    # gross_pnl: pre-commission PnL; net_pnl: post-commission
    gross_pnl = sum(t.profit_loss_absolute for t in completed_trades)
    net_pnl   = sum(t.net_profit_loss_absolute for t in completed_trades)
    cost_drag_pct = (
        round((gross_pnl - net_pnl) / abs(gross_pnl) * 100, 4) if gross_pnl != 0 else None
    )

    # A2: forecast→return correlation
    # Positive corr + negative Sharpe → signal predicts direction but sizing/costs destroy it.
    # Near-zero corr → signal has no predictive power.
    # Negative corr → signal is inverted.
    # 2026-07-09: a long-only (or otherwise single-constant-magnitude-when-active)
    # signal has ZERO VARIANCE among these active-bar forecast values -- the
    # correlation is mathematically undefined here, not "no correlation." Delegates
    # to performance.signal_statistics, which returns None (never a fabricated
    # 0.0) for this case, and never derives a p-value from an undefined
    # correlation. See that module's docstring for the incident this fixes: the
    # prior hardcoded corr=0.0 fallback produced a p=1.0 "confirmed no-edge"
    # result that was actually just an artifact of the signal's shape.
    forecast_return_corr       = None
    forecast_return_corr_pvalue = None
    # CUL-262 (E-039 parity): additive, block-adjusted counterpart to the raw
    # t-test above -- None unless both a real correlation AND a candle
    # interval are available, so every existing caller/consumer of this dict
    # sees byte-identical values for every key that already existed.
    forecast_return_corr_pvalue_block_adjusted = None
    forecast_return_corr_n_eff                 = None
    # CUL-264 (E-039 parity): real per-bar return volatility, needed for the
    # post-backtest cost hurdle below. None until bars_df is available.
    sigma_bar_bps_value  = None
    sigma_is_placeholder = None
    # CUL-266 (#50(A) on the PRIMARY corr path): counts of (forecast,
    # forward_return) pairs suppressed for spanning a real data gap. None --
    # not 0 -- when no gap check was performed, because "not measured" and
    # "measured, found none" are different claims and this codebase does not
    # fabricate the second (cf. _fmt_ic never printing 0.0000 for an undefined
    # IC).
    gap_skipped_pairs = None
    gap_skipped_pct   = None
    if bars_df is not None and "forecast" in bars_df.columns and "close" in bars_df.columns:
        df_all = bars_df[["forecast", "close"]].copy()
        df_all["forward_return"] = df_all["close"].shift(-1) / df_all["close"] - 1

        # #50(A) -- the successor must be the next BAR, not merely the next ROW.
        # shift(-1) above pairs row i with row i+1 unconditionally; across a
        # real hole in the cache that makes a multi-hour move wear a one-bar
        # label. Mirrors prescreen_signal.py::_extract_forecasts's contract:
        # suppress the pair, COUNT it, never drop it silently.
        #
        # APPLIED TO df_all (before the active-only filter), so BOTH sigma and
        # the correlation see the same gap-filtered population. That is not a
        # convenience -- it is what prescreen does: _extract_forecasts filters
        # gap-spanning pairs out of `records` (prescreen_signal.py:570), and
        # _sigma_from_records then consumes that already-filtered list
        # (::run_prescreen, :1479). Filtering only the corr population would
        # leave sigma measuring gap-inflated "one-bar" moves and silently
        # diverge from prescreen on the very number the cost hurdle rests on.
        if candle_interval_seconds and "timestamp" in bars_df.columns:
            expected_step   = pd.Timedelta(seconds=candle_interval_seconds)
            _ts             = pd.to_datetime(bars_df["timestamp"])
            # NaT for the final row => comparison is False => it is excluded
            # here, but it is NOT a gap skip (it simply has no successor), so
            # the count below requires a defined forward_return.
            valid_successor = (_ts.shift(-1) - _ts) == expected_step
            gap_skipped_pairs = int(
                (~valid_successor & df_all["forward_return"].notna()).sum()
            )
            df_all = df_all[valid_successor]

        df_all = df_all.dropna()

        if gap_skipped_pairs is not None:
            # Denominator is PAIRS REACHED (kept + skipped), matching
            # prescreen's own `pairs_reached` (::run_prescreen, :1443/:1446).
            # This is deliberately NOT the cache's contamination rate: bars
            # never reached -- e.g. dropped for a NaN close -- are outside both
            # terms, so this reads lower than a cache-level gap census.
            _pairs_reached  = len(df_all) + gap_skipped_pairs
            gap_skipped_pct = (
                round(gap_skipped_pairs / _pairs_reached * 100.0, 4)
                if _pairs_reached > 0 else None
            )

        # Sigma is measured across ALL bars with a defined forward return, not
        # just active ones -- it's a property of the underlying market, matching
        # prescreen_signal.py::_sigma_from_records's own population (that
        # function runs on the full per-symbol pairs list, not an active-only
        # filter).
        sigma_bar_bps_value, sigma_is_placeholder = sigma_bar_bps_from_returns(
            (df_all["forward_return"] * 10000.0).tolist()
        )
        df = df_all[df_all["forecast"] != 0]
        if len(df) >= 5:
            x = df["forecast"].values.astype(float)
            y = df["forward_return"].values.astype(float)
            corr = pearson_correlation(x, y)
            forecast_return_corr = round(corr, 6) if corr is not None else None
            pvalue = t_test_pvalue(corr, len(x))
            forecast_return_corr_pvalue = round(pvalue, 6) if pvalue is not None else None

            if corr is not None and candle_interval_seconds:
                block_size = max(86400 // candle_interval_seconds, 1)
                placeable_blocks = None
                if "timestamp" in bars_df.columns:
                    expected_step = pd.Timedelta(seconds=candle_interval_seconds)
                    # Exclude the final row: its forward_return is always NaN
                    # (nothing to shift(-1) into), so it was already dropped
                    # from `df`/`x` above. Keeping it here would let the
                    # gap-aware count see one bar `corr`/`len(x)` never did --
                    # off by at most one active bar, but a real population
                    # mismatch rather than an approximation.
                    records = [
                        {"active": bool(f != 0), "timestamp": ts}
                        for f, ts in zip(
                            bars_df["forecast"].iloc[:-1], bars_df["timestamp"].iloc[:-1]
                        )
                    ]
                    placeable_blocks = gap_aware_active_block_count(
                        records, block_size, expected_step
                    )
                pv, neff = block_adjusted_pvalue(
                    corr, len(x), block_size, placeable_blocks=placeable_blocks
                )
                forecast_return_corr_pvalue_block_adjusted = pv
                forecast_return_corr_n_eff                 = neff

    # Avg trade duration in bars (derived from trade timestamps + bar interval)
    avg_trade_duration_bars = None
    if n > 0 and bars_df is not None and "timestamp" in bars_df.columns and len(bars_df) >= 2:
        ts_diffs = pd.Series(bars_df["timestamp"].values).diff().dropna()
        if len(ts_diffs) > 0:
            med = ts_diffs.median()
            bar_minutes = med.total_seconds() / 60 if hasattr(med, "total_seconds") else float(med) / 60
            if bar_minutes > 0:
                avg_trade_duration_bars = round(
                    sum(t.duration_minutes for t in completed_trades) / n / bar_minutes, 2
                )

    # CUL-264 (E-039 parity). INFORMATIONAL ONLY: this route is computed and
    # recorded, but nothing anywhere reads it to skip, gate, or short-circuit
    # any LLM call or orchestrator decision -- see signal_statistics.py's
    # module docstring for `determine_route` and CUL-264's Linear issue.
    # Still computed (not suppressed) when sigma is a placeholder, matching
    # prescreen's own behavior -- `sigma_bar_bps_is_placeholder` is the flag a
    # reader must check before trusting this route, the same discipline
    # prescreen's `sigma_is_placeholder` field already enforces.
    post_backtest_route            = None
    post_backtest_route_rationale  = None
    post_backtest_cost_check       = None
    if (forecast_return_corr is not None
            and forecast_return_corr_pvalue_block_adjusted is not None
            and sigma_bar_bps_value is not None
            and avg_trade_duration_bars is not None):
        cost_model = _load_cost_model()
        rtc_bps    = _round_trip_cost_bps(symbol, cost_model)
        safety     = float(cost_model.get("safety_factor", 2.0))
        post_backtest_cost_check = cost_check(
            forecast_return_corr, sigma_bar_bps_value, avg_trade_duration_bars,
            rtc_bps, safety_factor=safety,
        )
        post_backtest_route, post_backtest_route_rationale = determine_route(
            forecast_return_corr, forecast_return_corr_pvalue_block_adjusted,
            post_backtest_cost_check,
        )

    # CUL-272: real, measured counterparts to the two ESTIMATED inputs above.
    # cost_check/determine_route above are a verbatim port of prescreen's own
    # logic -- appropriate there, since prescreen never executes a real trade
    # and has nothing to measure. Once a real backtest has run (always true by
    # the time build_core is called), re-deriving a theoretical edge/cost from
    # IC*sigma*sqrt(holding) and cost_model.yaml when the REAL numbers already
    # exist a few lines above (fees_paid, gross_pnl/net_pnl) is the same
    # estimate-vs-measurement gap this session already fixed for IC (prescreen
    # vs backtest corr) and turnover (the sign-flip proxy vs bar_equity).
    #
    # Real cost: CompletedTrade.total_commission_percent already sums the
    # entry+exit commission rates for that one trade, in percent -- averaged
    # and converted to bps, this is a real per-trade round-trip cost, unit-
    # compatible with round_trip_cost_bps (both bps-per-trade), no notional
    # estimation needed.
    # Real edge: CompletedTrade.profit_loss_percent is the GROSS (pre-
    # commission) per-trade return -- matching estimated_gross_edge's own
    # "gross, compared against cost separately" semantics. Net PnL is
    # deliberately NOT used here: it is already cost-adjusted, so ratio-ing it
    # against cost again would double-count fees.
    #
    # Deliberately NOT the same as strategy-research's per_trade_expectancy_bps
    # (run_protocol.py::_aggregate_trade_diagnostics, a {mean,se,t_stat,n}
    # block with real statistical care) -- that lives in strategy-research and
    # importing it here would invert this repo's one-way dependency direction
    # (the same reason CUL-262 ported rather than imported). This is a
    # simpler, trade-count-weighted mean, computed natively from
    # completed_trades already in scope here. Real, not estimated -- just less
    # statistically careful than the strategy-research figure.
    #
    # ADDITIVE ONLY: post_backtest_cost_check/post_backtest_route above are
    # UNTOUCHED for byte-identity. These are new, separate "_real" fields.
    real_round_trip_cost_bps           = None
    real_gross_edge_bps_per_trade      = None
    post_backtest_cost_check_real      = None
    post_backtest_route_real           = None
    post_backtest_route_real_rationale = None
    if n > 0:
        real_round_trip_cost_bps = round(
            sum(t.total_commission_percent for t in completed_trades) / n * 100, 4
        )
        real_gross_edge_bps_per_trade = round(
            sum(t.profit_loss_percent for t in completed_trades) / n * 100, 4
        )
    if (forecast_return_corr is not None
            and forecast_return_corr_pvalue_block_adjusted is not None
            and real_round_trip_cost_bps is not None
            and real_round_trip_cost_bps > 0):
        safety = float(_load_cost_model().get("safety_factor", 2.0))
        ratio  = abs(real_gross_edge_bps_per_trade) / real_round_trip_cost_bps
        post_backtest_cost_check_real = {
            # Key names match cost_check()'s own return shape (not renamed to
            # "real_*") so determine_route()'s rationale-string lookups
            # (cost.get("estimated_gross_edge_bps_per_trade") etc.) resolve
            # correctly -- these values are REAL/measured despite the
            # "estimated_" key name inherited from the shared shape.
            "estimated_gross_edge_bps_per_trade": real_gross_edge_bps_per_trade,
            "cost_bps_per_trade":                 real_round_trip_cost_bps,
            "edge_to_cost_ratio":                 round(ratio, 4),
            "safety_factor_required":             safety,
            "pass":                               bool(ratio >= safety),
            "basis":                              "real",
        }
        post_backtest_route_real, post_backtest_route_real_rationale = determine_route(
            forecast_return_corr, forecast_return_corr_pvalue_block_adjusted,
            post_backtest_cost_check_real,
        )

    return {
        "net_return_pct":              overall.get("[OVERALL ONLY] total_return_pct", 0.0),
        "sharpe":                      overall.get("sharpe_ratio", 0.0),
        "max_drawdown_pct":            overall.get("max_drawdown_pct", 0.0),
        "trade_count":                 n,
        "win_rate":                    overall.get("net_win_rate_pct", 0.0),
        "avg_trade_net_pnl":           round(avg_net_pnl, 6),
        "fees_paid":                   round(fees_paid, 6),
        "gross_pnl":                   round(gross_pnl, 6),
        "net_pnl":                     round(net_pnl, 6),
        "cost_drag_pct":               cost_drag_pct,
        "forecast_return_corr":        forecast_return_corr,
        "forecast_return_corr_pvalue": forecast_return_corr_pvalue,
        "forecast_return_corr_pvalue_block_adjusted": forecast_return_corr_pvalue_block_adjusted,
        "forecast_return_corr_n_eff":  forecast_return_corr_n_eff,
        # CUL-266: how much of the reachable sample the #50(A) gap filter
        # removed. A correlation computed over a heavily-decimated sample is a
        # different claim from one over a clean one, so the count travels with
        # the number rather than being inferable only from a log line.
        "gap_skipped_pairs":           gap_skipped_pairs,
        "gap_skipped_pct":             gap_skipped_pct,
        "avg_trade_duration_bars":     avg_trade_duration_bars,
        "sigma_bar_bps":               round(sigma_bar_bps_value, 4) if sigma_bar_bps_value is not None else None,
        "sigma_bar_bps_is_placeholder": sigma_is_placeholder,
        "post_backtest_cost_check":    post_backtest_cost_check,
        "post_backtest_route":         post_backtest_route,
        "post_backtest_route_rationale": post_backtest_route_rationale,
        "real_round_trip_cost_bps":      real_round_trip_cost_bps,
        "real_gross_edge_bps_per_trade": real_gross_edge_bps_per_trade,
        "post_backtest_cost_check_real":      post_backtest_cost_check_real,
        "post_backtest_route_real":           post_backtest_route_real,
        "post_backtest_route_real_rationale": post_backtest_route_real_rationale,
    }


def build_per_regime(bars_df: pd.DataFrame, trades: list) -> dict:
    result: Dict[str, Any] = {}

    if "regime" in bars_df.columns:
        for regime, grp in bars_df.groupby("regime"):
            avg_fc = float(grp["forecast"].mean()) if "forecast" in grp.columns else None
            result.setdefault(str(regime), {})["bar_count"] = len(grp)
            if avg_fc is not None:
                result[str(regime)]["avg_forecast"] = round(avg_fc, 6)

    for t in trades:
        regime = str(t.entry_regime) if t.entry_regime else "UNKNOWN"
        bucket = result.setdefault(regime, {})
        bucket["trade_count"] = bucket.get("trade_count", 0) + 1
        bucket["total_net_pnl"] = round(
            bucket.get("total_net_pnl", 0.0) + t.net_profit_loss_absolute, 6
        )

    return result


def build_forecast_bins(trades: list) -> dict:
    from performance.forecast_analyzer import calc_range_metrics

    records = [
        {
            "forecast": t.entry_forecast,
            "profitable_net": bool(t.profitable_net),
            "net_profit_loss_absolute": t.net_profit_loss_absolute,
        }
        for t in trades
        if t.entry_forecast is not None
    ]
    if not records:
        return {}
    return calc_range_metrics(pd.DataFrame(records))


def build_dynamic(bars_df: pd.DataFrame) -> dict:
    prefix = "debug_info.components."
    component_cols = [
        c for c in bars_df.columns
        if c.startswith(prefix) and pd.api.types.is_numeric_dtype(bars_df[c])
    ]
    if not component_cols or "regime" not in bars_df.columns:
        return {}

    result: Dict[str, Any] = {}
    for col in component_cols:
        col_stats: Dict[str, Any] = {}
        for regime, grp in bars_df.groupby("regime"):
            series = grp[col].dropna()
            col_stats[str(regime)] = {
                "mean": round(float(series.mean()), 6) if len(series) > 0 else None,
                "std":  round(float(series.std()),  6) if len(series) > 1 else None,
            }
        result[col] = col_stats
    return result


def build_regime_validity(bars_df: pd.DataFrame) -> dict:
    """A3: per-regime forward 1-bar return stats for regime label informativeness.

    A regime whose |forward_return_mean| < 0.0001 is near-random — an UNINFORMATIVE label.
    A regime with consistent non-zero mean is a REAL market state worth targeting.
    """
    if "regime" not in bars_df.columns or "close" not in bars_df.columns:
        return {}
    df = bars_df[["regime", "close"]].copy()
    df["forward_return"] = df["close"].shift(-1) / df["close"] - 1
    df = df.dropna()
    result: Dict[str, Any] = {}
    for regime, grp in df.groupby("regime"):
        fwd = grp["forward_return"]
        mean_fwd = round(float(fwd.mean()), 8)
        result[str(regime)] = {
            "forward_return_mean": mean_fwd,
            "forward_return_std":  round(float(fwd.std()), 8) if len(fwd) > 1 else None,
            "n_bars":              int(len(fwd)),
            "informative":         abs(mean_fwd) >= 0.0001,
        }
    return result


def build_bar_equity(bars_df: pd.DataFrame) -> dict:
    """Off-by-default bar-level equity metrics -- an honest alternative to
    core's trade-exit maxDD/Sharpe (see performance/bar_equity.py's module
    docstring for why the trade-exit basis understates risk).

    Excludes bars where regime == 'NOT_READY' (case/whitespace-normalized;
    the engine's own not-ready marker, ~120 bars for the reference window)
    from every statistic below: the strategy could not have acted during
    warmup, and including it dilutes volatility with flat bars that were
    never a real trading decision. RESIDUAL LIMITATION: if the engine's
    not-ready marker were ever renamed to something other than "NOT_READY"
    (any casing or surrounding whitespace), this function has no independent
    is_ready signal to fall back on and would silently include those bars.

    The flag is an explicit opt-in, so degenerate input is an error here,
    never silently swallowed into an empty block: missing required columns,
    zero bars surviving the warmup exclusion, NaN in a required column among
    the surviving bars, or a non-finite computed max_drawdown_pct all raise
    ValueError. n_bars_warmup_excluded == 0 is NOT one of those cases -- a
    warmup_prefetch run can be ready from bar 0, and that's reported through
    the field itself, not treated as degenerate.
    """
    from performance.bar_equity import (
        daily_returns, exposure_pct, max_drawdown_pct, sharpe_ratio_daily,
        sortino_ratio_daily, turnover,
    )

    required = {
        "regime", "timestamp", "postRebalance_total_value",
        "postRebalance_current_allocation", "previous_allocation",
    }
    missing = required - set(bars_df.columns)
    if missing:
        raise ValueError(f"build_bar_equity: missing required columns: {sorted(missing)}")

    n_total = len(bars_df)
    normalized_regime = bars_df["regime"].astype(str).str.strip().str.upper()
    ready = bars_df[normalized_regime != "NOT_READY"].sort_values("timestamp")
    if ready.empty:
        raise ValueError(
            "build_bar_equity: zero bars remain after excluding NOT_READY rows -- "
            "cannot compute bar-level metrics"
        )

    non_regime_required = list(required - {"regime"})
    if ready[non_regime_required].isna().any().any():
        raise ValueError(
            f"build_bar_equity: NaN found in a required column among the "
            f"{len(ready)} post-warmup bars -- refusing to compute silently wrong statistics"
        )

    equity = ready["postRebalance_total_value"]
    timestamps = ready["timestamp"]

    maxdd = max_drawdown_pct(equity)
    if not np.isfinite(maxdd):
        raise ValueError(f"build_bar_equity: computed max_drawdown_pct is non-finite ({maxdd})")

    dr = daily_returns(equity, timestamps)

    return {
        "max_drawdown_pct": round(maxdd, 4),
        "sharpe":           round(sharpe_ratio_daily(equity, timestamps), 4),
        "sortino":          round(sortino_ratio_daily(equity, timestamps), 4),
        "exposure_pct":     round(exposure_pct(ready["postRebalance_current_allocation"]), 4),
        "turnover":         round(
            turnover(ready["postRebalance_current_allocation"], ready["previous_allocation"]), 6
        ),
        "n_bars_total":           n_total,
        "n_bars_warmup_excluded": n_total - len(ready),
        "n_daily_returns":        len(dr),
        "n_downside_days":        int((dr < 0).sum()),
        "basis": (
            "postRebalance_total_value, post-warmup (regime != 'NOT_READY', normalized); "
            "sharpe: daily-resampled closes (resample('D').last()), annualized sqrt(365); "
            "sortino: same daily basis, downside deviation = sqrt(mean(min(r,0)^2)) over ALL "
            "daily returns (target 0), not the sample std of negative days alone"
        ),
    }
