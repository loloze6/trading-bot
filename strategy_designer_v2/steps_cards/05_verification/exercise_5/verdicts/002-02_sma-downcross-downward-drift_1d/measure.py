import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    short_rets, all_rets = [], []
    n_crosses = 0

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)

            # distinct downward crosses: forecast moving from >= 0 to < 0 inside the window
            for i in range(1, n):
                if np.isfinite(fc[i - 1]) and np.isfinite(fc[i]) and fc[i - 1] >= 0 and fc[i] < 0:
                    n_crosses += 1

            # non-overlapping 10-bar blocks at positions 0, 10, 20, ... of each window
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

    short_rets = np.array(short_rets, dtype=float)
    all_rets = np.array(all_rets, dtype=float)
    n_short, n_all = len(short_rets), len(all_rets)

    diff = None
    t_stat = None
    share_diff_pts = None
    if n_short > 0 and n_all > 0:
        diff = float(short_rets.mean() - all_rets.mean())
        share_short = float((short_rets < 0).mean())
        share_all = float((all_rets < 0).mean())
        share_diff_pts = (share_short - share_all) * 100.0
        if n_short >= 2 and n_all >= 2:
            tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
            if np.isfinite(tt.statistic):
                t_stat = float(tt.statistic)

    diff_pct = diff * 100.0 if diff is not None else None

    if n_short < 12 or n_crosses < 2 or diff is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 12 non-overlapping 10-bar short blocks or fewer than "
                      "2 distinct downward crosses across the windows.")
    elif diff >= 0 or share_diff_pts <= 0:
        status = "rejected"
        if diff >= 0:
            decided_by = "Rejected: the conditional-minus-unconditional 10-bar return difference is 0 or above."
        else:
            decided_by = "Rejected: the falling share on short bars is not above the unconditional share."
    elif (diff_pct <= -1.0 and t_stat is not None and t_stat <= -2.0 and share_diff_pts >= 10.0):
        status = "confirmed"
        decided_by = ("Confirmed: difference at most -1.0% per 10 bars, t-stat of -2 or lower, and the falling "
                      "share on short bars exceeds the unconditional share by at least 10 points.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the difference lies between -1.0% and 0, or its |t| is below 2, "
                      "or the falling-share gap is positive but under 10 points.")

    supporting_passed = None if share_diff_pts is None else bool(share_diff_pts >= 10.0)

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return on short bars minus mean over all bars (%)",
            "value": diff_pct,
            "statistic": None if t_stat is None else {"name": "Welch t", "value": t_stat},
            "threshold": "difference at most -1.0% per 10 bars with t-stat of -2 or lower",
        },
        "supporting_check": {
            "name": "falling share on short blocks minus falling share on all blocks (points)",
            "value": share_diff_pts,
            "passed": supporting_passed,
        },
        "counts": {
            "non-overlapping 10-bar short blocks": int(n_short),
            "non-overlapping 10-bar blocks, all bars": int(n_all),
            "distinct downward crosses": int(n_crosses),
        },
        "decided_by": decided_by,
        "reading": ("Short blocks are grid bars (positions 0,10,20,... per window, return needing t+10 in the same window) "
                    "with forecast < 0, compared by Welch t against all grid bars pooled over windows; a distinct downward "
                    "cross is a forecast moving from >= 0 to < 0 inside a window (a window opening already short is not "
                    "counted); reject rules are checked before confirm after the minimum-count gate."),
    }
