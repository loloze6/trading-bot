import numpy as np
import pandas as pd


def _to_dt(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
        if mx > 1e17:
            unit = "ns"
        elif mx > 1e14:
            unit = "us"
        elif mx > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    DEPTH = "debug_info.components.depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(d)
            for t in range(n):
                if f[t] == 0:
                    continue
                if t < 3 or np.isnan(c[t]) or np.isnan(c[t - 1]) or np.isnan(c[t - 2]) or np.isnan(c[t - 3]):
                    n_unverifiable += 1
                    continue
                n_active += 1
                up = c[t] > c[t - 1]
                run2 = (c[t - 1] < c[t - 2]) and (c[t - 2] < c[t - 3])
                if up and run2 and f[t] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    base_reading = ("Situation checked from prices as an up close after at least 2 down closes inside the window, "
                    "with short side (forecast < 0); the falling-calm profile is not recomputed (its 365-day volatility "
                    "percentile needs history before each window) and active bars in a window's first 3 rows are left "
                    "out of the check; case-days are distinct UTC dates, the t is clustered by day (deviations summed "
                    "per day), the slope is OLS over all cases, and fewer than 30 case-days gives 'not observable' as "
                    "the workflow's minimum-count rule requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars unverifiable": int(n_unverifiable)},
            "decided_by": ("Fewer than 90 % of the active bars are up closes after 2 or more down closes with a short "
                           "forecast, so the record does not do what the plan's Fidelity says."
                           if n_active > 0 else "No verifiable active bar in the record."),
            "reading": base_reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        rets_all = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            r = np.full(len(d), np.nan)
            r[:-1] = c[1:] / c[:-1] - 1.0
            rets_all.append(r[~np.isnan(r)])
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            x = (pd.to_numeric(d[DEPTH], errors="coerce").values
                 if DEPTH in d.columns else np.full(len(d), np.nan))
            days = _to_dt(d["timestamp"]).dt.floor("D").values
            for t in range(len(d)):
                if np.isnan(f[t]) or not (f[t] < 0) or np.isnan(r[t]):
                    continue
                coin_cases.append((days[t], r[t], x[t]))
        if not rets_all:
            continue
        allr = np.concatenate(rets_all)
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for day, rt, xt in coin_cases:
            rows.append({"coin": coin, "day": day, "ex": -(rt - mu), "x": xt})

    cases = pd.DataFrame(rows, columns=["coin", "day", "ex", "x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = None
    tval = None
    if n_cases > 0:
        mean = float(cases["ex"].mean())
        if n_days >= 2:
            g = cases.groupby("day")["ex"].agg(["sum", "count"])
            resid = g["sum"].values - g["count"].values * mean
            var = np.sum(resid ** 2) * n_days / (n_days - 1)
            se = np.sqrt(var) / n_cases
            tval = float(mean / se) if se > 0 else None

    slope = None
    sc = cases.dropna(subset=["x", "ex"]) if n_cases else cases
    if len(sc) >= 2 and np.unique(sc["x"].values).size >= 2:
        slope = float(np.polyfit(sc["x"].values.astype(float), sc["ex"].values.astype(float), 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days, below the plan's minimum of 30 case-days."
    elif mean is not None and tval is not None and mean > 0 and tval >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The main mean is positive with t >= 2 over at least 30 case-days and the supporting slope is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t whose supporting slope is not positive is inconclusive."
    elif mean is not None and tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2 over at least 30 case-days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (neither the confirm nor the reject rule is met)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean short-signed next-day return minus the coin's mean daily return, on forecast < 0 bars",
            "value": mean,
            "statistic": None if tval is None else {"name": "t of the mean, cases of one day pooled", "value": tval},
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 case-days; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "OLS slope of short-signed excess next-day return on depth last_history_value",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"case-days": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": base_reading,
    }
