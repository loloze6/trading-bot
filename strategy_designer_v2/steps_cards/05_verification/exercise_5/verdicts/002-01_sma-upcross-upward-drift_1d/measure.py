import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_LONG_BLOCKS = 20
    MIN_LONG_WINDOWS = 2
    MIN_POS_WINDOWS = 4

    all_rets = []                 # every block start (random points)
    long_rets = []                # block starts with forecast > 0
    slope_x, slope_y = [], []     # forecast size vs forward return, all blocks with a forecast
    per_window = {}               # (coin, window) -> (long returns, all returns)

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            w_all, w_long = [], []
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                w_all.append(r)
                f = fc[t]
                if np.isfinite(f):
                    slope_x.append(f)
                    slope_y.append(r)
                    if f > 0:
                        w_long.append(r)
            all_rets.extend(w_all)
            long_rets.extend(w_long)
            per_window[(coin, win)] = (w_long, w_all)

    all_rets = np.array(all_rets, dtype=float)
    long_rets = np.array(long_rets, dtype=float)
    n_long = int(len(long_rets))
    n_all = int(len(all_rets))

    # Main measure: mean long-block return minus mean all-block return, Welch t
    excess = None
    t_stat = None
    if n_long > 0 and n_all > 0:
        excess = float(long_rets.mean() - all_rets.mean())
    if n_long >= 2 and n_all >= 2:
        tt = stats.ttest_ind(long_rets, all_rets, equal_var=False)
        t_stat = float(tt.statistic) if np.isfinite(tt.statistic) else None

    # Supporting check: hit rates
    hit_long = float(np.mean(long_rets > 0)) if n_long > 0 else None
    hit_all = float(np.mean(all_rets > 0)) if n_all > 0 else None
    hit_diff = (hit_long - hit_all) if (hit_long is not None and hit_all is not None) else None
    hit_passed = (hit_diff > 0) if hit_diff is not None else None

    # Second view: slope of forward return on forecast size
    slope = None
    sx = np.array(slope_x, dtype=float)
    sy = np.array(slope_y, dtype=float)
    if len(sx) >= 3 and np.std(sx) > 0:
        slope = float(stats.linregress(sx, sy).slope)

    # Per-window excess
    windows_with_long = 0
    windows_pos_excess = 0
    for key, (wl, wa) in per_window.items():
        if len(wl) > 0 and len(wa) > 0:
            windows_with_long += 1
            if np.mean(wl) - np.mean(wa) > 0:
                windows_pos_excess += 1

    # Decision
    if n_long < MIN_LONG_BLOCKS or windows_with_long < MIN_LONG_WINDOWS or excess is None:
        status = "inconclusive"
        decided_by = (f"Inconclusive: {n_long} non-overlapping 10-bar long blocks (minimum 20) and "
                      f"{windows_with_long} windows containing long blocks (minimum 2).")
    elif excess <= 0:
        status = "rejected"
        if t_stat is not None and t_stat <= -2:
            decided_by = "Rejected: the mean excess 10-bar return in long blocks is negative with t <= -2 (reversal: the cross marks exhaustion)."
        else:
            decided_by = "Rejected: the mean excess 10-bar return in long blocks is <= 0."
    elif (t_stat is not None and t_stat >= 2 and hit_passed
          and windows_pos_excess >= MIN_POS_WINDOWS and windows_pos_excess > 1):
        status = "confirmed"
        decided_by = (f"Confirmed: excess > 0 with t >= 2, long-block hit rate above the unconditional one, "
                      f"and excess positive in {windows_pos_excess} windows with long blocks (at least 4).")
    else:
        status = "inconclusive"
        if t_stat is None or t_stat < 2:
            decided_by = "Inconclusive: the excess is > 0 but t is between 0 and 2."
        elif windows_pos_excess <= 1:
            decided_by = "Inconclusive: the confirming numbers are carried by a single window."
        else:
            decided_by = (f"Inconclusive: the excess is > 0 with t >= 2 but the confirm rule is not fully met "
                          f"(hit rate above unconditional: {hit_passed}; windows with positive excess: {windows_pos_excess}, need 4).")

    slope_txt = f"{slope:.6g}" if slope is not None else "n/a"
    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return in long blocks minus mean over all blocks",
            "value": excess,
            "statistic": ({"name": "Welch t (long blocks vs all blocks)", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": "excess > 0 with t >= 2 confirms; excess <= 0 rejects (t <= -2 means reversal); 0 < t < 2 inconclusive",
        },
        "supporting_check": {
            "name": f"long-block hit rate minus unconditional hit rate (slope of 10-bar return on forecast: {slope_txt})",
            "value": hit_diff,
            "passed": hit_passed,
        },
        "counts": {
            "non-overlapping 10-bar long blocks": n_long,
            "non-overlapping 10-bar blocks (all)": n_all,
            "windows containing long blocks": int(windows_with_long),
            "windows with positive excess": int(windows_pos_excess),
        },
        "decided_by": decided_by,
        "reading": ("Blocks start at rows 0, 10, 20, ... of each window with the return kept only when close[t+10] lies in the same window, "
                    "a long block is one whose forecast at the block start is > 0, the per-window excess is that window's long-block mean minus "
                    "that window's all-block mean, 'carried by a single window' is read as only one window having a positive excess, "
                    "and the forecast-size slope is fit over all blocks with a forecast and reported but does not enter the decision."),
    }
