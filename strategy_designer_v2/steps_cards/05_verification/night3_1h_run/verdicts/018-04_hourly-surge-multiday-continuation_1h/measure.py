import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 120
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.ret24_multiple.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            recomputed = close / close.shift(24) - 1.0
            if RAW in df.columns:
                raw = df[RAW].astype(float)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            situation = raw > 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 120-bar move after long forecast rises of >= 2 points"
    main_thr = "positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 over at least 30 cases to reject"
    sup_name = "OLS slope of unusual move on forecast at the case's bar"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the 24h return is positive, the plan's situation on its long side.",
            "reading": "The adapted situation is read as 'the 24-bar return is above 0' (graded size, any positive multiple), on the long side.",
        }

    # ---------- 2. Cases ----------
    unusual_all = []
    fc_all = []
    for coin, wins in bars.items():
        # coin's normal drift: mean 120-bar return on the non-overlapping grid of all its windows
        grid_rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).to_numpy()
            n = len(close)
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            close = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).to_numpy()
            n = len(close)
            low = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f):
                    continue
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    low = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n:
                        a, b = close[t], close[t + H]
                        if np.isfinite(a) and np.isfinite(b) and a > 0:
                            unusual_all.append((b / a - 1.0) - drift)
                            fc_all.append(f)
                else:
                    low = min(low, f)

    u = np.array(unusual_all, dtype=float)
    x = np.array(fc_all, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope = None
    if n_cases > 2 and np.std(x) > 0:
        slope = float(stats.linregress(x, u).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    reading = ("The situation is read as 'the 24-bar return is above 0' on the long side; a case is a long-side rise of the forecast of at least 2 points from its lowest level since the last such rise (from 0 after flat), the first per 120-bar grid cell counted from each window's first row, with a full 120-bar forward return inside the window; the drift is the coin's mean 120-bar return on that grid over all windows; the slope is an OLS fit of unusual move on forecast, failed if not computable; fewer than 30 cases is reported as not observable.")

    result = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": {"cases": n_cases},
        "reading": reading,
    }

    if n_cases < MIN_CASES:
        result["status"] = "not observable"
        result["decided_by"] = f"Only {n_cases} cases pooled over the coins and windows, below the plan's minimum of 30."
        return result

    if t_stat is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t-statistic could not be computed (zero spread of the unusual move), so neither confirm nor reject is met."
        return result

    if mean_u > 0 and t_stat >= 2:
        if slope_pass:
            result["status"] = "confirmed"
            result["decided_by"] = "The mean unusual move is positive with t >= 2 over at least 30 cases and the slope on the forecast is above 0."
        else:
            result["status"] = "inconclusive"
            result["decided_by"] = "t >= 2 with a slope at or below 0 (or not computable) is inconclusive."
    elif mean_u < 0 and t_stat <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "The mean unusual move is negative with t <= -2 over at least 30 cases."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t-statistic is between -2 and 2."
    return result
