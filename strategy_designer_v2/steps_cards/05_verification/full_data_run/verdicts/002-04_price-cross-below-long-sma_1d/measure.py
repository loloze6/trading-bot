import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.below_ma.last_history_value"

    # ---------- 1. Situation check ----------
    # The situation is "close below its 200-day SMA" (raw distance < 0). The expected side is short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            n_agree += int((act & (d[RAW] < 0) & (d["forecast"] < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the close "
                           "is below its 200-day SMA, so the config does not trade the plan's situation on its side."
                           if n_active > 0 else "No bar has a non-zero forecast, so the situation cannot be checked."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    sup_total, sup_below = 0, 0
    n_nonzero_periods = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            if n <= H:
                continue
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid_all = np.isfinite(fwd)
            if not valid_all.any():
                continue
            mean_ret = float(np.mean(fwd[valid_all]))
            med_ret = float(np.median(fwd[valid_all]))
            fc = df["forecast"].astype(float).values
            for p in range(0, n, H):
                if not (np.isfinite(fwd[p]) and np.isfinite(fc[p])):
                    continue
                xs.append(fc[p])
                ys.append(fwd[p] - mean_ret)
                if fc[p] != 0:
                    n_nonzero_periods += 1
                if fc[p] < 0:
                    sup_total += 1
                    if fwd[p] < med_ret:
                        sup_below += 1

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)

    slope, tstat = None, None
    if len(xs) >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    share = float(sup_below / sup_total) if sup_total > 0 else None
    sup_passed = None if share is None else bool(share > 0.5)

    if n_nonzero_periods < 30:
        status = "inconclusive"
        decided = "There are fewer than 30 non-overlapping 20-bar periods with a non-zero forecast, pooled across coins and windows, so the test is inconclusive."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope on the forecast cannot be estimated, so no t reaches either threshold and the test is inconclusive."
    elif slope > 0 and tstat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope on the forecast is positive with t >= 2 and the supporting share is above 50%, which meets the confirm rule."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2, but the supporting share is not above 50%, so the confirm rule is not fully met and the reject rule is not met either."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope on the forecast is negative with t <= -2, which meets the reject rule (price rises relative to holding the further it sits below the average)."
    else:
        status = "inconclusive"
        decided = "The t on the slope is strictly between -2 and 2, which meets the inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "OLS slope of excess forward 20-bar return (minus window mean) on forecast, pooled, non-overlapping blocks",
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS t of slope", "value": tstat},
            "threshold": "confirm if slope > 0 with t >= 2 (and supporting share > 50%); reject if slope < 0 with t <= -2; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "share of non-overlapping 20-bar periods with forecast < 0 whose forward return is below the coin's window median",
            "value": share,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 20-bar periods with a non-zero forecast": int(n_nonzero_periods),
            "non-overlapping 20-bar periods with forecast below 0": int(sup_total),
            "non-overlapping 20-bar periods in the regression": int(len(xs)),
        },
        "decided_by": decided,
        "reading": ("I used non-overlapping blocks (bars at positions 0, 20, 40, ... of each window, all forecasts including zero) "
                    "with an ordinary OLS t, and I took the coin's mean and median 20-bar return in a window over every bar of that window "
                    "with a complete 20-bar forward return; a positive slope with t >= 2 but a share not above 50% is counted as inconclusive."),
    }
