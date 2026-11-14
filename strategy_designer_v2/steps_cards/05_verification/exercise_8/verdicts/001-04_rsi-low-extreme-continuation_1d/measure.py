import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    VAL = "debug_info.components.rsi_low.last_history_value"

    # ---------- 1. Situation check: RSI < 50 (raw value > 0), expected side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", VAL]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            situ = d[VAL] > 0  # RSI = 50 - value/0.4 < 50
            n_agree += int((active & situ & (d["forecast"] < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean fwd 5-bar return after top-quintile |forecast| minus after neutral bars"
    thr_words = "confirm if difference < 0 with Welch t <= -2; reject if > 0 with t >= +2; else inconclusive; min 30 extreme cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars with RSI(14) below 50, "
                           "so the config does not trade the plan's situation (RSI below 50) on its side (short)."),
            "reading": "none",
        }

    # ---------- 2. Non-overlapping 5-bar grid, pooled ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].values.astype(float)
            fc = df["forecast"].values.astype(float)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, w, f, c1 / c0 - 1.0))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])

    if len(g) == 0:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": {"name": "same sign in >= 2 of 3 coins", "value": None, "passed": None},
            "counts": {"non-overlapping extreme cases": 0, "non-overlapping neutral cases": 0},
            "decided_by": "Fewer than 30 non-overlapping extreme cases in total, so inconclusive.",
            "reading": "No valid non-overlapping blocks were available.",
        }

    a = g["forecast"].abs()
    q80 = float(a.quantile(0.8))
    q20 = float(a.quantile(0.2))
    g["extreme"] = (a >= q80) & (a > 0)
    g["neutral"] = ((a == 0) | (a <= q20)) & ~g["extreme"]

    ext = g.loc[g["extreme"], "ret"].values
    neu = g.loc[g["neutral"], "ret"].values
    n_ext, n_neu = len(ext), len(neu)

    diff = None
    tval = None
    if n_ext >= 2 and n_neu >= 2:
        diff = float(np.mean(ext) - np.mean(neu))
        t = stats.ttest_ind(ext, neu, equal_var=False).statistic
        tval = float(t) if np.isfinite(t) else None
    elif n_ext >= 1 and n_neu >= 1:
        diff = float(np.mean(ext) - np.mean(neu))

    # ---------- supporting check: per-coin sign ----------
    coin_diffs = {}
    for coin, gc in g.groupby("coin"):
        e = gc.loc[gc["extreme"], "ret"].values
        nn = gc.loc[gc["neutral"], "ret"].values
        if len(e) >= 1 and len(nn) >= 1:
            coin_diffs[coin] = float(np.mean(e) - np.mean(nn))
    if diff is None or diff == 0:
        sup_val, sup_pass = None, None
    else:
        same = sum(1 for v in coin_diffs.values() if np.sign(v) == np.sign(diff))
        sup_val = int(same)
        sup_pass = bool(same >= 2)

    # ---------- decision ----------
    if n_ext < 30:
        status = "inconclusive"
        decided = f"Only {n_ext} non-overlapping extreme cases (fewer than 30), so inconclusive."
    elif diff is None or tval is None:
        status = "inconclusive"
        decided = "The difference or its t could not be computed, so inconclusive."
    elif diff < 0 and tval <= -2:
        status = "confirmed"
        decided = "Return after extremes minus after neutral readings is negative with t <= -2, so confirmed."
    elif diff > 0 and tval >= 2:
        status = "rejected"
        decided = "The difference is positive with t >= +2 (reversal, not continuation), so rejected."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and +2, so inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": thr_words,
        },
        "supporting_check": {
            "name": "number of coins whose difference has the pooled sign (need >= 2)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping extreme cases": int(n_ext),
            "non-overlapping neutral cases": int(n_neu),
            "coins": int(g["coin"].nunique()),
        },
        "decided_by": decided,
        "reading": ("Quintiles of |forecast| are taken over all pooled non-overlapping grid bars (extreme = |forecast| at or above "
                    "the 80th percentile and non-zero, neutral = forecast 0 or at or below the 20th percentile), and the "
                    "supporting check needs 2 coins with the pooled sign whatever the number of coins present."),
    }
