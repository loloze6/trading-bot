import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    BAND = 2.0
    MIN_CASES = 30
    RB = "debug_info.components.break.last_history_value"
    MA = "debug_info.components.above_ma.last_history_value"

    def _sorted(df):
        d = df.copy()
        if "timestamp" in d.columns:
            d = d.sort_values("timestamp", kind="mergesort")
        return d.reset_index(drop=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = _sorted(df)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if not active.any():
                continue
            rb = pd.to_numeric(d[RB], errors="coerce") if RB in d.columns else pd.Series(np.nan, index=d.index)
            ma = pd.to_numeric(d[MA], errors="coerce") if MA in d.columns else pd.Series(np.nan, index=d.index)
            situation = (rb > 0) & (ma > 0)  # NaN compares False
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "mean 20-bar unusual move of the cases",
                "value": None,
                "statistic": None,
                "threshold": "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject)",
            },
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": (f"Only {agreement:.1%} of the bars with a non-zero forecast are long bars where the close "
                           "crossed a 90-day swing-high level (rb > 0) with the close above its SMA50 (ma > 0), "
                           "below the 90 % required."),
            "reading": "The situation is read from the recorded raw values of the break (rb > 0) and above_ma (ma > 0) components on the active bars, with long as the expected side.",
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 20-bar returns over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            d = _sorted(df)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for p in range(0, n, H):
                if p + H < n and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for d in prepared:
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(c)
            # bets: a rise of the forecast on its side of at least the band,
            # measured from its lowest level on that side since the last bet
            side = 0
            low = 0.0
            bets = []
            for t in range(n):
                ft = f[t]
                s = int(np.sign(ft))
                if s == 0:
                    side, low = 0, 0.0
                    continue
                if s != side:
                    side, low = s, 0.0
                a = abs(ft)
                low = min(low, a)
                if a - low >= BAND:
                    bets.append((t, s))
                    low = a
            # once per 20-bar grid cell: the first bet in each cell
            seen = set()
            for t, s in bets:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                    r = c[t + H] / c[t] - 1.0
                    case_moves.append(s * (r - drift))
                    case_fc.append(float(f[t]))

    moves = np.asarray(case_moves, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        if sd > 0:
            tstat = float(mean / (sd / np.sqrt(n_cases)))

    # supporting check: rank split at the median entry forecast
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        order = np.argsort(fcs, kind="mergesort")
        half = n_cases // 2
        lower = moves[order[:half]]
        upper = moves[order[n_cases - half:]]
        if len(lower) > 0 and len(upper) > 0:
            sup_val = float(np.mean(upper) - np.mean(lower))
            sup_pass = bool(sup_val > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif mean is not None and tstat is not None and mean > 0 and tstat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is > 0 with t >= 2 over at least 30 cases, and the upper half's mean exceeds the lower half's."
    elif mean is not None and tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean unusual move is < 0 with t <= -2 over at least 30 cases."
    elif mean is not None and tstat is not None and mean > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "A t >= 2 whose supporting check fails (upper minus lower half not > 0) is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 30 cases, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "mean 20-bar unusual move of the cases (return minus coin's normal 20-bar drift), before costs",
            "value": mean,
            "statistic": None if tstat is None else {"name": "one-group t", "value": tstat},
            "threshold": "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject)",
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean unusual move, split at median entry forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": ("The situation is read from the recorded raw rb and ma values (both > 0, long side); a case is the first "
                    "bet (forecast rise of >= 2 points from its lowest level on its side since the last bet, from 0 after a "
                    "flat or side change) in each 20-bar grid cell counted from each window's first row, dropped if its "
                    "20-bar return leaves the window; the median split ranks cases by entry forecast and takes the lower "
                    "and upper floor(n/2), leaving out the middle case when n is odd."),
    }
