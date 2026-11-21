import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.ma_dist.last_history_value"

    def num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = num(df, "close")
            fc = np.nan_to_num(num(df, "forecast"), nan=0.0)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            raw = num(df, RAW)
            sma50 = pd.Series(close).rolling(50, min_periods=50).mean().to_numpy()
            for t in range(len(df)):
                if fc[t] == 0:
                    continue
                n_active += 1
                # close above SMA50: the recorded raw distance, else recomputed from in-window prices
                if np.isfinite(raw[t]):
                    above = raw[t] > 0
                elif np.isfinite(sma50[t]):
                    above = close[t] > sma50[t]
                else:
                    above = False
                # a fresh upward close-cross of a level needs the close to rise on that bar
                fresh_up = True if t == 0 else bool(close[t] > close[t - 1])
                # breakout and cluster conditions: the detector's recorded decision
                trending = regime[t] == "trending"
                if trending and above and fresh_up and fc[t] > 0:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-day move over long bet cases (5-day return minus coin's normal 5-day drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 independent cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("The breakout and swing-high cluster conditions are taken from the recorded regime 'trending', since the detector's "
               "components are not recorded. Close above SMA50 comes from the ma_dist raw value, or from the SMA50 of in-window "
               "closes where that value is missing. A fresh upward cross is checked as a close above the previous close. "
               "A case is the first long bet in each 5-bar grid cell counted from each window's first row. A bet is a rise of "
               ">= 2 points over the lowest positive forecast since the last bet, starting from 0 after a flat bar, on a trending bar. "
               "A case without 5 bars left in its window is dropped. The drift is the mean of non-overlapping 5-bar returns on the "
               "same grid over all of the coin's windows. The slope is the OLS slope of excess return on the case-bar forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent cases": None, "active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(trending breakout with close above SMA50); the plan needs at least 90%."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess_all = []
    fc_all = []
    for coin in bars:
        # coin's normal 5-day drift over all windows (non-overlapping grid)
        grid_rets = []
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = num(df, "close")
            for p in range(0, len(df) - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = num(df, "close")
            fc = np.nan_to_num(num(df, "forecast"), nan=0.0)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            base = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for t in range(len(df)):
                f = fc[t]
                if f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND:
                    if regime[t] == "trending":
                        bet[t] = True
                    base = f
                else:
                    base = min(base, f)
            for c0 in range(0, len(df), H):
                idx = [t for t in range(c0, min(c0 + H, len(df))) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= len(df):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1.0
                excess_all.append(r - drift)
                fc_all.append(fc[t])

    x = np.array(excess_all, dtype=float)
    f = np.array(fc_all, dtype=float)
    n = int(len(x))
    mean = float(np.mean(x)) if n > 0 else None
    tval = None
    if n >= 2:
        sd = float(np.std(x, ddof=1))
        tval = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n >= 3 and np.std(f) > 0:
        slope = float(stats.linregress(f, x).slope)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} independent cases, below the plan's minimum of 30."
        sup_passed = None if slope is None else bool(slope > 0)
    else:
        sup_passed = None if slope is None else bool(slope > 0)
        if tval is not None and mean > 0 and tval >= 2:
            if sup_passed:
                status = "confirmed"
                decided = "The mean unusual move is positive with t >= 2 over at least 30 cases, and the slope is above 0."
            else:
                status = "inconclusive"
                decided = "The t is confirming (>= 2) but the supporting slope is 0 or below (or not computable), so the result is inconclusive."
        elif tval is not None and mean < 0 and tval <= -2:
            status = "rejected"
            decided = "The mean unusual move is negative with t <= -2 over at least 30 cases."
        else:
            status = "inconclusive"
            decided = "The t lies between -2 and 2 (or could not be computed), so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if tval is None else {"name": "one-sample t", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of 5-day excess return on case forecast > 0",
                             "value": slope, "passed": sup_passed},
        "counts": {"independent cases": n},
        "decided_by": decided,
        "reading": reading,
    }
