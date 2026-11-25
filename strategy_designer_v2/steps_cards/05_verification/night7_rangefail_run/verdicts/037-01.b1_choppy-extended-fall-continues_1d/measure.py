import numpy as np
import pandas as pd


def measure(bars):
    H = 5          # horizon in bars, from the plan
    BAND = 2.0     # the holding period's band (forecast points), default
    LHV = "debug_info.components.fall_in_swings.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True)

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            # 20-day return from the window's own prices (never across windows)
            r20 = np.full(len(df), np.nan)
            if len(df) > 20:
                r20[20:] = close[20:] / close[:-20] - 1.0
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                fall = np.isfinite(raw[i]) and raw[i] < 0
                if np.isfinite(r20[i]):
                    in_fall20 = r20[i] < 0
                else:
                    # before 20 bars of the window, the detector's recorded decision stands in
                    in_fall20 = regime[i] == "trending"
                if fall and in_fall20 and fc[i] < 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.90)

    reading = ("Situation = raw fall_in_swings < 0 and 20-bar return < 0 recomputed from the window's closes "
               "(the recorded regime 'trending' stands in on the first 20 bars of a window), side short, the choppy "
               "profile not checked since the plan adds it by code; a case is a short bet (forecast growing more "
               "negative by at least 2 points from its smallest short size since the last bet, from 0 after a flat "
               "or side change), the first one in each 5-bar grid cell of its window, needing close 5 bars later in "
               "the same window; drift = mean of the coin's non-overlapping 5-bar grid returns over all its windows; "
               "t = mean over a day-clustered standard error (deviations summed per day, D/(D-1) correction); "
               "the slope is OLS of the unusual move on |forecast| at the case bar.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move per short case", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars where the 5-day "
                           "return in swing units is negative and the 20-day return is below 0, as the Fidelity states."),
            "reading": reading,
        }

    # ---------------- 2. criterion ----------------
    # coin's normal drift over 5 bars: non-overlapping grid returns of all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(close) - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, size)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            days = _ts(df).dt.strftime("%Y-%m-%d").values
            n = len(df)
            # short bets
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if fc[i] < 0:
                    mag = -fc[i]
                    if mag - ref >= BAND:
                        bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    ref = 0.0
            # one case per grid cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                ret = b / a - 1.0
                unusual = -(ret - drift[coin])
                cases.append((days[t], unusual, abs(fc[t])))

    n_cases = len(cases)
    n_days = len(set(c[0] for c in cases))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    t_stat = None
    slope = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases], dtype=float)
        s = np.array([c[2] for c in cases], dtype=float)
        d = np.array([c[0] for c in cases])
        mean_u = float(np.mean(u))
        dev = pd.Series(u - mean_u).groupby(d).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = float(np.sqrt(var))
            t_stat = float(mean_u / se) if se > 0 else None
        if n_cases > 1 and np.var(s) > 0:
            slope = float(np.sum((s - s.mean()) * (u - u.mean())) / np.sum((s - s.mean()) ** 2))

    slope_passed = None if slope is None else bool(slope > 0)

    main = {"name": "mean unusual 5-bar move per short case (short direction)",
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": "t >= 2 (with slope > 0) confirms; t <= -2 rejects; otherwise inconclusive"}
    support = {"name": "OLS slope of unusual move on forecast size", "value": slope, "passed": slope_passed}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on at least 30 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif t_stat >= 2 and slope_passed:
        status = "confirmed"
        decided = "The mean unusual move has t >= 2 and the supporting slope is above 0 (confirm rule)."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move has t <= -2: prices rise after these falls more than the coin's drift (reject rule)."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting slope is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
