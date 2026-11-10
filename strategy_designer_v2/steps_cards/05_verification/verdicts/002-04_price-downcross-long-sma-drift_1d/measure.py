import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    short_rets, short_fc, all_rets = [], [], []

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window].reset_index(drop=True)
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    short_rets.append(r)
                    short_fc.append(fc[t])

    short_rets = np.array(short_rets, dtype=float)
    short_fc = np.array(short_fc, dtype=float)
    all_rets = np.array(all_rets, dtype=float)
    n_short, n_all = len(short_rets), len(all_rets)

    diff_pp = None
    t_stat = None
    if n_short > 0 and n_all > 0:
        diff_pp = float((short_rets.mean() - all_rets.mean()) * 100.0)
    if n_short >= 2 and n_all >= 2:
        tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
        if np.isfinite(tt.statistic):
            t_stat = float(tt.statistic)

    hit_diff_pp = None
    if n_short > 0 and n_all > 0:
        hit_diff_pp = float(((short_rets < 0).mean() - (all_rets < 0).mean()) * 100.0)

    top_mean = None
    n_top = 0
    if n_short > 0:
        cut = np.quantile(short_fc, 1.0 / 3.0)
        mask = short_fc <= cut
        n_top = int(mask.sum())
        if n_top > 0:
            top_mean = float(short_rets[mask].mean())

    hit_pass = None if hit_diff_pp is None else bool(hit_diff_pp >= 10.0)

    if n_short < 15:
        status = "inconclusive"
        decided_by = "Fewer than 15 non-overlapping short cases pooled across windows, so the run is inconclusive whatever the numbers show."
    elif diff_pp is not None and diff_pp >= 0:
        status = "rejected"
        decided_by = "The difference is 0 or positive: price falls no further after short bars than after all bars."
    elif hit_diff_pp is not None and hit_diff_pp <= 0:
        status = "rejected"
        decided_by = "The hit rate on short bars is not above the unconditional share of negative 20-bar returns."
    elif top_mean is not None and top_mean > 0:
        status = "rejected"
        decided_by = "Mean forward return after the largest-tertile shorts is positive, indicating reversal."
    elif (diff_pp is not None and diff_pp <= -2.0 and t_stat is not None and t_stat <= -2.0
          and hit_diff_pp is not None and hit_diff_pp >= 10.0):
        status = "confirmed"
        decided_by = "The difference is at most -2 percentage points with t-stat at or below -2, and the short hit rate exceeds the unconditional share by at least 10 points."
    else:
        status = "inconclusive"
        decided_by = "The result lies between the confirm and reject lines."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar forward return on short bars minus mean over all bars (pp)",
            "value": diff_pp,
            "statistic": None if t_stat is None else {"name": "Welch t", "value": t_stat},
            "threshold": "confirm if at most -2 percentage points with t-stat at or below -2; reject if 0 or positive",
        },
        "supporting_check": {
            "name": "short-bar hit rate minus unconditional share of negative 20-bar returns (pp)",
            "value": hit_diff_pp,
            "passed": hit_pass,
        },
        "counts": {
            "non-overlapping short cases": int(n_short),
            "non-overlapping all-bar cases": int(n_all),
            "largest-tertile short cases": int(n_top),
        },
        "decided_by": decided_by,
        "reading": "Short bars are grid bars (positions 0, 20, 40, ... of each window with a full 20-bar forward return inside the window) whose forecast is below 0, the all-bars group is every such grid bar including the short ones, and the largest-tertile shorts are the pooled short cases whose forecast is at or below the 1/3 quantile of the short forecasts (the most negative third).",
    }
