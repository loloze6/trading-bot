import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    raw_col = "debug_info.components.vol_scaled_fall.last_history_value"

    # ---------- 1. Situation check: a down day (fall) -> long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0  # inside the window only
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # the situation: the day's 1-bar return is negative (raw value sign = return sign);
            # where the raw value is missing, fall back on the price return
            fall = raw.where(raw.notna(), ret1) < 0
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & fall & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of next-day excess return on forecast (forecast > 0)"
    thr = "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; |t| < 2 inconclusive"
    sup_name = "mean next-day excess return over top third of positive forecasts > 0"
    reading = ("Coin mean daily return is the mean of close[t+1]/close[t]-1 over every bar of all the coin's windows; "
               "the slope's t is the ordinary OLS t; the top third is the pooled positive-forecast bars with forecast "
               "at or above the pooled 2/3 quantile; the 300-bar minimum counts positive-forecast bars with a next-day "
               "return and, as a minimum count, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars on a fall, long": int(n_agree)},
            "decided_by": ("The plan's situation is a long on down days only, but fewer than 90% of the bars "
                           "with a non-zero forecast are long on a down day."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        frames = []
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            nxt = np.full(len(close), np.nan)
            if len(close) > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            all_rets.append(nxt[~np.isnan(nxt)])
            frames.append((fc, nxt))
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for fc, nxt in frames:
            m = (~np.isnan(fc)) & (~np.isnan(nxt)) & (fc > 0)
            xs.append(fc[m])
            ys.append(nxt[m] - mu)

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(len(x))
    counts = {"bars with forecast > 0": n}

    slope = None
    tval = None
    if n >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else (np.inf if res.slope > 0 else -np.inf)

    sup_val = None
    sup_pass = None
    if n > 0:
        q = np.quantile(x, 2.0 / 3.0)
        top = y[x >= q]
        if len(top) > 0:
            sup_val = float(np.mean(top))
            sup_pass = bool(sup_val > 0)
        counts["top-third bars"] = int(len(top))

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS t of slope", "value": tval} if tval is not None else None),
            "threshold": thr}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n < 300:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": f"Fewer than 300 bars with forecast > 0 across all coins and windows ({n}).",
                "reading": reading}

    if slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope could not be estimated (no variation in the forecast), so neither rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top-third mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the top-third mean excess return is not above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": decided, "reading": reading}
