import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    coin_key = None
    for k in bars.keys():
        if "BTC" in str(k).upper():
            coin_key = k
            break
    if coin_key is None and len(bars) > 0:
        coin_key = list(bars.keys())[0]

    all_rets, short_rets = [], []
    n_crosses = 0

    if coin_key is not None:
        windows = bars[coin_key]
        for w in sorted(windows.keys()):
            df = windows[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # distinct downward crosses: forecast moving from >= 0 to < 0 inside a window
            for i in range(1, n):
                if np.isfinite(fc[i - 1]) and np.isfinite(fc[i]) and fc[i - 1] >= 0 and fc[i] < 0:
                    n_crosses += 1

            # non-overlapping 10-bar blocks starting at the window's first bar
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    short_rets.append(r)

    all_rets = np.asarray(all_rets, dtype=float)
    short_rets = np.asarray(short_rets, dtype=float)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    diff = None
    tstat = None
    share_gap_pts = None
    sup_passed = None

    if n_short > 0 and n_all > 0:
        diff = float(short_rets.mean() - all_rets.mean())
        share_short = float((short_rets < 0).mean())
        share_all = float((all_rets < 0).mean())
        share_gap_pts = 100.0 * (share_short - share_all)
        sup_passed = bool(share_gap_pts >= 10.0)
        if n_short >= 2 and n_all >= 2:
            res = stats.ttest_ind(short_rets, all_rets, equal_var=False)
            tval = float(res.statistic)
            tstat = tval if np.isfinite(tval) else None

    threshold_txt = ("confirm if <= -1.0% per 10 bars with t <= -2 (Welch, non-overlapping blocks); "
                     "reject if >= 0; inconclusive in between or |t| < 2")

    if n_short < 12 or n_crosses < 2 or diff is None:
        status = "inconclusive"
        decided_by = (f"Inconclusive: fewer than 12 non-overlapping 10-bar short blocks ({n_short}) "
                      f"or fewer than 2 distinct downward crosses ({n_crosses}).")
    elif diff >= 0 or share_gap_pts <= 0:
        status = "rejected"
        decided_by = ("Rejected: the conditional-minus-unconditional difference is 0 or above, "
                      "or the falling share on short bars is not above the unconditional share.")
    elif diff <= -0.01 and tstat is not None and tstat <= -2.0 and share_gap_pts >= 10.0:
        status = "confirmed"
        decided_by = ("Confirmed: difference at most -1.0% per 10 bars, t-stat -2 or lower, and "
                      "falling share on short bars at least 10 points above the unconditional share.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: difference between -1.0% and 0, or |t| below 2, or falling-share "
                      "gap positive but below 10 points.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar fwd return on short blocks minus all blocks (pooled, %)",
            "value": None if diff is None else float(diff * 100.0),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "falling share on short blocks minus unconditional (points, need >= 10)",
            "value": None if share_gap_pts is None else float(share_gap_pts),
            "passed": sup_passed,
        },
        "cases": n_short,
        "decided_by": decided_by,
        "reading": ("Non-overlapping 10-bar blocks start at each window's first bar, a block is short when "
                    "the forecast at its start bar is below 0, the t-stat is Welch's t between short-block "
                    "and all-block returns, and a downward cross is a forecast move from >= 0 to < 0 inside a window."),
    }
