import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    PERIOD = 30
    NMR_MIN = 0.5
    MIN_CASES = 30
    RISE_COL = "debug_info.components.rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # NetMoveToRangeRatio(30, high_low), recomputed from prices
            net = (close - close.shift(PERIOD)).abs()
            rng = high.rolling(PERIOD + 1).max() - low.rolling(PERIOD + 1).min()
            nmr = net / rng.replace(0, np.nan)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            # where the price history is too short, the detector's own decision stands in
            trend_ok = np.where(nmr.notna(), nmr >= NMR_MIN, regime == "trending")

            # 30-day rise: recorded raw value, else recomputed from prices
            rise = pd.to_numeric(df[RISE_COL], errors="coerce") if RISE_COL in df.columns else pd.Series(np.nan, index=df.index)
            rise_px = close / close.shift(PERIOD) - 1
            rise = rise.where(rise.notna(), rise_px)
            rise_ok = (rise > 0).fillna(False).values

            active = (fc != 0).values
            situ = np.asarray(trend_ok, dtype=bool) & rise_ok & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "mean 10-bar excess return of rise-sized long bets over the coin's normal 10-bar drift"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation = recomputed NMR (|close[t]-close[t-30]| over the high-low range of bars t-30..t) >= 0.5 "
               "(regime column where history is short) with a positive 30-day rise, long side; a case is the first long bet "
               "(forecast rise >= 2 from its lowest level since the last bet, reset to 0 when flat) in each 10-bar grid cell "
               "counted from each window's first row; the drift is the coin's mean non-overlapping 10-bar return pooled over "
               "its windows; the median split uses cases strictly above and strictly below the median forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 30-day net move covers at least half the "
                           "30-day high-low range with a rise and a long forecast, as the plan's situation requires."
                           if n_active > 0 else "The record has no active bars to compare with the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess = []
    fcs = []
    for coin, wins in bars.items():
        # coin's normal 10-bar drift
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            ref = 0.0
            bets = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bets[i] = True
                    ref = f
                else:
                    ref = min(ref, f)
            for start in range(0, n, H):
                idx = np.where(bets[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                excess.append(c[t + H] / c[t] - 1 - drift)
                fcs.append(float(fc[t]))

    excess = np.asarray(excess, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        tval = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    if n_cases > 0:
        med = float(np.median(fcs))
        above = excess[fcs > med]
        below = excess[fcs < med]
        if len(above) > 0 and len(below) > 0:
            sup_val = float(np.mean(above) - np.mean(below))
    sup_passed = (sup_val > 0) if sup_val is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif tval is not None and mean_ex > 0 and tval >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "Mean excess return positive with t >= 2 over at least 30 cases and the supporting check above 0."
    elif tval is not None and mean_ex < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean excess return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        if tval is not None and tval >= 2:
            decided = "t >= 2 but the supporting check is not above 0, which the plan calls inconclusive."
        else:
            decided = "t between -2 and 2 (or undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess above median forecast minus below median",
            "value": sup_val,
            "passed": None if sup_passed is None else bool(sup_passed),
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
