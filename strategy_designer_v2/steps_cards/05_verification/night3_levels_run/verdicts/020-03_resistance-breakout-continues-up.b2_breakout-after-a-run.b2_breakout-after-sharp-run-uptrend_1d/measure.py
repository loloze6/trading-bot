import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    BRK_COL = "debug_info.components.break_strength.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            if BRK_COL in df.columns:
                brk = pd.to_numeric(df[BRK_COL], errors="coerce").values.astype(float)
            else:
                brk = np.full(len(df), np.nan)
            r60 = np.full(len(df), np.nan)
            if len(df) > 60:
                r60[60:] = close[60:] / close[:-60] - 1.0
            for i in range(len(df)):
                if fc[i] == 0 or not np.isfinite(fc[i]):
                    continue
                if not np.isfinite(r60[i]):
                    n_active_unverifiable += 1
                    continue
                n_active += 1
                b = brk[i]
                if np.isfinite(b) and b > 0 and r60[i] > 0 and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The 60-day return is recomputed from closes inside each window, so active bars in a window's first 60 "
               "bars (no 60-bar lookback) are left out of the agreement share; a case is the first long bet (forecast "
               "rise >= 2 points from its lowest long level since the last bet, from 0 after flat) in each 5-bar grid "
               "cell counted from the window's first row, its forecast size is the forecast on that bar, and the drift "
               "is the coin's mean 5-bar return on the same grid over all its windows; fewer than 30 cases is reported "
               "as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars without 60-bar lookback": int(n_active_unverifiable)},
            "decided_by": ("Fewer than 90% of the active bars are long bars where the break component is above 0 and "
                           "the 60-day return is positive, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    sizes = []
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on non-overlapping grid over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            prev = 0.0
            for i in range(n):
                f = fc[i]
                if f > 0:
                    if prev <= 0:
                        low = 0.0
                    if f - low >= BAND:
                        bet[i] = True
                        low = f
                    else:
                        low = min(low, f)
                else:
                    low = 0.0
                prev = f
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                unusual.append(r - drift)
                sizes.append(fc[i])

    u = np.array(unusual, dtype=float)
    s = np.array(sizes, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope = None
    slope_t = None
    if n_cases > 2 and np.std(s) > 0:
        lr = stats.linregress(s, u)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup_pass = None
    if slope is not None and slope_t is not None:
        sup_pass = bool(slope > 0 and slope_t >= 1.0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled over all coins and windows, below the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Mean unusual 5-day move above 0 with t >= 2 over at least 30 cases, and the slope on "
                       "forecast size is positive with t >= 1.")
        else:
            status = "inconclusive"
            decided = "Mean unusual 5-day move meets the confirm rule but the slope check fails."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual 5-day move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual 5-day move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean unusual 5-day move after long bets",
            "value": mean_u,
            "statistic": ({"name": "t of the mean", "value": t_u} if t_u is not None else None),
            "threshold": "above 0 with t >= 2 to confirm, below 0 with t <= -2 to reject, over at least 30 cases",
        },
        "supporting_check": {
            "name": "slope t of unusual move on forecast size",
            "value": slope_t,
            "passed": sup_pass,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
