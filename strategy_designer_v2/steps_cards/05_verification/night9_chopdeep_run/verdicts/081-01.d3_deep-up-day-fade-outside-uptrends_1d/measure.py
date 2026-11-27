import numpy as np
import pandas as pd
from scipy import stats


def _to_dt(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 1
    MIN_DAYS = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    cases = []        # (day, short-direction unusual return, |forecast|)
    coin_means = {}

    for coin, wins in bars.items():
        # coin's mean daily return over all its windows (never across windows)
        all_r = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                all_r.append(r[np.isfinite(r)])
        all_r = np.concatenate(all_r) if all_r else np.array([])
        coin_mean = float(np.mean(all_r)) if len(all_r) else np.nan
        coin_means[coin] = coin_mean

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
            ret1 = close / close.shift(1) - 1.0
            ret60 = close / close.shift(60) - 1.0
            fwd = close.shift(-H) / close - 1.0
            days = _to_dt(df["timestamp"]).dt.floor("D").reset_index(drop=True)

            active = fc.notna() & (fc != 0)
            computable = ret1.notna() & ret60.notna()
            situ = (ret1 > 0) & (ret60 <= 0.10)
            agree = active & computable & situ & (fc < 0)
            n_active += int((active & computable).sum())
            n_active_uncomputable += int((active & ~computable).sum())
            n_agree += int(agree.sum())

            # cases for the main measure: forecast < 0, next-day return in window
            if np.isfinite(coin_mean):
                sel = fc.notna() & (fc < 0) & fwd.notna()
                for i in np.where(sel.values)[0]:
                    cases.append((days.iloc[i], -(fwd.iloc[i] - coin_mean), abs(fc.iloc[i])))

    reading = ("The 1-day and 60-day returns are recomputed from closes inside each window, and active bars "
               "without 60 prior bars in their window are left out of the agreement share; the 100-day minimum "
               "is treated as the plan's minimum count (not observable when unmet); cases of one day are pooled "
               "by summing their deviations per day (clustered standard error with G/(G-1) correction); the "
               "supporting check splits active bars with a next-day return into |forecast| above the median "
               "(deeper) versus at or below it (shallower).")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-direction next-day return minus coin mean, days pooled",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 100 days"},
            "supporting_check": None,
            "counts": {"days": 0, "active bars": 0},
            "decided_by": "No active bar with computable situation in the record, so the idea could not be shown.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.90:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of active bars are up days (1-day return > 0) with a 60-day return "
                           "at most +10 % carrying a short forecast, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    cdf = pd.DataFrame(cases, columns=["day", "x", "absf"])
    n_cases = len(cdf)
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    mean_x = float(cdf["x"].mean()) if n_cases else np.nan
    t_main = np.nan
    if n_days >= 2:
        dev = cdf["x"] - mean_x
        S = dev.groupby(cdf["day"]).sum().values
        G = len(S)
        var = (G / (G - 1)) * np.sum(S ** 2) / (n_cases ** 2)
        if var > 0:
            t_main = mean_x / np.sqrt(var)

    # ---------- supporting check ----------
    sup_val, sup_t, sup_pass = None, None, None
    if n_cases >= 4:
        med = float(np.median(cdf["absf"].values))
        deep = cdf.loc[cdf["absf"] > med, "x"].values
        shal = cdf.loc[cdf["absf"] <= med, "x"].values
        if len(deep) >= 2 and len(shal) >= 2:
            sup_val = float(np.mean(deep) - np.mean(shal))
            tt = stats.ttest_ind(deep, shal, equal_var=False).statistic
            sup_t = float(tt) if np.isfinite(tt) else None
            sup_pass = bool(sup_t is not None and sup_t > 0)

    counts = {"days with cases": n_days, "cases": int(n_cases), "active bars": int(n_active)}
    main = {
        "name": "mean short-direction next-day return minus coin mean daily return, days pooled",
        "value": mean_x if np.isfinite(mean_x) else None,
        "statistic": {"name": "t of the mean (day-pooled)",
                      "value": float(t_main) if np.isfinite(t_main) else None},
        "threshold": "t >= 2 over at least 100 days (with deeper-half check) to confirm; t <= -2 over at least 100 days to reject",
    }
    support = {"name": "deeper-half minus shallower-half mean unusual short return, Welch t > 0",
               "value": sup_t, "passed": sup_pass}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} days with cases, below the plan's minimum of 100 days."
    elif not np.isfinite(t_main):
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so it is neither >= 2 nor <= -2."
    elif t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more over at least 100 days and the deeper half fades more (Welch t > 0)."
    elif t_main <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less over at least 100 days."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the deeper half does not fade more than the shallower half."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
