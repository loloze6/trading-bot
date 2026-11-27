import numpy as np
import pandas as pd


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        unit = "ms" if np.nanmedian(v) > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _clustered_t(x, days):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return None
    m = x.mean()
    dev = pd.Series(x - m).groupby(np.asarray(days)).sum().values
    D = len(dev)
    if D < 2:
        return None
    var = (D / (D - 1.0)) * np.sum(dev ** 2)
    se = np.sqrt(var) / n
    if se <= 0 or not np.isfinite(se):
        return None
    return float(m / se)


def measure(bars):
    # ---------- 1. situation check ----------
    sit_ok = 0
    sit_n = 0
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["ts"] = _to_dt(d["timestamp"])
            d = d.sort_values("ts").reset_index(drop=True)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            rng = high - low
            # RangeCompressionRatio: current range / mean of last 30 ranges (current included)
            mean30 = rng.rolling(30, min_periods=30).mean()
            width = rng / mean30
            cloc = (close - low) / rng.replace(0, np.nan)
            regime = d["regime"].astype(str)
            in_sit = (regime == "unknown") & (width >= 1.0) & (cloc < 0.5)
            computable = width.notna() & cloc.notna()
            active = fc.notna() & (fc != 0)
            chk = active & computable
            sit_n += int(chk.sum())
            sit_ok += int((chk & in_sit & (fc > 0)).sum())

            r1 = close.shift(-1) / close - 1.0
            all_r.append(r1.dropna().values)
            sel = fc.notna() & (fc > 0) & r1.notna()
            for i in np.where(sel.values)[0]:
                rows.append((coin, d["ts"].iloc[i].floor("D"), float(fc.iloc[i]), float(r1.iloc[i])))
        coin_rets[coin] = np.concatenate(all_r) if all_r else np.array([])

    agreement = (sit_ok / sit_n) if sit_n > 0 else None
    passed = agreement is not None and agreement >= 0.9
    reading = ("Situation recomputed from prices (range over the 30-bar mean range incl. the current bar >= 1, "
               "close location < 0.5) with the choppy-agitated profile read from regime == 'unknown', on active bars "
               "where the 30-bar range mean exists; cases are bars with forecast > 0 and a next-day return in the same "
               "window; the day-clustered t uses a D/(D-1) correction; the median split puts forecast > median in the "
               "upper half and <= median in the lower half; below the plan's minimum counts the status is 'not observable'.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"cases": len(rows), "distinct days": len(set(r[1] for r in rows))},
            "decided_by": ("Fewer than 90% of active bars are long bars of the plan's situation (choppy agitated profile, "
                           "range >= its 30-day mean, close in the lower half)." if agreement is not None
                           else "No active bar where the plan's situation could be computed."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    thr = "confirm: mean > 0 with t >= 2 and upper-minus-lower > 0; reject: mean < 0 with t <= -2"
    cdf = pd.DataFrame(rows, columns=["coin", "day", "fc", "r"])
    if len(cdf):
        cdf["mu"] = cdf["coin"].map(lambda c: float(np.mean(coin_rets[c])) if len(coin_rets[c]) else np.nan)
        cdf["x"] = cdf["r"] - cdf["mu"]
        cdf = cdf.dropna(subset=["x"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_x = float(cdf["x"].mean()) if n_cases else None
    t = _clustered_t(cdf["x"].values, cdf["day"].values) if n_cases else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = cdf["fc"].median()
        up = cdf.loc[cdf["fc"] > med, "x"]
        lo = cdf.loc[cdf["fc"] <= med, "x"]
        if len(up) and len(lo):
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": "mean excess next-day return of forecast>0 cases",
            "value": mean_x,
            "statistic": {"name": "day-clustered t", "value": t} if t is not None else None,
            "threshold": thr}
    sup = {"name": "upper minus lower half (median forecast) mean excess return", "value": sup_val, "passed": sup_pass}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} cases (need 100) on {n_days} distinct days (need 50)."
    elif t is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_x > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess return positive with t >= 2 and upper half minus lower half > 0."
    elif mean_x < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess return negative with t <= -2."
    elif mean_x > 0 and t >= 2:
        status = "inconclusive"
        decided = "Confirming t >= 2 but the supporting check failed (upper half minus lower half not > 0)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
