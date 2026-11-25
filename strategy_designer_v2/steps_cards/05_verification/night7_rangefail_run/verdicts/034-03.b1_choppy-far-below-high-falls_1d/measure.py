import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.depth_below_high.last_history_value"
    STRAT_REGIME = "unknown"  # the config's regime that holds the strategy: the choppy profile (|60-bar trend| <= 10)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            # prior 20-day closing high from prices, inside the window, where enough history exists
            prior_high = pd.Series(close).shift(1).rolling(20, min_periods=20).max().to_numpy()
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                choppy = reg[i] == STRAT_REGIME
                if np.isfinite(raw[i]):
                    below = raw[i] < 0
                elif np.isfinite(prior_high[i]) and np.isfinite(close[i]):
                    below = close[i] < prior_high[i]
                else:
                    below = False
                if choppy and below and f < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of drift-adjusted 5-bar forward return on forecast (forecast < 0, 5-bar grid)"
    threshold = "confirm: slope > 0 with t >= 2 and deepest third mean < 0; reject: slope < 0 with t <= -2"
    support_name = "mean drift-adjusted 5-bar return of the deepest third by |forecast|"
    reading = ("Choppy profile read as the bars whose recorded regime is 'unknown' (the config's only regime with a strategy, "
               "i.e. |60-bar price evolution| <= 10), below-high as a negative raw depth value; the coin's mean 5-bar return "
               "is over all grid cells of all its windows; the t is the slope over a day-clustered standard error "
               "(per-day sums of x-deviation times residual); thirds split by sorted |forecast| with np.array_split, "
               "the deepest third being the last part.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars inside the choppy profile with the close "
                           "below its prior 20-day high, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        cand = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0 and not pd.isna(ts.iloc[i]):
                    cand.append((fc[i], r, ts.iloc[i].normalize()))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for f, r, d in cand:
            rows.append((coin, f, r - mu, d))

    n_cases = len(rows)
    days = [r[3] for r in rows]
    n_days = len(set(days))
    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}

    slope = None
    t = None
    deep_mean = None
    if n_cases >= 3:
        x = np.array([r[1] for r in rows], dtype=float)
        y = np.array([r[2] for r in rows], dtype=float)
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            slope = float(np.sum(xd * (y - y.mean())) / sxx)
            intercept = y.mean() - slope * x.mean()
            e = y - intercept - slope * x
            s = pd.Series(xd * e).groupby(pd.Index(days)).sum().to_numpy()
            var = float(np.sum(s ** 2)) / sxx ** 2
            t = float(slope / np.sqrt(var)) if var > 0 else None
        order = np.argsort(np.abs(x), kind="mergesort")
        parts = np.array_split(order, 3)
        if len(parts[-1]) > 0:
            deep_mean = float(np.mean(y[parts[-1]]))

    check_pass = None if deep_mean is None else bool(deep_mean < 0)
    supporting = {"name": support_name, "value": deep_mean, "passed": check_pass}
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "slope t (day-clustered)", "value": t} if t is not None else None),
            "threshold": threshold}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The plan's minimum of 100 grid cases on 50 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, which meets neither the confirm nor the reject rule."
    elif slope > 0 and t >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the deepest third's mean drift-adjusted return is below 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper slips are followed by relatively higher returns."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope confirms (t >= 2) but the deepest third's mean is not below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
