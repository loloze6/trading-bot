import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    LHV = "debug_info.components.vol_dryup.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce")
            else:
                lhv = pd.Series(np.nan, index=df.index)
            falling = df["regime"].astype(str) == "unknown"
            shrunk = lhv < 0
            situation = falling & shrunk & lhv.notna()
            on_side = fc < 0
            n_active += int(active.sum())
            n_agree += int((active & situation & on_side).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of short-direction 20-bar excess return on |forecast| (grid cells with forecast < 0)"
    main_thr = "slope t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; fewer than 30 cells: not observable"
    reading = ("Falling profile taken as the regime detector's decision (regime 'unknown', i.e. not vetoed to 'chop'), "
               "dry-up as raw vol_dryup < 0 and expected side short; grid cells at positions 0,20,40,... of each window "
               "with t+20 inside it, coin mean 20-bar return taken over that grid in all its windows, cells pooled over "
               "all coins for one OLS slope t, thirds as floor(n/3) cells by |forecast|, and the plan's minimum of 30 "
               "cells treated as a minimum count (not observable below it).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling "
                           "profile with a shrunk 30-day volume (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid = []  # (forecast, return)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid.append((fc[t], c1 / c0 - 1.0))
        if not grid:
            continue
        rets = np.array([g[1] for g in grid], dtype=float)
        mu = float(np.mean(rets))
        for f, r in grid:
            if np.isfinite(f) and f < 0:
                xs.append(abs(f))
                ys.append(-(r - mu))

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cells = int(len(x))
    counts = {"grid cells with a negative forecast": n_cells}

    slope = None
    t_stat = None
    if n_cells >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_stat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = None
    sup_pass = None
    if n_cells >= 3:
        order = np.argsort(x, kind="mergesort")
        k = n_cells // 3
        if k >= 1:
            bottom = y[order[:k]]
            top = y[order[-k:]]
            sup_val = float(np.mean(top) - np.mean(bottom))
            sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_stat} if t_stat is not None else None),
            "threshold": main_thr}
    sup = {"name": "top third minus bottom third mean short excess return by |forecast|",
           "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cells < 30:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": "Fewer than 30 grid cells with a negative forecast (%d)." % n_cells,
                "reading": reading}

    if t_stat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no spread in |forecast|), so neither confirm nor reject is met."
    elif t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope t is 2 or more and the top third beats the bottom third."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": decided, "reading": reading}
