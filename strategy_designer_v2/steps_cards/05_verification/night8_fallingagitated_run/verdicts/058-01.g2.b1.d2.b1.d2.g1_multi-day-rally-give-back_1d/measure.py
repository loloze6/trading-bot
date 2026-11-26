import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.rally_in_swings.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime left when neither 'chop' veto fires = falling agitated

    def _prep(df):
        d = df.copy().reset_index(drop=True)
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
        return d

    def _raw_component(d):
        # raw value as recorded; where missing, recompute from prices:
        # 3-day return / (30-day std of daily returns * sqrt(3))
        close = d["close"]
        r1 = close.pct_change()
        r3 = close / close.shift(3) - 1.0
        vol = r1.rolling(30, min_periods=30).std() * np.sqrt(3.0)
        recomputed = r3 / vol.replace(0, np.nan)
        if RAW in d.columns:
            rec = pd.to_numeric(d[RAW], errors="coerce")
            return rec.where(rec.notna(), recomputed)
        return recomputed

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = _prep(df)
            raw = _raw_component(d)
            f = d["forecast"]
            active = f.notna() & (f != 0)
            in_profile = d["regime"].astype(str) == PROFILE_REGIME
            situation = in_profile & (raw > 0)
            agree = active & situation & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": (
                "Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling-agitated "
                "profile after a 3-day rise (positive scaled 3-day return), as the Fidelity requires."
            ),
            "reading": "The profile is read from the recorded regime (the strategy regime 'unknown' that remains when "
                       "neither chop veto fires), and the rise from the component's raw value (recomputed from prices where missing).",
        }

    # ---------- 2. criterion ----------
    # coin's normal 3-day drift: mean of non-overlapping 3-day returns over all its windows
    grid_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = _prep(df)
            close = d["close"].values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append({
                    "coin": coin,
                    "ret": c1 / c0 - 1.0,
                    "forecast": d["forecast"].iloc[i],
                    "day": d["timestamp"].iloc[i].normalize(),
                })
    g = pd.DataFrame(grid_rows, columns=["coin", "ret", "forecast", "day"])
    drift = g.groupby("coin")["ret"].mean() if len(g) else pd.Series(dtype=float)

    cases = g[g["forecast"].notna() & (g["forecast"] < 0)].copy()
    if len(cases):
        cases["unusual"] = -(cases["ret"] - cases["coin"].map(drift))
        cases = cases[cases["unusual"].notna()]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["unusual"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cases["unusual"] - mean_u
        day_sums = dev.groupby(cases["day"]).sum().values
        var_mean = (n_days / (n_days - 1.0)) * np.sum(day_sums ** 2) / (n_cases ** 2)
        se = np.sqrt(var_mean)
        if se > 0:
            t_val = float(mean_u / se)

    # supporting check: split at median |forecast|
    diff = None
    if n_cases:
        a = cases["forecast"].abs()
        med = float(a.median())
        large = cases.loc[a > med, "unusual"]
        small = cases.loc[a <= med, "unusual"]
        if len(large) and len(small):
            diff = float(large.mean() - small.mean())
    support_pass = None if diff is None else bool(diff > 0)

    counts = {"cases": n_cases, "cases on distinct days": n_days}

    if n_days < 30:
        status = "not observable"
        decided_by = f"Fewer than 30 cases on distinct days ({n_days}), the plan's minimum count."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t of the mean unusual move could not be computed, so it does not meet the confirm or reject rule."
    elif mean_u > 0 and t_val >= 2:
        if support_pass:
            status = "confirmed"
            decided_by = "Mean unusual move above 0 with t >= 2, and the larger-|forecast| half's mean exceeds the smaller half's."
        else:
            status = "inconclusive"
            decided_by = "Mean unusual move above 0 with t >= 2, but the size check (larger half minus smaller half > 0) fails."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "Mean unusual move below 0 with t <= -2: 3-day rises in this profile continue."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 3-day move in the short's direction (return minus coin's normal 3-day drift, x -1)",
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together", "value": t_val},
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 cases on distinct days",
        },
        "supporting_check": {
            "name": "mean unusual move of larger-|forecast| half minus smaller half",
            "value": diff,
            "passed": support_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": (
            "Profile read from the recorded regime 'unknown' (no chop veto) and the rise from the raw component > 0; "
            "cases are grid bars 0,3,6,... of each window with forecast < 0 and a 3-bar return inside the window; drift is "
            "the coin's mean non-overlapping 3-day return over all windows; the t uses deviations summed per UTC day with a "
            "D/(D-1) correction; the larger half is |forecast| strictly above the median and the smaller half at or below it; "
            "the minimum of 30 is applied to the number of distinct days of the cases."
        ),
    }
