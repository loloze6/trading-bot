import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.gc_spread.last_history_value"
    MIN_CASES = 100

    # ---------- 1. Situation check: SMA50 above SMA200 (raw spread > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & (f > 0) & raw.notna() & (raw > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of excess 10-day return on forecast, positive-forecast grid cases"
    threshold = "confirm if slope t >= 2 and forecast-weighted mean excess > 0; reject if slope t <= -2"
    reading = ("The situation is read from the recorded raw spread being above 0 with a positive forecast; "
               "the coin's usual 10-bar return is the mean of all its non-overlapping grid returns (positions 0, 10, 20, ...) "
               "pooled over its windows, the slope t is the ordinary OLS slope t from scipy linregress, and the plan's "
               "'fewer than 100 cases' rule is treated as a minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "positive-forecast grid cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where SMA50 is above SMA200 "
                           "with a long forecast, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_f, case_r, case_coin = [], [], []
    coin_grid_returns = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp", kind="mergesort").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    case_f.append(fc[t])
                    case_r.append(r)
                    case_coin.append(coin)
        coin_grid_returns[coin] = float(np.mean(allr)) if len(allr) else np.nan

    case_f = np.asarray(case_f, dtype=float)
    case_r = np.asarray(case_r, dtype=float)
    mu = np.array([coin_grid_returns.get(c, np.nan) for c in case_coin], dtype=float)
    excess = case_r - mu
    ok = np.isfinite(excess) & np.isfinite(case_f)
    case_f, excess = case_f[ok], excess[ok]
    n_cases = int(len(case_f))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(case_f) > 0:
        lr = stats.linregress(case_f, excess)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    wmean = float(np.sum(excess * case_f) / np.sum(case_f)) if n_cases > 0 and np.sum(case_f) > 0 else None
    sup_passed = None if wmean is None else bool(wmean > 0)

    counts = {"positive-forecast grid cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} positive-forecast grid cases, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the forecast-weighted mean excess return is 0 or less."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 10-day return > 0",
            "value": wmean,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
