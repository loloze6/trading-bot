import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    ER_P = 30
    R30_P = 30
    ER_MAX = 0.3
    MIN_ACTIVE = 40
    RAW = "debug_info.components.scaled_move.last_history_value"
    PPV = "debug_info.components.scaled_move.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active_checked = 0
    n_agree = 0
    n_active_total = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            n = len(df)
            absdiff = np.abs(np.diff(close, prepend=np.nan))
            for t in range(n):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                n_active_total += 1
                # needs 30 bars of history inside the window to recompute ER and r30
                if t < max(ER_P, R30_P):
                    continue
                c0 = close[t - ER_P]
                ct = close[t]
                path = np.nansum(absdiff[t - ER_P + 1:t + 1])
                if not (np.isfinite(c0) and np.isfinite(ct)) or path <= 0:
                    continue
                er = abs(ct - c0) / path
                r30 = ct / close[t - R30_P] - 1.0
                # 7-day move: the recorded raw component (sign = sign of r7), else from prices
                if np.isfinite(raw[t]):
                    r7s = np.sign(raw[t])
                elif t >= 7 and np.isfinite(close[t - 7]):
                    r7s = np.sign(ct / close[t - 7] - 1.0)
                else:
                    continue
                n_active_checked += 1
                in_situation = (er < ER_MAX + 1e-12) and r7s != 0 and np.sign(r30) == r7s
                expected_side = r7s  # continuation: rise -> long, fall -> short
                if in_situation and np.sign(fc[t]) == expected_side:
                    n_agree += 1

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation checked on active bars with at least 30 earlier bars in their window "
               "(ER and r30 recomputed from closes, side = sign of the recorded raw scaled_move, i.e. of r7, "
               "continuation expected); drift is the coin's mean 7-bar return on the 7-bar grid of all its "
               "windows; the slope t is the OLS t of drift-removed return on post_pipeline_value; the plan's "
               "minimum of 40 active grid bars is treated as a minimum count (not observable if unmet).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_checked),
                       "active bars total": int(n_active_total)},
            "decided_by": ("Fewer than 90% of active bars checked are bars with 30-day ER below 0.3 and "
                           "30-day and 7-day returns of the same sign, with the forecast on the 7-day move's side"
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # drift per coin: mean 7-bar return on non-overlapping grid of all windows
    drift = {}
    grid_rows = []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ppv = (pd.to_numeric(df[PPV], errors="coerce").to_numpy(dtype=float)
                   if PPV in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                rets.append(r)
                if np.isfinite(fc[t]) and fc[t] != 0:
                    grid_rows.append((coin, r, ppv[t], fc[t]))
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    x, y, d = [], [], []
    for coin, r, p, f in grid_rows:
        if not (np.isfinite(p) and np.isfinite(drift[coin])):
            continue
        dr = r - drift[coin]
        x.append(p)
        y.append(dr)
        d.append(np.sign(f) * dr)
    x = np.array(x)
    y = np.array(y)
    d = np.array(d)
    n_cases = int(len(x))

    slope = None
    tval = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr > 0 else None
    mean_dir = float(np.mean(d)) if n_cases > 0 else None
    check_pass = (mean_dir is not None and mean_dir > 0)

    main = {
        "name": "OLS slope of drift-removed next 7-bar return on scaled_move post_pipeline_value",
        "value": slope,
        "statistic": ({"name": "t of the OLS slope", "value": tval} if tval is not None else None),
        "threshold": "confirm if t >= 2 (with supporting check passing); reject if t <= -2",
    }
    sup = {"name": "mean drift-removed 7-bar return in forecast direction, before costs",
           "value": mean_dir, "passed": bool(check_pass) if mean_dir is not None else None}
    counts = {"active grid bars across all coins and windows": n_cases}

    if n_cases < MIN_ACTIVE:
        status = "not observable"
        decided = f"Only {n_cases} active grid bars, fewer than the plan's minimum of 40."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif tval >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean directional drift-removed return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger aligned moves are followed by moves the other way."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
