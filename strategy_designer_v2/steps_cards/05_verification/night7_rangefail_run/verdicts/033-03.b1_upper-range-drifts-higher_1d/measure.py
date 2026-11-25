import numpy as np
import pandas as pd

H = 10
RP = "debug_info.components.range_pos.last_history_value"
AH = "debug_info.components.above_high.last_history_value"


def _num(df, col):
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
    return np.full(len(df), np.nan)


def _cluster_slope_t(x, y, groups):
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    if n < 3 or np.linalg.matrix_rank(XtX) < 2:
        return np.nan, np.nan, 0
    XtX_inv = np.linalg.inv(XtX)
    beta = XtX_inv @ (X.T @ y)
    u = y - X @ beta
    meat = np.zeros((2, 2))
    uniq, inv = np.unique(groups, return_inverse=True)
    G = len(uniq)
    for g in range(G):
        m = inv == g
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    if G < 2:
        return float(beta[1]), np.nan, G
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
    V = corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    t = beta[1] / se if se and np.isfinite(se) else np.nan
    return float(beta[1]), float(t), G


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = _num(df, "forecast")
            rp = _num(df, RP)
            ah = _num(df, AH)
            active = np.isfinite(fc) & (fc != 0) & np.isfinite(rp)
            ah0 = np.where(np.isfinite(ah), ah, 0.0)
            # expected side: long when the close is through the prior 20-day high,
            # otherwise the side of the close's position in its 20-day range (above mid long, below mid short)
            expected = np.where(ah0 > 0, 1.0, np.sign(rp))
            n_active += int(active.sum())
            n_agree += int((active & (np.sign(fc) == expected) & (expected != 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled slope t of 10-bar excess return on forecast (day-clustered)"
    main_thr = "t >= 2 confirms (with check difference > 0); t <= -2 rejects; otherwise inconclusive"
    check_name = "mean excess return when above_high > 0 minus mean excess return when forecast < 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars have a forecast whose sign matches the plan's situation "
                          "(long above mid-range or through the 20-day high, short below mid-range).",
            "reading": "Expected side taken as long when above_high > 0, else the sign of the raw range position.",
        }

    # ---------- 2. grid cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = _num(df, "close")
            fc = _num(df, "forecast")
            ah = _num(df, AH)
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").to_numpy()
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((coin, str(ts[i]), c1 / c0 - 1.0, fc[i], ah[i]))
    g = pd.DataFrame(rows, columns=["coin", "day", "ret", "fc", "ah"])
    if len(g):
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
    else:
        g["excess"] = []

    reg = g[np.isfinite(g["fc"]) & np.isfinite(g["excess"])]
    n_cases = int(len(reg))
    above = g[np.isfinite(g["ah"]) & (g["ah"] > 0) & np.isfinite(g["excess"])]
    neg = reg[reg["fc"] < 0]
    n_above = int(len(above))
    counts = {"grid cases in total": n_cases, "cases above the 20-day high": n_above,
              "grid cases with forecast below 0": int(len(neg))}

    slope, t, G = (np.nan, np.nan, 0)
    if n_cases >= 3:
        slope, t, G = _cluster_slope_t(reg["fc"].to_numpy(float), reg["excess"].to_numpy(float),
                                       reg["day"].to_numpy())
    counts["days (clusters)"] = int(G)

    diff = (above["excess"].mean() - neg["excess"].mean()) if (n_above > 0 and len(neg) > 0) else np.nan
    check_pass = bool(np.isfinite(diff) and diff > 0)

    reading = ("Expected side taken as long when above_high > 0, else the sign of the raw range position; "
               "the slope is OLS with intercept of excess return on forecast, its t day-clustered (CR1); "
               "the drift is each coin's mean grid 10-bar return over all its windows; "
               "the minimum counts the plan lists under inconclusive are applied as 'not observable'.")

    def _f(v):
        return float(v) if v is not None and np.isfinite(v) else None

    out = {
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": _f(slope),
                         "statistic": {"name": "day-clustered slope t", "value": _f(t)},
                         "threshold": main_thr},
        "supporting_check": {"name": check_name, "value": _f(diff), "passed": check_pass},
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 300:
        out["status"] = "not observable"
        out["decided_by"] = f"Fewer than 300 grid cases in total ({n_cases})."
    elif n_above < 30:
        out["status"] = "not observable"
        out["decided_by"] = f"Fewer than 30 cases above the 20-day high ({n_above})."
    elif not np.isfinite(t):
        out["status"] = "inconclusive"
        out["decided_by"] = "The slope's t could not be computed, so it is not 2 or more nor -2 or less."
    elif t >= 2 and check_pass:
        out["status"] = "confirmed"
        out["decided_by"] = "The slope's t is 2 or more and the supporting check's difference is positive."
    elif t >= 2:
        out["status"] = "inconclusive"
        out["decided_by"] = "The slope's t is 2 or more but the supporting check fails."
    elif t <= -2:
        out["status"] = "rejected"
        out["decided_by"] = "The slope's t is -2 or less: higher range positions are followed by lower excess returns."
    else:
        out["status"] = "inconclusive"
        out["decided_by"] = "The slope's t is between -2 and 2."
    return out
