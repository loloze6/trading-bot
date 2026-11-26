import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RATIO_LEVEL = 1.5
    RANGE_WIN = 20

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            rng = (df["high"].astype(float) - df["low"].astype(float))
            mean_rng = rng.rolling(RANGE_WIN, min_periods=RANGE_WIN).mean()
            ratio = rng / mean_rng.replace(0, np.nan)
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            computable = ratio.notna()
            n_active_uncomputable += int((active & ~computable).sum())
            act = active & computable
            n_active += int(act.sum())
            situ = (ratio >= RATIO_LEVEL - 1e-9) & (fc > 0)
            n_agree += int((act & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "forecast-weighted mean unusual 3-bar move (return minus coin's normal 3-bar drift), before costs"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 distinct case days"
    reading_check = ("the situation is recomputed from prices as today's high-low over the mean high-low of the last 20 bars "
                     "of the same window (today included), side long; active bars in a window's first 19 bars, where the "
                     "ratio cannot be computed, are left out of the agreement")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars not checkable": n_active_uncomputable},
            "decided_by": ("fewer than 90 % of the active bars are long bars on days whose range is at least 1.5 times "
                           "the 20-day mean bar range" if n_active > 0 else "no active bars could be checked"),
            "reading": reading_check,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 3-bar returns over all windows
        grid_rets = []
        prepared = {}
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            prepared[w] = df
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in prepared.items():
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            ref = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND - 1e-12:
                    ref = f
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    if t + H >= n:
                        continue
                    if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                        continue
                    taken_cells.add(cell)
                    r = c[t + H] / c[t] - 1.0
                    case_rows.append({
                        "coin": coin, "window": w, "day": ts.iloc[t].strftime("%Y-%m-%d"),
                        "f": float(f), "u": r - drift,
                    })
                else:
                    ref = min(ref, f)

    cases = pd.DataFrame(case_rows, columns=["coin", "window", "day", "f", "u"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    wmean = None
    tstat = None
    slope = None
    if n_cases > 0 and cases["f"].sum() > 0:
        f = cases["f"].values
        u = cases["u"].values
        sw = f.sum()
        wmean = float((f * u).sum() / sw)
        dev = pd.Series(f * (u - wmean)).groupby(cases["day"].values).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1.0)) * np.sum(dev ** 2) / sw ** 2
            se = np.sqrt(var)
            tstat = float(wmean / se) if se > 0 else None
        if n_cases >= 2 and np.var(f) > 0:
            slope = float(np.polyfit(f, u, 1)[0])

    slope_pass = None if slope is None else bool(slope > 0)
    counts = {"distinct case days": n_days, "cases": n_cases, "active bars checked": n_active}

    if n_days < 30:
        status = "not observable"
        decided = f"only {n_days} distinct case days, fewer than the 30 the plan requires"
    elif tstat is None or wmean is None:
        status = "inconclusive"
        decided = "the t of the weighted mean could not be computed, so neither the confirm nor the reject rule is met"
    elif wmean > 0 and tstat >= 2 and slope_pass:
        status = "confirmed"
        decided = "the weighted mean unusual move is above 0 with t >= 2 and the slope is above 0"
    elif wmean < 0 and tstat <= -2:
        status = "rejected"
        decided = "the weighted mean unusual move is below 0 with t <= -2"
    elif tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope of the unusual move on the forecast is at or below 0 (or undefined)"
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2"

    reading = (reading_check + "; a case is a bet (a rise of the long forecast of at least 2 points from its lowest level "
               "since the last bet, from 0 after a flat bar), only the first bet of each 3-bar grid cell of its window is kept "
               "and weighted by its forecast, cases without 3 further bars in the window are dropped, the normal drift is the "
               "coin's mean non-overlapping 3-bar return over all windows, and the day-pooled t uses per-day sums of "
               "weighted deviations with a D/(D-1) correction; with fewer than 30 case days the status is 'not observable'")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": wmean,
            "statistic": None if tstat is None else {"name": "t of the weighted mean, cases on the same day pooled", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of unusual move on forecast > 0", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
