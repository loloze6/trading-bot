import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RNG_COL_LEN = 20
    rows_check = []
    cases = []
    coin_means = {}

    # ---------- per coin: situation recomputation, next-day returns, coin mean ----------
    for coin, wins in bars.items():
        all_rets = []
        per_win = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp").reset_index(drop=True)
            h = pd.to_numeric(d["high"], errors="coerce")
            l = pd.to_numeric(d["low"], errors="coerce")
            c = pd.to_numeric(d["close"], errors="coerce")
            width = h - l
            mean_rng = width.rolling(RNG_COL_LEN, min_periods=RNG_COL_LEN).mean()
            rng = width / mean_rng.replace(0, np.nan)
            loc = (c - l) / width.replace(0, np.nan)
            situation = (rng >= 1.5) & (loc <= 0.25)
            computable = rng.notna() & loc.notna()
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            ret1 = c.shift(-1) / c - 1.0
            all_rets.append(ret1.dropna().values)
            per_win.append((d, fc, situation, computable, ret1))
        coin_means[coin] = float(np.mean(np.concatenate(all_rets))) if all_rets and sum(len(a) for a in all_rets) > 0 else np.nan

        for d, fc, situation, computable, ret1 in per_win:
            active = fc != 0
            sel = active & computable
            for i in np.where(sel.values)[0]:
                rows_check.append(bool(situation.iloc[i]) and fc.iloc[i] > 0)
            reg = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            sig = (reg == "mean_reversion") & (fc > 0) & ret1.notna()
            ts = pd.to_datetime(d["timestamp"], utc=True) if "timestamp" in d.columns else pd.Series(pd.NaT, index=d.index)
            for i in np.where(sig.values)[0]:
                cases.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D"),
                    "forecast": float(fc.iloc[i]),
                    "ret": float(ret1.iloc[i]),
                })

    n_checked = len(rows_check)
    agreement = float(np.mean(rows_check)) if n_checked > 0 else None
    passed_sit = agreement is not None and agreement >= 0.9

    reading = ("The plan's situation is recomputed from prices as range(t)/mean of the last 20 bar ranges including t >= 1.5 "
               "and (close-low)/(high-low) <= 0.25, and the agreement is taken over active bars where these are computable "
               "(the first 19 bars of each window lack history); 'cases (signal days)' are coin-day signal bars, the t pools "
               "a day's cases by summing their deviations (cluster-robust by day), and cases equal to the median forecast "
               "are left out of both supporting groups.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_checked)},
            "decided_by": ("Fewer than 90% of active bars are wide-range low-close days with a long forecast, "
                           "so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    cdf = pd.DataFrame(cases)
    n_cases = int(len(cdf))
    if n_cases > 0:
        cdf["excess"] = cdf["ret"] - cdf["coin"].map(coin_means)
        cdf = cdf[cdf["excess"].notna()]
        n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases > 0 else 0

    mean_ex = None
    t_main = None
    if n_cases > 0:
        x = cdf["excess"].values
        mean_ex = float(np.mean(x))
        resid = cdf.assign(r=cdf["excess"] - mean_ex).groupby("day")["r"].sum().values
        G = len(resid)
        if G > 1:
            se = np.sqrt(G / (G - 1) * np.sum(resid ** 2)) / n_cases
            t_main = float(mean_ex / se) if se > 0 else None

    diff = None
    t_sup = None
    n_hi = n_lo = 0
    if n_cases > 0:
        med = float(np.median(cdf["forecast"].values))
        hi = cdf.loc[cdf["forecast"] > med, "excess"].values
        lo = cdf.loc[cdf["forecast"] < med, "excess"].values
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            diff = float(np.mean(hi) - np.mean(lo))
            if n_hi > 1 and n_lo > 1:
                tt = stats.ttest_ind(hi, lo, equal_var=False)
                t_sup = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = (diff > 0) if diff is not None else False

    counts = {"cases (signal days)": n_cases, "distinct days": n_days,
              "cases above median": n_hi, "cases below median": n_lo}

    main = {
        "name": "mean next-day excess return on signal bars (day-pooled)",
        "value": mean_ex,
        "statistic": {"name": "t of the mean, cases of one day pooled", "value": t_main} if t_main is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and high-minus-low > 0; reject: mean < 0 with t <= -2",
    }
    sup = {"name": "high-minus-low forecast excess return (Welch t %s)" % (
        "%.3f" % t_sup if t_sup is not None else "n/a"), "value": diff, "passed": bool(sup_passed)}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 30 cases (signal days) in total."
    elif mean_ex is not None and t_main is not None and mean_ex > 0 and t_main >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean excess return above 0 with t >= 2 and a high-minus-low difference above 0."
        else:
            status = "inconclusive"
            decided = "A confirming main measure with a high-minus-low difference at or below 0 is inconclusive."
    elif mean_ex is not None and t_main is not None and mean_ex < 0 and t_main <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (or cannot be computed)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
