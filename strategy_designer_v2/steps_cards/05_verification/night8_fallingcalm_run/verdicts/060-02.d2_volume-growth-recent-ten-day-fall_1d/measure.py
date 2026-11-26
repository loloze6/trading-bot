import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_growth.last_history_value"

    def _sign(x):
        return np.sign(x) if np.isfinite(x) else np.nan

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            vol = df["volume"].astype(float).values
            fc = df["forecast"].astype(float).values
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(len(df), np.nan)
            reg = df["regime"].astype(str).values
            for i in range(len(df)):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                # 10-day return below 0, from the prices inside the window;
                # before 10 bars of the window exist, the recorded regime stands in
                if i >= 10:
                    in_sit = (close[i] / close[i - 10] - 1.0) < 0
                else:
                    in_sit = reg[i] == "mean_reversion"
                if not in_sit:
                    continue
                # expected side: + when volume grew (log ratio > 0), - when it shrank
                r = raw[i]
                if not np.isfinite(r) and i >= 59:
                    recent = vol[i - 29:i + 1].mean()
                    before = vol[i - 59:i - 29].mean()
                    if recent > 0 and before > 0:
                        r = np.log(recent / before)
                s = _sign(r)
                if np.isfinite(s) and s != 0 and np.sign(fc[i]) == s:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of next 5-day return minus coin's mean 5-day return on the forecast"
    thr = "confirm: slope > 0 with t >= 2 on >= 100 cases; reject: slope < 0 with t <= -2 on >= 100 cases"
    reading = ("The situation is the 10-day close-to-close return below 0 computed inside each window "
               "(the recorded regime 'mean_reversion' stands in on a window's first 10 bars) and the side is the "
               "sign of the raw log volume ratio; the regression has an intercept, its t uses standard errors "
               "clustered by calendar day (CR1), the coin's mean 5-day return is taken on the non-overlapping grid "
               "of all its windows, and the plan's 100 cases is treated as a minimum count (not observable below it).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the 10-day return is "
                           "negative with the forecast on the side of the volume change, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df) - H, H):
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                ret = close[i + H] / close[i] - 1.0
                grid.append((ret, fc[i], ts.iloc[i].floor("D")))
        if not grid:
            continue
        mean_ret = float(np.mean([g[0] for g in grid]))
        for ret, f, day in grid:
            if np.isfinite(f) and f != 0:
                rows.append((ret - mean_ret, f, day))

    n = len(rows)
    days = len(set(r[2] for r in rows))
    counts = {"cases": int(n), "days": int(days)}

    slope = None
    tval = None
    if n >= 3:
        y = np.array([r[0] for r in rows], dtype=float)
        x = np.array([r[1] for r in rows], dtype=float)
        d = np.array([str(r[2]) for r in rows])
        X = np.column_stack([np.ones(n), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            meat = np.zeros((2, 2))
            groups = pd.Series(np.arange(n)).groupby(d).indices
            for _, idx in sorted(groups.items()):
                sg = X[idx].T @ e[idx]
                meat += np.outer(sg, sg)
            G = len(groups)
            if G > 1 and n > 2:
                c = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
                V = c * XtX_inv @ meat @ XtX_inv
                se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
                slope = float(beta[1])
                tval = float(slope / se) if np.isfinite(se) and se > 0 else None
            else:
                slope = float(beta[1])

    if n < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases is not reached ({n} cases)."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "Confirm rule: the slope is positive with t >= 2 on at least 100 cases."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule: the slope is negative with t <= -2 on at least 100 cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the t lies between -2 and 2 on at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t, day-clustered", "value": tval} if tval is not None else None,
            "threshold": thr,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
