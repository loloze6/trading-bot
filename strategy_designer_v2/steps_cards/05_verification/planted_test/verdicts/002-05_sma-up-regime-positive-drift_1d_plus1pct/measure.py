import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COMP = "debug_info.components.sma_cross_spread.last_history_value"
    MIN_IN, MIN_OUT, MIN_STRETCH = 100, 100, 3

    # ---------- 1. Situation check ----------
    # Situation: 50-day SMA above 200-day SMA (raw spread > 0); expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", COMP]].copy()
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
            d[COMP] = pd.to_numeric(d[COMP], errors="coerce")
            active = d["forecast"].notna() & (d["forecast"] != 0)
            n_active += int(active.sum())
            ok = active & d[COMP].notna() & (d[COMP] > 0) & (d["forecast"] > 0)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "in-stretch minus out-of-stretch mean next-bar return"
    main_thr = "confirm if positive with Welch t >= 2; reject if negative with Welch t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 50-day SMA "
                           "is above the 200-day SMA, so the config does not trade the plan's cross-to-cross stretch."),
            "reading": "Situation taken as the raw SMA spread (last_history_value) > 0 with a positive forecast.",
        }

    # ---------- 2. Criterion ----------
    in_rets = []
    out_rets = []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["close", "forecast"]].copy()
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
            d = d.reset_index(drop=True)
            nxt = d["close"].shift(-1) / d["close"] - 1.0
            f = d["forecast"]
            valid = nxt.notna() & np.isfinite(nxt) & f.notna()
            in_mask = valid & (f > 0)
            out_mask = valid & (f == 0)
            in_rets.extend(nxt[in_mask].tolist())
            out_rets.extend(nxt[out_mask].tolist())
            # distinct stretches: contiguous runs of forecast > 0 inside the window
            pos = (f > 0).fillna(False).astype(int).values
            if len(pos) > 0:
                starts = np.sum((pos[1:] == 1) & (pos[:-1] == 0)) + (1 if pos[0] == 1 else 0)
                n_stretches += int(starts)

    a = np.asarray(in_rets, dtype=float)
    b = np.asarray(out_rets, dtype=float)
    n_in, n_out = int(len(a)), int(len(b))

    diff = None
    tval = None
    if n_in >= 2 and n_out >= 2:
        diff = float(a.mean() - b.mean())
        t = stats.ttest_ind(a, b, equal_var=False).statistic
        tval = float(t) if np.isfinite(t) else None

    sup_val = None
    sup_pass = None
    if n_in > 0 and n_out > 0:
        sup_val = float((a > 0).mean() - (b > 0).mean())
        sup_pass = bool(sup_val > 0)

    counts = {
        "in-stretch bars": n_in,
        "out-of-stretch bars": n_out,
        "distinct up-cross stretches": int(n_stretches),
    }

    if n_in < MIN_IN or n_out < MIN_OUT or n_stretches < MIN_STRETCH:
        status = "inconclusive"
        decided = ("Fewer than 100 in-stretch bars, 100 out-of-stretch bars or 3 distinct up-cross stretches, "
                   "so the result is inconclusive whatever the t.")
    elif tval is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so no confirm or reject rule is met."
    elif diff > 0 and tval >= 2:
        status = "confirmed"
        decided = "The in-stretch minus out-of-stretch mean next-bar return is positive with t >= 2."
    elif diff < 0 and tval <= -2:
        status = "rejected"
        decided = "The difference is negative with t <= -2, so moves after up crosses reverse."
    else:
        status = "inconclusive"
        decided = "|t| < 2, which the plan rules inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "share of up next-bars in-stretch minus out-of-stretch",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Situation is the raw SMA spread > 0 on long bars. In-stretch means forecast > 0 and "
                    "out-of-stretch means forecast = 0, pooled over all windows with one next-bar return per bar "
                    "inside its window. A distinct up-cross stretch is a contiguous run of forecast > 0 bars within "
                    "one window, and a run already open at the window's start counts. 'Up' means a next-bar "
                    "return > 0, and the supporting check passes if the difference in up shares is > 0."),
    }
