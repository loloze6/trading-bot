import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MAX_BARS = 180

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): the coin is in a down-streak (consecutive closes below the previous close,
    # at least 2 bars, inside the window) whose volume is fading (least-squares slope of volume
    # over the streak's bars below 0, i.e. fade > 0). Expected side: long (forecast > 0).
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            vol = df["volume"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            n = len(df)
            streak = np.zeros(n, dtype=int)
            for i in range(1, n):
                if np.isfinite(close[i]) and np.isfinite(close[i - 1]) and close[i] < close[i - 1]:
                    streak[i] = min(streak[i - 1] + 1, MAX_BARS)
                else:
                    streak[i] = 0
            for i in range(n):
                if fc[i] == 0:
                    continue
                active_total += 1
                k = streak[i]
                in_sit = False
                if k >= 2:
                    v = vol[i - k + 1:i + 1]
                    if np.all(np.isfinite(v)):
                        x = np.arange(k, dtype=float)
                        slope = np.polyfit(x, v, 1)[0]
                        in_sit = slope < 0
                if in_sit and fc[i] > 0:
                    active_ok += 1
    agreement = float(active_ok / active_total) if active_total > 0 else 0.0
    passed = active_total > 0 and agreement >= 0.9

    main_name = "mean 18-bar unusual move of long bets (return minus coin's normal 18-bar drift)"
    threshold = "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject)"
    reading = ("Down-streak = consecutive bars with close below the previous close within the window, volume fade = "
               "least-squares volume slope over the streak's down bars below 0; a bet is a rise of a positive forecast "
               "of at least 2 from its lowest level since the last bet (from 0 after flat), the first bet in each "
               "18-bar grid cell from the window's first row is the case, cases without 18 bars left in the window are "
               "dropped, and the supporting check compares cases strictly above vs strictly below the median signal-bar forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside a down-streak "
                           "of at least 2 bars with fading volume, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # coin's normal drift: mean of non-overlapping 18-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            n = len(df)
            floor = 0.0
            prev = 0.0
            bet_bars = []
            for i in range(n):
                f = fc[i]
                if f > 0:
                    if prev <= 0:
                        floor = 0.0
                    if f - floor >= BAND:
                        bet_bars.append(i)
                        floor = f
                    else:
                        floor = min(floor, f)
                else:
                    floor = 0.0
                prev = f
            seen = set()
            for i in bet_bars:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                case_moves.append(r - drift)
                case_fc.append(fc[i])

    moves = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    ncases = int(len(moves))

    mean = float(np.mean(moves)) if ncases > 0 else None
    tval = None
    if ncases > 1:
        sd = np.std(moves, ddof=1)
        tval = float(mean / (sd / np.sqrt(ncases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if ncases > 0:
        med = np.median(fcs)
        above = moves[fcs > med]
        below = moves[fcs < med]
        if len(above) > 0 and len(below) > 0:
            sup_val = float(np.mean(above) - np.mean(below))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if ncases < 30:
        status = "not observable"
        decided = f"Fewer than the plan's minimum of 30 cases ({ncases})."
    elif tval is not None and mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 over at least 30 cases, and the supporting check passes."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 30 cases."
    elif tval is not None and mean > 0 and tval >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "A confirming t whose supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual move above-median forecast minus below-median forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": ncases, "active bars": int(active_total)},
        "decided_by": decided,
        "reading": reading,
    }
