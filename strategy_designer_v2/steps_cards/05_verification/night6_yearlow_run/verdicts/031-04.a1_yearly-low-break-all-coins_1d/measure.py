import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    LHV = "debug_info.components.depth.last_history_value"

    # ---------- 1. Situation check: active bars must be closes below the prior 365-day closing low, long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").values
            else:
                lhv = np.full(len(df), np.nan)
            active = f != 0
            n_active += int(active.sum())
            situ = np.where(np.isnan(lhv), False, lhv < 0)
            n_agree += int((active & situ & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else bool(agreement >= 0.90)

    main_name = "mean unusual 10-bar move of long cases (return from signal close minus coin's normal 10-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; min 30 cases on 20 distinct days"
    check_name = "mean unusual move of above-median-forecast cases minus below-median-forecast cases > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars whose close is below the prior "
                          "365-day closing low (recorded depth < 0), so the config does not do what the plan's Fidelity says.",
            "reading": "The situation is read from the recorded depth component (raw percent distance to the prior 365-day "
                       "closing low) being below 0; an active bar without that value counts as outside the situation.",
        }

    # ---------- 2. Coin drift: mean of non-overlapping 10-bar returns on each window's grid, all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: long bets (forecast rise >= band from its lowest level since last bet), once per grid cell ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.floor("D").values
            ref = 0.0
            used_cells = set()
            for t in range(len(f)):
                ft = f[t]
                if ft <= 0:
                    ref = 0.0
                    continue
                is_bet = (ft - ref) >= BAND
                if is_bet:
                    ref = ft
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H >= len(c):
                        continue
                    a, b = c[t], c[t + H]
                    if not (np.isfinite(a) and np.isfinite(b) and a > 0) or pd.isna(days[t]):
                        continue
                    r = b / a - 1.0
                    cases.append((days[t], r - drift[coin], ft))
                else:
                    ref = min(ref, ft)

    n_cases = len(cases)
    n_days = len(set(d for d, _, _ in cases))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    reading = ("A case is the first long bet (forecast rise of at least 2 points from its lowest long level since the last bet, "
               "from 0 after a flat) in each 10-bar grid cell of a window, cases whose 10-bar return leaves the window are dropped, "
               "the t uses a day-clustered standard error with a G/(G-1) correction, and cases with a forecast equal to the median "
               "are left out of the supporting check.")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": check_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases on at least 20 distinct days is not reached (no case).",
            "reading": reading,
        }

    u = np.array([x[1] for x in cases], dtype=float)
    fc = np.array([x[2] for x in cases], dtype=float)
    dser = pd.Series([x[0] for x in cases])
    mean_u = float(u.mean())

    # day-clustered t
    dev = pd.Series(u - mean_u).groupby(dser.values).sum().values
    G = len(dev)
    t_val = None
    if G > 1:
        var = (G / (G - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        if se > 0:
            t_val = float(mean_u / se)

    # supporting check
    med = float(np.median(fc))
    hi = u[fc > med]
    lo = u[fc < med]
    if len(hi) > 0 and len(lo) > 0:
        diff = float(hi.mean() - lo.mean())
        check_pass = bool(diff > 0)
    else:
        diff = None
        check_pass = False

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day summed", "value": t_val} if t_val is not None else None,
            "threshold": threshold}
    sup = {"name": check_name, "value": diff, "passed": check_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on at least 20 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if check_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and deeper breaks rebound more, meeting the confirm rule."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is above 0 with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 (breaks extend), meeting the reject rule."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
