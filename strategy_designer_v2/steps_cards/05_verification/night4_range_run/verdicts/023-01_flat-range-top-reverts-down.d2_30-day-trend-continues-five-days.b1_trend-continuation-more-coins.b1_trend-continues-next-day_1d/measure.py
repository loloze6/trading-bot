import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.ret30.last_history_value"
    PERIOD = 30
    THR = 0.5

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            # NetMoveToRangeRatio(30, high_low): |close[t]-close[t-30]| / (max high - min low over the last 30 bars)
            net = (close - close.shift(PERIOD)).abs()
            rng = high.rolling(PERIOD, min_periods=PERIOD).max() - low.rolling(PERIOD, min_periods=PERIOD).min()
            nmr = net / rng.replace(0, np.nan)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            # in-situation: from prices where computable, else the detector's recorded decision
            in_sit = pd.Series(np.where(nmr.notna(), nmr >= THR - 1e-12, regime == "trending"), index=d.index)
            # expected side: sign of the 30-bar return (raw component value, else from prices)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            price_ret = close / close.shift(PERIOD) - 1.0
            side_src = raw.where(raw.notna(), price_ret)
            side = np.sign(side_src)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & in_sit.astype(bool) & side.notna() & (np.sign(fc) == side)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of next-day excess return on forecast (trending, non-zero forecast bars, pooled)"
    thr_words = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; at least 300 bars"
    reading = ("Situation computed from prices as |close[t]-close[t-30]| over the 30-bar high-low range (detector's "
               "recorded regime used where a window lacks 30 bars of history), side from the sign of the 30-bar return; "
               "the plan's 'fewer than 300 bars' minimum is treated as a minimum count (not observable); the coin's mean "
               "daily return is the mean of all its in-window next-day returns; OLS with intercept, every bar used "
               "since the horizon is 1 bar.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"trending bars with a non-zero forecast": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars have a 30-bar net-move-to-range ratio >= 0.5 "
                           "with the forecast on the side of the 30-bar return (agreement %s)." % (
                               "n/a" if agreement is None else "%.3f" % agreement)),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        rets_all = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            r = close.shift(-1) / close - 1.0
            rets_all.append(r.dropna())
            frames.append((d, r))
        if not rets_all:
            continue
        allr = pd.concat(rets_all)
        if len(allr) == 0:
            continue
        mu = float(allr.mean())
        for d, r in frames:
            fc = pd.to_numeric(d[FC], errors="coerce")
            regime = d["regime"].astype(str)
            m = (regime == "trending") & fc.notna() & (fc != 0) & r.notna()
            xs.append(fc[m].values.astype(float))
            ys.append((r[m] - mu).values.astype(float))

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(len(x))
    counts = {"trending bars with a non-zero forecast": n}

    if n < 300:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 300 trending bars with a non-zero forecast (%d)." % n,
            "reading": reading,
        }

    slope = t = None
    if np.std(x) > 0 and n > 2:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    if slope is None or t is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm rule: the slope is positive with t = %.2f >= 2." % t
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule: the slope is negative with t = %.2f <= -2." % t
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: t = %.2f lies between -2 and 2." % t

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS t of slope", "value": t},
                         "threshold": thr_words},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
