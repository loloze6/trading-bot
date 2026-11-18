import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_EVENTS = 30
    FC_COL = "forecast"

    # ---------- 1. Situation check (from prices, per the Fidelity lines) ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = pd.to_numeric(df[FC_COL], errors="coerce").fillna(0.0)
            r1 = close / close.shift(1) - 1.0
            # usual move: std of the last 20 one-bar returns, with or without bar t
            sd_incl = r1.rolling(20, min_periods=20).std(ddof=1)
            sd_excl = r1.shift(1).rolling(20, min_periods=20).std(ddof=1)
            z_incl = r1 / sd_incl
            z_excl = r1 / sd_excl
            # volume at least twice its prior 20-bar mean (Fidelity wording)
            vmean = vol.shift(1).rolling(20, min_periods=20).mean()
            vratio = vol / vmean
            computable = sd_incl.notna() & sd_excl.notna() & vmean.notna() & (vmean > 0)
            fall_ok = (z_incl <= -2.0) | (z_excl <= -2.0)
            vol_ok = vratio >= 2.0
            sit = fall_ok & vol_ok
            regime_proxy = df["regime"].astype(str) == "mean_reversion"
            for i in range(len(df)):
                f = fc.iloc[i]
                if f == 0:
                    continue
                n_active += 1
                if bool(computable.iloc[i]):
                    in_sit = bool(sit.iloc[i])
                else:
                    in_sit = bool(regime_proxy.iloc[i])
                if in_sit and f > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = ("Situation recomputed from prices as a 1-bar return of -2 or less in units of the std of the last 20 "
               "one-bar returns (with or without bar t accepted) and volume at least twice the mean of the prior 20 "
               "bars as the Fidelity states, using the recorded regime only on bars with too little in-window history, "
               "expected side long; flush bars are regime == mean_reversion with t+3 inside the window, an event at "
               "1 to 3 bars after a kept event is dropped, the coin's mean 3-bar return is taken on the non-overlapping "
               "0,3,6,... grid of all its windows pooled, all flush events (including forecast 0) enter the OLS of "
               "excess return on forecast, and the 30-event minimum is on the pooled events of all coins.")

    main_name = "OLS slope of excess 3-bar return on forecast, flush bars"
    threshold = "slope t >= 2 with forecast-weighted mean excess > 0 confirms; slope t <= -2 rejects; at least 30 independent events"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent events": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are sharp falls (<= -2 usual moves) on volume at least "
                           "twice its prior 20-bar mean with a long forecast, so the config does not trade the plan's "
                           "situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean 3-bar return over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        coin_mean = float(np.mean(grid_rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df[FC_COL], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            last_kept = None
            for p in range(len(df)):
                if reg[p] != "mean_reversion":
                    continue
                if p + H >= len(df):
                    continue
                if last_kept is not None and p - last_kept <= H:
                    continue
                if not (np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0 and np.isfinite(fc[p])):
                    continue
                last_kept = p
                xs.append(float(fc[p]))
                ys.append(c[p + H] / c[p] - 1.0 - coin_mean)

    n = len(xs)
    x = np.array(xs)
    y = np.array(ys)

    slope = None
    tstat = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    wmean = None
    if n > 0 and np.sum(x) != 0:
        wmean = float(np.sum(y * x) / np.sum(x))
    sup_passed = None if wmean is None else bool(wmean > 0)

    if n < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n} independent flush events, below the plan's minimum of 30."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t-statistic could not be computed (no variation in the forecast), so neither rule is met."
    elif tstat >= 2.0 and sup_passed:
        status = "confirmed"
        decided = "Slope t is 2 or more and the forecast-weighted mean excess return is above 0, with at least 30 events."
    elif tstat >= 2.0:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the forecast-weighted mean excess return is not positive."
    elif tstat <= -2.0:
        status = "rejected"
        decided = "Slope t is -2 or less, with at least 30 independent events."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
                         "threshold": threshold},
        "supporting_check": {"name": "forecast-weighted mean excess 3-bar return > 0",
                             "value": wmean, "passed": sup_passed},
        "counts": {"independent events": int(n)},
        "decided_by": decided,
        "reading": reading,
    }
