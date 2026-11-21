import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    TEN, KIJ, SEN, DISP = 9, 26, 52, 26
    SLOPE_COL = "debug_info.components.slope_size.last_history_value"
    MIN_CASES = 30

    def cloud_edges(df):
        hi = df["high"].astype(float)
        lo = df["low"].astype(float)
        tenkan = (hi.rolling(TEN, min_periods=TEN).max() + lo.rolling(TEN, min_periods=TEN).min()) / 2.0
        kijun = (hi.rolling(KIJ, min_periods=KIJ).max() + lo.rolling(KIJ, min_periods=KIJ).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(DISP)
        span_b = ((hi.rolling(SEN, min_periods=SEN).max() + lo.rolling(SEN, min_periods=SEN).min()) / 2.0).shift(DISP)
        lower = np.minimum(span_a, span_b)
        mid = (span_a + span_b) / 2.0
        return lower, mid

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = df["close"].astype(float)
            lower, mid = cloud_edges(df)
            below = close < lower
            below_known = lower.notna()
            if SLOPE_COL in df.columns:
                slope = pd.to_numeric(df[SLOPE_COL], errors="coerce")
            else:
                slope = pd.Series(np.nan, index=df.index)
            slope_re = mid - mid.shift(H)
            slope = slope.where(slope.notna(), slope_re)
            active = fc.notna() & (fc != 0)
            verifiable = active & below_known & slope.notna()
            n_active += int(verifiable.sum())
            ok = verifiable & below & (slope < 0) & (fc < 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean of -forecast/10 x (26-bar forward return minus coin's mean 26-bar return), forecast<0, 26-bar grid"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting difference < 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Cloud position recomputed from each window's own prices (cloud at t = spans computed at t-26, below = close under "
               "the lower span), cloud-slope sign taken from the recorded slope_size raw value (recomputed from prices if missing), "
               "and only active bars where both are computable enter the agreement; drift is the coin's mean 26-bar return on the "
               "non-overlapping grid of all its windows; median split is strict (cases equal to the median left out).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"verifiable active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars with the close below the cloud and a falling 26-bar "
                           "cloud slope, so the forecast does not fire on the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    gains, excess, absf = [], [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n and close[i] > 0 and np.isfinite(close[i]) and np.isfinite(close[i + H]):
                    grid_rows.append((close[i + H] / close[i] - 1.0, fc[i]))
        if not grid_rows:
            continue
        rets = np.array([r for r, _ in grid_rows], dtype=float)
        drift = float(np.mean(rets))
        for r, f in grid_rows:
            if np.isfinite(f) and f < 0:
                ex = r - drift
                gains.append(-f / 10.0 * ex)
                excess.append(ex)
                absf.append(abs(f))

    gains = np.array(gains, dtype=float)
    excess = np.array(excess, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(gains))

    mean_gain = float(np.mean(gains)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(gains, ddof=1))
        if sd > 0:
            t_val = float(mean_gain / (sd / np.sqrt(n_cases)))

    diff = None
    n_hi = n_lo = 0
    if n_cases > 0:
        med = float(np.median(absf))
        hi_m = absf > med
        lo_m = absf < med
        n_hi, n_lo = int(hi_m.sum()), int(lo_m.sum())
        if n_hi > 0 and n_lo > 0:
            diff = float(np.mean(excess[hi_m]) - np.mean(excess[lo_m]))
    sup_pass = None if diff is None else bool(diff < 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases with forecast below 0, fewer than the plan's minimum of 30."
    elif t_val is not None and mean_gain > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Main mean positive with t >= 2 over at least 30 cases and supporting difference below 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "Confirming t, but the supporting difference is 0 or above (or not computable), which the plan makes inconclusive."
    elif t_val is not None and mean_gain < 0 and t_val <= -2:
        status = "rejected"
        decided = "Main mean negative with t <= -2 over at least 30 cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t of the main mean lies between -2 and 2 (or is undefined), which the plan makes inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_gain,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return, |forecast| above median minus below median, must be < 0",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping cases": n_cases,
            "cases above median": n_hi,
            "cases below median": n_lo,
        },
        "decided_by": decided,
        "reading": reading,
    }
