import numpy as np
import pandas as pd


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
        unit = "ns" if v > 1e17 else ("us" if v > 1e14 else ("ms" if v > 1e11 else "s"))
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    raw_col = "debug_info.components.heavy_fall.last_history_value"
    rows = []
    coin_rets = {}
    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            df["_ts"] = _to_dt(df["timestamp"])
            df = df.sort_values("_ts").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0
            prev_ret = close / close.shift(1) - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            coin_rets.setdefault(coin, []).append(fwd.dropna().values)
            rows.append(pd.DataFrame({
                "coin": coin,
                "day": df["_ts"].dt.floor("D"),
                "fc": fc.values,
                "raw": raw.values,
                "prev_ret": prev_ret.values,
                "fwd": fwd.values,
            }))
    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"bars with forecast > 0": 0, "distinct days": 0},
                "decided_by": "No bars in the record.", "reading": "none"}
    allr = pd.concat(rows, ignore_index=True)
    coin_mean = {c: float(np.mean(np.concatenate(v))) if sum(len(x) for x in v) else np.nan
                 for c, v in coin_rets.items()}

    # ---- situation check: down day (raw < 0), long side (forecast > 0)
    active = allr[allr["fc"].notna() & (allr["fc"] != 0)]
    down = np.where(active["raw"].notna(), active["raw"] < 0, active["prev_ret"] < 0)
    ok = down & (active["fc"].values > 0)
    n_active = len(active)
    agreement = float(ok.mean()) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("The situation is a bar whose raw component value is below 0 (the day's return sign, the prior close "
               "being used only where the raw value is missing) with a long forecast; the main measure's t is the "
               "day-clustered t of the weighted mean (per-day sums of weight x deviation from the weighted mean, "
               "variance scaled by D/(D-1)); thirds are the n//3 lowest and highest forecasts after a stable sort; "
               "the minimum counts use bars with forecast > 0 and a next-day return, and short counts give "
               "'not observable'.")
    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down days held long, "
                               "as the Fidelity requires (agreement %.3f)." % agreement),
                "reading": reading}

    # ---- criterion
    cases = allr[(allr["fc"] > 0) & allr["fwd"].notna()].copy()
    cases["ex"] = cases["fwd"] - cases["coin"].map(coin_mean)
    cases = cases[cases["ex"].notna()]
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0
    counts = {"bars with forecast > 0": n, "distinct days": n_days}
    main_name = "forecast-weighted mean next-day excess return (forecast > 0)"
    thr = "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"

    M = None
    t = None
    diff = None
    if n > 0:
        f = cases["fc"].values.astype(float)
        ex = cases["ex"].values.astype(float)
        W = f.sum()
        M = float((f * ex).sum() / W)
        contrib = (f / W) * (ex - M)
        per_day = pd.Series(contrib).groupby(cases["day"].values).sum().values
        D = len(per_day)
        if D > 1:
            var = (per_day ** 2).sum() * D / (D - 1)
            se = np.sqrt(var)
            t = float(M / se) if se > 0 else None
        order = np.argsort(f, kind="mergesort")
        k = n // 3
        if k > 0:
            bot = ex[order[:k]].mean()
            top = ex[order[-k:]].mean()
            diff = float(top - bot)

    supp_pass = None if diff is None else bool(diff > 0)
    main = {"name": main_name, "value": M,
            "statistic": None if t is None else {"name": "day-clustered t of the weighted mean", "value": t},
            "threshold": thr}
    supp = {"name": "top third minus bottom third mean next-day excess return",
            "value": diff, "passed": supp_pass}

    if n < 300 or n_days < 150:
        status = "not observable"
        decided = ("The plan's minimum of 300 bars with forecast > 0 over at least 150 distinct days is not reached "
                   "(%d bars, %d days)." % (n, n_days))
    elif t is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither the confirm nor the reject rule is met."
    elif M > 0 and t >= 2 and supp_pass:
        status = "confirmed"
        decided = "The main measure is above 0 with t >= 2 and the top third minus bottom third is above 0."
    elif M < 0 and t <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2."
    elif M > 0 and t >= 2:
        status = "inconclusive"
        decided = "The main measure is above 0 with t >= 2 but the top-minus-bottom difference is 0 or below."
    else:
        status = "inconclusive"
        decided = "The t of the main measure lies between -2 and 2."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": supp,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
