import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = SMA50 above SMA200 (raw spread > 0); outcome = price rises -> long side.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            fc = d["forecast"].astype(float).values
            raw = d[RAW].astype(float).values
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = ("Mean 20-bar forward return after forecast > 0 minus mean 20-bar forward "
                 "return of all bars, non-overlapping blocks, pooled")
    threshold = "excess > 0 with t >= 2 confirms; excess < 0 with t <= -2 rejects; else inconclusive; fewer than 30 blocks with forecast > 0 is inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are long bars where the "
                           "SMA50-minus-SMA200 spread is positive, so the config does not hold the "
                           "plan's situation (SMA50 above SMA200, long)."),
            "reading": "Situation taken as the component's raw value (last_history_value) > 0 with forecast > 0.",
        }

    # ---------- 2. Criterion ----------
    cond_rets = []
    all_rets = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    cond_rets.append(r)

    cond = np.array(cond_rets, dtype=float)
    allr = np.array(all_rets, dtype=float)
    n_cond = int(len(cond))
    n_all = int(len(allr))

    excess = None
    tval = None
    if n_cond >= 2 and n_all >= 2:
        excess = float(cond.mean() - allr.mean())
        t_res = stats.ttest_ind(cond, allr, equal_var=False)
        tval = float(t_res.statistic) if np.isfinite(t_res.statistic) else None
    elif n_cond >= 1 and n_all >= 1:
        excess = float(cond.mean() - allr.mean())

    # Supporting check: hit rate
    sup_val = None
    sup_pass = None
    if n_cond >= 1 and n_all >= 1:
        hit_c = float((cond > 0).mean())
        hit_a = float((allr > 0).mean())
        sup_val = float(hit_c - hit_a)
        sup_pass = bool(hit_c > hit_a)

    if n_cond < 30:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping 20-bar blocks with forecast > 0, so the result is inconclusive."
    elif excess is None or tval is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so the result is inconclusive."
    elif excess > 0 and tval >= 2:
        status = "confirmed"
        decided = "The excess 20-bar return is above 0 with t >= 2 over non-overlapping blocks, which confirms."
    elif excess < 0 and tval <= -2:
        status = "rejected"
        decided = "The excess 20-bar return is below 0 with t <= -2, so up-cross spans underperform: rejected."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": excess,
            "statistic": ({"name": "Welch t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Share of positive 20-bar forward returns when forecast > 0 minus unconditional share",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping 20-bar blocks with forecast > 0": n_cond,
            "non-overlapping 20-bar blocks, all bars": n_all,
        },
        "decided_by": decided,
        "reading": ("Situation is last_history_value > 0 with forecast > 0; blocks start at positions 0, 20, 40, ... of each "
                    "window with the full 20-bar return inside the window; the comparison group is all grid blocks of all "
                    "coin-windows pooled, tested with Welch t; the supporting check passes when the conditional hit rate "
                    "exceeds the unconditional one."),
    }
