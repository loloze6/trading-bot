import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if np.issubdtype(s.dtype, np.number):
        v = s.dropna()
        unit = "ms" if (len(v) and v.abs().median() > 1e11) else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 3
    MIN_CASES = 100
    col_ret = "debug_info.components.weekend_fall.last_history_value"
    col_ma = "debug_info.components.below_sma50.last_history_value"

    n_active = 0
    n_agree = 0
    cases_excess = []
    cases_fc = []

    for coin, wins in bars.items():
        prepared = []
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            d["_ts"] = _ts(d["timestamp"])
            d = d.sort_values("_ts").reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            # coin's normal 3-bar return: non-overlapping grid 0, 3, 6, ... per window
            for i in range(0, n - H, H):
                if close[i] > 0 and np.isfinite(close[i]) and np.isfinite(close[i + H]):
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            prepared.append(d)

        mean3 = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for d in prepared:
            close = d["close"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0)
            n = len(d)
            # raw component values, recorded where possible, else recomputed inside the window
            ret_rec = d[col_ret].astype(float) if col_ret in d.columns else pd.Series(np.nan, index=d.index)
            ma_rec = d[col_ma].astype(float) if col_ma in d.columns else pd.Series(np.nan, index=d.index)
            ret_re = close / close.shift(1) - 1.0
            sma = close.rolling(50, min_periods=50).mean()
            ma_re = (close - sma) / sma
            ret1 = ret_rec.where(ret_rec.notna(), ret_re)
            madist = ma_rec.where(ma_rec.notna(), ma_re)

            sunday = (d["_ts"].dt.dayofweek == 6).values
            situation = sunday & (ret1.values < 0) & (madist.values < 0)

            fv = fc.values
            active = fv != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fv > 0)).sum())

            cv = close.values
            for i in range(n):
                if sunday[i] and fv[i] > 0 and i + H < n:
                    if np.isfinite(cv[i]) and np.isfinite(cv[i + H]) and cv[i] > 0 and np.isfinite(mean3):
                        r = cv[i + H] / cv[i] - 1.0
                        cases_excess.append(r - mean3)
                        cases_fc.append(fv[i])

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("A Sunday bar is one whose UTC start timestamp is a Sunday (its next bar is a Monday); the coin's mean "
               "3-bar return is pooled over non-overlapping 3-bar stretches of all its windows; cases whose 3-bar "
               "return would leave the window are dropped; the minimum of 100 cases gives 'not observable' when unmet.")

    threshold = "t >= 2 over at least 100 cases (confirm, with slope > 0); t <= -2 over at least 100 cases (reject)"
    main_name = "t of mean of (excess 3-bar return x forecast/10) over Sunday cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": int(len(cases_excess)), "active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are Sunday bars with a negative 1-bar return "
                           "and a close below the 50-day SMA carrying a long forecast."),
            "reading": reading,
        }

    ex = np.array(cases_excess, dtype=float)
    fcs = np.array(cases_fc, dtype=float)
    n_cases = int(len(ex))
    prod = ex * fcs / 10.0

    mean_prod = float(np.mean(prod)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(prod, ddof=1))
        t = float(mean_prod / (sd / np.sqrt(n_cases))) if sd > 0 else None
    slope = None
    if n_cases >= 2 and np.std(fcs) > 0:
        slope = float(stats.linregress(fcs, ex).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 100 cases."
    elif t is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero dispersion), so neither confirm nor reject rule is met."
    elif t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Confirm: t >= 2 over at least 100 cases and the slope of excess return on forecast is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the slope of excess return on forecast is not above 0."
    elif t <= -2:
        status = "rejected"
        decided = "Reject: t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of excess 3-bar return on forecast > 0",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
