import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    FC = "forecast"
    RAW = "debug_info.components.vsfall.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan: the situation is a one-day fall, and the expected side is long (a rebound, i.e. a rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce")
            # One-bar return, computed inside the window only.
            ret1 = close / close.shift(1) - 1.0
            active = fc.notna() & (fc != 0) & ret1.notna()
            situ = ret1 < 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("Situation taken as a negative one-bar close-to-close return, computed from prices within "
               "each window (each window's first bar has no prior close and is left out), and the expected "
               "side as forecast > 0; the coin's mean 3-bar return is the mean over its non-overlapping grid "
               "bars pooled across all windows; the slope t is the OLS slope over its standard error on the "
               "pooled grid; the supporting check is the sign of the mean excess return on grid bars with "
               "forecast > 0; the plan's minimum of 200 grid bars with forecast > 0 maps to 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are one-day falls carrying a "
                           "long forecast: the config's standardised, negated and clipped signal does not "
                           "follow the plan's situation of a one-day fall on the long side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy()
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0 and np.isfinite(fc[i])):
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[i]))

    g = pd.DataFrame(rows, columns=["coin", "r", "f"])
    if len(g) > 0:
        g["ex"] = g["r"] - g.groupby("coin")["r"].transform("mean")
    else:
        g["ex"] = []

    pos = g[g["f"] > 0] if len(g) else g
    n_grid = int(len(g))
    n_pos = int(len(pos))
    counts = {"grid bars with forecast > 0": n_pos, "grid bars": n_grid}

    slope = None
    tval = None
    if n_grid >= 3 and np.nanstd(g["f"].to_numpy()) > 0:
        lr = stats.linregress(g["f"].to_numpy(), g["ex"].to_numpy())
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(pos["ex"].mean()) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {
        "name": "OLS slope of excess 3-bar forward return on forecast",
        "value": slope,
        "statistic": {"name": "t of OLS slope", "value": tval} if tval is not None else None,
        "threshold": "confirm if t >= 2 with supporting check passed; reject if t <= -2; otherwise inconclusive",
    }
    support = {"name": "mean excess 3-bar return on grid bars with forecast > 0",
               "value": sup_val, "passed": sup_pass}

    if n_pos < 200:
        status = "not observable"
        decided = f"Only {n_pos} grid bars have forecast > 0, below the plan's minimum of 200."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess 3-bar return on forecast > 0 grid bars is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger volatility-scaled falls are followed by smaller excess 3-bar returns."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more, but the supporting check fails, which the plan calls inconclusive."
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
