import numpy as np
import pandas as pd


def measure(bars):
    H = 6
    RNG_COL = "debug_info.components.range_excess.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            hl = (df["high"].astype(float) - df["low"].astype(float))
            rng_px = hl / hl.rolling(30, min_periods=30).mean()
            if RNG_COL in df.columns:
                rng = df[RNG_COL].astype(float).where(df[RNG_COL].notna(), rng_px)
            else:
                rng = rng_px
            ret30 = close / close.shift(30) - 1.0
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            known = active & rng.notna() & ret30.notna()
            sit = (rng > 1.0) & (ret30 > 0.0)
            agree = known & sit & (fc > 0)
            n_active += int(known.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "forecast-weighted mean excess 6-day return over coin drift (positive-forecast grid bars)"
    thr = "confirm: > 0 with t >= 2 and supporting check passes; reject: < 0 with t <= -2; else inconclusive; at least 100 positive-forecast grid cases"
    sup_name = "mean excess 6-day return, upper minus lower half at median forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are bars where the day's range exceeds its 30-day mean range with a positive 30-day return and a positive (long) forecast.",
            "reading": "Range ratio taken from the recorded range_excess raw value (recomputed from prices where missing), 30-day return from closes within the window; active bars where either cannot be computed are left out.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H])):
                    continue
                r = close[t + H] / close[t] - 1.0
                rows.append((coin, w, r, fc[t]))
    g = pd.DataFrame(rows, columns=["coin", "w", "r", "f"])
    drift = g.groupby("coin")["r"].mean()
    g["ex"] = g["r"] - g["coin"].map(drift)
    pos = g[(g["f"] > 0) & g["f"].notna() & g["ex"].notna()].copy()
    n_cases = int(len(pos))
    counts = {"positive-forecast grid cases": n_cases}

    wm = None
    tval = None
    if n_cases >= 2:
        f = pos["f"].values
        ex = pos["ex"].values
        wm = float(np.sum(f * ex) / np.sum(f))
        y = f * ex / np.mean(f)
        sd = np.std(y, ddof=1)
        tval = float(np.mean(y) / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = float(np.median(pos["f"].values))
        up = pos[pos["f"] > med]["ex"]
        lo = pos[pos["f"] <= med]["ex"]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} positive-forecast grid cases, below the plan's minimum of 100."
    elif wm is None or tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif wm > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Forecast-weighted mean excess return above 0 with t >= 2 and the upper-minus-lower half difference above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (upper minus lower half above 0) fails, which the plan calls inconclusive."
    elif wm < 0 and tval <= -2:
        status = "rejected"
        decided = "Forecast-weighted mean excess return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": wm,
            "statistic": {"name": "t of the forecast-weighted mean", "value": tval} if tval is not None else None,
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid bars at positions 0, 6, 12, ... of each window with a full 6-bar return inside it; the coin's drift is the mean of all its grid 6-day returns over all windows; the t of the weighted mean is the ordinary t of f*excess/mean(f); the median split puts forecasts above the median in the upper half and the rest in the lower.",
    }
