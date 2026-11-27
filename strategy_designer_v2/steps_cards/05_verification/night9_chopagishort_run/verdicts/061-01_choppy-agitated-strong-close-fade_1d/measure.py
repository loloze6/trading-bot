import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    BAND = 2.0
    MIN_CASES = 30
    EPS = 1e-12

    def close_loc(df):
        h = df["high"].astype(float).values
        l = df["low"].astype(float).values
        c = df["close"].astype(float).values
        rng = h - l
        with np.errstate(divide="ignore", invalid="ignore"):
            loc = np.where(rng > 0, (c - l) / rng, np.nan)
        return loc

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            loc = close_loc(df)
            active = np.isfinite(f) & (f != 0)
            situ = np.isfinite(loc) & (loc >= 0.8 - 1e-9)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The situation is checked as the close location recomputed from each bar's high, low and close being "
               "at least 0.8 with a negative forecast (the choppy-agitated profile is the config's veto, not recomputed); "
               "a case is a short bet (the forecast's short size rising by at least 2 points from its lowest short level "
               "since the last bet, from 0 after flat or long), the first per 2-bar grid cell of each window; the drift is "
               "each coin's mean non-overlapping 2-bar return over all its windows; the t is the mean over a day-clustered "
               "standard error; an empty close-location group makes the supporting check fail.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 2-bar move of short signals, short direction",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 (confirm) or t <= -2 (reject) over at least 30 cases"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of active bars are short bars with the close in the top 20% of the day's "
                           "range, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    cases = []  # (day, unusual_short, loc)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            loc = close_loc(df)
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            ref = 0.0
            used_cells = set()
            n = len(df)
            for t in range(n):
                s = -f[t]
                if s <= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND - EPS:
                    ref = s
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H >= n:
                        continue
                    if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                        continue
                    r = c[t + H] / c[t] - 1.0
                    cases.append((ts[t], -(r - drift[coin]), loc[t]))
                else:
                    ref = min(ref, s)

    n_cases = len(cases)
    if n_cases > 0:
        cdf = pd.DataFrame(cases, columns=["day", "u", "loc"])
        mean_u = float(cdf["u"].mean())
        n_days = int(cdf["day"].nunique())
        g = cdf.groupby("day")["u"].agg(["sum", "count"])
        resid = g["sum"].values - g["count"].values * mean_u
        if n_days > 1:
            se = np.sqrt(np.sum(resid ** 2) * n_days / (n_days - 1)) / n_cases
            t_stat = float(mean_u / se) if se > 0 else None
        else:
            t_stat = None
        hi = cdf.loc[cdf["loc"] >= 0.9, "u"]
        mid = cdf.loc[(cdf["loc"] >= 0.8) & (cdf["loc"] < 0.9), "u"]
        n_hi, n_mid = int(len(hi)), int(len(mid))
        if n_hi > 0 and n_mid > 0:
            diff = float(hi.mean() - mid.mean())
            sup_pass = bool(diff >= 0)
        else:
            diff = None
            sup_pass = False
    else:
        mean_u, t_stat, n_days, diff, sup_pass, n_hi, n_mid = None, None, 0, None, False, 0, 0

    # ---------- 4. decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_stat >= 2 and mean_u > 0:
        if sup_pass:
            status = "confirmed"
            decided = ("The mean unusual move in the short direction is positive with t >= 2 over at least 30 cases "
                       "and the supporting check passes.")
        else:
            status = "inconclusive"
            decided = "The main measure confirms but the supporting check fails."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction has t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": "mean unusual 2-bar move of short signals, short direction",
                         "value": mean_u,
                         "statistic": None if t_stat is None else {"name": "t of the mean, cases pooled by day",
                                                                   "value": float(t_stat)},
                         "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases"},
        "supporting_check": {"name": "mean unusual move (loc >= 0.9) minus (0.8 <= loc < 0.9)",
                             "value": diff, "passed": bool(sup_pass)},
        "counts": {"cases": int(n_cases), "days": int(n_days),
                   "cases loc >= 0.9": int(n_hi), "cases loc 0.8-0.9": int(n_mid)},
        "decided_by": decided,
        "reading": reading,
    }
