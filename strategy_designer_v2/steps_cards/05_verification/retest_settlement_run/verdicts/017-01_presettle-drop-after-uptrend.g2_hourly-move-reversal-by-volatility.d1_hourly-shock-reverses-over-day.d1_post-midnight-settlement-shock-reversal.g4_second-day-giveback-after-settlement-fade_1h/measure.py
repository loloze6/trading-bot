import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    FC = "forecast"
    R24_COL = "debug_info.components.reversal.last_history_value"

    # ---------- per-coin normal 24-bar drift (non-overlapping grid over all windows) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend(r[np.isfinite(r)].tolist())
        drift[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check + case collection ----------
    n_active = 0
    n_agree = 0
    xs, ys, dirs_unusual = [], [], []

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # raw r24: recorded component value where present, else rebuilt from prices
            r24_px = np.full(n, np.nan)
            if n > H:
                r24_px[H:] = c[H:] / c[:-H] - 1.0
            if R24_COL in df.columns:
                r24_rec = pd.to_numeric(df[R24_COL], errors="coerce").to_numpy(dtype=float)
                r24 = np.where(np.isfinite(r24_rec), r24_rec, r24_px)
            else:
                r24 = r24_px

            # h1: the one-bar return lagged 24 bars (sign of the vol-scaled return is the return's sign)
            h1 = np.full(n, np.nan)
            if n > H + 1:
                one = np.full(n, np.nan)
                one[1:] = c[1:] / c[:-1] - 1.0
                h1[H:] = one[:-H]

            hour0 = (ts.dt.hour.to_numpy() == 0) & (ts.dt.minute.to_numpy() == 0)
            situ = hour0 & np.isfinite(r24) & np.isfinite(h1) & (np.sign(r24) * np.sign(h1) < 0)
            exp_side = np.sign(h1)

            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (np.sign(f) == exp_side)).sum())

            # cases: trending regime with non-zero forecast
            reg = df["regime"].astype(str).to_numpy()
            case = active & (reg == "trending")
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = c[H:] / c[:-H] - 1.0
            d = drift.get(coin, np.nan)
            for i in np.where(case)[0]:
                if np.isfinite(fwd[i]) and np.isfinite(d):
                    u = fwd[i] - d
                    xs.append(float(f[i]))
                    ys.append(float(u))
                    dirs_unusual.append(float(np.sign(f[i]) * u))

    threshold = "confirm: slope > 0 with t >= 2 (and mean unusual move > 0); reject: slope < 0 with t <= -2; at least 300 cases"
    mm_name = "slope of 24-bar forward return minus normal drift on forecast, pooled"
    reading = ("The active bar of the situation is the bar stamped 00:00 UTC (closing at 01:00), with r24 the 24-bar return "
               "to its close and the hour's move the one-bar return 24 bars earlier, both by row position inside a window; "
               "cases are trending bars with non-zero forecast and a full 24-bar forward return in the window, one per day so "
               "already non-overlapping, the drift is the coin's mean 24-bar return on the non-overlapping grid of all its windows, "
               "the regression is OLS with intercept, and fewer than 300 cases is reported as not observable.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean unusual 24-bar move in forecast direction", "value": None, "passed": None},
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 300 cases is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": len(xs), "active_bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are 00:00-UTC bars where the 24-bar return runs against the "
                           "lagged 00:00-01:00 hour's move with the forecast on that hour's side."),
            "reading": reading,
        }

    n_cases = len(xs)
    slope = t = None
    sup_val = float(np.mean(dirs_unusual)) if n_cases else None
    if n_cases >= 3:
        x = np.asarray(xs)
        y = np.asarray(ys)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            t = float(lr.slope / lr.stderr) if lr.stderr and np.isfinite(lr.stderr) and lr.stderr > 0 else None
    sup_pass = (sup_val is not None) and (sup_val > 0)

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 300."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move in the forecast's direction is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the mean unusual move in the forecast's direction is 0 or below."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual 24-bar move in forecast direction",
            "value": sup_val,
            "passed": bool(sup_pass) if sup_val is not None else None,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
