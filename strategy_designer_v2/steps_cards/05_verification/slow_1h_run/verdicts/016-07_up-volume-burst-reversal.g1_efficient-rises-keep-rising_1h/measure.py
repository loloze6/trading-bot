import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    MIN_CASES = 200
    FC = "forecast"

    # ---------- 1. Situation check ----------
    # Plan's situation: close above its level 48 bars ago AND above its level 72 bars ago,
    # with the side expected long (outcome: the coin rises more).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp") if "timestamp" in df.columns else df
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            s = pd.Series(close)
            rise48 = (s / s.shift(48) - 1.0).to_numpy()
            rise72 = (s / s.shift(72) - 1.0).to_numpy()
            # Only bars where the forecast is known, non-zero, and the lookbacks exist
            # inside the window can be checked.
            valid = np.isfinite(fc) & (fc != 0) & np.isfinite(rise48) & np.isfinite(rise72)
            situation = (rise48 > 0) & (rise72 > 0)
            n_active += int(valid.sum())
            n_agree += int((valid & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "pooled OLS slope of excess forward 72-bar return on forecast (grid bars, forecast > 0)"
    threshold = "confirm if slope t >= 2 with >= 200 cases and forecast-weighted mean excess > 0; reject if t <= -2 with >= 200 cases"
    sup_name = "forecast-weighted mean excess 72-bar return > 0"
    reading = ("Situation checked on active bars whose 48- and 72-bar lookbacks lie inside the window; "
               "the coin's mean 72-bar return is the mean over all its non-overlapping grid bars (positions 0, 72, 144, ...) "
               "in all windows, grid bars without a full 72-bar forward return in the window are dropped, "
               "and the slope's t is the ordinary OLS t of the slope with an intercept.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars where close is above its level 48 and 72 bars ago "
                           "with a long forecast, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []  # (coin, forecast, fwd return)
    coin_grid_rets = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp") if "timestamp" in df.columns else df
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[j]) and close[i] > 0):
                    continue
                r = close[j] / close[i] - 1.0
                all_rets.append(r)
                rows.append((coin, fc[i], r))
        coin_grid_rets[coin] = float(np.mean(all_rets)) if len(all_rets) else np.nan

    f_list, ex_list = [], []
    for coin, f, r in rows:
        m = coin_grid_rets.get(coin, np.nan)
        if np.isfinite(f) and f > 0 and np.isfinite(m) and np.isfinite(r):
            f_list.append(f)
            ex_list.append(r - m)
    f_arr = np.asarray(f_list, dtype=float)
    ex_arr = np.asarray(ex_list, dtype=float)
    n_cases = int(len(f_arr))
    counts = {"non-overlapping grid bars with forecast > 0": n_cases}

    slope, t_slope = None, None
    if n_cases >= 3 and np.std(f_arr) > 0:
        lr = stats.linregress(f_arr, ex_arr)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    wmean = float(np.sum(f_arr * ex_arr) / np.sum(f_arr)) if n_cases > 0 and np.sum(f_arr) > 0 else None
    sup_passed = (wmean > 0) if wmean is not None else None

    main = {
        "name": main_name,
        "value": slope,
        "statistic": {"name": "OLS t of slope", "value": t_slope} if t_slope is not None else None,
        "threshold": threshold,
    }
    supporting = {"name": sup_name, "value": wmean, "passed": sup_passed}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping grid bars with forecast > 0, fewer than the plan's minimum of 200."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is >= 2 with at least 200 cases and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is <= -2 with at least 200 cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is >= 2 but the forecast-weighted mean excess return is <= 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
