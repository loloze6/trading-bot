import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    BAND = 2.0
    MIN_CASES = 30
    PL = "debug_info.components.plunge.last_history_value"
    RR = "debug_info.components.rise30_rec.last_history_value"

    def col(df, name):
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            plunge = col(df, PL)
            rise30 = col(df, RR)
            # fall back to prices (inside the window only) where not recorded
            plunge = plunge.where(plunge.notna(), close / close.shift(24) - 1)
            rise30 = rise30.where(rise30.notna(), close / close.shift(720) - 1)
            situation = (rise30 > 0) & (plunge < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual 72-bar move per long case (return minus coin's normal 72-bar drift)"
    main_thr = "t >= 2 confirms (with check > 0); t <= -2 rejects"
    sup_name = "mean unusual move with rise30_rec above its median minus below"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"independent cases": None},
            "decided_by": "Fewer than 90% of active bars are long bars with a positive 30-day return and a negative 24-hour return, as the Fidelity's situation and long side require.",
            "reading": "Situation taken as recorded 720-bar return > 0 and recorded 24-bar return < 0 (prices where not recorded), side long.",
        }

    # ---------- 2. criterion ----------
    unusual = []
    rise_vals = []
    for coin in sorted(bars):
        wins = sorted(bars[coin])
        # normal drift: mean 72-bar return on the grid 0, 72, ... of all windows
        grid_rets = []
        for w in wins:
            df = bars[coin][w].reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1
                if np.isfinite(r):
                    grid_rets.append(r)
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))

        for w in wins:
            df = bars[coin][w].reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            rr = col(df, RR).values
            # long bets: rise of forecast >= band from its lowest long level since last bet
            low = 0.0
            bets = []
            for i, f in enumerate(fc):
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bets.append(i)
                    low = f
                else:
                    low = min(low, f)
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1
                if not np.isfinite(r):
                    continue
                unusual.append(r - drift)
                rise_vals.append(rr[i])

    u = np.array(unusual, dtype=float)
    n = int(len(u))
    mean_u = float(np.mean(u)) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(np.std(u, ddof=1))
        t = float(mean_u / (sd / np.sqrt(n))) if sd > 0 else None

    rv = np.array(rise_vals, dtype=float)
    ok = np.isfinite(rv)
    diff = None
    n_above = n_below = 0
    if ok.sum() > 0:
        med = float(np.median(rv[ok]))
        above = u[ok & (rv > med)]
        below = u[ok & (rv < med)]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above > 0 and n_below > 0:
            diff = float(above.mean() - below.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    if n < MIN_CASES or t is None:
        status = "not observable"
        decided = f"Only {n} independent cases, below the plan's minimum of 30 across all coins and windows."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move has a t of at least 2 and the supporting check is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The mean unusual move has a t of -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The t is 2 or more but the supporting check is at or below 0 (or could not be computed)."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": {"independent cases": n, "cases above median": n_above, "cases below median": n_below},
        "decided_by": decided,
        "reading": "Cases are the first long bet per 72-bar grid cell of each window (cells from the window's first row, cases whose 72-bar return leaves the window dropped), the rise30_rec median is pooled over all cases with cases at the median left out, and fewer than 30 cases is reported as not observable.",
    }
