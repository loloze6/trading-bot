import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    LOC_MIN = 0.75
    MIN_CASE_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_undetermined = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            rng = hi - lo
            loc = (c - lo) / rng.where(rng > 0)
            up = c / c.shift(1) - 1.0
            prior_fall = c.shift(1) - c.shift(6)
            determinable = loc.notna() & up.notna() & prior_fall.notna()
            situation = (loc >= LOC_MIN) & (up > 0) & (prior_fall < 0)
            active = f != 0
            n_undetermined += int((active & ~determinable).sum())
            act_det = active & determinable
            n_active += int(act_det.sum())
            n_agree += int((act_det & situation & (f < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = ("Situation computed from prices as close location (close-low)/(high-low) >= 0.75, close above prior close, "
               "and close[t-1] < close[t-6] inside each window, with active bars whose situation cannot be computed "
               "(window start) left out of the agreement; cases are short bets (forecast falling by at least 2 points "
               "below its lowest short level since the last bet, from 0 after a flat), the first bet of each 5-bar grid "
               "cell per window; drift is the coin's mean non-overlapping 5-bar return over all its windows; the t "
               "clusters deviations by UTC day; the halves split the cases sorted by |forecast| at the signal bar into "
               "the top and bottom n//2 (the middle case dropped when n is odd); fewer than 30 case-days gives "
               "'not observable' as the workflow requires.")

    main_name = "mean unusual 5-bar move of short cases (return minus coin drift, signed short)"
    threshold = "t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; at least 30 case-days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars undetermined": n_undetermined},
            "decided_by": ("Fewer than 90% of active bars are short bars of the plan's situation (top-quarter close, up day, "
                           "close one day ago below the close five days before it): the config's forecast does not do what "
                           "the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, forecast)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            n = len(c)
            for p in range(0, n - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).to_numpy()
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                s = -f[t] if f[t] < 0 else 0.0
                if f[t] >= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND:
                    ref = s
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and c[t] > 0 and np.isfinite(c[t]) and np.isfinite(c[t + H]):
                        r = c[t + H] / c[t] - 1.0
                        cases.append((coin, ts.iloc[t].floor("D"), r, abs(f[t])))
                else:
                    ref = min(ref, s)

    rows = [(co, day, -(r - drift[co]), af) for (co, day, r, af) in cases if np.isfinite(drift.get(co, np.nan))]
    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)
    counts = {"case-days": n_days, "cases": n_cases}

    mean_u = None
    t_stat = None
    if n_cases > 0:
        u = np.array([r[2] for r in rows])
        mean_u = float(np.mean(u))
        if n_days >= 2:
            dev = pd.Series(u - mean_u, index=[r[1] for r in rows]).groupby(level=0).sum().to_numpy()
            var = np.sum(dev ** 2) * n_days / (n_days - 1)
            se = np.sqrt(var) / n_cases
            t_stat = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        order = sorted(rows, key=lambda r: r[3])
        k = n_cases // 2
        small = np.array([r[2] for r in order[:k]])
        large = np.array([r[2] for r in order[n_cases - k:]])
        sup_val = float(large.mean() - small.mean())
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases clustered by day", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold}
    sup = {"name": "mean unusual move, larger half of |forecast| minus smaller half", "value": sup_val, "passed": sup_pass}

    if n_days < MIN_CASE_DAYS or t_stat is None:
        status = "not observable"
        decided = f"Only {n_days} case-days, fewer than the plan's minimum of 30."
    elif t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main measure t >= 2 in the short's favour and the supporting check passes (confirm rule)."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "Main measure t >= 2 but the supporting check fails (inconclusive rule)."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Main measure t <= -2: prices rise more than drift after the cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "Main measure t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
