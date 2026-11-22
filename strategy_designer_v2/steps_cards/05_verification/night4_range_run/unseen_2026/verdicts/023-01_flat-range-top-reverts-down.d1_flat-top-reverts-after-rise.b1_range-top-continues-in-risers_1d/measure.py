import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RANGE_N = 30
    R90_N = 90
    RAW_COL = "debug_info.components.range_pos.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[RAW_COL], errors="coerce").values
                   if RAW_COL in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                # The regime: the 90-bar return is above 0. Use the prices when
                # 90 past closes exist in the window; otherwise the recorded regime.
                if t >= R90_N and close[t - R90_N] > 0:
                    trending = close[t] / close[t - R90_N] - 1.0 > 0.0
                else:
                    trending = regime[t] == "trending"
                if not trending:
                    continue
                # The expected side: above the middle of the last 30 closes (bar t
                # included) means long, below it means short.
                if t >= RANGE_N - 1:
                    win = close[t - RANGE_N + 1: t + 1]
                    hi, lo = np.max(win), np.min(win)
                    if hi > lo:
                        side = np.sign((close[t] - lo) / (hi - lo) - 0.5)
                    else:
                        side = 0.0
                else:
                    side = np.sign(raw[t]) if np.isfinite(raw[t]) else 0.0
                if side != 0 and np.sign(f) == side:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation check takes the 90-bar return from the prices where 90 past closes exist "
               "in the window and the recorded regime otherwise, and the side from the close's position in "
               "its last 30 closes (or the sign of the recorded raw value before 30 closes exist); the main "
               "measure uses the recorded regime == 'trending' on the grid bars 0,5,10,... of each window, "
               "trending grid bars with forecast 0 included, an OLS with intercept pooled over all coins, and "
               "the coin's mean 5-bar return from the same non-overlapping grid of all its windows; fewer than "
               "200 cases is reported as 'not observable'.")

    main_name = "OLS slope of demeaned 5-bar forward return on forecast, trending grid bars, pooled"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 200 independent grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent trending-regime grid cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the 90-bar return "
                           "is above 0 with the forecast's sign on the side of the close's position against the "
                           "middle of its 30-bar closing range (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all windows (non-overlapping grid)
        all_rets = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if regime[t] == "trending" and np.isfinite(fc[t]):
                    cases.append((fc[t], r))
        if not all_rets:
            continue
        mu = float(np.mean(all_rets))
        for f, r in cases:
            xs.append(float(f))
            ys.append(r - mu)

    n_cases = len(xs)
    slope = None
    tstat = None
    if n_cases >= 3:
        x = np.asarray(xs)
        y = np.asarray(ys)
        if np.std(x) > 0:
            res = stats.linregress(x, y)
            slope = float(res.slope)
            tstat = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    counts = {"independent trending-regime grid cases": int(n_cases)}

    if n_cases < 200:
        status = "not observable"
        decided = "Fewer than 200 independent trending-regime grid cases (%d), the plan's minimum." % n_cases
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 on at least 200 independent grid cases."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 200 independent grid cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
