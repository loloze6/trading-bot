import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.low_close_width.last_history_value"
    H = 3
    BAND = 2.0

    def prep(df):
        d = df.copy().reset_index(drop=True)
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        for c in ["open", "high", "low", "close", "forecast"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        if RAW in d.columns:
            d[RAW] = pd.to_numeric(d[RAW], errors="coerce")
        else:
            d[RAW] = np.nan
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = prep(df)
            f = d["forecast"].fillna(0.0)
            active = f != 0
            if not active.any():
                continue
            mid = (d["high"] + d["low"]) / 2.0
            raw = d[RAW]
            # below the middle: from the raw component where recorded, else from prices
            below = np.where(raw.notna(), raw < 0, d["close"] < mid)
            below = pd.Series(below, index=d.index).astype(bool)
            # choppy agitated profile = the regime the profile's code leaves trading ("unknown")
            in_profile = d["regime"].astype(str) == "unknown"
            ok = active & in_profile & below & (f > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    main_name = "mean excess 3-bar return of the long bets over the coin's normal 3-bar drift"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    reading = ("Profile read as regime == 'unknown' (the only regime with a strategy, the vetoes send everything else to chop); "
               "one case per 3-bar grid cell = the first bet bar in the cell, return taken from that bar's close; "
               "normal drift = mean non-overlapping 3-bar grid return of the coin over all its windows; "
               "day-clustered t uses summed deviations per day with a D/(D-1) correction; "
               "median split: top = forecast above the median, bottom = at or below it; "
               "the 30-distinct-days minimum gives 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "distinct days with cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the choppy agitated "
                           "profile with the close below the day's middle, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = prep(df)
            c = d["close"].values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, excess, forecast)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            d = prep(df)
            f = d["forecast"].fillna(0.0).values
            c = d["close"].values
            n = len(d)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    ref = 0.0
                    continue
                if fi - ref >= BAND:
                    bet[i] = True
                    ref = fi
                else:
                    ref = min(ref, fi)
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                cases.append((d["timestamp"].iloc[t].strftime("%Y-%m-%d"), r - drift[coin], float(f[t])))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"distinct days with cases": n_days, "cases": n_cases}

    mean_ex = None
    tval = None
    if n_cases > 0:
        x = np.array([v[1] for v in cases])
        mean_ex = float(x.mean())
        if n_days >= 2:
            dev = pd.Series(x - mean_ex, index=[v[0] for v in cases]).groupby(level=0).sum().values
            var = (dev ** 2).sum() * n_days / (n_days - 1) / n_cases ** 2
            if var > 0:
                tval = float(mean_ex / np.sqrt(var))

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        fc = np.array([v[2] for v in cases])
        x = np.array([v[1] for v in cases])
        med = np.median(fc)
        top = x[fc > med]
        bot = x[fc <= med]
        if len(top) > 0 and len(bot) > 0:
            sup_val = float(top.mean() - bot.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean_ex,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": tval}
                          if tval is not None else None),
            "threshold": thr}
    sup = {"name": "mean excess return, top half minus bottom half at the median forecast",
           "value": sup_val, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, below the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess return above 0 with t >= 2 and the top-half-minus-bottom-half difference above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t with a failed supporting check is inconclusive."
    elif mean_ex < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
