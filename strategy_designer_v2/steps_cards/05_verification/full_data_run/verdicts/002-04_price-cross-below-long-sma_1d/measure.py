import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.below_ma.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    # The situation is the close below its 200-day SMA, so the raw distance is < 0. The expected side is short, so forecast < 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            n_agree += int((active & (sub[RAW] < 0) & (sub["forecast"] < 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True  # nothing active to contradict the plan; the criterion's minimum count will decide

    main_name = "mean of allocation x (10-bar return - 10 x coin mean daily return), non-overlapping blocks, pooled"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; needs >= 30 nonzero-position blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are short bars with the close below its 200-day SMA, "
                          "so the config's forecast does not trade the plan's situation (close below the SMA200, short).",
            "reading": "Situation taken as raw below_ma distance < 0, with a negative forecast as the expected short side.",
        }

    # ---------- 2. Coin mean daily return over all windows together ----------
    mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- 3. Non-overlapping 10-bar blocks ----------
    products = []
    nz_alloc = []
    nz_excess = []
    for coin, wins in bars.items():
        m = mu[coin]
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            c = df["close"].astype(float).values
            a = df[ALLOC].astype(float).values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1, al = c[t], c[t + H], a[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(al)) or c0 == 0:
                    continue
                excess = (c1 / c0 - 1.0) - H * m
                products.append(al * excess)
                if al != 0:
                    nz_alloc.append(al)
                    nz_excess.append(excess)

    products = np.asarray(products, dtype=float)
    n_blocks = int(products.size)
    n_nz = len(nz_alloc)

    mean_val = float(np.mean(products)) if n_blocks > 0 else None
    t_val = None
    if n_blocks > 1:
        sd = float(np.std(products, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_blocks)))

    # ---------- 4. Supporting check ----------
    slope = None
    sup_passed = None
    if n_nz >= 3 and np.ptp(np.asarray(nz_alloc)) > 0:
        res = stats.linregress(np.asarray(nz_alloc), np.asarray(nz_excess))
        slope = float(res.slope)
        sup_passed = bool(slope > 0)

    # ---------- 5. Decision ----------
    if n_nz < 30:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping 10-bar blocks with a nonzero position pooled across coins, so the result is inconclusive."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so no t lies outside (-2, 2) and the result is inconclusive."
    elif mean_val > 0 and t_val >= 2:
        status = "confirmed"
        decided = "The mean excess gain of the short positions is positive with t >= 2."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess gain is negative with t <= -2: the coin rose beyond holding after closes below the SMA200."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "slope of excess 10-bar return on allocation, nonzero-position blocks",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 10-bar blocks with a nonzero position": n_nz,
            "non-overlapping 10-bar blocks": n_blocks,
            "active bars": n_active,
        },
        "decided_by": decided,
        "reading": "The mean and its t are taken over all pooled blocks, zero-position blocks included, because the main measure pools the products across all coins and blocks. "
                   "Blocks start at positions 0, 10, 20, ... of each window and need the close 10 bars later in the same window. "
                   "The coin's mean daily return pools the within-window daily returns of all its windows.",
    }
