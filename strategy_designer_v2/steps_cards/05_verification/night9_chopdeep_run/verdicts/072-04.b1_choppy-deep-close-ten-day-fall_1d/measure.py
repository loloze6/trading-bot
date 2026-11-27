import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    DEPTH = "debug_info.components.depth.last_history_value"
    ACTIVE_REGIME = "unknown"  # the regime whose strategy runs: the 60-bar trend is within -10..+10, i.e. choppy

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if not active.any():
                continue
            reg = df["regime"].astype(str).str.strip().str.lower()
            choppy = reg == ACTIVE_REGIME
            if DEPTH in df.columns:
                depth = pd.to_numeric(df[DEPTH], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=df.index)
            below_high = depth < 0
            short_side = f < 0
            situ = choppy & below_high & short_side
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {
                "name": "slope of drift-removed 10-bar return on forecast",
                "value": None,
                "statistic": None,
                "threshold": "positive with t >= 2 confirms (with check); negative with t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"grid cases with a nonzero forecast": 0},
            "decided_by": "No bar has a nonzero forecast, so fewer than 100 grid cases with a nonzero forecast exist.",
            "reading": "With no active bar the situation check cannot be computed.",
        }

    agreement = n_agree / n_active
    passed_situ = agreement >= 0.9
    if not passed_situ:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "slope of drift-removed 10-bar return on forecast",
                "value": None,
                "statistic": None,
                "threshold": "positive with t >= 2 confirms (with check); negative with t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": None,
            "decided_by": (
                "Fewer than 90% of the active bars are choppy-regime bars with the close below its 20-day high "
                "and a short forecast, as the plan's Fidelity requires."
            ),
            "reading": "The choppy profile is read from the recorded regime ('unknown', the only regime with a strategy) "
                       "and the depth from the recorded raw value being negative.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append({
                    "coin": coin,
                    "ret": c1 / c0 - 1.0,
                    "f": fc[p],
                    "day": ts.iloc[p].floor("D"),
                })
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            drift = cdf["ret"].mean()  # coin's mean 10-bar return over all windows (all grid cases)
            cdf["ex"] = cdf["ret"] - drift
            rows.append(cdf)

    if rows:
        g = pd.concat(rows, ignore_index=True)
        g = g[np.isfinite(g["f"]) & (g["f"] != 0) & np.isfinite(g["ex"])]
    else:
        g = pd.DataFrame(columns=["coin", "ret", "f", "day", "ex"])

    n_cases = int(len(g))
    n_days = int(g["day"].nunique()) if n_cases else 0

    slope = None
    tval = None
    if n_cases >= 3:
        x = g["f"].to_numpy(float)
        y = g["ex"].to_numpy(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX = X.T @ X
        try:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            u = y - X @ beta
            meat = np.zeros((2, 2))
            days = g["day"].to_numpy()
            for d in pd.unique(days):
                m = days == d
                s = X[m].T @ u[m]
                meat += np.outer(s, s)
            G = len(pd.unique(days))
            N, K = X.shape
            corr = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 and N > K else 1.0
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None
        except np.linalg.LinAlgError:
            slope, tval = None, None

    deep = g.loc[g["f"] <= -10, "ex"]
    shallow = g.loc[(g["f"] > -10) & (g["f"] < 0), "ex"]
    n_deep, n_shallow = int(len(deep)), int(len(shallow))
    if n_deep > 0 and n_shallow > 0:
        diff = float(deep.mean() - shallow.mean())
        check_passed = bool(diff < 0)
    else:
        diff = None
        check_passed = None

    counts = {
        "grid cases with a nonzero forecast": n_cases,
        "days of the cases": n_days,
        "grid cases with forecast at or below -10": n_deep,
        "grid cases with forecast between -10 and 0": n_shallow,
    }

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with a nonzero forecast, fewer than the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if check_passed is True:
            status = "confirmed"
            decided = "The slope is positive with t of 2 or more and the deep cases' mean excess return is below the shallow cases'."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t of 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t of -2 or less: deeper closes are followed by relatively higher returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "slope of drift-removed 10-bar return on forecast",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t, clustered by day", "value": tval},
            "threshold": "positive with t >= 2 confirms (with check); negative with t <= -2 rejects; else inconclusive",
        },
        "supporting_check": {
            "name": "mean excess return, forecast <= -10 minus forecast in (-10, 0)",
            "value": diff,
            "passed": check_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": (
            "The coin's drift is the mean of all its grid 10-bar returns over all windows (nonzero forecast or not), "
            "the slope is from an OLS with an intercept whose t uses day-clustered standard errors with the usual "
            "small-sample correction, the plan's fewer-than-100-cases rule is applied as a minimum count (not observable), "
            "and the choppy profile is read from the recorded regime 'unknown'."
        ),
    }
