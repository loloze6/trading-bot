import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    HIGH_PERIOD = 28
    RAW = "debug_info.components.compress.last_history_value"

    def _ratio_from_prices(close):
        r = close.pct_change()
        s20 = r.rolling(20, min_periods=20).std()
        s60 = r.rolling(60, min_periods=60).std()
        return s20 / s60 - 1.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # 28-bar closing high, current bar included, inside the window;
            # on the first bars of a window, the high of the bars available
            hi = close.rolling(HIGH_PERIOD, min_periods=1).max()
            at_high = (close / hi - 1.0) >= -1e-8
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), _ratio_from_prices(close))
            # expected side: long when the 20-day vol is below the 60-day one
            # (the quieter, the larger the long), short when it has expanded
            exp_sign = -np.sign(raw)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & at_high & raw.notna() & (np.sign(fc) == exp_sign)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of the slope of 5-bar excess return on the forecast, trending grid cases"
    threshold = "confirm: t >= 2 with top-third minus bottom-third > 0; reject: t <= -2; under 100 grid cases: not observable"
    sup_name = "mean excess 5-bar return, top third of forecasts minus bottom third"
    reading = ("The situation is recomputed from closes as close equal to the 28-bar closing high inside each window "
               "(on a window's first 27 bars, the high of the bars available), its side per bar is long when the "
               "20-to-60-day volatility ratio (recorded raw value, else recomputed from closes) is below 1 and short "
               "when above, since the Fidelity keeps the graded comparison; the cases are regime 'trending' bars at "
               "positions 0, 5, 10, ... of each window with a 5-bar forward close in the same window, the drift is "
               "the coin's mean 5-bar return on that grid over all windows, the regression is OLS with an intercept, "
               "and the thirds are the floor(n/3) largest and smallest forecasts.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where the close equals the "
                           "28-bar closing high with the forecast long when the 20-day volatility is below the "
                           "60-day one and short when above, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                ret = c1 / c0 - 1.0
                grid_all.append(ret)
                if reg[p] == "trending" and np.isfinite(fc[p]):
                    cases.append((ret, float(fc[p])))
        if len(grid_all) == 0:
            continue
        drift = float(np.mean(grid_all))
        for ret, f in cases:
            rows.append((ret - drift, f))

    n_cases = len(rows)
    counts = {"grid cases": int(n_cases)}
    sit = {"agreement": float(agreement), "passed": True}

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} grid cases across all coins and windows, fewer than the plan's minimum of 100.",
            "reading": reading,
        }

    arr = np.array(rows, dtype=float)
    y = arr[:, 0]
    x = arr[:, 1]

    t_slope = None
    slope = None
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)
        else:
            t_slope = 0.0
    else:
        slope = None
        t_slope = 0.0

    k = n_cases // 3
    order = np.argsort(x, kind="mergesort")
    bottom = y[order[:k]]
    top = y[order[-k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else None
    sup_pass = diff is not None and diff > 0
    counts["top third cases"] = int(k)
    counts["bottom third cases"] = int(k)

    if t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-third minus bottom-third difference is above 0: confirm."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: reject."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-third minus bottom-third difference is not above 0: inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name,
                         "value": t_slope,
                         "statistic": {"name": "OLS slope t", "value": t_slope},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": diff, "passed": bool(sup_pass)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
