import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_rise.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime left when neither 'chop' veto fires: falling and agitated

    # ---------- pass 1: the coin's mean daily return over all its windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            r = (c.shift(-1) / c - 1.0).iloc[:-1]
            rets.append(r.dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mu[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- pass 2: situation check and cases ----------
    n_active = 0
    n_agree = 0
    cases = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # up day: raw scaled rise > 0; where the raw value is not recorded, the sign of the day's return
            day_ret = c / c.shift(1) - 1.0
            up = np.where(raw.notna(), raw > 0, day_ret > 0)
            in_profile = (regime == PROFILE_REGIME).values
            situation = up & in_profile

            active = (f != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0).values).sum())

            nxt = (c.shift(-1) / c - 1.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in np.where(active)[0]:
                if i >= len(d) - 1 or not np.isfinite(nxt[i]) or not np.isfinite(mu):
                    continue
                unusual = -(nxt[i] - mu)
                cases.append((ts.iloc[i].floor("D"), unusual, abs(float(f.iloc[i]))))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean short-direction unusual move over the next 1 bar"
    main_thr = "confirm: > 0 with t >= 2 (and slope > 0); reject: < 0 with t <= -2"
    sup_name = "OLS slope of short-direction unusual move on abs(forecast)"
    reading = ("Profile bars are read from the recorded regime ('unknown', the regime left when neither 'chop' veto fires) "
               "and up days from the raw scaled rise > 0; cases are every active bar with a next-bar return in its window, "
               "the coin's mean is over all its 1-bar returns in all windows, and the day-clustered t uses "
               "se = sqrt(G/(G-1) * sum over days of (summed deviations)^2) / n.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are up days inside the falling agitated "
                           "profile with a short forecast, as the Fidelity's situation and side require."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": reading,
        }

    if cases:
        cdf = pd.DataFrame(cases, columns=["day", "u", "size"])
    else:
        cdf = pd.DataFrame(columns=["day", "u", "size"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["u"] - mean_u
        S = dev.groupby(cdf["day"]).sum().values
        G = len(S)
        var = (G / (G - 1)) * float(np.sum(S ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t = float(mean_u / se) if se > 0 else None

    slope = None
    if n_cases >= 2 and float(np.var(cdf["size"].astype(float).values)) > 0:
        x = cdf["size"].astype(float).values
        y = cdf["u"].astype(float).values
        slope = float(np.polyfit(x, y, 1)[0])
    slope_pass = (slope > 0) if slope is not None else None

    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day together", "value": t} if t is not None else None),
            "threshold": main_thr}
    sup = {"name": sup_name, "value": slope, "passed": slope_pass}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases on 50 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t is None or mean_u is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The main measure is above 0 with t >= 2 and the slope on abs(forecast) is above 0."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2: up days are followed by higher than usual returns."
    elif mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "The main measure confirms (above 0, t >= 2) but the slope is at or below 0."
    else:
        status = "inconclusive"
        decided = "The t of the main measure lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
