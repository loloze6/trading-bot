import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.day_fall.last_history_value"

    def _ts(s):
        if pd.api.types.is_numeric_dtype(s):
            unit = "s" if np.nanmax(s.values.astype(float)) < 1e11 else "ms"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- gather per-coin data, returns inside windows only ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        parts = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            close = d["close"].astype(float)
            d["_next_ret"] = close.shift(-1) / close - 1.0   # inside the window only
            d["_day_ret"] = close / close.shift(1) - 1.0     # inside the window only
            all_rets.append(d["_next_ret"].dropna().values)
            d["_coin"] = coin
            d["_win"] = w
            parts.append(d)
        if not parts:
            continue
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        coin_means[coin] = float(np.mean(allr)) if len(allr) else np.nan
        cd = pd.concat(parts, ignore_index=True)
        cd["_excess"] = cd["_next_ret"] - coin_means[coin]
        rows.append(cd)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast (forecast > 0)",
                             "value": None, "statistic": None,
                             "threshold": "slope t >= 2 confirms (with weighted mean > 0); t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"down-day cases": 0, "distinct days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    data = pd.concat(rows, ignore_index=True)
    data["_fc"] = pd.to_numeric(data["forecast"], errors="coerce").fillna(0.0)
    data["_date"] = _ts(data["timestamp"]).dt.floor("D")

    # ---------- situation check ----------
    # Situation: a one-day close-to-close fall (raw day_fall value < 0), inside the falling agitated
    # profile (the detector's non-"chop" regime, since the profile components are not recorded); side: long.
    if LHV in data.columns:
        raw = pd.to_numeric(data[LHV], errors="coerce")
    else:
        raw = pd.Series(np.nan, index=data.index)
    raw = raw.where(raw.notna(), data["_day_ret"])
    in_profile = data["regime"].astype(str).str.lower() != "chop"
    situation = (raw < 0) & in_profile
    active = data["_fc"] != 0
    n_active = int(active.sum())
    if n_active > 0:
        agree = float(((situation) & (data["_fc"] > 0) & active).sum() / n_active)
    else:
        agree = None
    passed = bool(agree is not None and agree >= 0.9)

    main_name = "OLS slope of next-day excess return on forecast, bars with forecast > 0"
    threshold = "slope t (clustered by day) >= 2 and weighted mean > 0 confirms; t <= -2 rejects; else inconclusive"
    reading = ("Profile bars are read from the recorded regime (not 'chop'), the raw one-day return from "
               "last_history_value (else recomputed from closes); the clustered standard error uses the usual "
               "small-sample factor G/(G-1)*(N-1)/(N-K) with an intercept in the regression; the plan's minimum "
               "counts (100 cases, 50 distinct days) are applied as 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are down days inside the falling agitated profile "
                           "with a long forecast, so the config does not do what the Fidelity says."
                           if agree is not None else "No active bars: the config never takes the plan's position."),
            "reading": reading,
        }

    # ---------- main measure ----------
    s = data[(data["_fc"] > 0) & data["_excess"].notna()].copy()
    n = int(len(s))
    n_days = int(s["_date"].nunique()) if n else 0
    counts = {"down-day cases": n, "distinct days": n_days}

    slope = None
    tstat = None
    wmean = None
    if n >= 3 and s["_fc"].std() > 0:
        x = s["_fc"].values.astype(float)
        y = s["_excess"].values.astype(float)
        X = np.column_stack([np.ones(n), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        k = X.shape[1]
        meat = np.zeros((k, k))
        groups = s["_date"].values
        G = 0
        for g in pd.unique(groups):
            m = groups == g
            sg = X[m].T @ u[m]
            meat += np.outer(sg, sg)
            G += 1
        if G > 1 and n > k:
            corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tstat = float(beta[1] / se) if np.isfinite(se) and se > 0 else None
        else:
            slope = float(beta[1])
    if n > 0 and s["_fc"].sum() > 0:
        wmean = float((s["_excess"] * s["_fc"]).sum() / s["_fc"].sum())
    check_pass = None if wmean is None else bool(wmean > 0)

    main = {"name": main_name, "value": slope,
            "statistic": None if tstat is None else {"name": "slope t, SE clustered by day", "value": tstat},
            "threshold": threshold}
    support = {"name": "forecast-weighted mean next-day excess return > 0", "value": wmean, "passed": check_pass}

    if n < 100 or n_days < 50:
        status = "not observable"
        decided = (f"Minimum count not reached: {n} down-day cases (need 100) on {n_days} distinct days (need 50).")
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it meets neither the confirm nor the reject rule."
    elif tstat >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the weighted mean excess return is not above 0 (check failed)."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
