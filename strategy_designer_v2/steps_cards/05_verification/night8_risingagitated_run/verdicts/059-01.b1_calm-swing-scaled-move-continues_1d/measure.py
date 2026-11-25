import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.swing_move.last_history_value"
    CALM_REGIME = "unknown"  # the regime that carries the strategy; "chop" is the veto when vol percentile > 0.5

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp")
            f = pd.to_numeric(d["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            calm = d["regime"].astype(str) == CALM_REGIME
            # expected side: same sign as the 20-day scaled move (rise -> long, fall -> short)
            side_ok = raw.notna() & (raw != 0) & (np.sign(raw) == np.sign(f))
            n_agree += int((active & calm & side_ok).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    threshold_txt = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"
    reading = ("Calm bars are the bars whose recorded regime is the strategy's regime 'unknown' (not the 'chop' veto), "
               "the expected side is the sign of the raw scaled move; the regression is pooled OLS with an intercept, "
               "the slope's t from standard errors clustered by UTC calendar day (with the usual small-sample factor), "
               "and the normal 5-bar drift is the coin's mean 5-bar return over the non-overlapping grids of all its windows.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": None,
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are calm-regime bars with the forecast "
                           "on the side of the 20-day scaled move, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] != 0:
                    coin_cases.append((r, float(f[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        if len(coin_grid_rets) == 0:
            continue
        drift = float(np.mean(coin_grid_rets))
        for r, fv, day in coin_cases:
            rows.append((r - drift, fv, day, coin))

    n_cases = len(rows)
    days = sorted(set(r[2] for r in rows))
    n_days = len(days)
    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}
    sit = {"agreement": (float(agreement) if agreement is not None else None), "passed": passed}

    slope = None
    tval = None
    if n_cases >= 3:
        y = np.array([r[0] for r in rows], dtype=float)
        x = np.array([r[1] for r in rows], dtype=float)
        X = np.column_stack([np.ones_like(x), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            day_arr = np.array([r[2] for r in rows])
            meat = np.zeros((2, 2))
            for dday in days:
                m = day_arr == dday
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            G = n_days
            N, K = X.shape
            corr = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 and N > K else 1.0
            V = corr * XtX_inv @ meat @ XtX_inv
            slope = float(beta[1])
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    main = {
        "name": "slope of 5-bar forward return minus normal drift on forecast (non-overlapping grid)",
        "value": slope,
        "statistic": ({"name": "t of slope, clustered by day", "value": tval} if tval is not None else None),
        "threshold": threshold_txt,
    }

    if n_cases < 200 or n_days < 100:
        return {
            "status": "not observable",
            "situation_check": sit,
            "main_measure": main,
            "supporting_check": None,
            "counts": counts,
            "decided_by": (f"The plan's minimum of 200 grid cases on at least 100 distinct days is not reached "
                           f"({n_cases} cases on {n_days} days)."),
            "reading": reading,
        }

    if slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "Confirm rule met: slope > 0 with t >= 2 (no supporting check in the plan)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule met: slope < 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
