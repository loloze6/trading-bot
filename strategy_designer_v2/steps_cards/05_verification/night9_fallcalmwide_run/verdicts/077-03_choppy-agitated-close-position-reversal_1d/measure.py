import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.close_off_mid.last_history_value"

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- collect rows ----------
    rows = []
    for coin, wins in bars.items():
        coin_frames = []
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = to_time(d["timestamp"])
            d = d.sort_values("ts").reset_index(drop=True)
            close = d["close"].astype(float)
            d["ret_next"] = close.shift(-1) / close - 1.0  # inside the window only
            d["ret_this"] = close / close.shift(1) - 1.0
            d["coin"] = coin
            d["window"] = w
            coin_frames.append(d)
        if not coin_frames:
            continue
        cdf = pd.concat(coin_frames, ignore_index=True)
        # coin's mean daily return over all windows together
        mu = cdf["ret_this"].dropna().mean()
        cdf["excess_next"] = cdf["ret_next"] - mu
        rows.append(cdf)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"in-position bars": 0, "distinct days": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }

    all_df = pd.concat(rows, ignore_index=True)
    all_df["forecast"] = all_df["forecast"].astype(float)
    all_df["day"] = all_df["ts"].dt.floor("D")

    # ---------- situation check ----------
    active = all_df[all_df["forecast"].fillna(0) != 0].copy()
    n_active = len(active)
    if n_active > 0:
        mid = (active["high"].astype(float) + active["low"].astype(float)) / 2.0
        off = np.sign(active["close"].astype(float) - mid)
        if RAW in active.columns:
            raw_sign = np.sign(active[RAW].astype(float))
            # raw value's sign is the close's side of mid-range; use it where recorded
            off = raw_sign.where(active[RAW].notna(), off)
        in_profile = active["regime"].astype(str) == "unknown"
        expected = -off  # close above middle -> short, below -> long
        ok = in_profile & (off != 0) & (np.sign(active["forecast"]) == expected)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the non-zero-forecast bars are choppy-agitated-profile bars "
                           "(regime 'unknown') with the forecast opposite the close's side of mid-range."),
            "reading": "The profile is read from the recorded regime ('unknown' = not vetoed to chop); the close's side from the raw component sign, or from close vs (high+low)/2 where not recorded.",
        }

    # ---------- main measure ----------
    reg = all_df[(all_df["forecast"].fillna(0) != 0)].dropna(subset=["excess_next"]).copy()
    x = reg["forecast"].to_numpy(float)
    y = reg["excess_next"].to_numpy(float)
    n = len(reg)

    slope, t_slope = None, None
    if n >= 3 and np.var(x) > 0:
        X = np.column_stack([np.ones(n), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        u = y - X @ beta
        groups = reg["day"].to_numpy()
        codes, uniq = pd.factorize(groups)
        G = len(uniq)
        S = np.zeros((G, 2))
        np.add.at(S, codes, X * u[:, None])
        meat = S.T @ S
        corr = (G / (G - 1)) * ((n - 1) / (n - 2)) if G > 1 else np.nan
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t_slope = float(slope / se) if se and np.isfinite(se) else None

    # ---------- in-position bars, supporting check ----------
    alloc = all_df["postRebalance_current_allocation"].astype(float).fillna(0)
    inpos = all_df[(alloc != 0)].dropna(subset=["excess_next", "forecast"]).copy()
    n_inpos = len(inpos)
    n_days = int(inpos["day"].nunique())

    sup_val, sup_pass = None, None
    k = n_inpos // 3
    if k > 0:
        inpos["absf"] = inpos["forecast"].abs()
        top = inpos.sort_values("absf", ascending=False, kind="mergesort").head(k)
        dir_ret = np.sign(top["forecast"].to_numpy(float)) * top["excess_next"].to_numpy(float)
        sup_val = float(np.mean(dir_ret))
        sup_pass = bool(sup_val > 0)

    counts = {"in-position bars": int(n_inpos), "distinct days": n_days,
              "bars with non-zero forecast (regression cases)": int(n),
              "top-third bars": int(k)}

    main = {"name": "OLS slope of next-day excess return on forecast",
            "value": slope,
            "statistic": {"name": "slope t, clustered by day", "value": t_slope} if t_slope is not None else None,
            "threshold": "t >= 2 (with supporting check) confirms; t <= -2 rejects; between is inconclusive"}
    support = {"name": "mean next-day excess return in forecast direction, top third |forecast|",
               "value": sup_val, "passed": sup_pass}
    reading = ("In-position bars are bars with a non-zero postRebalance_current_allocation and a next-day return in the same window; "
               "the top third is the n//3 largest |forecast| among them; the slope is OLS with an intercept on non-zero-forecast bars, "
               "its t from day-clustered (sandwich, G/(G-1)*(n-1)/(n-2)) standard errors; the coin's mean daily return uses all its in-window close-to-close returns.")

    result = {"situation_check": {"agreement": agreement, "passed": True},
              "main_measure": main, "supporting_check": support,
              "counts": counts, "reading": reading}

    if n_inpos < 300 or n_days < 150:
        result["status"] = "not observable"
        result["decided_by"] = ("Minimum count not reached: fewer than 300 in-position bars or fewer than 150 distinct days "
                                f"({n_inpos} bars, {n_days} days).")
        return result

    if t_slope is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
        return result

    if t_slope >= 2:
        if sup_pass:
            result["status"] = "confirmed"
            result["decided_by"] = "The slope's t is 2 or more and the top-third mean directional excess return is above 0."
        else:
            result["status"] = "inconclusive"
            result["decided_by"] = "The slope's t is 2 or more but the supporting check failed, which the plan calls inconclusive."
    elif t_slope <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "The slope's t is -2 or less."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "The slope's t lies between -2 and 2."
    return result
