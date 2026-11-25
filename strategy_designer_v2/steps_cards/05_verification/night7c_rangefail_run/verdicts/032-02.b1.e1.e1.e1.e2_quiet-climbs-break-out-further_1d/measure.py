import numpy as np
import pandas as pd


def measure(bars):
    PERIOD = 60
    H = 20
    WCOL = "debug_info.components.brk_runup.last_history_value"

    # ---------- per window preparation ----------
    act_total = 0
    act_agree = 0
    act_undetermined = 0
    cases = []        # dicts: coin, day, excess, weight
    grid_rets = {}    # coin -> list of non-overlapping 20-bar returns

    for coin, wins in bars.items():
        grid_rets.setdefault(coin, [])
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            n = len(d)
            prior_max = close.rolling(PERIOD, min_periods=PERIOD).max().shift(1)
            determinable = prior_max.notna() & close.notna()
            breakout = determinable & (close > prior_max)

            fwd = close.shift(-H) / close - 1.0  # inside the window only

            # coin's non-overlapping 20-bar returns (grid 0, 20, 40, ...)
            for p in range(0, n, H):
                r = fwd.iloc[p]
                if np.isfinite(r):
                    grid_rets[coin].append(float(r))

            # situation check
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            act_total += int(active.sum())
            act_undetermined += int((active & ~determinable).sum())
            act_agree += int((active & determinable & breakout & (fc > 0)).sum())

            # cases: first breakout in each 20-bar grid cell
            w = (pd.to_numeric(d[WCOL], errors="coerce") if WCOL in d.columns
                 else pd.Series(np.nan, index=d.index))
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bool(breakout.iloc[i])]
                if not idx:
                    continue
                i = idx[0]
                r = fwd.iloc[i]
                wt = w.iloc[i]
                if not (np.isfinite(r) and np.isfinite(wt)):
                    continue
                cases.append({"coin": coin, "day": str(ts.iloc[i].date()),
                              "ret": float(r), "weight": float(wt)})

    act_det = act_total - act_undetermined
    agreement = (act_agree / act_det) if act_det > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Breakouts are recomputed only on bars with 60 prior closes in the same window, so active bars "
               "without that history are left out of the agreement share; the 20-bar grid starts at each window's "
               "first row and a case needs its forward close inside the window; the slope's t uses a day-clustered "
               "(cases of one day summed) sandwich standard error; the plan's 'fewer than the minimum' is reported "
               "as not observable.")

    threshold = "t >= 2 with positive supporting check confirms; t <= -2 rejects; otherwise inconclusive"
    mm_name = "t of slope of 20-bar excess return on raw brk_runup weight"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": act_total, "active bars with determinable situation": act_det},
            "decided_by": ("Fewer than 90% of the active (nonzero forecast) bars are recomputed breakout bars "
                           "(close above the prior 60 closes) with a long forecast, as the Fidelity requires."),
            "reading": reading,
        }

    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in grid_rets.items()}
    cdf = pd.DataFrame(cases, columns=["coin", "day", "ret", "weight"])
    if len(cdf):
        cdf["excess"] = cdf["ret"] - cdf["coin"].map(coin_mean)
        cdf = cdf[np.isfinite(cdf["excess"])]
    n_cases = int(len(cdf))
    pos = cdf[cdf["weight"] > 0] if n_cases else cdf
    n_pos = int(len(pos))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    counts = {"breakout cases": n_cases, "cases with weight above 0": n_pos, "days": n_days}

    # slope and day-clustered t
    slope = None
    tval = None
    if n_cases >= 3:
        x = cdf["weight"].to_numpy(float)
        y = cdf["excess"].to_numpy(float)
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            b = float(np.sum(xc * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            score = pd.Series(xc * e).groupby(cdf["day"].to_numpy()).sum().to_numpy()
            G = len(score)
            if G > 1:
                var = float(np.sum(score ** 2)) / sxx ** 2 * G / (G - 1)
                slope = b
                tval = float(b / np.sqrt(var)) if var > 0 else None

    sup_val = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    result = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": tval,
                         "statistic": ({"name": "slope t (day-clustered)", "value": tval} if tval is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 20-bar return of cases with weight > 0",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "reading": reading,
    }
    result["main_measure"]["slope"] = slope

    if n_cases < 40:
        result["status"] = "not observable"
        result["decided_by"] = f"Only {n_cases} breakout cases, below the plan's minimum of 40."
        return result
    if n_pos < 20:
        result["status"] = "not observable"
        result["decided_by"] = f"Only {n_pos} cases with weight above 0, below the plan's minimum of 20."
        return result
    if tval is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The slope's t could not be computed (no spread in weights or a single day)."
        return result

    if tval >= 2 and sup_pass:
        result["status"] = "confirmed"
        result["decided_by"] = "The slope's t is 2 or more and the supporting check is positive."
    elif tval <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "The slope's t is -2 or less."
    elif tval >= 2:
        result["status"] = "inconclusive"
        result["decided_by"] = "The slope's t is 2 or more but the supporting check is not positive."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "The slope's t is between -2 and 2."
    return result
