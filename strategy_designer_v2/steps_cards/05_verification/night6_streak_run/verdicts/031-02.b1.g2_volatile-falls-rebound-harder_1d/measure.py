import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.vol_fall.last_history_value"
    H = 2

    # ---------- 1. Situation check: falling day (1-day return < 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(len(d), np.nan)
            ret1 = np.full(len(d), np.nan)
            if len(d) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            for i in range(len(d)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(ret1[i]):
                    fall = ret1[i] < 0
                elif np.isfinite(raw[i]):
                    fall = raw[i] > 0
                else:
                    fall = False
                if fall and f > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled slope of excess 2-bar return on forecast (non-overlapping grid)"
    main_thr = "confirm if slope t >= 2 with supporting difference > 0; reject if slope t <= -2"
    sup_name = "mean excess 2-bar return, high minus low 60-day volatility (per-coin median), forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are falling days with a positive (long) "
                          "forecast, so the config does not do what the plan's Fidelity says (long after a 1-day fall).",
            "reading": "The situation is a negative close-to-close return on the bar (inside its window; on a window's "
                       "first bar a positive raw value marks the fall), expected side long.",
        }

    # ---------- 2. Grid points ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(len(d), np.nan)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                prev_ret = close[i] / close[i - 1] - 1.0 if i >= 1 else np.nan
                rows.append({
                    "coin": coin, "window": w, "day": ts.iloc[i].strftime("%Y-%m-%d"),
                    "ret": r, "forecast": fc[i], "raw": raw[i], "ret1": prev_ret,
                })
    g = pd.DataFrame(rows)
    if len(g) == 0:
        g = pd.DataFrame(columns=["coin", "window", "day", "ret", "forecast", "raw", "ret1"])
    g = g[np.isfinite(g["ret"].astype(float))].copy()
    g["ret"] = g["ret"].astype(float)
    coin_mean = g.groupby("coin")["ret"].mean()
    g["excess"] = g["ret"] - g["coin"].map(coin_mean)

    reg = g[np.isfinite(g["forecast"].astype(float))].copy()
    reg["forecast"] = reg["forecast"].astype(float)

    pos = reg[reg["forecast"] > 0]
    n_pos = int(len(pos))
    n_days_pos = int(pos["day"].nunique())

    # ---------- Main measure: OLS slope, day-clustered SE ----------
    slope = None
    tstat = None
    if len(reg) >= 3 and reg["forecast"].var() > 0:
        X = np.column_stack([np.ones(len(reg)), reg["forecast"].values])
        y = reg["excess"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        scores = X * e[:, None]
        sdf = pd.DataFrame(scores, columns=["a", "b"])
        sdf["day"] = reg["day"].values
        summed = sdf.groupby("day")[["a", "b"]].sum().values
        for s in summed:
            meat += np.outer(s, s)
        V = XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    # ---------- Supporting check ----------
    diff = None
    sup = pos.copy()
    sup["raw"] = pd.to_numeric(sup["raw"], errors="coerce")
    sup["fall_pct"] = -sup["ret1"].astype(float) * 100.0
    sup = sup[np.isfinite(sup["raw"]) & np.isfinite(sup["fall_pct"]) & (sup["fall_pct"] > 0)].copy()
    if len(sup) > 0:
        sup["vol"] = sup["raw"] / sup["fall_pct"] / 100.0
        med = sup.groupby("coin")["vol"].transform("median")
        hi = sup[sup["vol"] > med]["excess"]
        lo = sup[sup["vol"] <= med]["excess"]
        if len(hi) > 0 and len(lo) > 0:
            diff = float(hi.mean() - lo.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {
        "grid points with a forecast above 0": n_pos,
        "distinct days of those grid points": n_days_pos,
        "grid points in regression": int(len(reg)),
        "distinct days in regression": int(reg["day"].nunique()),
    }

    if n_pos < 100 or n_days_pos < 50:
        status = "not observable"
        decided = ("Minimum not reached: the plan needs at least 100 grid points with a forecast above 0 over at least "
                   f"50 distinct days; there are {n_pos} over {n_days_pos} days.")
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the high-minus-low volatility difference is above 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger volatility-weighted falls are followed by weaker 2-day returns."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting difference is at or below 0 (or not computable)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    reading = ("Grid points are rows 0, 2, 4, ... of each window with the 2-bar return inside the window, the coin's "
               "mean is over all its grid points of all windows, the slope SE is the day-clustered sandwich without "
               "small-sample correction, the fall % for the volatility is the bar's own close-to-close fall from the "
               "previous close in the same window (points without it left out), the split puts volatility above the "
               "coin's median in the high group and at or below it in the low group, and the plan's minimum counts "
               "give 'not observable' as the workflow requires.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "slope t, SE clustered by day", "value": tstat},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
