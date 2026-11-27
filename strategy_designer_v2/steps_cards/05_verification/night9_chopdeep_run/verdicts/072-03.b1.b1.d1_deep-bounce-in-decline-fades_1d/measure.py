import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0)
            regime = d["regime"].astype(str)
            day_ret = close / close.shift(1) - 1.0
            ret20 = close / close.shift(20) - 1.0
            computable = day_ret.notna() & ret20.notna()
            cond_prices = (day_ret > 0) & (ret20 < 0)
            # where the lookback lies before the window's first recorded bar, the detector's own decision stands in
            cond = np.where(computable, cond_prices, regime == "mean_reversion")
            choppy = regime != "chop"
            situation = pd.Series(cond, index=d.index).astype(bool) & choppy
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("Day return and 20-bar return are recomputed from closes inside each window (the regime column "
               "stands in where the lookback precedes the window's first bar) and the choppy profile is read as "
               "regime != 'chop'; a short bet is a fall of the forecast of at least 2 points from its shallowest "
               "short level since the last bet (from 0 after flat), the first bet of each 10-bar grid cell counts as "
               "the case, the drift is the coin's mean 10-bar return on the grid of all its windows, the t clusters "
               "deviations by UTC day, and the deeper half is |forecast| strictly above the cases' median against "
               "the rest.")

    main_name = "mean unusual 10-bar move in the short direction"
    main_thr = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are choppy up-days with a negative "
                           "20-day return carrying a short forecast, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean of 10-bar returns on the non-overlapping grid of all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    prev_short = False
                    continue
                mag = -f
                if not prev_short:
                    ref = 0.0
                prev_short = True
                if mag - ref >= BAND:
                    bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0 or not np.isfinite(drift[coin]):
                    continue
                r = c1 / c0 - 1.0
                cases.append({
                    "day": ts.iloc[i].floor("D"),
                    "x": -(r - drift[coin]),
                    "absf": abs(fc[i]),
                })

    cdf = pd.DataFrame(cases)
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days carrying cases": n_days}

    mean = float(cdf["x"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["x"] - mean
        S = dev.groupby(cdf["day"]).sum().values
        G = len(S)
        var = (S ** 2).sum() / (n_cases ** 2) * G / (G - 1)
        se = np.sqrt(var)
        t = float(mean / se) if se > 0 else None

    sup_val = None
    if n_cases >= 2:
        med = cdf["absf"].median()
        deep = cdf.loc[cdf["absf"] > med, "x"]
        shal = cdf.loc[cdf["absf"] <= med, "x"]
        if len(deep) > 0 and len(shal) > 0:
            sup_val = float(deep.mean() - shal.mean())
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {"name": main_name, "value": mean,
            "statistic": {"name": "t of the mean, cases clustered by day", "value": t} if t is not None else None,
            "threshold": main_thr}
    support = {"name": "deeper half minus shallower half mean unusual move", "value": sup_val, "passed": sup_pass}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Fewer than 30 distinct days carry cases ({n_days})."
    elif mean is None or t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif mean > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the deeper half beats the shallower half."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: these bars rise more than the coin's drift."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "A positive main measure with t >= 2 but a supporting check at 0 or below (or not computable)."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
