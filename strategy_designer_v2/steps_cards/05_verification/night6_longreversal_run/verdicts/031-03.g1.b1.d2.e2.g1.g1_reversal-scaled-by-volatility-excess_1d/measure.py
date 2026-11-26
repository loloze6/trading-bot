import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.fade.last_history_value"
    ALLOC = "postRebalance_current_allocation"
    VAL = "postRebalance_total_value"

    # ---- gather per-window frames (single coin expected: XMR) ----
    frames = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        keys = sorted(wins.keys(), key=lambda k: int(str(k).lstrip("w")) if str(k).lstrip("w").isdigit() else str(k))
        for w in keys:
            df = wins[w].copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            df["_ret_prev"] = close / close.shift(1) - 1.0       # return into bar t (inside window)
            df["_ret_next"] = close.shift(-1) / close - 1.0      # close[t+1]/close[t]-1 (inside window)
            df["_coin"] = coin
            df["_win"] = w
            frames.append(df)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "OLS slope of next-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"bars with a non-zero forecast": 0},
            "decided_by": "No bars in the record, so the minimum of 500 bars with a non-zero forecast is not reached.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)
    fc = pd.to_numeric(allb[FC], errors="coerce")

    # ---- situation check: graded fade on every bar, side opposite to the day's return ----
    raw = pd.to_numeric(allb[RAW], errors="coerce") if RAW in allb.columns else pd.Series(np.nan, index=allb.index)
    raw_sign = np.sign(raw)
    fallback = np.sign(allb["_ret_prev"])
    raw_sign = raw_sign.where(raw.notna(), fallback)
    active = fc.notna() & (fc != 0)
    n_active = int(active.sum())
    if n_active > 0:
        ok = active & raw_sign.notna() & (raw_sign != 0) & (np.sign(fc) == -raw_sign)
        agreement = float(ok.sum() / n_active)
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of next-bar excess return on forecast (before costs)"
    threshold = "slope > 0 with OLS t >= 2 (and timing > 0) confirms; slope < 0 with t <= -2 rejects; |t| < 2 inconclusive"

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with a non-zero forecast": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are on the side opposite to the day's return (the fade the plan's situation and outcome require).",
            "reading": "The plan's situation holds on every bar with a non-zero one-day move, and its expected side is opposite to the sign of the component's raw value (the scaled one-day return), recomputed from closes where the raw value is missing.",
        }

    # ---- main measure ----
    mu = float(allb["_ret_prev"].dropna().mean())  # XMR mean daily return over all windows
    reg = pd.DataFrame({"x": fc, "y": allb["_ret_next"] - mu}).dropna()
    n_reg = int(len(reg))
    slope, tstat = None, None
    if n_reg >= 3 and reg["x"].var() > 0:
        x = reg["x"].values.astype(float)
        y = reg["y"].values.astype(float)
        xm, ym = x.mean(), y.mean()
        sxx = float(((x - xm) ** 2).sum())
        b = float(((x - xm) * (y - ym)).sum() / sxx)
        a = ym - b * xm
        resid = y - a - b * x
        s2 = float((resid ** 2).sum() / (n_reg - 2))
        se = np.sqrt(s2 / sxx) if s2 > 0 else np.nan
        slope = b
        tstat = float(b / se) if se and np.isfinite(se) and se > 0 else None

    # ---- supporting check: timing part of book's mean daily return ----
    book_rets, mkt_parts = [], []
    for df in frames:
        v = pd.to_numeric(df[VAL], errors="coerce")
        al = pd.to_numeric(df[ALLOC], errors="coerce")
        br = v / v.shift(1) - 1.0
        mp = al.shift(1) * mu
        d = pd.DataFrame({"b": br, "m": mp}).dropna()
        book_rets.append(d["b"])
        mkt_parts.append(d["m"])
    timing = None
    if book_rets:
        b_all = pd.concat(book_rets)
        m_all = pd.concat(mkt_parts)
        if len(b_all) > 0:
            timing = float(b_all.mean() - m_all.mean())
    sup_pass = None if timing is None else bool(timing > 0)

    n_nonzero = n_active
    counts = {"bars with a non-zero forecast": n_nonzero, "bars in the slope": n_reg}

    reading = ("The slope is an OLS of next-bar excess return on forecast with an intercept over every recorded bar with a next close in its window "
               "(forecast-0 bars included), XMR's mean daily return is the pooled close-to-close mean of all windows, the book's daily return is "
               "postRebalance_total_value bar to bar inside each window with the market part being the prior bar's allocation times that mean, "
               "and the minimum of 500 non-zero-forecast bars is counted over all recorded bars and, if missed, gives 'not observable'.")

    stat = None if tstat is None else {"name": "OLS t of the slope", "value": tstat}
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}
    sup = {"name": "timing part of the book's mean daily return (mean minus market-rise gain)", "value": timing, "passed": sup_pass}
    sit = {"agreement": agreement, "passed": bool(passed)}

    if n_nonzero < 500:
        status = "not observable"
        decided = f"Only {n_nonzero} bars have a non-zero forecast, below the plan's minimum of 500."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing part of the book's mean daily return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing part of the book's mean daily return is not above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: moves continue rather than reverse."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2 (or its sign and t disagree), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
