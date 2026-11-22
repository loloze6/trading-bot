import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.streak_loss.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: a down-streak in progress (positive streak loss); expected side: long
            sit = raw.notna() & (raw > 0)
            agree = active & sit & (f > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "t of mean unusual 18-bar move after long bets",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 over at least 30 cases to confirm; t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars of an ongoing down-streak "
                           "(positive streak loss) with a long forecast, as the plan's Fidelity requires."),
            "reading": "Situation taken as a positive raw streak-loss value, side long (forecast > 0).",
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift: mean 18-bar return on the non-overlapping grid of all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for s in range(0, len(c) - H, H):
                a, b = c[s], c[s + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(f)
            # bets: rise of the long forecast of at least BAND from its lowest level since the last bet
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    low = 0.0
                    continue
                if fi - low >= BAND:
                    bet[i] = True
                    low = fi
                else:
                    low = min(low, fi)
            # one case per 18-bar grid cell: the first bet in the cell
            for s in range(0, n, H):
                idx = np.where(bet[s:s + H])[0]
                if len(idx) == 0:
                    continue
                t = s + int(idx[0])
                if t + H >= n:
                    continue
                a, b = c[t], c[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                case_moves.append(b / a - 1.0 - drift)
                case_fc.append(f[t])

    moves = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(moves, ddof=1))
        t_val = float(mean_move / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_above = n_below = 0
    if n_cases > 0:
        med = float(np.median(fcs))
        above = moves[fcs > med]
        below = moves[fcs < med]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above > 0 and n_below > 0:
            sup_val = float(np.mean(above) - np.mean(below))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed (zero dispersion)."
    elif mean_move > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the above-minus-below-median difference is above 0."
    elif mean_move < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Positive t >= 2 but the supporting check fails (above-median minus below-median mean unusual move not above 0)."
    else:
        status = "inconclusive"
        decided = "t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 18-bar move after long bets (return minus coin's normal 18-bar drift)",
            "value": mean_move,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": "confirm: positive with t >= 2 over at least 30 cases; reject: negative with t <= -2 over at least 30 cases",
        },
        "supporting_check": {
            "name": "mean unusual move above median forecast minus below median",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "cases_above_median": n_above, "cases_below_median": n_below},
        "decided_by": decided,
        "reading": ("A case is the first bet (long forecast rise >= 2 from its low since the last bet) in each 18-bar grid cell "
                    "counted from each window's first row, cases whose 18-bar return leaves the window are dropped, "
                    "and cases exactly at the median forecast belong to neither half."),
    }
