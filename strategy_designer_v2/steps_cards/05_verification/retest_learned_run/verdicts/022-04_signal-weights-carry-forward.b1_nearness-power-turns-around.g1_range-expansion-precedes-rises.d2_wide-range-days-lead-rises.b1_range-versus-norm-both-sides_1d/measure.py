import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 1000
    RC = "debug_info.components.range_vs_norm.last_history_value"
    RP = "debug_info.components.range_vs_norm.post_pipeline_value"
    OP = "debug_info.components.offset.post_pipeline_value"

    def standardise(raw, window=60, min_periods=20):
        raw = np.asarray(raw, dtype=float)
        out = np.zeros(len(raw))
        for i in range(len(raw)):
            past = raw[max(0, i - window):i]
            past = past[~np.isnan(past)]
            if len(past) < min_periods or np.isnan(raw[i]):
                continue
            m = np.mean(np.abs(past))
            if m == 0:
                continue
            out[i] = np.clip(raw[i] * 10.0 / m, -20, 20)
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            # value of the range component on the forecast scale
            if RP in df.columns:
                rng = pd.to_numeric(df[RP], errors="coerce").to_numpy(dtype=float)
            else:
                rng = np.full(len(df), np.nan)
            if RC in df.columns:
                raw = pd.to_numeric(df[RC], errors="coerce").to_numpy(dtype=float)
                rebuilt = standardise(raw)
                rng = np.where(np.isnan(rng), rebuilt, rng)
            if OP in df.columns:
                off = pd.to_numeric(df[OP], errors="coerce").to_numpy(dtype=float)
                off = np.where(np.isnan(off), -10.0, off)
            else:
                off = np.full(len(df), -10.0)
            # situation: the day's range ratio above (long) or below (short) its usual level
            expected = np.sign(rng + off)
            active = (~np.isnan(fc)) & (fc != 0)
            n_active += int(active.sum())
            ok = active & (~np.isnan(rng)) & (expected != 0) & (np.sign(fc) == expected)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars have a forecast whose sign matches the day's range "
                          "being wider (long) or narrower (short) than its 30-bar norm, as the Fidelity states.",
            "reading": "The situation's side is rebuilt as the sign of the standardised range-ratio value plus the "
                       "-10 offset (post_pipeline values, or rebuilt from raw values when missing).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(df) - H, H):
                r = close[t + H] / close[t] - 1.0
                rows.append((coin, r, fc[t]))
    data = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.dropna(subset=["ret"])
    coin_mean = data.groupby("coin")["ret"].mean()
    data["excess"] = data["ret"] - data["coin"].map(coin_mean)
    data = data.dropna(subset=["excess", "fc"])
    n = int(len(data))

    slope = None
    tval = None
    if n >= 3 and np.var(data["fc"].to_numpy()) > 0:
        res = stats.linregress(data["fc"].to_numpy(dtype=float), data["excess"].to_numpy(dtype=float))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} independent grid cases ({n}): the plan's minimum count is not reached."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the slope is positive with t >= 2 over at least 1000 grid cases."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule met: the slope is negative with t <= -2 over at least 1000 grid cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: the slope's t lies between -2 and 2 with at least 1000 grid cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled OLS slope of next 3-bar excess return on forecast",
            "value": slope,
            "statistic": {"name": "OLS t of the slope", "value": tval} if tval is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 1000 grid cases",
        },
        "supporting_check": None,
        "counts": {"independent grid cases": n, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": "All grid cells (positions 0,3,6,... of each window with a bar 3 ahead) enter the regression, "
                   "including those with a zero forecast, and the coin's mean 3-bar return is taken over its grid "
                   "cells of all windows.",
    }
