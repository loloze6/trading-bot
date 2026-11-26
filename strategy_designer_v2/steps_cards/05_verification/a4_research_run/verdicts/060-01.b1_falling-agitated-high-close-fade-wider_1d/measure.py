import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.high_close.last_history_value"

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check + cases ----------
    n_active = 0
    n_agree = 0
    cases = []  # (day, |f|, unusual)
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            if len(d) == 0:
                continue
            hi = d["high"].astype(float).values
            lo = d["low"].astype(float).values
            cl = d["close"].astype(float).values
            f = d[FC].astype(float).values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            regime = d["regime"].astype(str).values
            in_sit = (loc >= 0.5) & (regime == "mean_reversion")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
                raw_ok = np.where(np.isfinite(raw), raw >= 0, True)
                in_sit = in_sit & raw_ok
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (f < 0)).sum())

            ts = pd.to_datetime(d["timestamp"], utc=True)
            days = ts.dt.floor("D").values
            mu = coin_mu.get(coin, np.nan)
            for i in range(len(d) - 1):
                if np.isfinite(f[i]) and f[i] < 0:
                    r = cl[i + 1] / cl[i] - 1.0
                    if np.isfinite(r) and np.isfinite(mu):
                        cases.append((days[i], abs(f[i]), mu - r))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "|forecast|-weighted mean unusual move of the short over the next bar"
    thr = "positive with day-clustered t >= 2 to confirm; negative with t <= -2 to reject; at least 30 distinct days"
    reading = ("The situation is location (close-low)/(high-low) >= 0.5 from prices on bars the detector put in "
               "'mean_reversion' (the profile vetoes are read from the regime column since its components are not "
               "recorded) with the raw range position >= 0 where recorded; the day-clustered t of the weighted mean sums "
               "the weighted deviations per UTC day; the supporting halves are |forecast| above the median versus at or "
               "below it, compared by their unweighted mean unusual moves.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close in the upper "
                           "half of the range inside the falling-agitated profile."),
            "reading": reading,
        }

    n_cases = len(cases)
    if n_cases:
        cdf = pd.DataFrame(cases, columns=["day", "w", "u"])
    else:
        cdf = pd.DataFrame({"day": [], "w": [], "u": []})
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    m = None
    t = None
    if n_cases and cdf["w"].sum() > 0:
        W = float(cdf["w"].sum())
        m = float((cdf["w"] * cdf["u"]).sum() / W)
        cdf["dev"] = cdf["w"] * (cdf["u"] - m) / W
        dsum = cdf.groupby("day")["dev"].sum().values
        G = len(dsum)
        if G > 1:
            se = float(np.sqrt(G / (G - 1) * np.sum(dsum ** 2)))
            t = float(m / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    sup_t = None
    if n_cases >= 2:
        med = float(cdf["w"].median())
        big = cdf.loc[cdf["w"] > med, "u"].values
        small = cdf.loc[cdf["w"] <= med, "u"].values
        if len(big) >= 1 and len(small) >= 1:
            sup_val = float(np.mean(big) - np.mean(small))
            sup_pass = bool(sup_val > 0)
            if len(big) >= 2 and len(small) >= 2:
                tt = stats.ttest_ind(big, small, equal_var=False).statistic
                sup_t = float(tt) if np.isfinite(tt) else None

    counts = {"short cases": int(n_cases), "distinct days with a short case": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days with a short case, under the plan's minimum of 30."
    elif m is None or t is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("The main measure is positive with t >= 2 over at least 30 distinct days and the larger-|forecast| "
                       "half's mean unusual move exceeds the smaller half's.")
        else:
            status = "inconclusive"
            decided = "The main measure is positive with t >= 2 but the supporting check's difference is not above 0."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2 over at least 30 distinct days."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": ({"name": "t of the mean, cases of one day as one piece of evidence", "value": t}
                                       if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move, larger minus smaller |forecast| half (Welch)"
                                     + (f", Welch t = {sup_t:.3f}" if sup_t is not None else ""),
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
