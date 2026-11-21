import numpy as np
import pandas as pd
from scipy import stats

H = 26
W_COL = "debug_info.components.cloud_width.last_history_value"


def _ichimoku(df):
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    tenkan = (high.rolling(9, min_periods=9).max() + low.rolling(9, min_periods=9).min()) / 2.0
    kijun = (high.rolling(26, min_periods=26).max() + low.rolling(26, min_periods=26).min()) / 2.0
    span_a_raw = (tenkan + kijun) / 2.0
    span_b_raw = (high.rolling(52, min_periods=52).max() + low.rolling(52, min_periods=52).min()) / 2.0
    # cloud under bar t: spans computed 26 bars earlier (displacement 26)
    span_a = span_a_raw.shift(26)
    span_b = span_b_raw.shift(26)
    top = pd.concat([span_a, span_b], axis=1).max(axis=1, skipna=False)
    pos = (close - top) / top * 100.0
    mid = (span_a + span_b) / 2.0
    slope = mid - mid.shift(26)
    return pos, slope


def _ols(y, X):
    X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X])
    y = np.asarray(y, float)
    n, k = X.shape
    if n <= k:
        return None, None
    XtX = X.T @ X
    if np.linalg.matrix_rank(XtX) < k:
        return None, None
    beta = np.linalg.solve(XtX, X.T @ y)
    resid = y - X @ beta
    s2 = resid @ resid / (n - k)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(XtX)))
    t = beta / se
    return beta, t


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    per_window = {}
    for coin in sorted(bars):
        for win in sorted(bars[coin], key=lambda w: int(str(w).lstrip("w")) if str(w).lstrip("w").isdigit() else str(w)):
            df = bars[coin][win].reset_index(drop=True)
            pos, slope = _ichimoku(df)
            regime_tr = (df["regime"].astype(str) == "trending")
            recomputable = pos.notna() & slope.notna()
            situ = pd.Series(np.where(recomputable, (pos > 0) & (slope > 0), regime_tr), index=df.index).astype(bool)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
            per_window[(coin, win)] = (df, slope, regime_tr, fc)
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The cloud position and 26-bar cloud slope are recomputed from each window's prices with the standard "
               "Ichimoku spans displaced 26 bars (falling back to the recorded regime on bars too early in a window to "
               "recompute them); in-regime cases are grid bars whose recorded regime is 'trending'; the supporting check "
               "z-scores width and slope across its cases and compares their OLS coefficients, using only cases where the "
               "slope can be recomputed; fewer than 30 cases gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with the close above a "
                           "rising cloud, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 26-bar return over all windows (non-overlapping grid)
    coin_rets = {}
    cases = []
    for (coin, win), (df, slope, regime_tr, fc) in per_window.items():
        close = df["close"].astype(float).values
        n = len(df)
        for i in range(0, n, H):
            if i + H >= n:
                continue
            r = close[i + H] / close[i] - 1.0
            if not np.isfinite(r):
                continue
            coin_rets.setdefault(coin, []).append(r)
            if bool(regime_tr.iloc[i]):
                w = df[W_COL].iloc[i] if W_COL in df.columns else np.nan
                cases.append({"coin": coin, "ret": r, "fc": float(fc.iloc[i]),
                              "width": float(w) if pd.notna(w) else np.nan,
                              "slope": float(slope.iloc[i]) if pd.notna(slope.iloc[i]) else np.nan})
    coin_mean = {c: float(np.mean(v)) for c, v in coin_rets.items()}
    for c in cases:
        c["excess"] = c["ret"] - coin_mean[c["coin"]]

    cdf = pd.DataFrame(cases, columns=["coin", "ret", "fc", "width", "slope", "excess"])
    cdf = cdf.dropna(subset=["fc", "excess"])
    n_cases = int(len(cdf))

    slope_val, t_val = None, None
    if n_cases >= 3 and np.std(cdf["fc"].values) > 0:
        beta, t = _ols(cdf["excess"].values, [cdf["fc"].values])
        if beta is not None:
            slope_val, t_val = float(beta[1]), float(t[1])

    # supporting check
    sdf = cdf.dropna(subset=["width", "slope"])
    n_sup = int(len(sdf))
    sup_val, sup_pass = None, None
    if n_sup >= 4 and sdf["width"].std() > 0 and sdf["slope"].std() > 0:
        zw = (sdf["width"] - sdf["width"].mean()) / sdf["width"].std()
        zs = (sdf["slope"] - sdf["slope"].mean()) / sdf["slope"].std()
        beta, _ = _ols(sdf["excess"].values, [zw.values, zs.values])
        if beta is not None:
            sup_val = float(beta[1] - beta[2])
            sup_pass = bool(beta[1] > beta[2])

    counts = {"independent in-regime cases": n_cases, "supporting check cases": n_sup}
    main = {"name": "OLS slope of 26-bar excess return on recorded forecast",
            "value": slope_val,
            "statistic": {"name": "OLS slope t", "value": t_val} if t_val is not None else None,
            "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; on at least 30 cases"}
    sup = {"name": "width coefficient minus slope coefficient (standardised joint regression)",
           "value": sup_val, "passed": sup_pass}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 independent in-regime cases on the 26-bar grid, the plan's minimum."
    elif t_val is None:
        status = "inconclusive"
        decided = "The forecast slope could not be estimated (no variation in the forecast), so neither rule is met."
    elif slope_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The forecast slope is positive with t >= 2 on at least 30 cases and the width coefficient exceeds the slope coefficient."
        else:
            status = "inconclusive"
            decided = "The forecast slope is positive with t >= 2, but the width coefficient does not exceed the slope coefficient (or could not be measured)."
    elif slope_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The forecast slope is negative with t <= -2 on at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The forecast slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
