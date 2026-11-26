import numpy as np
import pandas as pd


def _cluster_ols(y, X, groups):
    """OLS with an intercept and standard errors clustered by group (CR1)."""
    y = np.asarray(y, dtype=float)
    X = np.column_stack([np.ones(len(y)), np.asarray(X, dtype=float)])
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    u = y - X @ beta
    g = pd.Series(groups).astype(str).values
    uniq = pd.unique(g)
    G = len(uniq)
    meat = np.zeros((k, k))
    idx = pd.Series(np.arange(n)).groupby(g).indices
    for key in uniq:
        ii = idx[key]
        s = X[ii].T @ u[ii]
        meat += np.outer(s, s)
    if G > 1 and n > k:
        c = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    else:
        c = 1.0
    V = c * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    t = np.where(se > 0, beta / np.where(se > 0, se, 1.0), np.nan)
    return beta, se, t, G


def measure(bars):
    RAW = "debug_info.components.slide_depth.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            close = d["close"].astype(float)
            d["r_next"] = close.shift(-1) / close - 1.0
            d["r_last"] = close / close.shift(1) - 1.0
            d["slide_px"] = close.shift(1) / close.shift(5) - 1.0
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["fc"] = fc
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # slide: four days before the latest day fell (raw value negative; prices where raw missing)
            slide = np.where(raw.notna(), raw < 0, d["slide_px"] < 0)
            profile = d["regime"].astype(str).str.lower() == "unknown"
            situ = profile.values & slide.astype(bool)
            active = fc.values != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc.values > 0)).sum())
            coin_rets.append(d["r_next"].dropna().values)
            d["coin"] = coin
            d["day"] = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D").astype(str)
            frames.append(d[["coin", "day", "fc", "r_next", "r_last"]])
        if not frames:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if len(allr) else np.nan
        cdf = pd.concat(frames, ignore_index=True)
        cdf["excess"] = cdf["r_next"] - mu
        rows.append(cdf)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    situation = {"agreement": float(agreement), "passed": passed}

    main_name = "pooled slope of next-day excess return on forecast (forecast > 0)"
    main_thr = "confirm: slope > 0 with day-clustered t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    supp_name = "forecast slope with latest day's return added, day-clustered t"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are long bars in the falling agitated profile after a 4-day prior slide, so the config does not do what the Fidelity says.",
            "reading": "The situation is regime 'unknown' (the falling agitated profile left by the vetoes) with a negative raw slide value (prices close[t-1]/close[t-5]-1 where raw is missing), on the long side.",
        }

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["coin", "day", "fc", "r_next", "r_last", "excess"])
    sel = data[(data["fc"] > 0) & data["excess"].notna()]
    n_bars = int(len(sel))
    n_days = int(sel["day"].nunique())
    counts = {"bars with forecast > 0": n_bars, "distinct days": n_days}
    reading = ("The profile is the recorded regime 'unknown', the slide the raw component's sign; excess return uses each coin's mean next-day return over all its bars in all windows; "
               "SEs are CR1 clustered by UTC day; the supporting regression drops each window's first bar (no latest-day return); the plan's minimum of 100 bars and 50 days is applied as a minimum count.")

    if n_bars < 100 or n_days < 50:
        return {
            "status": "not observable",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 100 bars with forecast > 0 or fewer than 50 distinct days, the plan's minimum counts.",
            "reading": reading,
        }

    b, se, t, G = _cluster_ols(sel["excess"].values, sel[["fc"]].values, sel["day"].values)
    slope, tmain = float(b[1]), float(t[1])

    s2 = sel[sel["r_last"].notna()]
    supp_val, supp_t, supp_pass = None, None, None
    if len(s2) > 3:
        b2, se2, t2, _ = _cluster_ols(s2["excess"].values, s2[["fc", "r_last"]].values, s2["day"].values)
        supp_val, supp_t = float(b2[1]), float(t2[1])
        supp_pass = bool(np.isfinite(supp_t) and supp_val > 0 and supp_t >= 2)
    else:
        supp_pass = False

    if np.isfinite(tmain) and slope > 0 and tmain >= 2 and supp_pass:
        status = "confirmed"
        decided = "The main slope is positive with t >= 2 and the forecast's slope stays positive with t >= 2 with the latest day's return added."
    elif np.isfinite(tmain) and slope < 0 and tmain <= -2:
        status = "rejected"
        decided = "The main slope is negative with t <= -2."
    elif np.isfinite(tmain) and slope > 0 and tmain >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the supporting check failed."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "day-clustered t", "value": tmain},
                         "threshold": main_thr},
        "supporting_check": {"name": supp_name, "value": supp_t, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
