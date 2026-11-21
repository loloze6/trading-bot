import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.grind.last_history_value"

    # ---------- 1. Situation check: past 72-bar rise (from close), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            past = np.full(len(close), np.nan)
            if len(close) > H:
                past[H:] = close[H:] / close[:-H] - 1.0
            active = np.isfinite(fc) & (fc != 0) & np.isfinite(past)
            n_active += int(active.sum())
            n_agree += int((active & (past > 0) & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "pooled OLS slope of next-72-bar excess return on raw residual, risen grid bars"
    threshold = "confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; else inconclusive; at least 200 risen grid cases"
    reading = ("Active bars in each window's first 72 rows (no past 72-bar return computable from the record) are left out "
               "of the situation check; the grid is positions 0, 72, 144, ... of each window, so position 0 has no past return and drops out; "
               "the coin's mean 72-bar return is the mean of all its grid forward returns over all windows; the slope's t is the ordinary OLS "
               "t (slope / standard error); fewer than 200 risen grid cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of active forecast bars are long bars following a positive 72-bar return, "
                           "so the config does not trade the plan's situation (risen coin, long only)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin mean 72-bar return over all windows (non-overlapping grid)
        all_fwd = []
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(close), np.nan)
            n = len(close)
            for t in range(0, n, H):
                fwd = close[t + H] / close[t] - 1.0 if t + H < n else np.nan
                if np.isfinite(fwd):
                    all_fwd.append(fwd)
                past = close[t] / close[t - H] - 1.0 if t - H >= 0 else np.nan
                rows.append((past, fwd, raw[t]))
        if len(all_fwd) == 0:
            continue
        mu = float(np.mean(all_fwd))
        for past, fwd, r in rows:
            if np.isfinite(past) and past > 0 and np.isfinite(fwd) and np.isfinite(r):
                xs.append(r)
                ys.append(fwd - mu)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))
    counts = {"risen grid cases pooled across coins": n_cases}

    slope, tval = None, None
    if n_cases >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    if n_cases < 200:
        status = "not observable"
        decided_by = f"Only {n_cases} risen grid cases pooled across coins, below the plan's minimum of 200."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no variation in the raw residual), so neither rule is met."
    elif slope > 0 and tval >= 2.0:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2.0: the future excess rise grows as the top-3 share falls."
    elif slope < 0 and tval <= -2.0:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2.0."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2.0 and 2.0."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
