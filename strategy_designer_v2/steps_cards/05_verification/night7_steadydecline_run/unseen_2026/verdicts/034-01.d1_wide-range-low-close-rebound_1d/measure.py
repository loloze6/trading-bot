import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.lowclose_range.last_history_value"
    AGIT = "mean_reversion"

    rows = []
    all_rets = {}
    for coin, wins in bars.items():
        coin_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            coin_rets.append(nxt.dropna().values)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            rows.append(pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": ts.dt.floor("D").astype("int64").values,
                "forecast": pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values,
                "regime": d["regime"].astype(str).values,
                "raw": raw.values,
                "ret": nxt.values,
            }))
        all_rets[coin] = np.concatenate(coin_rets) if coin_rets else np.array([])

    reading = ("The agitated regime is read from the recorded `regime` (mean_reversion), since the detector's 365-day "
               "volatility rank cannot be rebuilt inside 120-bar windows; the situation is that regime with the raw "
               "low-close range reading above 0 on the long side; the next-day return (every bar, horizon 1) minus the "
               "coin's mean 1-day return over all its windows is regressed with OLS on the forecast with day-clustered "
               "errors (CR1 small-sample correction); the top quintile is the pooled agitated bars (all coins, forecast "
               "0 included) with forecast at or above the pooled 80th percentile; the minimum counts are agitated bars "
               "with forecast > 0 and a next-day return, and the distinct days they fall on.")

    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "slope of next-day excess return on forecast (agitated, forecast > 0)",
                                 "value": None, "statistic": None,
                                 "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects"},
                "supporting_check": None,
                "counts": {"agitated bars with forecast > 0": 0, "distinct days": 0},
                "decided_by": "No bars in the record.", "reading": reading}

    df = pd.concat(rows, ignore_index=True)

    # --- situation check ---
    active = df[df["forecast"] != 0]
    n_active = len(active)
    if n_active > 0:
        ok = (active["regime"] == AGIT) & (active["raw"] > 0) & (active["forecast"] > 0)
        agreement = float(ok.sum()) / n_active
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": {"name": "slope of next-day excess return on forecast (agitated, forecast > 0)",
                                 "value": None, "statistic": None,
                                 "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects"},
                "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are agitated bars with a low-close "
                               "range reading above 0 and a long forecast, as the Fidelity's situation and side require."
                               if n_active > 0 else "The record has no bar with a non-zero forecast."),
                "reading": reading}

    # --- excess returns ---
    mean_ret = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in all_rets.items()}
    df["xret"] = df["ret"] - df["coin"].map(mean_ret)
    agit = df[(df["regime"] == AGIT) & df["xret"].notna()]
    samp = agit[agit["forecast"] > 0]
    n = int(len(samp))
    n_days = int(samp["day"].nunique())

    # --- main measure: clustered OLS slope ---
    slope, t = None, None
    if n >= 3 and n_days >= 2:
        x = samp["forecast"].values.astype(float)
        y = samp["xret"].values.astype(float)
        X = np.column_stack([np.ones(n), x])
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        g_ids = samp["day"].values
        for g in np.unique(g_ids):
            m = g_ids == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        G = len(np.unique(g_ids))
        k = 2
        corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if n > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t = float(slope / se) if se and np.isfinite(se) and se > 0 else None

    # --- supporting check: top quintile ---
    top_mean, sup_pass = None, None
    if len(agit) > 0:
        q = float(np.quantile(agit["forecast"].values, 0.8))
        top = agit[agit["forecast"] >= q]
        if len(top) > 0:
            top_mean = float(top["xret"].mean())
            sup_pass = bool(top_mean > 0)

    counts = {"agitated bars with forecast > 0": n, "distinct days": n_days,
              "top-quintile agitated bars": int(len(top)) if len(agit) > 0 else 0}

    main = {"name": "slope of next-day excess return on forecast (agitated, forecast > 0)",
            "value": slope,
            "statistic": ({"name": "OLS t, errors clustered by day", "value": t} if t is not None else None),
            "threshold": "positive with t >= 2 (and top-quintile mean > 0) confirms; negative with t <= -2 rejects"}
    support = {"name": "mean next-day excess return of top-quintile forecasts (agitated bars)",
               "value": top_mean, "passed": sup_pass}

    if n < 300 or n_days < 150:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n} agitated bars with forecast > 0 (need 300) "
                   f"on {n_days} distinct days (need 150).")
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top-quintile mean excess return is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "A positive slope with t >= 2 while the top-quintile mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": support,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
