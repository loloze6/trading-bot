import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    spread_col = "debug_info.components.sma_cross_down.last_history_value"

    short_rets, all_rets = [], []
    n_crosses = 0

    for coin in bars:
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # Non-overlapping grid: positions 0, H, 2H, ... with t+H inside the window
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

            # Distinct downward crosses: SMA50-SMA200 spread goes from >= 0 to < 0 inside the window
            if spread_col in df.columns:
                s = pd.to_numeric(df[spread_col], errors="coerce").to_numpy(dtype=float)
                for i in range(1, n):
                    if np.isfinite(s[i - 1]) and np.isfinite(s[i]) and s[i - 1] >= 0 and s[i] < 0:
                        n_crosses += 1

    short_rets = np.asarray(short_rets, dtype=float)
    all_rets = np.asarray(all_rets, dtype=float)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    diff = None
    t_stat = None
    if n_short > 0 and n_all > 0:
        diff = float(short_rets.mean() - all_rets.mean())
        if n_short >= 2 and n_all >= 2:
            tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
            t_stat = float(tt.statistic) if np.isfinite(tt.statistic) else None

    share_diff_pts = None
    share_short = share_all = None
    if n_short > 0 and n_all > 0:
        share_short = float(np.mean(short_rets < 0))
        share_all = float(np.mean(all_rets < 0))
        share_diff_pts = float((share_short - share_all) * 100.0)

    supp_passed = None if share_diff_pts is None else bool(share_diff_pts >= 10.0)

    # Decision
    if n_short < 12 or n_crosses < 2 or diff is None:
        status = "inconclusive"
        decided_by = (f"Inconclusive: {n_short} non-overlapping 10-bar short blocks (minimum 12) and "
                      f"{n_crosses} distinct downward crosses (minimum 2) fall below the plan's minimum counts.")
    elif diff >= 0 or (share_diff_pts is not None and share_diff_pts <= 0):
        status = "rejected"
        decided_by = ("Rejected: the short-minus-all difference is 0 or above, or the falling share on short bars "
                      "is not above the unconditional share.")
    elif (diff <= -0.01 and t_stat is not None and t_stat <= -2.0
          and share_diff_pts is not None and share_diff_pts >= 10.0):
        status = "confirmed"
        decided_by = ("Confirmed: the difference is at most -1.0% per 10 bars, its t-stat is -2 or lower, and the "
                      "falling share on short bars exceeds the unconditional share by at least 10 points.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the difference is negative but not all confirm conditions hold "
                      "(difference between -1.0% and 0, |t| below 2, or falling-share edge below 10 points).")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return on short bars minus mean over all bars (%)",
            "value": None if diff is None else diff * 100.0,
            "statistic": None if t_stat is None else {"name": "Welch t", "value": t_stat},
            "threshold": "difference at most -1.0% per 10 bars with t-stat -2 or lower; 0 or above rejects",
        },
        "supporting_check": {
            "name": "falling share on short blocks minus falling share on all blocks (points)",
            "value": share_diff_pts,
            "passed": supp_passed,
        },
        "counts": {
            "non-overlapping 10-bar short blocks": n_short,
            "non-overlapping 10-bar blocks, all bars": n_all,
            "distinct downward crosses": int(n_crosses),
        },
        "decided_by": decided_by,
        "reading": ("Short blocks are grid bars (positions 0,10,20,... of each window with t+10 inside the window) "
                    "with forecast < 0, compared by Welch t against all grid bars, and a downward cross is counted "
                    "each time the raw SMA50-SMA200 spread (last_history_value) goes from >= 0 to < 0 inside a "
                    "window; the minimum counts are checked first, then the reject rule, then the confirm rule."),
    }
