import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    RAW = "debug_info.components.fall_in_usual_moves.last_history_value"

    def to_day(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            dt = pd.to_datetime(s, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            close = pd.to_numeric(df["close"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            # where the raw value is missing, its sign is the sign of the latest day's return
            r1 = np.full(len(df), np.nan)
            r1[1:] = close[1:] / close[:-1] - 1.0
            raw = np.where(np.isnan(raw), r1, raw)
            active = np.isfinite(fc) & (fc != 0)
            agree = active & np.isfinite(raw) & (raw < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of excess 2-day return on forecast (forecast > 0, non-overlapping grid)"
    thr = "slope t >= 2 confirms (with positive mean excess), t <= -2 rejects; day-clustered t"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are down days (negative vol-scaled "
                           "1-day return) with a positive (long) forecast, as the Fidelity's situation and side require."),
            "reading": "Situation = latest day's vol-scaled return below 0 (raw component value), expected side long.",
        }

    # ---------- 2. criterion ----------
    rows = []  # (coin, fc, ret, day)
    grid_all = {}  # coin -> list of all grid returns (for drift)
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            days = to_day(df["timestamp"])
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, fc[i], r, days[i]))
        grid_all[coin] = allr
    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in grid_all.items()}

    if rows:
        d = pd.DataFrame(rows, columns=["coin", "f", "r", "day"])
        d["x"] = d["r"] - d["coin"].map(drift)
        d = d[np.isfinite(d["x"]) & np.isfinite(d["f"])]
    else:
        d = pd.DataFrame(columns=["coin", "f", "r", "day", "x"])

    n_cases = int(len(d))
    n_days = int(d["day"].nunique()) if n_cases else 0
    counts = {"grid bars with forecast above 0": n_cases, "distinct days": n_days}

    slope = None
    t_slope = None
    mean_ex = float(d["x"].mean()) if n_cases else None
    if n_cases >= 3 and n_days >= 2 and d["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), d["f"].values.astype(float)])
        y = d["x"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in d.reset_index(drop=True).groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = n_days
        k = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_passed = None if mean_ex is None else bool(mean_ex > 0)

    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} grid bars with forecast above 0 (need 200) "
                   f"over {n_days} distinct days (need 100).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess 2-day return is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess 2-day return is not positive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t, day-clustered (CR1)", "value": t_slope},
            "threshold": thr,
        },
        "supporting_check": {"name": "mean excess 2-day return on grid bars with forecast > 0 is above 0",
                             "value": mean_ex, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid at positions 0,2,4,... of each window with a full 2-bar return inside it; normal drift = "
                    "coin's mean 2-day return over all its grid bars in all windows; regression with intercept, slope t "
                    "from day-clustered (UTC date of the bar) CR1 standard errors; the plan's 'fewer is inconclusive' "
                    "minimum is reported as 'not observable' per the workflow rule."),
    }
