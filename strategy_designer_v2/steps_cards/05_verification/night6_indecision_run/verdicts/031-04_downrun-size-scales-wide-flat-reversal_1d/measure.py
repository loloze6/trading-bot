import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    WIDE_MIN = 1.5
    BODY_MAX = 0.1
    LONG = 20
    FC_COL = "forecast"
    REGIME = "mean_reversion"

    # ---------- 1. Situation check (from prices only) ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            op = d["open"].astype(float)
            cl = d["close"].astype(float)
            rng = hi - lo
            mean_rng = rng.rolling(LONG, min_periods=LONG).mean()  # 20 bars ending today
            wide = rng / mean_rng
            body = (cl - op).abs() / rng.replace(0, np.nan)
            computable = wide.notna() & body.notna()
            situation = (wide >= WIDE_MIN - 1e-9) & (body <= BODY_MAX + 1e-9)
            fc = pd.to_numeric(d[FC_COL], errors="coerce")
            active = fc.notna() & (fc != 0) & computable
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active bars are wide (range >= 1.5x the 20-day mean range) "
                           "and flat (body <= 10% of range) days with a long forecast"
                           if n_active > 0 else "No active bars on which the situation could be checked"),
            "reading": "Bars whose 20-day mean range cannot be computed inside the window are left out of the check.",
        }

    # ---------- 2. Criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all windows (non-overlapping grid per window)
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            cl = d["close"].astype(float).values
            for i in range(0, len(cl) - H, H):
                if cl[i] > 0 and np.isfinite(cl[i]) and np.isfinite(cl[i + H]):
                    grid_rets.append(cl[i + H] / cl[i] - 1.0)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        coin_mean = float(np.mean(grid_rets))

        for d in prepared:
            cl = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC_COL], errors="coerce").values
            reg = d["regime"].astype(str).values
            ts = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D").values
            n = len(d)
            last_kept = -10 ** 9
            for i in range(n):
                if reg[i] != REGIME:
                    continue
                if i + H >= n:
                    continue
                if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H]) and cl[i] > 0 and np.isfinite(fc[i])):
                    continue
                if i - last_kept <= H:  # inside the 5 bars after a kept case
                    continue
                last_kept = i
                xs.append(float(fc[i]))
                ys.append(float(cl[i + H] / cl[i] - 1.0 - coin_mean))
                days.append(ts[i])

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))
    strong = x >= 2
    n_strong = int(strong.sum())
    n_days = int(len(set(days))) if n_cases else 0

    slope = None
    t = None
    if n_cases >= 3:
        xm = x.mean()
        dx = x - xm
        sxx = float(np.sum(dx ** 2))
        if sxx > 0:
            slope = float(np.sum(dx * (y - y.mean())) / sxx)
            intercept = y.mean() - slope * xm
            e = y - intercept - slope * x
            sc = pd.Series(dx * e).groupby(pd.Index(days)).sum().values
            G = len(sc)
            if G > 1:
                var = (G / (G - 1)) * float(np.sum(sc ** 2)) / sxx ** 2
                if var > 0:
                    t = float(slope / np.sqrt(var))

    sup_val = float(np.mean(y[strong])) if n_strong > 0 else None
    sup_pass = bool(sup_val > 0) if sup_val is not None else None

    counts = {"independent cases": n_cases, "cases with forecast >= 2": n_strong, "days with cases": n_days}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, below the plan's minimum of 30."
    elif n_strong < 10:
        status = "not observable"
        decided = f"Only {n_strong} cases with forecast >= 2, below the plan's minimum of 10."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation in the forecast); any other result is inconclusive."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the cases with forecast >= 2 have a positive mean excess return."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        if slope > 0 and t >= 2:
            decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
        else:
            decided = "The slope's |t| is below 2 (or its sign disagrees with t), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "slope of 5-bar forward excess return on forecast, mean_reversion bars",
            "value": slope,
            "statistic": {"name": "slope t, residual scores summed per day", "value": t} if t is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean 5-bar excess return of cases with forecast >= 2 above 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are mean_reversion bars with a 5-bar forward return inside their window, kept greedily so that "
                    "a case 1 to 5 bars after a kept case is dropped; the coin's mean 5-bar return is taken on the "
                    "non-overlapping grid (positions 0, 5, 10, ...) of all its windows; the day-summed t uses "
                    "the OLS residual scores clustered by UTC day with a G/(G-1) correction; the plan's minimum counts "
                    "give 'not observable' when not reached."),
    }
