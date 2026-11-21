import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    RAW = "debug_info.components.cloud_pos.last_history_value"

    # ---------- 1. Situation check ----------
    # Close above the cloud top means a long, close below means a short.
    # So the expected sign of the forecast is the sign of the raw distance.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            exp_side = np.sign(raw)
            agree = active & raw.notna() & (exp_side != 0) & (np.sign(f) == exp_side)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of slope of pooled 26-bar forward excess return (minus coin drift) on forecast"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 non-overlapping cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": None},
            "decided_by": ("Fewer than 90% of active bars have a forecast sign equal to the sign of the "
                           "close's distance from the cloud top (long above, short below), as the Fidelity requires."),
            "reading": "A bar with a missing or zero raw distance counts as not matching the situation.",
        }

    # ---------- 2. Criterion ----------
    # Grid bars at positions 0, 26, 52, ... of each window.
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[i]))

    data = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(data):
        # Normal drift: the coin's mean 26-bar return over all its windows.
        drift = data.groupby("coin")["ret"].transform("mean")
        data["ex"] = data["ret"] - drift
        data = data[np.isfinite(data["fc"]) & np.isfinite(data["ex"])]
    n_cases = int(len(data))

    slope = None
    tval = None
    if n_cases >= 3 and float(np.std(data["fc"].to_numpy())) > 0:
        x = data["fc"].to_numpy(dtype=float)
        y = data["ex"].to_numpy(dtype=float)
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and res.stderr > 0:
            tval = float(res.slope / res.stderr)

    counts = {"non-overlapping cases": n_cases}
    reading = ("Ordinary least squares with an intercept, pooled over all coins, on every grid bar with a 26-bar "
               "return inside its window (bars with forecast 0 included); drift is the coin's mean of these grid "
               "returns over all windows.")
    stat = {"name": "OLS t of slope", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": tval, "statistic": stat, "threshold": threshold}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {tval:.2f} >= 2 on {n_cases} non-overlapping cases."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {tval:.2f} <= -2 on {n_cases} non-overlapping cases."
    else:
        status = "inconclusive"
        decided = f"t = {tval:.2f} lies between -2 and 2 on {n_cases} non-overlapping cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
