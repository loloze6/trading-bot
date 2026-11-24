import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RISE = 5
    RAW = "debug_info.components.rise_range.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            rise = close / close.shift(RISE) - 1.0  # inside the window only
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # situation: the raw component is positive (it is >0 only when the 5-bar rise is >0);
            # where the raw value is missing, the 5-bar rise from the window's prices
            sit = pd.Series(np.where(raw.notna(), raw > 0,
                                     np.where(rise.notna(), rise > 0, False)),
                            index=d.index).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "slope of excess 3-bar return on positive forecast (day-clustered t)"
    thr = "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2"
    reading = ("Situation taken as raw component > 0 (5-bar return from prices where raw is missing); "
               "cases are grid bars 0,3,6,... of each window with forecast > 0 and a 3-bar return inside the window; "
               "coin drift is the mean of all its non-overlapping 3-bar grid returns over all windows; "
               "slope by OLS with intercept and cluster-robust (by UTC day, CR1) standard error; "
               "top third = the floor(n/3) largest positive forecasts; the plan's 'inconclusive' for too few cases "
               "is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on which the "
                           "5-day rise is positive (the plan's situation and side)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f > 0:
                    coin_cases.append((f, r, ts.iloc[i].strftime("%Y-%m-%d")))
        if coin_rets:
            drift = float(np.mean(coin_rets))
            for f, r, day in coin_cases:
                rows.append((coin, f, r - drift, day))

    cases = pd.DataFrame(rows, columns=["coin", "f", "ex", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"non-overlapping cases with a forecast above 0": n_cases, "distinct days": n_days}

    slope = None
    tstat = None
    sup_val = None
    sup_pass = None
    if n_cases >= 3 and cases["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), cases["f"].values])
        y = cases["ex"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        G = 0
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
            G += 1
        k = 2
        corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - k)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None
    if n_cases >= 3:
        k3 = n_cases // 3
        top = cases.sort_values("f", ascending=False, kind="mergesort").head(k3)
        if len(top) > 0:
            sup_val = float(top["ex"].mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t, clustered by day", "value": tstat}
                          if tstat is not None else None),
            "threshold": thr}
    sup = {"name": "mean excess 3-bar return of top third of positive forecasts",
           "value": sup_val, "passed": sup_pass}

    if n_cases < 300 or n_days < 150:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 300) on {n_days} days (need 150).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Slope positive with t >= 2 and the top-third mean excess return above 0."
        else:
            status = "inconclusive"
            decided = "Slope positive with t >= 2 but the supporting check fails."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "Slope negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "Slope with |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
