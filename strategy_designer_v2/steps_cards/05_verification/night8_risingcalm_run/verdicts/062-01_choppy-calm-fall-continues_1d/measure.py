import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    LHV = "debug_info.components.scaled_fall.last_history_value"
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            if not active.any():
                continue
            close = pd.to_numeric(d["close"], errors="coerce")
            # raw scaled 5-day return: recorded value, else recomputed from prices inside the window
            ret1 = close.pct_change()
            recomputed = (close / close.shift(H) - 1.0) / ret1.rolling(30, min_periods=30).std(ddof=1)
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            in_profile = regime == "unknown"  # choppy calm: no veto to "chop" fired
            situation = in_profile & (raw < 0)
            ok = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_ok += int(ok.sum())

    agreement = (n_ok / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean short-direction 5-day excess return over the coin's normal drift, forecast < 0 grid bars"
    threshold = "confirm t >= 2 with larger-half minus smaller-half > 0; reject t <= -2; at least 30 distinct days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short bars inside the choppy calm "
                           "profile (regime 'unknown') after a negative scaled 5-day return"
                           if n_active > 0 else "the record holds no bar with a non-zero forecast"),
            "reading": "the choppy calm profile is read as the regime detector's 'unknown' regime (no chop veto), "
                       "the situation as a negative raw scaled 5-day return, on the short side.",
        }

    # ---------- 2. criterion ----------
    drift_rets = {}
    cases = []  # (coin, day, fwd_ret, forecast)
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                rs.append(r)
                f = fc[p]
                if np.isfinite(f) and f < 0:
                    cases.append((coin, ts.iloc[p].floor("D"), r, float(f)))
        drift_rets[coin] = float(np.mean(rs)) if rs else np.nan

    rows = []
    for coin, day, r, f in cases:
        dr = drift_rets.get(coin, np.nan)
        if not np.isfinite(dr):
            continue
        rows.append((day, -(r - dr), f))
    cdf = pd.DataFrame(rows, columns=["day", "x", "f"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    def clustered(x, days):
        n = len(x)
        if n < 2:
            return (float(np.mean(x)) if n else None), None
        m = float(np.mean(x))
        dev = pd.Series(x - m).groupby(days.values).sum()
        G = len(dev)
        if G < 2:
            return m, None
        var = float((dev ** 2).sum()) / (n ** 2) * G / (G - 1)
        if var <= 0:
            return m, None
        return m, m / np.sqrt(var)

    mean_x, t = (None, None)
    if n_cases:
        mean_x, t = clustered(cdf["x"].values, cdf["day"])

    diff = None
    sup_pass = None
    if n_cases >= 2:
        a = cdf["f"].abs()
        med = a.median()
        big = cdf.loc[a > med, "x"]
        small = cdf.loc[a <= med, "x"]
        if len(big) and len(small):
            diff = float(big.mean() - small.mean())
            sup_pass = bool(diff > 0)

    counts = {"cases": n_cases, "distinct days holding cases": n_days}
    reading = ("choppy calm profile read as regime 'unknown'; the normal drift is each coin's mean 5-day return on the "
               "non-overlapping grid over all its windows; the day-clustered t uses a G/(G-1) correction; the larger half "
               "is |forecast| strictly above the median, the smaller half the rest; the plan's 'fewer than 30 distinct "
               "days' is treated as a minimum count, giving 'not observable'.")

    if n_days < MIN_DAYS or t is None:
        status = "not observable"
        decided = f"fewer than 30 distinct days hold cases ({n_days})" if n_days < MIN_DAYS else \
            "the t of the mean could not be computed"
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "t >= 2 and the larger-half minus smaller-half difference is above 0"
    elif t <= -2:
        status = "rejected"
        decided = "t <= -2: scaled falls are followed by rebounds relative to the coin's drift"
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the larger-half minus smaller-half difference is at or below 0"
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": (float(mean_x) if mean_x is not None else None),
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": float(t)} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "larger-|forecast| half minus smaller half, mean short excess return",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
