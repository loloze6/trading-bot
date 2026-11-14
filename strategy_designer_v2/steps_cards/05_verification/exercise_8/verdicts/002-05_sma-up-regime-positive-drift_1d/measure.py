import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the 50-day SMA is above the 200-day SMA (raw spread > 0), expected side long.
    active_total = 0
    active_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            active_total += int(act.sum())
            agree = act & (d[RAW] > 0) & (d["forecast"] > 0)
            active_agree += int(agree.sum())
    agreement = (active_agree / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("The plan's situation is a long position only while the 50-day SMA is above "
                           "the 200-day SMA (positive raw spread), but fewer than 90% of the bars with a "
                           "non-zero forecast are positive-spread bars with a positive forecast."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    in_rets, out_rets = [], []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0
            fc = df["forecast"]
            ok = nxt.notna() & fc.notna() & close.notna()
            in_mask = ok & (fc > 0)
            out_mask = ok & (fc == 0)
            in_rets.extend(nxt[in_mask].tolist())
            out_rets.extend(nxt[out_mask].tolist())

            # Distinct up-cross stretches: contiguous runs of positive raw spread in each window.
            raw = df[RAW]
            pos = (raw > 0) & raw.notna()
            starts = pos & ~pos.shift(1, fill_value=False)
            n_stretches += int(starts.sum())

    in_rets = np.asarray(in_rets, dtype=float)
    out_rets = np.asarray(out_rets, dtype=float)
    n_in, n_out = len(in_rets), len(out_rets)

    diff = None
    t = None
    if n_in >= 2 and n_out >= 2:
        diff = float(in_rets.mean() - out_rets.mean())
        tt = stats.ttest_ind(in_rets, out_rets, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    elif n_in >= 1 and n_out >= 1:
        diff = float(in_rets.mean() - out_rets.mean())

    sup = None
    if n_in >= 1 and n_out >= 1:
        sup = float((in_rets > 0).mean() - (out_rets > 0).mean())

    counts = {
        "in-stretch bars": int(n_in),
        "out-of-stretch bars": int(n_out),
        "distinct up-cross stretches": int(n_stretches),
    }

    enough = n_in >= 100 and n_out >= 100 and n_stretches >= 3
    if not enough:
        status = "inconclusive"
        decided = ("Fewer than 100 in-stretch bars, 100 out-of-stretch bars or 3 distinct up-cross "
                   "stretches, so the result is inconclusive whatever the t.")
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so |t| >= 2 is not met and the result is inconclusive."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "The in-stretch minus out-of-stretch mean next-bar return is positive with t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The difference is negative with t <= -2: moves after up crosses reverse."
    else:
        status = "inconclusive"
        decided = "|t| < 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean next-bar return in-stretch minus out-of-stretch",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
            "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects; |t| < 2 inconclusive",
        },
        "supporting_check": {
            "name": "share of up next-bars in-stretch minus out-of-stretch",
            "value": sup,
            "passed": (None if sup is None else bool(sup > 0)),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Distinct up-cross stretches are counted as contiguous runs of positive raw SMA spread within "
                    "each window, including a run already under way at the window's first bar, and the supporting "
                    "check passes when the in-stretch up-share exceeds the out-of-stretch one."),
    }
