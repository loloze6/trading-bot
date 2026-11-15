import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    SLOPE_COL = "debug_info.components.slope.last_history_value"
    ALLOC_COL = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            regime_ok = df["regime"].astype(str) == "trending"
            if SLOPE_COL in df.columns:
                slope = pd.to_numeric(df[SLOPE_COL], errors="coerce")
                slope_ok = slope.notna() & (slope < 0)
            else:
                slope_ok = pd.Series(False, index=df.index)
            side_ok = fc < 0
            agree = active & regime_ok & slope_ok & side_ok
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "ordinary t of mean allocation x (20-bar return minus coin mean 20-bar return), shorts only"
    threshold = "confirm if t >= 2 and supporting slope < 0; reject if t <= -2; inconclusive otherwise or if fewer than 30 active cases"
    reading = ("Situation checked as regime == 'trending' (detector's close below SMA200) and raw 20-bar SMA200 slope "
               "(last_history_value) below 0 with forecast below 0; allocation x is the postRebalance_current_allocation "
               "held after the case bar's trade, the coin's mean 20-bar return is taken over all non-overlapping grid bars "
               "of all its windows, and a case requires forecast < 0 at the grid bar and a close 20 bars later in the same window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active cases": None},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are short bars with the close below its SMA200 "
                           "and a declining SMA200, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_x, case_ex, case_absf = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            alloc = (pd.to_numeric(df[ALLOC_COL], errors="coerce").to_numpy(dtype=float)
                     if ALLOC_COL in df.columns else np.full(len(df), np.nan))
            for t in range(0, len(df) - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0 and np.isfinite(alloc[t]):
                    coin_cases.append((r, alloc[t], fc[t]))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for r, a, f in coin_cases:
            ex = r - mu
            case_x.append(a * ex)
            case_ex.append(ex)
            case_absf.append(abs(f))

    n_cases = len(case_x)
    x = np.asarray(case_x, dtype=float)
    mean_val = float(np.mean(x)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(x, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_cases)))

    slope_val = None
    if n_cases >= 3:
        af = np.asarray(case_absf, dtype=float)
        if np.ptp(af) > 0:
            slope_val = float(stats.linregress(af, np.asarray(case_ex, dtype=float)).slope)
    slope_pass = None if slope_val is None else bool(slope_val < 0)

    counts = {"active cases": int(n_cases)}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} active cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The main t could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif t_val >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "The main t is 2 or more and the supporting slope is below 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main t is -2 or less: the shorts lose against the coin's drift."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the supporting slope is not below 0."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "ordinary t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of excess 20-bar return on |forecast|, must be below 0",
            "value": slope_val,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
