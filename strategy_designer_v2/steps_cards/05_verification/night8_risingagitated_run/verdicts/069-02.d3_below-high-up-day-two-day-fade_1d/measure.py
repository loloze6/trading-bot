import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    BAND = 2.0
    DEPTH_COL = "debug_info.components.depth.last_history_value"

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            dt = pd.to_datetime(v, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.floor("D").dt.strftime("%Y-%m-%d").values

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float).values
            high = df["high"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            prev = np.r_[np.nan, close[:-1]]
            up = close > prev  # first bar of a window: prev is NaN -> not computable
            if DEPTH_COL in df.columns:
                raw = df[DEPTH_COL].astype(float).values
            else:
                raw = np.full(len(df), np.nan)
            rollmax = pd.Series(high).rolling(20, min_periods=20).max().values
            below_prices = close < rollmax
            below = np.where(np.isnan(raw), below_prices, raw < 0)
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                if i == 0:
                    continue  # up-day cannot be computed from the record on a window's first bar
                n_active += 1
                if up[i] and below[i] and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Up day = close above the previous close inside the window, with window-first bars "
               "left out of the situation check; depth below the high = raw depth < 0 (else close below "
               "the 20-bar max high); a bet is a short-side rise in |forecast| of >= 2 points from its lowest "
               "level since the last bet (reset at flat or side change); one case per 2-bar grid cell (the "
               "first bet in the cell), return from that bet's close; drift = mean of the coin's "
               "non-overlapping 2-bar grid returns over all windows; day-clustered t with D/(D-1) correction; "
               "the plan's minimum counts lead to 'not observable' when not reached.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean short-direction excess 2-bar return of the cases",
                             "value": None, "statistic": None,
                             "threshold": "above 0 with t >= 2 (confirm); below 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short forecasts on up days closing below "
                           "the 20-day high, the situation and side the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- cases ----------
    vals, absf, days = [], [], []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            dd = to_days(df["timestamp"])
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1
                if np.isfinite(r):
                    grid_rets.append(r)
            # bets
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                f = fc[i]
                if f < 0:
                    m = -f
                    if not prev_short:
                        ref = 0.0
                    if m - ref >= BAND:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
            for c0 in range(0, n, H):
                idx = [j for j in range(c0, min(c0 + H, n)) if bet[j]]
                if not idx:
                    continue
                j = idx[0]
                if j + H >= n:
                    continue
                r = close[j + H] / close[j] - 1
                if not np.isfinite(r):
                    continue
                coin_cases.append((r, abs(fc[j]), dd[j]))
        if not coin_cases:
            continue
        drift = float(np.mean(grid_rets)) if grid_rets else 0.0
        for r, a, d in coin_cases:
            vals.append(-(r - drift))
            absf.append(a)
            days.append(d)

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = float(np.mean(vals)) if n_cases > 0 else None
    tval = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(vals - mean)
        S = dev.groupby(pd.Series(days)).sum().values
        D = len(S)
        se = np.sqrt(np.sum(S ** 2) * D / (D - 1)) / n_cases
        tval = float(mean / se) if se > 0 else None
    slope = None
    if n_cases > 2 and np.var(absf) > 0:
        slope = float(np.polyfit(absf, vals, 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    main = {"name": "mean short-direction excess 2-bar return of the cases",
            "value": mean,
            "statistic": None if tval is None else {"name": "t of the mean, cases of one day taken together",
                                                    "value": tval},
            "threshold": "above 0 with t >= 2 (confirm); below 0 with t <= -2 (reject)"}
    support = {"name": "slope of short excess return on |forecast|", "value": slope, "passed": slope_pass}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = ("The plan's minimum of 100 cases on 60 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean short-direction excess 2-bar return is above 0 with t >= 2 and the slope is positive."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean short-direction excess 2-bar return is below 0 with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on |forecast| is not positive, so the plan calls it inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, so the plan calls it inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
