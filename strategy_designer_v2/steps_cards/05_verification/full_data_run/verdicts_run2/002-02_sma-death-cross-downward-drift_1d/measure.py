import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].apply(pd.to_numeric, errors="coerce").dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            # situation: 50-SMA below 200-SMA (raw spread < 0), side: short (forecast < 0)
            n_agree += int((act & (d[RAW] < 0) & (d["forecast"] < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "weighted mean excess gain of the short over holding (10 bars, non-overlapping, pooled)"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; fewer than 30 cases inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are short bars where the 50-day SMA is below the 200-day SMA, so the config does not do what the plan's situation says.",
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, fc[p]))
        if not grid_rows:
            continue
        rets = np.array([r for r, _ in grid_rows])
        fcs = np.array([f for _, f in grid_rows])
        hold = float(np.mean(rets))
        m = np.isfinite(fcs) & (fcs < 0)
        for r, f in zip(rets[m], fcs[m]):
            xs.append(-(r - hold))  # short side's excess gain
            ws.append(abs(f))

    xs = np.array(xs, dtype=float)
    ws = np.array(ws, dtype=float)
    n_cases = int(len(xs))

    def wstats(x, w):
        if len(x) == 0 or w.sum() <= 0:
            return None, None
        mu = float(np.sum(w * x) / np.sum(w))
        if len(x) < 2:
            return mu, None
        var = len(x) / (len(x) - 1) * np.sum(w ** 2 * (x - mu) ** 2) / np.sum(w) ** 2
        se = float(np.sqrt(var))
        t = mu / se if se > 0 else None
        return mu, t

    mean, t = wstats(xs, ws)

    # Supporting check: terciles of |forecast|
    sup_val, sup_pass = None, None
    if n_cases >= 3:
        order = np.argsort(ws, kind="mergesort")
        parts = np.array_split(order, 3)
        bot, top = parts[0], parts[-1]
        mb, _ = wstats(xs[bot], ws[bot])
        mt, _ = wstats(xs[top], ws[top])
        if mb is not None and mt is not None:
            sup_val = float(mt - mb)
            sup_pass = bool(mt > mb)

    if n_cases < 30:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping short cases in total, which the plan calls inconclusive."
    elif mean is None or t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so no confirm or reject rule is met."
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The short side's weighted mean excess gain is above 0 with t >= 2: price falls further than holding while the short average is below the long one."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The short side's weighted mean excess gain is below 0 with t <= -2: price rises relative to holding, moves reverse."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if mean is None else float(mean),
            "statistic": None if t is None else {"name": "t of |forecast|-weighted mean (weighted standard error)", "value": float(t)},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top minus bottom |forecast| tercile weighted excess gain",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping short cases": n_cases},
        "decided_by": decided,
        "reading": "Holding is each coin's mean 10-bar return over the same non-overlapping grid (positions 0, 10, 20, ... of every window) pooled across its windows, the short's excess gain is -(forward return - holding), the t uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w), and terciles are equal-count splits of the short cases sorted by |forecast| compared by their weighted means.",
    }
