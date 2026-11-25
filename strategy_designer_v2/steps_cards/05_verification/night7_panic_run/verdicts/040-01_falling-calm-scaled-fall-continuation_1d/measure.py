import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        unit = "ms" if v.abs().max() > 1e11 else "s"
        d = pd.to_datetime(v, unit=unit, utc=True)
    else:
        d = pd.to_datetime(s, utc=True)
    return d.dt.strftime("%Y-%m-%d").values


def _cluster_mean_t(x, days):
    x = np.asarray(x, float)
    n = len(x)
    if n < 2:
        return float(np.mean(x)) if n else None, None
    m = x.mean()
    dev = pd.Series(x - m).groupby(np.asarray(days)).sum().values
    g = len(dev)
    if g < 2:
        return float(m), None
    var = (g / (g - 1.0)) * np.sum(dev ** 2) / n ** 2
    if var <= 0:
        return float(m), None
    return float(m), float(m / np.sqrt(var))


def _cluster_slope_t(y, x, days):
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    n = len(y)
    if n < 3 or np.var(x) == 0:
        return None, None
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    sc = pd.DataFrame(X * e[:, None]).groupby(np.asarray(days)).sum().values
    g = sc.shape[0]
    if g < 2:
        return float(beta[1]), None
    meat = sc.T @ sc
    V = (g / (g - 1.0)) * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else None
    if not se:
        return float(beta[1]), None
    return float(beta[1]), float(beta[1] / se)


def measure(bars):
    H = 3
    raw_col = "debug_info.components.scaled_fall.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fall back on the 3-day return from prices where the raw value is not recorded
            ret3 = close / close.shift(H) - 1.0
            fall = np.where(raw.notna(), raw < 0, ret3 < 0)
            calm_falling = (df["regime"].astype(str) == "unknown").values
            active = (fc.notna() & (fc != 0)).values
            situ = calm_falling & fall & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean sign-flipped drift-removed 3-bar return after forecast < 0 (grid 0,3,6,...)"
    main_thr = "mean > 0 with day-clustered t >= 2 to confirm; t <= -2 rejects"
    sup_name = "OLS slope of drift-removed 3-bar return on forecast (day-clustered t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars after a 3-day fall "
                          "inside the falling calm profile (regime 'unknown'), as the Fidelity requires.",
            "reading": "Falling calm is read as the detector's regime 'unknown' (no veto fired) and the 3-day fall "
                       "as a negative raw scaled_fall value (3-day price return where it is not recorded).",
        }

    # ---------- criterion ----------
    ys, xs, ds = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        cand = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = _to_day(df["timestamp"])
            n = len(df)
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                grid_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    cand.append((r, fc[t], days[t]))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, f, d in cand:
            ys.append(r - drift)
            xs.append(f)
            ds.append(d)

    ys = np.asarray(ys, float)
    xs = np.asarray(xs, float)
    n_cases = int(len(ys))
    n_days = int(len(set(ds)))
    counts = {"cases": n_cases, "distinct days": n_days}

    vals = -ys
    mean, t_mean = _cluster_mean_t(vals, ds) if n_cases else (None, None)
    slope, t_slope = _cluster_slope_t(ys, xs, ds) if n_cases else (None, None)

    reading = ("Cases with no close 3 bars later in the same window are left out; the coin's drift is the mean of "
               "its non-overlapping 3-bar returns on the 0,3,6,... grid of all its windows; day clustering uses "
               "per-day sums of deviations (scores) with a G/(G-1) correction; the slope is fitted on the "
               "unflipped drift-removed return with an intercept.")

    sup_pass = None
    if slope is not None and t_slope is not None:
        sup_pass = bool(slope > 0 and t_slope >= 2)

    main = {"name": main_name, "value": mean,
            "statistic": {"name": "t of the mean, day-clustered", "value": t_mean} if t_mean is not None else None,
            "threshold": main_thr}
    sup = {"name": sup_name, "value": slope, "passed": sup_pass}
    if t_slope is not None:
        sup["t"] = t_slope

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"Minimum count not reached: {n_cases} cases (need 30) on {n_days} distinct days (need 30)."
    elif (mean is not None and t_mean is not None and mean > 0 and t_mean >= 2 and sup_pass):
        status = "confirmed"
        decided = "Confirm rule: mean above 0 with t >= 2, and the supporting slope above 0 with t >= 2."
    elif (t_mean is not None and t_mean <= -2) or (t_slope is not None and t_slope <= -2):
        status = "rejected"
        decided = "Reject rule: the main measure's t <= -2 or the supporting slope's t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: neither the confirm nor the reject rule is met (t between -2 and 2 on a measure, or a failed supporting check)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
