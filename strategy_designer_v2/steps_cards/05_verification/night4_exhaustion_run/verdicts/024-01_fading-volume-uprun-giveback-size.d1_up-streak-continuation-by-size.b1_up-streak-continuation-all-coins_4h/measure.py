import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 100
    RAW = "debug_info.components.up_streak.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(len(df), np.nan)
            prev = np.concatenate([[np.nan], close[:-1]])
            up_bar = close > prev  # False on first row (prev NaN)
            raw_pos = raw > 0      # NaN -> False
            # streak running through bar t: the bar closed up (the raw gain, where recorded, is positive)
            has_prev = ~np.isnan(prev)
            has_raw = ~np.isnan(raw)
            situ = np.where(has_prev, up_bar & np.where(has_raw, raw_pos, True), raw_pos)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 18-bar move per case (long), all coins pooled"
    threshold = "confirm t >= 2 with top-minus-bottom > 0; reject t <= -2; at least 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": n_active},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are long bars of a running up-streak "
                          "(bar closed up, positive streak gain), as the plan's situation requires",
            "reading": "situation taken as the bar closing above the previous close with a positive raw streak gain, side long",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 18-bar returns on each window's grid, all windows together
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df.sort_values("timestamp")["close"].astype(float).values
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    vals = []
    sizes = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0 or not np.isfinite(drift.get(coin, np.nan)):
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(df)
            # bets: rise of the long forecast of >= BAND from its lowest level since the last bet
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            # one case per 18-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                vals.append((b / a - 1.0) - drift[coin])
                sizes.append(fc[t])

    vals = np.array(vals, dtype=float)
    sizes = np.array(sizes, dtype=float)
    n_cases = int(len(vals))

    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t_val = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    n_top = n_bot = 0
    if n_cases >= 2:
        order = np.argsort(sizes, kind="mergesort")
        half = n_cases // 2
        bot = vals[order[:half]]
        top = vals[order[n_cases - half:]]
        n_top, n_bot = len(top), len(bot)
        diff = float(np.mean(top) - np.mean(bot))

    sup_passed = None if diff is None else bool(diff > 0)
    reading = ("cases are the first bet (long forecast rise >= 2 points from its low since the last bet) in each "
               "18-bar grid cell from each window's first row, with the return dropped if t+18 leaves the window; "
               "top/bottom halves are the upper and lower n//2 cases by forecast at the signal bar (middle case "
               "dropped when n is odd); fewer than 100 cases is reported as not observable.")

    if n_cases < MIN_CASES or t_val is None:
        status = "not observable"
        decided = f"only {n_cases} cases, below the plan's minimum of 100 cases"
    elif t_val >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "the mean unusual move has t >= 2 and the top-half minus bottom-half difference is above 0"
    elif t_val <= -2:
        status = "rejected"
        decided = "the mean unusual move has t <= -2: up-runs are followed by a give-back larger than the drift"
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-half minus bottom-half difference is at or below 0"
    else:
        status = "inconclusive"
        decided = "the t of the mean unusual move lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top-half minus bottom-half mean unusual move by forecast size",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {"cases": n_cases, "top_half_cases": int(n_top), "bottom_half_cases": int(n_bot)},
        "decided_by": decided,
        "reading": reading,
    }
