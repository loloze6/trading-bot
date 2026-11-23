import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.rise5.last_history_value"
    POST = "debug_info.components.rise5.post_pipeline_value"
    MIN_CASES = 200

    # ---------- 1. Situation check: a 5-day rise (raw > 0), long side ----------
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
            # fall back to the 5-bar return from prices inside the window where raw is not recorded
            price_rise = close / close.shift(5) - 1.0
            raw = raw.where(raw.notna(), price_rise)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of 3-bar excess forward return on rise5 forecast (grid cases with forecast > 0)"
    threshold = "confirm: slope > 0 with t >= 2.0 and supporting check passes; reject: slope < 0 with t <= -2.0"
    sup_name = "forecast-weighted mean excess 3-bar return > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases with a positive forecast": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars after a 5-day rise "
                           "(positive raw rise5) with a long forecast, so the config does not follow the plan's "
                           "situation and side."),
            "reading": "The situation is read as a positive raw rise5 value (the 5-day return in usual 5-day moves), side long.",
        }

    # ---------- 2. Drift: each coin's mean 3-bar return over all windows (non-overlapping grid) ----------
    drift = {}
    cases = []
    for coin, wins in bars.items():
        all_rets = []
        per_window = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if POST in df.columns:
                post = pd.to_numeric(df[POST], errors="coerce").to_numpy(dtype=float)
            else:
                post = np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                per_window.append((r, fc[i], post[i]))
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan
        for r, f, p in per_window:
            if np.isfinite(f) and f > 0 and np.isfinite(p) and np.isfinite(drift[coin]):
                cases.append((r - drift[coin], p))

    n_cases = len(cases)
    counts = {"grid cases with a positive forecast": int(n_cases)}

    slope = None
    tval = None
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        y = np.array([c[0] for c in cases], dtype=float)
        x = np.array([c[1] for c in cases], dtype=float)
        if np.std(x) > 0:
            res = stats.linregress(x, y)
            slope = float(res.slope)
            tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None
        sx = float(np.sum(x))
        if sx > 0:
            sup_val = float(np.sum(y * x) / sx)
            sup_pass = bool(sup_val > 0)

    reading = ("Grid cases are bars at positions 0, 3, 6, ... of each window with forecast > 0 and a 3-bar forward "
               "return inside the window; the drift is the coin's mean 3-bar return on that grid over all its windows; "
               "the slope is an OLS regression with intercept, t = slope / its standard error.")

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Fewer than {MIN_CASES} grid cases with a positive forecast ({n_cases}), so the plan's minimum count is not reached."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope or its t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif slope > 0 and tval >= 2.0 and sup_pass:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2.0 and the forecast-weighted mean excess return is above 0."
    elif slope > 0 and tval >= 2.0:
        status = "inconclusive"
        decided_by = "The slope is positive with t >= 2.0 but the supporting check failed, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2.0:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2.0."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2.0 and 2.0."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS t of the slope", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
