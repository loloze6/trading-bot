import numpy as np
import pandas as pd


def measure(bars):
    CL_RAW = "debug_info.components.close_loc.last_history_value"
    CL_PP = "debug_info.components.close_loc.post_pipeline_value"
    OF_PP = "debug_info.components.offset.post_pipeline_value"
    W_CL, W_OF = 1.0, 1.0
    WIN, MINP = 60, 20
    MIN_DAYS = 1000

    def rebuild_std(raw):
        # standardise: raw(t)*10 / mean(|raw| over last WIN values, t excluded), capped +-20
        a = raw.abs().shift(1)
        cnt = a.rolling(WIN, min_periods=1).count()
        m = a.rolling(WIN, min_periods=1).mean()
        x = raw * 10.0 / m
        x = x.where(m != 0, 0.0)
        x = x.clip(-20, 20)
        # only a full in-window history reproduces the engine's value (warm-up bars are not recorded)
        x = x.where(cnt >= WIN)
        return x

    # ---------- per coin: drift over all windows ----------
    rows = []
    check_rows = []
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            r = d["close"].shift(-1) / d["close"] - 1.0
            rets_all.append(r.dropna())
        drift = pd.concat(rets_all).mean() if rets_all else np.nan

        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            # situation: close location (high-close)/(high-low), standardised, against its usual size (+10)
            if CL_RAW in d.columns:
                raw = pd.to_numeric(d[CL_RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            rng = d["high"] - d["low"]
            raw_px = ((d["high"] - d["close"]) / rng).where(rng > 0, 0.0)
            raw = raw.where(raw.notna(), raw_px)
            x = rebuild_std(raw)
            if CL_PP in d.columns:
                x = x.where(x.notna(), pd.to_numeric(d[CL_PP], errors="coerce"))
            check_rows.append(pd.DataFrame({"forecast": fc, "x": x}))

            # forecast rebuilt from post_pipeline_values
            if CL_PP in d.columns and OF_PP in d.columns:
                f = (W_CL * pd.to_numeric(d[CL_PP], errors="coerce")
                     + W_OF * pd.to_numeric(d[OF_PP], errors="coerce")) / (W_CL + W_OF)
                f = f.clip(-20, 20)
            else:
                f = pd.Series(np.nan, index=d.index)
            nxt = d["close"].shift(-1) / d["close"] - 1.0 - drift
            rows.append(pd.DataFrame({
                "coin": coin, "window": w,
                "day": ts.dt.floor("D"),
                "f": f, "y": nxt,
            }))

    # ---------- situation check ----------
    chk = pd.concat(check_rows, ignore_index=True) if check_rows else pd.DataFrame(columns=["forecast", "x"])
    act = chk[(chk["forecast"].notna()) & (chk["forecast"] != 0)]
    n_act = len(act)
    if n_act > 0:
        expected = np.sign(act["x"] - 10.0)
        agree = (np.sign(act["forecast"]) == expected) & act["x"].notna()
        agreement = float(agree.mean())
    else:
        agreement = 0.0
    passed = bool(n_act > 0 and agreement >= 0.90)

    reading = ("The situation is the standardised close location above (long) or below (short) its usual size of +10, "
               "rebuilt from last_history_value with a full 60-bar in-window history and otherwise read from "
               "post_pipeline_value; the horizon of 1 bar uses every bar; quintiles are pooled over all coins and "
               "windows by forecast rank; the 1000-day count is the distinct UTC days in the slope's sample; the "
               "slope has an intercept and cluster-robust (CR1) day-clustered errors.")

    main_name = "pooled OLS slope of drift-removed next-day return on forecast"
    thr = "slope t >= 2 confirms (with top-minus-bottom > 0), t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_act)},
            "decided_by": ("The plan's situation (long when the close sits nearer the low than usual, short when "
                           "nearer the high) agrees with the forecast's sign on fewer than 90% of active bars."),
            "reading": reading,
        }

    data = pd.concat(rows, ignore_index=True)
    data = data.dropna(subset=["f", "y", "day"])
    n_obs = int(len(data))
    n_days = int(data["day"].nunique())

    counts = {"distinct days with recorded forecasts": n_days, "observations": n_obs}

    if n_days < MIN_DAYS:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Fewer than {MIN_DAYS} distinct days with recorded forecasts across the coins.",
            "reading": reading,
        }

    # ---------- pooled OLS with day-clustered SE ----------
    X = np.column_stack([np.ones(n_obs), data["f"].to_numpy(float)])
    y = data["y"].to_numpy(float)
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    u = y - X @ beta
    groups = pd.factorize(data["day"])[0]
    G = int(groups.max()) + 1
    S = np.zeros((G, 2))
    np.add.at(S, groups, X * u[:, None])
    meat = S.T @ S
    K = 2
    corr = (G / (G - 1.0)) * ((n_obs - 1.0) / (n_obs - K)) if G > 1 and n_obs > K else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    slope = float(beta[1])
    t = float(slope / se) if se and np.isfinite(se) and se > 0 else float("nan")

    # ---------- supporting: top minus bottom quintile ----------
    rk = data["f"].rank(method="first")
    q = pd.qcut(rk, 5, labels=False)
    top = data.loc[q == 4, "y"].mean()
    bot = data.loc[q == 0, "y"].mean()
    diff = float(top - bot)
    sup_pass = bool(np.isfinite(diff) and diff > 0)
    counts["top quintile observations"] = int((q == 4).sum())
    counts["bottom quintile observations"] = int((q == 0).sum())

    if np.isfinite(t) and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom quintile difference is above 0."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom quintile difference is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": {"name": "t, day-clustered SE", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "top minus bottom forecast quintile drift-removed next-day return",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
