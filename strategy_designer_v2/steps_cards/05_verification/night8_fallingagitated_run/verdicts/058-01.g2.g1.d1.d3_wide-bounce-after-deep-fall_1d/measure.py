import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FALL_COL = "debug_info.components.fall_depth_in_std.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []  # (day, coin, forecast, excess_short)

    for coin, windows in bars.items():
        # coin's mean daily return over all windows together
        all_rets = []
        prepared = {}
        for w, df in windows.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fwd = close.shift(-1) / close - 1.0
            all_rets.append(fwd.dropna().values)
            prepared[w] = (d, close, fwd)
        all_rets = np.concatenate(all_rets) if all_rets else np.array([])
        mu = float(np.mean(all_rets)) if all_rets.size else np.nan

        for w, (d, close, fwd) in prepared.items():
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            ret3_lag1 = close.shift(1) / close.shift(4) - 1.0
            if FALL_COL in d.columns:
                fall = pd.to_numeric(d[FALL_COL], errors="coerce")
                fall = fall.where(fall.notna(), ret3_lag1)
            else:
                fall = ret3_lag1

            active = fc.notna() & (fc != 0)
            known = ret1.notna() & fall.notna()
            sit = (ret1 > 0) & (fall < 0)
            chk = active & known
            n_active += int(chk.sum())
            n_agree += int((chk & sit & (fc < 0)).sum())

            # cases for the criterion
            day = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            is_case = fc.notna() & (fc <= -2) & fwd.notna()
            for i in np.where(is_case.values)[0]:
                ex = -(float(fwd.iloc[i]) - mu)
                case_rows.append((day.iloc[i], coin, float(fc.iloc[i]), ex))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction next-day excess return on bars with forecast <= -2"
    main_thr = "confirm: mean > 0 with t >= 2 on at least 100 cases; reject: mean < 0 with t <= -2 on at least 100 cases"
    sup_name = "top-half minus bottom-half (by |forecast|) mean short excess return, Welch t"
    reading = ("The situation is checked as a 1-day close-to-close return > 0 and a negative 3-day return ending the "
               "previous bar (recorded fall_depth raw value, else recomputed from closes), bars whose prior close is "
               "outside the window left out, profile not required; the coin mean is the mean of all its 1-bar returns "
               "over all windows; the main t clusters case deviations summed per UTC day; the top half is "
               "|forecast| above the cases' median, the bottom half at or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of active bars are short bars on up days after a negative 3-day return "
                           "ending the day before, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = pd.DataFrame(case_rows, columns=["day", "coin", "forecast", "ex"])
    N = int(len(cases))
    n_days = int(cases["day"].nunique()) if N else 0

    mean_ex = float(cases["ex"].mean()) if N else None
    t_main = None
    if N >= 2 and n_days >= 2:
        e = cases["ex"] - mean_ex
        s = e.groupby(cases["day"]).sum().values
        D = len(s)
        var = (D / (D - 1)) * np.sum(s ** 2) / (N ** 2)
        if var > 0:
            t_main = float(mean_ex / np.sqrt(var))

    diff = None
    t_w = None
    n_top = n_bot = 0
    if N >= 2:
        a = cases["forecast"].abs()
        med = float(a.median())
        top = cases.loc[a > med, "ex"].values
        bot = cases.loc[a <= med, "ex"].values
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top >= 1 and n_bot >= 1:
            diff = float(np.mean(top) - np.mean(bot))
        if n_top >= 2 and n_bot >= 2:
            tw = stats.ttest_ind(top, bot, equal_var=False).statistic
            if np.isfinite(tw):
                t_w = float(tw)
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {"cases": N, "days with cases": n_days, "top-half cases": n_top, "bottom-half cases": n_bot}

    if N < 100:
        status = "not observable"
        decided = f"Fewer than 100 cases with forecast <= -2 ({N}), the plan's minimum count."
    elif (mean_ex is not None and t_main is not None and mean_ex < 0 and t_main <= -2):
        status = "rejected"
        decided = "Reject: the main mean is below 0 with t <= -2 on at least 100 cases (bounces keep rising)."
    elif t_w is not None and t_w <= -2:
        status = "rejected"
        decided = "Reject: the top-half minus bottom-half difference has a Welch t <= -2."
    elif (mean_ex is not None and t_main is not None and mean_ex > 0 and t_main >= 2):
        if sup_passed:
            status = "confirmed"
            decided = ("Confirm: the main mean is above 0 with t >= 2 on at least 100 cases and the "
                       "top-half minus bottom-half difference is above 0.")
        else:
            status = "inconclusive"
            decided = ("Inconclusive: a confirming main mean with a size difference at or below 0 whose "
                       "Welch t is above -2.")
    else:
        status = "inconclusive"
        decided = "Inconclusive: the main t is between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_main is None else {"name": "t of the mean, cases summed per day", "value": t_main},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed,
                             "welch_t": t_w},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
