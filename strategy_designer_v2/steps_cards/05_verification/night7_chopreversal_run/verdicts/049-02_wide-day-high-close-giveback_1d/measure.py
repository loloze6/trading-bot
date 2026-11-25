import numpy as np
import pandas as pd


def measure(bars):
    W_RAW = "debug_info.components.width.last_history_value"
    B_RAW = "debug_info.components.below_high.last_history_value"

    def rebuild_std(raw):
        # standardise as the engine does: value * 10 / mean(|last 60 raw values|, bar t left out).
        # Warm-up bars are not recorded, so early rows of a window use the past values available
        # (at least 1), and the first row uses the window's mean size.
        a = raw.abs()
        base = a.shift(1).rolling(60, min_periods=1).mean()
        base = base.fillna(a.mean())
        out = raw * 10.0 / base.replace(0, np.nan)
        return out.clip(-20, 20)

    check_rows = []
    reg_rows = []
    for coin, wins in bars.items():
        # the coin's mean daily return over all its windows together
        rets_all = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            rets_all.append((c.shift(-1) / c - 1.0).dropna())
        if len(rets_all) == 0:
            continue
        rets_all = pd.concat(rets_all)
        coin_mean = float(rets_all.mean()) if len(rets_all) else np.nan

        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            fc = d["forecast"].astype(float)
            c = d["close"].astype(float)

            # situation check: graded reading = std(width) - std(distance under the high)
            if W_RAW in d.columns and B_RAW in d.columns:
                wr = d[W_RAW].astype(float)
                dist = d[B_RAW].astype(float).abs()  # the distance is a size
                s = rebuild_std(wr) - rebuild_std(dist)
            else:
                s = pd.Series(np.nan, index=d.index)
            check_rows.append(pd.DataFrame({"f": fc, "s": s}))

            nxt = c.shift(-1) / c - 1.0
            reg_rows.append(pd.DataFrame({
                "coin": coin, "window": w, "day": ts.dt.floor("D"),
                "f": fc, "y": nxt - coin_mean,
            }))

    chk = pd.concat(check_rows, ignore_index=True) if check_rows else pd.DataFrame(columns=["f", "s"])
    active = chk[(chk["f"].notna()) & (chk["f"] != 0)]
    active = active[active["s"].notna()]
    if len(active) > 0:
        agree = float((np.sign(active["f"]) == -np.sign(active["s"])).mean())
    else:
        agree = 0.0
    passed = agree >= 0.90

    main_name = "slope of next-day excess return on forecast (pooled, day-clustered)"
    threshold = "slope > 0 with t >= 2 (confirm); slope < 0 with t <= -2 (reject)"
    reading = ("Situation read as standardised width minus standardised distance under the high (rebuilt from raw values, "
               "short when positive); regression uses all bars with a next close in the window with an intercept and CR1 "
               "day-clustered errors; fifths of |forecast| are taken over those same bars (top fifth >= 80th percentile, "
               "bottom two fifths <= 40th percentile); a 'distinct day with a forecast' is a UTC day with a non-zero "
               "forecast on any coin among those bars.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(len(active))},
            "decided_by": ("Fewer than 90% of active bars have the forecast's sign opposite to the plan's graded reading "
                           "(width minus distance under the high): the config does not short high closes on wide days."),
            "reading": reading,
        }

    reg = pd.concat(reg_rows, ignore_index=True)
    reg = reg.dropna(subset=["f", "y", "day"]).reset_index(drop=True)
    n_days = int(reg.loc[reg["f"] != 0, "day"].nunique())

    slope = t = None
    if len(reg) > 2 and reg["f"].var() > 0:
        X = np.column_stack([np.ones(len(reg)), reg["f"].values])
        yv = reg["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ yv
        u = yv - X @ beta
        scores = pd.DataFrame(X * u[:, None], columns=["a", "b"])
        scores["g"] = reg["day"].values
        S = scores.groupby("g")[["a", "b"]].sum().values
        G = S.shape[0]
        N, K = X.shape
        meat = S.T @ S
        cfac = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if G > 1 else np.nan
        V = cfac * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t = float(slope / se) if se and np.isfinite(se) else None

    # supporting check
    af = reg["f"].abs()
    sup_val = None
    sup_pass = None
    if len(reg) > 0:
        q80 = af.quantile(0.8)
        q40 = af.quantile(0.4)
        lean = np.sign(reg["f"]) * reg["y"]
        top = lean[af >= q80]
        bot = lean[af <= q40]
        if len(top) > 0 and len(bot) > 0:
            sup_val = float(top.mean() - bot.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"distinct days with a forecast": n_days, "bars in regression": int(len(reg))}

    if n_days < 1000:
        status = "not observable"
        decided = f"Only {n_days} distinct days with a forecast, below the plan's minimum of 1,000."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Slope positive with t >= 2 and the top-fifth lean exceeds the bottom-two-fifths lean."
        else:
            status = "inconclusive"
            decided = "Slope positive with t >= 2 but the supporting check fails: a confirming slope with a failed check."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Slope negative with t <= -2: continuation in the direction of the wide day's close."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "day-clustered t", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean sign(forecast) x excess return, top fifth of |forecast| minus bottom two fifths",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
