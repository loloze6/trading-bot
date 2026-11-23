import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.failed_break_depth.last_history_value"
    H = 8
    BAND = 2.0
    PERIOD = 20
    FAIL_WINDOW = 3
    LAG = 2
    MIN_CASES = 30

    def price_failure(closes, t):
        # failure bar e = t - lag; breakout on one of e-3..e-1 above the prior 20 closes;
        # failure if close[e] is back below that old high
        e = t - LAG
        if e - FAIL_WINDOW - PERIOD < 0:
            return np.nan
        for j in range(e - 1, e - FAIL_WINDOW - 1, -1):
            old_high = np.max(closes[j - PERIOD:j])
            if closes[j] > old_high:
                return 1.0 if closes[e] < old_high else 0.0
        return 0.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            closes = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            for t in range(len(df)):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                r = raw[t]
                if np.isfinite(r):
                    situ = r != 0
                else:
                    pf = price_failure(closes, t)
                    situ = bool(pf == 1.0) if np.isfinite(pf) else False
                if situ and f < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean short-side unusual 8-bar move per case (before costs)"
    threshold = "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"
    sup_name = "mean unusual move of deeper half minus shallower half (split at median entry forecast size)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars with a non-zero "
                           "failed-breakout reading on the short side (agreement %.3f)." % agreement),
            "reading": ("Situation = non-zero last_history_value of failed_break_depth (recomputed from closes "
                        "where missing), expected side short (forecast < 0)."),
        }

    # ---------- 2. criterion ----------
    unusual = []
    sizes = []
    for coin, wins in bars.items():
        # normal drift: mean 8-bar return on non-overlapping grid over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(df)
            # short-side bets: rise of the short-side size of >= band from its lowest level since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                s = -fc[t] if fc[t] < 0 else 0.0
                if s == 0.0:
                    ref = 0.0
                    continue
                if s - ref >= BAND:
                    bet[t] = True
                    ref = s
                else:
                    ref = min(ref, s)
            # once per 8-bar grid cell: first bet in each cell
            for start in range(0, n, H):
                idx = np.where(bet[start:min(start + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                ret = c[t + H] / c[t] - 1.0
                unusual.append(-(ret - drift))
                sizes.append(abs(fc[t]))

    unusual = np.array(unusual, dtype=float)
    sizes = np.array(sizes, dtype=float)
    n_cases = int(len(unusual))

    mean = float(np.mean(unusual)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_deep = n_shallow = 0
    if n_cases > 0:
        med = float(np.median(sizes))
        deep = unusual[sizes > med]
        shallow = unusual[sizes <= med]
        n_deep, n_shallow = int(len(deep)), int(len(shallow))
        if n_deep > 0 and n_shallow > 0:
            sup_val = float(np.mean(deep) - np.mean(shallow))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = "Fewer than 30 independent cases over all coins and windows (%d)." % n_cases
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither confirm nor reject is met."
    elif mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-side unusual move is positive with t >= 2 and the deeper half beats the shallower half."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean short-side unusual move is negative with t <= -2: prices rise more than their drift after failures."
    elif mean > 0 and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the deeper half does not beat the shallower half."
    else:
        status = "inconclusive"
        decided = "The t of the main measure lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"independent cases": n_cases, "deeper half": n_deep, "shallower half": n_shallow},
        "decided_by": decided,
        "reading": ("A case is the first short-side bet (forecast falling >= 2 points from its lowest short "
                    "level since the last bet, reset at flat) in each 8-bar grid cell from each window's first "
                    "row, needing 8 bars ahead in the window; drift is the coin's mean 8-bar grid return over all "
                    "windows; the deeper half is entry |forecast| strictly above the median, the shallower half "
                    "at or below it."),
    }
