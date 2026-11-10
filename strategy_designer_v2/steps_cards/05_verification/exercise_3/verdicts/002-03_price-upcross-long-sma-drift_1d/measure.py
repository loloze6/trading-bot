import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_BLOCKS = 15
    MIN_CROSSES = 8

    all_rets = []      # non-overlapping 20-bar forward returns, all grid bars
    pos_rets = []      # same grid, bars with forecast > 0
    cross_rets = []    # 20-bar forward returns after each up-cross

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # Non-overlapping grid: positions 0, H, 2H, ... from the window's first row
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1, f = close[i], close[j], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                if not np.isfinite(f):
                    continue
                all_rets.append(r)
                if f > 0:
                    pos_rets.append(r)

            # Up-crosses: forecast goes from 0 (<= 0) on the prior bar to > 0, same window
            for i in range(1, n):
                fp, f = fc[i - 1], fc[i]
                if not (np.isfinite(fp) and np.isfinite(f)):
                    continue
                if fp <= 0 and f > 0:
                    j = i + H
                    if j >= n:
                        continue
                    c0, c1 = close[i], close[j]
                    if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                        continue
                    cross_rets.append(c1 / c0 - 1.0)

    all_rets = np.asarray(all_rets, dtype=float)
    pos_rets = np.asarray(pos_rets, dtype=float)
    cross_rets = np.asarray(cross_rets, dtype=float)

    n_all = int(len(all_rets))
    n_pos = int(len(pos_rets))
    n_cross = int(len(cross_rets))

    mean_all = float(np.mean(all_rets)) if n_all > 0 else None
    mean_pos = float(np.mean(pos_rets)) if n_pos > 0 else None
    diff = (mean_pos - mean_all) if (mean_pos is not None and mean_all is not None) else None

    t_val = None
    if n_pos >= 2 and n_all >= 2:
        t_res = stats.ttest_ind(pos_rets, all_rets, equal_var=False)
        tv = float(t_res.statistic)
        t_val = tv if np.isfinite(tv) else None

    share_cross = float(np.mean(cross_rets > 0)) if n_cross > 0 else None
    share_uncond = float(np.mean(all_rets > 0)) if n_all > 0 else None
    mean_cross = float(np.mean(cross_rets)) if n_cross > 0 else None

    support_passed = None
    support_value = None
    if share_cross is not None and share_uncond is not None:
        support_value = share_cross - share_uncond
        support_passed = bool(share_cross > share_uncond)

    counts = {
        "non-overlapping in-position blocks": n_pos,
        "up-crosses": n_cross,
        "non-overlapping all-bars blocks": n_all,
    }

    if n_pos < MIN_BLOCKS or n_cross < MIN_CROSSES or diff is None:
        status = "inconclusive"
        decided_by = ("Fewer than 15 non-overlapping in-position blocks or fewer than 8 up-crosses, "
                      "so the test neither confirms nor rejects.")
    elif diff <= 0:
        status = "rejected"
        decided_by = "The in-position minus all-bars difference is <= 0."
    elif mean_cross is not None and mean_cross < 0:
        status = "rejected"
        decided_by = "The 20-bar forward returns after up-crosses are on average negative (reversal)."
    elif t_val is not None and t_val >= 2 and support_passed is True:
        status = "confirmed"
        decided_by = ("The difference is above 0 with t >= 2 and the share of up-crosses followed by a "
                      "positive 20-bar return exceeds the unconditional share.")
    elif t_val is None or t_val < 2:
        status = "inconclusive"
        decided_by = "A positive difference with t < 2."
    else:
        status = "inconclusive"
        decided_by = "Main measure (positive, t >= 2) and supporting check disagree."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar fwd return, forecast>0 minus all bars",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t_val} if t_val is not None else None),
            "threshold": "difference > 0 with t >= 2 across non-overlapping 20-bar blocks",
        },
        "supporting_check": {
            "name": "share positive 20-bar returns after up-crosses minus unconditional share",
            "value": support_value,
            "passed": support_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Up-crosses are bars with forecast > 0 whose prior bar in the same window had forecast <= 0, "
                    "each with its own 20-bar forward return (overlap allowed); the unconditional share of positive "
                    "returns and the all-bars mean use the same non-overlapping grid (positions 0, 20, 40, ... per "
                    "window); the t is Welch's between in-position and all-bars blocks; the reversal reject is "
                    "checked before the confirm rule."),
    }
