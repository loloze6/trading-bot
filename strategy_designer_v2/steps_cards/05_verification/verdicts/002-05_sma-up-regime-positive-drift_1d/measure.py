import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COMP = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1) Situation check ----------
    # The situation is the stretch where SMA50 > SMA200 (raw spread > 0), and the expected side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            if "forecast" not in df.columns or COMP not in df.columns:
                continue
            sub = df[["forecast", COMP]].dropna()
            f = sub["forecast"].astype(float).values
            s = sub[COMP].astype(float).values
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & (s > 0) & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "in-stretch minus out-of-stretch mean next-bar return"
    threshold_txt = ("confirm if difference > 0 with Welch t >= 2; reject if difference < 0 "
                     "with t <= -2; |t| < 2 inconclusive; needs >=100 in-stretch bars, "
                     ">=100 out-of-stretch bars, >=3 distinct up-cross stretches")

    if not passed:
        if agreement is None:
            why = ("The forecast is never non-zero, so no active bar can be checked "
                   "against the plan's SMA50-above-SMA200 long situation.")
        else:
            why = (f"Only {agreement:.1%} of active bars are long bars with SMA50 above SMA200, "
                   "below the 90% needed: the forecast is not positive only inside the cross-to-cross stretch.")
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement),
                                "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"in-stretch bars": None, "out-of-stretch bars": None,
                       "distinct up-cross stretches": None},
            "decided_by": why,
            "reading": "none",
        }

    # ---------- 2) Criterion ----------
    in_rets, out_rets = [], []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0  # within this window only
            fc = df["forecast"].astype(float)
            ok = nxt.notna() & fc.notna() & np.isfinite(nxt)
            in_mask = ok & (fc > 0)
            out_mask = ok & (fc == 0)
            in_rets.extend(nxt[in_mask].tolist())
            out_rets.extend(nxt[out_mask].tolist())

            # Distinct up-cross stretches: maximal runs of raw spread > 0 within each window.
            s = df[COMP].astype(float)
            pos = (s > 0) & s.notna()
            arr = pos.values.astype(int)
            starts = int(((arr[1:] == 1) & (arr[:-1] == 0)).sum()) + (1 if len(arr) and arr[0] == 1 else 0)
            n_stretches += starts

    in_rets = np.array(in_rets, dtype=float)
    out_rets = np.array(out_rets, dtype=float)
    n_in, n_out = len(in_rets), len(out_rets)

    diff = None
    t = None
    if n_in >= 2 and n_out >= 2:
        diff = float(in_rets.mean() - out_rets.mean())
        tt = stats.ttest_ind(in_rets, out_rets, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    elif n_in >= 1 and n_out >= 1:
        diff = float(in_rets.mean() - out_rets.mean())

    sup_val = None
    if n_in > 0 and n_out > 0:
        sup_val = float((in_rets > 0).mean() - (out_rets > 0).mean())
    sup_passed = None if sup_val is None else bool(sup_val > 0)

    enough = n_in >= 100 and n_out >= 100 and n_stretches >= 3
    if not enough:
        status = "inconclusive"
        decided = (f"The minimum counts are not met ({n_in} in-stretch bars, {n_out} out-of-stretch bars, "
                   f"{n_stretches} up-cross stretches; needed 100, 100 and 3), so the result is inconclusive whatever the t.")
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so |t| >= 2 is not shown and the result is inconclusive."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "The in-stretch minus out-of-stretch mean next-bar return is positive with Welch t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The in-stretch minus out-of-stretch mean next-bar return is negative with Welch t <= -2."
    else:
        status = "inconclusive"
        decided = "The Welch t has |t| < 2, which the plan rules inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": None if t is None else {"name": "Welch t", "value": t},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "share of up next-bars in-stretch minus out-of-stretch",
            "value": sup_val,
            "passed": sup_passed,
        },
        "counts": {
            "in-stretch bars": int(n_in),
            "out-of-stretch bars": int(n_out),
            "distinct up-cross stretches": int(n_stretches),
        },
        "decided_by": decided,
        "reading": ("In-stretch and out-of-stretch bars are those with forecast > 0 and forecast = 0 that have "
                    "a next bar in the same window. A distinct up-cross stretch is each maximal run of raw "
                    "SMA spread > 0 within a window, including a run already under way at the window's first bar."),
    }
