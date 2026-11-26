import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    ER_N = 30
    ER_MAX = 0.3
    BAND = 2.0
    MIN_DAYS = 30
    MV_COL = "debug_info.components.move7.last_history_value"

    def prep(df):
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        return df

    data = {}
    for coin, wins in bars.items():
        data[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[coin][w] = prep(df)

    # ---------- 1. situation check ----------
    n_active = 0
    n_eval = 0
    n_agree = 0
    for coin, wins in data.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].values.astype(float)
            ser = pd.Series(c)
            net = (ser - ser.shift(ER_N)).abs()
            path = ser.diff().abs().rolling(ER_N, min_periods=ER_N).sum()
            er = (net / path.replace(0, np.nan)).values
            ret30 = (ser / ser.shift(ER_N) - 1.0).values
            ret7 = (ser / ser.shift(H) - 1.0).values
            if MV_COL in df.columns:
                mvrec = pd.to_numeric(df[MV_COL], errors="coerce").values
            else:
                mvrec = np.full(n, np.nan)
            mv = np.where(np.isfinite(mvrec), mvrec, ret7)
            for i in range(n):
                if f[i] == 0 or not np.isfinite(f[i]):
                    continue
                n_active += 1
                if not (np.isfinite(er[i]) and np.isfinite(ret30[i]) and np.isfinite(mv[i])):
                    continue
                n_eval += 1
                side = 0
                if er[i] < ER_MAX:
                    if ret30[i] > 0 and mv[i] > 0:
                        side = 1
                    elif ret30[i] < 0 and mv[i] < 0:
                        side = -1
                if side != 0 and np.sign(f[i]) == side:
                    n_agree += 1

    reading = ("Active bars whose 30-bar efficiency ratio or 30-bar return cannot be computed inside their window "
               "(first 30 recorded bars) are left out of the situation check; a case is the first bet (forecast rise "
               "of at least 2 points on its side) in each 7-bar grid cell counted from the window's first row; the "
               "drift is the coin's mean 7-bar return on that grid over all its windows; the day-clustered t uses "
               "per-day summed deviations with a G/(G-1) correction; large cases are |forecast| strictly above the "
               "cases' median.")

    if n_active == 0 or n_eval == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": None},
            "main_measure": {"name": "mean unusual 7-bar move of cases, in forecast direction", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2 (confirm); mean < 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"distinct case days": 0, "cases": 0, "active bars": int(n_active)},
            "decided_by": "No active bars with an evaluable situation: fewer than 30 distinct case days.",
            "reading": reading,
        }

    agreement = n_agree / n_eval
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 7-bar move of cases, in forecast direction", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "evaluated active bars": int(n_eval)},
            "decided_by": ("Under 90% of active bars are choppy (ER<0.3) bars with 30-bar and 7-bar returns aligned "
                           "and the forecast on their side (long after rises, short after falls)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # drift per coin
    drift = {}
    for coin, wins in data.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, |forecast|)
    for coin, wins in data.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            ts = df["timestamp"]
            n = len(c)
            side = 0
            trough = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i] if np.isfinite(f[i]) else 0.0
                if fi == 0:
                    side = 0
                    trough = 0.0
                    continue
                s = 1 if fi > 0 else -1
                a = abs(fi)
                if s != side:
                    side = s
                    trough = 0.0
                if a - trough >= BAND:
                    bet[i] = True
                    trough = a
                else:
                    trough = min(trough, a)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                i = start + idx[0]
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                d = 1.0 if f[i] > 0 else -1.0
                u = d * (r - drift[coin])
                cases.append((ts.iloc[i].strftime("%Y-%m-%d"), u, abs(f[i])))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)

    mean_u = None
    tval = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([x[0] for x in cases]).sum().values
        G = len(dev)
        if G > 1:
            var = (dev ** 2).sum() / (n_cases ** 2) * G / (G - 1)
            se = np.sqrt(var)
            tval = float(mean_u / se) if se > 0 else None

    diff = None
    sup_pass = None
    if n_cases > 0:
        af = np.array([x[2] for x in cases])
        u = np.array([x[1] for x in cases])
        med = np.median(af)
        lg = u[af > med]
        sm = u[af <= med]
        if len(lg) > 0 and len(sm) > 0:
            diff = float(lg.mean() - sm.mean())
            sup_pass = bool(diff > 0)
        else:
            sup_pass = False

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif mean_u is not None and tval is not None and mean_u > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and the large-minus-small difference above 0."
    elif mean_u is not None and tval is not None and mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the moves are given back."
    else:
        status = "inconclusive"
        if tval is not None and tval >= 2 and not sup_pass:
            decided = "t >= 2 but the supporting large-minus-small check fails, which the plan calls inconclusive."
        else:
            decided = "The day-clustered t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 7-bar move of cases, in forecast direction",
            "value": mean_u,
            "statistic": {"name": "day-clustered t", "value": tval} if tval is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual move of |forecast| above median minus at or below median",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"distinct case days": int(n_days), "cases": int(n_cases)},
        "decided_by": decided,
        "reading": reading,
    }
