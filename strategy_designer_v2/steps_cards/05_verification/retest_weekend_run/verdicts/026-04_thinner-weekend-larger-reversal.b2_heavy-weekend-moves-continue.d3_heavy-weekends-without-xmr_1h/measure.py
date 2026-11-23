import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    SHORT = 48
    BASE = 120
    COMP = "debug_info.components.wkmove.last_history_value"

    def _ts(df):
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        return pd.Series(ts.values, index=df.index)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)

            recent = vol.rolling(SHORT, min_periods=SHORT).mean()
            prior = vol.shift(SHORT).rolling(BASE, min_periods=BASE).mean()
            ratio = recent / prior
            ret48 = close / close.shift(H) - 1.0
            if COMP in df.columns:
                comp = df[COMP].astype(float)
                move = comp.where(comp.notna(), ret48)
            else:
                move = ret48

            is_sun23 = (ts.dt.dayofweek == 6) & (ts.dt.hour == 23)
            situation = is_sun23 & (ratio > 1.0)
            expected = np.sign(move)

            active = fc != 0
            n_active += int(active.sum())
            agree = active & situation & (np.sign(fc) == expected) & (expected != 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean signed unusual 48-bar move per case"
    threshold = "mean > 0 with t >= 2 (confirm, with size check); mean < 0 with t <= -2 (reject)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are bars stamped Sunday 23:00 UTC "
                           "with a weekend/weekday volume ratio above 1 and a forecast signed like the 48-bar weekend move."),
            "reading": ("The situation is the bar stamped Sunday 23:00 UTC with mean volume of the last 48 bars over the "
                        "120 before them above 1; the expected side is the sign of the wkmove raw value (the 48-bar return where it is missing)."),
        }

    # ---------- 2. criterion ----------
    vals = []
    absf = []
    for coin in sorted(bars):
        # normal drift: mean 48-bar return on the non-overlapping grid of all the coin's windows
        grid = []
        for w in sorted(bars[coin]):
            c = bars[coin][w]["close"].astype(float).reset_index(drop=True).values
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid.append(r)
        if len(grid) == 0:
            continue
        drift = float(np.mean(grid))

        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            last_kept = -10 ** 9
            for t in np.nonzero(fc != 0)[0]:
                if t + H >= len(c):
                    continue
                if t - last_kept < H:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                last_kept = t
                vals.append(np.sign(fc[t]) * (r - drift))
                absf.append(abs(fc[t]))

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n = int(len(vals))

    mean = float(np.mean(vals)) if n > 0 else None
    tval = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        tval = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if n > 0:
        med = float(np.median(absf))
        hi = vals[absf > med]
        lo = vals[absf < med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)

    reading = ("Cases are the nonzero-forecast bars with 48 bars ahead in their window, keeping a bar only if 48 bars "
               "after the previous kept case; the normal drift is the coin's mean 48-bar return on the non-overlapping "
               "grid of all its windows; cases with |forecast| equal to the median are left out of the size check; "
               "the plan's 30-case minimum maps to 'not observable'.")

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean signed unusual move cannot be computed, so neither confirm nor reject is met."
    elif mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean signed unusual move is positive with t >= 2 and the size check passes."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the size check (above-median minus below-median |forecast|) fails."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean signed unusual move is negative with t <= -2: heavy-volume weekend moves reverse."
    else:
        status = "inconclusive"
        decided = "The t of the mean signed unusual move is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean signed unusual move, |forecast| above median minus below median",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n, "cases above median": n_hi, "cases below median": n_lo},
        "decided_by": decided,
        "reading": reading,
    }
