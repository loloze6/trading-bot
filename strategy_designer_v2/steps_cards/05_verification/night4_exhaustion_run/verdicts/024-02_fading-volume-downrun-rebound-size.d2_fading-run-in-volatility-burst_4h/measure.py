import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    MAX_STREAK = 180

    def prep(df):
        df = df.copy()
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp")
        return df.reset_index(drop=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df0 in wins.items():
            df = prep(df0)
            close = df["close"].to_numpy(dtype=float)
            vol = df["volume"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            streak = 0
            for t in range(n):
                if t > 0 and np.isfinite(close[t]) and np.isfinite(close[t - 1]) and close[t] < close[t - 1]:
                    streak = min(streak + 1, MAX_STREAK)
                else:
                    streak = 0
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                situ = False
                if streak >= 2:
                    v = vol[t - streak + 1:t + 1]
                    x = np.arange(len(v), dtype=float)
                    ok = np.isfinite(v)
                    if ok.sum() >= 2:
                        slope = np.polyfit(x[ok], v[ok], 1)[0]
                        situ = slope < 0
                if situ and f > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90% of the active bars close a down-streak of at least 2 bars with falling volume "
                           "slope on the long side, as the plan's situation requires"
                           if n_active > 0 else "the forecast is never active, so the situation cannot be checked"),
            "reading": "the streak is consecutive closes below the previous close ending on the bar (capped at 180), and the volume slope is the least-squares slope of volume over the streak's falling bars.",
        }

    # ---------- 2. criterion ----------
    excess = []
    fvals = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 18-bar returns over all windows
        drift_rets = []
        prepped = {}
        for w, df0 in wins.items():
            df = prep(df0)
            prepped[w] = df
            c = df["close"].to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    drift_rets.append(r)
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))
        for w, df in prepped.items():
            c = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[t] = True
                    low = f
                else:
                    low = min(low, f)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + idx[0]
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                excess.append(r - drift)
                fvals.append(fc[t])

    excess = np.array(excess, dtype=float)
    fvals = np.array(fvals, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_ex = None
    if n_cases >= 2:
        sd = np.std(excess, ddof=1)
        t_ex = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_up = n_lo = 0
    if n_cases >= 2:
        med = np.median(fvals)
        up = excess[fvals > med]
        lo = excess[fvals <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_ex is not None and mean_ex > 0 and t_ex >= 2 and sup_pass:
        status = "confirmed"
        decided = "the mean excess return is positive with t >= 2 and the upper-minus-lower forecast half difference is above 0."
    elif t_ex is not None and mean_ex > 0 and t_ex >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif t_ex is not None and mean_ex < 0 and t_ex <= -2:
        status = "rejected"
        decided = "the mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 18-bar excess return of long bets over the coin's normal drift",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_ex} if t_ex is not None else None,
            "threshold": "confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2; at least 30 cases",
        },
        "supporting_check": {
            "name": "mean excess return of upper forecast half minus lower half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided,
        "reading": ("cases pooled over all coins, the first bet in each non-overlapping 18-bar cell per window, dropping cells whose 18-bar return leaves the window; "
                    "the median split puts forecasts above the median in the upper half and the rest in the lower half; "
                    "the situation's streak is consecutive lower closes ending on the bar with the volume least-squares slope over those bars below 0."),
    }
