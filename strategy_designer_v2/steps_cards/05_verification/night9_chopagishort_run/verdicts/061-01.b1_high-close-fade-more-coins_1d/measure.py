import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    BAND = 2.0
    CL_MIN = 0.8
    MIN_CASES = 30
    MIN_DAYS = 30
    TOL = 1e-9
    CL_COL = "debug_info.components.high_close.last_history_value"

    def close_location(df):
        hi = df["high"].astype(float).values
        lo = df["low"].astype(float).values
        cl = df["close"].astype(float).values
        rng = hi - lo
        with np.errstate(divide="ignore", invalid="ignore"):
            loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
        if CL_COL in df.columns:
            rec = pd.to_numeric(df[CL_COL], errors="coerce").values
            loc = np.where(np.isfinite(rec), rec, loc)
        return loc

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            loc = close_location(df)
            reg = df["regime"].astype(str).values
            active = fc != 0
            situ = (np.nan_to_num(loc, nan=-1.0) >= CL_MIN - TOL) & (reg == "mean_reversion")
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    reading = ("The choppy-agitated profile is taken from the recorded regime (mean_reversion is only reached when no "
               "chop veto fires, since the detector's trend and volatility components are not recorded and their "
               "warm-up is not in the record) together with the close location >= 0.8 from the prices and the short side; "
               "a case is the first short bet (forecast rise of >= 2 points on the short side from its lowest level since the "
               "last bet) in each non-overlapping 2-bar grid cell of a window, its return taken from that bar's close 2 bars "
               "ahead in the same window; the median split puts cases above the median close location in the upper half; "
               "the t clusters cases by UTC day with a G/(G-1) correction; fewer than the plan's minimum counts is reported "
               "as not observable.")

    thr_text = "mean unusual fall > 0 with t >= 2 confirms (with upper-minus-lower > 0); < 0 with t <= -2 rejects"
    main_name = "mean unusual 2-bar fall per short case (drift removed, sign flipped)"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_text},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 30 cases on 30 distinct days is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_text},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with a close location >= 0.8 inside the "
                           "choppy-agitated regime, so the config does not do what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, return, cl)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for i in range(0, n - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            loc = close_location(df)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.strftime("%Y-%m-%d").values
            # bets on the short side
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if fc[i] < 0:
                    s = -fc[i]
                    if s - ref >= BAND - TOL:
                        bet[i] = True
                        ref = s
                    else:
                        ref = min(ref, s)
                else:
                    ref = 0.0
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                cases.append((coin, days[t], c[t + H] / c[t] - 1.0, loc[t]))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    rows = []
    for coin, day, r, l in cases:
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        rows.append((day, -(r - d), l))
    n_cases = len(rows)
    day_arr = np.array([r[0] for r in rows], dtype=object)
    u = np.array([r[1] for r in rows], dtype=float)
    cl = np.array([r[2] for r in rows], dtype=float)
    n_days = int(len(set(day_arr.tolist()))) if n_cases else 0

    mean_u = float(np.mean(u)) if n_cases else None
    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        dev = u - mean_u
        s = pd.Series(dev).groupby(pd.Series(day_arr)).sum().values
        G = len(s)
        var = (G / (G - 1)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            t_stat = float(mean_u / np.sqrt(var))

    diff = None
    m = np.isfinite(cl)
    if m.sum() >= 2:
        med = np.median(cl[m])
        up = u[m][cl[m] > med]
        lo = u[m][cl[m] <= med]
        if len(up) > 0 and len(lo) > 0:
            diff = float(np.mean(up) - np.mean(lo))
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum of {MIN_CASES} cases on {MIN_DAYS} distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual fall cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = ("The mean unusual fall is above 0 with t >= 2 and the upper-half minus lower-half "
                       "difference is above 0 (confirm rule).")
        else:
            status = "inconclusive"
            decided = ("The mean unusual fall is above 0 with t >= 2 but the upper-half minus lower-half difference "
                       "is not above 0: a confirming main measure with a failed supporting check is inconclusive.")
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual fall is below 0 with t <= -2: prices rise after high closes (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual fall lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases clustered by day", "value": t_stat},
            "threshold": thr_text,
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean unusual fall, split at median close location",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
