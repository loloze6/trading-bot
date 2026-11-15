import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    LB = 60
    LHV = "debug_info.components.rsi_mom.last_history_value"

    # ---------- 1. Situation check: RSI(14) > 50, long side ----------
    # RSIPullbackComponent's raw value is (50 - RSI): the situation RSI > 50 is a raw value < 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            lhv = pd.to_numeric(df[LHV], errors="coerce") if LHV in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & lhv.notna() & (lhv < 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    threshold_txt = "confirm if slope t >= 2 and positive-60d slope > other slope; reject if t <= -2"
    main_name = "pooled OLS slope of 10-bar excess return on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast have RSI(14) above 50 (raw 50-RSI below 0) with a positive (long) forecast, so the config does not do what the plan's situation says.",
            "reading": "The situation RSI(14) > 50 is read as the component's raw last_history_value (50 - RSI) being below 0, with the expected side long (forecast > 0).",
        }

    # ---------- 2. Build non-overlapping 10-bar grid cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                r60 = close[t] / close[t - LB] - 1.0 if t - LB >= 0 else np.nan
                rows.append((coin, w, t, fc[t], r, r60))
    cases = pd.DataFrame(rows, columns=["coin", "window", "pos", "forecast", "ret", "ret60"])
    cases = cases.replace([np.inf, -np.inf], np.nan)
    cases = cases.dropna(subset=["forecast", "ret"])

    coin_mean = cases.groupby("coin")["ret"].mean()
    cases["y"] = cases["ret"] - cases["coin"].map(coin_mean)

    def ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        if len(x) < 3 or np.var(x) == 0:
            return None, None
        res = stats.linregress(x, y)
        slope = float(res.slope)
        se = float(res.stderr)
        t = float(slope / se) if se > 0 else None
        return slope, t

    n_cases = int(len(cases))
    n_pos_fc = int((cases["forecast"] > 0).sum())

    sub = cases.dropna(subset=["ret60"])
    pos_g = sub[sub["ret60"] > 0]
    oth_g = sub[sub["ret60"] <= 0]
    n_pos60 = int(len(pos_g))
    n_oth60 = int(len(oth_g))

    slope, tstat = ols(cases["forecast"], cases["y"])
    s_pos, _ = ols(pos_g["forecast"], pos_g["y"])
    s_oth, _ = ols(oth_g["forecast"], oth_g["y"])
    if s_pos is not None and s_oth is not None:
        diff = float(s_pos - s_oth)
        check_pass = bool(diff > 0)
    else:
        diff = None
        check_pass = None

    counts = {
        "cases": n_cases,
        "cases with forecast > 0": n_pos_fc,
        "cases with positive 60-day return": n_pos60,
        "cases with non-positive 60-day return": n_oth60,
    }

    reading = ("Cases are grid bars 0,10,20,... of each window with close[t+10] inside the window, the coin's mean 10-bar return "
               "is the mean over that coin's grid cases in all windows, the slope t is the ordinary OLS t (with intercept), the "
               "'other' group is cases with a 60-day return <= 0, the 30-case minimum is counted on all cases of each group, "
               "and minimum counts not reached give 'not observable'.")

    if n_pos_fc < 100 or n_pos60 < 30 or n_oth60 < 30:
        status = "not observable"
        miss = []
        if n_pos_fc < 100:
            miss.append(f"only {n_pos_fc} cases with forecast > 0 (need 100)")
        if n_pos60 < 30:
            miss.append(f"only {n_pos60} positive-60-day cases (need 30)")
        if n_oth60 < 30:
            miss.append(f"only {n_oth60} other 60-day cases (need 30)")
        decided = "Minimum count not reached: " + "; ".join(miss) + "."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no forecast variation), which meets neither the confirm nor the reject rule."
    elif tstat >= 2:
        if check_pass:
            status = "confirmed"
            decided = "The main slope's t is 2 or more and the slope on positive-60-day cases exceeds the slope on the other cases."
        else:
            status = "inconclusive"
            decided = "The main slope's t is 2 or more but the supporting check failed (positive-60-day slope not larger), which the plan calls inconclusive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The main slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The main slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tstat} if tstat is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "slope on positive-60d cases minus slope on other cases",
            "value": diff,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
