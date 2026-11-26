import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"

    # ---------- 1. Situation check ----------
    # Plan: an up day (close above the prior close) in the falling, agitated profile; expected side: short.
    # The up day comes from the prices, inside each window. The profile comes from the regime: the profile's
    # vetoes make a bar "chop", so a bar in the profile is a bar whose regime is not "chop".
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").astype(float).fillna(0.0)
            prev_close = close.shift(1)
            up_day = close > prev_close
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            in_profile = regime != "chop"
            # The first bar of a window has no prior close inside the window, so it is left out of the check.
            known = prev_close.notna() & close.notna()
            active = (fc != 0) & known
            situation_short = up_day & in_profile & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situation_short).sum())

            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D").astype(str)
            for i in range(len(df)):
                if fc.iloc[i] < 0 and np.isfinite(nxt.iloc[i]):
                    rows.append({"coin": coin, "day": day.iloc[i],
                                 "ret": float(nxt.iloc[i]), "absf": abs(float(fc.iloc[i]))})
        mu = float(np.mean(np.concatenate(all_rets))) if all_rets and sum(len(a) for a in all_rets) > 0 else np.nan
        for r in rows:
            if r["coin"] == coin and "mu" not in r:
                r["mu"] = mu

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    reading = ("Cases are bars with forecast < 0 and a next close in the same window; the coin's mean daily return "
               "is over all its 1-bar returns in all windows; the day-clustered t sums each day's deviations from the "
               "mean (SE = sqrt(D/(D-1) * sum of squared day sums) / N); the upper half is |forecast| strictly above "
               "the median, the lower half the rest; the profile in the situation check is read as regime not 'chop' "
               "and each window's first bar is left out of that check.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars on up days in the "
                           "falling agitated profile, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    main_name = "mean unusual next-day move of short cases (day-clustered t)"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2"
    cases = pd.DataFrame(rows)
    if len(cases) > 0:
        cases = cases.dropna(subset=["ret", "mu"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases > 0 else 0
    counts = {"cases across coins": n_cases, "distinct days": n_days}

    mean_u = None
    t_val = None
    diff = None
    sup_pass = None
    if n_cases > 0:
        cases["u"] = -(cases["ret"] - cases["mu"])
        mean_u = float(cases["u"].mean())
        dev = cases["u"] - mean_u
        S = dev.groupby(cases["day"]).sum()
        D = len(S)
        if D > 1:
            se = np.sqrt(D / (D - 1.0) * float((S ** 2).sum())) / n_cases
            t_val = float(mean_u / se) if se > 0 else None
        med = float(cases["absf"].median())
        up = cases.loc[cases["absf"] > med, "u"]
        lo = cases.loc[cases["absf"] <= med, "u"]
        if len(up) > 0 and len(lo) > 0:
            diff = float(up.mean() - lo.mean())
            sup_pass = bool(diff > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "day-clustered t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": thr}
    support = {"name": "mean unusual move, upper minus lower half of |forecast|", "value": diff, "passed": sup_pass}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases on 60 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif t_val is None or mean_u is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and wider up days fall more than narrow ones."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails (upper half not above lower half): inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: up days in the profile are followed by rises."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
