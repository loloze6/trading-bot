import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 4
    BAND = 2.0
    RAW = "debug_info.components.vol_fall.last_history_value"

    # ---------- 1. Situation check ----------
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
            n_active += int(active.sum())
            # situation: a volume-weighted, vol-scaled fall (raw < 0); expected side: long
            agree = active & np.isfinite(raw) & (raw < 0) & (f > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 4-bar move after heavy-volume plunge bets (long)"
    threshold = "confirm t >= 2 over >= 30 cases with slope > 0; reject t <= -2 over >= 30 cases"
    reading = ("Situation = bars whose raw volume-weighted scaled return is negative (graded fall), side long; "
               "a case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, "
               "reset to 0 after a flat bar) in each 4-bar grid cell counted from each window's first row, with its "
               "4-bar return kept only when it stays inside the window, and the normal drift is each coin's mean "
               "non-overlapping 4-bar return over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a "
                           "volume-weighted fall (raw component < 0), as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    unusual_all = []
    fc_all = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 4-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for i in range(0, n - H, H):
                a, b = c[i], c[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            bet = np.zeros(n, dtype=bool)
            trough = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi <= 0:
                    trough = 0.0
                    continue
                trough = min(trough, fi)
                if fi - trough >= BAND:
                    bet[i] = True
                    trough = fi
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                a, b = c[t], c[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                unusual_all.append((b / a - 1.0) - drift)
                fc_all.append(float(f[t]))

    u = np.asarray(unusual_all, dtype=float)
    x = np.asarray(fc_all, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t_stat = float(mean_u / (sd / np.sqrt(n_cases)))

    slope = None
    if n_cases >= 2 and np.ptp(x) > 0:
        slope = float(stats.linregress(x, u).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases over both coins and all windows, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed (zero spread), so neither rule is met."
    elif t_stat >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean unusual move has t >= 2 over at least 30 cases and the slope on the forecast is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t >= 2 with a slope at or below 0 (or undefined) is inconclusive."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move has t <= -2 over at least 30 cases: the price keeps falling after heavy-volume plunges."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of unusual move on signal-bar forecast",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
