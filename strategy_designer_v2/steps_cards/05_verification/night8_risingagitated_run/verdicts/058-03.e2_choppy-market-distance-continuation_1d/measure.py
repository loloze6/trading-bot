import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.ma_dist.last_history_value"
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            active = f != 0
            n_active += int(active.sum())
            # choppy profile: the detector's un-vetoed regime ("unknown": |60-bar evolution| <= 10)
            in_profile = reg == "unknown"
            side_ok = np.isfinite(raw) & (np.sign(raw) == np.sign(f)) & (raw != 0)
            n_agree += int((active & in_profile & side_ok).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "slope of 10-bar excess forward return on forecast"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy-profile bars "
                           "whose forecast sign matches the sign of the close's distance from its 20-day SMA."),
            "reading": "The choppy profile is read as the detector's un-vetoed regime 'unknown' and the expected side as the sign of the raw SMA distance.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        cand = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True).values
            n = len(df)
            for i in range(0, n - H, H):
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] != 0:
                    cand.append((r, float(f[i]), pd.Timestamp(ts[i]).floor("D")))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, fv, d in cand:
            rows.append((r - drift, fv, d))

    n_cases = len(rows)
    counts = {"grid cases with a non-zero forecast": int(n_cases)}
    reading = ("Choppy profile read as regime 'unknown' (no trend veto); slope is OLS with intercept of excess return "
               "on forecast, t from day-clustered standard errors with G/(G-1) correction; drift is the mean of each "
               "coin's non-overlapping 10-bar grid returns over all its windows.")

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Fewer than {MIN_CASES} grid cases with a non-zero forecast ({n_cases}).",
            "reading": reading,
        }

    y = np.array([r[0] for r in rows])
    x = np.array([r[1] for r in rows])
    days = np.array([str(r[2]) for r in rows])
    X = np.column_stack([np.ones(n_cases), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    meat = np.zeros((2, 2))
    uniq = np.unique(days)
    G = len(uniq)
    for d in uniq:
        m = days == d
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    V = XtX_inv @ meat @ XtX_inv
    if G > 1:
        V *= G / (G - 1)
    se = float(np.sqrt(max(V[1, 1], 0.0)))
    slope = float(beta[1])
    t = float(slope / se) if se > 0 else 0.0
    counts["days"] = int(G)

    if slope > 0 and t >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2: a larger distance is followed by a larger excess move its way."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: the distance is faded, not followed."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "day-clustered t of slope", "value": t},
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
