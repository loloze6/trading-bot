import numpy as np
import pandas as pd

RAW = "debug_info.components.vol_move.last_history_value"
H = 24
BAND = 2.0
MIN_CASES = 30


def _f(x):
    if x is None:
        return None
    x = float(x)
    return None if not np.isfinite(x) else x


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            hour_ret = np.full(len(close), np.nan)
            if len(close) > 1:
                hour_ret[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(close), np.nan)
            # situation: a rising hour (raw = scaled return x volume ratio > 0); fall back to price if raw missing
            rising = np.where(np.isfinite(raw), raw > 0, np.where(np.isfinite(hour_ret), hour_ret > 0, False))
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & rising & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90 % of active bars are long bars on a rising hour (positive raw "
                           "volume-weighted scaled return), as the Fidelity's situation and long side require"
                           if n_active > 0 else "the forecast is never active"),
            "reading": "situation taken as a positive raw component value (a rising hour), side long; "
                       "the graded dead zone is not a hard cut, so any rising hour counts.",
        }

    # ---------- 2. coin drift and usual move ----------
    coin_stats = {}
    for coin in bars:
        rets = []
        for w in bars[coin]:
            close = pd.to_numeric(bars[coin][w]["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        rets = np.asarray(rets, dtype=float)
        if len(rets) >= 2:
            coin_stats[coin] = (float(rets.mean()), float(rets.std(ddof=1)))
        else:
            coin_stats[coin] = (np.nan, np.nan)

    # ---------- 3. cases ----------
    unusual, strength, case_fc = [], [], []
    for coin in bars:
        drift, usual = coin_stats[coin]
        for w in bars[coin]:
            df = bars[coin][w]
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(fc)
            low = 0.0
            bets = np.zeros(n, dtype=bool)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bets[t] = True
                    low = f
                else:
                    low = min(low, f)
            for c0 in range(0, n, H):
                idx = np.nonzero(bets[c0:c0 + H])[0]
                if len(idx) == 0:
                    continue
                t = c0 + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not (np.isfinite(r) and np.isfinite(drift) and np.isfinite(usual) and usual > 0):
                    continue
                u = r - drift
                unusual.append(u)
                strength.append(u / usual)
                case_fc.append(fc[t])

    unusual = np.asarray(unusual, dtype=float)
    strength = np.asarray(strength, dtype=float)
    case_fc = np.asarray(case_fc, dtype=float)
    n_cases = int(len(strength))

    mean_s = float(strength.mean()) if n_cases > 0 else None
    t_s = None
    if n_cases >= 2:
        sd = strength.std(ddof=1)
        t_s = float(mean_s / (sd / np.sqrt(n_cases))) if sd > 0 else None
    mean_u = float(unusual.mean()) if n_cases > 0 else None

    # supporting check
    sup_val, sup_pass = None, None
    n_hi = n_lo = 0
    if n_cases > 0:
        med = float(np.median(case_fc))
        hi = case_fc > med
        lo = ~hi
        n_hi, n_lo = int(hi.sum()), int(lo.sum())
        if n_hi > 0 and n_lo > 0:
            sup_val = float(unusual[hi].mean() - unusual[lo].mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    # ---------- 4. decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"fewer than {MIN_CASES} cases in total (BTC and ETH together): {n_cases}."
    elif t_s is not None and mean_s > 0 and t_s >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean unusual move positive with t >= 2 over at least 30 cases, and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "a confirming t (>= 2) whose supporting check fails is inconclusive."
    elif t_s is not None and mean_s < 0 and t_s <= -2:
        status = "rejected"
        decided = "mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean strength of the 24-bar unusual move of bets",
            "value": mean_s,
            "statistic": {"name": "t of the mean", "value": t_s} if t_s is not None else None,
            "threshold": "confirm: positive with t >= 2 over >= 30 cases; reject: negative with t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "mean unusual move, forecast above case median minus at or below",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "cases": n_cases,
            "cases above median forecast": int(n_hi),
            "cases at or below median forecast": int(n_lo),
            "active bars": int(n_active),
        },
        "decided_by": decided,
        "reading": ("a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet, "
                    "reset to 0 after a flat) in each 24-bar grid cell counted from each window's first row, "
                    "dropped when its 24-bar return leaves the window; drift and usual move are the mean and std "
                    "of the coin's grid 24-bar returns over all windows; the confirm/reject t is the t of the mean "
                    "strength (the plan's main measure), and the supporting check splits cases by the signal bar's "
                    "forecast against the cases' median; situation = positive raw component (rising hour) on the long side."),
    }
