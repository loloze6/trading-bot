import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    MAX_STREAK = 180

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            vol = df["volume"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            streak = np.zeros(n, dtype=int)
            for i in range(1, n):
                if np.isfinite(close[i]) and np.isfinite(close[i - 1]) and close[i] < close[i - 1]:
                    streak[i] = min(streak[i - 1] + 1, MAX_STREAK)
                else:
                    streak[i] = 0
            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                k = streak[i]
                situ = False
                if k >= 2:
                    y = vol[i - k + 1:i + 1]
                    if np.all(np.isfinite(y)):
                        x = np.arange(k, dtype=float)
                        slope = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
                        situ = slope < 0
                if situ and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 18-bar return of bets over the coin's normal 18-bar drift"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation read as: the bar closed below the previous close, within a down-streak of at least 2 down closes "
               "inside the window, whose down bars' volume has a negative least-squares slope (declining volume), on the long side; "
               "a case is the first bet (forecast rise of >= 2 points from its lowest positive level since the last bet, from 0 after flat) "
               "in each 18-bar grid cell counted from each window's first row, with a full 18-bar return in the window; "
               "fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a down-streak with declining "
                           "volume: the config's gate (volume slope above 0) and the plan's situation disagree."
                           if n_active > 0 else "No active bars: the forecast is never non-zero."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess = []
    fvals = []
    for coin, wins in bars.items():
        # normal drift over all windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for df in prepared:
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            ref = 0.0
            prev_pos = False
            bets = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f > 0:
                    if not prev_pos:
                        ref = 0.0
                    if f - ref >= BAND:
                        bets[i] = True
                        ref = f
                    else:
                        ref = min(ref, f)
                    prev_pos = True
                else:
                    prev_pos = False
                    ref = 0.0
            for c0 in range(0, n, H):
                idx = np.where(bets[c0:c0 + H])[0]
                if len(idx) == 0:
                    continue
                i = c0 + idx[0]
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                excess.append(r - drift)
                fvals.append(fc[i])

    ncases = len(excess)
    ex = np.array(excess, dtype=float)
    fv = np.array(fvals, dtype=float)
    mean = float(ex.mean()) if ncases > 0 else None
    tval = None
    if ncases >= 2:
        sd = ex.std(ddof=1)
        tval = float(mean / (sd / np.sqrt(ncases))) if sd > 0 else None
    slope = None
    if ncases >= 3 and np.unique(fv).size >= 2:
        slope = float(stats.linregress(fv, ex).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if ncases < MIN_CASES:
        status = "not observable"
        decided = f"Only {ncases} cases across all coins and windows, below the plan's minimum of 30."
    elif tval is not None and mean > 0 and tval >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean excess 18-bar return positive with t >= 2 over at least 30 cases, and the slope on the forecast is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t with a slope at or below 0 (or not computable) is inconclusive."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean excess 18-bar return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or is not computable): inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
                         "threshold": threshold},
        "supporting_check": {"name": "slope of excess 18-bar return on bet-bar forecast", "value": slope,
                             "passed": slope_pass},
        "counts": {"cases": int(ncases)},
        "decided_by": decided,
        "reading": reading,
    }
