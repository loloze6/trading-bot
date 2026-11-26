import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    ER_P = 60
    HI_P = 60
    ER_MAX = 0.3
    BAND = 2.0
    MIN_CASES = 30
    MIN_DAYS = 30
    RAW = "debug_info.components.break_up.last_history_value"

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
            unit = "ms" if v > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            high = d["high"].astype(float).values
            fc = d["forecast"].astype(float).fillna(0.0).values
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            raw = d[RAW].astype(float).values if RAW in d.columns else np.full(len(d), np.nan)
            n = len(d)
            for t in range(n):
                if fc[t] == 0:
                    continue
                n_active += 1
                # regime: efficiency ratio over 60 closes, recomputed from prices when the window holds them
                if t >= ER_P:
                    net = abs(close[t] - close[t - ER_P])
                    path = np.sum(np.abs(np.diff(close[t - ER_P:t + 1])))
                    chop = (net / path if path > 0 else 0.0) <= ER_MAX
                else:
                    chop = reg[t] == "chop"
                # break above the prior 60-bar high: raw component value, else from prices
                if np.isfinite(raw[t]):
                    brk = raw[t] > 0
                elif t >= HI_P:
                    brk = close[t] > np.max(high[t - HI_P:t])
                else:
                    brk = False
                if chop and brk and fc[t] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-day move of the bets (drift removed)"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("fewer than 90% of the active bars are long bars with the 60-day efficiency ratio "
                           "at or below 0.3 and the close above the prior 60-day high"
                           if n_active > 0 else "the record has no active bars"),
            "reading": "Efficiency ratio recomputed from 60 close changes where the window holds them, "
                       "else the recorded regime; break taken from the raw component value.",
        }

    # ---------- 2. criterion ----------
    case_ret = []   # (coin, day, return, entry forecast)
    for coin, wins in bars.items():
        # coin's normal drift: non-overlapping 5-day returns over all its windows
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).fillna(0.0).values
            ts = to_time(d["timestamp"])
            n = len(d)
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            # bets: a rise of the long forecast of >= BAND from its lowest level since the last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bet[t] = True
                    ref = f
                else:
                    ref = min(ref, f)
            # once per 5-bar cell of the window's grid: the first bet in the cell
            for c0 in range(0, n, H):
                idx = np.where(bet[c0:min(c0 + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = c0 + int(idx[0])
                if t + H >= n or not (close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                coin_cases.append((coin, ts.iloc[t].strftime("%Y-%m-%d"), r, float(fc[t])))
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan
        for (cn, day, r, f) in coin_cases:
            if np.isfinite(drift):
                case_ret.append((cn, day, r - drift, f))

    n_cases = len(case_ret)
    days = sorted(set(c[1] for c in case_ret))
    n_days = len(days)
    x = np.array([c[2] for c in case_ret], dtype=float)
    fe = np.array([c[3] for c in case_ret], dtype=float)

    mean = float(np.mean(x)) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(x - mean).groupby([c[1] for c in case_ret]).sum().values
        se = np.sqrt(np.sum(dev ** 2) * n_days / (n_days - 1)) / n_cases
        tval = float(mean / se) if se > 0 else None
    slope = None
    if n_cases >= 3 and np.unique(fe).size >= 2:
        slope = float(stats.linregress(fe, x).slope)

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    stat = {"name": "t of the mean, cases of one day summed", "value": tval} if tval is not None else None
    sup_pass = (slope > 0) if slope is not None else None
    reading = ("A case is the first bet (forecast rise of at least 2 from its lowest long level since the last bet, "
               "reset to 0 when flat) in each 5-bar cell from each window's first row, cases whose 5 bars run past "
               "the window's end are dropped, the drift is the coin's mean 5-day return on the same grid pooled "
               "over its windows, and the t uses day-summed deviations with a D/(D-1) correction.")

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"minimum not reached: {n_cases} cases (need 30) on {n_days} distinct days (need 30).")
    elif tval is None:
        status = "inconclusive"
        decided = "the t could not be computed, so the result meets neither the confirm nor the reject rule."
    elif mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual 5-day move is positive with t >= 2 and the slope on the entry forecast is above 0."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual 5-day move is negative with t <= -2."
    elif mean > 0 and tval >= 2:
        status = "inconclusive"
        decided = "A t >= 2 with a slope of 0 or below is inconclusive."
    else:
        status = "inconclusive"
        decided = "Any t between -2 and 2 is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean, "statistic": stat, "threshold": thr},
        "supporting_check": {"name": "slope of unusual 5-day move on entry forecast",
                             "value": slope, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
