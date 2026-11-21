import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    RAW = "debug_info.components.vs_ret_7d.last_history_value"

    def recompute_raw(close):
        # VolatilityScaledReturnComponent: 42-bar return / (std of 1-bar returns over 180 bars * sqrt(42))
        r1 = close.pct_change()
        ret42 = close / close.shift(42) - 1.0
        vol = r1.rolling(180, min_periods=180).std()
        return ret42 / (vol * np.sqrt(42))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                rec = recompute_raw(close)
                raw = raw.where(raw.notna(), rec)
            else:
                raw = recompute_raw(close)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(fc) == np.sign(raw)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (18-bar return minus coin's normal 18-bar drift)"
    main_thr = "confirm: mean > 0 with ordinary t >= 2.0 and quintile difference > 0; reject: mean < 0 with t <= -2.0"
    sup_name = "mean unusual move of top forecast quintile minus bottom quintile"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"independent grid cases": None},
            "decided_by": "The forecast's sign does not follow the sign of the 7-day volatility-scaled return "
                          "(long after a rise, short after a fall) on at least 90% of active bars.",
            "reading": "Situation taken as the sign of the raw volatility-scaled 7-day return, expected side equal to that sign.",
        }

    # ---------- 2. criterion ----------
    # grid cells per coin/window
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((coin, w, t, fc[t], c1 / c0 - 1.0))
    grid = pd.DataFrame(rows, columns=["coin", "window", "t", "forecast", "ret"])

    if len(grid) == 0:
        cases = grid
    else:
        drift = grid.groupby("coin")["ret"].mean()
        grid["unusual"] = grid["ret"] - grid["coin"].map(drift)
        cases = grid[grid["forecast"].notna() & (grid["forecast"] != 0)].copy()

    n_cases = int(len(cases))
    counts = {"independent grid cases": n_cases}

    mean_v = None
    t_v = None
    qdiff = None
    if n_cases >= 2:
        v = (cases["forecast"] / 10.0) * cases["unusual"]
        mean_v = float(v.mean())
        sd = float(v.std(ddof=1))
        t_v = float(mean_v / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    if n_cases >= 5:
        rk = cases["forecast"].rank(method="first")
        q = pd.qcut(rk, 5, labels=False)
        qdiff = float(cases.loc[q == 4, "unusual"].mean() - cases.loc[q == 0, "unusual"].mean())

    sup_passed = None if qdiff is None else bool(qdiff > 0)

    if n_cases < 500:
        status = "not observable"
        decided = f"Only {n_cases} independent grid cases, below the plan's minimum of 500."
    elif t_v is not None and mean_v > 0 and t_v >= 2.0 and sup_passed:
        status = "confirmed"
        decided = "The main mean is positive with t >= 2.0 and the quintile difference is above 0."
    elif t_v is not None and mean_v > 0 and t_v >= 2.0:
        status = "inconclusive"
        decided = "t >= 2.0 but the quintile difference is at or below 0, which the plan calls inconclusive."
    elif t_v is not None and mean_v < 0 and t_v <= -2.0:
        status = "rejected"
        decided = "The main mean is negative with t <= -2.0."
    else:
        status = "inconclusive"
        decided = "The t of the main mean lies between -2.0 and 2.0."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": None if t_v is None else {"name": "ordinary t of the mean", "value": t_v},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": qdiff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid cells are positions 0,18,36,... of each window with t+18 inside the window, the coin's drift is "
                   "the mean of those grid returns over all its windows, quintiles are pooled over all cases by forecast "
                   "rank, and the plan's 500-case minimum is applied as 'not observable'.",
    }
