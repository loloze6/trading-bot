import numpy as np
import pandas as pd


def measure(bars):
    def _f(x):
        try:
            x = float(x)
        except Exception:
            return None
        return x if np.isfinite(x) else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            ret1 = close / close.shift(1) - 1.0
            rng = high - low
            mean_rng = rng.rolling(20, min_periods=20).mean()  # bar t included
            up = ret1 > 0.0
            wide = rng / mean_rng > 1.0
            computable = ret1.notna() & mean_rng.notna() & (mean_rng > 0)
            sit = up & wide
            if "regime" in d.columns:
                reg_sit = d["regime"].astype(str) == "trending"
            else:
                reg_sit = pd.Series(False, index=d.index)
            sit_full = np.where(computable, sit, reg_sit)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit_full, index=d.index).astype(bool) & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean next-day unusual move in the short direction on forecast<0 bars"
    threshold = "confirm: mean > 0 with t >= 2 over >= 100 distinct days and upper half beats lower half; reject: mean < 0 with t <= -2 over >= 100 distinct days"
    reading = ("Situation computed from prices as 1-day return > 0 and high-low range above its 20-bar mean (bar t included), "
               "falling back to regime=='trending' on the first bars of a window where it cannot be computed, side short (forecast < 0); "
               "coin mean daily return is the mean of all within-window next-day returns over all its windows; t clusters cases by UTC date; "
               "the median split puts abs(forecast) > median in the upper half and <= median in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _f(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on the short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on an up day with a range above "
                           "its 20-day mean range, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            m = (fc < 0) & nxt.notna() & ts.notna()
            for i in np.where(m.values)[0]:
                coin_cases.append((ts.iloc[i].strftime("%Y-%m-%d"), float(nxt.iloc[i]), float(abs(fc.iloc[i]))))
        if not coin_cases:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for day, r, af in coin_cases:
            rows.append({"day": day, "u": -(r - mu), "absf": af, "coin": coin})

    if rows:
        cases = pd.DataFrame(rows)
    else:
        cases = pd.DataFrame(columns=["day", "u", "absf", "coin"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = None
    t = None
    if n_cases > 0:
        mean_u = float(cases["u"].mean())
        dev = cases["u"] - mean_u
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        if D > 1:
            var = float(np.sum(S ** 2)) / (n_cases ** 2) * D / (D - 1)
            if var > 0:
                t = mean_u / np.sqrt(var)

    sup_val = None
    sup_pass = None
    mu_up = mu_lo = None
    if n_cases > 0:
        med = float(cases["absf"].median())
        upper = cases.loc[cases["absf"] > med, "u"]
        lower = cases.loc[cases["absf"] <= med, "u"]
        if len(upper) > 0 and len(lower) > 0:
            mu_up = float(upper.mean())
            mu_lo = float(lower.mean())
            sup_val = mu_up - mu_lo
            sup_pass = bool(sup_val > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 100."
    elif t is None or mean_u is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 over at least 100 distinct days, and the upper half of abs(forecast) beats the lower half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the upper half of abs(forecast) does not beat the lower half, which the plan calls inconclusive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 100 distinct days."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": _f(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": _f(mean_u),
            "statistic": ({"name": "t of the mean, cases summed per day", "value": _f(t)} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual move, upper minus lower half of abs(forecast)",
            "value": _f(sup_val),
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
