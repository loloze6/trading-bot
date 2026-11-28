import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_fall_3d.last_history_value"

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            price_ret3 = np.full(len(df), np.nan)
            if len(df) > H:
                price_ret3[H:] = close[H:] / close[:-H] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            fall_val = np.where(np.isnan(raw), price_ret3, raw)
            fell = np.where(np.isnan(fall_val), False, fall_val < 0)
            in_profile = (df["regime"].astype(str).values == "unknown")
            active = fc != 0
            situ = fell & in_profile & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 3-bar move of short bets, short direction"
    main_thr = "day-clustered t >= 2 confirms (with supporting difference > 0); t <= -2 rejects"
    sup_name = "large-|forecast| half mean unusual move minus small half"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling-calm "
                           "profile (regime 'unknown') after a 3-day fall, as the Fidelity's situation requires."
                           if n_active > 0 else "No active bars: the forecast is never non-zero."),
            "reading": "Situation = regime 'unknown' (profile not vetoed) and a negative raw 3-day scaled return "
                       "(price 3-bar return where the raw value is missing), with a negative forecast.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, absfc)
    for coin, wins in bars.items():
        # normal drift: mean non-overlapping 3-bar return over all windows of the coin
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = to_time(df["timestamp"])
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # short bets: rise of short magnitude by >= band from its lowest level since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                m = -fc[i] if fc[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                day = ts.iloc[t].floor("D")
                coin_cases.append((coin, day, r, abs(fc[t])))
        if not coin_cases:
            continue
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        if not np.isfinite(drift):
            continue
        for c, d, r, a in coin_cases:
            cases.append((c, d, -(r - drift), a))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([c[2] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([c[1] for c in cases]).sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    diff = None
    sup_pass = None
    if n_cases > 0:
        a = np.array([c[3] for c in cases])
        u = np.array([c[2] for c in cases])
        med = np.median(a)
        large = u[a > med]
        small = u[a <= med]
        if len(large) > 0 and len(small) > 0:
            diff = float(large.mean() - small.mean())
            sup_pass = bool(diff > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "day-clustered t", "value": t_val} if t_val is not None else None,
            "threshold": main_thr}
    sup = {"name": sup_name, "value": diff, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases on distinct days ({n_days}), the plan's minimum sample."
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the large-minus-small difference is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less: the scaled falls reverse against the drift."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "A confirming t of 2 or more with a supporting difference of 0 or less (or not computable) is inconclusive."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the "
                    "last bet, reset at flat) in each 3-bar grid cell of a window, with its 3-bar return inside the "
                    "window; drift is the coin's mean non-overlapping 3-bar return over all its windows; the t clusters "
                    "by UTC day with a G/(G-1) correction; the large half is |forecast| above the median, the small half "
                    "at or below it; the 30-case minimum counts distinct days and, as a minimum count, gives 'not observable'."),
    }
