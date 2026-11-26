import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check: 3-day rise (raw > 0), side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            ret3 = close / close.shift(3) - 1.0
            rise = raw.copy()
            # where the raw value is not recorded, use the 3-day price return (same sign)
            rise = rise.where(rise.notna(), ret3)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & (rise > 0) & (fc < 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of drift-adjusted 20-bar forward return on abs(forecast), forecast<0 grid cells"
    thr = "slope t <= -2 confirms (with supporting check); slope t >= +2 rejects"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars after a positive "
                           "3-day scaled return, so the config does not do what the Fidelity's situation and side say."),
            "reading": "Situation taken as raw scaled 3-day return > 0 (price 3-day return where not recorded), expected side short; the profile is left to the regime code.",
        }

    # ---------- 2. criterion ----------
    # coin drift: mean of non-overlapping 20-bar returns over all its windows
    grid_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append({
                    "coin": coin, "window": w, "ret": c1 / c0 - 1.0,
                    "forecast": fc[t], "day": ts.iloc[t].floor("D"),
                })
    g = pd.DataFrame(grid_rows, columns=["coin", "window", "ret", "forecast", "day"])
    if len(g) > 0:
        drift = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(drift)
    cases = g[g["forecast"].notna() & (g["forecast"] < 0)].copy() if len(g) > 0 else g
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases > 0 else 0

    slope = None
    slope_t = None
    if n_cases >= 3:
        x = cases["forecast"].abs().values.astype(float)
        y = cases["excess"].values.astype(float)
        if np.ptp(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
                slope_t = float(lr.slope / lr.stderr)

    mean_ex = None
    mean_t = None
    if n_cases >= 2:
        y = cases["excess"].values.astype(float)
        mean_ex = float(np.mean(y))
        dev = pd.Series(y - mean_ex, index=cases.index)
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        if D >= 2:
            var = (D / (D - 1.0)) * np.sum(S ** 2) / (n_cases ** 2)
            if var > 0:
                mean_t = float(mean_ex / np.sqrt(var))

    support_pass = None if mean_t is None else bool(mean_ex < 0 and mean_t <= -2)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 30."
    elif slope_t is not None and slope_t <= -2 and support_pass:
        status = "confirmed"
        decided = "Slope t is -2 or less and the mean drift-adjusted 20-bar return is below 0 with t of -2 or less."
    elif (slope_t is not None and slope_t >= 2) or (mean_t is not None and mean_t >= 2):
        status = "rejected"
        decided = "Slope t is +2 or more, or the mean drift-adjusted 20-bar return has a t of +2 or more."
    else:
        status = "inconclusive"
        decided = ("Neither the confirm rule (slope t <= -2 with supporting check passed) nor the reject rule "
                   "(slope t >= +2 or mean t >= +2) is met.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean drift-adjusted 20-bar return over cases < 0 with day-clustered t <= -2",
            "value": mean_t,
            "passed": support_pass,
        },
        "counts": {"non-overlapping cases": n_cases, "days": n_days, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("Cases are grid cells at positions 0,20,40,... of each window with forecast < 0 and a full 20-bar "
                    "forward return inside the window, drift is the coin's mean over that grid in all windows, the "
                    "supporting t clusters deviations by UTC day, the same t is used for the reject rule's mean, and "
                    "the plan's 30-case minimum gives 'not observable' when unmet."),
    }
