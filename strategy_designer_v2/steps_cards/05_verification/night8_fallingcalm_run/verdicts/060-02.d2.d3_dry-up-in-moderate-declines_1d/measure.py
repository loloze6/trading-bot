import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"

    # ---------- 1. situation check ----------
    # Plan situation: falling market (profile: 60-bar return < -10 %, i.e. not vetoed by gte -10)
    # and 10-bar return below 0; expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if i >= 60:
                    r10 = (close[i] / close[i - 10] - 1.0) * 100.0
                    r60 = (close[i] / close[i - 60] - 1.0) * 100.0
                    situ = (r10 < 0) and (r60 < -10)
                elif i >= 10:
                    r10 = (close[i] / close[i - 10] - 1.0) * 100.0
                    situ = (r10 < 0) and (regime[i] == "trending")
                else:
                    situ = regime[i] == "trending"
                if situ and f < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is the 10-bar return below 0 and the 60-bar return below -10 % (the profile veto), "
               "both from closes inside the window, with the recorded regime 'trending' standing in for the part "
               "that cannot be computed on a window's first 60 bars; the main mean is over the cases, its t uses "
               "the deviations summed per day (cluster standard error), the drift is the coin's mean 5-bar return "
               "on the same grid over all its windows, and 'fewer than 30 days' is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean sign-flipped 5-bar excess return on short-signal grid bars",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the active bars are short bars of the plan's situation "
                           "(10-day return < 0 in a falling market with 60-day return < -10 %), below 90 %."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean non-overlapping 5-bar return over all windows
    drift = {}
    grid_rows = []
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allret.append(r)
                grid_rows.append((coin, ts[i], fc[i], r))
        drift[coin] = float(np.mean(allret)) if allret else np.nan

    cases = [(c, d, f, r) for (c, d, f, r) in grid_rows if np.isfinite(f) and f < 0 and np.isfinite(drift[c])]
    x = np.array([-(r - drift[c]) for (c, d, f, r) in cases], dtype=float)
    absf = np.array([abs(f) for (c, d, f, r) in cases], dtype=float)
    days = pd.Series([d for (c, d, f, r) in cases])
    n_cases = int(len(x))
    n_days = int(days.nunique()) if n_cases else 0

    mean = float(np.mean(x)) if n_cases else None
    tval = None
    if n_cases and n_days >= 2:
        dev = pd.Series(x - mean).groupby(days.values).sum().values
        se = np.sqrt(n_days / (n_days - 1) * np.sum(dev ** 2)) / n_cases
        tval = float(mean / se) if se > 0 else None

    slope = None
    if n_cases >= 2 and np.unique(absf).size >= 2:
        slope = float(stats.linregress(absf, x).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"independent cases (days)": n_days, "cases": n_cases}
    mm = {"name": "mean sign-flipped 5-bar excess return on short-signal grid bars",
          "value": mean,
          "statistic": {"name": "t of the mean, cases of one day summed", "value": tval} if tval is not None else None,
          "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"}
    sc = {"name": "OLS slope of sign-flipped excess return on |forecast|", "value": slope, "passed": slope_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent cases (days), fewer than the 30 the plan requires."
    elif tval is None:
        status = "inconclusive"
        decided = "The main t could not be computed (zero dispersion), so neither rule is met."
    elif mean > 0 and tval >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The main mean is positive with t >= 2 and the supporting slope is above 0."
        else:
            status = "inconclusive"
            decided = "The main t >= 2 but the supporting slope is at or below 0, which the plan calls inconclusive."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2: the coin rises more than its drift after the short signal."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": mm,
        "supporting_check": sc,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
