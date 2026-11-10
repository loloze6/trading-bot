import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_BLOCKS = 15
    MIN_UPCROSSES = 8

    in_pos_rets = []        # non-overlapping grid bars with forecast > 0
    all_grid_rets = []      # non-overlapping grid bars, all
    upcross_rets = []       # forward 20-bar returns after each up-cross
    uncond_rets = []        # all bars' 20-bar forward returns (unconditional share)

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # non-overlapping grid: positions 0, H, 2H, ... from the window's first row
            for i in range(0, n, H):
                r = fwd[i]
                if not np.isfinite(r):
                    continue
                all_grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    in_pos_rets.append(r)

            # unconditional share: every bar with a valid 20-bar forward return
            for i in range(n):
                if np.isfinite(fwd[i]):
                    uncond_rets.append(fwd[i])

            # up-crosses: forecast goes from 0 (<= 0) on the previous bar to > 0, same window
            for i in range(1, n):
                if (np.isfinite(fc[i - 1]) and np.isfinite(fc[i])
                        and fc[i - 1] <= 0 and fc[i] > 0 and np.isfinite(fwd[i])):
                    upcross_rets.append(fwd[i])

    in_pos = np.array(in_pos_rets, dtype=float)
    allg = np.array(all_grid_rets, dtype=float)
    upc = np.array(upcross_rets, dtype=float)
    unc = np.array(uncond_rets, dtype=float)

    n_blocks = int(len(in_pos))
    n_up = int(len(upc))

    diff = None
    t_val = None
    if len(in_pos) > 0 and len(allg) > 0:
        diff = float(in_pos.mean() - allg.mean())
    if len(in_pos) >= 2 and len(allg) >= 2:
        t = stats.ttest_ind(in_pos, allg, equal_var=False).statistic
        t_val = float(t) if np.isfinite(t) else None

    up_share = float((upc > 0).mean()) if n_up > 0 else None
    unc_share = float((unc > 0).mean()) if len(unc) > 0 else None
    up_mean = float(upc.mean()) if n_up > 0 else None
    share_diff = (up_share - unc_share) if (up_share is not None and unc_share is not None) else None
    support_passed = (share_diff > 0) if share_diff is not None else None

    if n_blocks < MIN_BLOCKS or n_up < MIN_UPCROSSES or diff is None:
        status = "inconclusive"
        decided_by = (f"Fewer than the required {MIN_BLOCKS} non-overlapping in-position blocks "
                      f"or {MIN_UPCROSSES} up-crosses (have {n_blocks} and {n_up}), so the test neither confirms nor rejects.")
    elif diff <= 0 or (up_mean is not None and up_mean < 0):
        status = "rejected"
        if diff <= 0:
            decided_by = "Reject: the in-position minus all-bars difference is <= 0."
        else:
            decided_by = "Reject: the 20-bar forward returns after up-crosses are on average negative (reversal)."
    elif t_val is not None and t_val >= 2 and support_passed:
        status = "confirmed"
        decided_by = ("Confirm: the in-position minus all-bars difference is above 0 with t >= 2, and the share of "
                      "up-crosses followed by a positive 20-bar return exceeds the unconditional share.")
    else:
        status = "inconclusive"
        if t_val is None or t_val < 2:
            decided_by = "Inconclusive: a positive difference with t < 2."
        else:
            decided_by = ("Inconclusive: the main measure and the supporting check disagree "
                          "(up-cross positive share does not exceed the unconditional share).")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar fwd return with forecast > 0 minus mean over all bars (non-overlapping)",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t_val} if t_val is not None else None,
            "threshold": "difference above 0 with t >= 2",
        },
        "supporting_check": {
            "name": "up-cross positive 20-bar return share minus unconditional positive share",
            "value": share_diff,
            "passed": support_passed,
        },
        "counts": {
            "non-overlapping in-position blocks": n_blocks,
            "up-crosses": n_up,
            "non-overlapping all-bars blocks": int(len(allg)),
        },
        "decided_by": decided_by,
        "reading": ("In-position and all-bars groups share one grid per window at rows 0,20,40,... compared by Welch t; "
                    "an up-cross is a bar with forecast > 0 whose previous bar in the same window has forecast <= 0, "
                    "counted only when its 20-bar forward return exists; the unconditional share uses every bar's "
                    "20-bar forward return within each window; a reversal means the mean up-cross forward return is below 0."),
    }
