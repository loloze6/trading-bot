import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RATIO_MIN = 1.5
    MIN_CASES = 30
    MIN_DAYS = 30
    RISE_COL = "debug_info.components.rise20.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            hi = pd.to_numeric(d["high"], errors="coerce")
            lo = pd.to_numeric(d["low"], errors="coerce")
            rng = hi - lo
            mean_rng = rng.rolling(20, min_periods=20).mean()
            ratio = rng / mean_rng.replace(0, np.nan)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            raw = pd.to_numeric(d[RISE_COL], errors="coerce") if RISE_COL in d.columns else pd.Series([np.nan] * len(d))
            for i in range(len(d)):
                fi = f.iloc[i]
                if pd.isna(fi) or fi == 0:
                    continue
                n_active += 1
                r = ratio.iloc[i]
                if pd.notna(r):
                    wide = r >= RATIO_MIN - 1e-9
                else:
                    wide = regime.iloc[i] == "trending"
                rv = raw.iloc[i]
                rise_ok = True if pd.isna(rv) else (rv > 0)
                if wide and rise_ok and fi > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is a bar whose high-low range is at least 1.5 times the mean range of the last 20 bars "
               "(today included) within the window, with the regime column used where 20 recorded bars are not yet "
               "available, and a positive raw 20-day rise where recorded, on the long side; a case is the first bet "
               "(forecast rise of at least 2 points from its lowest long level since the last bet, from 0 after a flat) "
               "in each 3-bar grid cell of a window, with a full 3-bar return inside the window; the drift is the mean "
               "non-overlapping 3-bar return of the coin over all its windows; the t sums the deviations per UTC day; "
               "the upper half is the cases with forecast above the median, the lower half the rest.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars on a wide day "
                           "(range >= 1.5 x 20-day mean range) after a positive 20-day rise, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. Cases ----------
    cases = []  # (coin, day, ret, forecast)
    drift = {}
    for coin, wins in bars.items():
        rets_all = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            # drift grid
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    rets_all.append(c1 / c0 - 1.0)
            # bets
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi <= 0:
                    low = 0.0
                    continue
                if fi - low >= BAND - 1e-12:
                    bet[i] = True
                    low = fi
                else:
                    low = min(low, fi)
            for cell in range(0, n, H):
                idx = [i for i in range(cell, min(cell + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                coin_cases.append((coin, ts.iloc[i].floor("D"), c1 / c0 - 1.0, float(f[i])))
        if rets_all:
            drift[coin] = float(np.mean(rets_all))
        for c in coin_cases:
            if c[0] in drift:
                cases.append(c)

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)

    main_name = "mean unusual 3-bar move after the cases (return minus the coin's normal 3-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 and upper half beats lower half; reject: mean < 0 with t <= -2"
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        mean_u = None
        if n_cases > 0:
            mean_u = float(np.mean([c[2] - drift[c[0]] for c in cases]))
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": mean_u, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases on at least 30 distinct days is not reached.",
            "reading": reading,
        }

    u = np.array([c[2] - drift[c[0]] for c in cases])
    fc = np.array([c[3] for c in cases])
    day_arr = [c[1] for c in cases]
    mean_u = float(u.mean())
    dev = pd.Series(u - mean_u).groupby(pd.Index(day_arr)).sum().values
    se = float(np.sqrt(np.sum(dev ** 2)) / n_cases)
    t = float(mean_u / se) if se > 0 else 0.0

    med = float(np.median(fc))
    upper = u[fc > med]
    lower = u[fc <= med]
    if len(upper) > 0 and len(lower) > 0:
        diff = float(upper.mean() - lower.mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False
    counts["upper half cases"] = int(len(upper))
    counts["lower half cases"] = int(len(lower))

    if mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the upper half beats the lower half."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the upper half does not beat the lower half, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": {"name": "t of the mean, cases pooled by day", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "upper-half minus lower-half mean unusual move (split at median forecast)",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
