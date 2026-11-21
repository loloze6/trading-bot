import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    BRK = "debug_info.components.break.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_missing_r60 = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            r60 = close / close.shift(60) - 1.0
            brk = (pd.to_numeric(df[BRK], errors="coerce") if BRK in df.columns
                   else pd.Series(np.nan, index=df.index))
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                if pd.isna(r60.iloc[i]):
                    n_active_missing_r60 += 1
                    continue
                n_active += 1
                b = brk.iloc[i]
                in_sit = (not pd.isna(b)) and (b > 0) and (r60.iloc[i] > 0)
                if in_sit and fc.iloc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation = break component raw value > 0 and 60-bar close return (recomputed within the "
               "window) > 0, side long; active bars whose 60-bar return cannot be computed inside the window "
               "are left out of the agreement, a missing break value counts as outside the situation; a case "
               "is the first long bet (forecast rise >= 2 points from its lowest positive level since the last "
               "bet, from 0 after flat) in each 5-bar grid cell of a window, its excess return is the 5-bar "
               "return from that bar minus the coin's mean 5-bar return on the non-overlapping grid of all its "
               "windows, and the supporting check weights by the forecast on the signal bar.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars without 60-bar return": int(n_active_missing_r60)},
            "decided_by": ("Fewer than 90% of the active bars are long bars where the close breaks above a "
                           "90-day resistance level (break > 0) with a positive 60-day return, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess = []
    weights = []
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(f)
            bet = np.zeros(n, dtype=bool)
            floor = 0.0
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    floor = 0.0
                    continue
                if fi - floor >= BAND:
                    bet[i] = True
                    floor = fi
                else:
                    floor = min(floor, fi)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                excess.append(r - drift)
                weights.append(f[t])

    excess = np.asarray(excess, dtype=float)
    weights = np.asarray(weights, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(excess, ddof=1))
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0 and np.sum(weights) > 0:
        wmean = float(np.sum(excess * weights) / np.sum(weights))
        sup_val = float(wmean - mean_ex)
        sup_pass = bool(wmean > mean_ex)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Fewer than {MIN_CASES} cases ({n_cases}): the plan's minimum count is not reached."
    elif t_val is not None and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = "Mean excess return t >= 2 over at least 30 cases and the forecast-weighted mean exceeds the unweighted mean."
        else:
            status = "inconclusive"
            decided_by = "A confirming t >= 2 over at least 30 cases, but the supporting check fails."
    elif t_val is not None and t_val <= -2:
        status = "rejected"
        decided_by = "Mean excess return t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided_by = "Mean excess return t between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 5-bar excess return of long bets over the coin's mean 5-bar return",
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": "confirm t >= 2, reject t <= -2, over at least 30 cases",
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess minus unweighted mean excess (> 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }
