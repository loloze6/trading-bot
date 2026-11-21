import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.support_cluster.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            sma = close.rolling(50, min_periods=50).mean()
            below = close < sma
            # bars without 50 in-window closes: use the detector's recorded decision
            no_sma = sma.isna()
            if "regime" in df.columns:
                below = below.where(~no_sma, df["regime"].astype(str) == "trending")
            else:
                below = below.where(~no_sma, False)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                cluster = raw > 0
            else:
                cluster = pd.Series(False, index=df.index)
            situ = below & cluster.fillna(False)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    reading = ("Situation = close below the SMA50 computed inside the window (the recorded regime "
               "'trending' where fewer than 50 in-window closes exist) and the raw support_cluster value > 0, "
               "expected side short; cases are grid cells (positions 0,10,20,... of each window with t+10 in "
               "the window) with forecast <= -2, pooled over all coins; drift is the coin's mean 10-bar return "
               "on the same grid over all its windows; supporting check splits by |forecast| > median vs <= median.")

    main_name = "t of mean short-direction unusual 10-bar move, cases forecast <= -2"
    thr = "confirm t >= 2 over >= 30 cases with supporting check > 0; reject t <= -2 over >= 30 cases"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 30 cases exist.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with the close below its 50-day "
                           "average and a cluster of swing lows above the close, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    moves = []
    absf = []
    for coin, wins in bars.items():
        grid = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid.append((c1 / c0 - 1.0, fc[p]))
        if not grid:
            continue
        rets = np.array([g[0] for g in grid])
        drift = float(np.mean(rets))
        for r, f in grid:
            if np.isfinite(f) and f <= -2:
                moves.append(-(r - drift))
                absf.append(abs(f))

    moves = np.array(moves, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(moves))

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(moves, ddof=1))
        if sd > 0:
            t = float(mean_move / (sd / np.sqrt(n_cases)))

    supp_val = None
    supp_pass = None
    n_hi = n_lo = 0
    if n_cases > 0:
        med = float(np.median(absf))
        hi = moves[absf > med]
        lo = moves[absf <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            supp_val = float(np.mean(hi) - np.mean(lo))
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases with forecast <= -2, fewer than the plan's minimum of 30."
    elif t is not None and t >= 2 and supp_pass:
        status = "confirmed"
        decided = "The main-measure t is 2 or more over at least 30 cases and the supporting check is above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "The main-measure t is -2 or less over at least 30 cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "The main-measure t is 2 or more but the supporting check is at or below 0."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_move,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean move |forecast| above median minus at or below median",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {"cases": n_cases, "cases_above_median": n_hi, "cases_at_or_below_median": n_lo,
                   "active_bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
