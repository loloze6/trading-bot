import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    LB = 60
    FC = "forecast"
    RAW = "debug_info.components.rebound60.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            reg = d["regime"].astype(str).values
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(len(d), np.nan)
            for i in range(len(d)):
                if fc[i] == 0:
                    continue
                n_active += 1
                r = raw[i]
                if not np.isfinite(r):
                    if i >= LB and close[i - LB] > 0:
                        r = close[i] / close[i - LB] - 1.0
                    else:
                        r = np.nan
                # Situation: the veto's regime; expected side: short, only when the 60-day return is positive.
                if reg[i] == "mean_reversion" and fc[i] < 0 and np.isfinite(r) and r > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "slope of 20-bar forward return (net of coin drift) on 60-bar return, mean_reversion grid bars, all coins pooled"
    threshold = "confirm: slope < 0 with t <= -2 and supporting check > 0; reject: slope > 0 with t >= +2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the short side": int(n_agree)},
            "decided_by": ("No active bars, so the forecast never acts in the plan's situation."
                           if n_active == 0 else
                           "Fewer than 90% of the non-zero forecasts are shorts on mean_reversion bars with a positive 60-day return, as the Fidelity requires."),
            "reading": "The situation is read from the recorded regime (the detector's 365-day components are not recorded and windows are too short to rebuild them), and the side as short where the 60-bar change is positive.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    drift = {}
    for coin, wins in bars.items():
        all_fwd = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            reg = d["regime"].astype(str).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                fwd = close[i + H] / close[i] - 1.0
                all_fwd.append(fwd)
                if reg[i] != "mean_reversion":
                    continue
                if i >= LB and np.isfinite(close[i - LB]) and close[i - LB] > 0:
                    x = close[i] / close[i - LB] - 1.0
                else:
                    x = np.nan
                rows.append({"coin": coin, "day": ts.iloc[i].floor("D"), "fwd": fwd, "x": x, "fc": fc[i]})
        drift[coin] = float(np.mean(all_fwd)) if len(all_fwd) else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "fwd", "x", "fc"])
    if len(cases):
        cases["y"] = cases["fwd"] - cases["coin"].map(drift)
    else:
        cases["y"] = []
    reg_cases = cases.dropna(subset=["x", "y"])
    n_cases = int(len(reg_cases))
    n_days = int(reg_cases["day"].nunique()) if n_cases else 0

    # Supporting check: short cases in the grid, unusual move in the signal's direction
    shorts = cases[(cases["fc"] < 0)].dropna(subset=["y"])
    sup_val = float((-shorts["y"]).mean()) if len(shorts) else None
    sup_pass = (sup_val is not None and sup_val > 0) if len(shorts) else None

    counts = {"grid cases inside the regime": n_cases, "distinct days": n_days, "short cases (supporting check)": int(len(shorts))}
    reading = ("Cases are the mean_reversion bars at window positions 0,20,40,... with a 20-bar forward return inside the window; "
               "the 60-bar return is recomputed from closes inside the window only, so grid bars with fewer than 60 prior bars in their window are left out; "
               "drift is each coin's mean 20-bar return over its grid in all windows; the slope's t uses day-clustered standard errors; "
               "the supporting check uses the grid cases inside the regime with a short forecast; minimum counts are on the regression cases.")

    if n_cases < 30 or n_days < 20:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean unusual move of short cases, signal direction, net of drift", "value": sup_val, "passed": sup_pass},
            "counts": counts,
            "decided_by": f"The plan's minimum of 30 grid cases on 20 distinct days is not reached ({n_cases} cases, {n_days} days).",
            "reading": reading,
        }

    x = reg_cases["x"].values.astype(float)
    y = reg_cases["y"].values.astype(float)
    X = np.column_stack([np.ones(len(x)), x])
    XtX = X.T @ X
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    groups = reg_cases["day"].values
    meat = np.zeros((2, 2))
    for g in pd.unique(groups):
        m = groups == g
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    G = len(pd.unique(groups))
    n = len(y)
    k = 2
    corr = (G / (G - 1)) * ((n - 1) / (n - k)) if G > 1 and n > k else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    slope = float(beta[1])
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    t = float(slope / se) if np.isfinite(se) and se > 0 else None

    if t is not None and slope < 0 and t <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is negative with t <= -2 and the supporting check is positive: confirm."
        else:
            status = "inconclusive"
            decided = "The slope is negative with t <= -2 but the supporting check fails: inconclusive."
    elif t is not None and slope > 0 and t >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2: reject."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2 (or cannot be computed): inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "slope t, day-clustered", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move of short cases, signal direction, net of drift", "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
