import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 1
    MIN_CASES = 100
    COMP = "debug_info.components.agit.last_history_value"

    # ---------- per coin: mean daily return over all its windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            r = (c.shift(-H) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_active_checkable = 0
    n_agree = 0
    xs, ys = [], []

    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            fc = d["forecast"].astype(float)

            # regime detector components, recomputed from prices inside the window
            up = (c / c.shift(1) - 1.0) * 100.0                     # 1-day evolution
            hh = hi.rolling(20, min_periods=20).max()               # bar included
            ll = lo.rolling(20, min_periods=20).min()
            rngw = hh - ll
            pos = 2.0 * (c - ll) / rngw.replace(0, np.nan) - 1.0     # Donchian position
            trend = (c / c.shift(60) - 1.0) * 100.0                  # 60-day evolution (profile)

            checkable = up.notna() & pos.notna() & trend.notna()
            situation = (trend < -10.0) & (up > 0.0) & (pos < -0.6)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ac = active & checkable
            n_active_checkable += int(ac.sum())
            n_agree += int((ac & situation & (fc < 0)).sum())

            # cases: forecast < 0, next-day short-direction excess return
            fwd = c.shift(-H) / c - 1.0
            y = -(fwd - mu)
            mask = (fc < 0) & y.notna() & np.isfinite(y)
            xs.append(np.abs(fc[mask].values))
            ys.append(y[mask].values)

    agreement = (n_agree / n_active_checkable) if n_active_checkable > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Bars whose 60-day, 20-day or 1-day evolution cannot be recomputed inside their window "
               "(no warm-up recorded) are left out of the situation check, the falling profile is read as a "
               "60-bar price evolution in percent below -10 (the config veto), and every bar is a case grid "
               "cell since the horizon is 1 bar; the plan's 'fewer than 100 cases' is applied as a minimum count.")

    main_name = "OLS slope of next-day short-direction excess return on abs(forecast)"
    threshold = "confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checkable": int(n_active_checkable)},
            "decided_by": ("Fewer than 90% of the active (non-zero forecast) bars are falling-market bars "
                           "(60-day evolution < -10%) that closed up on the day in the lower fifth of the "
                           "20-day range with a short forecast."),
            "reading": reading,
        }

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(x.size)

    slope = None
    t = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    mean_ex = float(np.mean(y)) if n > 0 else None
    sup_pass = None if mean_ex is None else bool(mean_ex > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases (forecast < 0), fewer than the plan's minimum of 100."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in forecast size)."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean short-direction excess return is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the mean short-direction excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t is None else {"name": "OLS slope t", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean short-direction next-day excess return > 0",
            "value": mean_ex,
            "passed": sup_pass,
        },
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": reading,
    }
