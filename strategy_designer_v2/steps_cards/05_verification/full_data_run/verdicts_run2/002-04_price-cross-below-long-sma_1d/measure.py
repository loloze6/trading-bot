import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.below_ma.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    # Situation: close below its 200-day SMA (raw percent distance < 0); expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            fc = sub["forecast"].to_numpy(dtype=float)
            raw = sub[RAW].to_numpy(dtype=float)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of allocation x (10-bar return - 10 x coin mean daily return) over non-overlapping 10-bar blocks, before costs"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; needs >= 30 nonzero-position blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("No active bars in the record, so the short-while-below-SMA200 situation cannot be checked."
                           if agreement is None else
                           f"Only {agreement:.1%} of active bars are short while the close is below its 200-day SMA, below the 90% required by the plan's Fidelity."),
            "reading": "Situation taken as the component's raw distance from the SMA200 below zero, side taken as short (forecast < 0).",
        }

    # ---------- 2. Criterion ----------
    products = []
    nz_alloc = []
    nz_excess = []
    for coin, wins in bars.items():
        # coin's mean daily return over all its windows together (returns never cross windows)
        daily = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) >= 2:
                r = c[1:] / c[:-1] - 1.0
                daily.append(r[np.isfinite(r)])
        if not daily:
            continue
        daily = np.concatenate(daily)
        if daily.size == 0:
            continue
        mu = float(np.mean(daily))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            a = pd.to_numeric(df[ALLOC], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and np.isfinite(a[t])) or c[t] == 0:
                    continue
                r10 = c[t + H] / c[t] - 1.0
                ex = r10 - H * mu
                products.append(a[t] * ex)
                if a[t] != 0:
                    nz_alloc.append(a[t])
                    nz_excess.append(ex)

    products = np.asarray(products, dtype=float)
    n_blocks = int(products.size)
    n_nz = int(len(nz_alloc))

    mean_val = float(np.mean(products)) if n_blocks > 0 else None
    t_val = None
    if n_blocks >= 2:
        sd = float(np.std(products, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_blocks)))

    # supporting check: slope of excess return on allocation among nonzero-position blocks
    slope = None
    sup_passed = None
    if n_nz >= 3 and np.std(nz_alloc) > 0:
        res = stats.linregress(np.asarray(nz_alloc), np.asarray(nz_excess))
        slope = float(res.slope)
        sup_passed = bool(slope > 0)

    if n_nz < 30:
        status = "inconclusive"
        decided = f"Only {n_nz} non-overlapping 10-bar blocks with a nonzero position (fewer than 30), so the result is inconclusive."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so no confirm or reject rule is met: inconclusive."
    elif mean_val > 0 and t_val >= 2:
        status = "confirmed"
        decided = "The mean excess gain of the short positions is positive with t >= 2: confirmed."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess gain is negative with t <= -2 (the coin rose beyond holding below the SMA200): rejected."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of excess 10-bar return on allocation, nonzero-position blocks",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 10-bar blocks with a nonzero position": n_nz,
            "non-overlapping 10-bar blocks": n_blocks,
        },
        "decided_by": decided,
        "reading": ("Blocks start at rows 0, 10, 20, ... of each window and need a full 10-bar return inside the window; "
                    "the pooled mean and t use all such blocks (zero-position blocks contribute zero products) as the plan pools across coins and blocks; "
                    "the coin's mean daily return is the mean of its within-window close-to-close returns over all its windows."),
    }
