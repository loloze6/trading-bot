import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    BAND = 2.0
    BRK_PERIOD = 12
    MIN_CASES = 100

    # ---------- 1. situation check: close above max high of prior 12 bars, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            prior_max = high.shift(1).rolling(BRK_PERIOD, min_periods=BRK_PERIOD).max()
            situ = close > prior_max
            known = prior_max.notna() & close.notna()
            active = (fc != 0) & known
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean 72-bar unusual move per case (return minus coin's normal drift)"
    main_thr = "t >= 2 over at least 100 independent cases to confirm; t <= -2 over at least 100 to reject"
    reading = ("Breakout recomputed per window as close > max high of the prior 12 recorded bars, the first 12 bars of "
               "each window (no full prior history) left out of the agreement; a case is the first bet (forecast rise "
               "of >= 2 points on its side from its lowest level since the last bet, from 0 after flat) in each "
               "72-bar grid cell from each window's first row, dropped if its 72-bar return leaves the window; normal "
               "drift is the mean of the coin's non-overlapping 72-bar returns over all its windows; the slope check "
               "is the OLS slope t of unusual move on the case's forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"independent cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the close is above the "
                           "highest high of the prior 12 bars, so the config does not trade the plan's breakout situation "
                           "on the long side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 72-bar returns over all windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(d)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            prepared.append((close, fc))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc in prepared:
            n = len(close)
            # bets
            bets = []  # (index, side, forecast)
            ref = 0.0
            side = 0
            for t in range(n):
                f = fc[t]
                s = 1 if f > 0 else (-1 if f < 0 else 0)
                if s == 0:
                    side = 0
                    ref = 0.0
                    continue
                if s != side:
                    side = s
                    ref = 0.0
                mag = abs(f)
                if mag - ref >= BAND:
                    bets.append((t, s, f))
                    ref = mag
                else:
                    ref = min(ref, mag)
            # one per grid cell: the first bet in each cell
            seen = set()
            for t, s, f in bets:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                case_moves.append(s * (r - drift))
                case_fc.append(f)

    x = np.asarray(case_fc, dtype=float)
    y = np.asarray(case_moves, dtype=float)
    n_cases = int(len(y))

    mean_move = float(np.mean(y)) if n_cases > 0 else None
    t_mean = None
    if n_cases > 1:
        sd = float(np.std(y, ddof=1))
        t_mean = float(mean_move / (sd / np.sqrt(n_cases))) if sd > 0 else None

    slope_t = None
    if n_cases > 2 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        if lr.stderr is not None and lr.stderr > 0:
            slope_t = float(lr.slope / lr.stderr)
    slope_pass = (slope_t >= 1.0) if slope_t is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, below the plan's minimum of 100."
    elif t_mean is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif t_mean >= 2.0 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move has t >= 2 over at least 100 independent cases and the slope on the forecast has t >= 1."
    elif t_mean >= 2.0:
        status = "inconclusive"
        decided = "The mean unusual move has t >= 2 over at least 100 cases but the slope check (t >= 1) fails."
    elif t_mean <= -2.0:
        status = "rejected"
        decided = "The mean unusual move has t <= -2 over at least 100 independent cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 over at least 100 independent cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_move,
            "statistic": ({"name": "t of the mean", "value": t_mean} if t_mean is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "t of OLS slope of unusual move on forecast (>= 1)",
            "value": slope_t,
            "passed": slope_pass,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
