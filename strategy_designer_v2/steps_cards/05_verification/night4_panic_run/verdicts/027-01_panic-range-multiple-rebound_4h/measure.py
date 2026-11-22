import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 84
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.panic.last_history_value"

    # ---------- 1. situation check: active bars must be 24h-fall bars, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for t in range(n):
                if not np.isfinite(f[t]) or f[t] == 0:
                    continue
                n_active += 1
                if t >= 6 and np.isfinite(close[t]) and np.isfinite(close[t - 6]):
                    fall = close[t] < close[t - 6]
                else:
                    # no 24h price history inside the window: the component is 0 when there is no fall
                    fall = bool(np.isfinite(raw[t]) and raw[t] != 0)
                if fall and f[t] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean unusual 84-bar move of long cases (return minus coin's normal drift)"
    main_thr = "confirm: mean > 0 with t >= 2 and upper-minus-lower gradient > 0; reject: mean < 0 with t <= -2"
    sup_name = "upper-minus-lower half (median forecast at entry) mean unusual move, Welch t"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are 24h-fall bars with a long "
                           "forecast, so the config does not trade the plan's situation on its long side"),
            "reading": "a 24h fall is close below the close 6 bars earlier in the same window (the raw component "
                       "being non-zero on the first 6 bars of a window); the expected side is long.",
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    case_order = []
    order = 0
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 84-bar grid returns over all windows of the coin
        grid_rets = []
        prepared = {}
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            prepared[w] = df
            for s in range(0, len(close) - H, H):
                if np.isfinite(close[s]) and np.isfinite(close[s + H]) and close[s] > 0:
                    grid_rets.append(close[s + H] / close[s] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in prepared.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # bets: a rise of the forecast on the long side of at least the band,
            # from its lowest level since the last bet (from 0 after a flat)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for t in range(n):
                if f[t] <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, f[t])
                if f[t] - ref >= BAND:
                    bet[t] = True
                    ref = f[t]
            # once per grid cell: the first bet of each cell
            for s in range(0, n, H):
                idx = np.where(bet[s:min(s + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = s + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1.0
                case_moves.append(r - drift)
                case_fc.append(f[t])
                case_order.append(order)
                order += 1

    moves = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    tstat = None
    if n_cases >= 2:
        sd = float(np.std(moves, ddof=1))
        tstat = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    # gradient: sort by forecast at entry (ties by order of cases), lower half vs upper half
    diff = None
    welch = None
    n_up = n_lo = 0
    if n_cases >= 2:
        idx = np.lexsort((np.array(case_order), fcs))
        half = n_cases // 2
        lo = moves[idx[:half]]
        up = moves[idx[n_cases - half:]]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            diff = float(np.mean(up) - np.mean(lo))
            if n_up >= 2 and n_lo >= 2:
                res = stats.ttest_ind(up, lo, equal_var=False)
                welch = float(res.statistic) if np.isfinite(res.statistic) else None
    sup_passed = (diff is not None and diff > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"fewer than {MIN_CASES} cases over all coins and windows ({n_cases}), the plan's minimum count"
    elif tstat is None:
        status = "inconclusive"
        decided = "the t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met"
    elif mean > 0 and tstat >= 2 and sup_passed:
        status = "confirmed"
        decided = "the mean unusual move is positive with t >= 2 and the upper-minus-lower difference is above 0"
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "the mean unusual move is negative with t <= -2"
    elif mean > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the gradient (upper minus lower) is at or below 0, which the plan calls inconclusive"
    else:
        status = "inconclusive"
        decided = "the t of the mean unusual move is between -2 and 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": tstat} if tstat is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name + (f" (Welch t {welch:.3f})" if welch is not None else ""),
            "value": diff,
            "passed": sup_passed if diff is not None else None,
        },
        "counts": {
            "cases over all coins and windows": n_cases,
            "upper half cases": n_up,
            "lower half cases": n_lo,
        },
        "decided_by": decided,
        "reading": ("a case is the first long bet (forecast rise >= 2 from its lowest positive level since the "
                    "last bet, from 0 after a flat) in each 84-bar grid cell from each window's first row, kept "
                    "only if its 84-bar return stays inside the window; the median split sorts cases by entry "
                    "forecast (ties in case order) into equal lower and upper halves, dropping the middle case "
                    "when odd; the plan's fewer-than-30-cases rule is reported as not observable."),
    }
