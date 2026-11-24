import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    EPS = 1e-9

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unknown = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            o = d["open"].astype(float)
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            c = d["close"].astype(float)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            rng = h - l
            mean_rng = rng.rolling(20, min_periods=20).mean()
            width = rng / mean_rng.replace(0, np.nan)
            body = (c - o).abs() / rng.replace(0, np.nan)
            known = width.notna() & body.notna()
            situ = (width >= 1.5 - EPS) & (body <= 0.1 + EPS)
            active = f.notna() & (f != 0)
            n_active_unknown += int((active & ~known).sum())
            act_k = active & known
            n_active += int(act_k.sum())
            n_agree += int((act_k & situ & (f < 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    main_name = "mean unusual 5-day move in the short direction after a bet"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 (and check passes); reject: t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are wide flat days "
                           "(range >= 1.5x the 20-day mean range, body <= 10% of range) with a short forecast."),
            "reading": "Bars whose 20-day mean range cannot be computed inside the window were left out of the check.",
        }

    # ---------- 2. Cases ----------
    cases = []  # (day, unusual_short, abs_forecast)
    for coin, wins in bars.items():
        # normal drift: non-overlapping 5-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).to_numpy()
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            ref = 0.0
            used_cells = set()
            for t in range(n):
                m = -f[t] if f[t] < 0 else 0.0
                bet = False
                if m <= 0:
                    ref = 0.0
                else:
                    if m - ref >= BAND - EPS:
                        bet = True
                        ref = m
                    else:
                        ref = min(ref, m)
                if not bet:
                    continue
                cell = t // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if t + H >= n or not np.isfinite(c[t]) or not np.isfinite(c[t + H]) or c[t] == 0:
                    continue
                ret = c[t + H] / c[t] - 1.0
                unusual = -(ret - drift)
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), unusual, abs(f[t])))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}
    sc_out = {"agreement": (float(agreement) if agreement is not None else None), "passed": True}
    reading = ("A bet is a fall of the forecast at least 2 points below its lowest short level since the last bet "
               "(from 0 after a flat), the first bet of each 5-bar grid cell per window is the case; the drift is each "
               "coin's mean non-overlapping 5-bar return over all its windows; the t uses day-clustered errors with a "
               "G/(G-1) correction; above-median means |forecast| strictly above the median, below-median the rest; "
               "the plan's 30-case and 30-day minimums are applied as 'not observable'.")

    if n_cases < 30 or n_days < 30:
        return {
            "status": "not observable",
            "situation_check": sc_out,
            "main_measure": {"name": main_name,
                             "value": (float(np.mean([x[1] for x in cases])) if n_cases else None),
                             "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases on at least 30 distinct days is not reached.",
            "reading": reading,
        }

    x = np.array([v[1] for v in cases], dtype=float)
    a = np.array([v[2] for v in cases], dtype=float)
    dlist = [v[0] for v in cases]
    mean = float(x.mean())
    dev = pd.Series(x - mean).groupby(pd.Series(dlist)).sum().to_numpy()
    G = len(dev)
    var_mean = (G / (G - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2) if G > 1 else np.nan
    se = np.sqrt(var_mean) if np.isfinite(var_mean) else np.nan
    t_stat = float(mean / se) if (se is not None and np.isfinite(se) and se > 0) else float("nan")

    med = float(np.median(a))
    above = x[a > med]
    below = x[a <= med]
    if len(above) > 0 and len(below) > 0:
        diff = float(above.mean() - below.mean())
        check_pass = bool(diff > 0)
    else:
        diff = None
        check_pass = False

    if np.isfinite(t_stat) and mean > 0 and t_stat >= 2 and check_pass:
        status = "confirmed"
        decided = "The mean unusual move in the short direction is positive with t >= 2 and the above-median cases move more."
    elif np.isfinite(t_stat) and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction has t <= -2: the coin keeps rising after wide flat days."
    elif np.isfinite(t_stat) and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sc_out,
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": {"name": "t of the mean, cases of one day taken together",
                                       "value": (t_stat if np.isfinite(t_stat) else None)},
                         "threshold": main_thr},
        "supporting_check": {"name": "mean unusual move above-median |forecast| minus below-median",
                             "value": diff, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
