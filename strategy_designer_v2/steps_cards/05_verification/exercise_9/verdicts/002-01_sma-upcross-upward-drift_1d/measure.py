import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            # Situation: SMA50 above SMA200 (raw spread > 0); expected side: long (forecast > 0)
            agree = active & (sub[RAW] > 0) & (sub["forecast"] > 0)
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of active bars have SMA50 above SMA200 with a long forecast, "
                           "below the 90% needed for the config to match the plan's situation and side."),
            "reading": "Situation taken as raw SMA50-SMA200 spread > 0 with forecast > 0 (long).",
        }

    # ---------- 2. Criterion ----------
    xs = []
    ys = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            if n <= H:
                continue
            # Forward 10-bar return at every bar inside the window
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid_all = fwd[~np.isnan(fwd)]
            if len(valid_all) == 0:
                continue
            drift = float(np.mean(valid_all))  # window's mean 10-bar return (holding drift)
            for p in range(0, n - H, H):
                if np.isnan(fwd[p]) or np.isnan(fc[p]):
                    continue
                xs.append(fc[p])
                ys.append(fwd[p] - drift)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_total = int(len(x))
    n_pos = int((x > 0).sum())
    n_zero = int((x == 0).sum())

    slope = None
    tstat = None
    if n_total >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and lr.stderr > 0:
            tstat = float(lr.slope / lr.stderr)

    # Supporting check
    sup_val = None
    sup_pass = None
    if n_pos > 0 and n_zero > 0:
        share_pos = float(np.mean(y[x > 0] > 0))
        share_zero = float(np.mean(y[x == 0] > 0))
        sup_val = share_pos - share_zero
        sup_pass = bool(sup_val > 0)

    counts = {
        "non-overlapping samples in total": n_total,
        "samples with forecast > 0": n_pos,
    }

    if n_total < 40 or n_pos < 15:
        status = "not observable"
        decided_by = (f"Minimum count not reached: {n_total} non-overlapping samples (need 40) and "
                      f"{n_pos} with forecast > 0 (need 15).")
    elif tstat is None:
        status = "inconclusive"
        decided_by = "The slope's t-statistic could not be computed, so neither confirm nor reject is met."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided_by = f"The slope is positive with t = {tstat:.2f} >= 2."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided_by = f"The slope is negative with t = {tstat:.2f} <= -2: moves after up-crosses reverse."
    else:
        status = "inconclusive"
        decided_by = f"t = {tstat:.2f} lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "OLS slope of forward 10-bar excess return on forecast",
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": "slope positive with t >= 2 confirms; negative with t <= -2 rejects",
        },
        "supporting_check": {
            "name": "share positive excess (forecast > 0) minus share (forecast = 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The holding drift is the mean of all overlapping 10-bar forward returns available in each window, "
                    "samples are bars at positions 0,10,20,... with a full 10-bar return inside the window, the slope t is "
                    "the ordinary OLS t, and the supporting check passes when the forecast>0 share exceeds the forecast=0 share."),
    }
