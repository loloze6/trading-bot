import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RAW = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the 50-day SMA is below the 200-day SMA, so the raw spread is below 0.
    # Expected side: short, because the outcome is a fall.
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

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 20-bar excess log return on forecast at block start"
    thr = "slope > 0 with clustered t >= 2 confirms; slope < 0 with t <= -2 rejects"
    sup_name = ("share of negative excess blocks when forecast < 0 "
                "minus share across all blocks")
    reading_default = (
        "The situation is the raw component spread (last_history_value) below 0 on the short side; "
        "blocks start at positions 0, 20, 40, ... of each window and need close[t+20] inside the window; "
        "the coin-window mean is the mean of that coin-window's block log returns; "
        "the OLS has an intercept and CR1 standard errors clustered by coin; "
        "the supporting check passes when the share for forecast < 0 exceeds the all-block share.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars "
                           "where the 50-day SMA is below the 200-day SMA (raw spread < 0), "
                           "so the config does not trade the plan's situation."),
            "reading": reading_default,
        }

    # ---------- 2. Non-overlapping 20-bar blocks ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            recs = []
            for t in range(0, n, H):
                if t + H > n - 1:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 <= 0 or c1 <= 0:
                    continue
                recs.append((np.log(c1 / c0), f))
            if not recs:
                continue
            r = np.array([x[0] for x in recs])
            m = r.mean()
            for (ri, fi) in recs:
                rows.append((coin, ri - m, fi))

    if rows:
        blocks = pd.DataFrame(rows, columns=["coin", "excess", "forecast"])
    else:
        blocks = pd.DataFrame(columns=["coin", "excess", "forecast"])

    n_blocks = int(len(blocks))
    n_neg = int((blocks["forecast"] < 0).sum()) if n_blocks else 0
    counts = {"non-overlapping blocks": n_blocks,
              "non-overlapping blocks with forecast below 0": n_neg}

    # ---------- Supporting check ----------
    if n_blocks > 0 and n_neg > 0:
        share_neg_fc = float((blocks.loc[blocks["forecast"] < 0, "excess"] < 0).mean())
        share_all = float((blocks["excess"] < 0).mean())
        sup_val = share_neg_fc - share_all
        sup = {"name": sup_name, "value": float(sup_val), "passed": bool(sup_val > 0)}
    else:
        sup = {"name": sup_name, "value": None, "passed": None}

    # ---------- Regression with SEs clustered by coin ----------
    slope = None
    tstat = None
    if n_blocks >= 3:
        y = blocks["excess"].to_numpy(dtype=float)
        x = blocks["forecast"].to_numpy(dtype=float)
        X = np.column_stack([np.ones_like(x), x])
        groups = blocks["coin"].to_numpy()
        G = len(np.unique(groups))
        XtX = X.T @ X
        if np.var(x) > 0 and G >= 2 and np.linalg.matrix_rank(XtX) == 2:
            bread = np.linalg.inv(XtX)
            beta = bread @ X.T @ y
            u = y - X @ beta
            meat = np.zeros((2, 2))
            for g in np.unique(groups):
                idx = groups == g
                s = X[idx].T @ u[idx]
                meat += np.outer(s, s)
            N, K = X.shape
            c = (G / (G - 1)) * ((N - 1) / (N - K))
            V = c * bread @ meat @ bread
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    stat = {"name": "t of slope, SE clustered by coin", "value": tstat} if tstat is not None else None

    # ---------- Decision ----------
    if n_neg < 100:
        status = "inconclusive"
        decided = (f"Only {n_neg} non-overlapping blocks have a forecast below 0, fewer than "
                   "the 100 required, so the result is inconclusive.")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its clustered t could not be estimated, so the result is inconclusive."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = ("The slope is positive with clustered t >= 2: more negative forecasts are "
                   "followed by lower excess returns.")
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = ("The slope is negative with clustered t <= -2: deeper shorts are followed "
                   "by rebounds.")
    else:
        status = "inconclusive"
        decided = "The clustered t of the slope lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope, "statistic": stat, "threshold": thr},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_default,
    }
