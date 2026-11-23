import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.vol_surge.last_history_value"
    PERIOD = 20

    # ---------- 1. Situation check ----------
    # Situation: the log of the day's volume over the mean of the 20 prior days is above 0 (heavier than usual).
    # Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            prior_mean = vol.shift(1).rolling(PERIOD, min_periods=PERIOD).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                recomputed = np.log(vol / prior_mean)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of excess 10-bar forward return on forecast (non-overlapping grid)"
    threshold = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    reading = ("Situation read as raw log volume ratio > 0 with a long forecast (raw recomputed from volume where "
               "missing); grid bars at positions 0,10,20,... of each window with a full 10-bar forward return inside "
               "the window; the coin's mean 10-bar return is the mean over its grid returns of all windows; slope and "
               "t from ordinary least squares with intercept; the plan's minimum of 100 grid cases with forecast > 0 "
               "is treated as a minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on days whose volume "
                           "is above the prior 20-day mean, so the config does not follow the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, fc[t]))
    g = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast"])

    if len(g) > 0:
        coin_mean = g.groupby("coin")["ret"].transform("mean")
        g["excess"] = g["ret"] - coin_mean
        g = g[np.isfinite(g["forecast"]) & np.isfinite(g["excess"])]

    n_grid = int(len(g))
    pos = g[g["forecast"] > 0] if n_grid > 0 else g
    n_pos = int(len(pos))

    slope = None
    tval = None
    if n_grid >= 3 and g["forecast"].nunique() > 1:
        x = g["forecast"].values.astype(float)
        y = g["excess"].values.astype(float)
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    counts = {"independent grid cases with forecast > 0": n_pos,
              "independent grid cases (all)": n_grid}

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold}
    support = {"name": "mean excess 10-bar return on grid bars with forecast > 0",
               "value": sup_val, "passed": sup_pass}

    if n_pos < 100:
        status = "not observable"
        decided = f"Only {n_pos} independent grid cases with forecast > 0, below the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean excess on forecast > 0 bars is above 0."
        else:
            status = "inconclusive"
            decided = ("The slope is positive with t >= 2 but the mean excess on forecast > 0 bars is not above 0, "
                       "which the plan calls inconclusive.")
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
