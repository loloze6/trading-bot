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
from typing import Any, Dict, List

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Directory creation
# ---------------------------------------------------------------------------

def new_run_dir(results_root: str, config: dict) -> Path:
    canonical = json.dumps(config, sort_keys=True, separators=(",", ":"))
    config_hash = sha256(canonical.encode()).hexdigest()[:8]
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + config_hash
    run_dir = Path(results_root) / "runs" / run_id
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

def build_core(metrics_dict: dict, completed_trades: list) -> dict:
    overall = metrics_dict.get("overall_metrics", {})
    n = len(completed_trades)
    avg_net_pnl = (
        sum(t.net_profit_loss_absolute for t in completed_trades) / n if n > 0 else 0.0
    )
    fees_paid = sum(t.total_commission for t in completed_trades)
    return {
        "net_return_pct":    overall.get("[OVERALL ONLY] total_return_pct", 0.0),
        "sharpe":            overall.get("sharpe_ratio", 0.0),
        "max_drawdown_pct":  overall.get("max_drawdown_pct", 0.0),
        "trade_count":       n,
        "win_rate":          overall.get("net_win_rate_pct", 0.0),
        "avg_trade_net_pnl": round(avg_net_pnl, 6),
        "fees_paid":         round(fees_paid, 6),
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
