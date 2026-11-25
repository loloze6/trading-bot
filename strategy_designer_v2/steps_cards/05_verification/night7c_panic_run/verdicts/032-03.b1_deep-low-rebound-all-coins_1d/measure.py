import numpy as np
import pandas as pd


def _to_dates(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        dt = pd.to_datetime(s, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D").dt.strftime("%Y-%m-%d").values


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_DAYS = 30

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            regime = df["regime"].astype(str).values
            in_regime = regime == "mean_reversion"
            # close is the lowest of the last 30 closes (current included), computable from 30 bars in the window
            rmin = pd.Series(close).rolling(30, min_periods=30).min().values
            low_ok = np.where(np.isnan(rmin), True, close <= rmin * (1 + 1e-9))
            situation = in_regime & low_ok
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    reading = ("The range-ratio condition (365-bar over 30-bar mean range at or below 1) cannot be rebuilt from "
               "windows of about 122 recorded bars and the detector's components are not recorded, so it is read from "
               "the recorded regime ('mean_reversion'), while the 30-bar closing low is recomputed from closes where "
               "30 bars of the window exist; a bet is a rise of the long forecast of at least 2 points from its lowest "
               "positive level since the last bet (from 0 after a flat), the first bet per 5-bar grid cell from each "
               "window's first row is the case; the drift is the coin's mean 5-bar return on that grid over all its "
               "windows; the day-pooled t uses per-day sums of deviations from the mean (cluster SE with G/(G-1)); "
               "the median split puts cases above the median entry forecast in the upper half and the rest in the lower.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move of bets", "value": None, "statistic": None,
                             "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 distinct case days"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (mean_reversion regime with the close at its 30-bar low)."),
            "reading": reading,
        }

    # ---------------- 2. criterion ----------------
    cases = []  # (coin, date, ret, entry_fc)
    drift = {}
    for coin in sorted(bars):
        grid_rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            dates = _to_dates(df["timestamp"])
            n = len(df)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            ref = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND - 1e-12:
                    ref = f
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                        cases.append((coin, dates[t], close[t + H] / close[t] - 1.0, f))
                else:
                    ref = min(ref, f)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    rows = [(c, d, r - drift[c], f) for (c, d, r, f) in cases if np.isfinite(drift.get(c, np.nan))]
    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([r[2] for r in rows], dtype=float)
        mean_u = float(u.mean())
        if n_days >= 2:
            dev = pd.Series(u - mean_u, index=[r[1] for r in rows])
            S = dev.groupby(level=0).sum().values
            G = len(S)
            var = (G / (G - 1)) * np.sum(S ** 2) / (n_cases ** 2)
            se = float(np.sqrt(var))
            t_val = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        fcs = np.array([r[3] for r in rows], dtype=float)
        u = np.array([r[2] for r in rows], dtype=float)
        med = float(np.median(fcs))
        up = u[fcs > med]
        lo = u[fcs <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif mean_u is not None and t_val is not None and mean_u > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 over at least 30 case days and the upper-half minus lower-half difference is above 0."
    elif mean_u is not None and t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 case days."
    elif mean_u is not None and t_val is not None and mean_u > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "The mean unusual move is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean unusual 5-bar move of bets (return minus coin's 5-bar drift)",
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of the same day pooled", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": "confirm: positive with t >= 2; reject: negative with t <= -2; at least 30 distinct case days"},
        "supporting_check": {"name": "upper-half minus lower-half mean unusual move, split at median entry forecast",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"distinct case days": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
