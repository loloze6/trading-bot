import numpy as np
import pandas as pd


RAW_COL = "debug_info.components.stretch.last_history_value"


def _cluster_ols(y, x, groups):
    """OLS of y on [1, x]; slope, its day-clustered t, and the number of clusters."""
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    n = len(y)
    if n < 3 or np.nanstd(x) == 0:
        return None, None, 0
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        return None, None, 0
    beta = XtX_inv @ (X.T @ y)
    e = y - X @ beta
    g = pd.Series(groups).astype(str).values
    uniq = pd.unique(g)
    G = len(uniq)
    if G < 2:
        return float(beta[1]), None, G
    meat = np.zeros((2, 2))
    for u in uniq:
        m = g == u
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    k = 2
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if n > k else 1.0
    V = corr * (XtX_inv @ meat @ XtX_inv)
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    t = float(beta[1] / se) if se and np.isfinite(se) and se > 0 else None
    return float(beta[1]), t, G


def measure(bars):
    H = 5

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            if RAW_COL in d.columns:
                raw = pd.to_numeric(d[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback sign from prices (inside the window only): close minus its 20-bar SMA
            sma = close.rolling(20, min_periods=20).mean()
            price_dist = close - sma
            dist = raw.where(raw.notna(), price_dist)
            below = dist < 0
            calm = regime.str.lower() != "chop"
            active = fc != 0
            situ = below & calm & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of 5-bar unusual return on depth -forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope < 0 with day-clustered t <= -2 to confirm; slope > 0 with t >= +2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of active bars are bars with the close below its 20-day SMA "
                           "in the calm profile with a short forecast"
                           if n_active > 0 else "The record has no active bar, so the plan's short in a calm stretch never shows."),
            "reading": "Calm profile read as regime other than 'chop'; below-average read from the stretch raw value, or close minus 20-bar SMA when not recorded.",
        }

    # ---------- 2. criterion ----------
    ys, xs, days = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f < 0:
                    day = ts.iloc[i]
                    cases.append((r, -f, str(day.date()) if pd.notna(day) else f"{coin}-{w}-{i}"))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for r, x, day in cases:
            ys.append(r - mu)
            xs.append(x)
            days.append(day)

    n_cases = len(ys)
    n_days = len(set(days))
    slope, t, _ = _cluster_ols(ys, xs, days) if n_cases >= 3 else (None, None, 0)
    mean_y = float(np.mean(ys)) if n_cases > 0 else None
    mean_unusual_short = -mean_y if mean_y is not None else None
    support_pass = (mean_unusual_short > 0) if mean_unusual_short is not None else None

    threshold = "confirm: slope < 0 with day-clustered t <= -2 and mean unusual move of shorts > 0; reject: slope > 0 with t >= +2"
    counts = {"grid cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = f"Minimum counts not reached: {n_cases} grid cases (need 100) on {n_days} distinct days (need 60)."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and t <= -2 and support_pass:
        status = "confirmed"
        decided = "The slope is negative with t <= -2 and the mean unusual move of the shorts is above 0."
    elif slope > 0 and t >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2."
    elif slope < 0 and t <= -2:
        status = "inconclusive"
        decided = "t <= -2 but the mean unusual move of the shorts is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "slope of 5-bar unusual return on depth -forecast",
                         "value": slope,
                         "statistic": ({"name": "day-clustered OLS t of slope", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move of short cases, in short direction",
                             "value": mean_unusual_short, "passed": support_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Both minimums are required (at least 100 grid cases and at least 60 distinct days), "
                    "the coin's mean 5-bar return is the mean of its non-overlapping grid returns over all its windows, "
                    "the t uses cluster-robust standard errors by UTC day of the signal bar, and the calm profile is regime other than 'chop'."),
    }
