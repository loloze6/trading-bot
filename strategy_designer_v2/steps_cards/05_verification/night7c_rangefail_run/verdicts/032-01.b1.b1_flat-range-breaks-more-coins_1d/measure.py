import numpy as np
import pandas as pd


def measure(bars):
    H = 20          # plan horizon, in bars
    N = 60          # efficiency-ratio and breakout lookback
    ER_MAX = 0.3
    BAND = 2.0      # default min_allocation_change, in forecast points
    EPS = 1e-12

    # ---------- 1. situation check ----------
    n_active = 0
    n_active_computable = 0
    n_agree = 0
    n_active_regime_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            fc = d["forecast"].astype(float)
            direction = (close - close.shift(N)).abs()
            vol = close.diff().abs().rolling(N, min_periods=N).sum()
            er = direction / vol.replace(0.0, np.nan)
            prior_high = high.shift(1).rolling(N, min_periods=N).max()
            computable = er.notna() & prior_high.notna()
            situation = (er <= ER_MAX + 1e-9) & (close > prior_high)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ac = active & computable
            n_active_computable += int(ac.sum())
            n_agree += int((ac & situation & (fc > 0)).sum())
            if "regime" in d.columns:
                n_active_regime_ok += int((active & (d["regime"] == "mean_reversion") & (fc > 0)).sum())

    if n_active_computable > 0:
        agreement = n_agree / n_active_computable
        sit_reading = ("the situation is recomputed from each window's own prices (60-bar efficiency ratio of closes "
                       "<= 0.3 and close above the highest high of the 60 prior bars), active bars without 60 prior "
                       "bars in their window are left out")
    elif n_active > 0:
        agreement = n_active_regime_ok / n_active
        sit_reading = ("no active bar had 60 prior bars in its window, so the situation is read from the recorded "
                       "regime (mean_reversion) with a positive forecast")
    else:
        agreement = None
        sit_reading = "no active bar in the record"
    passed_sit = agreement is not None and agreement >= 0.9

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checked": int(n_active_computable)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are long bars where the 60-bar "
                           "efficiency ratio is at or below 0.3 and the close is above the prior 60-bar high"),
            "reading": sit_reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, unusual move, forecast)
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            # normal drift: non-overlapping grid returns
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            # long bets
            bets = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND - EPS:
                    bets[i] = True
                    low = f
                else:
                    low = min(low, f)
            # once per grid cell: the first bet of each cell
            for c0 in range(0, n, H):
                idx = np.where(bets[c0:min(c0 + H, n)])[0]
                if len(idx) == 0:
                    continue
                i = c0 + int(idx[0])
                if i + H >= n:
                    continue
                if not (close[i] > 0 and np.isfinite(close[i + H])):
                    continue
                r = close[i + H] / close[i] - 1.0
                coin_cases.append((ts.iloc[i].floor("D"), r, fc[i]))
        if len(coin_cases) == 0:
            continue
        drift = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan
        if not np.isfinite(drift):
            continue
        for day, r, f in coin_cases:
            cases.append((coin, day, r - drift, f))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([c[2] for c in cases], dtype=float)
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u, index=[c[1] for c in cases])
        per_day = dev.groupby(level=0).sum().values
        G = len(per_day)
        if G > 1:
            var_mean = (G / (G - 1.0)) * float(np.sum(per_day ** 2)) / (n_cases ** 2)
            if var_mean > 0:
                t_val = float(mean_u / np.sqrt(var_mean))

    supp_val = None
    supp_pass = None
    if n_cases > 0:
        f_arr = np.array([c[3] for c in cases], dtype=float)
        u = np.array([c[2] for c in cases], dtype=float)
        med = float(np.median(f_arr))
        above = u[f_arr > med]
        below = u[f_arr < med]
        if len(above) > 0 and len(below) > 0:
            supp_val = float(above.mean() - below.mean())
            supp_pass = bool(supp_val > 0)

    main = {
        "name": "mean unusual 20-bar move after long bets, in the long direction",
        "value": mean_u,
        "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together",
                                                 "value": t_val},
        "threshold": "confirm: mean > 0 with t >= 2 and the supporting check passing; reject: mean < 0 with t <= -2",
    }
    supporting = {"name": "above-median minus below-median forecast mean unusual move > 0",
                  "value": supp_val, "passed": supp_pass}

    reading = (sit_reading + "; a case is the first long bet (a forecast rise of at least 2 points from its low "
               "since the last bet, from 0 after a flat) in each 20-bar grid cell counted from each window's first "
               "row, with its 20-bar return inside the window; the day-clustered t uses the G/(G-1) correction; "
               "cases exactly at the median forecast are left out of the supporting check.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"the plan's minimum counts are not reached ({n_cases} cases against 30, "
                   f"{n_days} distinct days against 20)")
    elif t_val is None:
        status = "inconclusive"
        decided = "the t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met"
    elif mean_u > 0 and t_val >= 2 and supp_pass is True:
        status = "confirmed"
        decided = "the mean unusual move is above 0 with t >= 2 and the supporting check passes"
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "the mean unusual move is below 0 with t <= -2"
    elif mean_u > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails"
    else:
        status = "inconclusive"
        decided = "the t of the mean unusual move is between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
