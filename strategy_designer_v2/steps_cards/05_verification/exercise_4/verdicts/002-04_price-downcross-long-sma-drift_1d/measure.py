import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    short_rets = []
    short_fc = []
    all_rets = []

    for coin, windows in bars.items():
        for wname, df in windows.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0 or "close" not in df.columns or "forecast" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                f = fc[t]
                if np.isfinite(f) and f < 0:
                    short_rets.append(r)
                    short_fc.append(f)

    short_rets = np.array(short_rets, dtype=float)
    short_fc = np.array(short_fc, dtype=float)
    all_rets = np.array(all_rets, dtype=float)
    n_short = int(len(short_rets))
    n_all = int(len(all_rets))

    diff = None
    t_stat = None
    if n_short > 0 and n_all > 0:
        diff = float(short_rets.mean() - all_rets.mean())
        if n_short >= 2 and n_all >= 2:
            tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
            if np.isfinite(tt.statistic):
                t_stat = float(tt.statistic)

    hit_diff = None
    hit_short = hit_all = None
    if n_short > 0 and n_all > 0:
        hit_short = float(np.mean(short_rets < 0))
        hit_all = float(np.mean(all_rets < 0))
        hit_diff = hit_short - hit_all

    tert_mean = None
    n_tert = 0
    if n_short > 0:
        order = np.argsort(short_fc, kind="mergesort")  # most negative first
        n_tert = int(np.ceil(n_short / 3.0))
        tert_mean = float(short_rets[order[:n_tert]].mean())

    diff_pp = None if diff is None else diff * 100.0
    hit_pp = None if hit_diff is None else hit_diff * 100.0

    if n_short < 15:
        status = "inconclusive"
        decided_by = (f"Fewer than 15 non-overlapping short cases pooled across windows ({n_short}), "
                      "so the run is inconclusive whatever the numbers show.")
    elif diff is None or hit_diff is None:
        status = "inconclusive"
        decided_by = "The measures could not be computed, so the result is inconclusive."
    elif diff >= 0 or hit_diff <= 0 or (tert_mean is not None and tert_mean > 0):
        status = "rejected"
        reasons = []
        if diff >= 0:
            reasons.append("the difference is 0 or positive")
        if hit_diff <= 0:
            reasons.append("the short-bar hit rate is not above the unconditional share")
        if tert_mean is not None and tert_mean > 0:
            reasons.append("mean forward return after the largest-tertile shorts is positive")
        decided_by = "Reject: " + "; ".join(reasons) + "."
    elif diff <= -0.02 and t_stat is not None and t_stat <= -2 and hit_diff >= 0.10:
        status = "confirmed"
        decided_by = ("Confirm: the difference is at most -2 percentage points with Welch t at or below -2, "
                      "and the short-bar hit rate exceeds the unconditional share by at least 10 points.")
    else:
        status = "inconclusive"
        decided_by = "The result lies between the confirm and reject lines, so it is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar forward return on short bars minus on all bars (pp)",
            "value": diff_pp,
            "statistic": None if t_stat is None else {"name": "Welch t", "value": t_stat},
            "threshold": "confirm if at most -2 percentage points with t at or below -2; reject if 0 or positive",
        },
        "supporting_check": {
            "name": "hit rate of negative 20-bar returns, short bars minus all bars (pp)",
            "value": hit_pp,
            "passed": None if hit_diff is None else bool(hit_diff >= 0.10),
        },
        "counts": {
            "non-overlapping short cases": n_short,
            "non-overlapping all bars": n_all,
            "largest-tertile short cases": n_tert,
            "largest-tertile mean forward return (pp)": None if tert_mean is None else tert_mean * 100.0,
            "short-bar hit rate": hit_short,
            "all-bar hit rate": hit_all,
        },
        "decided_by": decided_by,
        "reading": ("Short bars are grid bars (positions 0, 20, 40, ... of each window, with a full 20-bar forward return "
                    "inside the window) whose forecast is below 0, compared against all grid bars of the same windows, "
                    "and the largest-tertile shorts are the ceil(n/3) short cases with the most negative forecast."),
    }
