import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_CASES = 60
    FC = "forecast"
    PP = "debug_info.components.width.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            high = df["high"].astype(float)
            close = df["close"].astype(float)
            prior_high = high.shift(1).rolling(20, min_periods=20).max()
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            active = fc != 0
            computable = prior_high.notna()
            mask = active & computable
            situation = close > prior_high
            n_active += int(mask.sum())
            n_agree += int((mask & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation recomputed as close above the highest high of the prior 20 rows within each window, "
               "active bars in a window's first 20 rows (no in-window history) left out of the agreement; "
               "breakout cases are regime 'trending' bars taken greedily (first, then next at least 10 bars later) "
               "per window, cases without a 10-bar forward return inside the window dropped; the coin's mean 10-bar "
               "return is taken on the non-overlapping grid (positions 0,10,20,...) of all its windows; thirds are "
               "the floor(n/3) lowest and highest forecasts; the plan's 'fewer than 60 cases' is reported as "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "t of slope of excess 10-bar return on width forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope t >= 2 confirms, <= -2 rejects"},
            "supporting_check": None,
            "counts": {"non-overlapping breakout cases": 0},
            "decided_by": (f"Only {agreement:.1%} of active bars are long bars with the close above the prior "
                           f"20-day high, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. coin mean 10-bar return (holding) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).to_numpy()
            for i in range(0, len(close) - H, H):
                if close[i] > 0 and np.isfinite(close[i]) and np.isfinite(close[i + H]):
                    rets.append(close[i + H] / close[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. breakout cases ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            pp = pd.to_numeric(df[PP], errors="coerce").to_numpy() if PP in df.columns \
                else np.full(len(df), np.nan)
            last = -10 ** 9
            for i in range(len(df)):
                if reg[i] != "trending":
                    continue
                if i - last < H:
                    continue
                last = i
                if i + H >= len(df):
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                if not np.isfinite(pp[i]) or not np.isfinite(coin_mean[coin]):
                    continue
                ret = close[i + H] / close[i] - 1.0
                xs.append(float(pp[i]))
                ys.append(ret - coin_mean[coin])
    x = np.array(xs)
    y = np.array(ys)
    n = int(len(x))
    counts = {"non-overlapping breakout cases": n}

    main_name = "t of slope of excess 10-bar return on width forecast"
    thr = "slope t >= 2 (with top-minus-bottom third > 0) confirms; slope t <= -2 rejects"

    if n < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n} non-overlapping breakout cases, fewer than the plan's minimum of 60.",
            "reading": reading,
        }

    slope_t = None
    slope = None
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    order = np.argsort(x, kind="mergesort")
    k = n // 3
    bot = y[order[:k]]
    top = y[order[n - k:]]
    diff = float(np.mean(top) - np.mean(bot)) if k > 0 else None
    welch = None
    if k >= 2:
        tt = stats.ttest_ind(top, bot, equal_var=False)
        welch = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = None if diff is None else bool(diff > 0)

    if slope_t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the forecast), so the result is inconclusive."
    elif slope_t >= 2 and sup_passed:
        status = "confirmed"
        decided = f"Slope t {slope_t:.2f} is 2 or more and the top-minus-bottom-third difference is positive."
    elif slope_t <= -2:
        status = "rejected"
        decided = f"Slope t {slope_t:.2f} is -2 or less."
    elif slope_t >= 2:
        status = "inconclusive"
        decided = (f"Slope t {slope_t:.2f} is 2 or more but the top-minus-bottom-third difference is "
                   f"at 0 or below, which the plan calls inconclusive.")
    else:
        status = "inconclusive"
        decided = f"Slope t {slope_t:.2f} lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope_t,
                         "statistic": {"name": "OLS slope t", "value": slope_t} if slope_t is not None else None,
                         "threshold": thr},
        "supporting_check": {"name": "top minus bottom third mean excess 10-bar return"
                                     + (f" (Welch t {welch:.2f})" if welch is not None else ""),
                             "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
