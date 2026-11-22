import numpy as np
import pandas as pd


def measure(bars):
    H = 78
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.panic.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the lagged 24h stretch fell (raw graded panic product > 0). Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            active = np.isfinite(f) & (f != 0)
            situ = np.isfinite(raw) & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the "
                           "lagged 24h stretch fell (raw panic product > 0), so the config does not trade "
                           "the plan's situation on its side."),
            "reading": "The situation is read as the component's raw value being positive (a falling stretch), the side as long.",
        }

    # ---------- 2. Criterion ----------
    unusual = []
    sig_fc = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 78-bar returns over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for i in range(0, n - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
            prepared.append((c, f))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for c, f in prepared:
            n = len(c)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft <= 0:
                    ref = 0.0
                    continue
                is_bet = (ft - ref) >= BAND
                if is_bet:
                    ref = ft
                else:
                    ref = min(ref, ft)
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                unusual.append(r - drift)
                sig_fc.append(ft)

    unusual = np.asarray(unusual, dtype=float)
    sig_fc = np.asarray(sig_fc, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    sup_pass = None
    n_up = n_lo = 0
    if n_cases > 0:
        med = float(np.median(sig_fc))
        up = unusual[sig_fc > med]
        lo = unusual[sig_fc <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            diff = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(diff > 0)
        else:
            sup_pass = False

    reading = ("A case is the first long bet (forecast rise of >= 2 points from its lowest level since the last bet, "
               "from 0 after a flat) in each non-overlapping 78-bar cell from each window's first row, cases without "
               "a full 78-bar return inside the window are dropped, the drift is the coin's mean 78-bar return on that "
               "grid over all windows, and the median split puts forecasts above the median in the upper half and the "
               "rest in the lower half.")

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases across all coins and windows, fewer than the plan's minimum of 30."
    elif t_u is not None and mean_u > 0 and t_u >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the upper-minus-lower half difference is above 0."
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif t_u is not None and t_u >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "The mean unusual move has t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 78-bar unusual move (return minus coin's normal drift) over cases, before costs",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": "confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual move of upper half minus lower half (median forecast split) > 0",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided,
        "reading": reading,
    }
