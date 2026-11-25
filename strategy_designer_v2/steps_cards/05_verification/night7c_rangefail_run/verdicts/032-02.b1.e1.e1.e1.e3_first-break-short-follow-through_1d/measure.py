import numpy as np
import pandas as pd


def measure(bars):
    PROX = "debug_info.components.margin_prox.last_history_value"
    H = 3
    LOOK = 60
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            prox = (pd.to_numeric(df[PROX], errors="coerce").values
                    if PROX in df.columns else np.full(len(df), np.nan))
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                if i >= LOOK:
                    prior_high = np.max(close[i - LOOK:i])
                    is_break = close[i] > prior_high
                else:
                    # not enough in-window history: the raw proximity 1/(1+margin%)
                    # lies strictly between 0 and 1 only when the margin is positive
                    p = prox[i]
                    is_break = bool(np.isfinite(p) and 0 < p < 1)
                if is_break and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of excess 3-bar return on raw proximity (day-clustered)"
    threshold = "confirm: t >= 2 with weighted mean excess > 0; reject: t <= -2; over at least 100 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close "
                           "is above the highest of the prior 60 closes, as the Fidelity's situation and long side require."),
            "reading": "Break bars are recomputed from in-window closes when 60 prior bars exist, else from the raw proximity lying in (0,1).",
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        # coin's mean 3-bar return over all windows, non-overlapping grid per window
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    grid_rets.append(c[i + H] / c[i] - 1.0)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        mean_ret = float(np.mean(grid_rets))

        for df in prepared:
            c = df["close"].astype(float).values
            reg = df["regime"].astype(str).values
            prox = (pd.to_numeric(df[PROX], errors="coerce").values
                    if PROX in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            last_kept = None
            for i in range(len(df)):
                if reg[i] != "trending":
                    continue
                if last_kept is not None and i - last_kept <= H:
                    continue
                last_kept = i
                if i + H >= len(df):
                    continue
                p = prox[i]
                if not np.isfinite(p) or not np.isfinite(c[i]) or not np.isfinite(c[i + H]) or c[i] <= 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                xs.append(float(p))
                ys.append(r - mean_ret)
                days.append(ts.iloc[i].strftime("%Y-%m-%d"))

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n = int(len(x))
    n_days = int(len(set(days)))

    slope = None
    t = None
    wmean = None
    if n >= 3 and np.var(x) > 0:
        X = np.column_stack([np.ones(n), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        dser = pd.Series(range(n)).groupby(pd.Series(days)).apply(list)
        meat = np.zeros((2, 2))
        for idx in dser.values:
            idx = np.array(idx)
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = len(dser)
        corr = G / (G - 1) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None
    if n > 0 and np.sum(x) != 0:
        wmean = float(np.sum(y * x) / np.sum(x))
    sup_pass = None if wmean is None else bool(wmean > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 100 cases."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in proximity), so neither rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the proximity-weighted mean excess return is above 0, over at least 100 cases."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less over at least 100 cases: larger overshoots are followed by larger rises."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the proximity-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t is None else {"name": "OLS slope t, day-clustered SE", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "proximity-weighted mean excess 3-bar return > 0",
            "value": wmean,
            "passed": sup_pass,
        },
        "counts": {"cases": n, "days": n_days},
        "decided_by": decided,
        "reading": ("A case is a 'trending' bar with no kept case 1 to 3 bars before it in its window, dropped if its 3-bar "
                    "return or raw proximity is missing; the coin's mean 3-bar return uses the non-overlapping grid 0,3,6,... "
                    "of every window pooled; same-day cases are summed into one deviation by clustering the OLS slope's "
                    "standard error by UTC day; fewer than 100 cases is reported as not observable."),
    }
