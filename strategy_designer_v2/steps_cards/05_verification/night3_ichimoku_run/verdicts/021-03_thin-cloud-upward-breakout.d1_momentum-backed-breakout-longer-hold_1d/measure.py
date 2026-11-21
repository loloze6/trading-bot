import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 40
    BAND = 2.0
    MIN_CASES = 30

    def _cloud_state(df):
        h = df["high"].astype(float)
        l = df["low"].astype(float)
        c = df["close"].astype(float)
        tenkan = (h.rolling(9).max() + l.rolling(9).min()) / 2.0
        kijun = (h.rolling(26).max() + l.rolling(26).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(26)
        span_b = ((h.rolling(52).max() + l.rolling(52).min()) / 2.0).shift(26)
        top = np.maximum(span_a, span_b)
        bot = np.minimum(span_a, span_b)
        state = pd.Series(np.nan, index=df.index)
        ok = top.notna() & bot.notna()
        state[ok & (c > top)] = 1.0
        state[ok & (c < bot)] = -1.0
        state[ok & (c <= top) & (c >= bot)] = 0.0
        return state.values

    def _situation(df):
        # returns array: 1 = situation, 0 = not, computed from prices; regime fallback where undetermined
        st = _cloud_state(df)
        reg = df["regime"].astype(str).str.lower().values if "regime" in df.columns else np.array([""] * len(df))
        n = len(df)
        out = np.zeros(n, dtype=bool)
        for t in range(n):
            determined = True
            sit = False
            if t == 0 or np.isnan(st[t]) or np.isnan(st[t - 1]):
                determined = False
            elif st[t] != 1.0 or st[t - 1] == 1.0:
                sit = False
            else:
                # first bar above after not above: last outside state before t must be below
                found = None
                for k in range(t - 1, -1, -1):
                    if np.isnan(st[k]):
                        break
                    if st[k] != 0.0:
                        found = st[k]
                        break
                if found is None:
                    determined = False
                else:
                    sit = (found == -1.0)
            if not determined:
                sit = (reg[t] == "trending")
            out[t] = sit
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = df["forecast"].astype(float).fillna(0.0).values
            sit = _situation(df)
            act = f != 0
            n_active += int(act.sum())
            n_agree += int((act & sit & (f > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "OLS slope of unusual 40-bar move on case forecast"
    thr = "confirm: slope > 0 with t >= 2 and mean unusual move > 0; reject: slope < 0 with t <= -2; at least 30 cases"
    reading = ("Situation recomputed from prices as an Ichimoku (9,26,52,26) close first above the cloud whose last "
               "outside state was below, using the recorded regime 'trending' where the window lacks the history to "
               "compute it; a case is the first long bet (forecast rise >= 2 from its low since the last bet, from 0 "
               "after flat) in each 40-bar grid cell of a window, cases without 40 forward bars in the window are "
               "dropped, drift is the coin's mean 40-bar return on the window grids, and the count of 30 is treated "
               "as a minimum count (not observable if unmet).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long forecasts on an upward "
                           "cloud-cross bar (cross age 1), so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- cases ----------
    cases = []  # (coin, forecast, ret)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for p in range(0, n, H):
                if p + H < n and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            f = df["forecast"].astype(float).fillna(0.0).values
            low = 0.0
            side = 0
            seen_cells = set()
            for t in range(n):
                ft = f[t]
                s = 1 if ft > 0 else (-1 if ft < 0 else 0)
                if s != side:
                    side = s
                    low = 0.0
                if s == 0:
                    low = 0.0
                    continue
                mag = abs(ft)
                if mag - low >= BAND:
                    if s > 0:
                        cell = t // H
                        if cell not in seen_cells:
                            seen_cells.add(cell)
                            if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                                cases.append((coin, float(ft), c[t + H] / c[t] - 1.0))
                    low = mag
                else:
                    low = min(low, mag)
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan

    xs, ys = [], []
    for coin, ft, r in cases:
        d = drift.get(coin, np.nan)
        if np.isfinite(d) and np.isfinite(r):
            xs.append(ft)
            ys.append(r - d)
    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_cases = int(len(ys))
    counts = {"cases": n_cases}
    sc = {"agreement": None if agreement is None else float(agreement), "passed": passed}

    mean_unusual = float(np.mean(ys)) if n_cases > 0 else None
    slope = None
    tstat = None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(xs, ys)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    supp = {"name": "mean unusual 40-bar move over cases > 0", "value": mean_unusual,
            "passed": None if mean_unusual is None else bool(mean_unusual > 0)}
    mm = {"name": main_name, "value": slope,
          "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
          "threshold": thr}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases across coins and windows, below the plan's minimum of 30."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the case forecasts), so neither rule is met."
    elif slope > 0 and tstat >= 2:
        if mean_unusual is not None and mean_unusual > 0:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move over the cases is above zero."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the mean unusual move is at or below zero."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": mm,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
