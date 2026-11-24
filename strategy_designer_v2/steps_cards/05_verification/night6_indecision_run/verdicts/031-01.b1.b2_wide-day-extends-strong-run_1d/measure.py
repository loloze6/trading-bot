import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    MIN_DAYS = 30
    COMP = "debug_info.components.rise_range.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            comp = (pd.to_numeric(df[COMP], errors="coerce").values
                    if COMP in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                rise = np.nan
                if i >= 5 and np.isfinite(close[i]) and np.isfinite(close[i - 5]) and close[i - 5] != 0:
                    rise = close[i] / close[i - 5] - 1.0
                if np.isfinite(rise):
                    situ = rise > 0
                elif np.isfinite(comp[i]):
                    # first bars of a window: the 5-bar rise lies before the record;
                    # the component's raw value (rise % x range multiple) carries its sign
                    situ = comp[i] > 0
                else:
                    situ = False
                if situ and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 3-bar move of long cases (forecast rises >= 2 points, one per 3-bar cell)"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and upper-minus-lower half > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation = 5-bar close return > 0 recomputed from prices inside each window (component raw value > 0 "
               "on a window's first 5 bars), side long; a case is the first bar in each 3-bar grid cell (from each "
               "window's first row) where the positive forecast has risen >= 2 points above its lowest level since the "
               "last bet (from 0 after flat); drift is the coin's mean 3-bar return on the same grid over all its windows; "
               "t sums case deviations per UTC day; the median split puts cases with forecast above the median in the "
               "upper half and the rest in the lower half; fewer than 30 case days gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive 5-bar "
                           "return, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, forecast)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = _ts(df)
            n = len(df)
            # grid returns for drift
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            # bets (long side)
            ref = 0.0
            prev = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                else:
                    if prev <= 0:
                        ref = 0.0
                    if f - ref >= BAND:
                        bet[i] = True
                        ref = f
                    else:
                        ref = min(ref, f)
                prev = f
            # one case per grid cell
            for c0 in range(0, n, H):
                for i in range(c0, min(c0 + H, n)):
                    if bet[i]:
                        if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                            r = close[i + H] / close[i] - 1.0
                            day = ts.iloc[i].strftime("%Y-%m-%d") if pd.notna(ts.iloc[i]) else f"{w}_{i}"
                            coin_cases.append((coin, day, r, float(fc[i])))
                        break
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for c in coin_cases:
            if np.isfinite(drift[coin]):
                cases.append((c[0], c[1], c[2] - drift[coin], c[3]))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"distinct case days": int(n_days), "cases": int(n_cases)}

    mean_u = None
    t_val = None
    if n_cases > 0:
        x = np.array([c[2] for c in cases])
        mean_u = float(x.mean())
        dev = pd.Series(x - mean_u).groupby([c[1] for c in cases]).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    diff = None
    if n_cases >= 2:
        f = np.array([c[3] for c in cases])
        x = np.array([c[2] for c in cases])
        med = np.median(f)
        up = x[f > med]
        lo = x[f <= med]
        if len(up) > 0 and len(lo) > 0:
            diff = float(up.mean() - lo.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the 30 the plan requires."
    elif mean_u is not None and t_val is not None and mean_u > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and upper-minus-lower half difference above 0."
    elif mean_u is not None and t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        if t_val is not None and mean_u is not None and mean_u > 0 and t_val >= 2:
            decided = "Positive mean with t >= 2 but the upper-minus-lower half difference is 0 or below (or not computable)."
        else:
            decided = "The t lies between -2 and 2 (or is not computable): neither confirm nor reject is met."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together",
                                                       "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": "upper-half minus lower-half mean unusual move (split at median forecast)",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
