import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.fall_vol_units.last_history_value"

    # ---------- 1. Situation check: active bars must be falls, on the long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ret1 = np.full(len(close), np.nan)
            if len(close) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(close), np.nan)
            # fall: raw vol-scaled 1-bar return < 0; if raw missing, use the price's 1-bar return
            sit_val = np.where(np.isnan(raw), ret1, raw)
            active = np.isfinite(fc) & (fc != 0)
            fall = np.isfinite(sit_val) & (sit_val < 0)
            n_active += int(active.sum())
            n_agree += int((active & fall & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of excess 3-bar forward return on forecast (forecast > 0, non-overlapping grid)"
    threshold = "confirm if slope t >= 2 and top-quintile mean excess > 0; reject if slope t <= -2"
    sup_name = "mean excess 3-bar return of top-quintile forecast cases"
    reading = ("Cases are pooled over all coins and windows on the 0,3,6,... grid of each window; the coin's mean "
               "3-bar return is the mean over all its grid bars in all windows; the top quintile is cases with "
               "forecast at or above the pooled 80th percentile; the plan's 'fewer cases -> inconclusive' minimums "
               "are reported as 'not observable' per the workflow; a fall is a negative raw component value "
               "(price 1-bar return where the raw value is missing).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are one-day falls with a long "
                           "forecast, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_fc, case_ret, case_coin = [], [], []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    case_fc.append(fc[i])
                    case_ret.append(r)
                    case_coin.append(coin)
        coin_grid_rets[coin] = float(np.mean(allr)) if len(allr) else np.nan

    case_fc = np.asarray(case_fc, dtype=float)
    case_ret = np.asarray(case_ret, dtype=float)
    mean_c = np.array([coin_grid_rets.get(c, np.nan) for c in case_coin], dtype=float)
    excess = case_ret - mean_c
    ok = np.isfinite(excess) & np.isfinite(case_fc)
    case_fc = case_fc[ok]
    excess = excess[ok]
    n_cases = int(len(case_fc))

    slope = None
    t_val = None
    if n_cases >= 3 and np.std(case_fc) > 0:
        lr = stats.linregress(case_fc, excess)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_val = float(lr.slope / lr.stderr)

    top_mean = None
    n_top = 0
    if n_cases > 0:
        q80 = float(np.quantile(case_fc, 0.8))
        top = case_fc >= q80
        n_top = int(top.sum())
        if n_top > 0:
            top_mean = float(np.mean(excess[top]))

    counts = {"cases with a positive forecast": n_cases, "cases in the top quintile": n_top}
    sup_pass = None if top_mean is None else bool(top_mean > 0)

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} cases with a positive forecast, below the plan's minimum of 300."
    elif n_top < 60:
        status = "not observable"
        decided = f"Only {n_top} cases in the top quintile, below the plan's minimum of 60."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-quintile mean excess return is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-quintile mean excess return is 0 or below."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger falls are followed by smaller excess returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": top_mean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
