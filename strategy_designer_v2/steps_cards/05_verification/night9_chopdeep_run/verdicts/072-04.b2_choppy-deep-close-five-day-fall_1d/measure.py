import numpy as np
import pandas as pd

RAW_COL = "debug_info.components.depth.last_history_value"
H = 5
CHOPPY_REGIME = "unknown"   # the config's default regime: the only one with a strategy (|60-bar evolution| <= 10)


def _to_days(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        unit = "ns" if med > 1e17 else ("us" if med > 1e14 else ("ms" if med > 1e11 else "s"))
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.strftime("%Y-%m-%d").values


def _cluster_slope_t(x, y, groups):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    if np.linalg.matrix_rank(XtX) < 2:
        return None, None
    XtX_inv = np.linalg.inv(XtX)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    g = pd.Series(groups)
    uniq = pd.unique(g)
    G = len(uniq)
    if G < 2:
        return float(beta[1]), None
    meat = np.zeros((2, 2))
    codes = pd.Categorical(g, categories=uniq).codes
    for k in range(G):
        m = codes == k
        sg = X[m].T @ e[m]
        meat += np.outer(sg, sg)
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0)) if n > 2 else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    if not np.isfinite(se) or se == 0:
        return float(beta[1]), None
    return float(beta[1]), float(beta[1] / se)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw = (pd.to_numeric(df[RAW_COL], errors="coerce").values
                   if RAW_COL in df.columns else np.full(len(df), np.nan))
            reg = df["regime"].astype(str).values
            active = f != 0
            situ = (reg == CHOPPY_REGIME) & np.isfinite(raw) & (raw < 0)
            agree = active & situ & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "clustered-by-day t of the slope of drift-adjusted 5-bar return on forecast (grid bars, forecast < 0)"
    thr = "confirm if t >= +2 with supporting check passing; reject if t <= -2; else inconclusive; at least 100 grid cases with forecast < 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars in the choppy regime (default regime) with the close "
                           "below its 20-day high (raw depth < 0): the forecast does not follow the plan's situation and side."),
            "reading": "The choppy situation is read from the recorded regime (the config's default regime 'unknown', the only one with a strategy) and the depth from last_history_value < 0.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        coin_grid = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            days = _to_days(df["timestamp"].values)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                coin_grid.append((coin, days[i], f[i], c1 / c0 - 1.0))
        if not coin_grid:
            continue
        drift = float(np.mean([r[3] for r in coin_grid]))
        for (c, d, fc, r) in coin_grid:
            rows.append((c, d, fc, r - drift))

    tab = pd.DataFrame(rows, columns=["coin", "day", "forecast", "excess"])
    tab = tab[np.isfinite(tab["forecast"]) & np.isfinite(tab["excess"])]
    neg = tab[tab["forecast"] < 0]
    deep = tab[tab["forecast"] <= -10]
    n_neg = int(len(neg))
    n_days = int(neg["day"].nunique()) if n_neg else 0
    n_deep = int(len(deep))

    slope, t = (None, None)
    if n_neg >= 3:
        slope, t = _cluster_slope_t(neg["forecast"].values, neg["excess"].values, neg["day"].values)

    deep_mean = float(deep["excess"].mean()) if n_deep > 0 else None
    sup_passed = (bool(deep_mean < 0) if deep_mean is not None else None)

    counts = {"grid cases with forecast below 0": n_neg,
              "days of those cases": n_days,
              "grid cases with forecast at or below -10": n_deep}

    if n_neg < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 grid cases with a forecast below 0 is not reached ({n_neg})."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it meets neither the confirm nor the reject rule."
    elif t >= 2:
        if sup_passed is True:
            status = "confirmed"
            decided = "The slope's t is +2 or more and the deep cases' mean drift-adjusted 5-bar return is below 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope's t is +2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: deeper closes are followed by better excess returns (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": (float(slope) if slope is not None else None),
                         "statistic": ({"name": "slope t, clustered by day (CR1)", "value": float(t)} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean drift-adjusted 5-bar return on grid bars with forecast <= -10 is below 0",
                             "value": deep_mean, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid cases are grid bars (positions 0,5,10,... per window) with a 5-bar forward return inside the window, the normal drift is "
                    "each coin's mean 5-bar return over all its grid bars in all windows, 'cases of one day together' is a day-clustered (CR1) OLS slope t, "
                    "the choppy situation is the recorded default regime 'unknown', and a missing minimum count gives 'not observable' as the workflow requires."),
    }
