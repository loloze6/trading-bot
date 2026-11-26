import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.ret20.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True)

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            recomputed = close / close.shift(20) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 10-bar forward return minus coin drift on forecast (grid cases)"
    threshold_txt = "slope t >= 2 confirms (with positive timing part), t <= -2 rejects, else inconclusive"
    sup_name = "timing part of book's mean daily return before costs"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the sign of the "
                           "20-day return (long after a rise, short after a fall), as the Fidelity's situation requires."),
            "reading": "The situation is the 20-day return itself, so a bar of the situation on its side is one whose forecast sign equals the raw 20-day return's sign (recomputed from closes where not recorded).",
        }

    # ---------------- main measure ----------------
    case_rows = []
    daily_rows = []
    for coin, wins in bars.items():
        coin_grid = []
        coin_daily = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").values
            day = _ts(d).dt.floor("D").values
            n = len(d)
            for i in range(0, n, H):
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    coin_grid.append((coin, day[i], fc[i], r))
            for i in range(n - 1):
                r1 = close[i + 1] / close[i] - 1.0
                coin_daily.append((coin, day[i], alloc[i], r1))
        g = pd.DataFrame(coin_grid, columns=["coin", "day", "fc", "r"])
        dd = pd.DataFrame(coin_daily, columns=["coin", "day", "alloc", "r1"])
        if len(g):
            drift = g["r"].dropna().mean()
            g["ex"] = g["r"] - drift
            case_rows.append(g)
        if len(dd):
            mu = dd["r1"].dropna().mean()
            dd["gross"] = dd["alloc"] * dd["r1"]
            dd["mkt"] = dd["alloc"] * mu
            daily_rows.append(dd)

    cases = pd.concat(case_rows, ignore_index=True) if case_rows else pd.DataFrame(columns=["coin", "day", "fc", "r", "ex"])
    cases = cases.dropna(subset=["fc", "ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t_val = None
    if n_cases >= 3 and n_days >= 2 and cases["fc"].astype(float).std() > 0:
        y = cases["ex"].astype(float).values
        x = cases["fc"].astype(float).values
        X = np.column_stack([np.ones_like(x), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days
        N, K = X.shape
        corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1]))
        slope = float(beta[1])
        t_val = float(slope / se) if se > 0 else None

    # ---------------- supporting check ----------------
    timing = None
    if daily_rows:
        dly = pd.concat(daily_rows, ignore_index=True).dropna(subset=["gross", "mkt"])
        if len(dly):
            per_day = dly.groupby("day")[["gross", "mkt"]].mean()
            timing = float(per_day["gross"].mean() - per_day["mkt"].mean())
    sup_passed = None if timing is None else bool(timing > 0)

    counts = {"grid cases": n_cases, "distinct days": n_days}

    if n_cases < 300 or n_days < 100:
        status = "not observable"
        decided = (f"The plan's minimum of at least 300 grid cases over at least 100 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing part of the book's mean daily return is positive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger 20-day moves are followed by moves back the other way."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing part of the book's mean daily return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_val is None else {"name": "slope t, SE clustered by day", "value": t_val},
            "threshold": threshold_txt,
        },
        "supporting_check": {"name": sup_name, "value": timing, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Every grid bar (positions 0,10,20,... of each window with a 10-bar forward return inside it) is a case, "
                    "including zero forecasts, regressed with an intercept and day-clustered SEs with the usual G/(G-1)*(N-1)/(N-K) "
                    "correction; the drift is the coin's mean grid 10-bar return over all windows; the book's return before costs "
                    "is the held allocation times the next bar's return, averaged over coins per day, minus the allocation times "
                    "the coin's mean daily return over all windows."),
    }
