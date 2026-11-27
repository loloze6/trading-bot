import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            n = len(d)
            for t in range(n):
                if f[t] == 0:
                    continue
                n_active += 1
                # the down close breaking an up run of 2 or more days, inside the window
                dip = False
                if t >= 1 and np.isfinite(c[t]) and np.isfinite(c[t - 1]) and c[t] < c[t - 1]:
                    k = 0
                    j = t - 1
                    while j >= 1 and k < 30 and c[j] > c[j - 1]:
                        k += 1
                        j -= 1
                    dip = k >= 2
                # the rising agitated profile: the detector's decision (its components are not recorded)
                prof = reg[t] == "mean_reversion"
                if dip and prof and f[t] < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("The up run is recomputed from closes inside each window (strict up closes, ties break it), the rising agitated "
               "profile is read from the detector's regime 'mean_reversion' since its 60-bar trend and 365-bar volatility "
               "percentile cannot be rebuilt inside a window; a case is the first short bet (forecast rising by 2+ points on the "
               "short side) of each 5-bar grid cell; the day-grouped t uses clustered errors with a G/(G-1) correction; cases at "
               "the median |forecast| are left out of the supporting check; the plan's 30-day minimum is applied as 'not observable'.")

    main_name = "mean short-direction unusual move over 5 bars"
    main_thr = "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "days carrying cases": 0},
            "decided_by": ("Fewer than 90 % of the bars with a nonzero forecast are short bets on a down close breaking an up run "
                           "of 2+ days inside the rising agitated profile (%d of %d)." % (n_agree, n_active)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual, |forecast|)
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on the grid of all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            for p in range(0, len(d) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for d in prepared:
            c = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            ref = 0.0
            bets = np.zeros(n, dtype=bool)
            for t in range(n):
                if f[t] >= 0:
                    ref = 0.0
                    continue
                s = -f[t]
                if s - ref >= BAND:
                    bets[t] = True
                    ref = s
                else:
                    ref = min(ref, s)
            seen = set()
            for t in range(n):
                if not bets[t]:
                    continue
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = -(r - drift)
                cases.append((ts.iloc[t].floor("D"), u, abs(f[t])))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)

    mean_u = None
    t_stat = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        mean_u = float(u.mean())
        if n_days >= 2:
            dev = pd.Series(u - mean_u, index=[x[0] for x in cases]).groupby(level=0).sum().values
            G = len(dev)
            var = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_stat = float(mean_u / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        a = np.array([x[2] for x in cases])
        u = np.array([x[1] for x in cases])
        med = np.median(a)
        hi = u[a > med]
        lo = u[a < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"days carrying cases": int(n_days), "cases": int(n_cases), "active bars": int(n_active)}
    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean, cases grouped by day", "value": t_stat} if t_stat is not None else None),
            "threshold": main_thr}
    support = {"name": "mean unusual move above minus below the median |forecast|", "value": sup_val, "passed": sup_pass}

    if n_days < MIN_DAYS or t_stat is None:
        status = "not observable"
        decided = "Only %d days carry cases, below the plan's minimum of 30 days." % n_days
    elif mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure is above 0 with t >= 2 and the supporting check passes."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2: prices rise more than their usual drift after the dip."
    elif mean_u > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "The main measure confirms (above 0, t >= 2) but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The t of the main measure lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
