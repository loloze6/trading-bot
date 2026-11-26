import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.scaled_rise.last_history_value"
    PROFILE_PERIOD = 60

    # ---------- collect per-window frames, coin drift ----------
    coin_rets = {}
    frames = []
    for coin, wins in bars.items():
        all_r = []
        for wname, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            d["next_ret"] = close.shift(-1) / close - 1.0  # inside the window only
            d["evo60"] = close / close.shift(PROFILE_PERIOD) - 1.0  # NaN where not computable in window
            d["coin"] = coin
            d["window"] = wname
            all_r.append(d["next_ret"].dropna().values)
            frames.append(d)
        allr = np.concatenate(all_r) if all_r else np.array([])
        coin_rets[coin] = float(np.mean(allr)) if len(allr) else np.nan

    if frames:
        data = pd.concat(frames, ignore_index=True)
    else:
        data = pd.DataFrame(columns=["forecast", "regime", RAW, "next_ret", "evo60", "coin", "timestamp"])

    fc = pd.to_numeric(data.get("forecast"), errors="coerce")
    raw = pd.to_numeric(data[RAW], errors="coerce") if RAW in data.columns else pd.Series(np.nan, index=data.index)
    regime = data["regime"].astype(str) if "regime" in data.columns else pd.Series("", index=data.index)

    # ---------- situation check ----------
    # rise: raw 1-bar vol-scaled return > 0; falling market: the code's falling profile (regime 'unknown',
    # not vetoed to 'chop') and, where the 60-bar change is computable inside the window, a negative change.
    rise = raw > 0
    evo = data["evo60"]
    falling = (regime == "unknown") & (evo.isna() | (evo < 0))
    expected_side = fc < 0
    active = fc.notna() & (fc != 0)
    n_active = int(active.sum())
    if n_active > 0:
        agree = float((active & rise & falling & expected_side).sum() / n_active)
        passed = agree >= 0.90
    else:
        agree = None
        passed = True

    reading = ("Falling profile taken from the recorded regime ('unknown' = not vetoed to 'chop'), plus a negative "
               "60-bar close change where computable inside the window; next-day return minus the coin's mean daily "
               "return over all its windows, sign-flipped for the short; the weighted mean's t uses day-clustered "
               "standard errors (weighted deviations summed per UTC day, small-sample factor K/(K-1)); the supporting "
               "check uses unweighted group means of the unusual move with Welch's t; fewer than 30 distinct days is "
               "treated as a minimum count not reached (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": "abs(forecast)-weighted mean next-day unusual move, short direction",
                             "value": None, "statistic": None,
                             "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on a one-day rise "
                           "(raw scaled return > 0) in the falling profile, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- cases ----------
    cases = data[(fc < 0) & data["next_ret"].notna()].copy()
    cases["fc"] = fc[cases.index]
    cases["w"] = cases["fc"].abs()
    cases["drift"] = cases["coin"].map(coin_rets)
    cases["u"] = -(cases["next_ret"] - cases["drift"])
    cases = cases[cases["u"].notna() & (cases["w"] > 0)]
    cases["day"] = cases["timestamp"].dt.floor("D")

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    main_value = None
    t_main = None
    if n_cases > 0:
        W = cases["w"].sum()
        m = float((cases["u"] * cases["w"]).sum() / W)
        main_value = m
        dev = cases["w"] * (cases["u"] - m)
        D = dev.groupby(cases["day"]).sum().values
        K = len(D)
        if K > 1:
            se = np.sqrt(np.sum(D ** 2) * K / (K - 1)) / W
            t_main = float(m / se) if se > 0 else None

    # supporting check
    sup_diff = None
    sup_t = None
    sup_pass = None
    if n_cases > 0:
        med = cases["w"].median()
        hi = cases.loc[cases["w"] > med, "u"].values
        lo = cases.loc[cases["w"] <= med, "u"].values
        if len(hi) > 0 and len(lo) > 0:
            sup_diff = float(np.mean(hi) - np.mean(lo))
            if len(hi) > 1 and len(lo) > 1:
                tt = stats.ttest_ind(hi, lo, equal_var=False).statistic
                sup_t = float(tt) if np.isfinite(tt) else None
            sup_pass = bool(sup_diff > 0)

    counts = {"distinct days carrying cases": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days carry cases, fewer than the plan's minimum of 30."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main t could not be computed, so neither the confirm nor the reject rule is met."
    elif main_value > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = ("The weighted mean unusual move is positive with t >= 2 and the larger-forecast minus "
                   "smaller-forecast difference is above 0.")
    elif main_value < 0 and t_main <= -2:
        status = "rejected"
        decided = ("The weighted mean unusual move is negative with t <= -2: the coin rises after sharp up days "
                   "more than its drift.")
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the supporting difference is at or below 0 (or not computable)."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": {"name": "abs(forecast)-weighted mean next-day unusual move, short direction",
                         "value": main_value,
                         "statistic": ({"name": "t of weighted mean, cases of one day pooled", "value": t_main}
                                       if t_main is not None else None),
                         "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject"},
        "supporting_check": {"name": "unusual move above-median minus at-or-below-median abs(forecast) (Welch t "
                                     + (f"{sup_t:.3f}" if sup_t is not None else "n/a") + ")",
                             "value": sup_diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
