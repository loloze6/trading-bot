import numpy as np
import pandas as pd

HC = "debug_info.components.high_close.last_history_value"
H = 5
BAND = 2.0


def _to_days(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        unit = "ms" if s.abs().max() > 1e11 else "s"
        s = pd.to_datetime(s, unit=unit, utc=True)
    else:
        s = pd.to_datetime(s, utc=True)
    return s.dt.strftime("%Y-%m-%d").values


def _close_location(df):
    hi = df["high"].astype(float).values
    lo = df["low"].astype(float).values
    cl = df["close"].astype(float).values
    rng = hi - lo
    with np.errstate(divide="ignore", invalid="ignore"):
        loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
    if HC in df.columns:
        rec = pd.to_numeric(df[HC], errors="coerce").values
        loc = np.where(np.isfinite(rec), rec, loc)
    return loc


def _short_bets(fc):
    # bet = rise of the short forecast (in size) of at least BAND from its lowest level since last bet
    n = len(fc)
    bets = np.zeros(n, dtype=bool)
    ref = 0.0
    for i in range(n):
        f = fc[i]
        if not np.isfinite(f) or f >= 0:
            ref = 0.0
            continue
        s = -f
        if s - ref >= BAND - 1e-12:
            bets[i] = True
            ref = s
        else:
            ref = min(ref, s)
    return bets


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            loc = _close_location(df)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            agree = active & (fc < 0) & np.isfinite(loc) & (loc >= 0.8 - 1e-9)
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed_sit = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean short-side unusual 5-bar move of the bets"
    thr = "confirm: mean > 0 with day-pooled t >= 2 and check passed; reject: mean < 0 with t <= -2"
    reading = ("A case is the first short bet (rise of the short forecast of >= 2 points from its lowest level since the last bet) "
               "in each 5-bar grid cell of a window, its return taken from that bar's close to 5 bars later inside the window; "
               "the normal drift is the coin's mean 5-bar return on the grid of all its windows; the day-pooled t uses summed "
               "deviations per UTC day with a D/(D-1) correction; the situation check uses close location >= 0.8 "
               "(recorded high_close value, else from prices) and a negative forecast, the profile not being recomputable.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the active bars are short bars with a close location of at least 0.8, "
                           "the plan's situation and side." if n_active > 0 else
                           "The record has no active bar, so the config never takes the plan's short on high closes."),
            "reading": reading,
        }

    # ---------- cases ----------
    cases = []  # (coin, day, ret, loc)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            bets = _short_bets(fc)
            loc = _close_location(df)
            days = _to_days(df["timestamp"])
            for start in range(0, n, H):
                idx = np.where(bets[start:min(start + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n or not (close[t] > 0) or not np.isfinite(close[t + H]):
                    continue
                coin_cases.append((coin, days[t], close[t + H] / close[t] - 1.0, loc[t]))
        if len(grid_rets) == 0:
            continue
        drift[coin] = float(np.mean(grid_rets))
        for c in coin_cases:
            cases.append((c[0], c[1], -(c[2] - drift[coin]), c[3]))

    n_cases = len(cases)
    days_arr = np.array([c[1] for c in cases]) if n_cases else np.array([])
    n_days = int(len(np.unique(days_arr))) if n_cases else 0
    x = np.array([c[2] for c in cases], dtype=float)
    locs = np.array([c[3] for c in cases], dtype=float)

    mean = float(np.mean(x)) if n_cases else None
    tstat = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(x - mean).groupby(days_arr).sum().values
        var = (dev ** 2).sum() * n_days / (n_days - 1) / (n_cases ** 2)
        se = np.sqrt(var)
        tstat = float(mean / se) if se > 0 else None

    hi_g = x[np.isfinite(locs) & (locs >= 0.9)]
    lo_g = x[np.isfinite(locs) & (locs >= 0.8) & (locs < 0.9)]
    if len(hi_g) and len(lo_g):
        diff = float(hi_g.mean() - lo_g.mean())
        chk_pass = bool(diff > 0)
    else:
        diff, chk_pass = None, None

    counts = {"cases": n_cases, "distinct days": n_days,
              "cases at 0.9 or more": int(len(hi_g)), "cases from 0.8 to below 0.9": int(len(lo_g))}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases on 30 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif tstat is not None and mean > 0 and tstat >= 2 and chk_pass is True:
        status = "confirmed"
        decided = "The mean short-side unusual move is above 0 with a t of 2 or more, and the supporting check passes."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean short-side unusual move is below 0 with a t of -2 or less: prices rose after these closes."
    elif tstat is not None and mean > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "A confirming t with a failed supporting check is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases of one day pooled", "value": tstat}
                                       if tstat is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move at close location >= 0.9 minus 0.8 to < 0.9",
                             "value": diff, "passed": chk_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
