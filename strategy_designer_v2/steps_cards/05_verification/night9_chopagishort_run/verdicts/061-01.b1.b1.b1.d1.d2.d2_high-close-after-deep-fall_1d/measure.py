import numpy as np
import pandas as pd


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 5
    BAND = 2.0
    FC = "forecast"
    DEPTH = "debug_info.components.depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            hi = df["high"].astype(float).values
            lo = df["low"].astype(float).values
            cl = df["close"].astype(float).values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                cloc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            ret5 = pd.Series(cl).pct_change(H).values
            if DEPTH in df.columns:
                rec = pd.to_numeric(df[DEPTH], errors="coerce").values
                ret5 = np.where(np.isnan(ret5) & ~np.isnan(rec), rec, ret5)
            sit = (cloc >= 0.8) & (ret5 < 0)
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & sit & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean short-side unusual 5-bar move per case"
    thr = "mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject"
    reading = ("A case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the "
               "last bet, from 0 after flat) in each non-overlapping 5-bar grid cell from each window's first row, "
               "needing close[t+5] in the same window; the coin's drift is the mean of its non-overlapping 5-bar "
               "returns over all windows; the day-pooled t sums deviations per entry day with a D/(D-1) correction; "
               "the halves are the n//2 largest and n//2 smallest |forecast| (middle case dropped if odd); the plan's "
               "100-day minimum, unmet, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on the short side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the close is in "
                           "the top fifth of the day's range while the 5-bar return is below zero."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rs.append(c[i + H] / c[i] - 1)
        drift[coin] = float(np.mean(rs)) if rs else np.nan

    cases = []  # (day, unusual, absf)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            ts = _to_dt(df["timestamp"])
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            side = 0
            for i in range(n):
                fi = f[i]
                s = 1 if fi > 0 else (-1 if fi < 0 else 0)
                if s == 0:
                    side, ref = 0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                mag = abs(fi)
                if mag - ref >= BAND:
                    if s < 0:
                        bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not np.isfinite(drift[coin]):
                    continue
                if not (c[t] > 0 and np.isfinite(c[t + H])):
                    continue
                r = c[t + H] / c[t] - 1
                u = -(r - drift[coin])
                cases.append((ts.iloc[t].date(), float(u), float(abs(f[t]))))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    counts = {"distinct days with cases": n_days, "cases": n_cases}

    mean_u = None
    tstat = None
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        mean_u = float(u.mean())
        if n_days > 1:
            dev = pd.Series(u - mean_u, index=[x[0] for x in cases]).groupby(level=0).sum().values
            var = (dev ** 2).sum() / n_cases ** 2 * n_days / (n_days - 1)
            se = np.sqrt(var)
            tstat = float(mean_u / se) if se > 0 else None
        if n_cases >= 2:
            af = np.array([x[2] for x in cases])
            order = np.argsort(af, kind="mergesort")
            k = n_cases // 2
            small = u[order[:k]]
            large = u[order[n_cases - k:]]
            sup_val = float(large.mean() - small.mean())
            sup_pass = bool(sup_val > 0)

    stat = {"name": "t of the mean, cases of one day pooled", "value": tstat} if tstat is not None else None
    main = {"name": main_name, "value": mean_u, "statistic": stat, "threshold": thr}
    supp = {"name": "mean unusual move, larger half of |forecast| minus smaller half",
            "value": sup_val, "passed": sup_pass}

    if n_days < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 distinct days with cases is not reached ({n_days} days)."
    elif tstat is None:
        status = "inconclusive"
        decided = "The day-pooled t cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean short-side unusual move is above 0 with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "A confirm-level t whose supporting check (larger half minus smaller half > 0) fails."
    elif mean_u < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean short-side unusual move is below 0 with t <= -2: prices rose more than their drift."
    else:
        status = "inconclusive"
        decided = "The day-pooled t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
