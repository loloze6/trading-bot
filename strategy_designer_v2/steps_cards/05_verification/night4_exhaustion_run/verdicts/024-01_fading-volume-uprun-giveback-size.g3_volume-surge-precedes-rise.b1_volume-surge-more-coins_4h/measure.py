import numpy as np
import pandas as pd

H = 18
BAND = 2.0
MIN_CASES = 100
RAW_COL = "debug_info.components.vol_surge.last_history_value"


def _raw_ratio(df):
    """Recorded raw component value; where missing, recompute from volume within the window."""
    vol = pd.to_numeric(df["volume"], errors="coerce").astype(float)
    prior_mean = vol.shift(1).rolling(180, min_periods=180).mean()
    recomputed = vol / prior_mean - 1.0
    if RAW_COL in df.columns:
        raw = pd.to_numeric(df[RAW_COL], errors="coerce").astype(float)
        raw = raw.where(raw.notna(), recomputed)
    else:
        raw = recomputed
    return raw.values


def _bets(f):
    """Long bets: a rise of the forecast of at least BAND from its lowest long level since the last bet."""
    n = len(f)
    is_bet = np.zeros(n, dtype=bool)
    low = 0.0
    for i in range(n):
        x = f[i]
        if not np.isfinite(x) or x <= 0:
            low = 0.0  # flat or other side: reset
            continue
        if x - low >= BAND:
            is_bet[i] = True
            low = x
        else:
            low = min(low, x)
    return is_bet


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            f = pd.to_numeric(df["forecast"], errors="coerce").astype(float).values
            raw = _raw_ratio(df)
            active = np.isfinite(f) & (f != 0)
            situ = np.isfinite(raw) & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean excess 18-bar return of long bets"
    main_thr = "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"
    sup_name = "upper-half minus lower-half mean excess return (split at median forecast)"
    reading = ("Situation read as the volume ratio above 1 (raw component value > 0) on the long side; "
               "bets detected per window from 0 at its start, first bet per 18-bar grid cell (counted from the "
               "window's first row) taken as the case; t of the weighted mean is the ordinary t of f*x/mean(f); "
               "the median split puts forecasts above the median in the upper half; fewer than 100 cases gives "
               "'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the volume is above "
                           "its prior 180-bar mean, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- cases ----------
    xs, fs = [], []
    for coin in sorted(bars):
        # coin's mean 18-bar return over all windows, non-overlapping grid
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            c = pd.to_numeric(df["close"], errors="coerce").astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").astype(float).values
            n = len(c)
            for p in range(0, n - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            is_bet = _bets(f)
            for start in range(0, n, H):
                idx = np.where(is_bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if np.isfinite(r) and np.isfinite(f[t]):
                    coin_cases.append((r, f[t]))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, fv in coin_cases:
            xs.append(r - drift)
            fs.append(fv)

    x = np.array(xs, dtype=float)
    fw = np.array(fs, dtype=float)
    n_cases = int(len(x))
    counts = {"cases": n_cases, "active bars": int(n_active)}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} cases across all coins and windows, below the plan's minimum of 100.",
            "reading": reading,
        }

    wmean = float(np.sum(x * fw) / np.sum(fw))
    z = x * fw / np.mean(fw)
    sd = float(np.std(z, ddof=1))
    tstat = float(np.mean(z) / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    med = float(np.median(fw))
    up = x[fw > med]
    lo = x[fw <= med]
    if len(up) > 0 and len(lo) > 0:
        diff = float(np.mean(up) - np.mean(lo))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False
    counts["upper half cases"] = int(len(up))
    counts["lower half cases"] = int(len(lo))

    if wmean > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the upper half beats the lower half."
    elif wmean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is below 0 with t <= -2."
    elif tstat >= 2 and wmean > 0:
        status = "inconclusive"
        decided = "t >= 2 but the upper half does not beat the lower half, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the forecast-weighted mean excess return lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": wmean,
                         "statistic": {"name": "t of the weighted mean", "value": tstat},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
