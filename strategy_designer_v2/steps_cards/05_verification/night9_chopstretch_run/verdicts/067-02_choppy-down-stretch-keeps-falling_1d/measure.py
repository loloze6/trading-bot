import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.stretch_below.last_history_value"

    # ---------- 1. situation check: close below its 20-day SMA, expected side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # fallback from prices (sign of distance = sign of close - SMA20), inside the window only
            sma = close.rolling(20, min_periods=20).mean()
            dist_px = close - sma
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                dist = raw.where(raw.notna(), dist_px)
            else:
                dist = dist_px
            active = fc.notna() & (fc != 0)
            agree = active & (dist < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "slope of 10-bar forward return net of drift on -forecast (grid, forecast < 0)"
    threshold = "confirm if slope t <= -2 (with supporting check); reject if slope t >= +2; else inconclusive"
    sup_name = "mean unusual move in the short direction (-(10-bar return - drift)) > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short bars with the close below "
                           "its 20-day average, as the Fidelity's situation and side require"
                           if n_active > 0 else "no bar has a non-zero forecast"),
            "reading": "situation = raw stretch_below value < 0 (close below its 20-day SMA), recomputed from closes where missing; side = short (forecast < 0).",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rows = []
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                grid_rows.append((r, fc[i]))
        if not all_rets:
            continue
        drift = float(np.mean(all_rets))
        for r, f in grid_rows:
            if np.isfinite(f) and f < 0:
                xs.append(-f)
                ys.append(r - drift)

    n_cases = len(xs)
    counts = {"grid cases with forecast < 0": n_cases}
    reading = ("Situation = raw stretch_below < 0 with forecast < 0; grid = bars 0,10,20,... of each window with a "
               "full 10-bar forward return; drift = coin's mean 10-bar return on that grid over all its windows; "
               "pooled OLS across coins and windows with the ordinary slope t; fewer than 30 cases is reported as not observable.")

    if n_cases < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": (float(-np.mean(ys)) if ys else None), "passed": None},
            "counts": counts,
            "decided_by": "fewer than 30 grid cases with forecast < 0 across all coins and windows",
            "reading": reading,
        }

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    sup_val = float(np.mean(-y))
    sup_pass = bool(sup_val > 0)

    if np.std(x) == 0:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
            "counts": counts,
            "decided_by": "the forecast's size does not vary across cases, so no slope t can be read (between -2 and +2 by default)",
            "reading": reading,
        }

    lr = stats.linregress(x, y)
    slope = float(lr.slope)
    t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else (np.inf if slope > 0 else -np.inf)
    t = float(t)

    if t <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "the slope is negative with t <= -2 and the mean unusual move in the short direction is above 0"
        else:
            status = "inconclusive"
            decided = "the slope is negative with t <= -2 but the supporting check failed (mean short-direction unusual move not above 0)"
    elif t >= 2:
        status = "rejected"
        decided = "the slope is positive with t >= +2: a larger stretch below the average is followed by a larger rise (reversion)"
    else:
        status = "inconclusive"
        decided = "the slope t lies between -2 and +2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
