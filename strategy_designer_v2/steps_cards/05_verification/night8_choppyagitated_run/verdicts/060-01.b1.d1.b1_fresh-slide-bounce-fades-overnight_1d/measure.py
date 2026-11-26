import numpy as np
import pandas as pd


def measure(bars):
    RISE = "debug_info.components.rise.last_history_value"
    FALL = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    rows = []  # (coin, day, forecast, next_ret)
    coin_mean = {}

    for coin, wins in bars.items():
        all_rets = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            per_win.append((d, nxt))

            fc = d["forecast"].astype(float)
            # raw values, recomputed from prices where not recorded
            rise_raw = d[RISE].astype(float) if RISE in d.columns else pd.Series(np.nan, index=d.index)
            fall_raw = d[FALL].astype(float) if FALL in d.columns else pd.Series(np.nan, index=d.index)
            rise_px = close / close.shift(1) - 1.0
            fall_px = close.shift(1) / close.shift(6) - 1.0
            rise_v = rise_raw.where(rise_raw.notna(), rise_px)
            fall_v = fall_raw.where(fall_raw.notna(), fall_px)

            active = fc.notna() & (fc != 0)
            situ = (fall_v < 0) & (rise_v > 0)
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

        if all_rets:
            allr = np.concatenate(all_rets)
            coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan
        else:
            coin_mean[coin] = np.nan

        for d, nxt in per_win:
            fc = d["forecast"].astype(float)
            mask = (fc < 0) & nxt.notna()
            for i in np.where(mask.values)[0]:
                rows.append((coin, d["timestamp"].iloc[i].floor("D"),
                             float(fc.iloc[i]), float(nxt.iloc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of next-day excess return on -forecast (short bars)"
    thr = "confirm: slope < 0 with day-clustered t <= -2 and check passes; reject: slope > 0 with t >= 2"
    reading = ("Situation taken as the raw 5-day lag-1 scaled return < 0 and today's raw 1-day scaled return > 0 "
               "(recomputed from prices if not recorded) with a negative forecast, the profile not rechecked since its "
               "components are not recorded and need more history than a window; the excess return removes the coin's "
               "mean 1-bar return over all its windows; t is an OLS slope t with standard errors clustered by UTC day; "
               "active bars are bars with forecast < 0 and a next-day return in the same window; the plan's minimum "
               "counts, when not reached, give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on which the 5-day fall "
                           "ending yesterday and today's rise both hold, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    if rows:
        R = pd.DataFrame(rows, columns=["coin", "day", "fc", "ret"])
        R["cm"] = R["coin"].map(coin_mean)
        R = R.dropna(subset=["fc", "ret", "cm"])
    else:
        R = pd.DataFrame(columns=["coin", "day", "fc", "ret", "cm"])

    n_bars = int(len(R))
    n_days = int(R["day"].nunique()) if n_bars else 0
    counts = {"active bars": n_bars, "distinct days": n_days}

    if n_bars < 100 or n_days < 50:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "mean next-day excess return, short-signed, > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": ("The plan's minimum of 100 active bars over at least 50 distinct days is not reached "
                           f"({n_bars} bars, {n_days} days)."),
            "reading": reading,
        }

    y = (R["ret"] - R["cm"]).values.astype(float)
    x = (-R["fc"]).values.astype(float)
    X = np.column_stack([np.ones_like(x), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    e = y - X @ beta
    groups = R["day"].values
    meat = np.zeros((2, 2))
    for g in pd.unique(groups):
        m = groups == g
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    G = len(pd.unique(groups))
    N, K = X.shape
    corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if G > 1 and N > K else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    slope = float(beta[1])
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    t = float(slope / se) if se and np.isfinite(se) and se > 0 else float("nan")

    short_excess = float(np.mean(-y))
    check_pass = bool(short_excess > 0)

    if np.isfinite(t) and slope < 0 and t <= -2 and check_pass:
        status = "confirmed"
        decided = "Confirm: the slope is below 0 with t <= -2 and the shorts' mean next-day excess return is above 0."
    elif np.isfinite(t) and slope > 0 and t >= 2:
        status = "rejected"
        decided = "Reject: the slope is above 0 with t >= 2, the next-day return rises with the size of the short."
    elif np.isfinite(t) and slope < 0 and t <= -2:
        status = "inconclusive"
        decided = "Inconclusive: a confirming slope (t <= -2) but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t, day-clustered", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "mean next-day excess return, short-signed, > 0",
                             "value": short_excess, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
