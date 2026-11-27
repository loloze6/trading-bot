import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.run_loss.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    coin_mean = {}
    rows = []  # (coin, day, excess_short, abs_forecast)

    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            r = pd.Series(c).shift(-1).values / c - 1.0
            all_rets.append(r[~np.isnan(r)])
        coin_mean[coin] = float(np.concatenate(all_rets).mean()) if all_rets else np.nan

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for t in range(n):
                if np.isnan(f[t]) or f[t] == 0:
                    continue
                n_active += 1
                if t >= 3:
                    sit = (c[t] > c[t - 1]) and (c[t - 1] < c[t - 2]) and (c[t - 2] < c[t - 3])
                else:
                    # run's history before the window's first rows is not in the record:
                    # fall back on the recorded run loss (present and positive only on an up close ending a down run)
                    sit = (not np.isnan(raw[t])) and raw[t] > 0 and (t < 1 or c[t] > c[t - 1])
                if sit and f[t] < 0:
                    n_agree += 1
            # events for the criterion
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(n - 1):
                if np.isnan(f[t]) or not (f[t] < 0):
                    continue
                ret = c[t + 1] / c[t] - 1.0
                if np.isnan(ret):
                    continue
                exc = -(ret - coin_mean[coin])
                rows.append((coin, ts.iloc[t].floor("D"), exc, abs(f[t])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    reading = ("Situation = up close after at least 2 strictly lower consecutive closes inside the window "
               "(first 3 rows of a window use the recorded run loss > 0 instead); main mean is the mean over cases "
               "and its t is on per-day sums; deeper half = |forecast| strictly above the median; the plan's "
               "minimum counts (100 event bars with a next-day return, 80 distinct days) give 'not observable'.")

    main_name = "next-day short-direction return minus coin mean daily return on event bars"
    main_thr = "mean > 0 with t >= 2 confirms; t <= -2 rejects"
    sup_name = "deeper-half minus shallower-half mean short excess return (split at median |forecast|)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of non-zero forecast bars are short forecasts on an up close ending a run "
                           "of at least 2 down closes, so the config does not do what the Fidelity states."),
            "reading": reading,
        }

    ev = pd.DataFrame(rows, columns=["coin", "day", "exc", "absf"])
    n_events = int(len(ev))
    n_days = int(ev["day"].nunique()) if n_events else 0
    counts = {"event bars": n_events, "distinct days": n_days}

    mean_main = float(ev["exc"].mean()) if n_events else None
    t_main = None
    if n_days >= 2:
        ds = ev.groupby("day")["exc"].sum()
        sd = ds.std(ddof=1)
        t_main = float(ds.mean() / (sd / np.sqrt(len(ds)))) if sd > 0 else None

    diff = None
    welch_t = None
    if n_events >= 2:
        med = ev["absf"].median()
        deep = ev.loc[ev["absf"] > med, "exc"]
        shal = ev.loc[ev["absf"] <= med, "exc"]
        if len(deep) > 0 and len(shal) > 0:
            diff = float(deep.mean() - shal.mean())
        if len(deep) >= 2 and len(shal) >= 2:
            wt = stats.ttest_ind(deep.values, shal.values, equal_var=False).statistic
            welch_t = float(wt) if np.isfinite(wt) else None

    sup_passed = (diff > 0) if diff is not None else None

    result = {
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_main,
                         "statistic": ({"name": "t of the mean (per-day sums)", "value": t_main}
                                       if t_main is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed,
                             "welch_t": welch_t},
        "counts": counts,
        "reading": reading,
    }

    if n_events < 100 or n_days < 80:
        result["status"] = "not observable"
        result["decided_by"] = ("Minimum not reached: at least 100 event bars over at least 80 distinct days are "
                                f"required, got {n_events} over {n_days}.")
        return result

    if t_main is not None and t_main <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "Reject rule: the main measure's t is <= -2 (rises follow run breaks)."
    elif welch_t is not None and welch_t <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "Reject rule: the deeper-minus-shallower Welch t is <= -2 (deeper runs give back less)."
    elif (mean_main is not None and mean_main > 0 and t_main is not None and t_main >= 2
          and diff is not None and diff > 0):
        result["status"] = "confirmed"
        result["decided_by"] = ("Confirm rule: main mean above 0 with t >= 2 and the deeper-minus-shallower "
                                "difference above 0.")
    else:
        result["status"] = "inconclusive"
        if mean_main is not None and mean_main > 0 and t_main is not None and t_main >= 2:
            result["decided_by"] = ("Inconclusive rule: the main measure confirms but the deeper-minus-shallower "
                                    "difference is at or below 0 with Welch t above -2.")
        else:
            result["decided_by"] = "Inconclusive rule: the main t lies between -2 and 2 and no reject rule is met."
    return result
