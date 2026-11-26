import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    FC = "forecast"
    RAW = "debug_info.components.fall.last_history_value"
    ER_PERIOD = 30
    ER_MAX = 0.3
    TOL = 1e-9

    # ---------------- 1. situation check ----------------
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)
            # efficiency ratio over 30 bars, recomputed from prices inside the window where possible
            net = (close - close.shift(ER_PERIOD)).abs()
            path = close.diff().abs().rolling(ER_PERIOD).sum()
            er = net / path.replace(0, np.nan)
            # 7-day fall: the recorded raw component, else recomputed from prices
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            r1 = close.pct_change()
            raw_px = (close / close.shift(H) - 1) / (r1.rolling(30).std() * np.sqrt(H))
            raw = raw.fillna(raw_px)

            in_regime = regime == "mean_reversion"
            er_ok = er.isna() | (er <= ER_MAX + TOL)
            fell = raw < 0
            situation = in_regime & er_ok & fell

            act = fc != 0
            active_total += int(act.sum())
            active_ok += int((act & situation & (fc > 0)).sum())

    agreement = float(active_ok / active_total) if active_total > 0 else 0.0
    passed = active_total > 0 and agreement >= 0.9

    main_name = "day-clustered t of the slope of 7-bar excess return on forecast"
    threshold = "confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2 or mean excess t <= -2"
    reading = ("The regime part of the situation (30-day efficiency ratio <= 0.3 and 30-day volatility at or above its "
               "one-year median) is read from the recorded `regime` (the detector is not recorded and 365 days of history "
               "are not in a window), with the efficiency ratio also recomputed from in-window prices where 30 prior bars "
               "exist; the fall is the recorded raw scaled 7-day return below 0; the slope t is OLS with intercept and "
               "day-clustered standard errors; the plan's 'fewer than 40 cases on distinct days' is applied as the "
               "minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars in situation on long side": int(active_ok)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bets in the plan's situation "
                           "(mean_reversion regime with ER <= 0.3 and high volatility, after a 7-day fall)."),
            "reading": reading,
        }

    # ---------------- 2. criterion ----------------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            regime = d["regime"].astype(str).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if regime[i] == "mean_reversion" and np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((ts.iloc[i].normalize(), float(fc[i]), r))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for day, f, r in coin_cases:
            rows.append({"day": day, "coin": coin, "f": f, "ex": r - mu})

    cases = pd.DataFrame(rows, columns=["day", "coin", "f", "ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "cases on distinct days": n_days}

    if n_days < 40:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean excess 7-bar return of the cases > 0",
                                 "value": float(cases["ex"].mean()) if n_cases else None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 40 cases on distinct days: the plan's minimum count is not reached.",
            "reading": reading,
        }

    # slope with day-clustered SE
    y = cases["ex"].values.astype(float)
    x = cases["f"].values.astype(float)
    X = np.column_stack([np.ones_like(x), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    groups = cases["day"].values
    G = n_days
    K = X.shape[1]
    meat = np.zeros((K, K))
    sc = pd.DataFrame(X * resid[:, None]).groupby(groups).sum().values
    for g in sc:
        meat += np.outer(g, g)
    corr = (G / (G - 1)) * ((n_cases - 1) / max(n_cases - K, 1))
    V = corr * XtX_inv @ meat @ XtX_inv
    se_slope = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    slope = float(beta[1])
    t_slope = float(slope / se_slope) if np.isfinite(se_slope) and se_slope > 0 else 0.0

    # mean excess with day-clustered SE
    m = float(y.mean())
    dev_day = pd.Series(y - m).groupby(groups).sum().values
    se_m = float(np.sqrt((G / (G - 1)) * np.sum(dev_day ** 2)) / n_cases)
    t_mean = float(m / se_m) if se_m > 0 else 0.0
    counts["mean excess t"] = t_mean  # informative only (kept numeric)
    counts.pop("mean excess t")

    support_pass = bool(m > 0)

    if t_slope <= -2:
        status = "rejected"
        decided = "Reject: the slope's t is -2 or less."
    elif t_mean <= -2:
        status = "rejected"
        decided = "Reject: the mean excess return has a t of -2 or less (the falls continue)."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided = "Confirm: the slope's t is 2 or more and the mean excess return of the cases is positive."
    else:
        status = "inconclusive"
        if t_slope >= 2:
            decided = "Inconclusive: a positive slope (t >= 2) with a mean excess return of 0 or below."
        else:
            decided = "Inconclusive: the slope's t is between -2 and 2, and the mean excess t is above -2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "day-clustered slope t", "value": t_slope},
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 7-bar return of the cases > 0 (its day-clustered t: %.3f)" % t_mean,
                             "value": m, "passed": support_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
