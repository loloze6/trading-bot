import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall_x_excess.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: a falling day whose range exceeds the closing loss -> the product is > 0
            situation = raw.notna() & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "day-clustered t of the slope of next-day unusual return on forecast (forecast > 0 bars)"
    threshold = "slope t >= 2 with mean unusual move > 0 confirms; slope t <= -2 or mean unusual move t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on falling days "
                           "whose range exceeds the closing loss (component raw value > 0)."),
            "reading": "The situation is read as the component's raw value being above 0, the side as forecast > 0.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            nxt = np.full(len(close), np.nan)
            nxt[:-1] = close[1:] / close[:-1] - 1.0
            coin_rets.append(nxt[np.isfinite(nxt)])
            day = ts.dt.floor("D").astype("int64").to_numpy()
            for i in range(len(close)):
                if np.isfinite(f[i]) and f[i] > 0 and np.isfinite(nxt[i]):
                    coin_cases.append((day[i], f[i], nxt[i]))
        if coin_cases:
            allr = np.concatenate(coin_rets) if coin_rets else np.array([])
            drift = float(np.mean(allr)) if len(allr) else np.nan
            for d, fv, r in coin_cases:
                if np.isfinite(drift):
                    rows.append((d, fv, r - drift))

    n_cases = len(rows)
    days = np.array([r[0] for r in rows]) if rows else np.array([])
    n_days = int(len(np.unique(days))) if n_cases else 0
    counts = {"case bars": int(n_cases), "distinct days": int(n_days)}

    reading = ("Cases are all bars with forecast > 0 and a next bar in the same window (horizon 1 bar, so every bar "
               "is its own grid cell); the regression is OLS with an intercept and Stata-style day-clustered "
               "standard errors; the mean unusual move's t sums the cases' deviations per UTC day.")

    if n_cases < 150 or n_days < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean unusual move > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 150 case bars on at least 100 distinct days is not reached.",
            "reading": reading,
        }

    fv = np.array([r[1] for r in rows], dtype=float)
    y = np.array([r[2] for r in rows], dtype=float)
    X = np.column_stack([np.ones(n_cases), fv])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    uniq, inv = np.unique(days, return_inverse=True)
    G = len(uniq)
    scores = np.zeros((G, 2))
    np.add.at(scores, inv, X * u[:, None])
    meat = scores.T @ scores
    k = 2
    corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k)) if G > 1 and n_cases > k else np.nan
    V = corr * XtX_inv @ meat @ XtX_inv
    se_slope = float(np.sqrt(V[1, 1])) if np.isfinite(V[1, 1]) and V[1, 1] > 0 else np.nan
    slope = float(beta[1])
    t_slope = float(slope / se_slope) if np.isfinite(se_slope) and se_slope > 0 else 0.0

    mean_u = float(np.mean(y))
    dev = y - mean_u
    S = np.zeros(G)
    np.add.at(S, inv, dev)
    var_mean = (G / (G - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2) if G > 1 else np.nan
    t_mean = float(mean_u / np.sqrt(var_mean)) if np.isfinite(var_mean) and var_mean > 0 else 0.0
    support_pass = bool(mean_u > 0)

    if t_slope >= 2 and support_pass:
        status = "confirmed"
        decided = "Confirm: the slope t is 2 or more and the mean unusual move of the cases is above 0."
    elif t_slope <= -2 or t_mean <= -2:
        status = "rejected"
        decided = ("Reject: the slope t is -2 or less." if t_slope <= -2
                   else "Reject: the mean unusual move of the cases has a t of -2 or less.")
    else:
        status = "inconclusive"
        if t_slope >= 2:
            decided = "Inconclusive: the slope t is 2 or more but the mean unusual move is at or below 0 (t above -2)."
        else:
            decided = "Inconclusive: the slope t is between -2 and 2 and the mean unusual move's t is above -2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": {"name": "day-clustered t of the slope", "value": t_slope},
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move > 0 (t " + str(round(t_mean, 3)) + ", day-clustered)",
                             "value": mean_u, "passed": support_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
