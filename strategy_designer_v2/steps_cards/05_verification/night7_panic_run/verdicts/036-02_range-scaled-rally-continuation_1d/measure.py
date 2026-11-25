import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RAW = "debug_info.components.scaled_rally.last_history_value"

    def recompute_raw(df):
        close = df["close"].astype(float)
        rel_range = (df["high"].astype(float) - df["low"].astype(float)) / close
        base = rel_range.rolling(30, min_periods=30).mean()
        ret3 = close / close.shift(3) - 1.0
        return ret3 / base.replace(0, np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rec = recompute_raw(df)
            raw = raw.where(raw.notna(), rec)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of next-7-bar excess return on forecast (forecast > 0 grid cells)",
                             "value": None, "statistic": None,
                             "threshold": "slope t >= 2 to confirm, <= -2 to reject"},
            "supporting_check": None,
            "counts": {"positive-forecast grid cells": 0},
            "decided_by": ("Fewer than 90% of active bars are bars with a positive range-scaled 3-day rise "
                           "held long, as the Fidelity's situation and side require."),
            "reading": "Situation taken as raw component value > 0 (a 3-day rise) on the long side; missing raw values recomputed from prices.",
        }

    # ---------- 2. grid cells ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = df["timestamp"].values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "window": w, "timestamp": ts[i],
                             "forecast": fc[i], "ret": c1 / c0 - 1.0})
    cells = pd.DataFrame(rows, columns=["coin", "window", "timestamp", "forecast", "ret"])
    if len(cells):
        coin_mean = cells.groupby("coin")["ret"].mean()
        cells["excess"] = cells["ret"] - cells["coin"].map(coin_mean)
    else:
        cells["excess"] = []
    pos = cells[cells["forecast"].notna() & (cells["forecast"] > 0)].copy()
    n_cases = int(len(pos))
    n_days = int(pos["timestamp"].nunique()) if n_cases else 0

    threshold = ("confirm: slope t >= 2 and mean excess > 0 with t >= 2; reject: slope t <= -2 or mean-excess t <= -2; "
                 "at least 100 cases")

    slope = None
    slope_t = None
    if n_cases >= 3 and pos["forecast"].nunique() > 1:
        lr = stats.linregress(pos["forecast"].values.astype(float), pos["excess"].values.astype(float))
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_ex = None
    mean_t = None
    if n_cases:
        daily = pos.groupby("timestamp")["excess"].sum()
        mean_ex = float(daily.mean())
        if len(daily) > 1:
            sd = daily.std(ddof=1)
            mean_t = float(mean_ex / (sd / np.sqrt(len(daily)))) if sd > 0 else None
    support_pass = None if mean_t is None else bool(mean_ex > 0 and mean_t >= 2)

    counts = {"positive-forecast grid cells": n_cases, "days with cases": n_days}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} positive-forecast grid cells, below the plan's minimum of 100 cases."
    elif slope_t is not None and slope_t >= 2 and support_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and mean excess > 0 with t >= 2, with at least 100 cases (confirm rule)."
    elif (slope_t is not None and slope_t <= -2) or (mean_t is not None and mean_t <= -2):
        status = "rejected"
        decided = "Slope t <= -2 or mean-excess t <= -2, with at least 100 cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "Neither the confirm nor the reject rule is met (slope t between -2 and 2, or positive slope with mean-excess t under 2)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "OLS slope of next-7-bar excess return on forecast (forecast > 0 grid cells)",
                         "value": slope,
                         "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
                         "threshold": threshold},
        "supporting_check": {"name": "mean next-7-bar excess return, same-day cases summed (t >= 2, > 0)",
                             "value": mean_ex, "passed": support_pass,
                             "t": mean_t} if True else None,
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid cells at positions 0,7,14,... of each window with a full 7-bar forward return; the coin's mean 7-bar "
                    "return is over all its grid cells in all windows; the slope is a pooled OLS across coins on per-cell values "
                    "(not day-summed), while the mean-excess t uses same-day sums; the 100-case minimum counts positive-forecast "
                    "cells and, being a minimum count, gives 'not observable'."),
    }
