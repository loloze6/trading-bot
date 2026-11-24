import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    STREAK = "debug_info.components.streak.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        for c in ["close", "forecast"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        if STREAK in d.columns:
            d[STREAK] = pd.to_numeric(d[STREAK], errors="coerce")
        else:
            d[STREAK] = np.nan
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            prepared[(coin, w)] = d
            close = d["close"].values
            n = len(d)
            ret30 = np.full(n, np.nan)
            if n > 30:
                ret30[30:] = close[30:] / close[:-30] - 1.0
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * n)
            # 30-day return from the prices; on the first 30 bars of a window (no history in the record)
            # the detector's own decision (`regime` == trending) stands in for it
            up30 = np.where(np.isnan(ret30), reg == "trending", ret30 > 0)
            streak = d[STREAK].values
            in_streak = np.where(np.isnan(streak), False, streak > 0)
            closed_up = np.zeros(n, dtype=bool)
            closed_up[1:] = close[1:] > close[:-1]
            # first bar: cannot see the previous close, rely on the streak raw value
            closed_up[0] = in_streak[0]
            situation = up30 & in_streak & closed_up
            f = d["forecast"].values
            active = np.nan_to_num(f) != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean unusual 5-day move after long bets (forecast rise >= 2 points, once per 5-bar cell)"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation = 30-day close return > 0 (detector's regime on a window's first 30 bars) and the bar "
               "closed up with a positive streak raw value, side long; a case is the first bet in each 5-bar grid "
               "cell of its window (bet = forecast rise >= 2 from its lowest positive level since the last bet, reset "
               "at flat), its forecast is the forecast on that bar, the drift is the coin's mean non-overlapping "
               "5-bar return over all its windows, and the t clusters cases by UTC calendar day with a G/(G-1) factor.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars inside the plan's "
                           "situation (30-day return > 0 and an up-close streak)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w in wins.keys():
            d = prepared.get((coin, w))
            if d is None:
                continue
            c = d["close"].values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (unusual, forecast, day)
    for (coin, w), d in prepared.items():
        f = np.nan_to_num(d["forecast"].values)
        c = d["close"].values
        n = len(d)
        low = 0.0
        bets = np.zeros(n, dtype=bool)
        for t in range(n):
            if f[t] <= 0:
                low = 0.0
                continue
            if f[t] - low >= BAND:
                bets[t] = True
                low = f[t]
            else:
                low = min(low, f[t])
        for start in range(0, n, H):
            idx = np.where(bets[start:start + H])[0]
            if len(idx) == 0:
                continue
            t = start + int(idx[0])
            if t + H >= n:
                continue
            if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                continue
            if not np.isfinite(drift.get(coin, np.nan)):
                continue
            r = c[t + H] / c[t] - 1.0
            cases.append((r - drift[coin], float(f[t]), d["timestamp"].iloc[t].strftime("%Y-%m-%d")))

    n_cases = len(cases)
    days = sorted(set(x[2] for x in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = None
    t_stat = None
    slope = None
    if n_cases > 0:
        u = np.array([x[0] for x in cases])
        fc = np.array([x[1] for x in cases])
        dd = np.array([x[2] for x in cases])
        mean_u = float(u.mean())
        e = u - mean_u
        sums = pd.Series(e).groupby(dd).sum().values
        G = len(sums)
        if G > 1:
            var = (sums ** 2).sum() / n_cases ** 2 * G / (G - 1)
            if var > 0:
                t_stat = float(mean_u / np.sqrt(var))
        if n_cases >= 2 and np.var(fc) > 0:
            slope = float(np.polyfit(fc, u, 1)[0])

    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (100 needed) on {n_days} distinct days (50 needed).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 and a positive slope on forecast size (confirm rule)."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 (reject rule)."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on forecast size is at or below 0 (or not computable): inconclusive rule."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases clustered by day", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of unusual move on forecast", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
