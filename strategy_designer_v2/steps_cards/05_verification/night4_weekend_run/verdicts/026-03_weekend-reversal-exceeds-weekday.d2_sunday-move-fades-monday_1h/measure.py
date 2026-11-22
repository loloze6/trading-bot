import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 24
    LB = 24
    raw_col = "debug_info.components.sunday_ret.last_history_value"

    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, forecast, fwd_return)
    drift_samples = {}  # coin -> list of non-overlapping 24-bar returns

    for coin, wins in bars.items():
        drift_samples.setdefault(coin, [])
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df["timestamp"])
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)

            # bar whose close is Monday 00:00 UTC: bar starting Sunday 23:00 UTC
            close_time = ts + pd.Timedelta(hours=1)
            is_sit = ((close_time.dt.weekday == 0) & (close_time.dt.hour == 0)).values

            # Sunday's 24-bar return: raw component value where recorded, else from prices
            ret_px = (close / close.shift(LB) - 1.0) * 100.0
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce").astype(float)
                sun_ret = raw.where(raw.notna(), ret_px)
            else:
                sun_ret = ret_px
            expected_side = -np.sign(sun_ret.values)

            active = fc.values != 0
            n_active += int(active.sum())
            agree = active & is_sit & (np.sign(fc.values) == expected_side) & (expected_side != 0)
            n_agree += int(agree.sum())

            # forward 24-bar return inside the window
            fwd = (close.shift(-H) / close - 1.0).values

            # drift grid: positions 0, H, 2H, ... of each window
            grid = np.arange(0, len(df), H)
            g = fwd[grid]
            drift_samples[coin].extend([float(x) for x in g if np.isfinite(x)])

            # cases: situation bars with nonzero forecast (one per week, non-overlapping)
            idx = np.where(is_sit & active)[0]
            for i in idx:
                if np.isfinite(fwd[i]):
                    case_rows.append((coin, float(fc.values[i]), float(fwd[i])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "OLS slope of next-24-bar return minus coin drift on the Monday 00:00 forecast"
    thr = "confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2"
    reading = ("Situation bars are the bars starting Sunday 23:00 UTC (closing Monday 00:00), Sunday's return is the "
               "recorded raw component value (recomputed from 24-row prices where missing), the regression is ordinary "
               "least squares with an intercept, the drift is each coin's mean 24-bar return on the 0, 24, 48, ... row "
               "grid of all its windows, and fewer than 300 cases is reported as not observable as the instructions require.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"Monday cases with a nonzero forecast": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active (nonzero-forecast) bars are Monday 00:00-close bars with a "
                           "forecast opposite to Sunday's 24-bar return (agreement %.3f)." % agreement),
            "reading": reading,
        }

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}
    xs, ys = [], []
    for coin, f, r in case_rows:
        d = drift.get(coin, np.nan)
        if np.isfinite(d):
            xs.append(f)
            ys.append(r - d)
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    n = int(len(xs))
    counts = {"Monday cases with a nonzero forecast": n}

    slope = None
    tval = None
    if n >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup = float(np.mean(np.sign(xs) * ys)) if n > 0 else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "t of the OLS slope", "value": tval} if tval is not None else None),
            "threshold": thr}
    sup_pass = (sup > 0) if sup is not None else None
    supporting = {"name": "mean of sign(forecast) x (next-24-bar return minus drift)",
                  "value": sup, "passed": sup_pass}

    if n < 300:
        status = "not observable"
        decided = "Fewer than 300 Monday cases with a nonzero forecast (%d), the plan's minimum count." % n
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it meets neither the confirm nor the reject rule."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting mean is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming slope (positive, t >= 2) whose supporting mean is not above 0 is inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
