import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    MIN_CASES = 100
    LHV = "debug_info.components.wide_day.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: 30-day return > 0 (trending regime) AND today's range above its
    # 30-bar mean range (today included), i.e. raw compression 1 - range/mean < 0; side long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            rng = (df["high"].astype(float) - df["low"].astype(float))
            # 30-day return from prices where available, else the detector's decision
            ret30 = close / close.shift(30) - 1.0
            reg_trend = df["regime"].astype(str).str.lower().eq("trending") if "regime" in df else pd.Series(False, index=df.index)
            up = pd.Series(np.where(ret30.notna(), ret30 > 0, reg_trend), index=df.index).astype(bool)
            # range versus its 30-bar mean: raw component value where recorded, else from prices
            mean_rng = rng.rolling(30, min_periods=30).mean()
            comp_px = 1.0 - rng / mean_rng
            if LHV in df.columns:
                comp = pd.to_numeric(df[LHV], errors="coerce")
                comp = comp.where(comp.notna(), comp_px)
            else:
                comp = comp_px
            wide = (comp < 0).fillna(False)
            situation = up & wide
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean of forecast x excess 3-bar return on positive-forecast grid bars"
    threshold = "t >= 2 (with supporting check > 0) confirms; t <= -2 rejects; at least 100 cases"
    sup_name = "mean excess 3-bar return, upper minus lower half at median forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases with positive forecast": None},
            "decided_by": ("fewer than 90% of the bars with a nonzero forecast are long bars where the 30-day return "
                           "is positive and today's range exceeds its 30-bar mean range"
                           if n_active > 0 else "no active bars in the record"),
            "reading": "situation recomputed from the raw wide_day value (range above mean when it is below 0) and the 30-bar price return, falling back to the recorded regime where 30 bars of history are missing in a window.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((fc[i], r))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for f, r in coin_cases:
            rows.append((f, r - mu))

    n_cases = len(rows)
    counts = {"grid cases with positive forecast": int(n_cases)}

    if n_cases > 0:
        f = np.array([x[0] for x in rows], dtype=float)
        ex = np.array([x[1] for x in rows], dtype=float)
        prod = f * ex
        mval = float(prod.mean())
        if n_cases > 1 and prod.std(ddof=1) > 0:
            tval = float(mval / (prod.std(ddof=1) / np.sqrt(n_cases)))
        else:
            tval = None
        med = float(np.median(f))
        upper = ex[f > med]
        lower = ex[f <= med]
        if len(upper) > 0 and len(lower) > 0:
            sup = float(upper.mean() - lower.mean())
        else:
            sup = None
    else:
        mval, tval, sup = None, None, None
        upper = lower = np.array([])

    sup_passed = None if sup is None else bool(sup > 0)
    counts["upper half cases"] = int(len(upper))
    counts["lower half cases"] = int(len(lower))

    if n_cases < MIN_CASES or tval is None:
        status = "not observable"
        decided = f"only {n_cases} grid cases with a positive forecast, fewer than the plan's minimum of 100."
    elif tval >= 2 and sup_passed:
        status = "confirmed"
        decided = "the main measure's t is 2 or more and the supporting check is above 0, with at least 100 cases."
    elif tval <= -2:
        status = "rejected"
        decided = "the main measure's t is -2 or less, with at least 100 cases."
    elif tval >= 2:
        status = "inconclusive"
        decided = "the main measure's t is 2 or more but the supporting check is at or below 0."
    else:
        status = "inconclusive"
        decided = "the main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mval,
            "statistic": None if tval is None else {"name": "ordinary t of the mean", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 3-bar return is taken over all its windows' non-overlapping grid returns (grid from each "
                    "window's first row, last incomplete cell dropped), and the median split puts forecasts above the median "
                    "in the upper half and those at or below it in the lower half."),
    }
