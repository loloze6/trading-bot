import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    REG = "regime"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    coin_means = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            rets.append(r.dropna())
            s = r.rolling(30, min_periods=30).std()
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            rng_sw = ((h - l) / c) / s
            hl = (h - l).replace(0, np.nan)
            loc = (h - c) / hl
            # wide day closing near its low, recomputed from prices where the 30-day swing exists
            shape_ok = (rng_sw >= 2.0) & (loc >= 0.667)
            shape_known = s.notna() & hl.notna()
            regime_ok = d[REG].astype(str) == "mean_reversion"
            # rising-calm profile: not computable from the windows (365-bar percentile), taken from the detector's regime
            situation = np.where(shape_known, shape_ok & regime_ok, regime_ok)
            f = d[FC].astype(float).fillna(0.0)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_means[coin] = float(allr.mean()) if len(allr) else np.nan

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean next-day return minus coin's mean daily return, forecast > 0 cases, before costs"
    main_thr = "mean > 0 with t >= 2 confirms; t <= -2 rejects; |t| < 2 inconclusive"
    sup_name = "correlation between forecast and next-day excess return"
    reading = ("The rising-calm profile is taken from the recorded regime (its 365-bar volatility percentile and 60-bar "
               "trend cannot be rebuilt inside the windows) while width and nearness to the low are recomputed from prices; "
               "the day-pooled t is the mean excess per case over its standard error clustered by UTC day (deviations "
               "summed per day), and the correlation's t is r*sqrt((n-2)/(1-r^2)) over all cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a wide day "
                           "(range >= 2 swings) closing in the lower third inside the rising-calm regime."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, fs, days = [], [], []
    for coin, wins in bars.items():
        mu = coin_means.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            f = d[FC].astype(float).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(len(d) - 1):
                if np.isfinite(f[i]) and f[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + 1]) and c[i] != 0:
                    xs.append(c[i + 1] / c[i] - 1.0 - mu)
                    fs.append(f[i])
                    days.append(ts.iloc[i].floor("D"))
    x = np.array(xs, dtype=float)
    fv = np.array(fs, dtype=float)
    n_cases = int(len(x))
    dser = pd.Series(days)
    n_days = int(dser.nunique()) if n_cases else 0

    mean = float(x.mean()) if n_cases else None
    t_mean = None
    if n_cases and n_days >= 2:
        dev = pd.Series(x - mean).groupby(dser.values).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        if var > 0:
            t_mean = float(mean / np.sqrt(var))
    r = None
    t_r = None
    if n_cases >= 3 and np.std(fv) > 0 and np.std(x) > 0:
        r = float(np.corrcoef(fv, x)[0, 1])
        t_r = float(r * np.sqrt((n_cases - 2) / max(1e-15, 1 - r * r)))
    sup_pass = None if r is None else bool(r > 0)

    counts = {"distinct case days": n_days, "cases": n_cases, "active bars": int(n_active)}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days ({n_days}), so the test cannot show the idea."
    elif t_mean is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif t_mean <= -2 or (r is not None and r < 0 and t_r is not None and t_r <= -2):
        status = "rejected"
        decided = ("Reject: the mean excess next-day return has t <= -2." if t_mean <= -2 else
                   "Reject: the correlation with the forecast is below 0 with t <= -2.")
    elif mean > 0 and t_mean >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: mean excess next-day return above 0 with t >= 2 and correlation with the forecast above 0."
    else:
        status = "inconclusive"
        if abs(t_mean) < 2:
            decided = "Inconclusive: |t| of the mean excess next-day return is below 2."
        else:
            decided = "Inconclusive: a positive mean with t >= 2 whose correlation with the forecast is not above 0."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": None if t_mean is None else {"name": "t of the mean, pooled by day", "value": t_mean},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": r, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
