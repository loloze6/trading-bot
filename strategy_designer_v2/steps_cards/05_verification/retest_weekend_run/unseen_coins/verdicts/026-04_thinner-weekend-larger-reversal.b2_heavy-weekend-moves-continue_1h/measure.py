import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    FC = "forecast"

    def _ts(df):
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        return ts.reset_index(drop=True)

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = _ts(d)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            vol = pd.to_numeric(d["volume"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(d)
            vs = pd.Series(vol)
            # weekend mean volume: bars t-47..t ; weekdays mean: bars t-167..t-48
            recent = vs.rolling(48, min_periods=48).mean().to_numpy()
            prior = vs.shift(48).rolling(120, min_periods=120).mean().to_numpy()
            ret48 = np.full(n, np.nan)
            if n > H:
                ret48[H:] = close[H:] / close[:-H] - 1.0
            dow = ts.dt.dayofweek.to_numpy()
            hr = ts.dt.hour.to_numpy()
            for i in np.where(fc != 0)[0]:
                n_active += 1
                if dow[i] != 6 or hr[i] != 23:
                    continue
                if not (np.isfinite(recent[i]) and np.isfinite(prior[i]) and prior[i] > 0):
                    continue
                if not (recent[i] / prior[i] > 1.0):
                    continue
                r = ret48[i]
                if not np.isfinite(r) or r == 0:
                    continue
                if np.sign(r) == np.sign(fc[i]):
                    n_agree += 1

    threshold_txt = ("confirm: t of the mean >= +2 with top-minus-bottom half above 0; "
                     "reject: t <= -2; at least 100 cases")
    main_name = "mean 48-bar directional excess return over the coin's normal drift"
    sup_name = "top half minus bottom half (median |forecast|) mean directional excess return"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"cases": 0},
            "decided_by": "No bar has a nonzero forecast, so fewer than the 100 cases the plan needs.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the nonzero-forecast bars are Sunday 23:00 bars with weekend "
                           "volume above the prior weekdays' mean and a forecast sign equal to the 48-bar "
                           "weekend return's sign."),
            "reading": ("The situation bar is the bar starting Sunday 23:00 UTC (closing Monday 00:00), the volume "
                        "ratio is mean volume of bars t-47..t over bars t-167..t-48 by row position in the window."),
        }

    # ---------- 2. Criterion ----------
    # normal drift per coin: mean of non-overlapping 48-bar returns over all its windows
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx) == 0:
                continue
            r = c[idx + H] / c[idx] - 1.0
            rs.append(r[np.isfinite(r)])
        rs = np.concatenate(rs) if rs else np.array([])
        drift[coin] = float(np.mean(rs)) if len(rs) else np.nan

    vals = []
    absf = []
    for coin, wins in bars.items():
        dr = drift.get(coin, np.nan)
        if not np.isfinite(dr):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            reg = d["regime"].astype(str).to_numpy()
            n = len(d)
            for i in range(n):
                if reg[i] != "trending" or not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                vals.append((r - dr) * np.sign(fc[i]))
                absf.append(abs(fc[i]))

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(vals))

    mean = float(np.mean(vals)) if n_cases else None
    tval = None
    if n_cases >= 2:
        sd = np.std(vals, ddof=1)
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_top = n_bot = 0
    if n_cases >= 2:
        med = np.median(absf)
        top = vals[absf > med]
        bot = vals[absf <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            sup_val = float(np.mean(top) - np.mean(bot))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    reading = ("Cases are all trending bars with nonzero forecast and a full 48-bar forward return in the same "
               "window, the drift is each coin's mean non-overlapping 48-bar return over all its windows, and the "
               "median split puts |forecast| > median in the top half and <= median in the bottom half.")

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 100 across coins and windows."
    elif tval is not None and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main mean's t is +2 or more and the top half minus bottom half is above 0."
    elif tval is not None and tval <= -2:
        status = "rejected"
        decided = "The main mean's t is -2 or less: heavy-volume weekend moves are reversed rather than continued."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "The main mean's t is +2 or more but the supporting check failed."
    else:
        status = "inconclusive"
        decided = "The main mean's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"cases": n_cases, "top_half": n_top, "bottom_half": n_bot},
        "decided_by": decided,
        "reading": reading,
    }
