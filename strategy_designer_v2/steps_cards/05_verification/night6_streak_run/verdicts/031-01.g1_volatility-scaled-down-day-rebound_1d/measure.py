import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ret1 = pd.Series(close).pct_change()
            vol = ret1.rolling(60, min_periods=60).std()
            recomputed = (ret1 / vol).values
            if RAW in df.columns:
                raw = df[RAW].astype(float).values.copy()
                miss = np.isnan(raw)
                raw[miss] = recomputed[miss]
            else:
                raw = recomputed
            for i in range(len(df)):
                if fc[i] != 0 and not np.isnan(fc[i]):
                    n_active += 1
                    r = raw[i]
                    if np.isnan(r) and i > 0:
                        r = ret1.values[i]
                    if (not np.isnan(r)) and r < 0 and fc[i] > 0:
                        n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down days "
                           "(raw volatility-scaled return below 0) with a positive (long) forecast, "
                           "as the plan's situation and side require."),
            "reading": "The situation is a down day (raw scaled return < 0, recomputed from closes where not recorded) and the side is long.",
        }

    # ---------- 2. per-coin drift and usual 3-day move ----------
    stats = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1.0)
        rs = np.array(rs, dtype=float)
        rs = rs[~np.isnan(rs)]
        if len(rs) >= 2:
            stats[coin] = (float(np.mean(rs)), float(np.std(rs, ddof=1)))

    # ---------- 3. grid rows and cases ----------
    ys, xs, days = [], [], []
    case_moves, case_days = [], []
    for coin, wins in bars.items():
        if coin not in stats:
            continue
        drift, usual = stats[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            dates = ts.dt.strftime("%Y-%m-%d").values
            n = len(df)
            # grid rows for the slope
            for i in range(0, n - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isnan(r) or np.isnan(fc[i]) or usual <= 0:
                    continue
                ys.append((r - drift) / usual)
                xs.append(fc[i])
                days.append(dates[i])
            # cases: long-side rises of the forecast of >= 2 points
            is_case = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if np.isnan(f) or f <= 0:
                    low = 0.0
                    continue
                if f - low >= 2.0:
                    is_case[i] = True
                    low = f
                else:
                    low = min(low, f)
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if is_case[j]]
                if not idx:
                    continue
                j = idx[0]
                if j + H >= n:
                    continue
                r = c[j + H] / c[j] - 1.0
                if np.isnan(r):
                    continue
                case_moves.append(r - drift)
                case_days.append(dates[j])

    y = np.array(ys, dtype=float)
    x = np.array(xs, dtype=float)
    d = np.array(days)
    n_pos = int(np.sum(x > 0))
    n_grid = int(len(y))

    # ---------- 4. pooled OLS slope with day-clustered t ----------
    slope, tstat = None, None
    if n_grid >= 3 and np.var(x) > 0:
        X = np.column_stack([np.ones(n_grid), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        uniq, inv = np.unique(d, return_inverse=True)
        G = len(uniq)
        scores = np.zeros((G, 2))
        np.add.at(scores, inv, X * e[:, None])
        meat = scores.T @ scores
        V = XtX_inv @ meat @ XtX_inv
        if G > 1 and n_grid > 2:
            V *= (G / (G - 1.0)) * ((n_grid - 1.0) / (n_grid - 2.0))
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        tstat = float(slope / se) if se and not np.isnan(se) else None

    # ---------- 5. supporting check ----------
    n_cases = int(len(case_moves))
    sup_val = float(np.mean(case_moves)) if n_cases > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    # ---------- 6. decision ----------
    if n_pos < 100:
        status = "not observable"
        decided = f"Only {n_pos} grid bars have a forecast above 0, fewer than the plan's minimum of 100."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the cases' mean unusual move over 3 days is above 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: deeper falls are followed by weaker returns than the coin's drift."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the cases' mean unusual move is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "pooled OLS slope of drift-removed, usual-move-scaled 3-day return on forecast",
            "value": slope,
            "statistic": ({"name": "day-clustered t of slope", "value": tstat} if tstat is not None else None),
            "threshold": "t >= 2 confirms (with supporting check), t <= -2 rejects, between is inconclusive",
        },
        "supporting_check": {
            "name": "mean unusual 3-day move of long cases (forecast rises >= 2 points)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "grid bars with a forecast above 0": n_pos,
            "grid bars": n_grid,
            "cases": n_cases,
            "days with cases": int(len(set(case_days))),
            "days clustered": int(len(set(days))),
        },
        "decided_by": decided,
        "reading": ("The regression has an intercept and uses a CR1 day-clustered standard error on grid bars 0,3,6,... "
                    "of each window with a full 3-bar return, drift and usual move are the mean and std of those same "
                    "non-overlapping 3-day returns per coin over all windows, cases are read once per 3-bar grid cell "
                    "(first case in the cell), and the plan's 'fewer than 100 grid bars with a forecast above 0' is reported as not observable."),
    }
