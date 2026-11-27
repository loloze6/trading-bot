import numpy as np
import pandas as pd
from scipy import stats


def _to_time(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        mx = np.nanmax(np.abs(v.values)) if len(v) else 0
        if mx > 1e17:
            unit = "ns"
        elif mx > 1e14:
            unit = "us"
        elif mx > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _depth_from_prices(df):
    close = df["close"].astype(float)
    hh = df["high"].astype(float).rolling(20, min_periods=20).max()
    ret = close.pct_change()
    sd = ret.rolling(20, min_periods=20).std()
    return ((close - hh) / hh) / sd


def _cluster_ols(x, y, groups):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(y)
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    if np.linalg.matrix_rank(XtX) < 2:
        return np.nan, np.nan
    bread = np.linalg.inv(XtX)
    beta = bread @ X.T @ y
    u = y - X @ beta
    g = pd.Series(groups).astype(str).values
    meat = np.zeros((2, 2))
    uniq = pd.unique(g)
    for key in uniq:
        m = g == key
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    G = len(uniq)
    k = 2
    if G < 2 or n <= k:
        return beta[1], np.nan
    c = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = c * bread @ meat @ bread
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    return beta[1], (beta[1] / se if se and np.isfinite(se) else np.nan)


def measure(bars):
    H = 5
    dcol = "debug_info.components.depth.last_history_value"
    active_regime = "unknown"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if dcol in df.columns:
                depth = pd.to_numeric(df[dcol], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=df.index)
            depth = depth.where(depth.notna(), _depth_from_prices(df))
            reg = df["regime"].astype(str)
            act = fc != 0
            sit = (reg == active_regime) & (depth < 0) & (fc < 0)
            n_active += int(act.sum())
            n_agree += int((act & sit).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The choppy profile is read as the bars whose recorded regime is 'unknown' (the only regime with a "
               "strategy, i.e. 60-bar price evolution between -10 and +10), the situation as a close below its 20-day "
               "high (depth < 0) on the short side; the drift is the coin's mean non-overlapping 5-bar return over all "
               "its windows' grids, the slope's t is clustered by calendar day (UTC), and thirds are cut by rank of "
               "|forecast| over all grid cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars in the choppy profile "
                           "with the close below its 20-day high, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- grid and drift ----------
    rows = []
    for coin, wins in bars.items():
        drift_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = _to_time(df["timestamp"])
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                drift_rets.append(r)
                if fc[i] != 0:
                    coin_rows.append((coin, w, ts.iloc[i].strftime("%Y-%m-%d"), float(fc[i]), r))
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))
        for (c, w, d, f, r) in coin_rows:
            rows.append({"coin": c, "window": w, "day": d, "forecast": f, "excess": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "window", "day", "forecast", "excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    main_name = "slope of 5-bar excess forward return on forecast (non-overlapping grid, active bars)"
    main_thr = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2 (t clustered by day)"
    sup_name = "deepest minus shallowest third by |forecast|, mean excess 5-bar return"

    if n_cases < 100 or n_days < 60:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 100 grid cases on at least 60 distinct days is not reached.",
            "reading": reading,
        }

    slope, t_slope = _cluster_ols(cases["forecast"].values, cases["excess"].values, cases["day"].values)

    # ---------- supporting check ----------
    absf = cases["forecast"].abs()
    rk = absf.rank(method="first")
    terc = pd.qcut(rk, 3, labels=[0, 1, 2])
    shallow = cases.loc[terc == 0, "excess"].values
    deep = cases.loc[terc == 2, "excess"].values
    diff = float(np.mean(deep) - np.mean(shallow)) if len(deep) and len(shallow) else np.nan
    if len(deep) > 1 and len(shallow) > 1:
        t_w = float(stats.ttest_ind(deep, shallow, equal_var=False).statistic)
    else:
        t_w = np.nan
    sup_pass = bool(np.isfinite(diff) and np.isfinite(t_w) and diff < 0 and t_w <= -2)
    counts["deepest third cases"] = int(len(deep))
    counts["shallowest third cases"] = int(len(shallow))

    slope_f = float(slope) if np.isfinite(slope) else None
    t_f = float(t_slope) if np.isfinite(t_slope) else None

    if t_f is not None and slope > 0 and t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = ("The slope is positive with t >= 2 and the deepest minus shallowest third is negative with "
                   "Welch t <= -2: the confirm rule is met.")
    elif t_f is not None and slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: the reject rule is met."
    else:
        status = "inconclusive"
        if t_f is not None and slope > 0 and t_slope >= 2:
            decided = ("The slope is positive with t >= 2 but the tercile check fails, so by the plan the result "
                       "is inconclusive.")
        else:
            decided = "The slope's |t| is below 2 (or undefined): neither confirm nor reject, so inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope_f,
            "statistic": {"name": "OLS slope t, clustered by day", "value": t_f},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name + " (Welch t <= -2)",
            "value": diff if np.isfinite(diff) else None,
            "passed": sup_pass,
            "welch_t": float(t_w) if np.isfinite(t_w) else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
