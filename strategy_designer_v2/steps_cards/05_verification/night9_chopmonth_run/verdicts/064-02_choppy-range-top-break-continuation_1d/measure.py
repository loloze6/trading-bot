import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    LOOKBACK = 30
    BRK_COL = "debug_info.components.brk.last_history_value"

    # ---------- 1. Situation check: close above the prior 30-day closing high, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # recomputed distance above the prior 30 closes' high (inside the window only)
            prior_high = close.shift(1).rolling(LOOKBACK, min_periods=LOOKBACK).max()
            dist_px = close - prior_high
            if BRK_COL in df.columns:
                raw = pd.to_numeric(df[BRK_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            in_sit = pd.Series(np.where(raw.notna(), raw > 0,
                                        np.where(dist_px.notna(), dist_px > 0, False)),
                               index=df.index).astype(bool)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean 5-bar unusual move per case (return from signal close minus coin's normal 5-bar drift)"
    main_thr = "mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject"
    sup_name = "OLS slope of the 5-bar unusual move on the signal-bar forecast, t >= 2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close is above "
                           "the prior 30-day closing high, as the plan's situation requires"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The situation is the plan's kept rule (distance above the prior 30-day closing high > 0, long); "
                       "the choppy profile, added by code, is not part of the check.",
        }

    # ---------- 2. Normal drift per coin: mean 5-bar return on the non-overlapping grid of all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: bets (rise of forecast on its side >= band), first one per 5-bar grid cell ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            side = 0
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                s = int(np.sign(f[i]))
                a = abs(f[i])
                if s == 0:
                    side, low = 0, 0.0
                    continue
                if s != side:
                    side, low = s, 0.0
                if a - low >= BAND:
                    bet[i] = True
                    low = a
                else:
                    low = min(low, a)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                u = np.sign(f[t]) * (r - drift[coin])
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), float(u), float(f[t])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)

    mean_u = None
    t_u = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        d = np.array([x[0] for x in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby(d).sum().to_numpy()
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t_u = float(mean_u / se) if se > 0 else None

    slope = None
    slope_t = None
    if n_cases >= 3:
        fx = np.array([x[2] for x in cases])
        uy = np.array([x[1] for x in cases])
        if np.std(fx) > 0:
            lr = stats.linregress(fx, uy)
            slope = float(lr.slope)
            slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup_pass = None if slope_t is None else bool(slope_t >= 2)

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum count not reached: {n_cases} cases (needs 30) and {n_days} distinct days (needs 20), "
                   "too few to decide either way.")
    elif t_u is None:
        status = "inconclusive"
        decided = "The day-pooled t of the mean unusual move could not be computed, so neither rule is met."
    elif mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 on at least 30 cases, and the forecast slope has t >= 2."
        else:
            status = "inconclusive"
            decided = "A positive main measure with t >= 2 whose supporting slope has t < 2 is inconclusive."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 on at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The day-pooled t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day pooled", "value": t_u}
                                       if t_u is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The situation check uses the recorded brk raw value (> 0, long) and the recomputed distance "
                    "where it is missing, and leaves out the code-added choppy profile; a case is the first bet of "
                    "each 5-bar grid cell from each window's first row, the day-pooled t uses the per-day sums of "
                    "deviations with a G/(G-1) correction, and the supporting t is the ordinary OLS slope t."),
    }
