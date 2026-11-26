import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    RAW = "debug_info.components.rise14.last_history_value"

    active_total = 0
    active_ok = 0
    case_rows = []  # (date, coin, forecast, ret)
    coin_drift = {}

    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            regime = d["regime"].astype(str).to_numpy() if "regime" in d.columns else np.array([""] * len(d))
            # Friday-close bar: daily bar that opens on Friday UTC, closes at Friday's close; next bar is Saturday
            is_friday = (ts.dt.dayofweek == 4).to_numpy()

            # forward 2-bar return inside window
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0

            # situation check
            act = fc != 0
            situ = is_friday & (raw > 0) & (fc > 0)
            active_total += int(act.sum())
            active_ok += int((act & situ).sum())

            # coin drift: non-overlapping grid 0, H, 2H ...
            idx = np.arange(0, n - H, H)
            if len(idx):
                g = fwd[idx]
                grid_rets.extend(list(g[np.isfinite(g)]))

            # cases
            sel = is_friday & (regime == "trending") & (fc > 0) & np.isfinite(fwd)
            for i in np.where(sel)[0]:
                coin_cases.append((ts.iloc[i].strftime("%Y-%m-%d"), coin, float(fc[i]), float(fwd[i])))
        coin_drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        case_rows.extend(coin_cases)

    agreement = (active_ok / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    main_name = "clustered OLS slope of excess 2-bar return on forecast (Friday-close, forecast > 0)"
    thr = "slope t >= 2 confirms (with weighted mean excess > 0); slope t <= -2 rejects"
    reading = ("Friday-close bars are the daily bars opening on Friday UTC (next bar Saturday); all such bars with "
               "forecast > 0 in the trending regime are used (weekly cases never overlap), the coin's mean 2-bar return "
               "is taken on each window's non-overlapping 0,2,4,... grid pooled over windows, the slope t uses "
               "CR1 standard errors clustered by date, and the plan's minimum counts not reached give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Friday-close bars after a "
                           "positive 14-day volatility-scaled rise with a long forecast, as the Fidelity requires."),
            "reading": reading,
        }

    cdf = pd.DataFrame(case_rows, columns=["date", "coin", "f", "ret"])
    if len(cdf):
        cdf["drift"] = cdf["coin"].map(coin_drift)
        cdf["ex"] = cdf["ret"] - cdf["drift"]
        cdf = cdf.dropna(subset=["f", "ex"])
    n_cases = int(len(cdf))
    n_fridays = int(cdf["date"].nunique()) if n_cases else 0
    counts = {"cases with forecast > 0": n_cases, "distinct Fridays": n_fridays}

    slope = None
    tval = None
    wmean = None
    if n_cases >= 3:
        f = cdf["f"].to_numpy(dtype=float)
        y = cdf["ex"].to_numpy(dtype=float)
        X = np.column_stack([np.ones(n_cases), f])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            u = y - X @ beta
            groups = cdf["date"].to_numpy()
            meat = np.zeros((2, 2))
            G = 0
            for gval in np.unique(groups):
                m = groups == gval
                s = X[m].T @ u[m]
                meat += np.outer(s, s)
                G += 1
            if G > 1 and n_cases > 2:
                adj = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
                V = XtX_inv @ meat @ XtX_inv * adj
                se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
                slope = float(beta[1])
                tval = float(beta[1] / se) if np.isfinite(se) and se > 0 else None
        sw = f.sum()
        if sw > 0:
            wmean = float((y * f).sum() / sw)
    elif n_cases > 0:
        f = cdf["f"].to_numpy(dtype=float)
        y = cdf["ex"].to_numpy(dtype=float)
        if f.sum() > 0:
            wmean = float((y * f).sum() / f.sum())

    sup_pass = (wmean > 0) if wmean is not None else None
    supporting = {"name": "forecast-weighted mean excess 2-bar return > 0",
                  "value": wmean, "passed": sup_pass}
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "slope t, clustered by day", "value": tval} if tval is not None else None),
            "threshold": thr}

    if n_cases < 100 or n_fridays < 50:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases with forecast > 0 (need 100) over "
                   f"{n_fridays} distinct Fridays (need 50).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "A confirming slope t but a forecast-weighted mean excess return at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
