import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.day_fall.last_history_value"

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            unit = "ms" if s.abs().max() > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    frames = []
    coin_mean = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = to_time(d["timestamp"])
            close = d["close"].astype(float)
            d["next_ret"] = close.shift(-1) / close - 1.0  # inside the window only
            # raw 1-bar percent change: recorded value, or recomputed from prices where not recorded
            raw = d[LHV].astype(float) if LHV in d.columns else pd.Series(np.nan, index=d.index)
            recomputed = close / close.shift(1) - 1.0
            d["raw"] = raw.where(raw.notna(), recomputed)
            d["coin"] = coin
            d["window"] = w
            all_rets.append(d["next_ret"].dropna())
            frames.append(d)
        r = pd.concat(all_rets) if all_rets else pd.Series(dtype=float)
        coin_mean[coin] = float(r.mean()) if len(r) else np.nan

    if not frames:
        data = pd.DataFrame(columns=["forecast", "raw", "regime", "next_ret", "coin", "ts"])
    else:
        data = pd.concat(frames, ignore_index=True)

    data["forecast"] = data["forecast"].astype(float)

    # ---- situation check: a one-day fall, in the agitated profile (regime not chop), held long ----
    active = data[data["forecast"].fillna(0) != 0]
    n_active = len(active)
    if n_active > 0:
        regime = active["regime"].astype(str).str.lower()
        in_sit = (active["raw"] < 0) & (regime != "chop") & (active["forecast"] > 0)
        agreement = float(in_sit.sum()) / n_active
    else:
        agreement = None
    passed = agreement is None or agreement >= 0.9

    main_name = "slope of (next-day return minus coin mean daily return) on forecast, bars with forecast > 0"
    threshold = "slope t >= 2 (with supporting mean > 0) confirms; slope t <= -2 rejects"
    sup_name = "mean next-day return minus coin mean daily return on bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": int((data["forecast"] > 0).sum()), "active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars on a one-day fall in the agitated (non-chop) profile, as the plan's Fidelity requires.",
            "reading": "The situation is a negative raw 1-bar change (recorded, or recomputed from closes where missing) on a non-chop regime bar, with a positive forecast.",
        }

    # ---- criterion ----
    s = data[(data["forecast"] > 0)].copy()
    s["cm"] = s["coin"].map(coin_mean)
    s["y"] = s["next_ret"] - s["cm"]
    s = s.dropna(subset=["y", "forecast"])
    n = int(len(s))
    s["day"] = s["ts"].dt.floor("D")
    n_days = int(s["day"].nunique()) if n else 0

    slope = None
    t_val = None
    sup_mean = None
    if n >= 1:
        sup_mean = float(s["y"].mean())
    if n >= 3 and s["forecast"].nunique() > 1 and n_days >= 2:
        X = np.column_stack([np.ones(n), s["forecast"].values])
        y = s["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in s.groupby("day").indices.items():
            g = X[idx].T @ u[idx]
            meat += np.outer(g, g)
        G = n_days
        k = 2
        corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_val = float(slope / se) if se and np.isfinite(se) and se > 0 else None

    sup_passed = None if sup_mean is None else bool(sup_mean > 0)
    counts = {"bars with forecast > 0 across all coins and windows": n, "days": n_days}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} bars with forecast > 0 across all coins and windows, below the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_mean is not None and sup_mean > 0:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the supporting mean is above 0 (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting mean is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_val is None else {"name": "OLS slope t, day-clustered standard errors", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_mean, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": "The regression has an intercept and its slope t uses cluster-robust (sandwich) standard errors with cases grouped by UTC day and the usual G/(G-1)*(N-1)/(N-K) correction; the coin's mean daily return is the mean of all its 1-bar returns over all its windows, and the 1-bar horizon makes every bar its own non-overlapping case.",
    }
