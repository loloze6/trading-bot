import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_CASES = 300
    RAW = "debug_info.components.dist_high.last_history_value"
    POST = "debug_info.components.dist_high.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            s = None
            if POST in df.columns:
                s = pd.to_numeric(df[POST], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                usual = raw.abs().shift(1).rolling(90, min_periods=22).mean()
                s_re = (raw * 10.0 / usual).clip(-20, 20)
                s = s_re if s is None else s.where(s.notna(), s_re)
            if s is None:
                s = pd.Series(np.nan, index=df.index)
            # nearer to the 90-bar high than usual (s > -10) -> long; farther (s < -10) -> short
            side = np.sign(s + 10.0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & side.notna() & (side != 0) & (np.sign(fc) == side)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of 20-bar excess return on forecast, grid cases pooled"
    thr = "confirm if slope t >= 2 with top-minus-bottom quintile > 0; reject if slope t <= -2"
    reading = ("Expected side rebuilt as sign(standardised distance + 10) from dist_high's post-pipeline value "
               "(rebuilt from raw values where missing); grid cases include every grid bar with a full 20-bar "
               "forward return inside its window, including zero forecasts; the coin's mean 20-bar return is the "
               "mean of its grid returns over all windows; quintiles are the bars at or above the 80th and at or "
               "below the 20th percentile of the pooled grid forecasts.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases": None},
            "decided_by": ("Fewer than 90% of the active bars have a forecast sign matching the plan's situation "
                           "(long when nearer than usual to the prior 90-day high, short when farther)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, w, f, c1 / c0 - 1.0))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    n_cases = int(len(g))
    counts = {"grid cases": n_cases}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Fewer than {MIN_CASES} grid cases across all coins and windows ({n_cases}).",
            "reading": reading,
        }

    g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
    x = g["forecast"].values.astype(float)
    y = g["excess"].values.astype(float)

    slope = None
    t_slope = None
    if np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else 0.0
    else:
        t_slope = 0.0

    q_lo = np.quantile(x, 0.2)
    q_hi = np.quantile(x, 0.8)
    top = y[x >= q_hi]
    bot = y[x <= q_lo]
    if len(top) > 0 and len(bot) > 0 and q_hi > q_lo:
        qdiff = float(np.mean(top) - np.mean(bot))
        sup_pass = bool(qdiff > 0)
    else:
        qdiff = None
        sup_pass = False
    counts["top quintile cases"] = int(len(top))
    counts["bottom quintile cases"] = int(len(bot))

    if t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope t is 2 or more and the top-minus-bottom quintile difference is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the quintile difference is not above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": {"name": "OLS slope t", "value": float(t_slope)},
                         "threshold": thr},
        "supporting_check": {"name": "top minus bottom quintile mean excess 20-bar return",
                             "value": qdiff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
