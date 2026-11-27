import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RUN = 5

    # ---------- 1. Situation check: 5-bar price change > 0, side long ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            run5 = np.full(n, np.nan)
            if n > RUN:
                run5[RUN:] = close[RUN:] / close[:-RUN] - 1.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                if not np.isfinite(run5[i]):
                    n_active_uncomputable += 1
                    continue
                n_active += 1
                if run5[i] > 0 and f > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("The 5-bar change is recomputed from closes inside each window, so active bars in a window's first 5 rows "
               "(no history recorded) are left out of the agreement; trending bars are those with regime == 'trending'; "
               "the coin's mean 3-bar return is taken over the 0,3,6,... grid of all its windows; the slope is OLS with "
               "intercept of excess return on forecast, with CR1 standard errors clustered by UTC day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars agreeing": int(n_agree),
                       "active bars without 5-bar history": int(n_active_uncomputable)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where the 5-bar price change "
                           "is above 0 with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        coin_rows = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            regime = d["regime"].astype(str).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_all.append(r)
                if regime[i] == "trending" and np.isfinite(fc[i]):
                    coin_rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        if len(grid_all) == 0:
            continue
        mu = float(np.mean(grid_all))
        for c, day, f, r in coin_rows:
            rows.append((c, day, f, r - mu))

    res = pd.DataFrame(rows, columns=["coin", "day", "forecast", "excess"])
    n_cases = int(len(res))
    n_days = int(res["day"].nunique()) if n_cases else 0
    counts = {"trending grid cases": n_cases, "distinct days": n_days}
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive"
    name = "slope of 3-bar excess forward return on forecast, trending grid bars"

    if n_cases < 100 or n_days < 60:
        which = "fewer than 100 trending grid cases" if n_cases < 100 else "cases on fewer than 60 distinct days"
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"The plan's minimum count is not reached: {which}.",
            "reading": reading,
        }

    x = res["forecast"].values.astype(float)
    y = res["excess"].values.astype(float)
    X = np.column_stack([np.ones(n_cases), x])
    XtX = X.T @ X
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        XtX_inv = None
    if XtX_inv is None:
        slope, t = None, None
    else:
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in res.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days
        K = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None

    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its clustered t could not be computed (no spread in the forecast), so neither rule is met."
    elif slope > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm rule: the slope is above 0 with clustered t >= 2."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule: the slope is below 0 with clustered t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's clustered t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": name,
                         "value": slope,
                         "statistic": ({"name": "t clustered by day", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
