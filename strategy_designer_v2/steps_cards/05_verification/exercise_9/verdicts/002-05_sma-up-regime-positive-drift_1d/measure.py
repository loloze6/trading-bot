import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    SPREAD_COL = "debug_info.components.sma_cross_spread.last_history_value"
    MIN_IN, MIN_OUT, MIN_STRETCH = 100, 100, 3
    threshold_txt = ("confirm if in-minus-out mean next-bar return > 0 with Welch t >= 2; "
                     "reject if < 0 with t <= -2; |t| < 2 inconclusive; needs >= 100 in-stretch bars, "
                     ">= 100 out-of-stretch bars and >= 3 distinct up-cross stretches")
    reading = ("In-stretch bars are rows with forecast > 0 and out-of-stretch rows with forecast == 0; "
               "the situation is the raw 50/200 SMA spread > 0 on the long side; distinct up-cross stretches "
               "are counted as contiguous runs of forecast > 0 inside each window (a run cut by a window "
               "boundary counts in each window); the supporting check passes when the up-share difference is > 0; "
               "a missing minimum count gives 'not observable' as the task prescribes.")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            if "forecast" not in df.columns or SPREAD_COL not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            s = pd.to_numeric(df[SPREAD_COL], errors="coerce")
            ok = f.notna()
            active = ok & (f != 0)
            n_active += int(active.sum())
            agree = active & s.notna() & (s > 0) & (f > 0)
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True  # vacuous; minimum counts will decide

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "in-stretch minus out-of-stretch mean next-bar return",
                             "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"in-stretch bars": None, "out-of-stretch bars": None,
                       "distinct up-cross stretches": None},
            "decided_by": (f"Only {agreement:.1%} of the active bars have forecast > 0 while the 50-day SMA "
                           "is above the 200-day SMA, below the 90% needed: the config's forecast does not "
                           "follow the plan's long-only cross-to-cross stretch."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    r_in, r_out = [], []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)

            # stretches: contiguous runs of forecast > 0
            pos = np.where(np.isnan(f), False, f > 0)
            prev = np.concatenate([[False], pos[:-1]])
            n_stretches += int(np.sum(pos & ~prev))

            if len(c) < 2:
                continue
            ret = c[1:] / c[:-1] - 1.0
            ff = f[:-1]
            valid = ~np.isnan(ret) & ~np.isnan(ff) & np.isfinite(ret)
            r_in.extend(ret[valid & (ff > 0)].tolist())
            r_out.extend(ret[valid & (ff == 0)].tolist())

    r_in = np.asarray(r_in, dtype=float)
    r_out = np.asarray(r_out, dtype=float)
    n_in, n_out = int(len(r_in)), int(len(r_out))
    counts = {"in-stretch bars": n_in, "out-of-stretch bars": n_out,
              "distinct up-cross stretches": int(n_stretches)}

    diff = None
    t = None
    if n_in > 0 and n_out > 0:
        diff = float(r_in.mean() - r_out.mean())
    if n_in >= 2 and n_out >= 2:
        tt = stats.ttest_ind(r_in, r_out, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    sup_val = None
    sup_pass = None
    if n_in > 0 and n_out > 0:
        sup_val = float(np.mean(r_in > 0) - np.mean(r_out > 0))
        sup_pass = bool(sup_val > 0)

    main = {"name": "in-stretch minus out-of-stretch mean next-bar return",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": threshold_txt}
    supporting = {"name": "share of up next-bars in-stretch minus out-of-stretch",
                  "value": sup_val, "passed": sup_pass}

    missing = []
    if n_in < MIN_IN:
        missing.append(f"in-stretch bars {n_in} < {MIN_IN}")
    if n_out < MIN_OUT:
        missing.append(f"out-of-stretch bars {n_out} < {MIN_OUT}")
    if n_stretches < MIN_STRETCH:
        missing.append(f"distinct up-cross stretches {n_stretches} < {MIN_STRETCH}")

    if missing:
        status = "not observable"
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = f"The in-minus-out mean next-bar return is positive ({diff:.5f}) with Welch t = {t:.2f} >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = f"The in-minus-out mean next-bar return is negative ({diff:.5f}) with Welch t = {t:.2f} <= -2."
    else:
        status = "inconclusive"
        decided = f"Welch t = {t:.2f} has |t| < 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
