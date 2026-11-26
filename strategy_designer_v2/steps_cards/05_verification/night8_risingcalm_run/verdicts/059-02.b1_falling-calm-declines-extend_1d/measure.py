import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    DEPTH = "debug_info.components.depth.last_history_value"

    def depth_from_prices(df):
        c = df["close"].astype(float)
        hi = c.rolling(14, min_periods=14).max()
        sd = c.pct_change().rolling(30, min_periods=30).std()
        return (c - hi) / hi / sd

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if DEPTH in df.columns:
                depth = pd.to_numeric(df[DEPTH], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=df.index)
            depth = depth.where(depth.notna(), depth_from_prices(df))
            profile = df["regime"].astype(str) == "unknown"
            situation = profile & (depth < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The falling-calm profile is read from the recorded regime 'unknown' (the detector's components are not "
               "recorded and the 365-day percentile cannot be rebuilt inside a window), the situation as profile plus a "
               "negative 14-day depth, the slope t as an OLS t with standard errors clustered by calendar day, and the "
               "minimum counts as 'not observable' when not reached.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of drift-adjusted 5-bar return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"grid cases with forecast below 0": 0, "distinct days": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are short bars in the falling-calm profile with the close "
                           "below its 14-day high, as the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        drift_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                drift_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_rows.append((ts.iloc[i].strftime("%Y-%m-%d"), float(fc[i]), r))
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))
        for d, f, r in coin_rows:
            rows.append((d, f, r - drift))

    n_cases = len(rows)
    days = [r[0] for r in rows]
    n_days = len(set(days))
    counts = {"grid cases with forecast below 0": n_cases, "distinct days": n_days}

    mm_name = "slope of drift-adjusted 5-bar forward return on forecast (forecast < 0 grid cases)"
    thr = "slope t >= 2 (with mean short unusual move > 0) confirms; t <= -2 rejects; else inconclusive"

    if n_cases < 30 or n_days < 20:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "mean unusual move in the short direction", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 30 grid cases with forecast below 0 on at least 20 distinct days is not reached.",
            "reading": reading,
        }

    f = np.array([r[1] for r in rows])
    y = np.array([r[2] for r in rows])
    d = np.array(days)

    short_move = float(np.mean(-y))
    sup_pass = bool(short_move > 0)

    slope = None
    t = None
    X = np.column_stack([np.ones(n_cases), f])
    XtX = X.T @ X
    if np.var(f) > 0 and np.linalg.matrix_rank(XtX) == 2:
        XtX_inv = np.linalg.inv(XtX)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        uniq = np.unique(d)
        for g in uniq:
            m = d == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        G = len(uniq)
        k = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k)) if G > 1 and n_cases > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else 0.0
        slope = float(beta[1])
        t = float(slope / se) if se > 0 else None

    if t is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (no spread in the forecast), so it meets neither rule: inconclusive."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean unusual move in the short direction is above 0: confirm."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean unusual move in the short direction is at or below 0: inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: deeper declines are followed by relatively larger rises: reject."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": slope,
                         "statistic": {"name": "OLS slope t, day-clustered", "value": t} if t is not None else None,
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move in the short direction", "value": short_move,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
