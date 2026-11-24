import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    MIN_DAYS = 30
    LHV = "debug_info.components.break_depth.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").to_numpy(dtype=float)
            else:
                lhv = np.full(len(df), np.nan)
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            situ = np.isfinite(lhv) & (lhv < 0)
            n_agree += int((active & situ & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The situation is read from the recorded break_depth raw value (same component and parameters as the "
               "detector's yl), with missing values counted as outside the situation; a case is the first bet "
               "(long forecast rise of at least 2 points from its lowest level since the last bet, from 0 after a flat) "
               "in each 10-bar grid cell of a window, cases without 10 bars ahead in the window are dropped, "
               "the drift is the mean of the coin's non-overlapping 10-bar grid returns over all its windows, "
               "the t clusters cases by UTC day with a D/(D-1) correction, and the slope is an OLS of the unusual move "
               "on the signal bar's forecast.")

    main_name = "mean unusual 10-bar move of long cases (return minus coin's 10-bar drift), before costs"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 on >= 30 distinct days and slope > 0; reject: mean < 0 with t <= -2 on >= 30 days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with the close below the "
                           "prior 365-day closing low, so the config does not do what the Fidelity's situation and side say."),
            "reading": reading,
        }

    # ---------- 2. Drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases ----------
    case_u, case_f, case_day = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").to_numpy()
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_pos = False
            for i in range(n):
                fi = f[i] if np.isfinite(f[i]) else 0.0
                if fi > 0:
                    if not prev_pos:
                        ref = 0.0
                    ref = min(ref, fi)
                    if fi - ref >= BAND:
                        bet[i] = True
                        ref = fi
                    prev_pos = True
                else:
                    prev_pos = False
                    ref = 0.0
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                r = c[t + H] / c[t] - 1.0
                case_u.append(r - d)
                case_f.append(f[t])
                case_day.append(pd.Timestamp(ts[t]).strftime("%Y-%m-%d"))

    u = np.asarray(case_u, dtype=float)
    fc = np.asarray(case_f, dtype=float)
    n_cases = int(len(u))
    n_days = int(len(set(case_day)))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1 and n_days > 1:
        dev = u - mean_u
        s = pd.Series(dev).groupby(pd.Series(case_day)).sum().to_numpy()
        var_mean = (n_days / (n_days - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        if var_mean > 0:
            t_val = float(mean_u / np.sqrt(var_mean))

    slope = None
    if n_cases > 2 and np.nanstd(fc) > 0:
        slope = float(stats.linregress(fc, u).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days over all coins and windows ({n_days})."
    elif t_val is not None and mean_u > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 on at least 30 distinct days and a positive slope on the forecast."
        else:
            status = "inconclusive"
            decided = "A confirming t with a slope at or below 0 is inconclusive."
    elif t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 on at least 30 distinct days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or cannot be computed), so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day together", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of unusual move on signal-bar forecast", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
