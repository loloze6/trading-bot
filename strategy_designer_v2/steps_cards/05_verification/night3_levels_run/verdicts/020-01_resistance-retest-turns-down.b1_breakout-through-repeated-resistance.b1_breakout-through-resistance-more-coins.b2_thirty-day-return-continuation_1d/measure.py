import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.ret30.last_history_value"

    # ---------- 1. Situation check: forecast sign must follow the sign of the 30-day return ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the component is not recorded, recompute the 30-bar return from prices (inside the window)
            recomputed = close / close.shift(30) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(raw) == np.sign(fc)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "OLS slope of coin-excess 10-bar forward return on forecast (non-overlapping grid)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars on the situation's side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast have a forecast whose sign matches "
                           "the sign of the coin's 30-day return (long after a rise, short after a fall), "
                           "as the plan's Fidelity requires."),
            "reading": "The situation's side is taken as the sign of the raw 30-day return; bars where it cannot be read count as not agreeing.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
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
                rows.append((coin, w, c1 / c0 - 1.0, fc[i]))

    g = pd.DataFrame(rows, columns=["coin", "window", "fwd", "forecast"])
    if len(g):
        coin_mean = g.groupby("coin")["fwd"].transform("mean")
        g["excess"] = g["fwd"] - coin_mean
        use = g[g["forecast"].notna() & g["excess"].notna()]
    else:
        use = g
    n_cases = int(len(use))
    counts = {"grid cases with a recorded forecast": n_cases}

    slope = None
    tval = None
    if n_cases >= 3 and use["forecast"].nunique() > 1:
        res = stats.linregress(use["forecast"].values.astype(float), use["excess"].values.astype(float))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    if n_cases < 300:
        status = "not observable"
        decided_by = f"Only {n_cases} grid cases with a recorded forecast, fewer than the plan's minimum of 300."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no variation in the forecast), so no rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "Confirm rule met: the slope is positive with t >= 2."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "Reject rule met: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive rule met: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Grid bars are positions 0, 10, 20, ... of each window with a 10-bar forward return inside the window; "
                    "the coin's mean is the mean of these grid returns over all its windows; every grid bar with a non-missing "
                    "forecast (zeros included) enters an OLS regression with an intercept; and the plan's 300-case minimum "
                    "is applied as 'not observable'."),
    }
