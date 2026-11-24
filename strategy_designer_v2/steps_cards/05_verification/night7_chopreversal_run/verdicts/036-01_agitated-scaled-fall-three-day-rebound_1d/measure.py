import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback where not recorded: 1-day return / std of last 30 daily returns (inside the window)
            r1 = close.pct_change()
            raw_re = r1 / r1.rolling(30, min_periods=30).std()
            raw = raw.where(raw.notna(), raw_re)
            regime = df["regime"].astype(str)
            agitated = regime != "chop"
            situation = (raw < 0) & agitated
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "slope t of 3-bar excess return on forecast, cases of a day clustered"
    thr = "confirm: t >= 2 with >= 100 cases and supporting check passing; reject: t <= -2 with >= 100 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a one-day fall "
                           "(scaled return < 0) in the agitated profile (regime not chop)"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "Agitated profile read from the recorded regime (any regime but the veto's 'chop').",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_r3, grid_r13 = [], []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1, c3 = close[t], close[t + 1], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c3)) or c0 <= 0:
                    continue
                r3 = c3 / c0 - 1.0
                r13 = (c3 / c1 - 1.0) if (np.isfinite(c1) and c1 > 0) else np.nan
                grid_r3.append(r3)
                if np.isfinite(r13):
                    grid_r13.append(r13)
                f = fc[t]
                if np.isfinite(f) and f > 0:
                    day = ts.iloc[t].floor("D") if pd.notna(ts.iloc[t]) else None
                    coin_rows.append((coin, day, f, r3, r13))
        if not grid_r3:
            continue
        m3 = float(np.mean(grid_r3))
        m13 = float(np.mean(grid_r13)) if grid_r13 else np.nan
        for (c, d, f, r3, r13) in coin_rows:
            rows.append({"coin": c, "day": d, "f": f, "ex3": r3 - m3,
                         "ex13": (r13 - m13) if np.isfinite(r13) and np.isfinite(m13) else np.nan})

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "ex3", "ex13"])
    cases = cases.dropna(subset=["f", "ex3", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope, tval = None, None
    if n_cases >= 3 and n_days >= 3 and cases["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), cases["f"].values])
        y = cases["ex3"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in cases.reset_index(drop=True).groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G, N, K = n_days, n_cases, 2
        corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1]))
        slope = float(beta[1])
        tval = float(slope / se) if se > 0 else None

    sup = cases.dropna(subset=["ex13"])
    sup_val = None
    if len(sup) and sup["f"].sum() > 0:
        sup_val = float((sup["ex13"] * sup["f"]).sum() / sup["f"].sum())
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if n_cases < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases is not reached ({n_cases} cases)."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t is 2 or more with at least 100 cases and the forecast-weighted t+1..t+3 excess return is above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the supporting check fails: a confirming slope with a failed check is inconclusive."
    elif tval <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less with at least 100 cases."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "day-clustered OLS slope t", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "forecast-weighted mean excess return close[t+1] to close[t+3]",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"cases": n_cases, "days": n_days},
        "decided_by": decided,
        "reading": ("Agitated profile read from the recorded regime (not 'chop'); the regression has an intercept and "
                    "a day-clustered (CR1) standard error; the supporting check's excess removes the coin's mean "
                    "close[t+1]-to-close[t+3] return on the same 3-bar grid over all its windows; fewer than 100 "
                    "cases is reported as 'not observable' per the minimum-count rule."),
    }
