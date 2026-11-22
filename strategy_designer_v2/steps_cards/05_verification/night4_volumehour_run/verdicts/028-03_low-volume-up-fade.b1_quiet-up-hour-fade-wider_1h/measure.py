import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    MIN_CASES = 30
    RISE_COL = "debug_info.components.rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            if RISE_COL in df.columns:
                rise = pd.to_numeric(df[RISE_COL], errors="coerce").to_numpy(dtype=float)
            else:
                rise = np.full(len(df), np.nan)
            active = np.isfinite(f) & (f != 0)
            # Situation: the volume regime (0.67..1.5 of its 720-bar mean, recorded as the
            # detector's decision) and an hour that rose (raw scaled return > 0).
            # The expected side is short.
            situ = (reg == "mean_reversion") & np.isfinite(rise) & (rise > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

    if n_active == 0:
        agreement = None
        passed = None
    else:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.90)

    main_name = "mean unusual move of short bets over 6 bars (in the signal's direction)"
    main_thr = "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 (reject)"
    reading = ("The volume condition is read from the recorded regime (mean_reversion = volume ratio "
               "between 0.67 and 1.5) and the rise from the raw scaled return being above 0; a case "
               "is the first short bet (forecast falling by >= 2 points from its least-short level "
               "since the last bet, reset at 0) in each 6-bar grid cell counted from each window's "
               "first row, with a full 6-bar return inside the window; the normal drift is the coin's "
               "mean non-overlapping 6-bar return over all its windows; the slope regresses the "
               "unusual move on |forecast|; the plan's 'fewer than 30 cases' is reported as not "
               "observable as the workflow requires.")

    if passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on "
                           "an ordinary-volume hour that rose, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    unusual = []
    sizes = []
    for coin, wins in bars.items():
        # normal drift: mean non-overlapping 6-bar return over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            grid_rets.extend(list(r[np.isfinite(r)]))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(f)
            ref = 0.0
            taken_cells = set()
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft >= 0:
                    ref = 0.0
                    continue
                mag = -ft
                if mag - ref >= BAND - 1e-12:
                    ref = mag
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                        ret = c[t + H] / c[t] - 1.0
                        unusual.append(-(ret - drift))
                        sizes.append(mag)
                else:
                    ref = min(ref, mag)

    unusual = np.asarray(unusual, dtype=float)
    sizes = np.asarray(sizes, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope = None
    if n_cases > 2 and np.ptp(sizes) > 0:
        slope = float(stats.linregress(sizes, unusual).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"cases": n_cases}
    sit = {"agreement": None if agreement is None else float(agreement),
           "passed": passed if passed is not None else False}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (no spread), so neither rule is met."
    elif mean_u > 0 and t_u >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 over at least 30 cases and a slope above 0."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2) but the slope is not above 0."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 with at least 30 cases."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "ordinary t of the mean", "value": t_u},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "slope of unusual move on forecast size",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
