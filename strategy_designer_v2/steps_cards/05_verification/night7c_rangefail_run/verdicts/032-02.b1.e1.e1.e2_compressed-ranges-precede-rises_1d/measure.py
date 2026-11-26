import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    C_RAW = "debug_info.components.compression.last_history_value"
    C_PP = "debug_info.components.compression.post_pipeline_value"
    O_RAW = "debug_info.components.offset.last_history_value"
    O_PP = "debug_info.components.offset.post_pipeline_value"

    def standardise(raw, pp, negate=False):
        # value(t) * 10 / mean(|last 61 raw values|, t left out), capped at +-20.
        # Only rebuilt where a full 61 past in-window raw values exist;
        # before that the engine's earlier history is not in the record, so the
        # recorded post_pipeline_value is used instead.
        raw = pd.to_numeric(raw, errors="coerce")
        denom = raw.abs().shift(1).rolling(61, min_periods=61).mean()
        val = raw * 10.0 / denom
        val = val.where(denom != 0, 0.0).clip(-20, 20)
        if negate:
            val = -val
        pp = pd.to_numeric(pp, errors="coerce") if pp is not None else pd.Series(np.nan, index=raw.index)
        out = val.where(denom.notna(), pp)
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if C_RAW in df.columns:
                c = standardise(df[C_RAW], df[C_PP] if C_PP in df.columns else None)
            elif C_PP in df.columns:
                c = pd.to_numeric(df[C_PP], errors="coerce")
            else:
                c = pd.Series(np.nan, index=df.index)
            if O_RAW in df.columns:
                o = standardise(df[O_RAW], df[O_PP] if O_PP in df.columns else None, negate=True)
            elif O_PP in df.columns:
                o = pd.to_numeric(df[O_PP], errors="coerce")
            else:
                o = pd.Series(-10.0, index=df.index)
            rebuilt = ((c + o) / 2.0).clip(-20, 20)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            exp_sign = np.sign(rebuilt)
            agree = active & rebuilt.notna() & (exp_sign != 0) & (np.sign(fc) == exp_sign)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of 20-bar excess return on forecast (date-clustered SE)"
    thr = "confirm: slope > 0 with t >= 2 and top-minus-bottom > 0; reject: slope < 0 with t <= -2"
    reading = ("Situation is every bar with the long side when the standardised compression exceeds its usual level "
               "(expected sign = sign of the rebuilt (compression + offset)/2, standardise rebuilt from "
               "last_history_value where 61 past in-window values exist, else the recorded post_pipeline_value); "
               "grid at positions 0,20,40,... of each window with the 20-bar return inside the window, coin mean = mean "
               "of that coin's grid returns over all windows, OLS with intercept and CR1 date-clustered SE, top/bottom "
               "fifth = forecast >= 80th / <= 20th percentile of pooled grid cases, and fewer than 300 cases or 100 dates "
               "gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The forecast's sign agrees with the plan's situation (long when the 60-day range is tighter "
                           "than usual, short when wider) on only %.1f%% of active bars, below 90%%." % (100 * agreement)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                rows.append({"coin": coin, "ret": c1 / c0 - 1.0, "f": fc[i],
                             "date": ts.iloc[i].strftime("%Y-%m-%d")})
    g = pd.DataFrame(rows, columns=["coin", "ret", "f", "date"])
    if len(g):
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
        g = g.dropna(subset=["excess", "f"])
    n_cases = int(len(g))
    n_dates = int(g["date"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct dates": n_dates}

    if n_cases < 300 or n_dates < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 300 grid cases on at least 100 distinct dates is not reached "
                          "(%d cases, %d dates)." % (n_cases, n_dates),
            "reading": reading,
        }

    y = g["excess"].values.astype(float)
    X = np.column_stack([np.ones(n_cases), g["f"].values.astype(float)])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    meat = np.zeros((2, 2))
    for _, idx in g.reset_index(drop=True).groupby("date").indices.items():
        s = X[idx].T @ u[idx]
        meat += np.outer(s, s)
    G = n_dates
    K = 2
    corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if G > 1 else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    slope = float(beta[1])
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    t = float(slope / se) if np.isfinite(se) and se > 0 else 0.0

    q80 = g["f"].quantile(0.8)
    q20 = g["f"].quantile(0.2)
    top = g.loc[g["f"] >= q80, "excess"]
    bot = g.loc[g["f"] <= q20, "excess"]
    if len(top) and len(bot):
        diff = float(top.mean() - bot.mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None
    counts["top fifth cases"] = int(len(top))
    counts["bottom fifth cases"] = int(len(bot))

    if slope > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Confirm: the slope is positive with t >= 2 and the top-minus-bottom difference is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: the slope is positive with t >= 2 but the top-minus-bottom difference is not above 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope has |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "date-clustered t of slope", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "mean excess 20-bar return, top fifth minus bottom fifth of forecast",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
