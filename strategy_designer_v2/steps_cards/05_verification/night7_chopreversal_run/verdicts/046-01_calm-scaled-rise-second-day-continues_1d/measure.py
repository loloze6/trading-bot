import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.lagged_scaled_rise.last_history_value"
    POST = "debug_info.components.lagged_scaled_rise.post_pipeline_value"
    MIN_BARS = 100
    MIN_DAYS = 60

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): a calm market (the profile: the regime detector leaves "unknown",
    # i.e. not vetoed to "chop") and a positive lagged volatility-scaled one-day return (a rise),
    # side expected: long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = _num(df, "forecast")
            raw = _num(df, RAW)
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            active = fc.notna() & (fc != 0)
            situ = (reg == "unknown") & raw.notna() & (raw > 0)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "clustered-by-day t of the slope of excess next-bar return on the forecast, forecast > 0 bars"
    threshold = "confirm if t >= 2 and forecast-weighted mean excess return > 0; reject if t <= -2"
    reading = ("Calm is read from the recorded regime ('unknown', i.e. not vetoed to 'chop') and the rise from "
               "last_history_value > 0; the slope's t uses an OLS with intercept and standard errors clustered by UTC "
               "calendar day (scores summed per day, small-sample corrected); the coin's mean daily return is the mean "
               "of all its within-window one-bar returns; the minimum counts are on bars with a forecast above 0 and a "
               "next-bar return inside the window, and a shortfall is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the calm rise situation, long": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are calm-market bars after a positive "
                           "scaled one-day rise with a long forecast, so the config does not do what the Fidelity says."
                           if n_active > 0 else "The record has no active bars, so the situation cannot be matched."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        parts = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            close = _num(d, "close")
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            coin_rets.append(nxt.dropna().values)
            parts.append(pd.DataFrame({
                "ts": pd.to_datetime(d["timestamp"], utc=True),
                "fc": _num(d, "forecast").values,
                "x": _num(d, POST).values,
                "r": nxt.values,
            }))
        if not parts:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if len(allr) else np.nan
        p = pd.concat(parts, ignore_index=True)
        p["y"] = p["r"] - mu
        p["coin"] = coin
        rows.append(p)

    if rows:
        data = pd.concat(rows, ignore_index=True)
        data = data[(data["fc"] > 0)]
        data = data.dropna(subset=["x", "y", "ts"])
    else:
        data = pd.DataFrame(columns=["ts", "fc", "x", "r", "y", "coin"])

    n = int(len(data))
    days = data["ts"].dt.floor("D") if n else pd.Series([], dtype="datetime64[ns, UTC]")
    n_days = int(days.nunique()) if n else 0
    counts = {"bars with a forecast above 0": n, "distinct days": n_days}

    if n < MIN_BARS or n_days < MIN_DAYS:
        missing = []
        if n < MIN_BARS:
            missing.append(f"{n} bars with a forecast above 0 (minimum 100)")
        if n_days < MIN_DAYS:
            missing.append(f"{n_days} distinct days (minimum 60)")
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "forecast-weighted mean excess next-bar return > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum count is not reached: " + "; ".join(missing) + ".",
            "reading": reading,
        }

    x = data["x"].values.astype(float)
    y = data["y"].values.astype(float)
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        XtX_inv = None

    slope = None
    t_slope = None
    if XtX_inv is not None:
        beta = XtX_inv @ (X.T @ y)
        e = y - X @ beta
        scores = pd.DataFrame(X * e[:, None], columns=["a", "b"])
        scores["day"] = days.values
        S = scores.groupby("day")[["a", "b"]].sum().values
        G = S.shape[0]
        meat = S.T @ S
        k = 2
        corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if G > 1 and n > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if se and np.isfinite(se) and se > 0 else None

    wsum = float(np.sum(x))
    wmean = float(np.sum(y * x) / wsum) if wsum > 0 else None
    sup_pass = bool(wmean is not None and wmean > 0)

    if t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Reject: the slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t is 2 or more but the forecast-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "slope t, day-clustered", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": "forecast-weighted mean excess next-bar return > 0", "value": wmean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
