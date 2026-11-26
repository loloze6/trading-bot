import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_move.last_history_value"
    MIN_CASES = 150

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # 5-day move from prices where the raw value is missing
            move = np.full(len(df), np.nan)
            if len(df) > H:
                move[H:] = close[H:] / close[:-H] - 1.0
            side_src = np.where(np.isfinite(raw), raw, move)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            choppy = regime == "unknown"
            active = fc != 0
            n_active += int(active.sum())
            ok = active & choppy & np.isfinite(side_src) & (np.sign(side_src) == np.sign(fc)) & (side_src != 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"grid cases with a nonzero forecast": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are bars of the choppy profile (regime 'unknown', "
                           "|60-day price evolution| <= 10) with a forecast of the same sign as the 5-day "
                           "volatility-scaled move."),
            "reading": "The choppy profile is read from the recorded regime 'unknown' (no chop veto); the expected side is the sign of the raw scaled move, or of the 5-day price move where it is not recorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    coin_rows.append((coin, ts.iloc[i].floor("D"), float(f), float(r)))
        if not all_grid_rets:
            continue
        drift = float(np.mean(all_grid_rets))
        for c, d, f, r in coin_rows:
            rows.append({"coin": c, "day": d, "f": f, "y": r - drift})

    n_cases = len(rows)
    counts = {"grid cases with a nonzero forecast": n_cases}
    reading = ("Grid of positions 0,5,10,... per window with a full 5-bar return inside the window; drift is the coin's "
               "mean 5-bar grid return over all its windows; slope t from OLS with intercept and standard errors "
               "clustered by UTC day; thirds are the n//3 cases with largest and smallest |forecast|; the choppy "
               "profile is the recorded regime 'unknown'.")
    mm_name = "pooled slope of drift-adjusted next 5-bar return on forecast"
    thr = "t >= 2 confirms (with supporting check), t <= -2 rejects"

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Fewer than {MIN_CASES} grid cases with a nonzero forecast ({n_cases}).",
            "reading": reading,
        }

    d = pd.DataFrame(rows)
    f = d["f"].values
    y = d["y"].values
    X = np.column_stack([np.ones(len(f)), f])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    groups = d["day"].values
    meat = np.zeros((2, 2))
    G = 0
    for g, idx in d.groupby("day").indices.items():
        s = X[idx].T @ e[idx]
        meat += np.outer(s, s)
        G += 1
    n, k = X.shape
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if G > 1 else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    slope = float(beta[1])
    t = float(slope / se) if np.isfinite(se) and se > 0 else float("nan")
    counts["days"] = int(G)

    # supporting check
    order = np.argsort(np.abs(f), kind="mergesort")
    m = n // 3
    signed = np.sign(f) * y
    bottom = signed[order[:m]]
    top = signed[order[-m:]] if m > 0 else np.array([])
    if m > 0:
        diff = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(diff > 0)
    else:
        diff, sup_pass = None, None
    counts["top third cases"] = int(m)
    counts["bottom third cases"] = int(m)

    if np.isfinite(t) and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom third difference is positive: confirm rule met."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger moves are followed by reversals (reject rule)."
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check failed: inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": slope,
                         "statistic": {"name": "slope t, clustered by day", "value": t if np.isfinite(t) else None},
                         "threshold": thr},
        "supporting_check": {"name": "top minus bottom third of |forecast|, mean sign(f) x drift-adjusted 5-bar return",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
