import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    REGIME = "mean_reversion"
    MIN_CASES = 100

    # ---------- 1. Situation check: fall over the last 5 bars (computed from prices), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            ret5 = close / close.shift(5) - 1.0  # inside this window only
            active = fc.notna() & (fc != 0) & ret5.notna()
            situation = (ret5 < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars (forecast not 0) are bars where the 5-bar price change "
                           "is negative with a long (positive) forecast, so the config does not trade the plan's "
                           "falling-coin situation on the long side." if n_active > 0 else
                           "No active bars with a computable 5-bar price change, so the config's trading cannot be "
                           "matched to the plan's falling-coin, long situation."),
            "reading": "The 5-bar fall is recomputed as close[t]/close[t-5]-1 < 0 inside each window; the first 5 bars of a window, where it cannot be computed, are left out of the check.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.append(r)
                if reg[t] == REGIME and np.isfinite(fc[t]):
                    coin_cases.append((fc[t], r))
        if len(coin_grid_rets) == 0:
            continue
        coin_mean = float(np.mean(coin_grid_rets))
        for f, r in coin_cases:
            xs.append(float(f))
            ys.append(r - coin_mean)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    sup_val = None
    sup_pass = None
    k = n_cases // 3
    if k >= 1:
        order = np.argsort(x, kind="mergesort")
        bottom = y[order[:k]]
        top = y[order[-k:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(sup_val > 0)

    main = {
        "name": "OLS slope of excess 3-bar return on forecast, pooled",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm if slope t >= 2 with supporting check passing; reject if slope t <= -2",
    }
    supporting = {
        "name": "top-third minus bottom-third forecast mean excess 3-bar return > 0",
        "value": sup_val,
        "passed": sup_pass,
    }
    counts = {"independent grid cases in the falling regime": n_cases}
    reading = ("Cases are the bars at positions 0,3,6,... of each window with regime mean_reversion, a recorded "
               "forecast and a close 3 bars later in the same window (zero forecasts kept); the coin's mean 3-bar "
               "return is taken over the same grid on all its bars in all windows; top and bottom thirds are the "
               "n//3 highest and lowest forecasts by stable sort.")

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent grid cases in the falling regime, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is at least 2 and the top-minus-bottom-third excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check failed, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
