import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    BAND = 2.0
    RISE_COL = "debug_info.components.rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            vol = df["volume"].astype(float)
            vr = vol / vol.rolling(720, min_periods=720).mean()
            f = df["forecast"].astype(float)
            ret1 = df["close"].astype(float) / df["close"].astype(float).shift(1) - 1.0
            if RISE_COL in df.columns:
                rise = df[RISE_COL].astype(float)
                rise = rise.where(rise.notna(), ret1)
            else:
                rise = ret1
            active = (f != 0) & f.notna() & vr.notna() & rise.notna()
            if active.sum() == 0:
                continue
            situ = (vr >= 0.8) & (vr <= 1.25) & (rise > 0) & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean short-direction 2-bar excess return of short bets (vs coin's normal 2-bar drift), before costs"
    threshold = "confirm t >= 2 over >= 30 cases with positive slope; reject t <= -2 over >= 30 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars_checked": n_active},
            "decided_by": ("Fewer than 90% of active bars (forecast != 0) are bars where the hour rose with volume "
                           "ratio between 0.8 and 1.25 and the forecast is short, as the Fidelity's situation requires."),
            "reading": ("The volume ratio is recomputed inside each window as volume over its 720-bar rolling mean "
                        "(current bar included); bars without 720 bars of history are left out of the check."),
        }

    # ---------- 2. criterion ----------
    excess_all = []
    size_all = []
    for coin, wins in bars.items():
        # coin's normal 2-bar drift over all windows, non-overlapping grid
        drifts = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                drifts.extend(list(c[idx + H] / c[idx] - 1.0))
        drifts = np.array(drifts, dtype=float)
        drifts = drifts[np.isfinite(drifts)]
        if len(drifts) == 0:
            continue
        drift = float(drifts.mean())

        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            f = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(f)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                if f[i] < 0:
                    s = -f[i]
                    if not prev_short:
                        ref = 0.0
                    if s - ref >= BAND:
                        bet[i] = True
                        ref = s
                    else:
                        ref = min(ref, s)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
            for start in range(0, n, H):
                cell = np.where(bet[start:start + H])[0]
                if len(cell) == 0:
                    continue
                t = start + int(cell[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                excess_all.append(-(r - drift))
                size_all.append(abs(f[t]))

    ex = np.array(excess_all, dtype=float)
    sz = np.array(size_all, dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(ex.mean()) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = ex.std(ddof=1)
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    slope = None
    if n_cases > 2 and np.std(sz) > 0:
        slope = float(stats.linregress(sz, ex).slope)

    reading = ("A bet is a rise of the short forecast's magnitude of at least 2 points from its lowest short level since "
               "the last bet (reset to 0 after flat or long), the first bet bar of each non-overlapping 2-bar cell of a "
               "window is the case, cases are pooled over all coins for the mean and its ordinary t, the forecast size is "
               "its absolute value, and the volume ratio for the situation check is recomputed within each window with a "
               "720-bar mean including the current bar.")

    slope_passed = None if slope is None else bool(slope > 0)
    result = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of short-direction excess return on forecast size",
                             "value": slope, "passed": slope_passed},
        "counts": {"cases": n_cases},
        "reading": reading,
    }

    if n_cases < 30:
        result["status"] = "not observable"
        result["decided_by"] = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
        return result
    if t_val is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
        return result
    if t_val >= 2 and slope_passed:
        result["status"] = "confirmed"
        result["decided_by"] = "Mean short-direction excess return has t >= 2 over at least 30 cases and the supporting slope is above 0."
    elif t_val >= 2:
        result["status"] = "inconclusive"
        result["decided_by"] = "t >= 2 but the supporting slope is at or below 0, which the plan calls inconclusive."
    elif t_val <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "Mean short-direction excess return has t <= -2 over at least 30 cases: such rises extend rather than give back."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "t lies between -2 and 2, which the plan calls inconclusive."
    return result
