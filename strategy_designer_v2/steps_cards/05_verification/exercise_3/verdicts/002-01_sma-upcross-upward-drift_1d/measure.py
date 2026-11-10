import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_LONG_BLOCKS = 20
    MIN_LONG_WINDOWS = 2
    MIN_POS_WINDOWS = 4

    # Collect non-overlapping 10-bar blocks: grid positions 0, 10, 20, ... of each window.
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                recs.append({"coin": coin, "window": w, "key": f"{coin}|{w}",
                             "ret": c1 / c0 - 1.0, "fc": f})
    blocks = pd.DataFrame(recs, columns=["coin", "window", "key", "ret", "fc"])

    n_all = int(len(blocks))
    long_b = blocks[blocks["fc"] > 0] if n_all else blocks
    n_long = int(len(long_b))
    long_keys = sorted(long_b["key"].unique().tolist()) if n_long else []
    n_long_windows = len(long_keys)

    excess = None
    t_stat = None
    hit_long = hit_all = hit_diff = None
    hit_pass = None
    slope = None
    if n_long > 0 and n_all > 0:
        excess = float(long_b["ret"].mean() - blocks["ret"].mean())
        if n_long >= 2 and n_all >= 2:
            tt = stats.ttest_ind(long_b["ret"].values, blocks["ret"].values, equal_var=False)
            t_stat = float(tt.statistic) if np.isfinite(tt.statistic) else None
        hit_long = float((long_b["ret"] > 0).mean())
        hit_all = float((blocks["ret"] > 0).mean())
        hit_diff = hit_long - hit_all
        hit_pass = bool(hit_long > hit_all)
    if n_all >= 3 and blocks["fc"].nunique() > 1:
        slope = float(stats.linregress(blocks["fc"].values, blocks["ret"].values).slope)

    # Per-window excess: window's long-block mean minus that window's all-block mean.
    win_excess = {}
    for k in long_keys:
        wb = blocks[blocks["key"] == k]
        wl = wb[wb["fc"] > 0]
        win_excess[k] = float(wl["ret"].mean() - wb["ret"].mean())
    n_pos_windows = int(sum(1 for v in win_excess.values() if v > 0))

    # Single-window carry: pooled excess must stay > 0 when any one window is left out.
    carried_by_single = False
    if n_long_windows >= 1:
        for k in long_keys:
            rest = blocks[blocks["key"] != k]
            rl = rest[rest["fc"] > 0]
            if len(rl) == 0 or len(rest) == 0 or (rl["ret"].mean() - rest["ret"].mean()) <= 0:
                carried_by_single = True
                break

    if n_long < MIN_LONG_BLOCKS or n_long_windows < MIN_LONG_WINDOWS or excess is None:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_long} long blocks (minimum {MIN_LONG_BLOCKS}) in "
                   f"{n_long_windows} windows (minimum {MIN_LONG_WINDOWS}).")
    elif excess <= 0:
        status = "rejected"
        if t_stat is not None and t_stat <= -2:
            decided = "Rejected: mean excess 10-bar return in long blocks is negative with t <= -2 (reversal: the cross marks exhaustion)."
        else:
            decided = "Rejected: mean excess 10-bar return in long blocks is <= 0."
    else:
        confirm = (t_stat is not None and t_stat >= 2 and hit_pass
                   and n_pos_windows >= MIN_POS_WINDOWS)
        if confirm and not carried_by_single:
            status = "confirmed"
            decided = ("Confirmed: excess > 0 with t >= 2, long-block hit rate above the unconditional hit rate, "
                       f"and excess positive in {n_pos_windows} of {n_long_windows} windows with long blocks.")
        elif confirm and carried_by_single:
            status = "inconclusive"
            decided = "Inconclusive: confirming numbers are carried by a single window (pooled excess turns <= 0 without it)."
        else:
            status = "inconclusive"
            reasons = []
            if t_stat is None or t_stat < 2:
                reasons.append("t below 2")
            if not hit_pass:
                reasons.append("hit rate not above unconditional")
            if n_pos_windows < MIN_POS_WINDOWS:
                reasons.append(f"excess positive in only {n_pos_windows} windows (need 4)")
            decided = "Inconclusive: excess > 0 but confirm rule not met (" + "; ".join(reasons) + ")."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 10-bar forward return in long blocks minus mean over all blocks",
            "value": excess,
            "statistic": ({"name": "Welch t", "value": t_stat} if t_stat is not None else None),
            "threshold": "excess > 0 with t >= 2 to confirm; excess <= 0 rejects (t <= -2 means reversal)",
        },
        "supporting_check": {
            "name": "long-block hit rate minus all-block hit rate (slope of return on forecast as second view)",
            "value": hit_diff,
            "passed": hit_pass,
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
        "reading": ("Blocks start at rows 0,10,20,... of each window with a full 10-bar return inside it, 'all blocks' "
                    "includes long ones and the t is Welch's between long and all blocks, per-window excess uses that "
                    "window's own all-block mean, the slope is fit over all blocks, and 'carried by a single window' "
                    "means the pooled excess is <= 0 once any one window is left out."),
    }
