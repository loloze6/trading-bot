import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_week_rise.last_history_value"

    # ---------- 1. Situation check: a 7-day rise (raw value > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # recompute the 7-day return inside the window where the raw value is missing
            ret7 = np.full(len(df), np.nan)
            if len(df) > 7:
                ret7[7:] = close[7:] / close[:-7] - 1.0
            sit_val = np.where(np.isnan(raw), ret7, raw)
            active = f != 0
            n_active += int(active.sum())
            agree = active & (f > 0) & (np.nan_to_num(sit_val, nan=0.0) > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 3-bar move of the cases", "value": None,
                             "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct days with cases": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on which the "
                           "coin has risen over the last 7 days, the plan's situation and side."),
            "reading": "none",
        }

    # ---------- 2. Normal drift per coin: mean non-overlapping 3-bar return over all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            for t in range(0, len(df) - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: bets (forecast rise >= band on the long side), once per grid cell ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            trough = 0.0
            for t in range(n):
                v = f[t]
                if v <= 0:
                    trough = 0.0
                    continue
                trough = min(trough, v)
                if v - trough >= BAND:
                    bet[t] = True
                    trough = v
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), r - drift[coin], float(f[t])))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)

    reading = ("A case is the first bar in each non-overlapping 3-bar grid cell (from each window's first row) "
               "where the forecast rises by at least 2 points above its lowest positive level since the last bet "
               "(from 0 after a flat), its return taken from that bar's close over 3 bars inside the window; "
               "the t is the mean over its day-clustered standard error (deviations summed per day); the halves "
               "are the top and bottom floor(n/2) cases by forecast at the signal, the middle case dropped when n is odd.")

    mean_u = None
    t_u = None
    diff = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        fc = np.array([c[2] for c in cases])
        mean_u = float(u.mean())
        dser = pd.Series(u - mean_u, index=[c[0] for c in cases]).groupby(level=0).sum()
        D = len(dser)
        if D > 1:
            se = np.sqrt(float((dser.values ** 2).sum()) * D / (D - 1)) / n_cases
            t_u = float(mean_u / se) if se > 0 else None
        if n_cases >= 2:
            order = np.argsort(fc, kind="mergesort")
            half = n_cases // 2
            small = u[order[:half]]
            large = u[order[n_cases - half:]]
            diff = float(large.mean() - small.mean())

    counts = {"distinct days with cases": n_days, "cases": n_cases}
    main = {"name": "mean unusual 3-bar move of the cases",
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day pooled", "value": t_u} if t_u is not None else None,
            "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"}
    sup_pass = None if diff is None else bool(diff > 0)
    sup = {"name": "larger-forecast half minus smaller-forecast half mean unusual move",
           "value": diff, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, fewer than the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither rule is met."
    elif mean_u > 0 and t_u >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the larger-minus-smaller difference is above 0."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif t_u >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the supporting difference is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
