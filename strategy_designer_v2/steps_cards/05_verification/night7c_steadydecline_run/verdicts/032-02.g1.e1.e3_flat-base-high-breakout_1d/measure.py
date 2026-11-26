import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PERIOD = 28
    MIN_CASES = 100
    FC_COL = "forecast"

    # ---------- 1. Situation check: the close equals its 28-day closing high, side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC_COL], errors="coerce")
            # 28-day closing high including the current bar (exclude_current = 0);
            # only bars with a full 28-bar history inside the window can be checked
            roll_max = close.rolling(PERIOD, min_periods=PERIOD).max()
            checkable = roll_max.notna() & close.notna() & fc.notna()
            at_high = close >= roll_max * (1 - 1e-12)
            active = checkable & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & at_high & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    reading = ("The situation is recomputed as close >= max of the last 28 closes including the bar, "
               "checked only on bars with 28 bars of history inside their window, side long; "
               "cases are 'trending' bars at grid positions 0,5,10,... of each window with a 5-bar return "
               "inside the window, the coin's mean 5-day return is the mean over all its windows' grid samples, "
               "the slope t is the OLS slope over its standard error, and the plan's minimum of 100 cases "
               "gives 'not observable' when unmet.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars at the 28-day "
                           "closing high, which is the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_ret, case_fc, case_coin = [], [], []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC_COL], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]):
                    case_ret.append(r)
                    case_fc.append(fc[i])
                    case_coin.append(coin)
        coin_grid_rets[coin] = np.mean(allr) if len(allr) else np.nan

    excess, fcs = [], []
    for r, f, c in zip(case_ret, case_fc, case_coin):
        m = coin_grid_rets.get(c, np.nan)
        if np.isfinite(m):
            excess.append(r - m)
            fcs.append(f)
    excess = np.asarray(excess, float)
    fcs = np.asarray(fcs, float)
    n_cases = int(len(excess))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(fcs) > 0:
        lr = stats.linregress(fcs, excess)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    wmean = None
    if n_cases > 0 and np.sum(fcs) != 0:
        wmean = float(np.sum(excess * fcs) / np.sum(fcs))
    check_passed = (wmean is not None) and (wmean > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, below the plan's minimum of 100 cases."
    elif t_slope is not None and t_slope >= 2 and check_passed:
        status = "confirmed"
        decided_by = "The slope t is 2 or more and the forecast-weighted mean excess 5-day return is above 0."
    elif t_slope is not None and t_slope <= -2:
        status = "rejected"
        decided_by = "The slope t is -2 or less: larger positions are followed by smaller excess rises."
    else:
        status = "inconclusive"
        if t_slope is not None and t_slope >= 2:
            decided_by = "The slope t is 2 or more but the forecast-weighted mean excess return is at or below 0."
        else:
            decided_by = "The slope t is between -2 and 2 (or undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "slope of excess 5-day return on forecast",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "confirm if slope t >= 2 (with supporting check); reject if slope t <= -2",
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 5-day return > 0",
            "value": wmean,
            "passed": bool(check_passed) if wmean is not None else None,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }
