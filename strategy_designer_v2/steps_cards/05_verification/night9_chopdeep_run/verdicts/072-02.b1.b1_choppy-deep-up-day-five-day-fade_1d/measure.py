import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    MIN_CASES = 30
    DEPTH_RAW = "debug_info.components.depth.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            day_ret = close / close.shift(1) - 1.0  # inside the window only
            up = day_ret > 0
            # first bar of a window: no previous close in the window, fall back on the detector's decision
            if "regime" in d.columns and len(d) > 0 and pd.isna(day_ret.iloc[0]):
                up.iloc[0] = str(d["regime"].iloc[0]) == "mean_reversion"
            if DEPTH_RAW in d.columns:
                depth = pd.to_numeric(d[DEPTH_RAW], errors="coerce")
                below_high = depth.notna() & (depth <= 0)
            else:
                below_high = pd.Series(False, index=d.index)
            situation = up & below_high
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    sit = {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)}

    main_name = "slope of 5-day return minus drift on forecast, pooled, day-clustered"
    threshold = "confirm if slope t >= 2 (with supporting check), reject if slope t <= -2, with at least 30 cases"
    reading = ("Up day recomputed from consecutive closes inside each window (the detector's regime on a window's first bar), "
               "situation = up day with the recorded depth at or below 0, side short; grid = rows 0,5,10,... of each window "
               "with a 5-bar return inside it; drift = coin's mean grid 5-day return over all its windows; OLS with intercept, "
               "CR1 cluster-robust SE by UTC day; fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are up days with the close below the 20-day high "
                           "carrying a short forecast, so the config does not do what the Fidelity's situation and side say."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_all = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_all.append(r)
                if fc[i] != 0:
                    coin_rows.append((r, float(fc[i]), ts.iloc[i].normalize()))
        if len(coin_all) == 0:
            continue
        drift = float(np.mean(coin_all))
        for r, f, day in coin_rows:
            rows.append((r - drift, f, day))

    n_cases = len(rows)
    days = sorted(set(x[2] for x in rows))
    counts = {"cases": int(n_cases), "days": int(len(days))}

    slope = None
    t = None
    sup_val = None
    if n_cases >= 3:
        y = np.array([x[0] for x in rows], dtype=float)
        f = np.array([x[1] for x in rows], dtype=float)
        X = np.column_stack([np.ones(n_cases), f])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            u = y - X @ beta
            day_idx = {d: k for k, d in enumerate(days)}
            g = np.array([day_idx[x[2]] for x in rows])
            G = len(days)
            meat = np.zeros((2, 2))
            for k in range(G):
                m = g == k
                s = X[m].T @ u[m]
                meat += np.outer(s, s)
            if G > 1 and n_cases > 2:
                corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
                V = corr * XtX_inv @ meat @ XtX_inv
                se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
                slope = float(beta[1])
                t = float(beta[1] / se) if np.isfinite(se) and se > 0 else None
            else:
                slope = float(beta[1])
        sup_val = float(np.mean(-y))
    elif n_cases > 0:
        y = np.array([x[0] for x in rows], dtype=float)
        sup_val = float(np.mean(-y))

    sup_passed = (sup_val > 0) if sup_val is not None else None
    supporting = {"name": "mean unusual 5-day move in the short direction > 0",
                  "value": sup_val, "passed": (bool(sup_passed) if sup_passed is not None else None)}
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "day-clustered slope t", "value": t} if t is not None else None),
            "threshold": threshold}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with a nonzero forecast, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Slope t is 2 or more with at least 30 cases and the mean short-direction unusual move is above 0."
        else:
            status = "inconclusive"
            decided = "Slope t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less with at least 30 cases: deeper up-day closes are followed by larger rises."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2 with at least 30 cases."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
