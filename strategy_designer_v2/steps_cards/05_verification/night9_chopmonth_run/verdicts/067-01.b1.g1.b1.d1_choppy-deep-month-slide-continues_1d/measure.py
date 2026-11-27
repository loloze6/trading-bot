import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    FC = "forecast"
    RAW = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for i in range(n):
                if f[i] == 0:
                    continue
                n_active += 1
                if i >= 60 and close[i - 60] > 0:
                    tr60 = (close[i] / close[i - 60] - 1.0) * 100.0
                    chop = (-10.0 <= tr60 <= 10.0)
                else:
                    chop = (reg[i] == "chop")
                if i >= 30 and close[i - 30] > 0:
                    r30 = (close[i] / close[i - 30] - 1.0) * 100.0
                else:
                    r30 = raw[i]
                if not np.isnan(raw[i]):
                    r30 = raw[i]
                fall = (r30 is not None) and (not np.isnan(r30)) and (r30 < 0)
                if chop and fall and f[i] < 0:
                    n_agree += 1

    reading = ("The 60-day return is recomputed from closes inside the window (recorded regime used where 60 prior bars "
               "are not in the window) and the 30-day fall is the recorded fall30 raw value < 0; a bet is a rise of the "
               "short forecast's size of >= 2 points from its lowest level since the last bet (reset at flat), the first "
               "bet in each 10-bar grid cell of a window is the case, drift is the coin's mean 10-bar grid return over "
               "all its windows, the t clusters cases by UTC day with a G/(G-1) correction, thirds are equal splits of "
               "cases sorted by |forecast|, and fewer than 30 distinct days gives 'not observable'.")

    main_name = "mean signed unusual 10-bar move of short bets (minus coin drift, x -1)"
    thr = "t >= 2 with positive mean confirms (with check); t <= -2 with negative mean rejects"
    sup_name = "largest-forecast third minus smallest third of signed unusual move"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"distinct days with cases": 0, "cases": 0},
            "decided_by": "No active bars: the minimum of 30 distinct days with cases is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars in a chop market (60-day return in -10..+10%) "
                           "after a 30-day fall, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    vals, sizes, days = [], [], []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                if f[i] >= 0:
                    ref = 0.0
                    continue
                mag = -f[i]
                if mag - ref >= BAND:
                    bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (c[i] > 0) or not np.isfinite(c[i + H]):
                    continue
                r = c[i + H] / c[i] - 1.0
                vals.append(-(r - drift[coin]))
                sizes.append(abs(f[i]))
                days.append(ts.iloc[i].floor("D"))

    n_cases = len(vals)
    n_days = len(set(days))
    counts = {"distinct days with cases": int(n_days), "cases": int(n_cases)}

    if n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name,
                             "value": float(np.mean(vals)) if n_cases else None,
                             "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"The minimum of 30 distinct days with cases is not reached ({n_days}).",
            "reading": reading,
        }

    x = np.array(vals, dtype=float)
    mean = float(x.mean())
    dev = pd.Series(x - mean).groupby(pd.Series(days)).sum().values
    G = len(dev)
    se = np.sqrt(G / (G - 1.0) * np.sum(dev ** 2)) / n_cases if G > 1 else np.nan
    t = float(mean / se) if se and np.isfinite(se) and se > 0 else float("nan")

    order = np.argsort(np.array(sizes), kind="mergesort")
    thirds = np.array_split(x[order], 3)
    if all(len(p) > 0 for p in thirds):
        diff = float(thirds[2].mean() - thirds[0].mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None

    if np.isfinite(t) and t >= 2 and mean > 0 and sup_pass is True:
        status = "confirmed"
        decided = "Mean signed unusual move positive with t >= 2 and largest third minus smallest third > 0."
    elif np.isfinite(t) and t <= -2 and mean < 0:
        status = "rejected"
        decided = "Mean signed unusual move negative with t <= -2: coins rebound after deep slides in choppy markets."
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the largest-third minus smallest-third difference is at or below 0 (or undefined)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": {"name": "t of the mean, cases summed per day",
                                       "value": t if np.isfinite(t) else None},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
