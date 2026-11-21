import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.mom28.last_history_value"
    POST = "debug_info.components.mom28.post_pipeline_value"
    PERIOD = 28

    # ---------- 1. Situation check ----------
    # Situation: the coin's 28-day return; the expected side is long when it is positive
    # and short when it is negative (graded: higher return means higher forecast).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce") if "forecast" in df.columns else pd.Series(np.nan, index=df.index)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Fall back to the price-based 28-bar return, inside the window, where the raw value is not recorded
            price_ret = close / close.shift(PERIOD) - 1.0
            raw = raw.where(raw.notna(), price_ret)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(raw) == np.sign(fc)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 5-day excess return on the mom28 post-pipeline forecast, pooled"
    threshold = "confirm if t >= 2 (with top-minus-bottom fifth > 0); reject if t <= -2; otherwise inconclusive; at least 300 grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases with a recorded forecast": None},
            "decided_by": "Fewer than 90% of the active bars have a forecast whose sign matches the sign of the coin's 28-day return, so the config does not take the long-on-rise / short-on-fall side the Fidelity states.",
            "reading": "The situation's side is the sign of the raw 28-bar return (last_history_value, or the in-window price return where missing); a bar with a zero raw return and a non-zero forecast counts as disagreeing.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            post = pd.to_numeric(df[POST], errors="coerce").to_numpy() if POST in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, close[i + H] / close[i] - 1.0, post[i]))

    g = pd.DataFrame(rows, columns=["coin", "window", "fwd", "fc"])
    if len(g) > 0:
        coin_mean = g.groupby("coin")["fwd"].mean()
        g["excess"] = g["fwd"] - g["coin"].map(coin_mean)
    else:
        g["excess"] = []
    s = g[g["fc"].notna() & g["excess"].notna()].reset_index(drop=True)
    n_cases = int(len(s))

    slope = None
    t_val = None
    if n_cases >= 3 and np.nanstd(s["fc"].to_numpy()) > 0:
        lr = stats.linregress(s["fc"].to_numpy(dtype=float), s["excess"].to_numpy(dtype=float))
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    diff = None
    n_top = n_bot = 0
    if n_cases >= 5:
        order = np.argsort(s["fc"].to_numpy(dtype=float), kind="mergesort")
        k = n_cases // 5
        if k > 0:
            bot = s.iloc[order[:k]]
            top = s.iloc[order[-k:]]
            n_top, n_bot = int(len(top)), int(len(bot))
            diff = float(top["excess"].mean() - bot["excess"].mean())
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {
        "grid cases with a recorded forecast": n_cases,
        "top fifth cases": n_top,
        "bottom fifth cases": n_bot,
    }

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} independent grid cases with a recorded forecast, below the plan's minimum of 300."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom-fifth excess return difference is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom-fifth difference is 0 or less, which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 5-day return, top fifth minus bottom fifth of forecasts",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid cases are window rows 0, 5, 10, ... with a full in-window 5-bar forward return; the coin's mean is taken over all its grid cases in all windows; the top and bottom fifths are the floor(n/5) highest and lowest forecasts after a stable sort; the plan's 'fewer than 300 is inconclusive' is reported as 'not observable' as the workflow requires.",
    }
