import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    short_r, short_f, all_r = [], [], []

    coins = [c for c in bars.keys() if "BTC" in str(c).upper()]
    for coin in coins:
        for window, df in bars[coin].items():
            if df is None or len(df) == 0:
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
                all_r.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    short_r.append(r)
                    short_f.append(fc[t])

    short_r = np.array(short_r, dtype=float)
    short_f = np.array(short_f, dtype=float)
    all_r = np.array(all_r, dtype=float)
    n_short = int(len(short_r))
    n_all = int(len(all_r))

    diff = None
    t_stat = None
    hit_short = hit_all = hit_diff = None
    top_mean = None
    n_top = 0

    if n_short > 0 and n_all > 0:
        diff = float(short_r.mean() - all_r.mean())
        hit_short = float(np.mean(short_r < 0))
        hit_all = float(np.mean(all_r < 0))
        hit_diff = hit_short - hit_all
        # largest-tertile shorts: the third of short cases with the most negative forecast
        n_top = int(np.ceil(n_short / 3.0))
        order = np.argsort(short_f, kind="mergesort")
        top_mean = float(short_r[order[:n_top]].mean())
    if n_short >= 2 and n_all >= 2:
        tt = stats.ttest_ind(short_r, all_r, equal_var=False)
        if np.isfinite(tt.statistic):
            t_stat = float(tt.statistic)

    diff_pp = None if diff is None else diff * 100.0
    hit_diff_pts = None if hit_diff is None else hit_diff * 100.0

    supp_passed = None if hit_diff is None else bool(hit_diff >= 0.10 - 1e-12)

    if n_short < 15:
        status = "inconclusive"
        decided_by = (f"Fewer than 15 non-overlapping short cases pooled across windows ({n_short}), "
                      "so the run is inconclusive whatever the numbers show.")
    else:
        reject_reasons = []
        if diff >= 0:
            reject_reasons.append("the difference is 0 or positive")
        if hit_diff <= 0:
            reject_reasons.append("the short hit rate is not above the unconditional share")
        if top_mean is not None and top_mean > 0:
            reject_reasons.append("mean forward return after the largest-tertile shorts is positive (reversal)")
        if reject_reasons:
            status = "rejected"
            decided_by = "Reject rule met: " + "; ".join(reject_reasons) + "."
        elif (diff <= -0.02 + 1e-12 and t_stat is not None and t_stat <= -2
              and hit_diff >= 0.10 - 1e-12):
            status = "confirmed"
            decided_by = ("Confirm rule met: difference at most -2 percentage points with t-stat at or below -2, "
                          "and short hit rate exceeds the unconditional share by at least 10 points.")
        else:
            status = "inconclusive"
            decided_by = "The result lies between the confirm and reject lines, so it is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar forward return on short bars minus on all bars (pp)",
            "value": diff_pp,
            "statistic": None if t_stat is None else {"name": "Welch t", "value": t_stat},
            "threshold": "confirm if at most -2 percentage points with t-stat at or below -2; reject if 0 or positive",
        },
        "supporting_check": {
            "name": "short-bar hit rate minus unconditional share of negative 20-bar returns (points)",
            "value": hit_diff_pts,
            "passed": supp_passed,
        },
        "counts": {
            "non-overlapping short cases": n_short,
            "non-overlapping all-bar cases": n_all,
            "largest-tertile short cases": int(n_top),
        },
        "decided_by": decided_by,
        "reading": ("Short bars are non-overlapping grid bars (positions 0, 20, 40, ... of each window, with a full 20-bar "
                    "forward return inside the window) whose forecast is below 0, compared with all grid bars of the same "
                    "windows via Welch t; the largest-tertile shorts are the ceil(n/3) short cases with the most negative "
                    "forecast, and the fewer-than-15 rule is applied before the confirm and reject rules."),
    }
