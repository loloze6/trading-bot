import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    VR_MIN = 2.0
    BODY_MAX = 0.3
    VOL_PERIOD = 20
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            o = d["open"].astype(float)
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            c = d["close"].astype(float)
            v = d["volume"].astype(float)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            rng = h - l
            prior_mean = v.shift(1).rolling(VOL_PERIOD, min_periods=VOL_PERIOD).mean()
            vr = v / prior_mean.replace(0, np.nan)
            body = (c - o).abs() / rng.replace(0, np.nan)
            cloc = (2 * c - h - l) / rng.replace(0, np.nan)
            sit = (vr >= VR_MIN) & (body <= BODY_MAX)
            # first bars of a window lack 20 prior bars in the record: use the detector's regime there
            if "regime" in d.columns:
                fallback = d["regime"].astype(str) == "trending"
                sit = sit.where(vr.notna(), fallback)
            sit = sit.fillna(False).astype(bool)
            exp_side = np.sign(cloc).fillna(0.0)
            active = f != 0
            agree = active & sit & (np.sign(f) == exp_side) & (exp_side != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    threshold_txt = "confirm: slope > 0 with t >= 2 on >= 30 cases; reject: slope < 0 with t <= -2 on >= 30 cases"
    reading = ("Situation recomputed from prices (volume over the mean of the 20 prior bars of the window, body over range, "
               "side from the sign of the close location), falling back to the recorded regime on a window's first 20 bars; "
               "a case is the first bet (forecast rise of >= 2 on its side from its lowest level since the last bet, reset to 0 "
               "after flat or a side change) in each 5-bar grid cell of a window, with its 5-bar return inside the window, "
               "pooled over all coins in one OLS of the unusual move (not direction-flipped) on the signed forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "OLS slope of unusual 5-bar move on forecast", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of active forecast bars are absorption days (volume >= 2x prior 20-day mean, "
                           "body <= 30% of range) with the forecast sign equal to the close-location sign."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all its windows (non-overlapping grid)
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            n = len(c)
            for p in range(0, n - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for d in prepared:
            c = d["close"].astype(float).values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(c)
            side = 0
            ref = 0.0
            bets = np.zeros(n, dtype=bool)
            for i in range(n):
                s = int(np.sign(f[i]))
                if s == 0:
                    side, ref = 0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                a = abs(f[i])
                if a - ref >= BAND:
                    bets[i] = True
                    ref = a
                else:
                    ref = min(ref, a)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bets[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] == 0:
                    continue
                ys.append(c[i + H] / c[i] - 1 - drift)
                xs.append(float(f[i]))

    n_cases = len(xs)
    slope, tval = None, None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Fewer than {MIN_CASES} cases ({n_cases}): the plan's minimum count is not reached."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2 on at least 30 cases (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2 on at least 30 cases (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2 on at least 30 cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "OLS slope of unusual 5-bar move on forecast",
                         "value": slope,
                         "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
                         "threshold": threshold_txt},
        "supporting_check": None,
        "counts": {"cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }
