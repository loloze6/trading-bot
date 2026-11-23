import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.sun_fall.last_history_value"
    MIN_CASES = 100

    n_active = 0
    n_agree = 0
    case_f = []
    case_r = []
    case_coin = []

    # coin normal 3-day drift: mean of non-overlapping 3-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if len(rets) else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            price_ret = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), price_ret)
            else:
                raw = price_ret
            is_sunday = (ts.dt.dayofweek == 6).values

            # situation check
            active = (fc != 0).values
            situation = is_sunday & (raw < 0).fillna(False).values
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0).values).sum())

            # cases
            c = close.values
            n = len(d)
            for i in range(n):
                if is_sunday[i] and fc.iloc[i] > 0 and i + H < n:
                    if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 and np.isfinite(drift[coin]):
                        r = c[i + H] / c[i] - 1.0 - drift[coin]
                        case_f.append(float(fc.iloc[i]))
                        case_r.append(float(r))
                        case_coin.append(coin)

    threshold = "confirm: slope > 0 with t >= 2 (and mean drift-adjusted return > 0); reject: slope < 0 with t <= -2; at least 100 cases"
    mname = "OLS slope of drift-adjusted 3-day return on Sunday forecast"
    reading = ("Sunday bars are those whose UTC timestamp is a Sunday; the situation is a Sunday with a negative raw 1-bar return "
               "(last_history_value, or the price return where missing) and a positive forecast; the coin's drift is the mean of "
               "non-overlapping 3-bar returns on each window's grid from its first row over all windows; cases need t+3 inside the "
               "window; the plan's 'fewer than 100 cases' is reported as not observable.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mname, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean drift-adjusted 3-day return of cases > 0", "value": None, "passed": None},
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 100 cases is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mname, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "cases": len(case_f)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are Sunday bars after a fall with a long forecast, as the Fidelity's situation and side require.",
            "reading": reading,
        }

    n_cases = len(case_f)
    x = np.array(case_f)
    y = np.array(case_r)
    mean_r = float(np.mean(y)) if n_cases else None

    slope = None
    tval = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    supp_pass = (mean_r > 0) if mean_r is not None else None
    counts = {"cases": int(n_cases), "coins": int(len(set(case_coin)))}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases across coins and windows, below the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), which meets neither the confirm nor the reject rule."
    elif slope > 0 and tval >= 2 and supp_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the cases' mean drift-adjusted 3-day return is above 0."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the cases' mean drift-adjusted return is 0 or below, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mname,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean drift-adjusted 3-day return of cases > 0",
            "value": mean_r,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
