import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    EPS = 1e-9
    RAW = "debug_info.components.scaled_rise.last_history_value"

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            unit = "ms" if v.dropna().abs().median() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            r1 = close.pct_change()
            recomputed = r1 / r1.rolling(30, min_periods=30).std(ddof=1)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                rise = raw.where(raw.notna(), recomputed)
            else:
                rise = recomputed
            active = fc != 0
            in_sit = (rise >= 0.0 - EPS) & (rise <= 1.0 + EPS)
            agree = active & in_sit & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean unusual 3-bar move of short bets, in the short direction"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move of larger-forecast half minus smaller half"
    reading = ("The falling-agitated profile cannot be rebuilt from the record (its detector components are not "
               "recorded and windows are shorter than its 365-bar lookback), so the situation check tests the "
               "0-to-1.0 scaled-rise band (recorded raw value, else recomputed with a 30-bar std including the day) "
               "and the short side; a case is the first short bet (forecast magnitude up >= 2 points from its lowest "
               "level since the last bet) in each 3-bar grid cell of a window; the drift is the mean of each coin's "
               "non-overlapping 3-bar grid returns over all its windows; the clustered standard error uses day sums "
               "of deviations with a G/(G-1) correction; the larger half is forecast size above the median; fewer "
               "than 30 case days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "distinct case days": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a day's return "
                           "between 0 and 1.0 thirty-day standard deviations, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, size)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w in sorted(wins.keys(), key=lambda x: str(x)):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = to_time(df["timestamp"])
            n = len(df)
            for t in range(0, n - H, H):
                if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] != 0:
                    grid_rets.append(close[t + H] / close[t] - 1.0)
            # bets on the short side
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f < 0:
                    m = -f
                    if m - ref >= BAND - EPS:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H])) or close[t] == 0:
                    continue
                r = close[t + H] / close[t] - 1.0
                day = ts.iloc[t]
                day = str(day.date()) if pd.notna(day) else f"{w}-{t}"
                cases.append((coin, day, r, abs(fc[t])))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    rows = []
    for coin, day, r, size in cases:
        d = drift.get(coin, np.nan)
        if np.isfinite(d):
            rows.append((day, -(r - d), size))
    n_cases = len(rows)
    days = sorted(set(x[0] for x in rows))
    n_days = len(days)

    mean_u = None
    t_stat = None
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        u = np.array([x[1] for x in rows], dtype=float)
        sizes = np.array([x[2] for x in rows], dtype=float)
        dlab = np.array([x[0] for x in rows])
        mean_u = float(u.mean())
        dev = u - mean_u
        sums = pd.Series(dev).groupby(dlab).sum().values
        G = len(sums)
        if G > 1:
            var = (G / (G - 1.0)) * float(np.sum(sums ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t_stat = float(mean_u / se) if se > 0 else None
        med = float(np.median(sizes))
        big = u[sizes > med]
        small = u[sizes <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n_cases, "distinct case days": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days ({n_days}), the plan's minimum count."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("The mean unusual move is above 0 with t >= 2 and the larger-forecast half shows a larger "
                       "unusual move than the smaller half.")
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2) whose supporting check fails is inconclusive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2: the coin rises further after these rises."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t clustered by day", "value": t_stat} if t_stat is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
