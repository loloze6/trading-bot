import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_BLOCKS = 15
    MIN_CROSSES = 8

    all_grid = []      # non-overlapping 20-bar returns, all grid bars
    in_grid = []       # non-overlapping 20-bar returns, grid bars with forecast > 0
    cross_rets = []    # 20-bar forward returns after each up-cross
    uncond_rets = []   # every bar's 20-bar forward return (unconditional share)

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # forward 20-bar return inside this window only
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # unconditional: all bars with a valid forward return
            for t in range(n):
                if np.isfinite(fwd[t]):
                    uncond_rets.append(fwd[t])

            # non-overlapping grid: positions 0, 20, 40, ... from the window's first row
            for t in range(0, n, H):
                if not np.isfinite(fwd[t]):
                    continue
                all_grid.append(fwd[t])
                if np.isfinite(fc[t]) and fc[t] > 0:
                    in_grid.append(fwd[t])

            # up-crosses: forecast goes from 0 (or below) to > 0 within the window
            for t in range(1, n):
                if not (np.isfinite(fc[t]) and np.isfinite(fc[t - 1])):
                    continue
                if fc[t - 1] <= 0 and fc[t] > 0 and np.isfinite(fwd[t]):
                    cross_rets.append(fwd[t])

    all_grid = np.asarray(all_grid, dtype=float)
    in_grid = np.asarray(in_grid, dtype=float)
    cross_rets = np.asarray(cross_rets, dtype=float)
    uncond_rets = np.asarray(uncond_rets, dtype=float)

    n_in = int(len(in_grid))
    n_all = int(len(all_grid))
    n_cross = int(len(cross_rets))

    diff = None
    t_stat = None
    if n_in > 0 and n_all > 0:
        diff = float(np.mean(in_grid) - np.mean(all_grid))
        if n_in >= 2 and n_all >= 2:
            res = stats.ttest_ind(in_grid, all_grid, equal_var=False)
            if np.isfinite(res.statistic):
                t_stat = float(res.statistic)

    cross_share = float(np.mean(cross_rets > 0)) if n_cross > 0 else None
    uncond_share = float(np.mean(uncond_rets > 0)) if len(uncond_rets) > 0 else None
    cross_mean = float(np.mean(cross_rets)) if n_cross > 0 else None
    share_gap = (cross_share - uncond_share) if (cross_share is not None and uncond_share is not None) else None
    support_passed = (share_gap > 0) if share_gap is not None else None

    if n_in < MIN_BLOCKS or n_cross < MIN_CROSSES or diff is None:
        status = "inconclusive"
        decided_by = (f"Fewer than the required minimums ({n_in} in-position non-overlapping blocks vs 15, "
                      f"{n_cross} up-crosses vs 8), so the test neither confirms nor rejects.")
    elif diff <= 0:
        status = "rejected"
        decided_by = "Reject: the in-position minus all-bars difference in mean 20-bar forward return is <= 0."
    elif cross_mean is not None and cross_mean < 0:
        status = "rejected"
        decided_by = "Reject: the 20-bar forward returns after up-crosses are on average negative (reversal)."
    elif t_stat is not None and t_stat >= 2 and support_passed:
        status = "confirmed"
        decided_by = ("Confirm: the difference is above 0 with t >= 2 and the share of up-crosses followed by a "
                      "positive 20-bar return exceeds the unconditional share.")
    elif t_stat is None or t_stat < 2:
        status = "inconclusive"
        decided_by = "Inconclusive: a positive difference with t < 2."
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the main measure (positive, t >= 2) and the supporting check "
                      "(up-cross share not above the unconditional share) disagree.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar fwd return in-position minus all bars (non-overlapping)",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t_stat} if t_stat is not None else None),
            "threshold": "difference above 0 with t >= 2 to confirm; difference <= 0 rejects",
        },
        "supporting_check": {
            "name": "up-cross positive 20-bar share minus unconditional share",
            "value": share_gap,
            "passed": support_passed,
        },
        "counts": {
            "non-overlapping in-position blocks": n_in,
            "up-crosses": n_cross,
        },
        "decided_by": decided_by,
        "reading": ("Pooled all windows of every coin present, used the 0,20,40,... grid per window for both groups "
                    "with Welch t, counted an up-cross as a bar with forecast > 0 after a bar with forecast <= 0 inside "
                    "the same window that has a full 20-bar forward return, took the unconditional share over every "
                    "bar with a valid 20-bar forward return, and applied the minimum counts first, then reject, then "
                    "confirm."),
    }
