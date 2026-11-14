import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    comp_col = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is "SMA50 above SMA200", which means a raw spread > 0.
    # The expected side is long, because the outcome is a rise.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", comp_col]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (d[comp_col] > 0) & (d["forecast"] > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = ("confirm if difference > 0 with Welch t >= 2; reject if difference < 0 with t <= -2; "
                     "else inconclusive; needs >= 100 in-stretch bars, >= 100 out-of-stretch bars, "
                     ">= 3 distinct up-cross stretches")
    main_name = "mean next-bar return in-stretch minus out-of-stretch"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with the 50-day SMA "
                           "above the 200-day SMA, so the config does not trade the plan's cross-to-cross stretch."),
            "reading": "Situation taken as raw spread > 0 with forecast > 0; rows with missing values left out.",
        }

    # ---------- 2. Criterion ----------
    in_rets = []
    out_rets = []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret = close.shift(-1) / close - 1.0
            fc = df["forecast"]
            m = ret.notna() & fc.notna()
            in_rets.append(ret[m & (fc > 0)].values)
            out_rets.append(ret[m & (fc == 0)].values)

            # Distinct up-cross stretches: contiguous runs of raw spread > 0 within the window.
            raw = df[comp_col]
            pos = (raw > 0) & raw.notna()
            starts = pos & ~pos.shift(1, fill_value=False)
            n_stretches += int(starts.sum())

    in_r = np.concatenate(in_rets) if in_rets else np.array([])
    out_r = np.concatenate(out_rets) if out_rets else np.array([])
    n_in, n_out = int(len(in_r)), int(len(out_r))

    diff = None
    t = None
    if n_in >= 2 and n_out >= 2:
        diff = float(np.mean(in_r) - np.mean(out_r))
        tt = stats.ttest_ind(in_r, out_r, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    sup_val = None
    sup_pass = None
    if n_in > 0 and n_out > 0:
        sup_val = float(np.mean(in_r > 0) - np.mean(out_r > 0))
        sup_pass = bool(sup_val > 0)

    counts = {"in-stretch bars": n_in, "out-of-stretch bars": n_out,
              "distinct up-cross stretches": int(n_stretches)}

    enough = n_in >= 100 and n_out >= 100 and n_stretches >= 3
    if not enough:
        status = "inconclusive"
        decided = ("There are fewer than 100 in-stretch bars, fewer than 100 out-of-stretch bars, or fewer than "
                   "3 distinct up-cross stretches, so the result is inconclusive whatever the t.")
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so the result is inconclusive."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "The in-stretch minus out-of-stretch mean next-bar return is positive with t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The difference is negative with t <= -2, so moves after up crosses reverse."
    else:
        status = "inconclusive"
        decided = "|t| < 2, which is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
                         "threshold": threshold_txt},
        "supporting_check": {"name": "share of up next-bars in-stretch minus out-of-stretch",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Distinct up-cross stretches are counted as contiguous runs of raw spread > 0 within each "
                    "window, a run starting at a window's first row included. The supporting check passes "
                    "when its difference is > 0."),
    }
