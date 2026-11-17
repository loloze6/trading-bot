import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    MIN_CASES = 200
    comp_col = "debug_info.components.wkd_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            d["_dow"] = ts.dt.dayofweek
            close = d["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0  # inside this window only
            if comp_col in d.columns:
                raw = pd.to_numeric(d[comp_col], errors="coerce")
                ret1 = ret1.where(ret1.notna(), raw)  # fallback on a window's first bar
            d["_ret1"] = ret1
            d["_fwd"] = close.shift(-H) / close - 1.0
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            d["_fc"] = fc
            prepared[coin][w] = d

            active = fc.notna() & (fc != 0)
            situation = (d["_dow"] == 6) & (d["_ret1"] < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of excess 2-bar return on forecast (Sunday falls)"
    thr_words = "slope t >= 2 with positive forecast-weighted mean excess 2-bar return confirms; slope t <= -2 rejects; at least 200 cases"
    sup_name = "forecast-weighted mean excess 2-bar return > 0"

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"Sunday-fall cases": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are Sunday bars after a Saturday-to-Sunday fall with a long forecast, as the plan's situation and side require.",
            "reading": "Sunday is the bar whose UTC start timestamp is a Sunday; the weekend fall is the Saturday-to-Sunday close-to-close return below 0 (the component's raw value on a window's first bar); the expected side is long.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in prepared.items():
        grid = []
        for w, d in wins.items():
            g = d["_fwd"].iloc[0::H].dropna()
            grid.append(g.values)
        grid = np.concatenate(grid) if grid else np.array([])
        coin_mean = float(np.mean(grid)) if grid.size else np.nan
        for w, d in wins.items():
            sel = (d["_dow"] == 6) & (d["regime"] == "mean_reversion") & (d["_fc"] > 0) & d["_fwd"].notna()
            if sel.any() and np.isfinite(coin_mean):
                xs.append(d.loc[sel, "_fc"].values.astype(float))
                ys.append(d.loc[sel, "_fwd"].values.astype(float) - coin_mean)
    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(x.size)

    slope, tstat, wmean = None, None, None
    if n >= 3 and np.ptp(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr > 0 else None
    if n > 0 and x.sum() > 0:
        wmean = float(np.sum(x * y) / np.sum(x))

    sup_pass = None if wmean is None else bool(wmean > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} Sunday-fall cases, fewer than the plan's minimum of 200."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess 2-bar return is positive, with at least 200 cases."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, with at least 200 cases."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the weighted mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": thr_words,
        },
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass},
        "counts": {"Sunday-fall cases": n},
        "decided_by": decided,
        "reading": "Sunday is the bar whose UTC start timestamp is a Sunday; the coin's mean 2-bar return is pooled over all its windows on each window's grid of rows 0, 2, 4, ...; the regression is ordinary least squares with an intercept on all pooled cases.",
    }
