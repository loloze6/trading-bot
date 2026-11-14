import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross_spread.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: SMA50 above SMA200 (raw spread > 0); expected side: long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            n_agree += int(((sub[RAW] > 0) & (sub["forecast"] > 0) & active).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of forward 10-bar excess return (minus window mean 10-bar return) on forecast"
    threshold = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive; inconclusive if < 40 samples or < 15 with forecast > 0"
    reading = ("The holding drift is each window's mean forward 10-bar return over all its bars with a valid return, "
               "the excess returns are taken on the non-overlapping grid of positions 0, 10, 20, ... of each window, "
               "the t is the OLS slope t (with intercept) on the pooled samples, and the supporting check passes when "
               "the positive share with forecast > 0 exceeds the share with forecast = 0.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars where SMA50 is above SMA200 "
                           "with a long forecast, so the config does not do what the plan's situation states."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            if n <= H:
                continue
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid_all = np.isfinite(fwd)
            if not valid_all.any():
                continue
            drift = float(np.mean(fwd[valid_all]))
            for i in range(0, n, H):
                if np.isfinite(fwd[i]) and np.isfinite(fc[i]):
                    xs.append(fc[i])
                    ys.append(fwd[i] - drift)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_samples = int(len(x))
    n_pos = int((x > 0).sum())
    n_zero = int((x == 0).sum())

    slope = None
    t_stat = None
    if n_samples >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and res.stderr > 0:
            t_stat = float(res.slope / res.stderr)

    # supporting check
    sup_val = None
    sup_pass = None
    if n_pos > 0 and n_zero > 0:
        share_pos = float(np.mean(y[x > 0] > 0))
        share_zero = float(np.mean(y[x == 0] > 0))
        sup_val = share_pos - share_zero
        sup_pass = bool(sup_val > 0)

    if n_samples < 40 or n_pos < 15:
        status = "inconclusive"
        decided_by = "Inconclusive: fewer than 40 non-overlapping samples in total or fewer than 15 samples with forecast > 0."
    elif slope is None or t_stat is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t-statistic cannot be computed, so it is not outside -2 to 2."
    elif slope > 0 and t_stat >= 2:
        status = "confirmed"
        decided_by = "Confirm: the slope is positive with t >= 2."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided_by = "Reject: the slope is negative with t <= -2, meaning moves after up-crosses reverse."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of positive 10-bar excess returns, forecast > 0 minus forecast = 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping samples": n_samples,
            "samples with forecast > 0": n_pos,
        },
        "decided_by": decided_by,
        "reading": reading,
    }
