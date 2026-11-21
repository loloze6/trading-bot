import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    F28 = "debug_info.components.fall28.last_history_value"
    NL60 = "debug_info.components.near_low60.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            f28 = pd.to_numeric(df[F28], errors="coerce") if F28 in df.columns else pd.Series(np.nan, index=df.index)
            nl = pd.to_numeric(df[NL60], errors="coerce") if NL60 in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            situation = (f28 < 0).fillna(False) | (nl < 0).fillna(False)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of 10-bar forward return minus normal drift on forecast, non-overlapping 10-bar grid"
    thr = "slope > 0 with t >= 2 confirms (with check); slope < 0 with t <= -2 rejects"
    sup_name = "mean unusual 10-bar move over cases (forecast rise >= 2 points, once per grid cell), long direction, > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("fewer than 90% of bars with a non-zero forecast are long bars where the 28-bar change "
                           "is negative or the close is in the lower half of its 60-bar range, as the Fidelity's situation requires"),
            "reading": "situation read as raw fall28 < 0 or raw near_low60 < 0 (either graded part active), expected side long",
        }

    # ---------- 2. grid samples and drift ----------
    grid_rows = {}   # coin -> list of (forecast, fwd_ret)
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for g in range(0, n, H):
                if g + H < n:
                    r = close[g + H] / close[g] - 1.0
                    if np.isfinite(r):
                        rows.append((fc[g], r))
        grid_rows[coin] = rows

    drift = {}
    for coin, rows in grid_rows.items():
        rs = [r for _, r in rows]
        drift[coin] = float(np.mean(rs)) if len(rs) else np.nan

    X, Y = [], []
    for coin, rows in grid_rows.items():
        d = drift[coin]
        for f, r in rows:
            if np.isfinite(f) and np.isfinite(d):
                X.append(f)
                Y.append(r - d)
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    n_pos_cells = int((X > 0).sum())

    # ---------- 3. cases (long bets), once per grid cell ----------
    case_moves = []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            on_long = False
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    on_long = False
                    ref = 0.0
                    continue
                if not on_long:
                    on_long = True
                    ref = 0.0
                if f - ref >= BAND:
                    bet[i] = True
                    ref = f
                else:
                    ref = min(ref, f)
            for g in range(0, n, H):
                idx = np.where(bet[g:min(g + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = g + int(idx[0])
                if t + H < n and np.isfinite(d):
                    r = close[t + H] / close[t] - 1.0
                    if np.isfinite(r):
                        case_moves.append(r - d)
    n_cases = len(case_moves)
    mean_unusual = float(np.mean(case_moves)) if n_cases else None
    sup_pass = bool(mean_unusual is not None and mean_unusual > 0)

    # ---------- 4. regression ----------
    slope, tval = None, None
    if len(X) >= 3 and np.std(X) > 0:
        lr = stats.linregress(X, Y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {"grid cells with forecast > 0": n_pos_cells, "cases": n_cases, "grid cells (all)": int(len(X))}
    reading = ("situation read as raw fall28 < 0 or raw near_low60 < 0, side long; the regression uses every grid cell "
               "(forecast zero included) at positions 0,10,20,... of each window; normal drift is the coin's mean of those "
               "non-overlapping 10-bar returns over all windows; a case is the first long bet (forecast rise >= 2 from its "
               "lowest level since the last bet, from 0 after a flat) in each grid cell, measured from its bar's close; "
               "the plan's too-few-cases rule is reported as 'not observable'.")

    if n_pos_cells < 300 or n_cases < 100:
        status = "not observable"
        missing = []
        if n_pos_cells < 300:
            missing.append(f"grid cells with forecast > 0 = {n_pos_cells} < 300")
        if n_cases < 100:
            missing.append(f"cases = {n_cases} < 100")
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move over cases is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": mean_unusual,
                             "passed": (sup_pass if n_cases > 0 else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
