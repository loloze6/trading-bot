import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    COMP = "debug_info.components.rise5.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            regime = df["regime"].astype(str)
            # 60-day return from the window's prices where 60 bars of history exist,
            # else the detector's own decision (regime "trending" == r60 > 0)
            r60 = close / close.shift(60) - 1.0
            up60 = np.where(r60.notna(), r60 > 0, regime == "trending")
            if COMP in df.columns:
                rise5 = pd.to_numeric(df[COMP], errors="coerce")
            else:
                rise5 = pd.Series(np.nan, index=df.index)
            rise5 = rise5.where(rise5.notna(), close / close.shift(5) - 1.0)
            situ = up60 & (rise5 > 0).values
            active = (fc.fillna(0) != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc.fillna(0) > 0).values).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("The 60-day return is recomputed from the window's closes where 60 prior bars exist and "
               "taken as regime 'trending' otherwise, the 5-day rise is the recorded rise5 raw value; "
               "the normal 3-bar drift is each coin's mean 3-bar return over the non-overlapping grid of all "
               "its windows and all regimes, the slope t is the OLS slope t pooled over all coins and windows, "
               "and the plan's 100-bar minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive "
                           "60-day return and a positive 5-day rise, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                rows.append({
                    "coin": coin,
                    "ret": close[i + H] / close[i] - 1.0,
                    "regime": str(df["regime"].iloc[i]),
                    "forecast": pd.to_numeric(df["forecast"].iloc[i], errors="coerce"),
                })
    g = pd.DataFrame(rows, columns=["coin", "ret", "regime", "forecast"])
    g = g[np.isfinite(g["ret"].astype(float))]
    drift = g.groupby("coin")["ret"].mean()
    g["excess"] = g["ret"] - g["coin"].map(drift)

    t_bars = g[(g["regime"] == "trending")].dropna(subset=["excess", "forecast"])
    n_trend = int(len(t_bars))
    n_pos = int((t_bars["forecast"] > 0).sum())

    slope = None
    t_slope = None
    x = t_bars["forecast"].astype(float).values
    y = t_bars["excess"].astype(float).values
    if n_trend >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    wsum = float(np.sum(x))
    wmean = float(np.sum(x * y) / wsum) if wsum > 0 else None
    sup_pass = (wmean > 0) if wmean is not None else None

    counts = {
        "grid bars in trending with forecast above 0": n_pos,
        "grid bars in trending": n_trend,
    }
    main = {
        "name": "t of slope of excess 3-bar return on forecast, trending grid bars",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2",
    }
    support = {"name": "forecast-weighted mean excess 3-bar return", "value": wmean, "passed": sup_pass}

    if n_pos < 100:
        status = "not observable"
        decided = "Fewer than 100 grid bars in trending with forecast above 0, the plan's minimum."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the forecast-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
