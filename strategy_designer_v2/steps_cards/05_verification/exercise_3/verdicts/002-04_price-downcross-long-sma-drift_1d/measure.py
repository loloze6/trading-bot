import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    short_rets, short_fc, all_rets = [], [], []
    windows_used = 0

    for coin, wins in bars.items():
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            windows_used += 1
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
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

    diff_pp = None
    t_stat = None
    if n_short > 0 and n_all > 0:
        diff_pp = float((short_rets.mean() - all_rets.mean()) * 100.0)
    if n_short >= 2 and n_all >= 2:
        tt = stats.ttest_ind(short_rets, all_rets, equal_var=False)
        t_stat = float(tt.statistic) if np.isfinite(tt.statistic) else None

    hit_short = float(np.mean(short_rets < 0)) if n_short > 0 else None
    hit_all = float(np.mean(all_rets < 0)) if n_all > 0 else None
    hit_diff_pp = (hit_short - hit_all) * 100.0 if (hit_short is not None and hit_all is not None) else None

    # Largest-tertile shorts: the most negative third of short-case forecasts
    tert_mean = None
    n_tert = 0
    if n_short > 0:
        n_tert = int(np.ceil(n_short / 3.0))
        order = np.argsort(short_fc, kind="mergesort")  # most negative first
        tert_mean = float(short_rets[order[:n_tert]].mean())

    if n_short < 15:
        status = "inconclusive"
        decided_by = f"Fewer than 15 non-overlapping short cases pooled across windows ({n_short}), so the run is inconclusive whatever the numbers show."
    else:
        reasons = []
        if diff_pp is not None and diff_pp >= 0:
            reasons.append("the short-minus-all difference is 0 or positive")
        if hit_diff_pp is not None and hit_diff_pp <= 0:
            reasons.append("the short-bar hit rate is not above the unconditional share")
        if tert_mean is not None and tert_mean > 0:
            reasons.append("mean forward return after largest-tertile shorts is positive")
        if reasons:
            status = "rejected"
            decided_by = "Reject: " + "; ".join(reasons) + "."
        elif (diff_pp is not None and diff_pp <= -2.0 and t_stat is not None and t_stat <= -2.0
              and hit_diff_pp is not None and hit_diff_pp >= 10.0):
            status = "confirmed"
            decided_by = "Confirm: difference at most -2 pp with Welch t at or below -2, and short-bar hit rate exceeds the unconditional share by at least 10 points."
        else:
            status = "inconclusive"
            decided_by = "The result lies between the confirm and reject lines, so it is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 20-bar forward return on short bars minus on all bars (pp)",
            "value": diff_pp,
            "statistic": {"name": "Welch t", "value": t_stat} if t_stat is not None else None,
            "threshold": "confirm if difference <= -2 percentage points with t <= -2; reject if difference >= 0",
        },
        "supporting_check": {
            "name": "hit rate on short bars minus unconditional share of negative 20-bar returns (pp)",
            "value": hit_diff_pp,
            "passed": (None if hit_diff_pp is None else bool(hit_diff_pp >= 10.0)),
        },
        "counts": {
            "non-overlapping short cases pooled across windows": n_short,
            "non-overlapping all-bar cases pooled across windows": n_all,
            "largest-tertile short cases": n_tert,
            "largest-tertile mean forward return": tert_mean,
            "windows": windows_used,
        },
        "decided_by": decided_by,
        "reading": "Short bars are grid bars (positions 0, 20, 40, ... of each window) with forecast < 0 compared against all grid bars of the same windows, both groups taking the Welch t, and the 'largest-tertile shorts' are the ceil(n/3) short cases with the most negative forecast; the minimum-count rule is applied before the reject and confirm rules.",
    }
