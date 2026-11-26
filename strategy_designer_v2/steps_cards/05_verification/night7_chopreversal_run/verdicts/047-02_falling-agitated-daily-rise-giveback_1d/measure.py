import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.day_rise_fade.last_history_value"
    PPV = "debug_info.components.day_rise_fade.post_pipeline_value"
    PROFILE_REGIME = "unknown"  # the regime the detector keeps when neither veto (-> chop) fires: falling and agitated

    # ---------- collect per-window rows ----------
    frames = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["_next_ret"] = close.shift(-1) / close - 1.0          # inside the window only
            d["_prev_ret"] = close / close.shift(1) - 1.0           # inside the window only
            rets_all.append(d["_next_ret"].dropna().values)
            d["_coin"] = coin
            d["_win"] = wname
            frames.append(d)
        coin_rets[coin] = np.concatenate(rets_all) if rets_all else np.array([])
    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "OLS slope of next-day excess return on forecast", "value": None,
                             "statistic": None, "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases (bars with forecast < 0)": 0, "distinct days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }
    all_df = pd.concat(frames, ignore_index=True)
    coin_mean = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}

    fc = pd.to_numeric(all_df[FC], errors="coerce").fillna(0.0)
    # one-day return: the component's raw value where recorded, else from prices
    if RAW in all_df.columns:
        day_ret = pd.to_numeric(all_df[RAW], errors="coerce")
        day_ret = day_ret.where(day_ret.notna(), all_df["_prev_ret"])
    else:
        day_ret = all_df["_prev_ret"]
    in_profile = all_df["regime"].astype(str) == PROFILE_REGIME

    # ---------- situation check ----------
    active = fc != 0
    n_active = int(active.sum())
    situation = in_profile & (day_ret > 0)
    agree = active & situation & (fc < 0)
    agreement = float(agree.sum() / n_active) if n_active > 0 else None
    passed = (agreement is not None) and (agreement >= 0.9)

    mm_name = "OLS slope of next-day excess return on forecast (post_pipeline_value), day-clustered SE"
    thr = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    reading = ("The profile is read from the recorded regime ('unknown' = neither chop veto fired), the one-day rise "
               "from last_history_value (prices where missing); cases are bars with forecast < 0 that have a next bar "
               "in the same window; the regression has an intercept with CR1 day-clustered standard errors "
               "(G/(G-1)*(N-1)/(N-K)); the plan's 'fewer than 100 cases or 50 days' is treated as 'not observable' "
               "per the workflow's minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of non-zero forecast bars are short bars on an up day inside the falling "
                           "agitated profile (regime 'unknown'), as the Fidelity requires."
                           if n_active > 0 else "The forecast is never non-zero, so no bar acts on the plan's situation."),
            "reading": reading,
        }

    # ---------- main measure ----------
    x_all = pd.to_numeric(all_df[PPV], errors="coerce") if PPV in all_df.columns else fc.copy()
    x_all = x_all.where(x_all.notna(), fc)
    y_all = all_df["_next_ret"] - all_df["_coin"].map(coin_mean)
    days = pd.to_datetime(all_df["timestamp"], utc=True).dt.floor("D").astype(str)

    sel = (fc < 0) & x_all.notna() & y_all.notna()
    x = x_all[sel].values.astype(float)
    y = y_all[sel].values.astype(float)
    g = days[sel].values
    n_cases = int(len(x))
    n_days = int(len(np.unique(g))) if n_cases else 0
    counts = {"cases (bars with forecast < 0)": n_cases, "distinct days": n_days}

    slope = None
    tstat = None
    if n_cases >= 3 and np.var(x) > 0:
        X = np.column_stack([np.ones(n_cases), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        dfu = pd.DataFrame({"g": g, "a": X[:, 0] * u, "b": X[:, 1] * u})
        sums = dfu.groupby("g")[["a", "b"]].sum().values
        for s in sums:
            meat += np.outer(s, s)
        G = sums.shape[0]
        K = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if G > 1 and n_cases > K else np.nan
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if np.isfinite(V[1, 1]) and V[1, 1] > 0 else np.nan
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None
    elif n_cases >= 1:
        slope = None

    mean_short = float(-np.mean(y)) if n_cases > 0 else None
    sup_passed = (mean_short is not None) and (mean_short > 0)

    main = {"name": mm_name, "value": slope,
            "statistic": ({"name": "day-clustered t of slope", "value": tstat} if tstat is not None else None),
            "threshold": thr}
    sup = {"name": "mean next-day excess return, short direction (negated), > 0",
           "value": mean_short, "passed": bool(sup_passed) if mean_short is not None else None}

    # ---------- decision ----------
    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 100) over {n_days} distinct days (need 50).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Confirm rule: slope > 0 with t >= 2, and the short-direction mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: slope > 0 with t >= 2 but the supporting check fails."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "Reject rule: slope < 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
