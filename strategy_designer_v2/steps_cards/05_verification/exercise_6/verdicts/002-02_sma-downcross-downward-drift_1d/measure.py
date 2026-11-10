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
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)

            # downward crosses: raw spread (SMA50 - SMA200)/SMA200 going from >= 0 to < 0 inside the window
            if spread_col in df.columns:
                sp = pd.to_numeric(df[spread_col], errors="coerce").values
            else:
                sp = fc
            prev = None
            for v in sp:
                if np.isnan(v):
                    continue
                if prev is not None and prev >= 0 and v < 0:
                    n_crosses += 1
                prev = v

            # non-overlapping grid: positions 0, H, 2H, ... from the window's first row
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if not np.isnan(fc[t]) and fc[t] < 0:
                    short_rets.append(r)

    short_rets = np.array(short_rets, dtype=float)
    all_rets = np.array(all_rets, dtype=float)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    diff = None
    t_stat = None
    share_diff_pts = None
    if n_short > 0 and n_all > 0:
        diff = float(short_rets.mean() - all_rets.mean())
        share_short = float((short_rets < 0).mean())
        share_all = float((all_rets < 0).mean())
        share_diff_pts = float((share_short - share_all) * 100.0)
        if n_short >= 2 and n_all >= 2:
            tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
            if np.isfinite(tt.statistic):
                t_stat = float(tt.statistic)

    support_passed = None if share_diff_pts is None else bool(share_diff_pts >= 10.0)

    if n_short < 12 or n_crosses < 2 or diff is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 12 non-overlapping 10-bar short blocks "
                      "or fewer than 2 distinct downward crosses across the windows.")
    elif diff >= 0 or share_diff_pts <= 0:
        status = "rejected"
        decided_by = ("Rejected: the conditional-minus-unconditional difference is 0 or above, "
                      "or the falling share on short bars is not above the unconditional share.")
    elif diff <= -0.01 and t_stat is not None and t_stat <= -2.0 and share_diff_pts >= 10.0:
        status = "confirmed"
        decided_by = ("Confirmed: difference at most -1.0% per 10 bars, t-stat of -2 or lower, "
                      "and falling share on short bars at least 10 points above the unconditional share.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: difference between -1.0% and 0, or |t| below 2, "
                      "or falling-share excess positive but below 10 points.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return on short bars minus mean over all bars (non-overlapping blocks)",
            "value": None if diff is None else diff * 100.0,
            "statistic": None if t_stat is None else {"name": "Welch t", "value": t_stat},
            "threshold": "at most -1.0% per 10 bars with t-stat of -2 or lower to confirm; 0 or above rejects",
        },
        "supporting_check": {
            "name": "falling share on short blocks minus falling share on all blocks (points)",
            "value": share_diff_pts,
            "passed": support_passed,
        },
        "counts": {
            "non-overlapping 10-bar short blocks": n_short,
            "non-overlapping 10-bar blocks (all bars)": n_all,
            "distinct downward crosses": int(n_crosses),
        },
        "decided_by": decided_by,
        "reading": ("Blocks are the bars at positions 0,10,20,... of each window with a full 10-bar forward return inside the window, short blocks are those whose bar has forecast < 0, the t-stat is Welch's t between short blocks and all blocks, the main measure is reported in percent, and a downward cross is counted each time the component's raw spread goes from >= 0 to < 0 within a window."),
    }
