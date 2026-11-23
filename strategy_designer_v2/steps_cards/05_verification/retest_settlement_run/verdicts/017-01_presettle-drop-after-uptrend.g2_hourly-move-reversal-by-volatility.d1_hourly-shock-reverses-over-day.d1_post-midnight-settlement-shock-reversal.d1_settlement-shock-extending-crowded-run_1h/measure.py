import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    MIN_CASES = 300

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    # ---------- 2. data for the criterion ----------
    case_f = []
    case_r = []
    case_coin = []
    coin_grid_returns = {}

    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)

            # raw situation values from prices (positional, inside the window)
            r1 = close / close.shift(1) - 1.0                 # the 00:00 hour's own return
            p23 = close.shift(1) / close.shift(H) - 1.0       # the 23 hours before it
            hour0 = (ts.dt.hour == 0) & (ts.dt.minute == 0)
            aligned = hour0 & (
                ((r1 > 0) & (p23 > 0)) | ((r1 < 0) & (p23 < 0))
            )
            expected_sign = -np.sign(r1)                      # fade the hour's move

            active = fc != 0
            n_active += int(active.sum())
            agree = active & aligned & (np.sign(fc) == expected_sign)
            n_agree += int(agree.sum())

            # forward 24-bar return inside the window
            fwd = close.shift(-H) / close - 1.0

            # coin's mean 24-bar return: non-overlapping grid 0, H, 2H, ... of each window
            grid = fwd.iloc[::H].dropna()
            grid_rets.extend(grid.tolist())

            # case bars: non-zero forecast, at most one per coin-day (first one of the day)
            day = ts.dt.floor("D")
            act_idx = np.where(active.values)[0]
            seen = set()
            for i in act_idx:
                d = day.iloc[i]
                if d in seen:
                    continue
                seen.add(d)
                if np.isfinite(fwd.iloc[i]) and np.isfinite(fc.iloc[i]):
                    coin_cases.append((float(fc.iloc[i]), float(fwd.iloc[i])))
        coin_grid_returns[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan
        for f, r in coin_cases:
            case_f.append(f)
            case_r.append(r)
            case_coin.append(coin)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled OLS slope of excess 24-bar forward return on forecast"
    threshold = "slope > 0 with t >= 2 (confirm), slope < 0 with t <= -2 (reject), on at least 300 cases"
    support_name = "mean of sign(forecast) x excess 24-bar return > 0"
    reading = ("Situation bars are those stamped 00:00 UTC whose own return close[t]/close[t-1]-1 has the same sign "
               "as close[t-1]/close[t-24]-1, expected side opposite to that hour's return; a coin-day's case is its "
               "first non-zero-forecast bar (UTC date of the timestamp); the coin's mean 24-bar return is taken on the "
               "non-overlapping 24-bar grid of all its windows; the slope is ordinary least squares with an intercept "
               "and t = slope / its standard error.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of the non-zero forecast bars are aligned 00:00 UTC bars faded "
                           "against the hour's move (below 90%), so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    f = np.array(case_f, dtype=float)
    r = np.array(case_r, dtype=float)
    mu = np.array([coin_grid_returns.get(c, np.nan) for c in case_coin], dtype=float)
    ex = r - mu
    ok = np.isfinite(f) & np.isfinite(ex)
    f = f[ok]
    ex = ex[ok]
    n = int(len(f))

    slope = None
    tval = None
    if n >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, ex)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(np.mean(np.sign(f) * ex)) if n > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 300."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 on at least 300 cases and the supporting check passes."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 300 cases."
    elif slope > 0 and tval >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": support_name, "value": sup_val,
                             "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": reading,
    }
