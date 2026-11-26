import numpy as np
import pandas as pd

H = 5
COL_RAW = "debug_info.components.range_pos.last_history_value"


def _position_from_prices(df):
    # Donchian position, 20 bars, high/low source, bar t included: -1 at low, 0 middle, +1 at high
    hh = df["high"].astype(float).rolling(20, min_periods=20).max()
    ll = df["low"].astype(float).rolling(20, min_periods=20).min()
    rng = hh - ll
    pos = 2.0 * (df["close"].astype(float) - ll) / rng - 1.0
    return pos.where(rng > 0)


def _clustered_ols(x, y, groups):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(y)
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    if np.linalg.matrix_rank(XtX) < 2:
        return None, None
    XtX_inv = np.linalg.inv(XtX)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    meat = np.zeros((2, 2))
    g_arr = np.asarray(groups)
    uniq = pd.unique(g_arr)
    for g in uniq:
        m = g_arr == g
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    G = len(uniq)
    corr = G / (G - 1) if G > 1 else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    t = beta[1] / se if se and np.isfinite(se) and se > 0 else None
    return float(beta[1]), (float(t) if t is not None and np.isfinite(t) else None)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            pos_p = _position_from_prices(df)
            if COL_RAW in df.columns:
                raw = pd.to_numeric(df[COL_RAW], errors="coerce")
                pos = raw.where(raw.notna(), pos_p)
            else:
                pos = pos_p
            calm_choppy = df["regime"].astype(str) == "unknown"
            situation = calm_choppy & (pos < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of drift-adjusted 5-bar forward return on forecast (grid bars, forecast < 0)"
    thr = "confirm if slope t >= 2 and supporting check passes; reject if slope t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are choppy-calm bars (regime 'unknown') with the close below the middle of its 20-day range and a short forecast, as the Fidelity's situation and side require",
            "reading": "the choppy calm profile is the detector's 'unknown' regime (all vetoes send other bars to 'chop'); nearness to the bottom is a range position below 0, from last_history_value or recomputed from prices where not recorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        drift_samples = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                drift_samples.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_rows.append((ts.iloc[i].normalize(), float(fc[i]), r))
        if not drift_samples:
            continue
        drift = float(np.mean(drift_samples))
        for d, f, r in coin_rows:
            rows.append((d, f, r - drift))

    n_cases = len(rows)
    days = sorted(set(r[0] for r in rows))
    n_days = len(days)
    counts = {"grid cases with forecast < 0": n_cases, "distinct days": n_days}

    slope, t = (None, None)
    mean_ex = None
    if n_cases >= 3:
        d = [r[0] for r in rows]
        f = [r[1] for r in rows]
        y = [r[2] for r in rows]
        slope, t = _clustered_ols(f, y, d)
        mean_ex = float(np.mean(y))
    elif n_cases > 0:
        mean_ex = float(np.mean([r[2] for r in rows]))

    sup_pass = (mean_ex < 0) if mean_ex is not None else None

    reading = ("Same-day clustering is a day-clustered (cluster-robust, G/(G-1) corrected) OLS standard error of the slope; "
               "the coin's mean 5-bar return is taken over the non-overlapping 5-bar grid of all its windows; "
               "the supporting check is the plain mean of the drift-adjusted returns of the same grid cases.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = ("fewer than 30 grid cases with forecast < 0" if n_cases < 30
                   else "cases fall on fewer than 20 distinct days")
    elif t is None:
        status = "inconclusive"
        decided = "the slope's t could not be computed (no variation in the forecast), so neither rule is met"
    elif t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "slope t >= 2 and the mean drift-adjusted 5-bar forward return is below 0"
        else:
            status = "inconclusive"
            decided = "slope t >= 2 but the supporting check fails (mean drift-adjusted return not below 0)"
    elif t <= -2:
        status = "rejected"
        decided = "slope t <= -2: bars nearer the low are followed by higher excess returns"
    else:
        status = "inconclusive"
        decided = "slope t between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t, day-clustered", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean drift-adjusted 5-bar forward return < 0", "value": mean_ex, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
