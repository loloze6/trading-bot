import numpy as np
import pandas as pd


def _to_time(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    rows = []
    for coin in sorted(bars.keys()):
        coin_rets = []
        coin_rows = []
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rng = high - low
            cl = (close - low) / rng.where(rng > 0)
            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)
            t = _to_time(df["timestamp"])
            day = t.dt.floor("D").astype(str)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            coin_rows.append(pd.DataFrame({
                "coin": coin, "window": window, "day": day.values,
                "forecast": fc.values, "cl": cl.values, "regime": regime.values,
                "ret": nxt.values,
            }))
        if not coin_rows:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if len(allr) else np.nan
        cdf = pd.concat(coin_rows, ignore_index=True)
        cdf["mu"] = mu
        rows.append(cdf)

    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"distinct days with a case": 0},
                "decided_by": "No bars in the record.", "reading": "none"}
    d = pd.concat(rows, ignore_index=True)

    # ---- situation check
    active = d[d["forecast"] != 0]
    n_active = len(active)
    if n_active == 0:
        agreement = None
        passed = False
    else:
        sit = (active["cl"] > 0.5) & (active["regime"] == "mean_reversion")
        ok = sit & (active["forecast"] < 0)
        agreement = float(ok.mean())
        passed = agreement >= 0.9
    reading = ("Situation = close location (close-low)/(high-low) > 0.5 recomputed from prices, with the "
               "falling-agitated profile read from the recorded regime (its 365-bar volatility lookback cannot be "
               "rebuilt inside a window), side short; t of the size-weighted mean groups size-weighted deviations "
               "per UTC day; the wider half is |forecast| strictly above the median, the narrower half the rest, "
               "compared on next-day return minus the coin's all-window mean; fewer than 30 days gives 'not observable'.")
    if n_active > 0 and not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars with a close in the "
                              "upper half of the range inside the falling-agitated profile.",
                "reading": reading}

    # ---- main measure
    c = d[(d["forecast"] < 0) & d["ret"].notna() & d["mu"].notna()].copy()
    c["size"] = -c["forecast"] / 10.0
    c["exc"] = c["ret"] - c["mu"]
    c["gain"] = -c["exc"]
    n_cases = int(len(c))
    n_days = int(c["day"].nunique()) if n_cases else 0
    counts = {"distinct days with a case": n_days, "cases": n_cases}

    value = None
    tval = None
    if n_cases > 0 and c["size"].sum() > 0:
        S = float(c["size"].sum())
        m = float((c["size"] * c["gain"]).sum() / S)
        value = m
        if n_days >= 2:
            dev = (c["size"] * (c["gain"] - m)).groupby(c["day"]).sum()
            var = (n_days / (n_days - 1.0)) * float((dev ** 2).sum()) / (S ** 2)
            if var > 0:
                tval = float(m / np.sqrt(var))

    # ---- supporting check
    sup_val = None
    if n_cases > 0:
        a = c["forecast"].abs()
        med = float(a.median())
        wide = c[a > med]
        narrow = c[a <= med]
        if len(wide) and len(narrow):
            sup_val = float(wide["exc"].mean() - narrow["exc"].mean())
    sup_pass = None if sup_val is None else bool(sup_val < 0)

    main = {"name": "size-weighted mean next-day short excess gain",
            "value": value,
            "statistic": None if tval is None else {"name": "t of the weighted mean, cases grouped by day", "value": tval},
            "threshold": "t >= 2 confirms (with supporting check < 0); t <= -2 rejects"}
    support = {"name": "wider-range half minus narrower half, mean next-day excess return",
               "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": bool(passed)}

    if n_days < 30:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": support, "counts": counts,
                "decided_by": "Fewer than the plan's minimum of 30 distinct days with a case.",
                "reading": reading}

    if tval is not None and tval >= 2 and sup_pass is True:
        status, why = "confirmed", "The main measure's t is 2 or more and the supporting check is below 0."
    elif tval is not None and tval <= -2:
        status, why = "rejected", "The main measure's t is -2 or less."
    elif tval is not None and tval >= 2:
        status, why = "inconclusive", "A confirming t whose supporting check is not below 0 is inconclusive."
    else:
        status, why = "inconclusive", "The main measure's t is between -2 and 2 (or not computable)."
    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": support, "counts": counts,
            "decided_by": why, "reading": reading}
