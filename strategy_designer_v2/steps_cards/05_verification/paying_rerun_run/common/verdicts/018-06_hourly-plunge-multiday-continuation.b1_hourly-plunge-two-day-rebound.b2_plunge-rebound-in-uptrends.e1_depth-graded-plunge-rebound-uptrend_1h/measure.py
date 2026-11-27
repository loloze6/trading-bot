import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 96
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.plunge_in_uptrend.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            # fall back to prices where the raw value is missing (within the window only)
            c = pd.Series(close)
            fall24 = (c / c.shift(24) - 1.0).to_numpy()
            rise720 = (c / c.shift(720) - 1.0).to_numpy()
            price_sit = (fall24 < 0) & (rise720 > 0)
            sit = np.where(np.isnan(raw), price_sit, raw > 0)
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 96-bar move of long bets (return minus coin's mean 96-bar return)"
    thr = "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject; at least 30 independent cases"
    sup_name = "Spearman rank correlation of forecast at case bar vs unusual move > 0"
    reading = ("Situation = raw component > 0 (24h fall with positive 30-day return, recomputed from prices where the raw "
               "value is missing) on the long side; cases are long bets (forecast rise >= 2 from its lowest positive level "
               "since the last bet, from 0 after a flat), the first one in each 96-bar grid cell of a window counted from its "
               "first row, kept only if the 96-bar forward return stays inside the window; the drift is the coin's mean "
               "return on the 0, 96, 192, ... grid of all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the coin fell over "
                           "24 hours with a positive 30-day return, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean of non-overlapping 96-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    moves = []
    fcs = []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            on_long = False
            trough = 0.0
            for i in range(n):
                fi = f[i]
                if np.isfinite(fi) and fi > 0:
                    if not on_long:
                        on_long = True
                        trough = 0.0
                    trough = min(trough, fi)
                    if fi - trough >= BAND:
                        bet[i] = True
                        trough = fi
                else:
                    on_long = False
                    trough = 0.0
            for start in range(0, n, H):
                idx = np.where(bet[start:min(start + H, n)])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= n:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                moves.append((b / a - 1.0) - drift[coin])
                fcs.append(f[i])

    moves = np.asarray(moves, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    ncase = int(len(moves))
    mean = float(np.mean(moves)) if ncase > 0 else None
    t = None
    if ncase >= 2:
        sd = float(np.std(moves, ddof=1))
        if sd > 0:
            t = float(mean / (sd / np.sqrt(ncase)))
    rho = None
    if ncase >= 3 and np.std(fcs) > 0 and np.std(moves) > 0:
        r = stats.spearmanr(fcs, moves).correlation
        rho = float(r) if np.isfinite(r) else None
    sup_pass = (rho > 0) if rho is not None else None

    if ncase < MIN_CASES:
        status = "not observable"
        decided = f"Only {ncase} independent cases, fewer than the plan's minimum of 30."
    elif t is not None and mean > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 independent cases, and the Spearman correlation is above 0."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 independent cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the rank correlation is 0 or below (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": rho, "passed": sup_pass},
        "counts": {"independent cases": ncase},
        "decided_by": decided,
        "reading": reading,
    }
