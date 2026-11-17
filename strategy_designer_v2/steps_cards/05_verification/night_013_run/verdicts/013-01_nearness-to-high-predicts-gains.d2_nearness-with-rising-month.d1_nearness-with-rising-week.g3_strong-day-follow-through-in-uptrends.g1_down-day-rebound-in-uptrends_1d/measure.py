import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FALL_COL = "debug_info.components.fall.last_history_value"

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).iloc[:-1]
            rets.append(r.dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mean[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- situation check + collection of qualifying bars ----------
    n_active = 0
    n_agree = 0
    xs, ys = [], []

    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)

            # 30-day return from prices (inside window); where not computable, use the detector's decision
            ret30 = close / close.shift(30) - 1.0
            trending = pd.Series(np.where(ret30.notna(), ret30 > 0, regime == "trending"), index=d.index)

            # down day: raw vol-scaled 1-day return < 0 where recorded, else 1-day price return < 0
            if FALL_COL in d.columns:
                raw = pd.to_numeric(d[FALL_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            r1 = close / close.shift(1) - 1.0
            down = pd.Series(np.where(raw.notna(), raw < 0, r1 < 0), index=d.index)

            situation = trending & down
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # main-measure bars: regime trending and forecast > 0
            fwd = close.shift(-1) / close - 1.0
            sel = (regime == "trending") & (fc > 0) & fwd.notna()
            if sel.any() and np.isfinite(coin_mean[coin]):
                xs.extend(fc[sel].tolist())
                ys.extend((fwd[sel] - coin_mean[coin]).tolist())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    threshold_txt = "confirm: slope > 0 with t >= 2 and weighted mean excess > 0; reject: slope < 0 with t <= -2; else inconclusive; at least 100 qualifying bars"
    reading = ("The plan's situation is taken as the 30-day close-to-close return > 0 (from prices inside the window, the "
               "recorded regime where 30 prior bars are missing) and a negative raw vol-scaled 1-day return (the recorded "
               "'fall' value, else the 1-day price return), side long; the coin's mean daily return is the mean of all its "
               "next-1-bar returns over all windows; the slope t is the OLS slope over its standard error.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "OLS slope of excess next-1-bar return on forecast", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"qualifying bars": len(xs), "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down days (negative vol-scaled 1-day "
                           "return) in a positive 30-day-return regime with a long forecast: the standardised, negated, "
                           "clipped forecast does not follow the plan's situation."),
            "reading": reading,
        }

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n = len(x)
    counts = {"qualifying bars": n}

    slope = None
    t = None
    if n >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None
    wmean = float(np.sum(y * x) / np.sum(x)) if n > 0 and np.sum(x) > 0 else None
    sup_pass = (wmean > 0) if wmean is not None else None

    main = {"name": "OLS slope of excess next-1-bar return on forecast",
            "value": slope,
            "statistic": {"name": "t of OLS slope", "value": t} if t is not None else None,
            "threshold": threshold_txt}
    sup = {"name": "forecast-weighted mean excess next-1-bar return", "value": wmean, "passed": sup_pass}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} qualifying bars (trending, forecast > 0), below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the forecast-weighted mean excess return is <= 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
