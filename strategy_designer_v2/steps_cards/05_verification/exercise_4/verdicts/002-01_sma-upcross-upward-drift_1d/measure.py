import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    rows = []  # (window, ret, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((f"{coin}:{w}", c1 / c0 - 1.0, f))

    d = pd.DataFrame(rows, columns=["window", "ret", "fc"])
    long_d = d[d["fc"] > 0] if len(d) else d
    n_all = int(len(d))
    n_long = int(len(long_d))
    long_windows = sorted(long_d["window"].unique().tolist()) if n_long else []
    n_long_windows = len(long_windows)

    excess = None
    t_stat = None
    if n_long > 0 and n_all > 0:
        excess = float(long_d["ret"].mean() - d["ret"].mean())
        if n_long >= 2 and n_all >= 2:
            t_res = stats.ttest_ind(long_d["ret"].to_numpy(), d["ret"].to_numpy(), equal_var=False)
            t_stat = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    # hit rates
    hit_long = float((long_d["ret"] > 0).mean()) if n_long else None
    hit_all = float((d["ret"] > 0).mean()) if n_all else None
    hit_passed = None
    if hit_long is not None and hit_all is not None:
        hit_passed = bool(hit_long > hit_all)

    # slope of return on forecast (all blocks)
    slope = None
    if n_all >= 3 and d["fc"].nunique() > 1:
        slope = float(stats.linregress(d["fc"].to_numpy(), d["ret"].to_numpy()).slope)

    # per-window excess
    win_excess = {}
    for w in long_windows:
        dw = d[d["window"] == w]
        lw = dw[dw["fc"] > 0]
        win_excess[w] = float(lw["ret"].mean() - dw["ret"].mean())
    n_pos_windows = int(sum(1 for v in win_excess.values() if v > 0))

    # carried by a single window: dropping any one window makes pooled excess <= 0
    carried_single = False
    if excess is not None and excess > 0:
        for w in d["window"].unique():
            dd = d[d["window"] != w]
            ll = dd[dd["fc"] > 0]
            if len(ll) == 0 or len(dd) == 0:
                carried_single = True
                break
            if ll["ret"].mean() - dd["ret"].mean() <= 0:
                carried_single = True
                break

    if n_long < 20 or n_long_windows < 2:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_long} non-overlapping long blocks (<20 needed) "
                   f"or {n_long_windows} windows with long blocks (<2 needed).")
    elif excess is None:
        status = "inconclusive"
        decided = "Inconclusive: excess could not be computed."
    elif excess <= 0:
        status = "rejected"
        if t_stat is not None and t_stat <= -2:
            decided = "Rejected: mean excess 10-bar return in long blocks is <= 0 with t <= -2 (reversal: the cross marks exhaustion)."
        else:
            decided = "Rejected: mean excess 10-bar return in long blocks is <= 0."
    elif (t_stat is not None and t_stat >= 2 and hit_passed and n_pos_windows >= 4
          and not carried_single):
        status = "confirmed"
        decided = ("Confirmed: excess > 0 with t >= 2, long-block hit rate above unconditional, "
                   "excess positive in at least 4 windows with long blocks, not carried by one window.")
    else:
        status = "inconclusive"
        if carried_single:
            decided = "Inconclusive: positive excess carried by a single window."
        elif t_stat is None or t_stat < 2:
            decided = "Inconclusive: excess > 0 with t between 0 and 2."
        else:
            decided = ("Inconclusive: excess > 0 with t >= 2 but hit-rate or at-least-4-windows "
                       "confirm condition not met.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return in long blocks minus mean over all blocks",
            "value": excess,
            "statistic": ({"name": "Welch t (long blocks vs all blocks)", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": "excess > 0 with t >= 2 confirms; excess <= 0 rejects (t <= -2 reversal); 0 < t < 2 inconclusive",
        },
        "supporting_check": {
            "name": "hit rate long blocks minus hit rate all blocks",
            "value": (hit_long - hit_all) if hit_passed is not None else None,
            "passed": hit_passed,
            "hit_rate_long": hit_long,
            "hit_rate_all": hit_all,
            "slope_return_on_forecast": slope,
        },
        "counts": {
            "non-overlapping 10-bar long blocks": n_long,
            "all non-overlapping 10-bar blocks": n_all,
            "windows containing long blocks": n_long_windows,
            "windows with positive excess": n_pos_windows,
        },
        "decided_by": decided,
        "reading": ("Blocks start at rows 0,10,20,... of each window with a full 10-bar forward return inside the window, "
                    "long means forecast > 0 at block start, t is Welch's long-blocks vs all-blocks, each window's excess "
                    "is its long mean minus its own all-block mean, 'carried by a single window' means dropping some one "
                    "window makes the pooled excess <= 0, and the slope (over all blocks) is reported only."),
    }
