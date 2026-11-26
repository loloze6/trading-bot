import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.wide_low_close.last_history_value"

    def _to_day(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            dt = pd.to_datetime(v, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.floor("D")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: the day closes below its high (the raw product of range multiple and
            # low-close location is strictly negative), expected side long
            sit = raw.notna() & (raw < 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of next-day excess return on forecast (all coins, windows)"
    thr = "confirm: slope > 0 with t >= 2 and top-minus-bottom fifth > 0; reject: slope < 0 with t <= -2"
    sup_name = "mean next-day excess return, top fifth minus bottom fifth of forecasts (per coin)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on days "
                           "closing below their high (raw component < 0), as the plan's situation requires."),
            "reading": "The situation is every day whose close is below its high (raw component value < 0), on the long side.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_parts = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            day = _to_day(df["timestamp"]).reset_index(drop=True)
            nxt = close.shift(-1) / close - 1.0
            part = pd.DataFrame({"coin": coin, "day": day, "f": fc, "r": nxt})
            coin_parts.append(part)
        if not coin_parts:
            continue
        cdf = pd.concat(coin_parts, ignore_index=True)
        cdf = cdf[np.isfinite(cdf["r"])]
        mu = cdf["r"].mean()  # coin's mean daily return over all its windows
        cdf = cdf.assign(x=cdf["r"] - mu)
        cdf = cdf[cdf["f"].notna() & np.isfinite(cdf["x"])]
        rows.append(cdf)

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["coin", "day", "f", "r", "x"])

    n_days = int(data["day"].nunique()) if len(data) else 0
    n_f2 = int((data["f"] >= 2).sum()) if len(data) else 0
    counts = {"independent days": n_days, "bars with forecast >= 2": n_f2, "bars": int(len(data))}

    # slope with day-clustered standard error
    slope = None
    tstat = None
    if len(data) >= 3 and data["f"].var() > 0:
        f = data["f"].to_numpy(float)
        y = data["x"].to_numpy(float)
        X = np.column_stack([np.ones_like(f), f])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        codes = pd.factorize(data["day"])[0]
        G = codes.max() + 1
        sx = np.zeros((G, 2))
        np.add.at(sx, codes, X * e[:, None])
        meat = sx.T @ sx
        n, k = X.shape
        corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    # supporting check: per-coin fifths by rank
    diff = None
    if len(data):
        parts = []
        for coin, g in data.groupby("coin", sort=True):
            if len(g) < 5:
                continue
            rk = g["f"].rank(method="first")
            q = pd.qcut(rk, 5, labels=False)
            parts.append(g.assign(q=q.to_numpy()))
        if parts:
            qd = pd.concat(parts, ignore_index=True)
            top = qd.loc[qd["q"] == 4, "x"]
            bot = qd.loc[qd["q"] == 0, "x"]
            if len(top) and len(bot):
                diff = float(top.mean() - bot.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    reading = ("Every recorded bar enters the regression (forecast 0 included), the coin mean is over all its "
               "next-day returns in all windows, t is OLS with day-clustered errors, the fifths are cut per coin by "
               "forecast rank (ties broken by time order), and a minimum count not reached is reported as 'not observable'.")

    if n_days < 2000 or n_f2 < 500:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_days} independent days (need 2,000) and "
                   f"{n_f2} bars with forecast >= 2 (need 500).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top-minus-bottom fifth difference is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the top-minus-bottom fifth difference is 0 or below."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: stronger readings are followed by further falls."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS t, day-clustered", "value": tstat},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
