import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.below_ma.last_history_value"

    # ---------- 1. Situation check ----------
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
            # situation: close below the 200-day SMA (raw distance < 0), expected side short
            agree = active & raw.notna() & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess forward 20-bar return (minus coin-window mean 20-bar return) on forecast, pooled, non-overlapping 20-bar blocks"
    threshold = "confirm if slope > 0 with t >= 2 (and supporting share > 50%); reject if slope < 0 with t <= -2; inconclusive otherwise or if fewer than 30 non-overlapping 20-bar periods with non-zero forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are short bars with the close below its 200-day SMA, as the plan's situation requires.",
            "reading": "Situation taken as the raw component value (distance from the 200-day SMA) below zero, with a short (negative) forecast.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    n_nonzero_periods = 0
    n_short_periods = 0
    n_below_median = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid_fwd = fwd[np.isfinite(fwd)]
            if len(valid_fwd) == 0:
                continue
            mean_ret = float(np.mean(valid_fwd))
            med_ret = float(np.median(valid_fwd))
            for i in range(0, n, H):
                r = fwd[i]
                f = fc[i]
                if not (np.isfinite(r) and np.isfinite(f)):
                    continue
                xs.append(f)
                ys.append(r - mean_ret)
                if f != 0:
                    n_nonzero_periods += 1
                if f < 0:
                    n_short_periods += 1
                    if r < med_ret:
                        n_below_median += 1

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    slope, tstat = None, None
    if len(xs) >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    share = float(n_below_median / n_short_periods) if n_short_periods > 0 else None
    sup_passed = None if share is None else bool(share > 0.5)

    if n_nonzero_periods < 30:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping 20-bar periods with a non-zero forecast, pooled across coins and windows, so the test is inconclusive."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t-statistic cannot be computed, so no confirm or reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope on the forecast is positive with t >= 2 and the supporting share is above 50%."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope on the forecast is negative with t <= -2: price rises relative to holding the further below the average."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting share is not above 50%, so the confirm rule is not fully met."
    else:
        status = "inconclusive"
        decided = "The slope's t lies strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS t of slope (non-overlapping 20-bar blocks)", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of non-overlapping 20-bar short periods with forward return below coin-window median 20-bar return",
            "value": share,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 20-bar periods with non-zero forecast": int(n_nonzero_periods),
            "non-overlapping 20-bar periods with forecast below 0": int(n_short_periods),
            "non-overlapping 20-bar periods in regression": int(len(xs)),
        },
        "decided_by": decided,
        "reading": "The regression uses all bars (including zero forecast) on the 0, 20, 40, ... grid of each window, with the coin's mean and median 20-bar return taken over all overlapping forward returns in that window, and a supporting share not above 50% blocks confirmation.",
    }
