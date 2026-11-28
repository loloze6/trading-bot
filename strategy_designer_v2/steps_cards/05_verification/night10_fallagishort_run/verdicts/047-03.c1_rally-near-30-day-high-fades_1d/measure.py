import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    FC = "forecast"
    MIN_CASES = 30
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            day_ret = close / close.shift(1) - 1.0
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            in_profile_rule = regime == "mean_reversion"
            up = day_ret > 0
            # first bar of a window has no previous close inside the window: fall back on the detector's regime
            up = up.where(day_ret.notna(), in_profile_rule)
            situation = up & in_profile_rule
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "OLS slope of drift-adjusted 3-day return on abs forecast, over the cases"
    threshold = "slope t <= -2 confirms (with supporting check and >=30 cases on >=30 days); t >= +2 rejects"
    reading = ("Up day recomputed from closes and the falling-agitated profile read from the recorded regime "
               "(the detector's components are not recorded); a case is the first short bet (forecast rising "
               "in size by >= 2 points from its lowest level on the short side since the last bet) in each 3-bar "
               "grid cell of each window, and the slope's t is the ordinary OLS t pooled over all coins.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on up days inside "
                           "the falling agitated profile, which the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 3-bar returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            bet = np.zeros(n, dtype=bool)
            side = 0
            level = 0.0
            for t in range(n):
                s = int(np.sign(f[t]))
                a = abs(f[t])
                if s == 0:
                    side, level = 0, 0.0
                    continue
                if s != side:
                    side, level = s, 0.0
                if a - level >= BAND:
                    bet[t] = True
                    level = a
                else:
                    level = min(level, a)
            for start in range(0, n, H):
                cell = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not cell:
                    continue
                t = cell[0]
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r) or pd.isna(ts.iloc[t]):
                    continue
                xs.append(abs(f[t]))
                ys.append(r - drift)
                days.append(ts.iloc[t].strftime("%Y-%m-%d"))

    n_cases = len(xs)
    n_days = len(set(days))
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_unusual_short = float(np.mean(-ys)) if n_cases > 0 else None
    support_pass = None if mean_unusual_short is None else bool(mean_unusual_short > 0)

    counts = {"cases": n_cases, "distinct days": n_days}
    main = {
        "name": main_name,
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": threshold,
    }
    support = {"name": "mean unusual move in the short direction > 0",
               "value": mean_unusual_short, "passed": support_pass}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on 30 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in forecast size), so neither rule is met."
    elif t_slope <= -2:
        if support_pass:
            status = "confirmed"
            decided = ("The slope's t is -2 or less with at least 30 cases on 30 days and the mean unusual move "
                       "in the short direction is above 0.")
        else:
            status = "inconclusive"
            decided = ("The slope's t is -2 or less but the mean unusual move in the short direction is at or "
                       "below 0, an inconclusive case of the plan.")
    elif t_slope >= 2:
        status = "rejected"
        decided = "The slope's t is +2 or more with at least 30 cases on at least 30 days."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
