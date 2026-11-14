import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    long_rets, all_rets, long_fc = [], [], []
    per_window = {}  # (coin, window) -> (long list, all list)

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win].reset_index(drop=True)
            if "close" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float) \
                if "forecast" in df.columns else np.full(len(df), np.nan)
            n = len(df)
            wl, wa = [], []
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                wa.append(r)
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    wl.append(r)
                    long_rets.append(r)
                    long_fc.append(fc[t])
            per_window[(coin, win)] = (wl, wa)

    long_rets = np.array(long_rets, dtype=float)
    all_rets = np.array(all_rets, dtype=float)
    long_fc = np.array(long_fc, dtype=float)
    n_long = int(len(long_rets))
    n_all = int(len(all_rets))

    windows_with_long = [k for k, (wl, wa) in per_window.items() if len(wl) > 0]
    n_win_long = len(windows_with_long)

    # Main measure: mean long-block return minus mean all-block return
    excess = None
    t_stat = None
    if n_long > 0 and n_all > 0:
        excess = float(long_rets.mean() - all_rets.mean())
    if n_long >= 2 and n_all >= 2:
        tt = stats.ttest_ind(long_rets, all_rets, equal_var=False)
        t_stat = float(tt.statistic) if np.isfinite(tt.statistic) else None

    # Supporting: hit rates
    hit_long = float((long_rets > 0).mean()) if n_long > 0 else None
    hit_all = float((all_rets > 0).mean()) if n_all > 0 else None
    hit_diff = (hit_long - hit_all) if (hit_long is not None and hit_all is not None) else None
    hit_pass = (hit_diff > 0) if hit_diff is not None else None

    # Second view: slope of long-block return on forecast size
    slope = None
    if n_long >= 3 and np.std(long_fc) > 0:
        slope = float(stats.linregress(long_fc, long_rets).slope)

    # Per-window excess
    win_excess = {}
    for k in windows_with_long:
        wl, wa = per_window[k]
        win_excess[k] = float(np.mean(wl) - np.mean(wa))
    n_win_pos = int(sum(1 for v in win_excess.values() if v > 0))

    # Single-window carry check: pooled excess stays > 0 when any one window is dropped
    carried_by_one = False
    if n_win_long >= 2 and excess is not None and excess > 0:
        for drop in windows_with_long:
            l2, a2 = [], []
            for k, (wl, wa) in per_window.items():
                if k == drop:
                    continue
                l2 += wl
                a2 += wa
            if len(l2) == 0 or len(a2) == 0 or (np.mean(l2) - np.mean(a2)) <= 0:
                carried_by_one = True
                break

    # Decision
    if n_long < 20 or n_win_long < 2:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_long} non-overlapping 10-bar long blocks (min 20) and "
                   f"{n_win_long} windows with long blocks (min 2).")
    elif excess is None or t_stat is None:
        status = "inconclusive"
        decided = "Inconclusive: the excess or its t-statistic could not be computed."
    elif excess <= 0:
        status = "rejected"
        if t_stat <= -2:
            decided = "Rejected: mean excess 10-bar return in long blocks <= 0 with t <= -2 (reversal: the cross marks exhaustion)."
        else:
            decided = "Rejected: mean excess 10-bar return in long blocks is <= 0."
    elif t_stat >= 2 and hit_pass and n_win_pos >= 4 and not carried_by_one:
        status = "confirmed"
        decided = ("Confirmed: excess > 0 with t >= 2, long-block hit rate above the unconditional hit rate, "
                   "and excess positive in at least 4 windows with long blocks.")
    else:
        status = "inconclusive"
        if t_stat < 2:
            decided = "Inconclusive: excess > 0 but t between 0 and 2."
        elif carried_by_one:
            decided = "Inconclusive: confirming numbers carried by a single window."
        else:
            decided = ("Inconclusive: excess > 0 with t >= 2 but the hit-rate condition or the "
                       "at-least-4-positive-windows condition is not met, so neither confirm nor reject holds.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return in long blocks minus mean over all blocks",
            "value": excess,
            "statistic": {"name": "Welch t (long blocks vs all blocks)", "value": t_stat} if t_stat is not None else None,
            "threshold": "excess > 0 with t >= 2 to confirm; excess <= 0 rejects (t <= -2 means reversal)",
        },
        "supporting_check": {
            "name": ("hit rate of long blocks minus hit rate of all blocks"
                     f" (long {hit_long}, all {hit_all}; slope of return on forecast: {slope})"),
            "value": hit_diff,
            "passed": hit_pass,
        },
        "counts": {
            "non-overlapping 10-bar long blocks": n_long,
            "non-overlapping 10-bar blocks (all)": n_all,
            "windows containing long blocks": int(n_win_long),
            "windows with positive excess": n_win_pos,
        },
        "decided_by": decided,
        "reading": ("Blocks start at rows 0, 10, 20, ... of each window with returns kept inside the window; long means forecast > 0 "
                    "at the block start; the t is Welch's long-blocks vs all-blocks; per-window excess is the window's long mean "
                    "minus its all-block mean; 'carried by a single window' means the pooled excess drops to <= 0 when any one "
                    "window is removed; the forecast-slope view is reported but does not enter the decision since the confirm rule omits it."),
    }
