import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_LONG_BLOCKS = 20
    MIN_LONG_WINDOWS = 2
    MIN_POS_WINDOWS = 4

    def find_raw_col(df):
        cands = [c for c in df.columns
                 if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        for c in cands:
            if "sma_cross" in c:
                return c
        return cands[0] if cands else None

    # ---------- 1. situation check ----------
    # Situation (adapted): 50-day SMA above 200-day SMA, i.e. raw percent spread > 0; expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            col = find_raw_col(df)
            if col is None or "forecast" not in df.columns:
                continue
            d = df[["forecast", col]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (d[col] > 0) & (d["forecast"] > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is 'long while the 50-day SMA is above the 200-day SMA' "
                           "(raw spread > 0, forecast > 0), but fewer than 90% of the bars with a non-zero "
                           "forecast are such bars on the long side"
                           + (" (no active bars at all)." if n_active == 0 else ".")),
            "reading": "Situation taken as raw sma_cross spread (last_history_value) > 0 with forecast > 0.",
        }

    # ---------- 2. non-overlapping 10-bar blocks ----------
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].values.astype(float)
            fc = d["forecast"].values.astype(float)
            n = len(d)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1, f = close[p], close[p + H], fc[p]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                recs.append({"coin": coin, "window": w, "ret": c1 / c0 - 1.0, "fc": f})
    blocks = pd.DataFrame(recs, columns=["coin", "window", "ret", "fc"])
    allr = blocks["ret"].values
    longb = blocks[blocks["fc"] > 0]
    longr = longb["ret"].values

    n_long = int(len(longr))
    n_all = int(len(allr))
    long_windows = sorted(set(zip(longb["coin"], longb["window"])))
    n_long_windows = len(long_windows)

    excess = float(np.mean(longr) - np.mean(allr)) if n_long > 0 and n_all > 0 else None
    t_val = None
    if n_long >= 2 and n_all >= 2:
        t_res = stats.ttest_ind(longr, allr, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    # Hit rates
    hit_long = float(np.mean(longr > 0)) if n_long > 0 else None
    hit_all = float(np.mean(allr > 0)) if n_all > 0 else None
    hit_diff = (hit_long - hit_all) if (hit_long is not None and hit_all is not None) else None
    hit_pass = bool(hit_diff is not None and hit_diff > 0) if hit_diff is not None else None

    # Slope of 10-bar return on forecast size at block start (all blocks)
    slope = None
    if n_all >= 3 and np.std(blocks["fc"].values) > 0:
        slope = float(stats.linregress(blocks["fc"].values, allr).slope)

    # Per-window excess (window's long mean minus that window's all-block mean)
    win_excess = {}
    for (c, w) in long_windows:
        sub = blocks[(blocks["coin"] == c) & (blocks["window"] == w)]
        lr = sub.loc[sub["fc"] > 0, "ret"].values
        win_excess[f"{c}:{w}"] = float(np.mean(lr) - np.mean(sub["ret"].values))
    n_pos_windows = int(sum(1 for v in win_excess.values() if v > 0))

    # Carried by a single window: dropping one window makes the pooled excess <= 0
    carried = False
    if excess is not None and excess > 0:
        for (c, w) in long_windows:
            rest = blocks[~((blocks["coin"] == c) & (blocks["window"] == w))]
            rl = rest.loc[rest["fc"] > 0, "ret"].values
            if len(rl) == 0 or len(rest) == 0 or (np.mean(rl) - np.mean(rest["ret"].values)) <= 0:
                carried = True
                break

    # ---------- 3. decision ----------
    if n_long < MIN_LONG_BLOCKS or n_long_windows < MIN_LONG_WINDOWS:
        status = "inconclusive"
        decided_by = (f"Inconclusive: {n_long} non-overlapping long blocks (minimum 20) and "
                      f"{n_long_windows} windows containing long blocks (minimum 2).")
    elif excess is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the excess return could not be computed."
    elif excess <= 0:
        status = "rejected"
        if t_val is not None and t_val <= -2:
            decided_by = ("Rejected: the mean excess 10-bar return in long blocks is negative with t <= -2, "
                          "a reversal (the cross marks exhaustion).")
        else:
            decided_by = "Rejected: the mean excess 10-bar return in long blocks is <= 0."
    elif (t_val is not None and t_val >= 2 and hit_pass and n_pos_windows >= MIN_POS_WINDOWS
          and not carried):
        status = "confirmed"
        decided_by = ("Confirmed: excess > 0 with t >= 2, long-block hit rate above the unconditional one, "
                      f"and the excess positive in {n_pos_windows} windows with long blocks (>= 4), "
                      "not carried by a single window.")
    else:
        status = "inconclusive"
        if t_val is None or t_val < 2:
            decided_by = "Inconclusive: the excess is > 0 but with t between 0 and 2."
        elif carried:
            decided_by = "Inconclusive: the confirming numbers are carried by a single window."
        else:
            decided_by = ("Inconclusive: excess > 0 with t >= 2, but the confirm rule is not fully met "
                          f"(hit rate above unconditional: {hit_pass}; windows with positive excess: "
                          f"{n_pos_windows} of {n_long_windows}, need 4).")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean 10-bar forward return in long blocks minus mean over all blocks",
            "value": excess,
            "statistic": ({"name": "Welch t (long blocks vs all blocks)", "value": t_val}
                          if t_val is not None else None),
            "threshold": "excess > 0 with t >= 2 confirms; excess <= 0 rejects (t <= -2 = reversal)",
        },
        "supporting_check": {
            "name": "hit rate of long blocks minus hit rate of all blocks",
            "value": hit_diff,
            "passed": hit_pass,
            "hit_rate_long": hit_long,
            "hit_rate_all": hit_all,
            "slope_return_on_forecast": slope,
            "window_excess": win_excess,
        },
        "counts": {
            "non-overlapping 10-bar long blocks": n_long,
            "windows containing long blocks": int(n_long_windows),
            "windows with positive excess": n_pos_windows,
            "all blocks": n_all,
        },
        "decided_by": decided_by,
        "reading": ("Blocks start at positions 0, 10, 20, ... of each window with the forward return inside the window, "
                    "long blocks have forecast > 0 at the start, t is Welch's t of long-block returns against all-block "
                    "returns, each window's excess uses that window's own all-block mean, the slope is fitted over all "
                    "blocks, and 'carried by a single window' means that dropping any one window leaves a pooled excess <= 0."),
    }
