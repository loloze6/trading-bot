import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    all_rets = []        # 10-bar returns of every non-overlapping block (random points)
    long_rets = []       # 10-bar returns of blocks whose start forecast is > 0
    long_fc = []         # forecast at the start of long blocks
    long_win = []        # window key of each long block

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for s in range(0, n - H, H):
                c0, c1 = close[s], close[s + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                f = fc[s]
                if np.isfinite(f) and f > 0:
                    long_rets.append(r)
                    long_fc.append(f)
                    long_win.append((coin, win))

    all_rets = np.asarray(all_rets, dtype=float)
    long_rets = np.asarray(long_rets, dtype=float)
    long_fc = np.asarray(long_fc, dtype=float)
    n_long = int(len(long_rets))

    reading = ("Blocks are consecutive non-overlapping 10-bar blocks starting at each window's first row, "
               "and a block is long when the forecast at its start is > 0. The baseline is the pooled mean "
               "over all blocks of all windows, and the per-window excess is that window's long-block mean "
               "minus this pooled baseline. The t-stat is a one-sample t on the long-block excess returns. "
               "'Carried by a single window' is read as the excess being positive in only one window; with "
               "fewer than 4 windows containing long blocks, confirmation cannot be met.")

    main_name = "mean excess 10-bar return of long blocks over all-block mean"
    main_thr = "> 0 with t >= 2 to confirm; <= 0 to reject"

    if len(all_rets) == 0 or n_long == 0:
        return {
            "status": "inconclusive",
            "main_measure": {"name": main_name, "value": None, "threshold": main_thr},
            "supporting_check": None,
            "cases": n_long,
            "decided_by": "Inconclusive: fewer than 20 non-overlapping 10-bar long blocks.",
            "reading": reading,
        }

    base = float(np.mean(all_rets))
    excess = long_rets - base
    mean_ex = float(np.mean(excess))
    if n_long >= 2:
        sd = float(np.std(excess, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n_long))) if sd > 0 else (
            float(np.inf) if mean_ex > 0 else (float(-np.inf) if mean_ex < 0 else 0.0))
    else:
        t = None

    hit_long = float(np.mean(long_rets > 0))
    hit_all = float(np.mean(all_rets > 0))
    hit_pass = bool(hit_long > hit_all)

    slope = None
    if n_long >= 3 and np.ptp(long_fc) > 0:
        slope = float(stats.linregress(long_fc, long_rets).slope)

    wins = sorted(set(long_win))
    win_ex = {}
    for w in wins:
        m = np.array([lw == w for lw in long_win])
        win_ex[f"{w[0]}:{w[1]}"] = float(np.mean(long_rets[m]) - base)
    n_win_long = len(wins)
    n_win_pos = int(sum(1 for v in win_ex.values() if v > 0))

    t_out = None if t is None or not np.isfinite(t) else t

    supporting = {
        "name": "hit rate of long blocks minus unconditional hit rate",
        "value": hit_long - hit_all,
        "passed": hit_pass,
        "hit_rate_long": hit_long,
        "hit_rate_all": hit_all,
        "slope_return_on_forecast": slope,
        "slope_positive": None if slope is None else bool(slope > 0),
    }

    if n_long < 20 or n_win_long < 2:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_long} long blocks (minimum 20) in {n_win_long} windows "
                   f"(minimum 2).")
    elif mean_ex <= 0:
        status = "rejected"
        if t is not None and t <= -2:
            decided = f"Rejected with reversal: the mean excess {mean_ex:.5f} is <= 0 with t = {t:.2f} <= -2."
        else:
            decided = f"Rejected: the mean excess 10-bar return in long blocks ({mean_ex:.5f}) is <= 0."
    elif t is not None and t >= 2 and hit_pass and n_win_pos >= 4 and n_win_pos > 1:
        status = "confirmed"
        decided = (f"Confirmed: the mean excess {mean_ex:.5f} > 0 with t = {t:.2f} >= 2, the long hit rate "
                   f"{hit_long:.3f} > the unconditional {hit_all:.3f}, and the excess is positive in "
                   f"{n_win_pos} of {n_win_long} windows with long blocks.")
    else:
        status = "inconclusive"
        reasons = []
        if t is None or t < 2:
            reasons.append(f"t = {t_out} is below 2")
        if not hit_pass:
            reasons.append("the long hit rate is not above the unconditional hit rate")
        if n_win_pos < 4:
            reasons.append(f"the excess is positive in only {n_win_pos} windows (needs 4)")
        decided = "Inconclusive: the excess is > 0 but " + "; ".join(reasons) + "."

    return {
        "status": status,
        "main_measure": {"name": main_name, "value": mean_ex, "threshold": main_thr,
                         "t_stat": t_out, "baseline_mean_all_blocks": base,
                         "n_all_blocks": int(len(all_rets)),
                         "windows_with_long_blocks": n_win_long,
                         "windows_positive_excess": n_win_pos,
                         "per_window_excess": win_ex},
        "supporting_check": supporting,
        "cases": n_long,
        "decided_by": decided,
        "reading": reading,
    }
