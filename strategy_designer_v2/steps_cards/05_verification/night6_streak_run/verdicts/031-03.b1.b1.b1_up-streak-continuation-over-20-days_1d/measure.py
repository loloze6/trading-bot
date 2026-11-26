import numpy as np
import pandas as pd

H = 20
BAND = 2.0
MIN_DAYS = 30
RAW = "debug_info.components.streak_rank.last_history_value"


def _bets(f):
    """Long bets: forecast rise of at least BAND from its lowest level since the last bet (from 0 after a flat)."""
    out = np.zeros(len(f), dtype=bool)
    low = 0.0
    for i, v in enumerate(f):
        if not np.isfinite(v) or v <= 0:
            low = 0.0
            continue
        if v - low >= BAND:
            out[i] = True
            low = v
        else:
            low = min(low, v)
    return out


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            ret30 = np.full(len(df), np.nan)
            if len(df) > 30:
                ret30[30:] = close[30:] / close[:-30] - 1.0
            for i in range(len(df)):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                if not np.isfinite(ret30[i]):
                    continue  # 30-day return not computable inside the window
                n_active += 1
                situ = (ret30[i] > 0) and np.isfinite(raw[i]) and (raw[i] > 0)
                if situ and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Situation = 30-day close return > 0 (recomputed inside each window, active bars of a window's first 30 rows left out "
               "of the check) and raw streak rank > 0, expected side long; a case is the first long bet (forecast rise >= 2 "
               "from its low since the last bet, from 0 after a flat) in each 20-bar grid cell of a window, its return taken "
               "from that bar's close 20 bars on inside the window, the drift is the mean non-overlapping 20-bar grid return "
               "over all the coin's windows, t uses day-clustered deviations, and the thirds are the first and last n//3 "
               "cases sorted by forecast value at the signal bar.")

    main_name = "mean unusual 20-bar move of cases (forecast rise >= 2), before costs"
    thr = "confirm: mean > 0 with t >= 2 and top-third minus bottom-third > 0; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90 % of active bars are bars with a positive 30-day return and an up streak "
                           "with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, forecast, unusual)
    for coin, wins in bars.items():
        grid_rets = []
        per_window = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            n = len(df)
            for p in range(0, n, H):
                if p + H < n and np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            per_window.append((df, close, fc))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for df, close, fc in per_window:
            n = len(df)
            bet = _bets(fc)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (np.isfinite(close[i]) and np.isfinite(close[i + H])) or close[i] <= 0:
                    continue
                r = close[i + H] / close[i] - 1.0
                day = ts.iloc[i]
                if pd.isna(day):
                    continue
                cases.append((coin, day.strftime("%Y-%m-%d"), float(fc[i]), float(r - drift)))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct case days": int(n_days)}

    mean_u = None
    t = None
    if n_cases > 0:
        u = np.array([c[3] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([c[1] for c in cases]).sum().to_numpy()
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    k = n_cases // 3
    if k >= 1:
        order = sorted(range(n_cases), key=lambda j: (cases[j][2], cases[j][1], cases[j][0]))
        bottom = np.mean([cases[j][3] for j in order[:k]])
        top = np.mean([cases[j][3] for j in order[-k:]])
        sup_val = float(top - bottom)
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean, cases summed per day", "value": t} if t is not None else None),
            "threshold": thr}
    sup = {"name": "top-third minus bottom-third mean unusual move (by forecast size)",
           "value": sup_val, "passed": sup_pass}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif t is not None and mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the top third beats the bottom third."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-third case mean is not above the bottom-third one."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or cannot be computed)."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
