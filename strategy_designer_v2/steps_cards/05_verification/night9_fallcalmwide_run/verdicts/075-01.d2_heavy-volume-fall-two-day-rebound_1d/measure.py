import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    H = 2
    MIN_CASES = 300
    MIN_DAYS = 150

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    per_coin_frames = {}
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float).values
            ret1 = np.full(len(d), np.nan)
            if len(d) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            down = ret1 < 0
            # first bar of a window: previous close not recorded; use the regime the detector chose there
            if len(d) > 0 and "regime" in d.columns:
                down[0] = str(d["regime"].iloc[0]) == "mean_reversion"
            d["_down"] = down
            fc = pd.to_numeric(d[FC], errors="coerce").values
            d["_fc"] = fc
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & down & (fc > 0)).sum())
            fwd = np.full(len(d), np.nan)
            if len(d) > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0
            d["_fwd"] = fwd
            d["_pos"] = np.arange(len(d))
            d["_win"] = w
            frames.append(d)
        if frames:
            per_coin_frames[coin] = frames

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    sit = {"agreement": float(agreement), "passed": passed}

    main_name = "t of slope of excess 2-bar return on forecast, SE clustered by day"
    main_thr = "confirm if t >= 2 (with top-minus-bottom third > 0); reject if t <= -2"
    reading = ("A down day is close below the previous close inside the window (the regime column on a window's "
               "first bar), cases are grid bars (positions 0,2,4,... of each window) with a down day, forecast > 0 and "
               "a 2-bar return inside the window, the coin's mean is over all its windows' grid 2-bar returns, thirds "
               "are the n//3 cases with the largest and smallest forecasts (stable sort), the cluster-robust SE uses "
               "the usual G/(G-1)*(N-1)/(N-K) correction, and too few cases or days gives 'not observable' as the "
               "workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with non-zero forecast are down days with a long forecast, "
                           "so the config does not do what the plan's Fidelity (long after a down day) says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []
    for coin, frames in per_coin_frames.items():
        grid_rets = []
        for d in frames:
            g = d[(d["_pos"] % H == 0) & np.isfinite(d["_fwd"])]
            grid_rets.append(g["_fwd"].values)
        allg = np.concatenate(grid_rets) if grid_rets else np.array([])
        if len(allg) == 0:
            continue
        mu = float(np.mean(allg))
        for d in frames:
            m = ((d["_pos"] % H == 0) & np.isfinite(d["_fwd"]) & d["_down"].astype(bool)
                 & np.isfinite(d["_fc"]) & (d["_fc"] > 0))
            sub = d[m]
            for _, r in sub.iterrows():
                cases.append((r["timestamp"].floor("D"), float(r["_fc"]), float(r["_fwd"]) - mu))

    n_cases = len(cases)
    days = pd.Series([c[0] for c in cases]) if cases else pd.Series([], dtype="datetime64[ns, UTC]")
    n_days = int(days.nunique()) if n_cases else 0
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    t_val = None
    slope = None
    diff = None
    if n_cases >= 3:
        x = np.array([c[1] for c in cases])
        y = np.array([c[2] for c in cases])
        X = np.column_stack([np.ones(n_cases), x])
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        u = y - X @ beta
        codes = pd.factorize(days)[0]
        G = int(codes.max()) + 1
        meat = np.zeros((2, 2))
        for gi in range(G):
            idx = codes == gi
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        K = 2
        corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - K)) if G > 1 else np.nan
        V = corr * XtX_inv @ meat @ XtX_inv
        se = np.sqrt(V[1, 1]) if np.isfinite(V[1, 1]) and V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_val = float(slope / se) if np.isfinite(se) and se > 0 else None

        k = n_cases // 3
        if k >= 1:
            order = np.argsort(x, kind="mergesort")
            bottom = y[order[:k]]
            top = y[order[-k:]]
            diff = float(np.mean(top) - np.mean(bottom))

    sup_passed = None if diff is None else bool(diff > 0)
    main = {"name": main_name, "value": t_val,
            "statistic": {"name": "OLS slope t, day-clustered SE", "value": t_val} if t_val is not None else None,
            "threshold": main_thr}
    sup = {"name": "mean excess 2-bar return, top third minus bottom third by forecast",
           "value": diff, "passed": sup_passed}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum of {MIN_CASES} cases on {MIN_DAYS} distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom-third difference is above 0 (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom-third difference is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
