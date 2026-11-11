import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    comp = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    # The plan's situation is the 50-day SMA above the 200-day SMA (raw spread > 0).
    # The expected side is long, because the plan's outcome is a rise.
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            sp = pd.to_numeric(df[comp], errors="coerce") if comp in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (sp > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9

    main_name = "in-stretch minus out-of-stretch mean next-bar return"
    thr = "confirm if positive with Welch t >= 2; reject if negative with t <= -2; else inconclusive (needs >=100 in, >=100 out, >=3 stretches)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "The non-zero forecasts do not fall, long, on the bars where the 50-day SMA is above the 200-day SMA in at least 90% of cases, so the config does not do what the plan's situation says.",
            "reading": "Situation taken as raw SMA spread > 0 with a positive forecast; bars with a missing spread count as not agreeing.",
        }

    # ---------- 2. Criterion ----------
    in_rets, out_rets = [], []
    n_stretches = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            if n == 0:
                continue
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            ok = ~np.isnan(nxt) & ~np.isnan(fc)
            in_mask = ok & (fc > 0)
            out_mask = ok & (fc == 0)
            in_rets.extend(nxt[in_mask].tolist())
            out_rets.extend(nxt[out_mask].tolist())
            # Distinct stretches: maximal runs of forecast > 0 inside this window.
            pos = np.nan_to_num(fc, nan=0.0) > 0
            prev = np.concatenate([[False], pos[:-1]])
            n_stretches += int((pos & ~prev).sum())

    a = np.asarray(in_rets, dtype=float)
    b = np.asarray(out_rets, dtype=float)
    n_in, n_out = len(a), len(b)

    diff = None
    t = None
    if n_in >= 2 and n_out >= 2:
        diff = float(a.mean() - b.mean())
        tt = stats.ttest_ind(a, b, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    elif n_in >= 1 and n_out >= 1:
        diff = float(a.mean() - b.mean())

    sup = None
    if n_in >= 1 and n_out >= 1:
        sup = float((a > 0).mean() - (b > 0).mean())

    counts = {
        "in-stretch bars": int(n_in),
        "out-of-stretch bars": int(n_out),
        "distinct up-cross stretches": int(n_stretches),
    }

    if n_in < 100 or n_out < 100 or n_stretches < 3:
        status = "inconclusive"
        decided = "There are fewer than 100 in-stretch bars, fewer than 100 out-of-stretch bars, or fewer than 3 distinct up-cross stretches, so the result is inconclusive whatever the t."
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so |t| < 2 cannot be excluded and the result is inconclusive."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "The in-stretch minus out-of-stretch mean next-bar return is positive with Welch t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The difference is negative with Welch t <= -2: moves after up crosses reverse."
    else:
        status = "inconclusive"
        decided = "|t| < 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "share of up next-bars in-stretch minus out-of-stretch",
            "value": sup,
            "passed": (sup > 0) if sup is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "In-stretch bars are forecast > 0 and out-of-stretch bars are forecast = 0, with every bar that has a next close in the same window pooled across windows. Distinct up-cross stretches are maximal runs of forecast > 0 within each window. The supporting check passes when its value is above zero.",
    }
