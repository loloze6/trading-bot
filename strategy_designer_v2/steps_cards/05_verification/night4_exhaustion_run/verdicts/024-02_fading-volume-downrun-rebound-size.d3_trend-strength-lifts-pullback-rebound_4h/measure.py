import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    MAX_BARS = 180
    RISE_COL = "debug_info.components.rise30.last_history_value"

    def wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return str(w)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=wkey):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float).values
            vol = df["volume"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(df)
            # rise30: recorded raw value, else recomputed from closes in the window
            rise_rec = df[RISE_COL].astype(float).values if RISE_COL in df.columns else np.full(n, np.nan)
            rise_calc = np.full(n, np.nan)
            if n > 180:
                rise_calc[180:] = close[180:] / close[:-180] - 1.0
            rise = np.where(np.isnan(rise_rec), rise_calc, rise_rec)
            # down streak length ending at each bar (close below previous close)
            streak = np.zeros(n, dtype=int)
            for i in range(1, n):
                if close[i] < close[i - 1]:
                    streak[i] = streak[i - 1] + 1
            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                L = min(streak[i], MAX_BARS)
                fade_ok = False
                if L >= 2:
                    v = vol[i - L + 1:i + 1]
                    x = np.arange(L, dtype=float)
                    if np.all(np.isfinite(v)):
                        slope = np.polyfit(x, v, 1)[0]
                        fade_ok = (-slope) > 0
                rise_ok = np.isfinite(rise[i]) and rise[i] > 0
                if rise_ok and fade_ok and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 18-bar move of the cases (return minus coin's normal 18-bar drift, signal direction)"
    thr = "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject)"
    reading = ("The down streak is recomputed from prices as consecutive bars closing below the previous close "
               "(capped at 180 bars), volume fading means a negative least-squares slope of volume over those down bars, "
               "rise30 uses the recorded raw value (recomputed from closes where missing); in the supporting check the "
               "upper half is cases with forecast above the median and the lower half those at or below it; cases are the "
               "first bet in each 18-bar grid cell, pooled over coins, each against its own coin's drift.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 30-day rise is above 0 "
                           "and a down streak of at least 2 bars on falling volume closes (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- criterion ----------
    case_moves = []
    case_fc = []
    for coin in sorted(bars):
        wins = sorted(bars[coin], key=wkey)
        # coin's normal 18-bar drift over all windows (non-overlapping grid)
        grid_rets = []
        for w in wins:
            c = bars[coin][w]["close"].astype(float).reset_index(drop=True).values
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w in wins:
            df = bars[coin][w].reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(df)
            ref = 0.0
            side = 0
            bets = []
            for i in range(n):
                s = int(np.sign(fc[i]))
                if s != side:
                    ref = 0.0
                    side = s
                if s == 0:
                    continue
                mag = abs(fc[i])
                if mag - ref >= BAND:
                    bets.append(i)
                    ref = mag
                else:
                    ref = min(ref, mag)
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                d = np.sign(fc[i])
                case_moves.append(float(d * (r - drift)))
                case_fc.append(float(fc[i]))

    x = np.array(case_moves, dtype=float)
    f = np.array(case_fc, dtype=float)
    ncase = int(len(x))
    mean = float(np.mean(x)) if ncase > 0 else None
    tval = None
    if ncase > 1:
        sd = float(np.std(x, ddof=1))
        tval = float(mean / (sd / np.sqrt(ncase))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_up = n_lo = 0
    if ncase > 0:
        med = float(np.median(f))
        up = x[f > med]
        lo = x[f <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if ncase < 30:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 30 cases (%d)." % ncase
    elif tval is not None and mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 over at least 30 cases, and the upper-minus-lower forecast half difference is above 0."
        else:
            status = "inconclusive"
            decided = "Mean unusual move above 0 with t >= 2 but the supporting check (upper minus lower half above 0) fails."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (or is undefined)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move, upper minus lower forecast half",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"cases": ncase, "upper half cases": n_up, "lower half cases": n_lo,
                   "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
