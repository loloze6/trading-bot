import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    short_rets = []
    all_rets = []
    n_crosses = 0

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # Distinct downward crosses: forecast moves from >= 0 to < 0 inside the window
            for i in range(1, n):
                a, b = fc[i - 1], fc[i]
                if np.isfinite(a) and np.isfinite(b) and a >= 0 and b < 0:
                    n_crosses += 1

            # Non-overlapping grid: positions 0, H, 2H, ... with a forward return inside the window
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    short_rets.append(r)

    short_rets = np.asarray(short_rets, dtype=float)
    all_rets = np.asarray(all_rets, dtype=float)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    diff_pct = None
    t_stat = None
    share_diff_pts = None
    if n_short > 0 and n_all > 0:
        diff_pct = float((short_rets.mean() - all_rets.mean()) * 100.0)
        share_short = float((short_rets < 0).mean() * 100.0)
        share_all = float((all_rets < 0).mean() * 100.0)
        share_diff_pts = share_short - share_all
    if n_short >= 2 and n_all >= 2:
        tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
        if np.isfinite(tt.statistic):
            t_stat = float(tt.statistic)

    counts = {
        "non-overlapping 10-bar short blocks": n_short,
        "non-overlapping 10-bar blocks (all bars)": n_all,
        "distinct downward crosses": int(n_crosses),
    }

    support_passed = None if share_diff_pts is None else bool(share_diff_pts >= 10.0)

    if n_short < 12 or n_crosses < 2:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 12 non-overlapping 10-bar short blocks or fewer than 2 "
                      "distinct downward crosses across the windows.")
    elif diff_pct is None or share_diff_pts is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the measures could not be computed."
    elif (diff_pct <= -1.0 and t_stat is not None and t_stat <= -2.0 and share_diff_pts >= 10.0):
        status = "confirmed"
        decided_by = ("Confirmed: the difference is at most -1.0% per 10 bars, its t-stat is -2 or lower, "
                      "and the falling share on short bars exceeds the unconditional share by at least 10 points.")
    elif diff_pct >= 0.0 or share_diff_pts <= 0.0:
        status = "rejected"
        decided_by = ("Rejected: the difference is 0 or above, or the falling share on short bars is not "
                      "above the unconditional share.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the difference lies between -1.0% and 0, or its |t| is below 2, "
                      "or the falling-share gap is positive but under 10 points.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return on short bars minus mean over all bars",
            "value": diff_pct,
            "statistic": None if t_stat is None else {"name": "Welch t", "value": t_stat},
            "threshold": "at most -1.0% per 10 bars with t-stat of -2 or lower",
        },
        "supporting_check": {
            "name": "falling share on short blocks minus unconditional falling share (points)",
            "value": share_diff_pts,
            "passed": support_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Blocks are the bars at positions 0, 10, 20, ... of each window with a forward return inside "
                    "the window, short blocks are those with forecast < 0 at the block start, the difference is in "
                    "percent and tested with Welch's t against all blocks, and a distinct downward cross is a move "
                    "of the forecast from >= 0 to < 0 between consecutive bars inside a window; the minimum counts "
                    "are checked first, then confirm, then reject, else inconclusive."),
    }
