import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 200
    PCOL = "debug_info.components.calm.post_pipeline_value"

    # ---------- 1. situation check: 28-day return < 0, short side ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for win in sorted(bars[coin]):
            df = bars[coin][win].reset_index(drop=True)
            if df.empty:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            n = len(df)
            ret28 = np.full(n, np.nan)
            if n > 28:
                ret28[28:] = close[28:] / close[:-28] - 1.0
            for i in range(n):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                if not np.isfinite(ret28[i]):
                    continue  # 28-day return not computable inside the window
                n_active += 1
                if ret28[i] < 0 and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation check counts only active bars whose 28-day return can be computed from the window's own "
               "closes (the first 28 bars of each window are left out), side short when forecast < 0; grid cases are "
               "bars at positions 0,5,10,... of each window with regime 'trending', a finite 5-bar forward return "
               "inside the window and a recorded calm post_pipeline_value, the coin's drift being the mean 5-bar "
               "return over all its windows' grid bars, the slope's t from ordinary least squares, and fewer than "
               "200 cases gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars with a negative 28-day return carrying a "
                           "short forecast, so the config does not trade the plan's falling-coin situation on the "
                           "short side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin in sorted(bars):
        grid_all = []
        cases = []
        for win in sorted(bars[coin]):
            df = bars[coin][win].reset_index(drop=True)
            n = len(df)
            if n <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            reg = df["regime"].astype(str).values
            post = (pd.to_numeric(df[PCOL], errors="coerce").values.astype(float)
                    if PCOL in df.columns else np.full(n, np.nan))
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_all.append(r)
                if reg[i] == "trending" and np.isfinite(post[i]):
                    cases.append((r, abs(post[i])))
        if not grid_all:
            continue
        drift = float(np.mean(grid_all))
        for r, w in cases:
            ys.append(r - drift)
            xs.append(w)

    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    n_cases = int(len(xs))

    slope = None
    t_val = None
    if n_cases >= 3 and np.ptp(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    sw = float(np.sum(xs)) if n_cases else 0.0
    wmean = float(np.sum(xs * ys) / sw) if sw > 0 else None
    sup_pass = bool(wmean < 0) if wmean is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases in the 'trending' regime, fewer than the 200 the plan requires."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and t_val <= -2:
        if sup_pass:
            status = "confirmed"
            decided = ("The slope is negative with t <= -2 and the abs-forecast-weighted drift-adjusted 5-bar "
                       "return is below 0, meeting the confirm rule.")
        else:
            status = "inconclusive"
            decided = ("The slope is negative with t <= -2 but the weighted drift-adjusted return is not below 0, "
                       "a confirming slope whose supporting check fails.")
    elif slope > 0 and t_val >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2, meeting the reject rule."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2, the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of drift-adjusted 5-bar return on abs forecast (trending grid bars)",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_val} if t_val is not None else None),
            "threshold": "confirm: slope negative with t <= -2 (and supporting check passes); reject: slope positive with t >= +2",
        },
        "supporting_check": {
            "name": "abs-forecast-weighted mean drift-adjusted 5-bar return below 0",
            "value": wmean,
            "passed": sup_pass,
        },
        "counts": {"grid cases in the regime": n_cases, "active bars checked": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
