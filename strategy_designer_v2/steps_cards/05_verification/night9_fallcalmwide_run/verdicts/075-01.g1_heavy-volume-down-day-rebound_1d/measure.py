import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    MIN_CASES = 300
    MIN_DAYS = 150

    def _ts(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.astype(float)
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce")
            prev_close = close.shift(1)
            next_ret = close.shift(-1) / close - 1.0
            coin_rets.append(next_ret.dropna().values)
            down = pd.Series(np.where(prev_close.notna() & close.notna(),
                                      (close < prev_close).astype(float), np.nan))
            day = _ts(d["timestamp"]).dt.floor("D")
            coin_rows.append(pd.DataFrame({
                "coin": coin, "window": w, "day": day.values,
                "fc": fc.values, "down": down.values, "next_ret": next_ret.values,
            }))
        if not coin_rows:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mean_ret = float(np.mean(allr)) if len(allr) else np.nan
        cdf = pd.concat(coin_rows, ignore_index=True)
        cdf["excess"] = cdf["next_ret"] - mean_ret
        rows.append(cdf)

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(
        columns=["coin", "window", "day", "fc", "down", "next_ret", "excess"])

    reading = ("Down day = close below the prior close inside the same window (a window's first bar has no prior close "
               "in the record and is left out of the check and the measure); the slope's t uses a day-clustered standard "
               "error (deviations x residuals summed per day, G/(G-1) correction) so cases on the same day across coins "
               "count as one piece of evidence; top and bottom thirds are forecasts at or above the pooled 2/3 quantile "
               "and at or below the 1/3 quantile; the minimum is unmet if either fewer than 300 cases or fewer than 150 "
               "distinct days.")

    # ---- situation check ----
    active = data[(data["fc"].notna()) & (data["fc"] != 0) & data["down"].notna()]
    n_active = len(active)
    if n_active > 0:
        agree = float(((active["down"] == 1.0) & (active["fc"] > 0)).mean())
    else:
        agree = 0.0
    passed = bool(n_active > 0 and agree >= 0.90)

    main_name = "t of the slope of next-day excess return on the forecast, down days, day-pooled"
    thr = "t >= 2 confirms (with top-minus-bottom > 0); t <= -2 rejects; otherwise inconclusive"
    sup_name = "mean excess next-day return, top third minus bottom third of forecasts"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down days held long, as the plan's "
                           "situation (a down day, long, graded by the 20-day volume ratio) requires."),
            "reading": reading,
        }

    # ---- main measure ----
    s = data[(data["down"] == 1.0) & data["fc"].notna() & (data["fc"] != 0) & data["excess"].notna()].copy()
    n_cases = int(len(s))
    n_days = int(s["day"].nunique()) if n_cases else 0
    counts = {"down-day cases": n_cases, "distinct days": n_days}

    slope = None
    t = None
    if n_cases >= 3:
        x = s["fc"].values.astype(float)
        y = s["excess"].values.astype(float)
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = float(y.mean() - b * x.mean())
            e = y - a - b * x
            sc = pd.Series(xm * e).groupby(s["day"].values).sum().values
            G = len(sc)
            var = float(np.sum(sc ** 2)) / sxx ** 2
            if G > 1:
                var *= G / (G - 1.0)
            slope = b
            t = float(b / np.sqrt(var)) if var > 0 else None

    diff = None
    if n_cases >= 3:
        q1 = s["fc"].quantile(1.0 / 3.0)
        q2 = s["fc"].quantile(2.0 / 3.0)
        top = s.loc[s["fc"] >= q2, "excess"]
        bot = s.loc[s["fc"] <= q1, "excess"]
        if len(top) and len(bot):
            diff = float(top.mean() - bot.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum of 300 down-day cases on 150 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom difference is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom difference is at or below 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: heavier-volume down days are followed by weaker next days."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": {"name": main_name,
                         "value": t,
                         "statistic": None if t is None else {"name": "slope t, day-clustered", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
