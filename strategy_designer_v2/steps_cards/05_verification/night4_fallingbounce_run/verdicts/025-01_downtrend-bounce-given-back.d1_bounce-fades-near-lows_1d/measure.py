import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.bounce_near_low.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            ret90 = close / close.shift(90) - 1.0
            day_ret = close / close.shift(1) - 1.0
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            for i in range(len(df)):
                if fc.iloc[i] == 0:
                    continue
                n_active += 1
                # falling regime: 90-day return < 0 from prices when computable in-window,
                # otherwise the detector's recorded decision
                if not np.isnan(ret90.iloc[i]):
                    falling = ret90.iloc[i] < 0
                else:
                    falling = regime.iloc[i] == "mean_reversion"
                # a one-day rise: raw component > 0 (0 on down days), else from prices
                r = raw.iloc[i]
                if not np.isnan(r):
                    rise = r > 0
                elif not np.isnan(day_ret.iloc[i]):
                    rise = day_ret.iloc[i] > 0
                else:
                    rise = False
                if falling and rise and fc.iloc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("The 90-day return is recomputed from in-window closes where 90 prior bars exist and taken from the "
               "recorded regime otherwise; a case is the first short bet (a rise of the short forecast's size of at "
               "least 2 points from its lowest size since the last bet, reset at flat or side change) in each 5-bar "
               "grid cell of its window, with its 5-bar return inside the window; the larger half is abs forecast "
               "above the median and the smaller half at or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move in the short direction", "value": None,
                             "statistic": None, "threshold": "t >= 2 over at least 30 cases"},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are falling-regime one-day rises held short "
                           f"(agreement {agreement:.3f}): the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    vals = []
    absf = []
    for coin, wins in bars.items():
        # coin's normal 5-bar drift: non-overlapping grid returns, all windows together
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for s in range(0, len(c) - H, H):
                if np.isfinite(c[s]) and np.isfinite(c[s + H]) and c[s] > 0:
                    grid_rets.append(c[s + H] / c[s] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(c)
            bet = np.zeros(n, dtype=bool)
            side = 0
            low = 0.0
            for i in range(n):
                f = fc[i]
                s = -1 if f < 0 else (1 if f > 0 else 0)
                m = abs(f)
                if s == 0:
                    side = 0
                    low = 0.0
                    continue
                if s != side:
                    side = s
                    low = 0.0
                if m - low >= BAND - 1e-12:
                    if s == -1:
                        bet[i] = True
                    low = m
                else:
                    low = min(low, m)
            for start in range(0, n, H):
                cell = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not cell:
                    continue
                i = cell[0]
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                ret = c[i + H] / c[i] - 1.0
                vals.append(-(ret - drift))
                absf.append(abs(fc[i]))

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(vals))

    mean = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(absf))
        large = vals[absf > med]
        small = vals[absf <= med]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            sup_val = float(np.mean(large) - np.mean(small))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": "mean unusual 5-bar move in the short direction",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2"}
    support = {"name": "mean unusual move, larger-|forecast| half minus smaller half",
               "value": sup_val, "passed": sup_pass}
    counts = {"cases": n_cases, "larger half": n_large, "smaller half": n_small}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no dispersion), so neither rule is met."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 over at least 30 cases and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "A confirming t with a failed supporting check is inconclusive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
