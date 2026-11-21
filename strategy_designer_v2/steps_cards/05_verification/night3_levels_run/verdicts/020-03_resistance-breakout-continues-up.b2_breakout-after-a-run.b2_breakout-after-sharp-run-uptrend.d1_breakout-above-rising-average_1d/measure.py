import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    BRK = "debug_info.components.break.last_history_value"
    MAD = "debug_info.components.ma_dist.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            brk = pd.to_numeric(df[BRK], errors="coerce").values if BRK in df.columns else np.full(len(df), np.nan)
            mad = pd.to_numeric(df[MAD], errors="coerce").values if MAD in df.columns else np.full(len(df), np.nan)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            for t in range(len(df)):
                if fc[t] == 0:
                    continue
                n_active += 1
                if t >= 60 and close[t - 60] > 0:
                    ret60_ok = (close[t] / close[t - 60] - 1.0) > 0
                else:
                    ret60_ok = regime[t] == "trending"
                brk_ok = np.isfinite(brk[t]) and brk[t] > 0
                mad_ok = np.isfinite(mad[t]) and mad[t] > 0
                if brk_ok and mad_ok and ret60_ok and fc[t] > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean 5-bar unusual move (return minus coin's normal 5-bar drift, in signal direction)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("ret60 is recomputed from closes inside the window where 60 prior bars exist, else taken from the recorded "
               "regime being 'trending'; break and ma_dist conditions use their recorded raw values; a case is the first "
               "bet bar (forecast rise of >= 2 points on its side from its lowest level since the last bet, from 0 after "
               "flat) in each 5-bar grid cell of a window, with a full 5-bar forward return inside that window; drift is "
               "the coin's mean 5-bar return on the grid positions 0,5,10,... of all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of active bars are long bars where the close has just broken above a 90-bar "
                           "swing-high level with the 60-bar return positive and the close above its 50-bar SMA."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    fcs = []
    for coin, wins in bars.items():
        # coin's normal 5-bar drift over all its windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            # detect bets
            is_bet = np.zeros(n, dtype=bool)
            side = 0
            base = 0.0
            for t in range(n):
                f = fc[t]
                s = 1 if f > 0 else (-1 if f < 0 else 0)
                if s == 0:
                    side = 0
                    base = 0.0
                    continue
                if s != side:
                    side = s
                    base = 0.0
                a = abs(f)
                if a - base >= BAND:
                    is_bet[t] = True
                    base = a
                else:
                    base = min(base, a)
            # once per grid cell
            for start in range(0, n, H):
                for t in range(start, min(start + H, n)):
                    if is_bet[t]:
                        if t + H < n and c[t] > 0 and np.isfinite(c[t + H]):
                            r = c[t + H] / c[t] - 1.0
                            sgn = 1.0 if fc[t] > 0 else -1.0
                            unusual.append((r - drift) * sgn)
                            fcs.append(float(fc[t]))
                        break

    unusual = np.array(unusual, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n_cases = int(len(unusual))

    mean = float(np.mean(unusual)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None
    rho = None
    if n_cases > 2 and np.std(fcs) > 0 and np.std(unusual) > 0:
        rho = float(stats.spearmanr(fcs, unusual).correlation)
        if not np.isfinite(rho):
            rho = None
    sup_pass = None if rho is None else bool(rho > 0)

    result = {
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman(forecast, unusual move) > 0", "value": rho, "passed": sup_pass},
        "counts": {"cases": n_cases},
        "reading": reading,
    }

    if n_cases < 30:
        result["status"] = "not observable"
        result["decided_by"] = "Fewer than the plan's minimum of 30 cases in total."
        return result

    if tval is not None and mean > 0 and tval >= 2:
        if sup_pass:
            result["status"] = "confirmed"
            result["decided_by"] = "Mean unusual move positive with t >= 2 over at least 30 cases, and the Spearman rank correlation is above 0."
        else:
            result["status"] = "inconclusive"
            result["decided_by"] = "A confirming t with a rank correlation of 0 or below is inconclusive."
    elif tval is not None and mean < 0 and tval <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t of the mean unusual move lies between -2 and 2."
    return result
