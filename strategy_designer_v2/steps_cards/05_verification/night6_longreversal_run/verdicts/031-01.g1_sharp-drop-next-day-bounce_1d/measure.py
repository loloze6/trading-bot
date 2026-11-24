import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall_in_usual_moves.last_history_value"

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- collect rows, coin means ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            # raw value: recorded, else recomputed from prices (within window)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            r1 = close / close.shift(1) - 1.0
            vol = r1.rolling(30, min_periods=30).std()
            recomputed = r1 / vol
            raw = raw.where(raw.notna(), recomputed)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            day = to_ts(d["timestamp"]).dt.floor("D")
            frames.append(pd.DataFrame({
                "coin": coin, "window": w, "day": day.values,
                "forecast": f.values, "raw": raw.values, "nxt": nxt.values,
            }))
        if all_rets:
            cat = np.concatenate(all_rets)
            coin_means[coin] = float(np.mean(cat)) if len(cat) else np.nan
        rows.extend(frames)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-bar excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with day-clustered t >= 2"},
            "supporting_check": None, "counts": {"bars with forecast > 0": 0, "distinct days": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }
    data = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = data[data["forecast"].notna() & (data["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = (active["raw"] < 0) & (active["forecast"] > 0)
        agreement = float(ok.sum()) / n_active
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of next-bar excess return on forecast (forecast > 0 bars)"
    main_thr = "slope > 0 with day-clustered t >= 2 confirms (with check); slope < 0 with t <= -2 rejects"
    sup_name = "forecast-weighted mean next-bar excess return, day-clustered t"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are down days (raw "
                           "vol-scaled return < 0) with a long forecast, as the Fidelity's situation and side require."),
            "reading": "The situation is read as the component's raw value (one-day return over 30-day volatility) below 0, the side as long (forecast > 0).",
        }

    # ---------- main measure ----------
    data["mu"] = data["coin"].map(coin_means)
    s = data[(data["forecast"] > 0) & data["nxt"].notna() & data["mu"].notna()].copy()
    s["ex"] = s["nxt"] - s["mu"]
    n = len(s)
    n_days = int(s["day"].nunique())
    counts = {"bars with forecast > 0": int(n), "distinct days": n_days}

    reading = ("Every bar with forecast > 0 and a next bar in the same window is used; the coin's mean is the mean "
               "next-bar return over all its windows; clustered standard errors use the CR1 sandwich with the "
               "G/(G-1)*(N-1)/(N-K) correction; the plan's 'fewer is inconclusive' minimum is reported as "
               "'not observable' as the workflow requires.")

    if n < 300 or n_days < 200:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 300 bars with forecast > 0 over at least 200 distinct days is not reached.",
            "reading": reading,
        }

    x = s["forecast"].values.astype(float)
    y = s["ex"].values.astype(float)
    g = s["day"].values
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    resid = y - X @ beta
    sc = pd.DataFrame(X * resid[:, None]).groupby(g).sum().values
    G = sc.shape[0]
    meat = sc.T @ sc
    K = 2
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - K)) if G > 1 else np.nan
    V = corr * XtX_inv @ meat @ XtX_inv
    slope = float(beta[1])
    se_slope = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    t_slope = slope / se_slope if se_slope and np.isfinite(se_slope) else np.nan

    # ---------- supporting check ----------
    wsum = x.sum()
    wmean = float((x * y).sum() / wsum)
    u = x * (y - wmean) / wsum
    us = pd.Series(u).groupby(g).sum().values
    var_w = (G / (G - 1.0)) * float((us ** 2).sum()) if G > 1 else np.nan
    se_w = np.sqrt(var_w) if var_w and var_w > 0 else np.nan
    t_w = wmean / se_w if np.isfinite(se_w) else np.nan
    sup_pass = bool(wmean > 0 and np.isfinite(t_w) and t_w >= 2)

    # ---------- decision ----------
    slope_reject = bool(slope < 0 and np.isfinite(t_slope) and t_slope <= -2)
    w_reject = bool(wmean < 0 and np.isfinite(t_w) and t_w <= -2)
    slope_confirm = bool(slope > 0 and np.isfinite(t_slope) and t_slope >= 2)

    if slope_reject or w_reject:
        status = "rejected"
        if slope_reject:
            decided = "Reject: the slope is negative with day-clustered t <= -2."
        else:
            decided = "Reject: the forecast-weighted mean excess return is negative with day-clustered t <= -2."
    elif slope_confirm and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0 with t >= 2."
    else:
        status = "inconclusive"
        if slope_confirm and not sup_pass:
            decided = "Inconclusive: the slope meets the confirm rule but the supporting check fails."
        else:
            decided = "Inconclusive: neither the confirm nor the reject rule is met (t between -2 and 2)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "day-clustered t of slope",
                                       "value": float(t_slope) if np.isfinite(t_slope) else None},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass,
                             "t": float(t_w) if np.isfinite(t_w) else None},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
