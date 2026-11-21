import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    RAW = "debug_info.components.clearance.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback from prices: close above the highest close of the prior 20 bars
            prior_high = close.shift(1).rolling(20, min_periods=20).max()
            price_sit = close > prior_high
            price_ok = prior_high.notna()
            for i in range(len(df)):
                f = fc.iloc[i]
                if pd.isna(f) or f == 0:
                    continue
                n_active += 1
                r = raw.iloc[i]
                if pd.notna(r):
                    sit = r > 0
                elif price_ok.iloc[i]:
                    sit = bool(price_sit.iloc[i])
                else:
                    sit = False
                if sit and f > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "pooled OLS slope of 10-bar excess return on signal-bar forecast"
    threshold = "slope t >= 2 with mean excess > 0 confirms; slope t <= -2 rejects; at least 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars with the close above its prior 20-day high (raw clearance > 0), so the config does not do what the Fidelity's situation and long side say.",
            "reading": "The situation is raw clearance > 0 (or, where unrecorded, close above the prior 20 closes' max) and the expected side is long.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's normal 10-bar drift: non-overlapping grid of all its windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(c)
            # reconstruct bets: a rise of the long forecast of >= BAND from its lowest level since the last bet
            bets = np.zeros(n, dtype=bool)
            base = 0.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND:
                    bets[i] = True
                    base = f
                else:
                    base = min(base, f)
            # one case per 10-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bets[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                ret = c[t + H] / c[t] - 1.0
                xs.append(float(fc[t]))
                ys.append(ret - drift)

    n_cases = len(xs)
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    mean_excess = float(np.mean(ys)) if n_cases > 0 else None
    sup_passed = (mean_excess > 0) if mean_excess is not None else None

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled over all coins and windows, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the signal-bar forecast), so it meets neither the confirm nor the reject rule."
    elif t_slope >= 2 and mean_excess > 0:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return of the cases is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger clearances are followed by smaller excess rises."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess return is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return over all cases above 0",
            "value": mean_excess,
            "passed": bool(sup_passed) if sup_passed is not None else None,
        },
        "counts": {"cases": int(n_cases)},
        "decided_by": decided,
        "reading": "A case is the first bar in each 10-bar grid cell (counted from each window's first row) where the long forecast rises at least 2 points above its lowest level since the last such rise (reset to 0 when flat, starting from 0 at each window's start), cases whose 10-bar return would leave the window are dropped, the drift is the coin's mean return on the non-overlapping 10-bar grid of all its windows, and the plan's fewer-than-100-cases rule is reported as not observable.",
    }
