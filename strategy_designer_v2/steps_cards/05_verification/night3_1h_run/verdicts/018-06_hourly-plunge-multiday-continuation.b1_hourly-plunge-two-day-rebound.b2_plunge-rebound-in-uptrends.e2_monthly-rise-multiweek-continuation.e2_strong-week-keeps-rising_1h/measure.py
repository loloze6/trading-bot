import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 168
    BAND = 2.0
    RAW = "debug_info.components.week_rise.last_history_value"

    # ---------- 1. Situation check: raw 168-bar return > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            recomputed = close / close.shift(H) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 168-bar move after bets (return minus coin's normal 168-bar drift)"
    main_thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars with a positive 7-day return held long, as the plan's situation and side require.",
            "reading": "Situation taken as the raw 168-bar return (last_history_value) above 0 with a positive forecast.",
        }

    # ---------- 2. Normal drift per coin: mean non-overlapping 168-bar return ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for t in range(0, n - H, H):
                a, b = close[t], close[t + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: bets (rise of long forecast >= 2 from its low since last bet) ----------
    unusual = []
    fc_at = []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(f)
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi):
                    continue
                if fi <= 0:
                    low = 0.0
                    continue
                if fi - low >= BAND:
                    bet[i] = True
                    low = fi
                else:
                    low = min(low, fi)
            for start in range(0, n, H):
                idx = np.nonzero(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                unusual.append((b / a - 1.0) - d)
                fc_at.append(f[t])

    u = np.asarray(unusual, dtype=float)
    x = np.asarray(fc_at, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t_stat = float(mean_u / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases >= 3 and np.unique(x).size >= 2:
        slope = float(stats.linregress(x, u).slope)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled over the coins and windows, fewer than the plan's minimum of 30."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2:
        if slope is not None and slope > 0:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 over at least 30 cases and the supporting slope is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure is at t >= 2 but the slope of the unusual move on the forecast is at or below 0."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t-statistic of the mean unusual move lies between -2 and 2."

    sup_passed = None if slope is None else bool(slope > 0)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "slope of unusual move on forecast at signal bar",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": "A bet is a rise of the positive forecast of at least 2 points from its lowest level since the last bet (reset to 0 when the forecast is not positive and at each window's start), the first bet of each 168-bar grid cell counted from the window's first row is the case, cases without 168 bars ahead in their window are dropped, and the normal drift is the coin's mean non-overlapping 168-bar return over all its windows.",
    }
