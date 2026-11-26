import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    MIN_CASES = 30
    EPS = 1e-9
    COL_FLAT = "debug_info.components.flatness.last_history_value"
    COL_RUN = "debug_info.components.run_up.last_history_value"

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    def wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return str(w)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_undetermined = 0

    # ---------- 2. drift and cases ----------
    drift = {}
    cases = []  # (coin, day, forecast, ret)

    for coin in sorted(bars.keys()):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin].keys(), key=wkey):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            o = pd.to_numeric(df["open"], errors="coerce").values.astype(float)
            h = pd.to_numeric(df["high"], errors="coerce").values.astype(float)
            l = pd.to_numeric(df["low"], errors="coerce").values.astype(float)
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            ts = to_time(df["timestamp"])
            n = len(df)

            # situation from prices, preferring recorded raw component values
            rng = h - l
            with np.errstate(divide="ignore", invalid="ignore"):
                flat_p = np.where(rng > 0, 1.0 - np.abs(c - o) / rng, np.nan)
            rise_p = pd.Series(c).pct_change(5).values
            mean_rng = pd.Series(rng).rolling(20, min_periods=20).mean().values
            with np.errstate(divide="ignore", invalid="ignore"):
                wide = np.where(mean_rng > 0, rng / mean_rng, np.nan)
            flat = flat_p.copy()
            rise = rise_p.copy()
            if COL_FLAT in df.columns:
                rf = pd.to_numeric(df[COL_FLAT], errors="coerce").values.astype(float)
                flat = np.where(np.isfinite(rf), rf, flat)
            if COL_RUN in df.columns:
                rr = pd.to_numeric(df[COL_RUN], errors="coerce").values.astype(float)
                rise = np.where(np.isfinite(rr), rr, rise)

            for i in range(n):
                if f[i] == 0:
                    continue
                if not (np.isfinite(flat[i]) and np.isfinite(rise[i]) and np.isfinite(wide[i])):
                    n_active_undetermined += 1
                    continue
                n_active += 1
                sit = (rise[i] > 0) and (wide[i] >= 1.5 - EPS) and (flat[i] >= 0.5 - EPS)
                if sit and f[i] > 0:
                    n_agree += 1

            # non-overlapping grid returns for the coin's normal drift
            for p in range(0, n - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)

            # bets: rise of the forecast on its side of at least the band
            bet = np.zeros(n, dtype=bool)
            side = 0
            ref = 0.0
            for i in range(n):
                s = int(np.sign(f[i]))
                a = abs(f[i])
                if s != side:
                    side = s
                    ref = 0.0
                if side == 0:
                    continue
                if a - ref >= BAND - EPS:
                    bet[i] = True
                    ref = a
                else:
                    ref = min(ref, a)

            # one case per grid cell: the first bet in the cell
            for p in range(0, n, H):
                idx = [i for i in range(p, min(p + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] <= 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                day = ts.iloc[t].strftime("%Y-%m-%d") if pd.notna(ts.iloc[t]) else f"{coin}{w}{t}"
                coin_cases.append((coin, day, f[t], float(np.sign(f[t])), r))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for (cn, day, fc, sd, r) in coin_cases:
            if np.isfinite(drift[cn]):
                cases.append((cn, day, fc, sd * (r - drift[cn])))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation is rebuilt per window from the recorded raw flatness and run_up where present and "
               "otherwise from prices, with 'wide' as the day's range over the mean range of the last 20 bars "
               "including it, active bars whose 20-bar range history is incomplete being left out of the agreement; "
               "a case is the first bet (forecast rise of >= 2 points from its lowest level on its side since the last "
               "bet) in each cell of the per-window 3-bar grid, its unusual move is its 3-bar return minus the coin's "
               "mean 3-bar return on the pooled grid of all its windows, the t is clustered by UTC day, the median "
               "split drops cases equal to the median, and the minimum is 30 cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree,
                       "active bars undetermined": n_active_undetermined},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on which the 5-day rise "
                           "is above 0, the range is at least 1.5 times its 20-day mean and flatness is at least 0.5."
                           if agreement is not None else
                           "No active bar could be checked against the plan's situation."),
            "reading": reading,
        }

    u = np.array([x[3] for x in cases], dtype=float)
    fc = np.array([x[2] for x in cases], dtype=float)
    days = [x[1] for x in cases]
    n_cases = len(u)
    n_days = len(set(days))

    mean_u = float(np.mean(u)) if n_cases else None
    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        dev = u - mean_u
        sums = pd.Series(dev).groupby(pd.Series(days)).sum().values
        G = len(sums)
        var = (G / (G - 1.0)) * np.sum(sums ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_stat = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        med = np.median(fc)
        above = u[fc > med]
        below = u[fc < med]
        if len(above) > 0 and len(below) > 0:
            sup_val = float(np.mean(above) - np.mean(below))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases (on {n_days} days), under the plan's minimum of 30 cases."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 over at least 30 cases, and the supporting check passes."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 over at least 30 cases."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "A confirm-level t whose supporting check (above-median minus below-median unusual move > 0) fails."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 3-bar unusual move of long bets (return minus coin's normal 3-bar drift), before costs",
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day taken together",
                          "value": t_stat} if t_stat is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases and supporting check passes; "
                         "reject: mean < 0 with t <= -2 over at least 30 cases",
        },
        "supporting_check": {
            "name": "mean unusual move above minus below the median case forecast > 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "distinct days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
