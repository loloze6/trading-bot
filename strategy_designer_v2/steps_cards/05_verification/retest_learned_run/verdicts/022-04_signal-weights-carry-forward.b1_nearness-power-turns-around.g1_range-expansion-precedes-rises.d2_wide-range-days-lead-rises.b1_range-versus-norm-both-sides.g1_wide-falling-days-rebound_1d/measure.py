import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.range_mult.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            prev = close.shift(1)
            falling = close < prev
            # first row of a window has no prior close inside the window: fall back to the detector's decision
            first_nan = prev.isna()
            falling = falling.where(~first_nan, df["regime"] == "mean_reversion")
            if RAW in df.columns:
                raw = df[RAW].astype(float)
            else:
                raw = pd.Series(np.nan, index=df.index)
            # recompute the range ratio from prices where it is not recorded
            rng = (df["high"] - df["low"]).astype(float)
            raw_px = rng / rng.rolling(30, min_periods=30).mean()
            raw = raw.where(raw.notna(), raw_px)
            active = fc.notna() & (fc != 0)
            agree = active & falling & (
                ((fc > 0) & (raw > 1.0)) | ((fc < 0) & (raw < 1.0))
            )
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation = a falling day (close below prior close, regime column on a window's first row) and the "
               "side is long when its raw range ratio is above 1 (range above its 30-day average) and, for the "
               "graded adaptation, short when below 1; grid cases are regime 'mean_reversion' bars at positions "
               "0,3,6,... of each window, the coin's mean 3-day return is the mean of all its grid returns over all "
               "windows, the slope t is the OLS slope over its standard error, and the top third is the n//3 cases "
               "with the highest forecast.")

    main_name = "t of OLS slope of excess 3-day return on forecast, falling-day grid cases pooled"
    threshold = "confirm if slope t >= 2 with top-third mean excess > 0; reject if slope t <= -2; at least 300 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are falling days with the forecast's "
                           "sign matching the range above (long) or below (short) the 30-day average."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        all_grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_grid_rets.append(r)
                if df["regime"].iloc[i] == "mean_reversion":
                    f = df["forecast"].iloc[i]
                    if pd.notna(f):
                        coin_cases.append((float(f), r))
        if not all_grid_rets:
            continue
        mu = float(np.mean(all_grid_rets))
        for f, r in coin_cases:
            case_rows.append((f, r - mu))

    n_cases = len(case_rows)
    counts = {"falling-day grid cases": n_cases}

    if n_cases < 300:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "top-third forecast mean excess 3-day return", "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Fewer than 300 falling-day grid cases ({n_cases}): no verdict.",
            "reading": reading,
        }

    arr = np.array(case_rows, dtype=float)
    x, y = arr[:, 0], arr[:, 1]
    if np.std(x) == 0:
        slope, t = 0.0, 0.0
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0

    order = np.argsort(-x, kind="mergesort")
    k = n_cases // 3
    top_mean = float(np.mean(y[order[:k]])) if k > 0 else float("nan")
    sup_pass = bool(np.isfinite(top_mean) and top_mean > 0)
    counts["top-third cases"] = int(k)

    if t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t is 2 or more and the top-third mean excess return is positive: confirm."
    elif t <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less: reject."
    elif t >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the top-third mean excess return is 0 or below: inconclusive."
    else:
        status = "inconclusive"
        decided = "Slope t is between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": t,
                         "statistic": {"name": "OLS slope t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "top-third forecast mean excess 3-day return", "value": top_mean,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
