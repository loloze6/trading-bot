import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    P = 30
    FCOL = "forecast"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            fc = df[FCOL].astype(float)
            hh = high.rolling(P, min_periods=P).max()
            ll = low.rolling(P, min_periods=P).min()
            rng = hh - ll
            net = (close - close.shift(P - 1)).abs()
            ratio = net / rng.replace(0, np.nan)
            mid = (hh + ll) / 2.0
            dist = (close - mid) / mid * 100.0
            computable = ratio.notna() & dist.notna()
            sit_calc = (ratio <= 0.3) & (dist < 0.0)
            # where the 30-bar history is not inside the window, fall back on the recorded regime
            sit_reg = df["regime"].astype(str) == "mean_reversion" if "regime" in df.columns else pd.Series(False, index=df.index)
            sit = np.where(computable, sit_calc, sit_reg)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit, index=df.index).astype(bool) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Net move is |close[t] - close[t-29]| over the 30-bar high-low range and the middle is (30-bar high + low)/2 "
               "(all Ichimoku spans coincide at period 30), with the recorded regime used on the first 29 bars of a window "
               "where the 30-bar history is not recorded; the coin's mean 5-bar return is the mean over its grid returns "
               "of all windows; the slope's t is from one OLS regression pooling all coins' cases; and the plan's "
               "'fewer than 30 grid cases' minimum is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 30-bar net-move/range "
                           "ratio is 0.3 or less and the close is below the 30-bar range middle."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df[FCOL].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    cases.append((fc[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for f, r in cases:
            xs.append(float(f))
            ys.append(r - drift)

    n_cases = len(xs)
    counts = {"grid cases with forecast > 0": n_cases}
    mean_excess = float(np.mean(ys)) if n_cases > 0 else None

    slope = None
    t = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_passed = (mean_excess > 0) if mean_excess is not None else None

    main = {
        "name": "pooled OLS slope of drift-removed next-5-bar return on forecast (grid bars with forecast > 0)",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
        "threshold": "confirm if t >= 2 with positive mean drift-removed return; reject if t <= -2",
    }
    sup = {"name": "mean drift-removed 5-bar return over the cases > 0",
           "value": mean_excess, "passed": sup_passed}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean drift-removed 5-bar return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean drift-removed return fails the check (not above 0)."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
