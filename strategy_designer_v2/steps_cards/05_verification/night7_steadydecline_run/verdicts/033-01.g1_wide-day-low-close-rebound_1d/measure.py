import numpy as np
import pandas as pd


def measure(bars):
    C1 = "debug_info.components.high_to_close_in_ranges.last_history_value"
    C2 = "debug_info.components.day_range_multiple.last_history_value"

    # ---------- collect cases ----------
    rows = []
    for coin, wins in bars.items():
        coin_parts = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            # next 1-bar return inside the window only
            d["ret1"] = close.shift(-1) / close - 1.0
            # situation value: 2 x (high-close)/base - (high-low)/base = (high+low-2close)/base
            sit_price = (high + low - 2.0 * close)
            if C1 in d.columns and C2 in d.columns:
                c1 = pd.to_numeric(d[C1], errors="coerce")
                c2 = pd.to_numeric(d[C2], errors="coerce")
                sit_raw = 2.0 * c1 - c2
                # where components are not recorded, recompute from prices (base > 0 keeps the sign)
                sit = sit_raw.where(sit_raw.notna(), sit_price)
            else:
                sit = sit_price
            d["situation"] = sit
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["day"] = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            d["coin"] = coin
            d["window"] = w
            coin_parts.append(d[["coin", "window", "day", "forecast", "situation", "ret1"]])
        if not coin_parts:
            continue
        cdf = pd.concat(coin_parts, ignore_index=True)
        # coin's mean daily return over all windows together
        coin_mean = cdf["ret1"].dropna().mean()
        cdf["excess"] = cdf["ret1"] - coin_mean
        rows.append(cdf)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"bars with |forecast| >= 2": 0, "distinct days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allb = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    if len(active) > 0:
        agree = (np.sign(active["situation"]) == np.sign(active["forecast"])) & (active["situation"] != 0) \
                & active["situation"].notna()
        agreement = float(agree.mean())
    else:
        agreement = 0.0
    passed_sit = agreement >= 0.90

    reading = ("Every bar with a forecast and a next-day return inside its window is a case (forecast-0 bars included); "
               "the day-clustered slope t uses residual-times-forecast deviations summed per UTC day with a G/(G-1) "
               "correction; fifths are the pooled 20th/80th forecast percentiles; the plan's minimum counts, if not "
               "reached, give 'not observable' as the workflow requires.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"active bars": int(len(active))},
            "decided_by": ("Fewer than 90 % of active bars have the forecast's sign equal to the sign of "
                           "(high + low - 2 x close) / mean range (long near the low, short near the high)."),
            "reading": reading,
        }

    # ---------- cases ----------
    cases = allb[allb["forecast"].notna() & allb["excess"].notna()].copy()
    n_big = int((cases["forecast"].abs() >= 2).sum())
    n_days = int(cases["day"].nunique())
    counts = {"bars with |forecast| >= 2": n_big, "distinct days": n_days, "cases": int(len(cases))}

    x = cases["forecast"].to_numpy(float)
    y = cases["excess"].to_numpy(float)
    slope = None
    t = None
    if len(cases) >= 3:
        xm = x.mean()
        ym = y.mean()
        xd = x - xm
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            slope = float(np.sum(xd * (y - ym)) / sxx)
            a = ym - slope * xm
            e = y - a - slope * x
            score = pd.Series(xd * e).groupby(cases["day"].to_numpy()).sum().to_numpy()
            G = len(score)
            if G > 1:
                var = (G / (G - 1.0)) * float(np.sum(score ** 2)) / sxx ** 2
                if var > 0:
                    t = float(slope / np.sqrt(var))

    # supporting check
    diff = None
    sup_pass = None
    if len(cases) >= 5:
        q20 = np.percentile(x, 20)
        q80 = np.percentile(x, 80)
        top = cases.loc[cases["forecast"] >= q80, "excess"]
        bot = cases.loc[cases["forecast"] <= q20, "excess"]
        if len(top) > 0 and len(bot) > 0:
            diff = float(top.mean() - bot.mean())
            sup_pass = bool(diff > 0)

    main = {
        "name": "pooled slope of next-day excess return on forecast",
        "value": slope,
        "statistic": {"name": "slope t, cases of one day summed", "value": t} if t is not None else None,
        "threshold": "confirm: t >= 2 with top-minus-bottom fifth > 0; reject: t <= -2",
    }
    support = {"name": "top fifth minus bottom fifth mean next-day excess return",
               "value": diff, "passed": sup_pass}

    if n_big < 500 or n_days < 1000:
        miss = []
        if n_big < 500:
            miss.append(f"{n_big} bars with |forecast| >= 2 (< 500)")
        if n_days < 1000:
            miss.append(f"{n_days} distinct days (< 1,000)")
        status = "not observable"
        decided = "Minimum count not reached: " + "; ".join(miss) + "."
    elif t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and the top-minus-bottom-fifth difference is above 0 (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "Slope t <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the top-minus-bottom-fifth difference is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Slope t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
