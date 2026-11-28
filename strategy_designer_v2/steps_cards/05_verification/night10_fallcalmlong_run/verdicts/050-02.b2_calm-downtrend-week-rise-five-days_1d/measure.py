import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    COMP = "debug_info.components.scaled_rise.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # raw sign of the 7-day scaled return: recorded value, else 7-bar return from prices
            raw = pd.to_numeric(df[COMP], errors="coerce") if COMP in df.columns else pd.Series(np.nan, index=df.index)
            ret7 = close / close.shift(7) - 1.0
            rise = raw.where(raw.notna(), ret7)
            # falling calm profile = regime detector leaves default "unknown" (no veto to chop)
            profile = df["regime"].astype(str).str.lower() == "unknown"
            active = fc.notna() & (fc != 0)
            situ = profile & (rise > 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 5-bar forward return over holding the coin, cases forecast > 0"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: t <= -2"
    sup_name = "OLS slope of excess 5-bar return on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None, "active bars": n_active},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars inside the falling calm profile "
                          "(regime 'unknown') with a positive 7-day scaled return, as the Fidelity's situation requires.",
            "reading": "The falling calm profile is read from the recorded regime ('unknown' = no veto to chop), the rise "
                       "from the sign of the recorded scaled_rise raw value (7-bar price return where missing).",
        }

    # ---------- 2. criterion ----------
    xs, fs, days = [], [], []
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all its windows, on each window's non-overlapping grid
        all_r = []
        per_window = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = _ts(df)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                per_window.append((r, fc[i], ts.iloc[i]))
        if not all_r:
            continue
        mu = float(np.mean(all_r))
        for r, f, t in per_window:
            if np.isfinite(f) and f > 0 and pd.notna(t):
                xs.append(r - mu)
                fs.append(float(f))
                days.append(t.normalize())

    xs = np.asarray(xs, dtype=float)
    fs = np.asarray(fs, dtype=float)
    n_cases = int(len(xs))
    n_days = int(len(set(days)))

    mean_ex = float(np.mean(xs)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1 and n_days > 1:
        dev = xs - xs.mean()
        s = pd.Series(dev).groupby(pd.Series(days)).sum().to_numpy()
        D = len(s)
        var = (D / (D - 1)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            t_val = float(xs.mean() / np.sqrt(var))
    slope = None
    if n_cases > 2 and np.unique(fs).size > 1:
        slope = float(stats.linregress(fs, xs).slope)

    counts = {"cases": n_cases, "distinct days": n_days}
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 50 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum of 50 cases on at least 30 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed (zero variance), so neither confirm nor reject is met."
    elif mean_ex > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean excess return is above 0 with t >= 2 and the slope on the forecast is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The mean excess return has t <= -2: the coin underperforms holding after scaled rises."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope is at or below 0 (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are grid bars (positions 0,5,10,... per window with a full 5-bar forward return) with forecast > 0; "
                   "the coin's mean is over all its windows' grid 5-bar returns; the profile is the recorded regime 'unknown'; "
                   "the plan's 'fewer cases' rule is applied as 'not observable' as the workflow requires.",
    }
