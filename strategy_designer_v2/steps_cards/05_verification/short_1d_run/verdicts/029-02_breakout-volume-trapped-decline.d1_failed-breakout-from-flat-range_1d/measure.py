import numpy as np
import pandas as pd
from scipy import stats


RAW_COL = "debug_info.components.failed_bo.last_history_value"
H = 5
PERIOD = 20
FAIL_WIN = 3
BAND = 2.0
MIN_CASES = 30


def _breakout_info(close, t):
    """Most recent bar j in t-1..t-3 whose close is above the max of its prior 20 closes.
    Returns (computable, j, old_high). computable is False if the history needed is not in the window."""
    for k in range(1, FAIL_WIN + 1):
        j = t - k
        if j - PERIOD < 0:
            return False, None, None
        hi = np.max(close[j - PERIOD:j])
        if close[j] > hi:
            return True, j, hi
    return True, None, None


def _t_mean(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return float(np.mean(x)) if n else None, None
    sd = np.std(x, ddof=1)
    m = float(np.mean(x))
    if sd == 0:
        return m, None
    return m, float(m / (sd / np.sqrt(n)))


def measure(bars):
    active_total = 0
    active_agree = 0
    case_moves = []
    case_pre = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]

        # coin's normal 5-bar drift: non-overlapping grid over all windows
        drift_samples = []
        for w in sorted(wins.keys()):
            df = wins[w]
            c = df["close"].to_numpy(dtype=float)
            for p in range(0, len(c), H):
                if p + H < len(c) and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    drift_samples.append(c[p + H] / c[p] - 1.0)
        drift = float(np.mean(drift_samples)) if drift_samples else np.nan

        for w in sorted(wins.keys()):
            df = wins[w].reset_index(drop=True)
            c = df["close"].to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            raw = (pd.to_numeric(df[RAW_COL], errors="coerce").to_numpy(dtype=float)
                   if RAW_COL in df.columns else np.full(len(df), np.nan))
            n = len(df)

            # --- situation check ---
            for t in range(n):
                if f[t] == 0:
                    continue
                active_total += 1
                comp, j, hi = _breakout_info(c, t)
                if comp:
                    sit = (j is not None) and (c[t] < hi)
                else:
                    sit = bool(np.isfinite(raw[t]) and raw[t] > 0)
                if sit and f[t] < 0:
                    active_agree += 1

            # --- bets on the short side (holding-period definition) ---
            bets = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_side = 0
            for t in range(n):
                side = int(np.sign(f[t]))
                if side != prev_side:
                    ref = 0.0
                if side < 0:
                    mag = -f[t]
                    if mag - ref >= BAND:
                        bets[t] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    ref = 0.0
                prev_side = side

            # --- one case per 5-bar grid cell ---
            for p in range(0, n, H):
                idx = [t for t in range(p, min(p + H, n)) if bets[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] <= 0:
                    continue
                if not np.isfinite(drift):
                    continue
                ret = c[t + H] / c[t] - 1.0
                move = -(ret - drift)
                case_moves.append(move)
                comp, j, hi = _breakout_info(c, t)
                pre = np.nan
                if comp and j is not None and j - 21 >= 0 and c[j - 21] > 0:
                    pre = c[j - 1] / c[j - 21] - 1.0
                case_pre.append(pre)

    agreement = (active_agree / active_total) if active_total else 0.0
    passed = active_total > 0 and agreement >= 0.9
    reading = ("Cases are the first short-side bet (forecast rise of >= 2 points from its lowest short level since the "
               "last bet) in each 5-bar grid cell of each window, with a full 5-bar forward return inside the window; "
               "the breakout bar j is the most recent of the 1-3 prior bars closing above its prior 20 closes, cases "
               "without close[j-21] in the window are left out of the slope, and the situation on bars lacking 20+3 "
               "bars of window history is read from the recorded raw value being above 0.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars during a live failed "
                           "breakout (close 1-3 bars ago above its prior 20-close high, today's close back below it)."),
            "reading": reading,
        }

    moves = np.asarray(case_moves, dtype=float)
    n_cases = int(len(moves))
    mean_move, t_main = _t_mean(moves) if n_cases else (None, None)

    pre = np.asarray(case_pre, dtype=float)
    ok = np.isfinite(pre) & np.isfinite(moves) if n_cases else np.array([], dtype=bool)
    n_slope = int(ok.sum())
    slope, t_slope = None, None
    if n_slope >= 3 and np.std(pre[ok]) > 0:
        lr = stats.linregress(pre[ok], moves[ok])
        slope = float(lr.slope)
        if lr.stderr and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    sup_pass = None if t_slope is None else bool(t_slope <= -2)

    main = {
        "name": "mean short-direction 5-bar unusual move (return minus coin drift) over short bets, pooled",
        "value": mean_move,
        "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
        "threshold": "confirm t >= 2 on at least 30 independent cases; reject t <= -2",
    }
    sup = {
        "name": "t of LS slope of unusual move on pre-breakout 20-day return (slope %s)" %
                ("n/a" if slope is None else "%.6g" % slope),
        "value": t_slope,
        "passed": sup_pass,
    }
    counts = {"independent cases": n_cases, "cases with pre-breakout return": n_slope}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = "Fewer than 30 independent cases (%d), the plan's minimum count." % n_cases
    elif t_main is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed; every other result is inconclusive."
    elif t_main <= -2:
        status = "rejected"
        decided = "Main measure t <= -2: the coin rises more than its drift after failed breakouts."
    elif t_main > 0 and t_slope is not None and t_slope >= 2:
        status = "rejected"
        decided = "Main measure positive with slope t >= +2: the fall is larger after larger run-ups."
    elif t_main >= 2 and t_slope is not None and t_slope <= -2:
        status = "confirmed"
        decided = "Main measure t >= 2 on at least 30 independent cases and supporting slope t <= -2."
    else:
        status = "inconclusive"
        decided = ("Neither confirm nor reject is met (main t between -2 and 2, or a confirmed fall with slope t "
                   "between -2 and 2 or not computable): inconclusive.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
