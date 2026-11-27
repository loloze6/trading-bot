import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    BAND = 2.0
    H = 1
    DEPTH_COL = "debug_info.components.depth.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            pe1 = close / close.shift(1) - 1.0
            pe5_price = (close / close.shift(5) - 1.0) * 100.0
            if DEPTH_COL in df.columns:
                pe5 = df[DEPTH_COL].astype(float).where(df[DEPTH_COL].notna(), pe5_price)
            else:
                pe5 = pe5_price
            active = fc != 0
            known = pe1.notna() & pe5.notna()
            situ = (pe1 > 0) & (pe5 < 0)
            sel = active & known
            n_active += int(sel.sum())
            n_agree += int((sel & situ & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None) and (agreement >= 0.9)

    main_name = "mean drift-adjusted short-side next-day return over short bets"
    thr = "confirm: mean > 0 with day-pooled t >= 2 and slope > 0; reject: mean < 0 with t <= -2; >= 100 cases on >= 50 days"
    reading_base = ("Situation checked as 1-day return > 0 and 5-day return < 0 (depth raw value, or prices where not recorded) "
                    "with a short forecast, bars whose returns cannot be computed inside the window left out, the falling "
                    "profile not rechecked as its 60-day return is not computable on early recorded bars; cases are short "
                    "bets (rise of -forecast by >= 2 from its lowest level on the short side since the last bet, from 0 after "
                    "flat or side change) on every bar (horizon 1), drift is the coin's mean 1-bar return over all its windows, "
                    "and t is the mean over a standard error with deviations summed per UTC day.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of active bars are up days (1-day return > 0) with a negative 5-day return "
                           "carrying a short forecast, as the plan's situation and side require."),
            "reading": reading_base,
        }

    # ---------- 2. Drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = df.sort_values("timestamp")["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            rets.append(r[np.isfinite(r)])
        drift[coin] = float(np.mean(np.concatenate(rets))) if rets and sum(len(x) for x in rets) > 0 else np.nan

    # ---------- 3. Cases ----------
    xs, absf, days = [], [], []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ref = 0.0
            side = 0
            for i in range(len(df)):
                f = fc[i]
                s = 0 if f == 0 else (1 if f > 0 else -1)
                if s != side:
                    ref = 0.0
                    side = s
                if s == 0:
                    continue
                level = abs(f)
                bet = (level - ref) >= BAND
                if bet:
                    ref = level
                else:
                    ref = min(ref, level)
                if bet and s < 0 and (i % H == 0) and i + H < len(df):
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        xs.append(-(r - drift[coin]))
                        absf.append(level)
                        days.append(ts.iloc[i].floor("D"))

    n = len(xs)
    n_days = len(set(days))
    counts = {"cases": int(n), "distinct days": int(n_days)}
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed) if agreement is not None else None}

    if n < 100 or n_days < 50:
        mean_v = float(np.mean(xs)) if n > 0 else None
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": {"name": main_name, "value": mean_v, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"The plan's minimum of 100 cases on at least 50 distinct days is not reached ({n} cases on {n_days} days).",
            "reading": reading_base,
        }

    x = np.asarray(xs, float)
    m = float(x.mean())
    dev = pd.Series(x - m).groupby(pd.Series(days)).sum().values
    se = float(np.sqrt(np.sum(dev ** 2)) / n)
    t = float(m / se) if se > 0 else 0.0

    a = np.asarray(absf, float)
    if np.ptp(a) > 0:
        slope = float(stats.linregress(a, x).slope)
    else:
        slope = None
    slope_ok = (slope is not None) and (slope > 0)

    if m > 0 and t >= 2 and slope_ok:
        status = "confirmed"
        decided = "The mean drift-adjusted short-side next-day return is positive with t >= 2 and the slope on |forecast| is above 0."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The mean drift-adjusted short-side next-day return is negative with t <= -2: the coin rises more than its drift after these days."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on |forecast| is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "t of the mean, cases of one day pooled", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "OLS slope of drift-adjusted short-side next-day return on |forecast|",
                             "value": slope, "passed": bool(slope_ok)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
