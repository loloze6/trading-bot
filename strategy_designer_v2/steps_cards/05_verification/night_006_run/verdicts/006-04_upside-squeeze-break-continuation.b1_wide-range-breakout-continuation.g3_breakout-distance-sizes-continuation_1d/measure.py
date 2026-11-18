import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.clear_high.last_history_value"

    # ---------- 1. Situation check: close above the prior 20-day high, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # price-based fallback: close vs highest high of the prior 20 bars inside the window
            prior_high = pd.to_numeric(d["high"], errors="coerce").shift(1).rolling(20, min_periods=20).max()
            close = pd.to_numeric(d["close"], errors="coerce")
            price_sit = close > prior_high
            price_known = prior_high.notna() & close.notna()
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                sit = pd.Series(np.where(raw.notna(), raw > 0, np.where(price_known, price_sit, False)),
                                index=d.index).astype(bool)
            else:
                sit = (price_sit & price_known).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    threshold_txt = ("confirm if slope t >= +2 on >= 30 cases and mean excess > 0; "
                     "reject if slope t <= -2 on >= 30 cases; else inconclusive")
    main_name = "t of OLS slope of excess 10-bar forward return on forecast (forecast > 0 grid samples)"
    reading = ("The coin's mean 10-bar return is the mean of all its non-overlapping 10-bar grid returns over all "
               "windows (not only forecast > 0 samples), the slope t is the ordinary OLS t with intercept, and the "
               "situation is read from the raw component value > 0 (price-based prior 20-bar high where it is missing).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the close is above "
                           "the prior 20-day high with a positive (long) forecast."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        samples = []  # (forecast, fwd return)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                samples.append((fc[t], c1 / c0 - 1.0))
        if not samples:
            continue
        rets = np.array([s[1] for s in samples], dtype=float)
        coin_mean = float(np.mean(rets))
        for f, r in samples:
            if np.isfinite(f) and f > 0:
                xs.append(float(f))
                ys.append(float(r - coin_mean))

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_stat = None
    if n_cases >= 3 and np.var(x) > 0:
        xm, ym = x.mean(), y.mean()
        sxx = float(np.sum((x - xm) ** 2))
        b = float(np.sum((x - xm) * (y - ym)) / sxx)
        a = ym - b * xm
        resid = y - (a + b * x)
        s2 = float(np.sum(resid ** 2) / (n_cases - 2))
        se = np.sqrt(s2 / sxx) if s2 > 0 else 0.0
        slope = b
        if se > 0:
            t_stat = float(b / se)
        else:
            t_stat = float(np.sign(b) * np.inf) if b != 0 else 0.0

    mean_excess = float(y.mean()) if n_cases > 0 else None
    support_pass = bool(mean_excess > 0) if mean_excess is not None else None

    counts = {"forecast > 0 grid samples": n_cases}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} forecast > 0 grid samples, fewer than the plan's minimum of 30 cases."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_stat >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope's t is +2 or more on at least 30 cases and the mean excess 10-bar return is above 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less on at least 30 cases."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The slope's t is +2 or more but the mean excess 10-bar return is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    def _num(v):
        if v is None:
            return None
        v = float(v)
        return v if np.isfinite(v) else (1e308 if v > 0 else -1e308)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": _num(t_stat),
            "statistic": ({"name": "OLS slope t", "value": _num(t_stat)} if t_stat is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return over forecast > 0 samples above 0",
            "value": mean_excess,
            "passed": support_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
