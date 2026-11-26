import numpy as np
import pandas as pd


def measure(bars):
    act_total = 0
    act_ok = 0
    cases = []  # (day, excess_short, absf)

    for coin, wins in bars.items():
        # coin's mean daily return over all windows together
        all_r = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            all_r.append((c.shift(-1) / c - 1.0).dropna())
        allr = pd.concat(all_r) if all_r else pd.Series(dtype=float)
        mu = float(allr.mean()) if len(allr) else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            n = len(df)
            cv = c.values

            # run of consecutive down closes before bar t, bar t closing up
            run_known = np.zeros(n, dtype=bool)
            run_ok = np.zeros(n, dtype=bool)
            for t in range(1, n):
                if not (cv[t] > cv[t - 1]):
                    run_known[t] = True
                    run_ok[t] = False
                    continue
                k = 0
                j = t - 1
                while j >= 1 and cv[j] < cv[j - 1] and k < 30:
                    k += 1
                    j -= 1
                if k >= 2:
                    run_known[t] = True
                    run_ok[t] = True
                elif j >= 1 or k >= 30:
                    run_known[t] = True
                    run_ok[t] = False
                # else the run may reach back past the window's start: not known from the record's prices

            # falling profile: 60-bar price evolution (percent) below -10
            evo = (c / c.shift(60) - 1.0) * 100.0
            prof_known = evo.notna().values
            prof_ok = (evo < -10).values

            for t in range(n):
                if f.iloc[t] == 0:
                    continue
                act_total += 1
                r_ok = run_ok[t] if run_known[t] else (reg.iloc[t] == "mean_reversion")
                p_ok = prof_ok[t] if prof_known[t] else (reg.iloc[t] == "mean_reversion")
                if r_ok and p_ok and f.iloc[t] < 0:
                    act_ok += 1

            # cases for the criterion (horizon 1 bar: every bar is its own grid cell)
            fwd = (c.shift(-1) / c - 1.0)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for t in range(n):
                if f.iloc[t] < 0 and np.isfinite(fwd.iloc[t]) and np.isfinite(mu) and pd.notna(ts.iloc[t]):
                    cases.append((ts.iloc[t].floor("D"), -(fwd.iloc[t] - mu), abs(f.iloc[t])))

    agreement = float(act_ok / act_total) if act_total else 0.0
    passed = act_total > 0 and agreement >= 0.9
    main_name = "mean next-bar return minus coin mean, short direction, on forecast < 0"
    thr = "confirm: mean > 0 with t >= 2 and check passes; reject: t <= -2"
    reading = ("Profile is the 60-bar close change in percent below -10 and the down-run is counted from closes inside the window, "
               "falling back to the recorded regime where the window lacks the history; t clusters cases by UTC day "
               "(deviations summed per day); top half of |forecast| is cases above the median |forecast|, bottom half at or below; "
               "fewer than 30 case-days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(act_total), "independent case-days": None},
            "decided_by": ("Fewer than 90% of active bars are short bars on an up close after >=2 down closes in a falling (60-bar < -10%) market."),
            "reading": reading,
        }

    cdf = pd.DataFrame(cases, columns=["day", "x", "absf"])
    n_cases = len(cdf)
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean = float(cdf["x"].mean()) if n_cases else None
    tval = None
    if n_cases >= 2:
        dev = cdf["x"] - mean
        ds = dev.groupby(cdf["day"]).sum()
        G = len(ds)
        se = np.sqrt((ds ** 2).sum() * (G / (G - 1.0) if G > 1 else 1.0)) / n_cases
        tval = float(mean / se) if se > 0 else None

    diff = None
    chk = None
    if n_cases >= 2:
        med = cdf["absf"].median()
        top = cdf.loc[cdf["absf"] > med, "x"]
        bot = cdf.loc[cdf["absf"] <= med, "x"]
        if len(top) and len(bot):
            diff = float(top.mean() - bot.mean())
            chk = bool(diff > 0)

    counts = {"independent case-days": n_days, "cases": int(n_cases), "active bars": int(act_total)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent case-days, below the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero spread), so neither rule is met."
    elif mean > 0 and tval >= 2 and chk:
        status = "confirmed"
        decided = "Mean short-direction excess return > 0 with t >= 2 and the top-half minus bottom-half difference > 0."
    elif tval <= -2:
        status = "rejected"
        decided = "Mean short-direction excess return has t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed (top half not larger than bottom half)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases summed per day", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "excess return top half minus bottom half of |forecast|", "value": diff, "passed": chk},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
