import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    FC = "forecast"
    LHV = "debug_info.components.mom20.last_history_value"

    # ---------- 1. Situation check ----------
    # Adapted situation: the 20-day return as a graded size. Long when it is positive, short when negative.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            lhv = (pd.to_numeric(df[LHV], errors="coerce").values
                   if LHV in df.columns else np.full(len(df), np.nan))
            n = len(df)
            past = np.full(n, np.nan)
            if n > H:
                past[H:] = close[H:] / close[:-H] - 1.0
            # Where the window does not hold 20 prior closes, use the component's raw value.
            sit = np.where(np.isfinite(past), past, lhv)
            for i in range(n):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(sit[i]) and sit[i] != 0 and np.sign(sit[i]) == np.sign(fc[i]):
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t-statistic of slope of forward 20-bar excess return on forecast (non-overlapping, pooled)"
    thr = "confirm if t >= 2 and top-minus-bottom > 0; reject if t <= -2; otherwise inconclusive"
    sup_name = "mean forward 20-bar excess return, top fifth minus bottom fifth of forecasts"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The forecast's sign does not follow the sign of the past 20-bar return "
                           "on at least 90% of active bars, as the Fidelity's graded situation requires."),
            "reading": "Past 20-bar return taken from closes inside the window, falling back to the component's raw value where the window holds fewer than 20 prior bars.",
        }

    # ---------- 2. Criterion ----------
    # Mean forward 20-bar return of each coin, over all bars of all its windows together.
    coin_mean = {}
    per_window = {}
    for coin, wins in bars.items():
        allf = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0
            per_window[(coin, w)] = (fwd, fc)
            allf.append(fwd[np.isfinite(fwd)])
        allf = np.concatenate(allf) if allf else np.array([])
        coin_mean[coin] = float(np.mean(allf)) if allf.size else np.nan

    # Sample only the bars at positions 0, 20, 40, ... of each window.
    xs, ys = [], []
    for (coin, w), (fwd, fc) in per_window.items():
        for i in range(0, len(fwd), H):
            if np.isfinite(fwd[i]) and np.isfinite(fc[i]) and np.isfinite(coin_mean[coin]):
                xs.append(fc[i])
                ys.append(fwd[i] - coin_mean[coin])
    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    tstat = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    diff = None
    if n_cases >= 5:
        q80 = np.quantile(x, 0.8)
        q20 = np.quantile(x, 0.2)
        top = y[x >= q80]
        bot = y[x <= q20]
        if top.size and bot.size:
            diff = float(np.mean(top) - np.mean(bot))

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping 20-bar cases, fewer than the plan's minimum of 300."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t-statistic could not be computed."
    elif tstat >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "The slope t-statistic is 2 or more and the top-minus-bottom difference is positive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope t-statistic is -2 or less."
    else:
        status = "inconclusive"
        if tstat >= 2:
            decided = "The slope t-statistic is 2 or more, but the top-minus-bottom difference is not positive, so the confirm rule is not met."
        else:
            decided = "The slope t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": tstat,
            "statistic": ({"name": "OLS slope t", "value": tstat} if tstat is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": diff,
            "passed": (bool(diff > 0) if diff is not None else None),
        },
        "counts": {"non-overlapping 20-bar cases": n_cases},
        "decided_by": decided,
        "reading": ("Each coin's mean 20-bar return is taken over all bars of all its windows that have a forward return. "
                    "The regression and the top/bottom fifths (cut at the 80th and 20th percentiles of forecasts) both use the same "
                    "pooled non-overlapping sample at positions 0, 20, 40, ... of each window, and too few cases is reported as not observable."),
    }
