import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_week.last_history_value"

    # ---------- 1. situation check: active bars must be up-weeks (raw > 0) with a long forecast ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret7 = close / close.shift(7) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # sign of the scaled return is the sign of the 7-day return; fall back on prices where raw is missing
            sit_val = raw.where(raw.notna(), ret7)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (sit_val > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess next-3-bar return on forecast (forecast > 0 grid cases, pooled)"
    threshold = "confirm: slope t >= 2 with mean excess return > 0; reject: slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are up-week bars (7-day return > 0) with a long forecast, "
                          "so the config does not trade the plan's situation on its side.",
            "reading": "The situation is read from the sign of the recorded raw scaled return (the 7-day return from prices where it is missing).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_rows.append((ts.iloc[i].normalize(), float(fc[i]), float(r)))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for d, f, r in coin_rows:
            rows.append((d, f, r - drift))

    n_cases = len(rows)
    days = [r[0] for r in rows]
    n_days = len(set(days))
    counts = {"grid cases with a positive forecast": int(n_cases), "distinct days": int(n_days)}

    slope = None
    t_slope = None
    mean_ex = None
    if n_cases >= 3:
        f = np.array([r[1] for r in rows])
        y = np.array([r[2] for r in rows])
        X = np.column_stack([np.ones(n_cases), f])
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        day_codes = pd.factorize(pd.Series(days))[0]
        G = int(day_codes.max()) + 1
        meat = np.zeros((2, 2))
        for g in range(G):
            m = day_codes == g
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
        k = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None
        mean_ex = float(np.mean(y))

    sup_pass = None if mean_ex is None else bool(mean_ex > 0)

    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided_by = (f"The plan's minimum of 200 grid cases with a positive forecast on at least 100 distinct days is not reached "
                      f"({n_cases} cases on {n_days} days).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "Slope t of 2 or more and a mean excess 3-bar return above 0: the plan's confirm rule."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "Slope t of -2 or less: the plan's reject rule."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "Slope t of 2 or more but a mean excess return of 0 or below: the plan's inconclusive rule."
    else:
        status = "inconclusive"
        decided_by = "Slope t between -2 and 2: the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "day-clustered OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 3-bar return (long) on the same cases",
            "value": mean_ex,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": "The slope is from an OLS of excess return on forecast with an intercept, its t from a day-clustered (CR1) sandwich "
                   "variance, the normal drift is each coin's mean non-overlapping 3-bar grid return over all its windows, and grid "
                   "bars without a full 3-bar return inside their window are left out.",
    }
