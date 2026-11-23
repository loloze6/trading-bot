import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    FC = "forecast"
    RAW = "debug_info.components.sun_rev.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            ret1 = np.full(len(d), np.nan)
            if len(d) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            is_sun = (d["timestamp"].dt.weekday == 6).to_numpy()
            prepared[coin][w] = (close, fc, raw, ret1, is_sun)

            for i in range(len(d)):
                if fc[i] == 0 or not np.isfinite(fc[i]):
                    continue
                n_active += 1
                if not is_sun[i]:
                    continue
                move = ret1[i] if np.isfinite(ret1[i]) else raw[i]
                if np.isfinite(move) and move != 0 and np.sign(fc[i]) == -np.sign(move):
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    reading = ("Cases are Sunday-stamped bars (UTC weekday 6) with a non-zero forecast and a close two bars later "
               "in the same window; the normal 2-bar drift is the coin's mean 2-bar return on the non-overlapping "
               "grid (positions 0, 2, 4, ...) of all its windows pooled; the slope is ordinary least squares with "
               "an intercept over all coins pooled, with its usual t; the plan's 'fewer than 300 cases' outcome is "
               "reported as 'not observable' per the workflow's minimum-count rule; the situation's side is "
               "against Sunday's one-bar close-to-close return (the raw component value when the previous close "
               "is not in the window).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "pooled OLS slope of 2-bar unusual move on forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of active bars are Sunday bars with a forecast against Sunday's "
                           "move, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in prepared.items():
        rs = []
        for w, (close, fc, raw, ret1, is_sun) in wins.items():
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rs.append(r)
        drift[coin] = float(np.mean(rs)) if rs else np.nan

    # ---------- 3. cases ----------
    xs, ys = [], []
    for coin, wins in prepared.items():
        if not np.isfinite(drift[coin]):
            continue
        for w, (close, fc, raw, ret1, is_sun) in wins.items():
            n = len(close)
            for i in range(n - H):
                if not is_sun[i] or fc[i] == 0 or not np.isfinite(fc[i]):
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                xs.append(fc[i])
                ys.append(r - drift[coin])
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))

    slope, t = None, None
    if n_cases >= 3 and np.var(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0 and np.sum(np.abs(x)) > 0:
        sup_val = float(np.sum(np.abs(x) * np.sign(x) * y) / np.sum(np.abs(x)))
        sup_pass = bool(sup_val > 0)

    main = {"name": "pooled OLS slope of 2-bar unusual move on forecast",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": "slope > 0 with t >= 2 (and check passing) to confirm; slope < 0 with t <= -2 to reject"}
    sup = {"name": "forecast-weighted mean unusual move in forecast direction > 0",
           "value": sup_val, "passed": sup_pass}
    counts = {"Sunday cases": n_cases}

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} Sunday cases, below the plan's minimum of 300."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the forecast-weighted mean unusual move is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: larger, more turbulent Sunday moves continue rather than reverse."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
