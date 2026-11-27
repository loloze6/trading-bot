import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.high_close_wide.last_history_value"
    BAND = 2.0
    H = 1

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
            unit = "s" if v < 1e11 else ("ms" if v < 1e14 else ("us" if v < 1e17 else "ns"))
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            hi = df["high"].astype(float)
            lo = df["low"].astype(float)
            cl = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rng = hi - lo
            mid = (hi + lo) / 2.0
            loc = (cl - lo) / rng.replace(0, np.nan)
            # mean range: from the recorded raw value where it exists, else from prices in the window
            mean_rng_px = rng.rolling(20, min_periods=20).mean()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                mean_rng_raw = (cl - mid) / raw.replace(0, np.nan)
                mean_rng = mean_rng_raw.where(mean_rng_raw.notna() & (mean_rng_raw > 0), mean_rng_px)
            else:
                mean_rng = mean_rng_px
            width = rng / mean_rng
            situ = (width > 1.0) & (loc > 0.5)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ.fillna(False) & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("no active bars to compare with the plan's situation" if n_active == 0 else
                           "fewer than 90% of the bars with a non-zero forecast are short bars with a range above "
                           "its 20-day mean range and a close above the range's middle"),
            "reading": "situation = range / 20-bar mean range (current bar included, taken from the recorded raw "
                       "value where present) > 1 and close location > 0.5, expected side short.",
        }

    # ---------- 2. criterion ----------
    # coin drift: mean 1-bar return over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = df["close"].astype(float).values
            rets.append(c[1:] / c[:-1] - 1.0)
        rets = np.concatenate(rets) if rets else np.array([])
        rets = rets[np.isfinite(rets)]
        drift[coin] = float(np.mean(rets)) if len(rets) else np.nan

    cases = []  # (day, unusual move, size)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            cl = df["close"].astype(float).values
            ts = to_time(df["timestamp"])
            ref = 0.0
            for t in range(len(df)):
                f = fc[t]
                if f >= 0:
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND:
                    ref = m
                    if t + H < len(df) and np.isfinite(cl[t]) and np.isfinite(cl[t + H]) and np.isfinite(drift[coin]):
                        r = cl[t + H] / cl[t] - 1.0
                        u = -(r - drift[coin])
                        cases.append((ts.iloc[t].floor("D"), u, m))
                else:
                    ref = min(ref, m)

    n = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"cases": n, "distinct days": n_days}

    mean_u = None
    tval = None
    if n > 0:
        u = np.array([c[1] for c in cases])
        mean_u = float(np.mean(u))
        if n_days > 1:
            dev = pd.Series(u - mean_u, index=[c[0] for c in cases]).groupby(level=0).sum().values
            var = n_days / (n_days - 1) * np.sum(dev ** 2) / n ** 2
            se = np.sqrt(var)
            tval = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n > 0:
        sizes = np.array([c[2] for c in cases])
        u = np.array([c[1] for c in cases])
        med = np.median(sizes)
        big = u[sizes > med]
        small = u[sizes <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(np.mean(big) - np.mean(small))
            sup_pass = bool(sup_val >= 0)

    main = {
        "name": "mean next-day unusual move in the short direction (return minus coin drift)",
        "value": mean_u,
        "statistic": {"name": "t of the mean, same-day cases clustered", "value": tval} if tval is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2",
    }
    supporting = {"name": "mean unusual move of cases above median forecast size minus at/below median",
                  "value": sup_val, "passed": sup_pass}
    reading = ("cases are short bets (forecast fall of >= 2 points from its lowest short level since the last bet, "
               "reset at 0) on every bar (1-bar grid) with a next bar in the window; larger cases are those with size "
               "strictly above the median, smaller those at or below it; the t clusters cases by UTC day; the plan's "
               "minimum counts give 'not observable'.")

    if n < 50 or n_days < 30:
        status = "not observable"
        decided = "minimum counts not reached: fewer than 50 cases or cases on fewer than 30 distinct days."
    elif tval is None:
        status = "inconclusive"
        decided = "the t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean unusual move positive with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "confirming t but the supporting check fails, which the plan calls inconclusive."
    elif mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "mean unusual move negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
