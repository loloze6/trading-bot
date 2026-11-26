import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_decline.last_history_value"
    MIN_CASES = 30
    MIN_DAYS = 20

    def raw_from_prices(df):
        close = df["close"].astype(float)
        ret14 = close / close.shift(14) - 1.0
        std30 = close.pct_change().rolling(30, min_periods=30).std()
        return ret14 / (std30 * np.sqrt(14.0))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), raw_from_prices(df))
            else:
                raw = raw_from_prices(df)
            in_profile = df["regime"].astype(str) == "unknown"
            situation = in_profile & (raw < 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "slope of 5-day excess return on forecast (forecast < 0, day-clustered)"
    threshold = "confirm: slope > 0 with t >= 2 (and mean excess < 0); reject: slope < 0 with t <= -2"
    sup_name = "mean 5-day excess return on the forecast < 0 grid bars"
    reading = ("The falling calm profile is read from the recorded regime (regime 'unknown', the only regime "
               "with a strategy, i.e. both vetoes not triggered) and the decline from the raw scaled 14-day return "
               "< 0, expected side short; the coin's mean 5-day return is the mean over its non-overlapping grid "
               "(positions 0, 5, 10, ... of each window) of all windows; the slope is OLS with intercept and "
               "day-clustered standard errors with the usual G/(G-1)*(N-1)/(N-K) correction; minimum counts not "
               "reached give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars in the falling calm "
                           "profile with a negative scaled 14-day return, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_rows.append((ts.iloc[i].floor("D").strftime("%Y-%m-%d"), float(fc[i]), r))
        if len(coin_grid_rets) == 0:
            continue
        drift = float(np.mean(coin_grid_rets))
        for day, f, r in coin_rows:
            rows.append((day, f, r - drift))

    n_cases = len(rows)
    days = sorted(set(r[0] for r in rows))
    n_days = len(days)
    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}
    sit = {"agreement": (float(agreement) if agreement is not None else None), "passed": True}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        mean_ex = float(np.mean([r[2] for r in rows])) if n_cases > 0 else None
        return {
            "status": "not observable",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": mean_ex,
                                 "passed": (bool(mean_ex < 0) if mean_ex is not None else None)},
            "counts": counts,
            "decided_by": (f"The plan needs at least {MIN_CASES} grid cases on at least {MIN_DAYS} distinct days; "
                           f"the record has {n_cases} cases on {n_days} days."),
            "reading": reading,
        }

    day_arr = np.array([r[0] for r in rows])
    f = np.array([r[1] for r in rows], dtype=float)
    y = np.array([r[2] for r in rows], dtype=float)
    mean_ex = float(np.mean(y))
    sup_pass = bool(mean_ex < 0)

    X = np.column_stack([np.ones(n_cases), f])
    XtX = X.T @ X
    slope = None
    t = None
    if np.linalg.matrix_rank(XtX) == 2:
        XtX_inv = np.linalg.inv(XtX)
        beta = XtX_inv @ (X.T @ y)
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for d in days:
            m = day_arr == d
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
        G = n_days
        K = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else 0.0
        slope = float(beta[1])
        if se > 0:
            t = float(slope / se)

    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its clustered t cannot be computed (no spread in the forecast), so neither rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Confirm: the slope is positive with t >= 2 and the mean 5-day excess return on the same bars "
                       "is below 0.")
        else:
            status = "inconclusive"
            decided = "Inconclusive: a confirming slope (t >= 2) but a mean excess return >= 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope has |t| < 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "day-clustered OLS t of the slope", "value": t}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": mean_ex, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
