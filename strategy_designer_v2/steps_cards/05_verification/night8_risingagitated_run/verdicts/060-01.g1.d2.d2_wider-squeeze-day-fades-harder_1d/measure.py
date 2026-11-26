import numpy as np
import pandas as pd


def _to_time(s):
    if pd.api.types.is_numeric_dtype(s):
        v = pd.to_numeric(s, errors="coerce")
        mx = np.nanmax(v.values) if len(v) else 0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True, errors="coerce")


def measure(bars):
    rows = []
    drift = {}
    # --- gather per coin, per window ---
    for coin, wins in bars.items():
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            all_rets.append(nxt.dropna().values)
            rng = high - low
            cl = np.where(rng > 0, (close - low) / rng, np.nan)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            t = _to_time(d["timestamp"])
            coin_rows.append(pd.DataFrame({
                "coin": coin, "window": w, "time": t,
                "day": t.dt.floor("D"),
                "forecast": fc.values, "ret1": nxt.values,
                "cl": cl, "regime": regime.values,
            }))
        r = np.concatenate(all_rets) if all_rets else np.array([])
        drift[coin] = float(np.mean(r)) if len(r) else np.nan
        rows.extend(coin_rows)

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(
        columns=["coin", "window", "time", "day", "forecast", "ret1", "cl", "regime"])

    # --- situation check ---
    active = data[data["forecast"] != 0]
    n_active = len(active)
    if n_active > 0:
        in_sit = (active["regime"] == "mean_reversion") & (active["cl"] > 0.5) & (active["forecast"] < 0)
        agreement = float(in_sit.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean next-day unusual move of short cases (return minus coin drift, short-signed)"
    threshold = "confirm: mean > 0 with t >= 2 and check difference > 0; reject: mean < 0 with t <= -2"
    reading = ("Profile taken from the recorded regime (mean_reversion only when neither chop veto fired, as the "
               "detector's 60-day trend and 365-day volatility percentile cannot be rebuilt from the recorded windows) "
               "and close location recomputed from prices; day-clustered t uses per-day summed deviations with a "
               "G/(G-1) correction; the upper half is |forecast| strictly above the median, the lower half the rest; "
               "a minimum count not reached gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars in the falling agitated profile "
                           "(regime mean_reversion) with close location above 0.5." if n_active > 0 else
                           "No active bars: the config never takes the plan's short in its situation."),
            "reading": reading,
        }

    # --- cases ---
    cases = data[(data["forecast"] < 0)].dropna(subset=["ret1"]).copy()
    cases["drift"] = cases["coin"].map(drift)
    cases = cases.dropna(subset=["drift", "day"])
    cases["u"] = -(cases["ret1"] - cases["drift"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    m = float(cases["u"].mean()) if n else None
    tval = None
    if n >= 2:
        dev = cases["u"] - m
        per_day = dev.groupby(cases["day"]).sum()
        G = len(per_day)
        if G >= 2:
            var = float((per_day ** 2).sum()) / (n ** 2) * G / (G - 1)
            se = np.sqrt(var)
            tval = float(m / se) if se > 0 else None

    diff = None
    if n >= 2:
        a = cases["forecast"].abs()
        med = float(a.median())
        up = cases.loc[a > med, "u"]
        lo = cases.loc[a <= med, "u"]
        if len(up) and len(lo):
            diff = float(up.mean() - lo.mean())
    check_pass = None if diff is None else bool(diff > 0)

    counts = {"cases": n, "distinct days": n_days}

    if n < 100 or n_days < 60:
        status = "not observable"
        decided = ("Minimum not reached: at least 100 cases on at least 60 distinct days are needed "
                   f"(got {n} cases on {n_days} days).")
    elif tval is None or m is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and tval >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the wider-half minus narrower-half difference is above 0."
    elif m < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: high closes are followed by rises beyond the coin's drift."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check's difference is 0 or below (or not computable)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": None if tval is None else {"name": "t of the mean, cases of one day together", "value": tval},
                         "threshold": threshold},
        "supporting_check": {"name": "upper minus lower half (|forecast| median split) mean unusual move",
                             "value": diff, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
