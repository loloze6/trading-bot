import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    DEPTH = "debug_info.components.depth.last_history_value"
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            ret30 = close / close.shift(30) - 1.0  # inside the window only
            # where the 30-bar return cannot be recomputed in the window, fall back on the detector's decision
            neg_month = np.where(ret30.notna(), ret30 < 0,
                                 d["regime"].astype(str) == "mean_reversion")
            if DEPTH in d.columns:
                depth = pd.to_numeric(d[DEPTH], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=d.index)
            below_high = (depth < 0).fillna(False).values
            situation = np.asarray(neg_month, dtype=bool) & below_high
            active = (fc.fillna(0) != 0).values
            long_side = (fc > 0).fillna(False).values
            n_active += int(active.sum())
            n_agree += int((active & situation & long_side).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of 7-bar forward excess return on forecast, regime grid bars"
    threshold = "t >= 2 confirms (with supporting check), t <= -2 rejects, else inconclusive; at least 100 regime grid cases"
    reading = ("30-bar return recomputed from closes inside each window (detector's regime used where fewer than 30 prior bars exist); "
               "situation = that return < 0 and depth < 0, side long; grid = positions 0,7,14,... of each window with t+7 in the window; "
               "coin mean 7-bar return = mean over that coin's grid bars in all windows; top third = regime grid bars with forecast >= its 2/3 quantile.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with a negative 30-bar return "
                           "and a close below the 60-bar high, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                if reg[i] == "mean_reversion" and np.isfinite(fc[i]):
                    rows.append((coin, fc[i], r))
        coin_grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    fcs = np.array([r[1] for r in rows], dtype=float)
    exc = np.array([r[2] - coin_grid_rets[r[0]] for r in rows], dtype=float)
    ok = np.isfinite(fcs) & np.isfinite(exc)
    fcs, exc = fcs[ok], exc[ok]
    n_cases = int(len(fcs))

    slope, t = None, None
    if n_cases >= 3 and np.std(fcs) > 0:
        lr = stats.linregress(fcs, exc)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else (np.inf if lr.slope > 0 else -np.inf)

    top_mean, top_n, sup_pass = None, 0, None
    if n_cases > 0:
        q = np.quantile(fcs, 2.0 / 3.0)
        top = exc[fcs >= q]
        top_n = int(len(top))
        if top_n > 0:
            top_mean = float(np.mean(top))
            sup_pass = bool(top_mean > 0)

    counts = {"independent regime grid cases": n_cases, "top third cases": top_n}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent regime grid cases, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in forecast), so neither rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top third's mean excess return is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: deeper falls are followed by lower excess returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": float(t)} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean 7-bar excess return of top third by forecast > 0",
                             "value": top_mean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
