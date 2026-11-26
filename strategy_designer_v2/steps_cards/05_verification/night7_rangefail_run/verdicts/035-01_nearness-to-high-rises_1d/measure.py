import numpy as np
import pandas as pd

NEAR_RAW = "debug_info.components.near_high.last_history_value"
OFF_RAW = "debug_info.components.offset.last_history_value"


def _standardise(raw, window=60, min_periods=20):
    # value(t) * 10 / mean(|last `window` raw values|, bar t left out), capped at -20..+20; 0 when that mean is 0.
    # Only the recorded bars are available (warm-up not recorded), so bars with fewer than
    # min_periods recorded past values cannot be rebuilt and are left as NaN.
    raw = pd.to_numeric(raw, errors="coerce")
    m = raw.abs().shift(1).rolling(window, min_periods=min_periods).mean()
    val = raw * 10.0 / m
    val = val.where(m != 0, 0.0)
    val = val.where(m.notna())
    return val.clip(-20, 20)


def _cluster_ols(y, x, groups):
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    g = np.asarray(groups)
    n = len(y)
    if n < 3 or np.nanstd(x) == 0:
        return None, None
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    e = y - X @ beta
    k = X.shape[1]
    meat = np.zeros((k, k))
    uniq, inv = np.unique(g, return_inverse=True)
    G = len(uniq)
    scores = np.zeros((G, k))
    np.add.at(scores, inv, X * e[:, None])
    for s in scores:
        meat += np.outer(s, s)
    if G < 2:
        return float(beta[1]), None
    c = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = c * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    t = beta[1] / se if se and np.isfinite(se) and se > 0 else None
    return float(beta[1]), (float(t) if t is not None else None)


def measure(bars):
    H = 5
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            if NEAR_RAW not in df.columns:
                continue
            near_s = _standardise(df[NEAR_RAW])
            if OFF_RAW in df.columns:
                off_s = _standardise(df[OFF_RAW])
            else:
                off_s = pd.Series(np.nan, index=df.index)
            pred = ((near_s + off_s) / 2.0).clip(-20, 20)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ok = fc.notna() & pred.notna() & (fc != 0)
            n_active += int(ok.sum())
            n_agree += int((np.sign(fc[ok]) == np.sign(pred[ok])).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90 % of the active bars carry the sign of the plan's situation, "
                           "(standardised nearness + standardised +10 offset) / 2, long when nearer the high than usual."
                           if n_active > 0 else
                           "No active bar could be checked against the plan's situation."),
            "reading": "The situation was rebuilt from the recorded raw values with standardise (window 60, min_periods 20) "
                       "inside each window, bars without 20 recorded past values left out of the check.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                r60 = close[t] / close[t - 60] - 1.0 if t >= 60 else np.nan
                rows.append((coin, ts.iloc[t].floor("D"), fc[t], r, r60))
    cells = pd.DataFrame(rows, columns=["coin", "day", "forecast", "ret", "ret60"])
    cells = cells.dropna(subset=["ret"])
    drift = cells.groupby("coin")["ret"].mean()
    cells["excess"] = cells["ret"] - cells["coin"].map(drift)
    main = cells.dropna(subset=["forecast", "excess"])

    n_cases = int(len(main))
    n_days = int(main["day"].nunique())
    slope, t = _cluster_ols(main["excess"], main["forecast"], main["day"].astype(str)) if n_cases > 2 else (None, None)

    sub = main.dropna(subset=["ret60"])
    sub = sub[sub["ret60"] <= 0.10]
    sub_slope, _ = _cluster_ols(sub["excess"], sub["forecast"], sub["day"].astype(str)) if len(sub) > 2 else (None, None)
    sup_pass = (sub_slope > 0) if sub_slope is not None else None

    counts = {"grid cases": n_cases, "distinct days": n_days, "non-rising-market cells": int(len(sub))}

    if n_cases < 500 or n_days < 100:
        status = "not observable"
        decided = (f"The plan needs at least 500 grid cases over at least 100 distinct days; "
                   f"the record has {n_cases} cases over {n_days} days.")
    elif t is None:
        status = "inconclusive"
        decided = "The main slope's t could not be computed."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main slope has t >= 2 and the non-rising-market slope is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The main slope has t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main slope has t >= 2 but the non-rising-market slope is at or below 0."
    else:
        status = "inconclusive"
        decided = "The main slope has t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "slope of 5-bar excess return on forecast, pooled grid cells",
            "value": slope,
            "statistic": {"name": "OLS slope t, clustered by day", "value": t} if t is not None else None,
            "threshold": "confirm t >= 2 (with positive non-rising-market slope); reject t <= -2",
        },
        "supporting_check": {
            "name": "slope on cells with 60-day return <= +10 %",
            "value": sub_slope,
            "passed": (bool(sup_pass) if sup_pass is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("All grid cells with a full 5-bar forward return are regressed with an intercept (including forecast-0 cells), "
                    "the t uses standard errors clustered by calendar day, the normal drift is the coin's mean grid-cell 5-bar return, "
                    "and cells before bar 60 of a window have no 60-day return and are left out of the supporting check."),
    }
