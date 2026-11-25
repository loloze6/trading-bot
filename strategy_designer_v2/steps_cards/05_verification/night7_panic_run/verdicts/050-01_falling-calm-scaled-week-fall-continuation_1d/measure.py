import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_fall.last_history_value"
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).str.lower().values
            # 7-day return sign: raw component value where recorded, else from prices
            ret7 = np.full(len(df), np.nan)
            ret7[7:] = close[7:] / close[:-7] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            fell = np.where(np.isfinite(raw), raw < 0, np.where(np.isfinite(ret7), ret7 < 0, False))
            # falling calm profile: the detector did not veto to chop (regime 'unknown' carries the strategy)
            in_profile = regime == "unknown"
            situation = fell & in_profile
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The active bars are not, for at least 90 %, bars where the coin fell over 7 days "
                           "inside the falling-calm profile with a short forecast (agreement %.3f)." % agreement),
            "reading": "The falling-calm profile is read from the recorded regime (not 'chop'), the 7-day fall from the raw component's sign (prices where missing).",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean non-overlapping 3-bar return over all windows
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            close = df["close"].astype(float).values
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rs.append(r)
        drift[coin] = float(np.mean(rs)) if rs else np.nan

    ex, absf, days = [], [], []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(close) - H, H):
                if not np.isfinite(fc[i]) or fc[i] >= 0:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                ex.append(-(r - drift[coin]))
                absf.append(abs(fc[i]))
                days.append(ts.iloc[i].strftime("%Y-%m-%d"))

    ex = np.array(ex, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(ex))
    n_days = int(len(set(days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    main_val, main_t, slope, slope_t = None, None, None, None
    if n_cases >= 2:
        main_val = float(ex.mean())
        dev = pd.Series(ex - main_val).groupby(pd.Series(days)).sum().values
        G = len(dev)
        if G > 1:
            se = np.sqrt(G / (G - 1.0) * np.sum(dev ** 2)) / n_cases
            main_t = float(main_val / se) if se > 0 else None
        if n_cases >= 3 and np.std(absf) > 0:
            lr = stats.linregress(absf, ex)
            slope = float(lr.slope)
            slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    main = {
        "name": "mean short-direction 3-bar excess return over the coin's normal drift",
        "value": main_val,
        "statistic": {"name": "t, cases of one day summed together", "value": main_t} if main_t is not None else None,
        "threshold": "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject",
    }
    sup_pass = None if slope_t is None else bool(slope > 0 and slope_t >= 2)
    sup = {"name": "OLS slope of excess return on |forecast| (t)", "value": slope, "passed": sup_pass,
           "t": slope_t}
    sup = {"name": "OLS slope of short excess return on |forecast|, t = %s" % (
        "null" if slope_t is None else "%.3f" % slope_t), "value": slope, "passed": sup_pass}
    reading = ("Cases are grid bars 0,3,6,... of each window with forecast < 0 and a full 3-bar return inside the window; "
               "the drift is the coin's mean non-overlapping 3-bar return over all its windows; the main t is clustered by "
               "UTC day with a G/(G-1) correction; the slope t is the ordinary OLS t; the plan's 30 distinct days is "
               "applied as a minimum count.")

    sc = {"agreement": agreement, "passed": True}
    if n_days < MIN_DAYS or main_t is None:
        return {"status": "not observable", "situation_check": sc, "main_measure": main, "supporting_check": sup,
                "counts": counts,
                "decided_by": "The cases fall on %d distinct days, fewer than the plan's 30." % n_days,
                "reading": reading}

    if main_val > 0 and main_t >= 2 and slope_t is not None and slope > 0 and slope_t >= 2:
        status = "confirmed"
        dec = "The main measure is above 0 with t >= 2 and the slope on |forecast| is above 0 with t >= 2."
    elif main_val < 0 and main_t <= -2:
        status = "rejected"
        dec = "The main measure is below 0 with t <= -2 (a reversal)."
    elif slope_t is not None and slope < 0 and slope_t <= -2:
        status = "rejected"
        dec = "The slope on |forecast| is below 0 with t <= -2 (the carry shrinks with the fall's size)."
    else:
        status = "inconclusive"
        if main_val > 0 and main_t >= 2:
            dec = "The main measure is above 0 with t >= 2 but the slope t is not >= 2 (nor <= -2): inconclusive."
        else:
            dec = "The main t lies between -2 and 2 and no reject rule is met: inconclusive."

    return {"status": status, "situation_check": sc, "main_measure": main, "supporting_check": sup,
            "counts": counts, "decided_by": dec, "reading": reading}
