import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_change.last_history_value"
    RISING_REGIME = "unknown"  # the config's only regime with a strategy: the "rising" profile (60-bar price evolution > 10)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values
            # raw log volume ratio: recorded value, else recomputed from the window's volume
            vol = pd.to_numeric(df["volume"], errors="coerce")
            m_short = vol.rolling(30, min_periods=30).mean()
            m_prior = m_short.shift(30)
            with np.errstate(divide="ignore", invalid="ignore"):
                recomputed = np.log(m_short / m_prior)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed).values
            else:
                raw = recomputed.values
            active = fc != 0
            n_active += int(active.sum())
            in_profile = regime == RISING_REGIME
            expected = -np.sign(raw)  # long when volume shrank, short when it grew
            ok = active & in_profile & np.isfinite(raw) & (np.sign(fc) == expected) & (expected != 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None and agreement >= 0.9)
    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are rising-profile bars where the forecast's sign is the opposite of the 30/30-day log volume ratio's sign (long after shrinking volume, short after growing volume).",
            "reading": "The rising profile is read from the recorded regime (the config's only strategy regime, 'unknown', outside the 'chop' veto of 60-bar price evolution <= 10), and the expected side is minus the sign of the raw log volume ratio.",
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    cases.append((r, float(fc[i]), ts.iloc[i].floor("D")))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, f, d in cases:
            ys.append(r - drift)
            xs.append(f)
            days.append(d)

    n_cases = len(ys)
    n_days = len(set(days))
    counts = {"non-overlapping in-profile cases": int(n_cases), "days": int(n_days)}
    name = "slope of 5-day forward return minus coin drift on forecast (non-overlapping grid, non-zero forecast)"
    thr = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; at least 200 cases"
    reading = ("The rising profile is the recorded regime 'unknown' (the config's only strategy regime); cases are the "
               "grid bars at positions 0,5,10,... of each window with a full 5-bar forward return in the window and a "
               "non-zero forecast; the coin's drift is the mean of all its grid 5-day returns over all windows; the slope "
               "comes from OLS with an intercept and its t uses standard errors clustered by UTC day.")

    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed) if n_active > 0 else None}

    if n_cases < 200:
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": {"name": name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 200 non-overlapping in-profile cases, the plan's minimum count.",
            "reading": reading,
        }

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    X = np.column_stack([np.ones_like(x), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    e = y - X @ beta
    day_codes = pd.factorize(pd.Series(days))[0]
    G = int(day_codes.max()) + 1
    k = X.shape[1]
    meat = np.zeros((k, k))
    for g in range(G):
        idx = day_codes == g
        s = X[idx].T @ e[idx]
        meat += np.outer(s, s)
    corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k)) if G > 1 and n_cases > k else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else float("nan")
    slope = float(beta[1])
    t = slope / se if np.isfinite(se) and se > 0 else float("nan")

    if np.isfinite(t) and slope > 0 and t >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2: rises are larger after shrinking volume and smaller after growing volume, beyond the coin's drift."
    elif np.isfinite(t) and slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: rises are larger after growing volume."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2, with at least 200 cases."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": {
            "name": name,
            "value": slope,
            "statistic": {"name": "slope t, clustered by day", "value": (float(t) if np.isfinite(t) else None)},
            "threshold": thr,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
