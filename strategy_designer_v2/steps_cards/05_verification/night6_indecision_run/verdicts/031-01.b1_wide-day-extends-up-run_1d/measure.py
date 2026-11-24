import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    FC = "forecast"

    def to_day(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            unit = "ms" if s.abs().max() > 1e11 else "s"
            t = pd.to_datetime(s, unit=unit, utc=True)
        else:
            t = pd.to_datetime(s, utc=True)
        return t.dt.floor("D").astype(str).values

    # ---------- 1. Situation check ----------
    # The Fidelity situation is a 5-day close-to-close return above 0, and the outcome is a rise, so the side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret5 = close / close.shift(5) - 1.0
            fc = pd.to_numeric(df[FC], errors="coerce")
            active = fc.notna() & (fc != 0) & ret5.notna()
            n_active += int(active.sum())
            agree = active & (ret5 > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation check: the 5-bar return is computed inside each window from closes, and the first 5 bars of a "
               "window are left out because they have no 5-bar history; main measure: the trending regime is read from "
               "the record's regime column, the coin's mean 3-bar return is taken over the non-overlapping grid of all "
               "its bars in all windows, the t is an OLS slope t with standard errors clustered by UTC day, and the "
               "independent cases are the in-regime grid cases with a 3-bar forward return.")

    threshold = ("confirm if the slope is > 0 with t >= 2; reject if the slope is < 0 with t <= -2; "
                 "at least 200 independent cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope t of excess 3-bar return on forecast, clustered by day",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Only {:.1%} of the active bars are long bars with a positive 5-bar return, "
                           "under the 90 % the plan's situation (a 5-day up-run, long) requires.").format(agreement),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            reg = df["regime"].astype(str).values
            days = to_day(df["timestamp"])
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                all_rets.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]):
                    cases.append((r, float(fc[i]), days[i]))
        if not all_rets:
            continue
        mu = float(np.mean(all_rets))
        for r, f, d in cases:
            rows.append((r - mu, f, d, coin))

    n_cases = len(rows)
    days_arr = np.array([r[2] for r in rows]) if rows else np.array([])
    n_days = int(len(np.unique(days_arr))) if n_cases else 0
    counts = {"independent in-regime grid cases": n_cases, "days": n_days}

    slope = None
    tval = None
    if n_cases >= 3:
        y = np.array([r[0] for r in rows], dtype=float)
        x = np.array([r[1] for r in rows], dtype=float)
        X = np.column_stack([np.ones(n_cases), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            meat = np.zeros((2, 2))
            uniq, inv = np.unique(days_arr, return_inverse=True)
            G = len(uniq)
            for g in range(G):
                m = inv == g
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            K = 2
            corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if G > 1 else 1.0
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    main = {"name": "slope t of excess 3-bar return on forecast, clustered by day",
            "value": slope,
            "statistic": ({"name": "OLS slope t, day-clustered", "value": tval} if tval is not None else None),
            "threshold": threshold}

    if n_cases < 200:
        status = "not observable"
        decided = ("Only {} independent in-regime grid cases, below the plan's minimum of 200.").format(n_cases)
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = ("The slope is positive with t = {:.2f} >= 2 over {} independent cases (confirm rule).").format(tval, n_cases)
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = ("The slope is negative with t = {:.2f} <= -2 over {} independent cases (reject rule).").format(tval, n_cases)
    else:
        status = "inconclusive"
        decided = ("The slope's t = {:.2f} lies between -2 and 2 over {} cases (inconclusive rule).").format(tval, n_cases)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
