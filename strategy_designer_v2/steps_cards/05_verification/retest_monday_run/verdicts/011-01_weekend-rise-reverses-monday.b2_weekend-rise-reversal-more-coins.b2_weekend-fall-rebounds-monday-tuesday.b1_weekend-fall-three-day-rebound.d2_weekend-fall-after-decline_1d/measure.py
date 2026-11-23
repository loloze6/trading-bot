import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 100
    RAW = "debug_info.components.weekend_fall_x_20d_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            # Sunday bar: the coming bar (start + 1 day) is a Monday
            sunday = ((ts + pd.Timedelta(days=1)).dt.dayofweek == 0).values
            r1 = (close / close.shift(1) - 1).values
            r20 = (close / close.shift(20) - 1).values
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            # situation: Sunday bar, weekend fall and 20-day fall (raw product > 0),
            # checked on prices wherever they are computable inside the window
            raw_ok = np.where(np.isnan(raw), True, raw > 0)
            r1_ok = np.where(np.isnan(r1), True, r1 < 0)
            r20_ok = np.where(np.isnan(r20), True, r20 < 0)
            have_info = ~(np.isnan(raw) & np.isnan(r1) & np.isnan(r20))
            situ = sunday & raw_ok & r1_ok & r20_ok & have_info
            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0).values).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": True},
            "main_measure": {"name": "mean excess 3-day return after Sunday bars with forecast > 0",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 (confirm) or t <= -2 (reject) on at least 100 cases"},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than the 100 cases the plan requires.",
            "reading": "With no active bar the situation check is vacuous and the case count is 0.",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean excess 3-day return after Sunday bars with forecast > 0",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 (confirm) or t <= -2 (reject) on at least 100 cases"},
            "supporting_check": None,
            "counts": None,
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long Sunday bars after both a "
                           "weekend fall and a 20-day fall, as the plan's situation requires."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    excess, fcs = [], []
    for coin, wins in bars.items():
        # coin's mean 3-day return over all its windows (non-overlapping grid 0, 3, 6, ...)
        grid = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    grid.append(c[i + H] / c[i] - 1)
        if len(grid) == 0:
            continue
        drift = float(np.mean(grid))
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            sunday = ((ts + pd.Timedelta(days=1)).dt.dayofweek == 0).values
            for i in range(len(d) - H):
                if sunday[i] and np.isfinite(fc[i]) and fc[i] > 0:
                    if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                        excess.append(c[i + H] / c[i] - 1 - drift)
                        fcs.append(float(fc[i]))

    n = len(excess)
    ex = np.array(excess, dtype=float)
    f = np.array(fcs, dtype=float)
    mean_ex = float(ex.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = ex.std(ddof=1)
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n > 2 and np.ptp(f) > 0:
        slope = float(stats.linregress(f, ex).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    main = {"name": "mean excess 3-day return after Sunday bars with forecast > 0",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "t >= 2 with slope > 0 (confirm), t <= -2 (reject), on at least 100 cases"}
    supp = {"name": "OLS slope of excess 3-day return on forecast", "value": slope, "passed": slope_pass}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the 100 the plan requires."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (zero dispersion), so neither rule is met."
    elif t >= 2 and mean_ex > 0 and slope_pass:
        status = "confirmed"
        decided = "Mean excess 3-day return positive with t >= 2 on at least 100 cases and a positive slope."
    elif t <= -2 and mean_ex < 0:
        status = "rejected"
        decided = "Mean excess 3-day return negative with t <= -2 on at least 100 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "t is 2 or more but the supporting slope is 0 or below (or not computable)."
    else:
        status = "inconclusive"
        decided = "t falls between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": {"cases": int(n)},
        "decided_by": decided,
        "reading": ("A Sunday bar is one whose next calendar day is a Monday (UTC), a case needs close[t+3] in the "
                    "same window, and the coin's mean 3-day return is taken on the non-overlapping grid 0, 3, 6, ... "
                    "of all its windows pooled; fewer than 100 cases is reported as not observable."),
    }
