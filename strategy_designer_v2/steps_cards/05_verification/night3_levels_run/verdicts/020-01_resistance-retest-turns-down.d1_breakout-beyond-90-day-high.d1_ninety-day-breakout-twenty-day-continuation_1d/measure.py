import numpy as np
import pandas as pd

H = 20
MIN_CASES = 30
RAW = "debug_info.components.beyond_high.last_history_value"
PPV = "debug_info.components.beyond_high.post_pipeline_value"


def _raw_distance(df):
    """Raw percent distance above the prior 90-bar closing high, from the record or recomputed from the window's closes."""
    close = df["close"].astype(float).reset_index(drop=True)
    if RAW in df.columns:
        raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
    else:
        raw = pd.Series(np.nan, index=close.index)
    prior_high = close.shift(1).rolling(90, min_periods=90).max()
    recomputed = (close - prior_high) / prior_high * 100.0
    return raw.where(raw.notna(), recomputed)


def _t_of_mean(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return None
    sd = x.std(ddof=1)
    if not np.isfinite(sd) or sd == 0:
        return None
    return float(x.mean() / (sd / np.sqrt(n)))


def measure(bars):
    # ---------- 1. situation check ----------
    active_total = 0
    active_ok = 0
    for coin in sorted(bars):
        for win in sorted(bars[coin]):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            raw = _raw_distance(df)
            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw > 0)
            active_total += int(active.sum())
            active_ok += int((active & situation & (fc > 0)).sum())
    agreement = float(active_ok / active_total) if active_total > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "ordinary t of mean of post_pipeline_value x drift-adjusted 20-bar forward return, positive-forecast 20-bar grid bars"
    main_threshold = "confirm if t >= 2 with >= 30 cases and supporting check passes; reject if t <= -2 with >= 30 cases"
    sup_name = "upper-half minus lower-half (by forecast) mean drift-adjusted 20-bar return, positive-forecast grid bars"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"active bars": active_total, "active bars in situation on long side": active_ok},
            "decided_by": ("The plan's situation is a close above the prior 90-day closing high, held long; "
                           "fewer than 90% of the bars with a non-zero forecast are such bars with a positive forecast"
                           if active_total > 0 else
                           "No bar has a non-zero forecast, so the config never takes the plan's situation on its long side"),
            "reading": "Situation taken as raw beyond_high distance > 0 (recomputed from the window's closes where missing), side long.",
        }

    # ---------- 2. criterion ----------
    rows = []  # (coin, forecast, ppv, fwd)
    coin_drift = {}
    for coin in sorted(bars):
        all_fwd = []
        coin_rows = []
        for win in sorted(bars[coin]):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ppv = (pd.to_numeric(df[PPV], errors="coerce").to_numpy(dtype=float)
                   if PPV in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                fwd = c1 / c0 - 1.0
                all_fwd.append(fwd)
                coin_rows.append((fc[t], ppv[t], fwd))
        coin_drift[coin] = float(np.mean(all_fwd)) if all_fwd else np.nan
        for f, p, r in coin_rows:
            rows.append((coin, f, p, r))

    prods, fcs, adjs = [], [], []
    for coin, f, p, r in rows:
        if not np.isfinite(f) or f <= 0:
            continue
        d = coin_drift[coin]
        if not (np.isfinite(p) and np.isfinite(r) and np.isfinite(d)):
            continue
        adj = r - d
        prods.append(p * adj)
        fcs.append(f)
        adjs.append(adj)

    n_cases = len(prods)
    mean_prod = float(np.mean(prods)) if n_cases > 0 else None
    t = _t_of_mean(prods)

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        order = np.argsort(np.asarray(fcs), kind="mergesort")
        a = np.asarray(adjs)[order]
        half = n_cases // 2
        lower = a[:half]
        upper = a[n_cases - half:]
        sup_val = float(upper.mean() - lower.mean())
        sup_pass = bool(sup_val > 0)

    reading = ("Grid = rows 0, 20, 40, ... of each window with a full 20-bar forward return inside the window; "
               "the coin's mean 20-bar return is the mean over all its grid bars of all windows; halves split by "
               "sorted forecast into the bottom and top n//2 cases (the middle case dropped when n is odd); "
               "fewer than 30 cases is reported as 'not observable'.")

    counts = {"positive-forecast grid cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} positive-forecast grid cases across all coins and windows, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean product could not be computed (zero dispersion), so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main-measure t is 2 or more with at least 30 cases and the supporting upper-minus-lower difference is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The main-measure t is -2 or less with at least 30 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main-measure t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_prod,
                         "statistic": ({"name": "ordinary t of the mean", "value": t} if t is not None else None),
                         "threshold": main_threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
