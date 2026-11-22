import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MA = 180
    RAW = "debug_info.components.relief_rally.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            up = close > close.shift(1)
            sma = close.rolling(MA, min_periods=MA).mean()
            below = close < sma
            # situation: component positive (up streak gain x depth below average) and,
            # where computable from prices, bar closed up and close below its 180-bar SMA
            sit = raw.fillna(0) > 0
            sit = sit & (up | close.shift(1).isna())
            sit = sit & (below | sma.isna())
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 18-bar move of short cases (signed for the short), pooled"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    supp_name = "mean unusual move of cases with |forecast| above median minus the others"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars where the 4h bar closed up in a streak with the close below its 180-bar average, as the Fidelity's situation and short side require.",
            "reading": "Situation taken as a positive raw component value, checked against an up close and close below the 180-bar SMA where the SMA is computable inside the window.",
        }

    # ---------- 2. Criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 18-bar returns over all windows
        drift_rets = []
        prepared = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    drift_rets.append(r)
            prepared.append((close, fc))
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))

        for close, fc in prepared:
            n = len(close)
            ref = 0.0
            prev_short = False
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f >= 0:
                    ref = 0.0
                    prev_short = False
                    continue
                if not prev_short:
                    ref = 0.0
                prev_short = True
                if f <= ref - BAND:
                    ref = f
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            unusual.append(-(r - drift))
                            absf.append(abs(f))
                else:
                    ref = max(ref, f)

    u = np.array(unusual, dtype=float)
    a = np.array(absf, dtype=float)
    n_cases = int(len(u))
    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases >= 2:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    supp_val = None
    supp_pass = None
    n_hi = n_lo = 0
    if n_cases > 0:
        med = float(np.median(a))
        hi = u[a > med]
        lo = u[a <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            supp_val = float(np.mean(hi) - np.mean(lo))
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 independent cases ({n_cases}), the plan's minimum count, so the data could not show the idea."
    elif mean_u > 0 and t_u is not None and t_u >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "Mean unusual move is positive with t >= 2 over at least 30 independent cases and the supporting check is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2, positive mean) whose supporting check is not above 0."
    elif mean_u < 0 and t_u is not None and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual move is negative with t <= -2 over at least 30 independent cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": supp_name, "value": supp_val, "passed": supp_pass},
        "counts": {"independent cases": n_cases, "cases above median |forecast|": n_hi, "cases at or below median |forecast|": n_lo},
        "decided_by": decided,
        "reading": "A case is the first short bet (forecast falling >= 2 points below its highest short level since the last bet, reset at flat or side change) in each 18-bar grid cell counted from each window's first row, the drift is the coin's mean non-overlapping 18-bar return over all its windows, and cases at the median |forecast| go to the smaller group.",
    }
