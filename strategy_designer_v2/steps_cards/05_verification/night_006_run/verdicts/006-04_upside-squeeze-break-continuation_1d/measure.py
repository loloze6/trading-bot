import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 100

    # ---------- 1. Situation check ----------
    # Fidelity: situation = close above the high of the prior 20 bars (exclude current), side = long (a rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            prior_high = high.shift(1).rolling(20, min_periods=20).max()
            computable = prior_high.notna() & close.notna()
            active = fc.notna() & (fc != 0) & computable
            situation = close > prior_high
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation is rebuilt per window as close > max(high of the 20 prior bars). Each window's "
               "first 20 bars cannot be rebuilt and are left out of the agreement. The cases are pooled "
               "across all coins and windows into one OLS regression. Each coin's baseline is its mean "
               "3-bar return on the non-overlapping grid of all its windows. The plan's 'fewer than 100 "
               "break-bar cases' minimum is treated as a minimum count, which gives 'not observable'.")

    main_name = "OLS slope of excess 3-bar return on forecast, break-bar grid cases"
    threshold = "confirm: t >= 2 and mean excess > 0; reject: t <= -2; else inconclusive; min 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"break-bar cases": None},
            "decided_by": ("Fewer than 90% of active bars (forecast != 0) are bars where the close is above "
                           "the prior 20-bar high with a long forecast, so the config does not do what the "
                           "Fidelity's situation and side say."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        grid_fc = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rets.append(c1 / c0 - 1.0)
                grid_fc.append(fc[t])
        if not grid_rets:
            continue
        grid_rets = np.asarray(grid_rets, float)
        grid_fc = np.asarray(grid_fc, float)
        base = float(np.mean(grid_rets))
        sel = np.isfinite(grid_fc) & (grid_fc > 0)
        xs.extend(grid_fc[sel].tolist())
        ys.extend((grid_rets[sel] - base).tolist())

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    n_cases = int(len(x))
    mean_excess = float(np.mean(y)) if n_cases > 0 else None

    slope, t_slope = None, None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and np.isfinite(res.stderr) and res.stderr > 0:
            t_slope = float(res.slope / res.stderr)

    support_pass = (mean_excess > 0) if mean_excess is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} break-bar cases across all coins and windows, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess 3-bar return on break-bar cases is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: a narrower band is followed by a smaller rise."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more, but the mean excess return is 0 or below, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 3-bar return on break-bar cases > 0",
            "value": mean_excess,
            "passed": support_pass,
        },
        "counts": {"break-bar cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
