import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RV = "debug_info.components.rise_vol_units.last_history_value"
    RN = "debug_info.components.rise_near_high.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            # one-day return inside the window
            ret1 = np.full(len(df), np.nan)
            ret1[1:] = close[1:] / close[:-1] - 1.0
            # raw component value (day return / 30-day sd); fall back to price return
            if RV in df.columns:
                raw = pd.to_numeric(df[RV], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            if RN in df.columns:
                raw2 = pd.to_numeric(df[RN], errors="coerce").values
            else:
                raw2 = np.full(len(df), np.nan)
            rise_val = np.where(np.isfinite(raw), raw, np.where(np.isfinite(raw2), raw2, ret1))
            rise = np.where(np.isfinite(rise_val), rise_val > 0, False)
            # choppy-calm profile: the detector's vetoes send every other bar to "chop";
            # the profile is the regime that is not vetoed ("unknown")
            if "regime" in df.columns:
                calm = (df["regime"].astype(str).values == "unknown")
            else:
                calm = np.ones(len(df), dtype=bool)
            active = fc != 0
            situation = rise & calm
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None) and (agreement >= 0.9)

    main_name = "pooled slope of coin-excess 5-bar forward return on forecast, grid bars with forecast > 0"
    thr = "slope > 0 with t >= 2 confirms (with mean excess > 0); slope < 0 with t <= -2 rejects"
    reading = ("The situation is a rise day (raw rise_vol_units > 0, or the 1-day close return when not recorded) on a bar "
               "of the choppy-calm profile (regime 'unknown', the only non-vetoed regime), long side; the coin's mean "
               "5-bar return is the mean of its non-overlapping grid 5-bar returns over all windows; the regression "
               "has an intercept and cluster-robust (by UTC date) errors with the usual small-sample correction; the "
               "plan's minimum of 40 grid bars over 20 dates, if not reached, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars on a rise day inside "
                           "the choppy-calm profile, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                rows.append((coin, r, fc[t], ts.iloc[t]))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    d = pd.DataFrame(rows, columns=["coin", "ret", "fc", "ts"])
    if len(d):
        d["excess"] = d["ret"] - d["coin"].map(coin_rets)
        d = d[(d["fc"] > 0) & np.isfinite(d["excess"]) & np.isfinite(d["fc"]) & d["ts"].notna()].copy()
        d["date"] = d["ts"].dt.floor("D")
    n_cases = int(len(d))
    n_dates = int(d["date"].nunique()) if n_cases else 0
    counts = {"grid bars with forecast > 0": n_cases, "distinct dates": n_dates}

    slope = None
    tval = None
    mean_ex = float(d["excess"].mean()) if n_cases else None
    if n_cases >= 3 and n_dates >= 2:
        X = np.column_stack([np.ones(n_cases), d["fc"].values.astype(float)])
        y = d["excess"].values.astype(float)
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("date").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_dates
        N, K = n_cases, 2
        corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if N > K else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_pass = (mean_ex > 0) if mean_ex is not None and np.isfinite(mean_ex) else None
    supporting = {"name": "mean excess 5-bar return on the same grid bars > 0",
                  "value": mean_ex, "passed": sup_pass}
    stat = {"name": "slope t, errors clustered by date", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": thr}

    if n_cases < 40 or n_dates < 20:
        status = "not observable"
        decided = ("The plan's minimum of 40 grid bars with forecast > 0 spread over at least 20 distinct dates is "
                   "not reached (%d bars, %d dates)." % (n_cases, n_dates))
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean excess 5-bar return is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the mean excess 5-bar return is at or below 0 (inconclusive rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
