import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.scaled_week.last_history_value"
    ER_P, R30_P, R7_P = 30, 30, 7

    def to_days(ts):
        s = pd.Series(ts)
        if np.issubdtype(s.dtype, np.number):
            unit = "ms" if s.abs().max() > 1e11 else "s"
            d = pd.to_datetime(s, unit=unit, utc=True)
        else:
            d = pd.to_datetime(s, utc=True)
        return d.dt.floor("D").astype("int64").values

    # ---------- coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check + collection of cases ----------
    n_active_checkable = 0
    n_agree = 0
    n_active_total = 0
    xs, ys, ss, days = [], [], [], []

    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df[FC], errors="coerce").values.astype(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
                   if RAW in df.columns else np.full(n, np.nan))
            d = to_days(df["timestamp"])
            absdiff = np.abs(np.diff(c, prepend=np.nan))

            for t in range(n):
                if not np.isfinite(f[t]) or f[t] == 0:
                    continue
                n_active_total += 1
                # situation (ER, r30 need 30 bars back inside the window)
                if t >= ER_P:
                    path = np.nansum(absdiff[t - ER_P + 1:t + 1])
                    net = abs(c[t] - c[t - ER_P])
                    er = net / path if path > 0 else np.nan
                    r30 = c[t] / c[t - R30_P] - 1.0
                    if np.isfinite(raw[t]):
                        r7s = np.sign(raw[t])
                    else:
                        r7s = np.sign(c[t] / c[t - R7_P] - 1.0)
                    if np.isfinite(er) and np.isfinite(r30):
                        n_active_checkable += 1
                        in_sit = (er < 0.3) and (np.sign(r30) == r7s) and (r7s != 0)
                        side_ok = np.sign(f[t]) == r7s  # continuation: up week -> long
                        if in_sit and side_ok:
                            n_agree += 1
                # case for the criterion
                if t + 1 < n and np.isfinite(c[t]) and np.isfinite(c[t + 1]) and np.isfinite(mu):
                    y = c[t + 1] / c[t] - 1.0 - mu
                    xs.append(f[t] / 10.0)
                    ys.append(y)
                    ss.append(np.sign(f[t]))
                    days.append(d[t])

    agreement = (n_agree / n_active_checkable) if n_active_checkable > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation checked only on active bars with 30 prior bars inside the same window "
               "(earlier bars cannot be recomputed from prices and are left out of the agreement); "
               "the regression is OLS with an intercept and a standard error clustered by UTC day; "
               "fewer than 100 active bars is reported as 'not observable' per the workflow's minimum-count rule.")

    threshold = "t >= 2 with positive supporting mean confirms; t <= -2 rejects; at least 100 active bars"
    mm_name = "slope of next-day excess return on forecast/10, active bars"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_total),
                       "active bars checkable": int(n_active_checkable)},
            "decided_by": ("Fewer than 90% of the checkable active bars are bars where the raw 30-day efficiency "
                           "ratio is below 0.3 and the 7-day and 30-day returns share a sign, with the forecast "
                           "on the 7-day return's side." if agreement is not None else
                           "No active bar could be checked against the plan's situation."),
            "reading": reading,
        }

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    s = np.asarray(ss, float)
    g = np.asarray(days)
    N = len(y)
    G = len(np.unique(g)) if N else 0
    counts = {"active bars": int(N), "days": int(G)}

    sup_val = float(np.mean(s * y)) if N else None
    sup_pass = (sup_val is not None) and (sup_val > 0)

    slope, tstat = None, None
    if N >= 3 and G >= 2 and np.var(x) > 0:
        X = np.column_stack([np.ones(N), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        e = y - X @ beta
        meat = np.zeros((2, 2))
        dfu = pd.DataFrame({"g": g, "a": X[:, 0] * e, "b": X[:, 1] * e}).groupby("g")[["a", "b"]].sum().values
        for row in dfu:
            meat += np.outer(row, row)
        K = 2
        corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K))
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    sc = {"agreement": float(agreement), "passed": True}
    mm = {"name": mm_name, "value": slope,
          "statistic": None if tstat is None else {"name": "OLS t, SE clustered by day", "value": tstat},
          "threshold": threshold}
    sup = {"name": "mean of sign(forecast) x next-day excess return", "value": sup_val, "passed": bool(sup_pass)}

    if N < 100:
        status = "not observable"
        decided = f"Only {N} active bars with a next-day return, below the plan's minimum of 100."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the supporting mean is positive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting mean is not positive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": mm,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
