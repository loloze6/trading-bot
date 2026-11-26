import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_pos.last_history_value"
    PPV = "debug_info.components.range_pos.post_pipeline_value"

    # ---------- 1. Situation check ----------
    # Situation: choppy profile, i.e. the bars where range_pos is recorded (its regime is active).
    # Expected side: long when the raw range position is above the middle (> 0), short below (< 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(raw) == np.sign(fc)) & (raw != 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of 5-day forward return minus coin mean 5-day return on range_pos post_pipeline_value"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases inside the profile": None},
            "decided_by": ("fewer than 90% of the bars with a nonzero forecast are choppy-profile bars "
                           "(range_pos recorded) whose forecast sign matches the sign of the raw range position"),
            "reading": "the choppy profile is read as the bars where range_pos is recorded, and the expected side as the sign of its raw range position",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            ppv = (pd.to_numeric(df[PPV], errors="coerce").values
                   if PPV in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(ppv[i]):
                    coin_cases.append((ppv[i], r))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for x, r in coin_cases:
            xs.append(float(x))
            ys.append(float(r - mu))

    n_cases = len(xs)
    slope = None
    tval = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {"active bars": int(n_active), "grid cases inside the profile": int(n_cases)}
    reading = ("the choppy profile is the bars where range_pos is recorded and the expected side is the sign of its raw range position; "
               "the grid starts at each window's first row, the coin's mean 5-day return is taken over all its grid returns in all windows, "
               "the slope is a pooled OLS with intercept on all recorded grid bars (including zero values), and its t is slope over its standard error.")

    if n_cases < 100:
        status = "not observable"
        decided_by = f"the pool has {n_cases} grid cases inside the profile, fewer than the plan's minimum of 100"
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "the slope's t could not be computed (no variation in the forecast)"
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "the slope is positive with t >= 2 (confirm rule)"
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "the slope is negative with t <= -2 (reject rule)"
    else:
        status = "inconclusive"
        decided_by = "the slope's t lies between -2 and +2 (inconclusive rule)"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
