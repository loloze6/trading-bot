import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)
            up = close / close.shift(1) - 1 > 0
            up_valid = close.shift(1).notna()
            up4 = up.astype(float).rolling(4).sum() == 4
            up4_valid = up_valid.astype(float).rolling(4).sum() == 4
            m2 = vol.rolling(2).mean()
            m4 = vol.rolling(4).mean()
            fade = (m2 / m4) < 1.0
            fade_valid = m4.notna() & (m4 != 0)
            valid = up4_valid & fade_valid
            situ = up4 & fade
            active = (fc != 0) & fc.notna() & valid
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Bars whose 4-bar history lies before the window's first recorded bar are left out of the situation "
               "check; a case is the first short bet (rise of the short forecast's size of at least 2 points from its "
               "lowest size since the last bet, from 0 after a flat or long bar) in each 18-bar grid cell of a window "
               "with an 18-bar return inside the window; the drift is the mean 18-bar return on each coin's "
               "non-overlapping grid over all its windows; the larger half is the cases with absolute forecast above "
               "the median, the smaller half those at or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on which the last 4 "
                           "bars closed up and the mean volume of the last 2 bars is below that of the last 4."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    unusual = []
    absfc = []
    for coin, wins in bars.items():
        # normal drift: mean 18-bar return on non-overlapping grid of all windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            n = len(c)
            ref = 0.0
            bets = []
            for i in range(n):
                m = -f[i] if f[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    bets.append(i)
                    ref = m
                else:
                    ref = min(ref, m)
            seen_cells = set()
            for i in bets:
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                r = c[i + H] / c[i] - 1
                unusual.append(-(r - drift))
                absfc.append(abs(f[i]))

    u = np.array(unusual, dtype=float)
    a = np.array(absfc, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    sup_val = None
    sup_pass = None
    if n_cases > 1:
        med = float(np.median(a))
        big = u[a > med]
        small = u[a <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(np.mean(big) - np.mean(small))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES or t_u is None:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 30."
    elif mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("The mean unusual move in the short direction is above 0 with t >= 2 over at least 30 cases, "
                       "and the larger-forecast half beats the smaller half.")
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2, mean above 0) whose supporting check fails is inconclusive."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction is below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 18-bar unusual move in the short direction",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases",
        },
        "supporting_check": {
            "name": "mean unusual move of larger-|forecast| half minus smaller half, above 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
