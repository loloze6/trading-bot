import numpy as np
import pandas as pd


def _cluster_ols(y, X, groups):
    """OLS with cluster-robust (CR1) standard errors, clusters = groups."""
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    resid = y - X @ beta
    g = pd.Series(groups).reset_index(drop=True)
    codes, uniq = pd.factorize(g)
    G = len(uniq)
    meat = np.zeros((k, k))
    scores = X * resid[:, None]
    S = np.zeros((G, k))
    np.add.at(S, codes, scores)
    meat = S.T @ S
    if G > 1 and n > k:
        c = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    else:
        c = 1.0
    V = c * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(se > 0, beta / se, np.nan)
    return beta, se, t, G


def measure(bars):
    RAW = "debug_info.components.scaled_rise.last_history_value"

    active_total = 0
    active_agree = 0
    case_rows = []

    # coin mean daily return over all windows
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = c.shift(-1) / c - 1.0
            rets.append(r.dropna())
        coin_mean[coin] = float(pd.concat(rets).mean()) if rets else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback: sign of the 1-day return from the prices (same sign as the scaled return)
            ret1 = close / close.shift(1) - 1.0
            up = np.where(raw.notna(), raw > 0, ret1 > 0)
            in_profile = (regime == "unknown").values
            situation = in_profile & up

            active = (fc != 0).values
            active_total += int(active.sum())
            active_agree += int((active & situation & (fc < 0).values).sum())

            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            mu = coin_mean.get(coin, np.nan)
            for i in np.where((fc < 0).values)[0]:
                r = nxt.iloc[i]
                if pd.isna(r) or pd.isna(mu) or pd.isna(day.iloc[i]):
                    continue
                case_rows.append((coin, day.iloc[i], abs(float(fc.iloc[i])), -(float(r) - mu)))

    agreement = (active_agree / active_total) if active_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "slope of signal-direction next-day excess return on |forecast|"
    main_thr = "confirm: slope t >= 2 (with mean excess > 0, t >= 2); reject: slope t <= -2 or mean t <= -2"
    sup_name = "mean signal-direction next-day excess return"
    reading = ("Profile bars are those with regime 'unknown' (not vetoed to chop), the situation is a positive raw scaled return "
               "(price return when unrecorded); next-day return is close[t+1]/close[t]-1 inside the window on every case bar, "
               "the coin's mean is over all its 1-day returns in all windows, t's use CR1 cluster-robust errors by UTC day, "
               "and the plan's 'fewer than 100 cases or 50 days' is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars after an up day inside "
                           "the falling agitated profile, as the Fidelity requires."
                           if active_total > 0 else "The record has no active bars to compare with the plan's situation."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "absf", "y"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    slope = slope_t = mean_v = mean_t = None
    if n_cases >= 3 and n_days >= 2:
        X = np.column_stack([np.ones(n_cases), cases["absf"].values])
        if np.ptp(cases["absf"].values) > 0:
            b, se, t, _ = _cluster_ols(cases["y"].values, X, cases["day"].values)
            slope, slope_t = float(b[1]), (float(t[1]) if np.isfinite(t[1]) else None)
        bm, sem, tm, _ = _cluster_ols(cases["y"].values, np.ones((n_cases, 1)), cases["day"].values)
        mean_v, mean_t = float(bm[0]), (float(tm[0]) if np.isfinite(tm[0]) else None)

    sup_pass = None
    if mean_v is not None and mean_t is not None:
        sup_pass = bool(mean_v > 0 and mean_t >= 2)

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "slope t, clustered by day", "value": slope_t} if slope_t is not None else None),
            "threshold": main_thr}
    sup = {"name": sup_name + " (t clustered by day = %s)" % (None if mean_t is None else round(mean_t, 3)),
           "value": mean_v, "passed": sup_pass}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = "Minimum count not reached: %d cases (need 100) on %d distinct days (need 50)." % (n_cases, n_days)
    elif (slope_t is not None and slope_t <= -2) or (mean_t is not None and mean_t <= -2):
        status = "rejected"
        decided = "Reject rule met: the slope's t is -2 or less, or the mean signal-direction excess return has a t of -2 or less."
    elif slope_t is not None and slope_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: the slope's t is 2 or more and the mean signal-direction excess return is above 0 with t of 2 or more."
    else:
        status = "inconclusive"
        decided = "Neither rule met: the slope's t and the mean's t lie between the confirm and reject thresholds (or the slope passes without the mean)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
