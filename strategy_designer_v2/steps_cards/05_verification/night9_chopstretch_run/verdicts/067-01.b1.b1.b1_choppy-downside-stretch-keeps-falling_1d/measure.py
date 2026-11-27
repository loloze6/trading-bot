import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.stretch.last_history_value"
    STRAT_REGIME = "unknown"  # the only regime with a strategy: |60-bar price evolution| <= 10, the choppy profile

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = d["forecast"].astype(float)
            # raw stretch from the record; recomputed from prices where missing
            sma = close.rolling(20, min_periods=20).mean()
            rstd = close.pct_change().rolling(20, min_periods=20).std()
            recomputed = ((close - sma) / sma) / rstd
            if RAW in d.columns:
                raw = d[RAW].astype(float).where(d[RAW].notna(), recomputed)
            else:
                raw = recomputed
            regime = d["regime"].astype(str)
            active = fc.notna() & (fc != 0)
            situation = (regime == STRAT_REGIME) & (raw < 0)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 5-bar return on forecast, forecast<0 grid cases"
    thr = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    sup_name = "mean excess 5-bar return on cases with forecast <= -10 is below 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars in the choppy regime with the close below its 20-day SMA.",
            "reading": "The choppy profile is the strategy's regime 'unknown' (|60-bar price evolution| <= 10) and the stretch below the average is a negative raw stretch value, recomputed from prices where unrecorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                rows.append((coin, fc[i], r, ts.iloc[i].floor("D")))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    df = pd.DataFrame(rows, columns=["coin", "forecast", "ret", "day"])
    df = df[np.isfinite(df["forecast"])]
    df["mean5"] = df["coin"].map(coin_rets)
    df["excess"] = df["ret"] - df["mean5"]
    cases = df[(df["forecast"] < 0) & np.isfinite(df["excess"])].copy()
    deep = cases[cases["forecast"] <= -10]
    n_cases = int(len(cases))
    n_deep = int(len(deep))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    tval = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), cases["forecast"].values])
        y = cases["excess"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        G = 0
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
            G += 1
        N, K = n_cases, 2
        corr = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_val = float(deep["excess"].mean()) if n_deep > 0 else None
    sup_pass = (sup_val < 0) if sup_val is not None else None

    counts = {
        "grid cases with forecast < 0": n_cases,
        "cases with forecast <= -10": n_deep,
        "days of the cases": n_days,
    }

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 grid cases with forecast < 0 ({n_cases})."
    elif n_deep < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases with forecast <= -10 ({n_deep})."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm: the slope is positive with t >= 2 and deeper stretches (forecast <= -10) have a mean excess return below 0."
        else:
            status = "inconclusive"
            decided = "Inconclusive: positive slope with t >= 2 but the supporting check fails (mean excess on forecast <= -10 is not below 0)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2, deeper stretches are followed by relative rises."
    else:
        status = "inconclusive"
        decided = "Inconclusive: |t| < 2 for the slope."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "slope t, clustered by day", "value": tval} if tval is not None else None,
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "The choppy profile is the strategy's regime 'unknown'; the regression is OLS with an intercept and a cluster-robust (by UTC day, CR1 small-sample corrected) slope variance; the coin's mean 5-bar return is over all its non-overlapping grid returns in all windows; and the plan's minimum counts give 'not observable' as the workflow requires.",
    }
