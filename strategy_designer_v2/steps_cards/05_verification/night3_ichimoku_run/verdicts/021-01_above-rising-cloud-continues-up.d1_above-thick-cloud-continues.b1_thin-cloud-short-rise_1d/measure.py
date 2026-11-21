import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    TEN, KIJ, SEN, DISP, LOOK = 9, 26, 52, 26, 26

    def ichimoku_situation(df):
        hi = df["high"].astype(float)
        lo = df["low"].astype(float)
        cl = df["close"].astype(float)
        tenkan = (hi.rolling(TEN).max() + lo.rolling(TEN).min()) / 2.0
        kijun = (hi.rolling(KIJ).max() + lo.rolling(KIJ).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(DISP)
        span_b = ((hi.rolling(SEN).max() + lo.rolling(SEN).min()) / 2.0).shift(DISP)
        top = np.maximum(span_a, span_b)
        mid = (span_a + span_b) / 2.0
        slope = mid / mid.shift(LOOK) - 1.0
        pos = cl - top
        computable = pos.notna() & slope.notna()
        situ = (pos > 0) & (slope > 0)
        return situ, computable

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_recomputed = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            situ, comp = ichimoku_situation(df)
            regime_trend = df["regime"].astype(str) == "trending" if "regime" in df.columns else pd.Series(False, index=df.index)
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                n_active += 1
                if comp.iloc[i]:
                    n_recomputed += 1
                    in_situ = bool(situ.iloc[i])
                else:
                    in_situ = bool(regime_trend.iloc[i])
                if in_situ and fc.iloc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation recomputed from each window's recorded prices (close above max(spanA, spanB), "
               "26-bar percent change of the cloud mid > 0); on active bars too early in a window for the "
               "Ichimoku lines to be computed, the recorded regime ('trending') stands in for the detector; "
               "the plan's 'fewer than 50 grid cases' minimum is reported as 'not observable'; the coin's normal "
               "5-day drift is the mean of its non-overlapping 5-bar grid returns over all windows; the slope's t "
               "is the ordinary OLS t (slope / its standard error).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars recomputed": n_recomputed},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (close above a rising Ichimoku cloud)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, ret, forecast)
    grid_rets = {}
    for coin, wins in bars.items():
        grid_rets.setdefault(coin, [])
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            cl = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H]) and cl[i] > 0):
                    continue
                r = cl[i + H] / cl[i] - 1.0
                grid_rets[coin].append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    cases.append((coin, r, float(fc[i])))

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in grid_rets.items()}
    xs, ys = [], []
    for coin, r, f in cases:
        d = drift.get(coin, np.nan)
        if np.isfinite(d):
            xs.append(f)
            ys.append(r - d)
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    n_cases = int(len(xs))

    slope = None
    tval = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {"grid cases with a forecast above 0": n_cases}
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 50 grid cases"
    main = {
        "name": "t of the OLS slope of excess 5-day return on forecast",
        "value": tval,
        "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
        "threshold": threshold,
    }

    if n_cases < 50:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with a forecast above 0, fewer than the plan's minimum of 50."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2: excess 5-day returns grow with cloud thinness."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: thinner clouds are followed by smaller excess returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
