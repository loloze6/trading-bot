import numpy as np
import pandas as pd


def measure(bars):
    H = 45
    RAW = "debug_info.components.fall90.last_history_value"

    # ---------- 1. Situation check: 90-day return below zero (raw < 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of excess 45-day return on forecast, non-overlapping grid cases, all coins"
    threshold = "confirm if slope t >= 2 and supporting check passes; reject if slope t <= -2; else inconclusive"
    reading = ("Situation = raw fall90 value below zero with forecast > 0 (bars with the raw value missing count as not "
               "agreeing); grid = positions 0, 45, 90, ... of each window with t+45 inside the window; the coin's mean "
               "45-day return is the mean over all its grid returns in all its windows; the slope is a one-variable "
               "OLS with intercept over all grid cases (forecast 0 included) and its t uses a day-clustered "
               "standard error (cross-products summed per UTC day, G/(G-1) correction); the plan's 'fewer is "
               "inconclusive' minimum is reported as 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where the 90-day "
                           "return (raw fall90) is below zero with a long (positive) forecast, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Grid cases ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rows.append({"coin": coin, "ret": r, "f": fc[p],
                                  "day": ts.iloc[p].strftime("%Y-%m-%d")})
        if coin_rows:
            cm = float(np.mean([x["ret"] for x in coin_rows]))
            for x in coin_rows:
                x["ex"] = x["ret"] - cm
            rows.extend(coin_rows)

    g = pd.DataFrame(rows, columns=["coin", "ret", "f", "day", "ex"])
    g = g[np.isfinite(g["f"].astype(float)) & np.isfinite(g["ex"].astype(float))].copy()
    g["f"] = g["f"].astype(float)

    pos = g[g["f"] > 0]
    n_pos = int(len(pos))
    days_pos = int(pos["day"].nunique())
    counts = {
        "grid cases": int(len(g)),
        "grid cases with forecast > 0": n_pos,
        "distinct days of grid cases with forecast > 0": days_pos,
        "distinct days of all grid cases": int(g["day"].nunique()),
    }

    # slope and clustered t
    slope = None
    t = None
    if len(g) >= 3 and g["f"].var() > 0:
        x = g["f"].values
        y = g["ex"].values
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        slope = float(np.sum(xd * (y - y.mean())) / sxx)
        a = y.mean() - slope * x.mean()
        e = y - a - slope * x
        sc = pd.Series(xd * e).groupby(g["day"].values).sum()
        G = len(sc)
        if G > 1:
            var_b = (G / (G - 1)) * float(np.sum(sc.values ** 2)) / sxx ** 2
            if var_b > 0:
                t = float(slope / np.sqrt(var_b))

    # supporting check
    sup_val = None
    sup_pass = None
    if n_pos > 0 and pos["f"].sum() > 0:
        sup_val = float(np.sum(pos["f"] * pos["ex"]) / np.sum(pos["f"]))
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "slope t, same-day cases clustered", "value": t} if t is not None else None,
            "threshold": threshold}
    sup = {"name": "forecast-weighted mean excess 45-day return over grid cases with forecast > 0, above 0",
           "value": sup_val, "passed": sup_pass}

    if n_pos < 100 or days_pos < 30:
        status = "not observable"
        decided = (f"Minimum not reached: {n_pos} grid cases with forecast > 0 (need 100) over "
                   f"{days_pos} distinct days (need 30).")
    elif t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule: the slope t is at least 2 and the forecast-weighted mean excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "Reject rule: the slope t is at most -2, deeper falls are followed by weaker 45-day moves."
    elif t >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
