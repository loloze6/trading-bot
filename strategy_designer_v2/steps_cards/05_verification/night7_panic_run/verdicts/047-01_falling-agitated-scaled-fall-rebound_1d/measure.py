import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    LHV = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(d["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if LHV in d.columns:
                lhv = pd.to_numeric(d[LHV], errors="coerce")
            else:
                lhv = pd.Series(np.nan, index=d.index)
            # down day: the component's raw value (return / 30-day swing) below 0;
            # where it is not recorded, the day's close-to-close return from the prices
            down = np.where(lhv.notna(), lhv < 0, ret1 < 0)
            down = pd.Series(down, index=d.index).astype(bool)
            # falling agitated profile: the detector's decision (its components are not recorded);
            # the vetoes send trend >= -10 or swing <= 0.5 to "chop", leaving "unknown" as the profile
            in_profile = d["regime"].astype(str) == "unknown"
            active = fc != 0
            agree = active & down & in_profile & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 3-day move after forecast > 0 (long), minus the coin's normal 3-day drift"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 case-days and slope > 0; reject: mean < 0 with t <= -2 over >= 30 case-days"
    reading = ("Situation bars are taken as regime 'unknown' (the profile left by the vetoes) with a negative "
               "scaled_fall raw value (or a negative close-to-close return where unrecorded), side long; cases are "
               "grid bars 0,3,6,... of each window with forecast > 0 and a close 3 bars later in the same window, "
               "drift is the coin's mean 3-bar return on that grid over all its windows, and t uses the standard "
               "error from per-day summed deviations with the number of distinct case days as n.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"case-days": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars on down days inside the "
                           "falling-agitated profile, so the config does not do what the plan's Fidelity says."
                           if n_active > 0 else "No bar has a nonzero forecast, so the plan's situation is never traded."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    grid_rets = {}
    cases = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                f = fc[i]
                if np.isfinite(f) and f > 0 and not pd.isna(ts.iloc[i]):
                    cases.append((coin, ts.iloc[i].floor("D"), float(f), r))
        grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    rows = [(c, day, f, r - grid_rets[c]) for (c, day, f, r) in cases if np.isfinite(grid_rets.get(c, np.nan))]
    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)

    mean_u = None
    t = None
    slope = None
    if n_cases > 0:
        u = np.array([r[3] for r in rows])
        f = np.array([r[2] for r in rows])
        day_s = pd.Series([r[1] for r in rows])
        mean_u = float(u.mean())
        if n_days >= 2:
            dev = pd.Series(u - mean_u).groupby(day_s.values).sum().values
            K = len(dev)
            var = (dev ** 2).sum() * K / (K - 1) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None
        if n_cases >= 2 and np.unique(f).size >= 2:
            slope = float(np.polyfit(f, u, 1)[0])

    slope_pass = None if slope is None else bool(slope > 0)
    counts = {"case-days": int(n_days), "cases": int(n_cases), "active bars": int(n_active)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 case-days, and the slope on the forecast is positive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 case-days."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the forecast is at or below 0 (or not computable): inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": {"name": "t of the mean, same-day cases summed per day", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": "least-squares slope of unusual move on forecast, > 0", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
