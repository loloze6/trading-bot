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
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
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
    forecast_return_corr       = None
    forecast_return_corr_pvalue = None
    if bars_df is not None and "forecast" in bars_df.columns and "close" in bars_df.columns:
        df = bars_df[["forecast", "close"]].copy()
        df["forward_return"] = df["close"].shift(-1) / df["close"] - 1
        df = df.dropna()
        df = df[df["forecast"] != 0]
        if len(df) >= 5:
            x = df["forecast"].values.astype(float)
            y = df["forward_return"].values.astype(float)
            xm, ym = x - x.mean(), y - y.mean()
            denom = np.sqrt((xm**2).sum() * (ym**2).sum())
            corr = float((xm * ym).sum() / denom) if denom > 1e-12 else 0.0
            corr = max(-1.0, min(1.0, corr))
            forecast_return_corr = round(corr, 6)
            n_c = len(x)
            if n_c > 2 and abs(corr) < 1.0:
                t_stat = corr * np.sqrt((n_c - 2) / (1.0 - corr**2))
                try:
                    from scipy.stats import t as t_dist
                    forecast_return_corr_pvalue = round(float(2 * t_dist.sf(abs(t_stat), df=n_c - 2)), 6)
                except ImportError:
                    pass

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
        "avg_trade_duration_bars":     avg_trade_duration_bars,
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
