import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    ER_P = 30
    ER_MAX = 0.3
    RAW = "debug_info.components.scaled_move.last_history_value"

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            # efficiency ratio from prices: |close[t]-close[t-30]| / sum |daily moves| over 30 bars
            er = np.full(n, np.nan)
            ad = np.abs(np.diff(close))
            for t in range(ER_P, n):
                den = ad[t - ER_P:t].sum()
                if den > 0:
                    er[t] = abs(close[t] - close[t - ER_P]) / den
            # raw scaled move: recorded raw value, else recomputed 7-bar return sign
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(n, np.nan)
            ret7 = np.full(n, np.nan)
            for t in range(H, n):
                ret7[t] = close[t] / close[t - H] - 1.0
            side_val = np.where(np.isfinite(raw), raw, ret7)
            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                if np.isfinite(er[t]):
                    in_sit = er[t] <= ER_MAX + 1e-9
                else:
                    in_sit = reg[t] == "mean_reversion"
                sv = side_val[t]
                right_side = np.isfinite(sv) and sv != 0 and np.sign(sv) == np.sign(fc[t])
                if in_sit and right_side:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "slope of 7-bar excess forward return on forecast (grid cases, day-clustered)"
    thr = "confirm: slope > 0 with t >= 2 and supporting check > 0; reject: slope < 0 with t <= -2"
    reading = ("The 30-bar efficiency ratio is recomputed from each window's closes and, on a window's first 30 bars "
               "where it cannot be, the recorded regime stands in; the side is the sign of the recorded raw scaled move "
               "(7-bar return where missing); the slope's t uses day-clustered standard errors, and the supporting "
               "check uses the same grid cases with excess return signed by the forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": fnum(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are bars with 30-bar efficiency ratio <= 0.3 "
                           "and a forecast sign matching the sign of the scaled 7-day move (continuation)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        # normal drift: mean 7-bar return on non-overlapping grid of all windows
        all_r = []
        per_w = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = df["close"].astype(float).values
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r):
                    all_r.append(r)
            per_w.append(df)
        if not all_r:
            continue
        drift = float(np.mean(all_r))
        for df in per_w:
            n = len(df)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(0, n - H, H):
                if reg[t] != "mean_reversion":
                    continue
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append((coin, ts.iloc[t].floor("D"), float(f), r - drift))

    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)
    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}

    slope = None
    tstat = None
    sup_val = None
    if n_cases >= 3:
        f = np.array([r[2] for r in rows])
        y = np.array([r[3] for r in rows])
        d = [r[1] for r in rows]
        sup_val = float(np.mean(np.sign(f) * y))
        X = np.column_stack([np.ones(n_cases), f])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtXi = np.linalg.inv(XtX)
            beta = XtXi @ X.T @ y
            u = y - X @ beta
            dser = pd.Series(range(n_cases), index=pd.Index(d))
            meat = np.zeros((2, 2))
            groups = {}
            for i, g in enumerate(d):
                groups.setdefault(g, []).append(i)
            for g in sorted(groups):
                idx = groups[g]
                s = X[idx].T @ u[idx]
                meat += np.outer(s, s)
            G = len(groups)
            k = 2
            if G > 1 and n_cases > k:
                c = (G / (G - 1)) * ((n_cases - 1) / (n_cases - k))
                V = c * XtXi @ meat @ XtXi
                se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
                slope = float(beta[1])
                tstat = float(beta[1] / se) if np.isfinite(se) and se > 0 else None
            else:
                slope = float(beta[1])
    elif n_cases > 0:
        f = np.array([r[2] for r in rows])
        y = np.array([r[3] for r in rows])
        sup_val = float(np.mean(np.sign(f) * y))

    sup_pass = None if sup_val is None else bool(sup_val > 0)

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum of 30 grid cases on 30 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean unusual move in the signal's direction is above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: scaled moves are followed by moves the other way."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": fnum(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": fnum(slope),
                         "statistic": ({"name": "slope t (day-clustered)", "value": fnum(tstat)}
                                       if tstat is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move in signal's direction > 0",
                             "value": fnum(sup_val), "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
