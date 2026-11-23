import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_undetermined = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = pd.to_numeric(df["open"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")
            v = pd.to_numeric(df["volume"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            prior_mean = v.shift(1).rolling(20, min_periods=20).mean()
            vr = v / prior_mean
            body = (c - o).abs() / o * 100.0
            situ = (vr >= 2.0) & (body <= 1.0)
            determinable = vr.notna() & np.isfinite(vr) & body.notna()
            active = f != 0
            act_det = active & determinable
            n_undetermined += int((active & ~determinable).sum())
            n_active += int(act_det.sum())
            n_agree += int((act_det & situ & (f < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_base = (
        "The situation is recomputed per window from prices: volume over the mean of the 20 prior bars' volume "
        "(rows of the same window, current bar excluded) at least 2 and |close-open|/open at most 1 percent, the "
        "expected side short; active bars of a window's first 20 rows, where the ratio cannot be computed, are left "
        "out of the agreement; a case is a short bet (a rise of the short forecast's size of at least 2 points from "
        "its lowest level on that side since the last bet, reset to 0 after flat or long), the first such bet in each "
        "5-row grid cell of a window, pooled over all coins, its 5-bar return taken from that bet's close and "
        "dropped if it runs past the window's end; the drift is the coin's mean non-overlapping 5-bar grid return "
        "over all its windows; the slope is ordinary least squares, judged above 0 by sign alone."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars not determinable": n_undetermined},
            "decided_by": ("Fewer than 90 % of the active bars are heavy, flat days (volume >= 2x its prior "
                           "20-day mean, body <= 1 %) with a short forecast, so the config does not do what the "
                           "plan's situation and side say."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    excess = []
    sizes = []
    for coin, wins in bars.items():
        # drift: mean non-overlapping 5-bar return over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(c)
            for p in range(0, n - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append((c, f))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for c, f in prepared:
            n = len(c)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                ft = f[t]
                if ft < 0:
                    m = -ft
                    if m - ref >= BAND:
                        # a short bet
                        ref = m
                        cell = t // H
                        if cell not in seen_cells:
                            seen_cells.add(cell)
                            if t + H < n:
                                r = c[t + H] / c[t] - 1.0
                                if np.isfinite(r):
                                    excess.append(-(r - drift))
                                    sizes.append(abs(ft))
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0

    excess = np.asarray(excess, dtype=float)
    sizes = np.asarray(sizes, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases > 2 and np.ptp(sizes) > 0:
        slope = float(stats.linregress(sizes, excess).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30 cases."
    elif t_val is not None and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean excess fall has t >= 2 and its slope on abs(forecast) is above 0, with at least 30 cases."
    elif t_val is not None and t_val <= -2:
        status = "rejected"
        decided = "The mean excess fall has t <= -2 with at least 30 cases: the coin rises more than its drift after these days."
    elif t_val is not None and t_val >= 2:
        status = "inconclusive"
        decided = "The mean excess fall has t >= 2 but its slope on abs(forecast) is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess fall lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean 5-day excess fall after short bets (minus coin drift, fall positive)",
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": "confirm t >= 2 with the slope check passing; reject t <= -2; at least 30 cases",
        },
        "supporting_check": {
            "name": "slope of excess fall on abs(forecast) above 0",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading_base,
    }
