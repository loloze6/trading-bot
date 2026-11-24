import numpy as np
import pandas as pd


def measure(bars):
    FC = "debug_info.components.near_high.post_pipeline_value"
    H = 2
    TOL = 1e-12

    # ---------- 1. situation check: Friday bar (UTC) with a positive 14-bar return, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            for i in range(n):
                if abs(fc[i]) <= TOL:
                    continue
                if i < 14:
                    # the 14-bar return cannot be computed from this window's prices: not judged
                    continue
                n_active += 1
                friday = ts.iloc[i].weekday() == 4
                rise = close[i] / close[i - 14] - 1.0 > 0.0
                if friday and rise and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    sit_reading = ("Friday = timestamp (bar start, UTC) weekday 4 and the 14-bar return is "
                   "close[t]/close[t-14]-1 inside the window; active bars in a window's first 14 rows, "
                   "where it cannot be computed, are left out of the agreement")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are post-rise Friday bars with a long forecast, "
                           "as the Fidelity's situation and side require."),
            "reading": sit_reading + ".",
        }

    # ---------- 2. criterion ----------
    # coin's mean 2-bar return on the non-overlapping grid over all its windows
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            if FC not in df.columns:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].astype(float).values
            reg = df["regime"].astype(str).values
            f = pd.to_numeric(df[FC], errors="coerce").values
            for i in range(len(df) - H):
                if reg[i] != "trending":
                    continue
                if ts.iloc[i].weekday() != 4:
                    continue
                if not np.isfinite(f[i]) or not np.isfinite(coin_mean[coin]):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append({"day": ts.iloc[i].normalize(), "x": float(f[i]),
                             "y": float(r - coin_mean[coin])})

    cases = pd.DataFrame(rows, columns=["day", "x", "y"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t = None
    wmean = None
    if n_cases >= 3:
        x = cases["x"].values
        y = cases["y"].values
        xm = x.mean()
        sxx = float(((x - xm) ** 2).sum())
        if sxx > 0:
            b = float(((x - xm) * (y - y.mean())).sum() / sxx)
            a = float(y.mean() - b * xm)
            e = y - a - b * x
            cases = cases.assign(s=(x - xm) * e)
            sd = cases.groupby("day")["s"].sum().values
            G = len(sd)
            if G > 1:
                var_b = (G / (G - 1)) * float((sd ** 2).sum()) / sxx ** 2
                if var_b > 0:
                    t = float(b / np.sqrt(var_b))
            slope = b
        sw = float(x.sum())
        if sw != 0:
            wmean = float((y * x).sum() / sw)

    sup_pass = None if wmean is None else bool(wmean > 0)
    counts = {"cases": n_cases, "distinct Fridays": n_days}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided_by = (f"Minimum not reached: the plan needs at least 100 cases on at least 50 distinct Fridays "
                      f"({n_cases} cases on {n_days} Fridays).")
    elif t is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "Confirm: slope t >= 2 and the forecast-weighted mean excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided_by = "Reject: slope t <= -2, weekends after closes nearer the yearly high do worse than the coin's drift."
    elif t >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive: slope t >= 2 but the forecast-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of excess weekend return on forecast (post_pipeline_value)",
            "value": slope,
            "statistic": None if t is None else {"name": "slope t, deviations summed per day (day-clustered)",
                                                 "value": t},
            "threshold": "confirm at t >= 2 (with weighted mean excess > 0), reject at t <= -2",
        },
        "supporting_check": {"name": "forecast-weighted mean excess weekend return > 0",
                             "value": wmean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": (sit_reading + "; a case is a Friday bar with regime 'trending', a recorded post_pipeline_value "
                    "and close[t+2] in the same window; 'deviations summed per day' is read as a day-clustered "
                    "standard error of the slope (slope-score terms (x-mean x)*residual summed per day, factor G/(G-1)); "
                    "a missing minimum count gives 'not observable' as the workflow requires."),
    }
