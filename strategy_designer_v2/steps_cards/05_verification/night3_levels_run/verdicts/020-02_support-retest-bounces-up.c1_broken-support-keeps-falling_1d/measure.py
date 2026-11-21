import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.support_above.last_history_value"

    # ---------- 1. situation check ----------
    # Situation: a 90-day swing low cluster lies at/above the close (raw graded value > 0); expected side: short.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            active = np.isfinite(f) & (f != 0)
            situ = np.isfinite(raw) & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 5-bar unusual move in the short direction per bet case"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 independent cases; reject: mean < 0 with t <= -2 over >= 30 cases"
    sup_name = "mean unusual move of larger-|forecast| half minus smaller half"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": 0},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short bars where a swing-low "
                           "cluster lies at or above the close (raw component > 0), as the plan's situation requires"),
            "reading": "situation taken as raw component value > 0 with a negative forecast",
        }

    # ---------- 2. criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # coin's normal 5-bar drift: non-overlapping grid over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # bets on the short side: rise of |forecast| of >= BAND from its lowest size since the last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft >= 0:
                    ref = 0.0
                    continue
                s = -ft
                if s - ref >= BAND:
                    bet[t] = True
                    ref = s
                else:
                    ref = min(ref, s)
            # one case per 5-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                unusual.append(-(r - drift))
                absf.append(abs(f[t]))

    unusual = np.asarray(unusual, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    else:
        t_u = None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = float(np.median(absf))
        large = unusual[absf > med]
        small = unusual[absf <= med]
        if len(large) > 0 and len(small) > 0:
            sup_val = float(np.mean(large) - np.mean(small))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    reading = ("situation taken as raw component > 0 with a negative forecast; a bet is a rise of |forecast| on the "
               "short side of >= 2 points from its lowest size since the last bet (reset to 0 when flat or long); "
               "each 5-bar grid cell's case is its first bet; the larger half is |forecast| strictly above the "
               "median, the smaller half at or below it")

    if n_cases < 30:
        status = "not observable"
        decided = f"only {n_cases} independent cases, fewer than the plan's minimum of 30"
    elif t_u is not None and mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean unusual move in the short direction positive with t >= 2 over >= 30 cases, and the supporting check passes"
        else:
            status = "inconclusive"
            decided = "confirming t >= 2 but the supporting check (larger minus smaller |forecast| half > 0) fails"
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "mean unusual move in the short direction negative with t <= -2 over >= 30 cases"
    else:
        status = "inconclusive"
        decided = "t of the mean unusual move lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
