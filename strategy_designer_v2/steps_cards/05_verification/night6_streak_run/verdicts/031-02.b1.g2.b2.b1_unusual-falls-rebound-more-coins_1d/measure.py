import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. Situation check: a fall on the latest day -> long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # situation: the latest day's return is a fall (raw scaled return < 0);
            # where the raw value is missing, rebuild the sign from the prices
            fall = np.where(raw.notna(), raw < 0, ret1 < 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(fall, index=d.index) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "day-clustered t of the slope of 2-day forward return minus normal drift on forecast (forecast > 0, non-overlapping 2-bar grid)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 cases over at least 50 days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in the situation on the long side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars after a down day, the plan's situation and side.",
            "reading": "Situation taken as a negative raw scaled return (price return where the raw value is missing), side long.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_rows.append((ts.iloc[i].floor("D"), fc[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for day, f, r in coin_rows:
            rows.append((day, f, r - drift))

    n_cases = len(rows)
    days = pd.Series([r[0] for r in rows]) if rows else pd.Series([], dtype="datetime64[ns, UTC]")
    n_days = int(days.nunique()) if n_cases else 0
    counts = {"cases with forecast > 0": n_cases, "distinct days": n_days}

    slope = None
    tval = None
    if n_cases >= 3 and n_days >= 2:
        x = np.array([r[1] for r in rows], dtype=float)
        y = np.array([r[2] for r in rows], dtype=float)
        X = np.column_stack([np.ones(n_cases), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            codes = pd.factorize(days)[0]
            G = int(codes.max()) + 1
            meat = np.zeros((2, 2))
            for g in range(G):
                m = codes == g
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            K = 2
            c = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if n_cases > K else 1.0
            V = c * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = ("The plan's minimum of 100 cases with forecast > 0 spread over at least 50 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with a day-clustered t of 2 or more, on at least 100 cases over at least 50 days (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with a day-clustered t of -2 or less, on at least 100 cases over at least 50 days (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's day-clustered t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": tval,
            "statistic": {"name": "day-clustered t of the OLS slope", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": ("OLS with intercept of excess 2-day return on forecast over grid bars (positions 0, 2, 4, ... of each window with a "
                    "forward close in the window) with forecast > 0, the normal drift being the coin's mean 2-day return over all its "
                    "windows' grid bars, day-clustered standard errors with the usual CR1 small-sample correction, and the plan's "
                    "too-few-cases case reported as 'not observable' as the workflow requires."),
    }
