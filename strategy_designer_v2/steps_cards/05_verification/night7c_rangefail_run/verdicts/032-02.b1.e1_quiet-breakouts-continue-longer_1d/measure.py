import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    ER_N, ER_SMOOTH, ER_MAX = 60, 5, 0.3
    BRK_N = 60

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            f = df["forecast"].astype(float)
            change = (c - c.shift(ER_N)).abs()
            vol = c.diff().abs().rolling(ER_N, min_periods=ER_N).sum()
            er = change / vol.replace(0, np.nan)
            er_s = er.rolling(ER_SMOOTH, min_periods=ER_SMOOTH).mean()
            prior_high = c.shift(1).rolling(BRK_N, min_periods=BRK_N).max()
            computable = er_s.notna() & prior_high.notna()
            situ = (er_s < ER_MAX) & (c > prior_high)
            active = f.notna() & (f != 0)
            n_active_uncomputable += int((active & ~computable).sum())
            sel = active & computable
            n_active += int(sel.sum())
            n_agree += int((sel & situ & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_parts = [
        "Situation recomputed as the 60-bar Kaufman efficiency ratio smoothed by a 5-bar simple mean below 0.3 and the close above the highest of the prior 60 closes, long side, on active bars where the record holds enough bars to compute it (earlier active bars left out of the agreement)",
        "cases are the first 2-point forecast rise (holding-period bet) in each 10-bar grid cell from each window's first row, the day-pooled t uses cluster sums of deviations with a G/(G-1) correction, the larger half is entry forecast above the median and the smaller half at or below it, the reject rule is applied before the confirm rule, and the plan's minimum of 30 cases on 30 days gives 'not observable' when not reached",
    ]
    reading = "; ".join(reading_parts) + "."

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars not computable": n_active_uncomputable},
            "decided_by": ("Fewer than 90% of the active bars are long bars where the smoothed 60-bar efficiency ratio "
                           "is below 0.3 and the close breaks the prior 60-bar closing high"
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation"),
            "reading": reading,
        }

    # ---------------- cases ----------------
    rows = []
    for coin, wins in bars.items():
        # normal drift: mean non-overlapping 10-bar return over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    ref = 0.0
                    continue
                if fi - ref >= BAND:
                    bet[i] = True
                    ref = fi
                else:
                    ref = min(ref, fi)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                rows.append({"coin": coin, "day": ts.iloc[t].strftime("%Y-%m-%d"),
                             "unusual": r - drift, "fc": f[t]})

    cases = pd.DataFrame(rows, columns=["coin", "day", "unusual", "fc"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    main_name = "mean unusual 10-bar move per case (long, minus coin's normal 10-bar drift)"
    main_thr = "mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject"
    sup_name = "mean unusual move of larger-forecast half minus smaller-forecast half (Welch t)"

    main_val = float(cases["unusual"].mean()) if n_cases else None
    main_t = None
    if n_cases >= 2:
        dev = cases["unusual"] - main_val
        sums = dev.groupby(cases["day"]).sum().values
        G = len(sums)
        if G >= 2:
            var = (sums ** 2).sum() / (n_cases ** 2) * G / (G - 1)
            se = np.sqrt(var)
            if se > 0:
                main_t = float(main_val / se)

    diff_val, diff_t = None, None
    if n_cases >= 4:
        med = cases["fc"].median()
        hi = cases.loc[cases["fc"] > med, "unusual"].values
        lo = cases.loc[cases["fc"] <= med, "unusual"].values
        if len(hi) >= 2 and len(lo) >= 2:
            diff_val = float(hi.mean() - lo.mean())
            tt = stats.ttest_ind(hi, lo, equal_var=False).statistic
            diff_t = float(tt) if np.isfinite(tt) else None

    # ---------------- decision ----------------
    sup_passed = None
    if diff_val is not None and diff_t is not None:
        sup_passed = bool(diff_val > 0 and diff_t >= 2)

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum of at least 30 cases on at least 30 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    else:
        main_rej = main_t is not None and main_val < 0 and main_t <= -2
        diff_rej = diff_t is not None and diff_val < 0 and diff_t <= -2
        main_conf = main_t is not None and main_val > 0 and main_t >= 2
        if main_rej or diff_rej:
            status = "rejected"
            decided = ("Reject: the mean unusual move is below 0 with t <= -2." if main_rej else
                       "Reject: the larger-minus-smaller forecast difference is below 0 with Welch t <= -2.")
        elif main_conf and sup_passed:
            status = "confirmed"
            decided = ("Confirm: the mean unusual move is above 0 with t >= 2 and the supporting difference "
                       "is above 0 with Welch t >= 2.")
        else:
            status = "inconclusive"
            if main_conf:
                decided = "Inconclusive: the main measure meets the confirm rule but the supporting check does not."
            else:
                decided = "Inconclusive: the main measure meets neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": passed},
        "main_measure": {"name": main_name,
                         "value": main_val,
                         "statistic": ({"name": "t of the mean, cases of the same day pooled", "value": main_t}
                                       if main_t is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name,
                             "value": diff_val,
                             "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
