import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. Situation check: a 1-day rise (raw scaled return > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the raw value is missing, its sign is the sign of the 1-day return (within the window)
            ret1 = close / close.shift(1) - 1.0
            raw_sign = np.sign(raw.where(raw.notna(), ret1))
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw_sign > 0) & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope t of 5-bar excess return on forecast, positive-forecast grid bars"
    threshold = "confirm if t >= 2 with positive forecast-weighted mean excess; reject if t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars after a 1-day rise (positive scaled return), which the plan's situation requires.",
            "reading": "Bars with a missing raw value take the sign of the 1-day close return within the window.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] > 0:
                    cases.append((f[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for fv, r in cases:
            xs.append(float(fv))
            ys.append(r - drift)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))
    counts = {"positive-forecast grid cases": n_cases}

    slope = None
    t_val = None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_val = float(res.slope / res.stderr) if res.stderr > 0 else None
    wmean = float(np.sum(y * x) / np.sum(x)) if n_cases > 0 and np.sum(x) > 0 else None
    sup_pass = None if wmean is None else bool(wmean > 0)

    main = {
        "name": main_name,
        "value": slope,
        "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
        "threshold": threshold,
    }
    support = {"name": "forecast-weighted mean 5-bar excess return > 0", "value": wmean, "passed": sup_pass}

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} positive-forecast grid cases pooled over coins and windows, below the plan's minimum of 300."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is positive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the forecast-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": "The normal drift is each coin's mean non-overlapping 5-bar grid return over all its windows, the regression pools all coins' positive-forecast grid cases into one OLS, and a grid bar whose 5-bar return would end beyond its window is dropped.",
    }
