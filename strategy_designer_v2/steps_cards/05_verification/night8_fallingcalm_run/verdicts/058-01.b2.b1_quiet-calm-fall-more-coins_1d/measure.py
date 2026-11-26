import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D").astype(str).values


def _cluster_slope_t(x, y, groups):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if n < 3:
        return None, None
    xm = x.mean()
    dx = x - xm
    sxx = float(np.sum(dx * dx))
    if sxx <= 0:
        return None, None
    slope = float(np.sum(dx * (y - y.mean())) / sxx)
    intercept = y.mean() - slope * xm
    e = y - intercept - slope * x
    df = pd.DataFrame({"g": groups, "s": dx * e})
    sc = df.groupby("g")["s"].sum().values
    G = len(sc)
    if G < 2:
        return slope, None
    meat = float(np.sum(sc ** 2))
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
    var = corr * meat / (sxx ** 2)
    if var <= 0:
        return slope, None
    return slope, float(slope / np.sqrt(var))


def measure(bars):
    H = 5
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            reg = d["regime"].astype(str)
            ret30 = close / close.shift(30) - 1.0
            fall30 = pd.Series(np.where(ret30.notna(), ret30 < 0, reg == "trending"), index=d.index)
            in_sit = fall30.astype(bool) & (reg == "trending")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (fc < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed_sit = True if agreement is None else bool(agreement >= 0.9)

    main_name = "OLS slope of drift-adjusted 5-day return on forecast, in-regime grid bars"
    threshold = "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2; else inconclusive"
    reading = ("The situation is the 30-day close-to-close return below 0 (from prices, or the recorded 'trending' regime "
               "on a window's first 30 bars) with the bar's regime 'trending' standing for the falling-calm profile, side short; "
               "in-regime means regime == 'trending'; the coin's mean 5-day return is taken on the 5-bar grid of all its windows; "
               "the slope's t pools same-day cases as day-clustered standard errors; the supporting check is the sign of the mean; "
               "distinct days are the days of the in-regime grid bars.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of the plan's situation "
                           "(30-day return below 0 inside the falling calm profile)."),
            "reading": reading,
        }

    # ---------- criterion ----------
    rows = []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            days = _to_day(d["timestamp"])
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.setdefault(coin, []).append(r)
                rows.append((coin, days[i], fc[i], reg[i], r))

    drift = {c: float(np.mean(v)) for c, v in coin_grid_rets.items() if len(v)}
    g = pd.DataFrame(rows, columns=["coin", "day", "forecast", "regime", "ret"])
    if len(g):
        g = g[(g["regime"] == "trending") & g["forecast"].notna()].copy()
        g["adj"] = g["ret"] - g["coin"].map(drift)
        g = g[g["adj"].notna()]
    else:
        g = pd.DataFrame(columns=["coin", "day", "forecast", "regime", "ret", "adj"])

    n_grid = int(len(g))
    n_neg = int((g["forecast"] < 0).sum()) if n_grid else 0
    n_zero = int((g["forecast"] == 0).sum()) if n_grid else 0
    n_days = int(g["day"].nunique()) if n_grid else 0
    counts = {"in-regime grid bars": n_grid, "bars with forecast below 0": n_neg,
              "bars with forecast 0": n_zero, "distinct days": n_days}

    slope, t = (None, None)
    if n_grid >= 3:
        slope, t = _cluster_slope_t(g["forecast"].values, g["adj"].values, g["day"].values)
    neg = g[g["forecast"] < 0]["adj"] if n_grid else pd.Series(dtype=float)
    sup_val = float(neg.mean()) if len(neg) else None
    sup_pass = (bool(sup_val < 0) if sup_val is not None else None)

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "slope t, day-clustered", "value": t} if t is not None else None),
            "threshold": threshold}
    support = {"name": "mean drift-adjusted 5-day return on grid bars with forecast < 0",
               "value": sup_val, "passed": sup_pass}

    if n_grid < 100 or n_neg < 30 or n_zero < 30 or n_days < 30:
        miss = []
        if n_grid < 100: miss.append("100 in-regime grid bars")
        if n_neg < 30: miss.append("30 bars with forecast below 0")
        if n_zero < 30: miss.append("30 bars with forecast 0")
        if n_days < 30: miss.append("30 distinct days")
        status = "not observable"
        decided = "Minimum count not reached: " + ", ".join(miss) + "."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean drift-adjusted return on forecast-below-0 bars is below 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails (mean return on forecast-below-0 bars not below 0)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: heavy-volume falls continue more than quiet ones."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed_sit},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
