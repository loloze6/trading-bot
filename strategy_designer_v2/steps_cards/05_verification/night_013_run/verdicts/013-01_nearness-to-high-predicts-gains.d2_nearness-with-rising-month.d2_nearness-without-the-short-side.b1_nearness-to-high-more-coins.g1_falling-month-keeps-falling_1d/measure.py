import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    DEPTH = "debug_info.components.depth.last_history_value"

    # ---------------- 1. Situation check ----------------
    active_total = 0
    active_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # 30-day return, recomputed from prices inside the window
            ret30 = close / close.shift(30) - 1.0
            reg_mr = d["regime"].astype(str) == "mean_reversion"
            falling = pd.Series(np.where(ret30.notna(), ret30 < 0, reg_mr), index=d.index).astype(bool)
            # depth below 60-day high: recorded raw value, else recomputed from closes
            if DEPTH in d.columns:
                depth = pd.to_numeric(d[DEPTH], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=d.index)
            depth_px = close / close.rolling(60, min_periods=1).max() - 1.0
            depth = depth.where(depth.notna(), depth_px)
            below = depth < 0
            situation = falling & below
            act = fc.notna() & (fc != 0)
            active_total += int(act.sum())
            active_agree += int((act & situation & (fc < 0)).sum())

    agreement = float(active_agree / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of excess 7-bar return on forecast, falling-month regime grid bars"
    thr = "confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2; at least 100 grid cases"
    reading = ("The falling month is the 30-day close-to-close return recomputed inside each window (the recorded regime "
               "is used on the first 30 rows where it cannot be recomputed), the depth below the high is the recorded "
               "depth raw value (< 0), the expected side is short, the coin's mean 7-bar return is taken over all its "
               "grid bars in all windows, and the minimum of 100 grid cases is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars in situation on short side": int(active_agree)},
            "decided_by": (f"Only {agreement:.1%} of the {active_total} active bars are short bars of the plan's situation "
                           "(close below its 60-day high with a negative 30-day return), below the 90% required."),
            "reading": reading,
        }

    # ---------------- 2. Criterion ----------------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                rows.append({
                    "coin": coin,
                    "ret": r,
                    "regime": str(d["regime"].iloc[i]),
                    "forecast": pd.to_numeric(pd.Series([d["forecast"].iloc[i]]), errors="coerce").iloc[0],
                })
    g = pd.DataFrame(rows, columns=["coin", "ret", "regime", "forecast"])
    if len(g) > 0:
        g = g[np.isfinite(g["ret"])]
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
        cases = g[(g["regime"] == "mean_reversion")].dropna(subset=["forecast", "excess"])
    else:
        cases = g
    n_cases = int(len(cases))

    slope = None
    tval = None
    gain = None
    if n_cases >= 3:
        x = cases["forecast"].astype(float).values
        y = cases["excess"].astype(float).values
        xm = x - x.mean()
        sxx = float((xm ** 2).sum())
        if sxx > 0:
            b = float((xm * (y - y.mean())).sum() / sxx)
            a = y.mean() - b * x.mean()
            resid = y - a - b * x
            s2 = float((resid ** 2).sum() / (n_cases - 2))
            se = np.sqrt(s2 / sxx)
            slope = b
            tval = float(b / se) if se > 0 else (float(np.sign(b) * np.inf) if b != 0 else 0.0)
    if n_cases > 0:
        gain = float(np.mean(cases["forecast"].astype(float).values / 10.0 * cases["excess"].astype(float).values))
    gain_pass = None if gain is None else bool(gain > 0)

    counts = {"grid cases in the regime": n_cases}
    supporting = {"name": "mean of (forecast/10) x excess 7-bar return", "value": gain, "passed": gain_pass}
    stat = None if tval is None else {"name": "OLS t of slope", "value": float(tval)}
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": thr}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases in the falling-month regime, fewer than the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope could not be estimated (no variation in the forecast), which meets neither confirm nor reject."
    elif slope > 0 and tval >= 2:
        if gain_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing gain is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing gain is not above 0 (inconclusive rule)."
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
