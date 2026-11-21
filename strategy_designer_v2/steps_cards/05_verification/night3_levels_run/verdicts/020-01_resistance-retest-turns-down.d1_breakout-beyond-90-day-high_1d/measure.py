import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.breakout_dist.last_history_value"
    PPV = "debug_info.components.breakout_dist.post_pipeline_value"
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    # Situation: close above the highest close of the previous 90 days (bar t excluded); side: long.
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            # where the raw value is missing, recompute it from the prices (needs 90 prior bars in the window)
            prior_high = pd.Series(close).shift(1).rolling(90, min_periods=90).max().to_numpy()
            recomputed = (close / prior_high - 1.0) * 100.0
            raw_full = np.where(np.isnan(raw), recomputed, raw)
            for i in range(len(df)):
                f = fc[i]
                if np.isnan(f) or f == 0:
                    continue
                n_active += 1
                r = raw_full[i]
                if (not np.isnan(r)) and r > 0 and f > 0:
                    n_agree += 1

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "breakout cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close stands "
                           "above the highest close of the previous 90 days, which the plan's situation requires."),
            "reading": "The situation is the raw breakout distance above 0 (recomputed from closes where missing) with a positive forecast.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin], key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if PPV in df.columns:
                ppv = pd.to_numeric(df[PPV], errors="coerce").to_numpy(dtype=float)
            else:
                ppv = np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                ret = c1 / c0 - 1.0
                grid_rets.append(ret)
                f = fc[i]
                if not np.isnan(f) and f > 0:
                    x = ppv[i] if not np.isnan(ppv[i]) else f
                    coin_cases.append((x, ret))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for x, r in coin_cases:
            xs.append(float(x))
            ys.append(r - drift)

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.ptp(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        if lr.stderr is not None and lr.stderr > 0 and np.isfinite(lr.stderr):
            t_slope = float(lr.slope / lr.stderr)
    mean_dr = float(np.mean(ys)) if n_cases > 0 else None
    support_pass = (mean_dr > 0) if mean_dr is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} breakout cases on the non-overlapping 5-bar grid, fewer than the plan's minimum of 30."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed (no variation in the forecast across cases), so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided_by = "The slope t is 2 or more with at least 30 cases and the mean drift-removed 5-bar return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope t is -2 or less with at least 30 cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope t is 2 or more but the mean drift-removed 5-bar return is 0 or below."
    else:
        status = "inconclusive"
        decided_by = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)},
        "main_measure": {
            "name": "slope of drift-removed 5-bar return on forecast (pooled breakout cases)",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": "confirm if slope t >= 2 (with supporting check), reject if slope t <= -2, at least 30 cases",
        },
        "supporting_check": {
            "name": "mean drift-removed 5-bar return of breakout cases above 0",
            "value": mean_dr,
            "passed": (bool(support_pass) if support_pass is not None else None),
        },
        "counts": {"breakout cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided_by,
        "reading": ("Grid bars are positions 0,5,10,... of each window with a full 5-bar return inside it; the coin's mean "
                    "5-bar return is the mean over all its grid returns across windows; the regressor is post_pipeline_value "
                    "(forecast where it is missing); the situation check uses the raw distance above 0 with a positive forecast."),
    }
