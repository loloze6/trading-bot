import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.range_pos.last_history_value"
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback from prices where the raw value is not recorded
            hi = close.rolling(30, min_periods=30).max()
            lo = close.rolling(30, min_periods=30).min()
            mid = (hi + lo) / 2.0
            price_pos = close - mid
            pos = raw.where(raw.notna(), price_pos)
            active = fc.notna() & (fc != 0)
            situation = pos > 0
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "OLS slope of excess 10-bar forward return on forecast (forecast > 0, non-overlapping grid)"
    threshold = "confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the active bars are long bars with the close above the middle of its 30-day closing range, as the plan's situation requires.",
            "reading": "The situation is read as the component's raw range position (last_history_value) above 0, from prices where not recorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
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
    grid = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast"])

    if len(grid):
        coin_mean = grid.groupby("coin")["ret"].transform("mean")
        grid["excess"] = grid["ret"] - coin_mean
        cases = grid[grid["forecast"].notna() & (grid["forecast"] > 0)]
    else:
        cases = pd.DataFrame(columns=["excess", "forecast"])
    n_cases = int(len(cases))

    slope = None
    tval = None
    if n_cases >= 3 and np.var(cases["forecast"].values) > 0:
        lr = stats.linregress(cases["forecast"].values.astype(float), cases["excess"].values.astype(float))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    mean_ex = float(cases["excess"].mean()) if n_cases > 0 else None
    sup_pass = (mean_ex > 0) if mean_ex is not None else None

    counts = {"grid cases with forecast > 0": n_cases, "grid cases total": int(len(grid))}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation in the forecast), so neither confirm nor reject applies."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean excess return of the forecast > 0 cases is above 0."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the mean excess return is not above 0, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return of forecast > 0 grid cases",
            "value": mean_ex,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The coin's mean 10-bar return is the mean over all grid cells of all its windows, the slope is an OLS fit with intercept, and the plan's 'fewer than 100 cases' rule is treated as a minimum count giving 'not observable'.",
    }
