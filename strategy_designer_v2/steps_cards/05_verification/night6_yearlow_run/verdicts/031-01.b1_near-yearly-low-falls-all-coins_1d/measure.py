import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RAW = "debug_info.components.low_prox.last_history_value"
    MIN_CASES = 100
    MIN_DATES = 30

    # ---------- 1. situation check ----------
    # Fidelity: situation = nearness of the close to its 365-day lowest close (graded, ungated),
    # outcome = a fall -> expected side short. The raw proximity 1/(1+D) is defined (and > 0)
    # on every bar where the situation can be read, so a bar of the situation on its side is an
    # active bar with a valid positive raw value and a negative forecast.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                in_sit = raw.notna() & np.isfinite(raw) & (raw > 0) & (raw <= 1.0 + 1e-9)
            else:
                in_sit = pd.Series(False, index=df.index)
            n_agree += int((active & in_sit & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of the 20-bar excess forward return on the forecast (non-overlapping grid)"
    main_thr = "confirm: slope > 0 with t >= 2 and top-quintile check passed; reject: slope < 0 with t <= -2"
    sup_name = "mean excess 20-bar return of the top quintile of |forecast| below 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation (nearness to the 365-day closing low, held short) "
                           "and the config's forecast disagree: fewer than 90 % of active bars carry "
                           "a valid proximity value with a negative (short) forecast."),
            "reading": "Active bars are bars with a non-zero forecast; a bar of the situation has a valid proximity in (0, 1] and a negative forecast.",
        }

    # ---------- 2. grid cases ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                coin_rows.append({
                    "coin": coin,
                    "date": ts.iloc[i].normalize(),
                    "ret": c1 / c0 - 1.0,
                    "fc": fc[i],
                })
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            cdf["excess"] = cdf["ret"] - cdf["ret"].mean()  # coin's mean 20-bar return over all its windows
            rows.append(cdf)

    if rows:
        cases = pd.concat(rows, ignore_index=True)
        cases = cases[np.isfinite(cases["fc"]) & np.isfinite(cases["excess"])]
    else:
        cases = pd.DataFrame(columns=["coin", "date", "ret", "fc", "excess"])

    n_cases = int(len(cases))
    n_dates = int(cases["date"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct dates": n_dates}

    reading = ("Grid = rows 0, 20, 40, ... of each window with the forward return inside the window; "
               "excess = return minus the coin's mean grid 20-bar return over all its windows; all grid cases with a "
               "forecast are used (zero forecasts included); OLS with intercept, t from date-clustered standard errors "
               "(cases of one date pooled, G/(G-1) correction); top quintile = cases with |forecast| at or above its 80th percentile.")

    if n_cases < MIN_CASES or n_dates < MIN_DATES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": (f"Minimum counts not reached: {n_cases} grid cases (need 100) on "
                           f"{n_dates} distinct dates (need 30)."),
            "reading": reading,
        }

    # ---------- 3. regression with date-clustered t ----------
    x = cases["fc"].to_numpy(dtype=float)
    y = cases["excess"].to_numpy(dtype=float)
    X = np.column_stack([np.ones_like(x), x])
    XtX = X.T @ X
    slope = None
    t = None
    try:
        XtX_inv = np.linalg.inv(XtX)
        beta = XtX_inv @ (X.T @ y)
        u = y - X @ beta
        scores = X * u[:, None]
        sdf = pd.DataFrame(scores, columns=["a", "b"])
        sdf["date"] = cases["date"].to_numpy()
        g = sdf.groupby("date")[["a", "b"]].sum().to_numpy()
        G = g.shape[0]
        meat = g.T @ g
        V = XtX_inv @ meat @ XtX_inv
        if G > 1:
            V = V * G / (G - 1)
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None
    except np.linalg.LinAlgError:
        pass

    # ---------- 4. supporting check ----------
    absf = np.abs(x)
    q80 = float(np.quantile(absf, 0.8))
    top = cases[absf >= q80]
    top_mean = float(top["excess"].mean()) if len(top) else None
    sup_pass = bool(top_mean is not None and top_mean < 0)
    counts["top-quintile cases"] = int(len(top))

    # ---------- 5. decision ----------
    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so no rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm rule: positive slope with t >= 2 and a negative top-quintile mean excess return."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: a confirming slope (t >= 2) whose supporting check fails (top-quintile mean excess return not below 0)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule: negative slope with t <= -2 (a deeper short is followed by a higher excess return)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "date-clustered OLS t of the slope", "value": t} if t is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": top_mean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
