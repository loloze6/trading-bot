import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    DEPTH = "debug_info.components.depth.last_history_value"

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            v = s.astype("float64")
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
            dt = pd.to_datetime(v, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            low = pd.to_numeric(df["low"], errors="coerce")
            prior_low = low.shift(1).rolling(20, min_periods=20).min().values
            recomputed = (close / prior_low - 1.0) * 100.0
            if DEPTH in df.columns:
                raw = pd.to_numeric(df[DEPTH], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            dist = np.where(np.isfinite(raw), raw, recomputed)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            choppy = regime != "chop"
            situation = np.isfinite(dist) & (dist < 0) & choppy
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-bar move over the cases (long)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and slope on forecast > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation = recorded depth raw value (or its recomputation from prior 20 lows) below 0 on a bar whose regime "
               "is not the 'chop' veto, long side; a case is the first bet (forecast rise of >= 2 points from its lowest long "
               "level since the last bet, reset at flat) in each 5-bar grid cell of a window counted from its first row, needing "
               "close 5 bars later in the same window; drift = mean of the coin's non-overlapping 5-bar grid returns over all "
               "windows; t clusters cases by UTC day with a G/(G-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are long bars where the close is below the prior 20-day low "
                           "in a choppy market, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_moves, case_fc, case_days = [], [], []
    for coin, wins in bars.items():
        # coin's normal drift over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            days = to_days(df["timestamp"])
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            lowest = 0.0
            for t in range(n):
                v = f[t]
                if v <= 0:
                    lowest = 0.0
                    continue
                if v - lowest >= BAND:
                    bet[t] = True
                    lowest = v
                else:
                    lowest = min(lowest, v)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                case_moves.append(r - drift)
                case_fc.append(f[t])
                case_days.append(days[t])

    x = np.array(case_moves, dtype=float)
    fc = np.array(case_fc, dtype=float)
    n_cases = int(len(x))
    n_days = int(len(set(case_days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = float(np.mean(x)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(x - mean).groupby(pd.Series(case_days)).sum().values
        G = len(dev)
        var = (G / (G - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
        if var > 0:
            tstat = float(mean / np.sqrt(var))

    slope = None
    if n_cases > 1 and np.var(fc) > 0:
        slope = float(np.sum((fc - fc.mean()) * (x - x.mean())) / np.sum((fc - fc.mean()) ** 2))
    slope_pass = None if slope is None else bool(slope > 0)

    main = {"name": main_name, "value": mean,
            "statistic": None if tstat is None else {"name": "t of the mean, cases clustered by day", "value": tstat},
            "threshold": thr}
    supp = {"name": "OLS slope of unusual move on forecast", "value": slope, "passed": slope_pass}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases on {n_days} distinct days, "
                   "the plan needs at least 30 of each.")
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject applies."
    elif mean > 0 and tstat >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and a positive slope on the forecast: the confirm rule holds."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the reject rule holds."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the forecast is 0 or below (or undefined): inconclusive by the plan."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2: inconclusive by the plan."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
