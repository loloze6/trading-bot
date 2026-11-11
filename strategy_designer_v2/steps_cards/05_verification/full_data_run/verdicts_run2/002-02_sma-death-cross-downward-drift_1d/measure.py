import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RAW = "debug_info.components.sma_cross_down.last_history_value"
    MAIN_NAME = "slope of 20-bar excess log return on forecast (non-overlapping blocks)"
    THRESH = "confirm if slope > 0 with coin-clustered t >= 2; reject if slope < 0 with t <= -2; else inconclusive; at least 100 blocks with forecast < 0"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or RAW not in df.columns or "forecast" not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            # situation: 50-day SMA below 200-day SMA (raw spread < 0); expected side: short
            ok = act & (d[RAW] < 0) & (d["forecast"] < 0)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": MAIN_NAME, "value": None, "statistic": None, "threshold": THRESH},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("No active bars in the record, so the config does not take the plan's short position while the 50-day SMA is below the 200-day SMA."
                           if n_active == 0 else
                           f"Only {agreement:.1%} of active bars are short while the 50-day SMA is below the 200-day SMA, below the required 90%."),
            "reading": "Situation taken as raw SMA spread (last_history_value) < 0 with the expected side short (forecast < 0).",
        }

    # ---------- 2. criterion ----------
    rows = []  # (coin, forecast, excess)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            blk = []
            for t in range(0, n - H, H):
                c0, c1, f0 = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f0)) or c0 <= 0 or c1 <= 0:
                    continue
                blk.append((f0, np.log(c1 / c0)))
            if not blk:
                continue
            arr = np.array(blk)
            mean_r = arr[:, 1].mean()
            for f0, r in arr:
                rows.append((coin, float(f0), float(r - mean_r)))

    n_blocks = len(rows)
    coins = np.array([r[0] for r in rows]) if rows else np.array([])
    f = np.array([r[1] for r in rows], dtype=float)
    y = np.array([r[2] for r in rows], dtype=float)
    n_short = int((f < 0).sum()) if n_blocks else 0
    n_coins = int(len(np.unique(coins))) if n_blocks else 0

    slope, tstat = None, None
    if n_blocks >= 3 and np.var(f) > 0 and n_coins >= 2:
        X = np.column_stack([np.ones(n_blocks), f])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for g in np.unique(coins):
            m = coins == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        G, N, K = n_coins, n_blocks, 2
        c = (G / (G - 1.0)) * ((N - 1.0) / (N - K))
        V = c * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    # supporting check
    sup_val, sup_pass = None, None
    if n_blocks > 0 and n_short > 0:
        share_short = float((y[f < 0] < 0).mean())
        share_all = float((y < 0).mean())
        sup_val = share_short - share_all
        sup_pass = bool(sup_val > 0)

    # decision
    if n_short < 100:
        status = "inconclusive"
        decided = f"Only {n_short} non-overlapping blocks with forecast below 0, fewer than the 100 required, so the result is inconclusive."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its clustered t could not be computed, so no t reaches +/-2 and the result is inconclusive."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The slope is positive with coin-clustered t >= 2 on at least 100 short blocks: deeper shorts are followed by lower excess returns."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with coin-clustered t <= -2: deeper shorts are followed by rebounds."
    else:
        status = "inconclusive"
        decided = "The coin-clustered t lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": MAIN_NAME,
            "value": slope,
            "statistic": ({"name": "OLS slope t, SE clustered by coin (CR1)", "value": tstat} if tstat is not None else None),
            "threshold": THRESH,
        },
        "supporting_check": {
            "name": "share of negative excess blocks when forecast < 0 minus share across all blocks",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping blocks with forecast below 0": n_short,
            "non-overlapping blocks": int(n_blocks),
            "coins": n_coins,
        },
        "decided_by": decided,
        "reading": ("Blocks start at rows 0, 20, 40, ... of each window with the full 20-bar forward log return inside the window; "
                    "the coin-window mean 20-bar return is the mean of those block returns; the regression is pooled OLS with intercept and "
                    "Stata-style CR1 coin-clustered standard errors; the supporting check passes if the short-block share of negative excess returns exceeds the all-block share."),
    }
