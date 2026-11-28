import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            if len(df) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # up-day indicator: the raw scaled rise when recorded, else the day's price return
            upval = np.where(np.isfinite(raw), raw, ret1)
            for i in range(len(df)):
                if fc[i] != 0:
                    n_active += 1
                    if np.isfinite(upval[i]) and upval[i] > 0 and fc[i] < 0:
                        n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 3-bar move per short case (signed short)"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 and check passed; reject: mean < 0 with day-clustered t <= -2"
    sup_name = "mean unusual move (forecast <= -10) minus (0 > forecast > -10)"
    reading = ("The situation is an up day (raw scaled rise > 0, or the day's close-to-close return when the raw value "
               "is not recorded) with a short forecast; a case is the first short bet (forecast falling >= 2 points below "
               "its least-short level since the last bet, reset at flat) in each 3-bar grid cell from each window's first "
               "row, with a full 3-bar return inside the window; the drift is each coin's mean non-overlapping 3-bar return "
               "over all its windows; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the "
               "plan's 'fewer than 30 days' rule is reported as not observable; an empty forecast group makes the check fail.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are up days with a short forecast, "
                           "so the config does not fade up days as the plan's Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, forecast, ret)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            anchor = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                if fc[i] >= 0:
                    anchor = 0.0
                    continue
                depth = -fc[i]
                if depth - anchor >= BAND - 1e-12:
                    bet[i] = True
                    anchor = depth
                else:
                    anchor = min(anchor, depth)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                if not np.isfinite(drift.get(coin, np.nan)) or pd.isna(ts.iloc[i]):
                    continue
                r = close[i + H] / close[i] - 1.0
                u = -(r - drift[coin])
                cases.append((coin, ts.iloc[i].normalize(), float(fc[i]), float(u)))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([c[3] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u, index=[c[1] for c in cases])
        S = dev.groupby(level=0).sum().values
        G = len(S)
        if G > 1:
            var = (S ** 2).sum() * G / (G - 1) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    big = [c[3] for c in cases if c[2] <= -10]
    small = [c[3] for c in cases if -10 < c[2] < 0]
    if big and small:
        diff = float(np.mean(big) - np.mean(small))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False

    counts = {"days with cases": int(n_days), "cases": int(n_cases),
              "cases forecast <= -10": int(len(big)), "cases 0 > forecast > -10": int(len(small))}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} days with cases, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with a day-clustered t >= 2 and the larger-rise cases fall more."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (t >= 2) but the supporting check fails."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with a day-clustered t <= -2 (prices rise after up days)."
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "day-clustered t", "value": t_val} if t_val is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
