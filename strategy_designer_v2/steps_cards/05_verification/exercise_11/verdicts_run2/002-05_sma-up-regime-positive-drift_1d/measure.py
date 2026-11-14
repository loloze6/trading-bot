import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    comp_col = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: 50-day SMA above 200-day SMA (raw spread > 0). Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or comp_col not in df.columns:
                continue
            sub = df[["forecast", comp_col]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (sub[comp_col] > 0) & (sub["forecast"] > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "in-stretch minus out-of-stretch mean next-bar return"
    threshold = "confirm if difference > 0 with Welch t >= 2; reject if < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("No active bars: the forecast is never non-zero, so it cannot follow the 50-over-200 SMA stretch."
                           if agreement is None else
                           "Fewer than 90% of active bars are long bars where the 50-day SMA is above the 200-day SMA."),
            "reading": "Situation taken as raw SMA spread > 0 with a positive forecast (long side).",
        }

    # ---------- 2. Criterion ----------
    in_rets, out_rets = [], []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret = close.shift(-1) / close - 1.0  # next-bar return inside the window
            fc = df["forecast"]
            mask = fc.notna() & ret.notna()
            in_rets.extend(ret[mask & (fc > 0)].tolist())
            out_rets.extend(ret[mask & (fc == 0)].tolist())

            # distinct up-cross stretches: runs of raw spread > 0 in this window
            if comp_col in df.columns:
                sp = df[comp_col]
                pos = (sp > 0) & sp.notna()
                starts = pos & ~pos.shift(1, fill_value=False)
                n_stretches += int(starts.sum())

    in_rets = np.asarray(in_rets, dtype=float)
    out_rets = np.asarray(out_rets, dtype=float)
    n_in, n_out = len(in_rets), len(out_rets)

    counts = {
        "in-stretch bars": int(n_in),
        "out-of-stretch bars": int(n_out),
        "distinct up-cross stretches": int(n_stretches),
    }

    diff = None
    t = None
    if n_in > 0 and n_out > 0:
        diff = float(in_rets.mean() - out_rets.mean())
    if n_in >= 2 and n_out >= 2:
        tt = stats.ttest_ind(in_rets, out_rets, equal_var=False)
        if np.isfinite(tt.statistic):
            t = float(tt.statistic)

    sup_val = None
    sup_pass = None
    if n_in > 0 and n_out > 0:
        sup_val = float((in_rets > 0).mean() - (out_rets > 0).mean())
        sup_pass = bool(sup_val > 0)

    reading = ("In-stretch bars are forecast > 0 and out-of-stretch bars forecast = 0, every bar's next-bar return counted once "
               "within its window; distinct up-cross stretches are counted as separate runs of raw SMA spread > 0 in each window "
               "(a run already under way at a window's start counts); the plan's 'inconclusive with fewer cases' is reported as "
               "'not observable' per the minimum-count rule.")

    if n_in < 100 or n_out < 100 or n_stretches < 3:
        missing = []
        if n_in < 100:
            missing.append(f"{n_in} in-stretch bars < 100")
        if n_out < 100:
            missing.append(f"{n_out} out-of-stretch bars < 100")
        if n_stretches < 3:
            missing.append(f"{n_stretches} up-cross stretches < 3")
        status = "not observable"
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif t is not None and diff is not None and diff > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm rule: the in-stretch minus out-of-stretch mean next-bar return is positive with t >= 2."
    elif t is not None and diff is not None and diff < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule: the difference is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: |t| < 2 (or t undefined)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": None if t is None else {"name": "Welch t", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of up next-bars in-stretch minus out-of-stretch",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
