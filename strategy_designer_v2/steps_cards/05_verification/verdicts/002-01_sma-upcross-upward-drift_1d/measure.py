import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    comp_col = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: SMA50 above SMA200 (raw spread > 0), expected side: long (rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or comp_col not in df.columns:
                continue
            d = df[["forecast", comp_col]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (d[comp_col] > 0) & (d["forecast"] > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of forward 10-bar excess return (vs window mean 10-bar return) on forecast"
    threshold = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping samples": None, "samples with forecast > 0": None},
            "decided_by": ("Fewer than 90% of active bars are bars with SMA50 above SMA200 held long "
                           "(or there are no active bars), so the config does not implement the plan's situation and side."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            rets, fcs = [], []
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if np.isnan(c0) or np.isnan(c1) or np.isnan(f) or c0 == 0:
                    continue
                rets.append(c1 / c0 - 1.0)
                fcs.append(f)
            if len(rets) == 0:
                continue
            rets = np.asarray(rets)
            drift = rets.mean()
            xs.extend(fcs)
            ys.extend(list(rets - drift))

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_total = int(len(x))
    n_pos = int((x > 0).sum())
    n_zero = int((x == 0).sum())

    slope = None
    tstat = None
    if n_total >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and lr.stderr > 0 and np.isfinite(lr.stderr):
            tstat = float(lr.slope / lr.stderr)

    # Supporting check
    sup_value = None
    sup_passed = None
    if n_pos > 0 and n_zero > 0:
        share_pos = float((y[x > 0] > 0).mean())
        share_zero = float((y[x == 0] > 0).mean())
        sup_value = share_pos - share_zero
        sup_passed = bool(sup_value > 0)

    # Decision
    if n_total < 40 or n_pos < 15:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 40 non-overlapping samples in total or fewer than 15 "
                      "samples with forecast > 0.")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t-statistic cannot be computed, so t is not outside -2..2."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided_by = "Confirm: the slope is positive with t >= 2."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided_by = "Reject: the slope is negative with t <= -2, so moves after up-crosses reverse."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of positive excess returns, forecast > 0 minus forecast = 0",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping samples": n_total,
            "samples with forecast > 0": n_pos,
        },
        "decided_by": decided_by,
        "reading": ("Samples are the bars at positions 0, 10, 20, ... of each window with a full 10-bar forward "
                    "return inside the window, the holding drift is the mean of those same non-overlapping 10-bar "
                    "returns in that window, the slope's t is the ordinary OLS slope / standard error, and the "
                    "supporting check passes when the forecast > 0 share exceeds the forecast = 0 share."),
    }
