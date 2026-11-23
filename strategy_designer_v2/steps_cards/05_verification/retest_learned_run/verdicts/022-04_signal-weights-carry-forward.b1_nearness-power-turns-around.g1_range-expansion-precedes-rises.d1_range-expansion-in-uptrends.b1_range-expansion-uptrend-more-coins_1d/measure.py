import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_ratio.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret20 = close / close.shift(20) - 1.0  # inside the window only
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0) & ret20.notna()
            situ = (ret20 > 0) & raw.notna() & (raw > 0)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "upper-half minus lower-half mean excess 5-bar return (split at median forecast)"
    thr = "confirm: difference > 0 with Welch t >= 2 and supporting check; reject: difference < 0 with Welch t <= -2"
    reading = ("The 20-day return is recomputed as close[t]/close[t-20]-1 inside each window, so active bars of a "
               "window's first 20 rows are left out of the agreement; the trending regime for cases is the record's "
               "`regime` column; the coin's mean 5-bar return is the mean of all its non-overlapping grid returns over "
               "all its windows; the median is taken over all cases of all coins pooled; returns are fractions.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with the coin's 20-day "
                           "return above 0 and a recorded range ratio, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    cases = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_rets.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((fc[i], r))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for f, r in coin_cases:
            cases.append((f, r - mu))

    if cases:
        arr = np.array(cases, dtype=float)
        med = float(np.median(arr[:, 0]))
        upper = arr[arr[:, 0] > med, 1]
        lower = arr[arr[:, 0] <= med, 1]
    else:
        upper = np.array([])
        lower = np.array([])
    n_up, n_lo = int(len(upper)), int(len(lower))
    counts = {"cases in upper half": n_up, "cases in lower half": n_lo, "cases": n_up + n_lo}

    diff = float(upper.mean() - lower.mean()) if n_up > 0 and n_lo > 0 else None
    t = None
    if n_up >= 2 and n_lo >= 2:
        tt = stats.ttest_ind(upper, lower, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    sup_val = float(upper.mean()) if n_up > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {"name": main_name, "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": thr}
    sup = {"name": "mean excess 5-bar return of upper-half cases > 0", "value": sup_val, "passed": sup_pass}

    if n_up < 30 or n_lo < 30:
        status = "not observable"
        decided = "Fewer than 30 cases in at least one half, the plan's minimum count, so the data cannot show the idea."
    elif diff is None or t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif diff > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The difference is above 0 with Welch t >= 2 and the upper half's mean excess return is above 0."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The difference is below 0 with Welch t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "Welch t is 2 or more but the supporting check fails (upper-half mean excess return not above 0)."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
