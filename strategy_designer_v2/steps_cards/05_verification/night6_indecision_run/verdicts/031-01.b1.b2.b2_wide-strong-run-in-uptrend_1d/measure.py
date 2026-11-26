import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    FC = "forecast"
    RAW = "debug_info.components.wide_run.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            ret60 = close / close.shift(60) - 1.0
            ret5 = close / close.shift(5) - 1.0
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series([np.nan] * len(df))
            for i in range(len(df)):
                if f.iloc[i] == 0:
                    continue
                n_active += 1
                r60, r5 = ret60.iloc[i], ret5.iloc[i]
                if np.isfinite(r60) and np.isfinite(r5):
                    in_sit = (r60 > 0) and (r5 > 0)
                else:
                    # prices before the recorded bars are not available: use the detector's recorded decision
                    in_sit = regime.iloc[i] == "trending"
                rv = raw.iloc[i]
                if np.isfinite(rv):
                    in_sit = in_sit and (rv > 0)
                if in_sit and f.iloc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("The 60-day and 5-day returns are recomputed from closes inside each window, and on bars too early in a "
               "window for that the recorded regime 'trending' stands for the detector's decision; a case is the first "
               "long bet (forecast rise of at least 2 points from its lowest level since the last bet, from 0 after a "
               "flat) in each 3-bar grid cell of a window with a 3-bar forward return inside the window; the normal "
               "drift is the coin's mean non-overlapping 3-bar return over all its windows; the day-pooled t uses the "
               "per-day sums of deviations with a D/(D-1) correction; the upper half is forecast above the median, the "
               "lower half forecast at or below it.")

    threshold = "confirm: mean > 0 with t >= 2 (and upper-minus-lower > 0); reject: mean < 0 with t <= -2"
    mname = "mean unusual 3-day move of long cases (return minus coin's normal 3-day drift)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mname, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the plan's "
                           "situation (60-day return > 0 and 5-day return > 0)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, forecast, ret)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            ref = 0.0
            taken_cells = set()
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    ref = 0.0
                    continue
                bet = (fi - ref) >= BAND
                if bet:
                    ref = fi
                else:
                    ref = min(ref, fi)
                if not bet:
                    continue
                cell = i // H
                if cell in taken_cells:
                    continue
                taken_cells.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                cases.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), float(fi), float(r - drift[coin])))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    t = None
    diff = None
    if n_cases > 0:
        u = np.array([c[3] for c in cases])
        mean_u = float(u.mean())
        dev = u - mean_u
        per_day = pd.Series(dev).groupby([c[1] for c in cases]).sum().values
        D = len(per_day)
        if D > 1:
            var = (D / (D - 1.0)) * np.sum(per_day ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None
        fc = np.array([c[2] for c in cases])
        med = np.median(fc)
        up = u[fc > med]
        lo = u[fc <= med]
        if len(up) > 0 and len(lo) > 0:
            diff = float(up.mean() - lo.mean())

    sup_pass = None if diff is None else bool(diff > 0)
    main = {"name": mname, "value": mean_u,
            "statistic": None if t is None else {"name": "t of the mean, same-day cases pooled", "value": t},
            "threshold": threshold}
    sup = {"name": "upper-half minus lower-half mean unusual move (split at median forecast)",
           "value": diff, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 30 or n_days < 30:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": f"Minimum not reached: {n_cases} cases on {n_days} distinct days, the plan needs at least 30 of each.",
                "reading": reading}

    if t is not None and mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            dec = "The mean unusual move is positive with t >= 2 and the upper-half minus lower-half difference is above 0."
        else:
            status = "inconclusive"
            dec = "t >= 2 but the supporting check (upper-half minus lower-half above 0) fails, which the plan calls inconclusive."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        dec = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        dec = "The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": dec, "reading": reading}
