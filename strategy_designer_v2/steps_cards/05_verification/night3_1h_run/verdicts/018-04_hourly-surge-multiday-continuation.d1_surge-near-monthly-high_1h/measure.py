import numpy as np
import pandas as pd

RAW = "debug_info.components.surge_near_high.last_history_value"
H = 120
BAND = 2.0
MIN_CASES = 30


def _bets_long(f):
    """Bar positions of long-side bets: a rise of the forecast of at least BAND,
    measured from its lowest long level since the last bet (from 0 after a flat or a short)."""
    out = []
    trough = 0.0
    for i, v in enumerate(f):
        if not np.isfinite(v) or v <= 0:
            trough = 0.0
            continue
        if v < trough:
            trough = v
        if v - trough >= BAND:
            out.append(i)
            trough = v
    return out


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            active = np.isfinite(f) & (f != 0)
            situ = np.isfinite(raw) & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    sit = {"agreement": agreement, "passed": passed}

    main_name = "mean unusual 120-bar move after long cases (return minus coin's normal 120-bar drift)"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation bars are those where the raw component (24h return in usual daily moves times proximity weight) is "
               "positive, on the long side; a case is the first long bet (forecast rise >= 2 points from its long trough) in each "
               "120-bar grid cell from each window's first row, with a full 120-bar forward return inside the window; drift is the coin's "
               "mean non-overlapping 120-bar return over all windows; halves are the lower and upper n//2 cases by entry forecast "
               "(stable sort, middle case dropped if n is odd); fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "independent cases": 0},
            "decided_by": ("Only %.3f of active (non-zero forecast) bars are bars where the plan's upside surge near the 30-day high "
                           "holds with a long forecast, below the 90%% needed." % agreement),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin in sorted(bars):
        rets = []
        for w in sorted(bars[coin]):
            c = pd.to_numeric(bars[coin][w]["close"], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(c) - H, H):
                a, b = c[t], c[t + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    unusual = []
    entry_f = []
    for coin in sorted(bars):
        if not np.isfinite(drift[coin]):
            continue
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            seen = set()
            for i in _bets_long(f):
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c):
                    continue
                a, b = c[i], c[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                unusual.append(b / a - 1.0 - drift[coin])
                entry_f.append(f[i])

    u = np.asarray(unusual, dtype=float)
    ef = np.asarray(entry_f, dtype=float)
    n = int(len(u))
    mean_u = float(u.mean()) if n > 0 else None
    tstat = None
    if n >= 2:
        sd = float(u.std(ddof=1))
        tstat = float(mean_u / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n >= 2:
        order = np.argsort(ef, kind="stable")
        k = n // 2
        lower = u[order[:k]]
        upper = u[order[n - k:]]
        sup_val = float(upper.mean() - lower.mean())
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean", "value": tstat} if tstat is not None else None),
            "threshold": thr}
    sup = {"name": "upper-half minus lower-half mean unusual move by entry forecast",
           "value": sup_val, "passed": sup_pass}
    counts = {"independent cases": n}

    if n < MIN_CASES:
        status = "not observable"
        decided = "Only %d independent cases, fewer than the plan's minimum of 30." % n
    elif tstat is not None and mean_u > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move is positive with t >= 2 over at least 30 cases and the supporting check is above 0."
    elif tstat is not None and mean_u < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual move is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        if tstat is not None and mean_u > 0 and tstat >= 2:
            decided = "The main measure meets the confirm rule but the supporting check fails, which the plan calls inconclusive."
        else:
            decided = "The t-statistic lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
