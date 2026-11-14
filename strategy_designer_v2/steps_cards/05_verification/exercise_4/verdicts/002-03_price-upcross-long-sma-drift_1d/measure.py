import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    grid_all = []        # non-overlapping 20-bar forward returns, all grid bars
    grid_in = []         # non-overlapping 20-bar forward returns, grid bars with forecast > 0
    cross_rets = []      # 20-bar forward returns after each up-cross
    uncond_rets = []     # all bars' 20-bar forward returns (unconditional)

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

            # non-overlapping grid: positions 0, H, 2H, ... of the window
            for i in range(0, n, H):
                r = fwd[i]
                if not np.isfinite(r) or not np.isfinite(fc[i]):
                    continue
                grid_all.append(r)
                if fc[i] > 0:
                    grid_in.append(r)

            # unconditional share: every bar with a valid forward return
            for i in range(n):
                if np.isfinite(fwd[i]):
                    uncond_rets.append(fwd[i])

            # up-crosses: forecast goes from 0 (<= 0) to > 0, inside the window
            for i in range(1, n):
                if np.isfinite(fc[i - 1]) and np.isfinite(fc[i]) and fc[i - 1] <= 0 and fc[i] > 0:
                    if np.isfinite(fwd[i]):
                        cross_rets.append(fwd[i])

    grid_all = np.array(grid_all, dtype=float)
    grid_in = np.array(grid_in, dtype=float)
    cross_rets = np.array(cross_rets, dtype=float)
    uncond_rets = np.array(uncond_rets, dtype=float)

    n_in = int(len(grid_in))
    n_all = int(len(grid_all))
    n_cross = int(len(cross_rets))

    diff = None
    t_val = None
    if n_in > 0 and n_all > 0:
        diff = float(grid_in.mean() - grid_all.mean())
    if n_in >= 2 and n_all >= 2:
        t = stats.ttest_ind(grid_in, grid_all, equal_var=False).statistic
        if np.isfinite(t):
            t_val = float(t)

    share_cross = float((cross_rets > 0).mean()) if n_cross > 0 else None
    share_uncond = float((uncond_rets > 0).mean()) if len(uncond_rets) > 0 else None
    mean_cross = float(cross_rets.mean()) if n_cross > 0 else None
    sup_passed = None
    if share_cross is not None and share_uncond is not None:
        sup_passed = bool(share_cross > share_uncond)

    if n_in < 15 or n_cross < 8:
        status = "inconclusive"
        decided_by = ("Fewer than 15 non-overlapping in-position blocks or fewer than 8 up-crosses, "
                      "so the test neither confirms nor rejects.")
    elif diff is None:
        status = "inconclusive"
        decided_by = "The main measure could not be computed."
    elif diff <= 0 or (mean_cross is not None and mean_cross < 0):
        status = "rejected"
        if diff <= 0:
            decided_by = "The in-position minus all-bars difference is <= 0."
        else:
            decided_by = "The 20-bar forward returns after up-crosses are on average negative (reversal)."
    elif t_val is not None and t_val >= 2 and sup_passed is True:
        status = "confirmed"
        decided_by = ("The difference is above 0 with t >= 2 and the share of up-crosses followed by a "
                      "positive 20-bar return exceeds the unconditional share.")
    else:
        status = "inconclusive"
        if t_val is None or t_val < 2:
            decided_by = "A positive difference with t < 2."
        else:
            decided_by = "The main measure and the supporting check disagree."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar fwd return in position minus all bars",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t_val} if t_val is not None else None),
            "threshold": "difference above 0 with t >= 2",
        },
        "supporting_check": {
            "name": "share of positive 20-bar returns after up-crosses minus unconditional share",
            "value": (share_cross - share_uncond) if (share_cross is not None and share_uncond is not None) else None,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping in-position blocks": n_in,
            "non-overlapping all-bars blocks": n_all,
            "up-crosses": n_cross,
            "mean 20-bar return after up-crosses": mean_cross,
            "share positive after up-crosses": share_cross,
            "unconditional share positive": share_uncond,
        },
        "decided_by": decided_by,
        "reading": ("Blocks are the bars at positions 0, 20, 40, ... of each window, with in-position meaning forecast > 0 "
                    "on the block's first bar, compared by Welch t against all grid bars. An up-cross is a bar with "
                    "forecast > 0 whose previous bar in the same window has forecast <= 0, counted only when it has a full "
                    "20-bar forward return. The unconditional share uses every bar with a valid 20-bar forward return."),
    }
