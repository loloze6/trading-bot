import numpy as np
import pandas as pd


def measure(bars):
    H = 42
    BAND = 2.0
    FC = "forecast"
    RAW = "debug_info.components.streak_vol_rise.last_history_value"

    def down_streak_vol_slope(close, volume, max_bars=180):
        n = len(close)
        down = np.zeros(n, dtype=bool)
        down[1:] = close[1:] < close[:-1]
        slope = np.full(n, np.nan)
        length = np.zeros(n, dtype=int)
        run = 0
        for i in range(n):
            run = run + 1 if down[i] else 0
            length[i] = run
            if run >= 2:
                L = min(run, max_bars)
                v = volume[i - L + 1:i + 1].astype(float)
                if np.any(~np.isfinite(v)):
                    continue
                x = np.arange(L, dtype=float)
                xm = x - x.mean()
                mv = v.mean()
                if mv > 0:
                    slope[i] = float(np.sum(xm * (v - v.mean())) / np.sum(xm * xm)) / mv
        return length, slope

    # ---------- 1. situation check ----------
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].to_numpy(dtype=float)
            vol = df["volume"].to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            length, slope = down_streak_vol_slope(close, vol)
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                active_total += 1
                sit = (regime[i] == "trending") and length[i] >= 2 and np.isfinite(slope[i]) and slope[i] > 0
                if sit and f > 0:
                    active_ok += 1
    agreement = (active_ok / active_total) if active_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean 42-bar unusual move (return minus coin's normal 42-bar drift) over bets"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation computed from prices: regime 'trending' (the detector's recorded decision for 180-bar return > 0), "
               "bar t closed below the prior close, a down-close streak of at least 2 bars inside the window, and a positive "
               "least-squares slope of volume over that streak, with a long (positive) forecast; a case is the first bet "
               "(forecast rise >= 2 points from its lowest long level since the last bet, from 0 after flat) in each 42-bar "
               "grid cell counted from each window's first row, cases whose 42-bar return leaves the window are dropped, "
               "and the drift is the coin's mean 42-bar return on the same grid over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "independent cases": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars in the trending regime on a "
                           "down-close streak of 2+ bars with rising volume, as the plan's Fidelity describes."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift: mean 42-bar return on non-overlapping grid, all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].to_numpy(dtype=float)
            for p in range(0, len(close) - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            ref = 0.0
            bets = []
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bets.append(i)
                    ref = f
                else:
                    ref = min(ref, f)
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                case_moves.append((b / a - 1.0) - drift)
                case_fc.append(fc[i])

    moves = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    ncase = int(len(moves))

    mean_move = float(np.mean(moves)) if ncase > 0 else None
    tval = None
    if ncase >= 2:
        sd = float(np.std(moves, ddof=1))
        if sd > 0:
            tval = float(mean_move / (sd / np.sqrt(ncase)))

    supp_val = None
    if ncase > 0:
        med = float(np.median(fcs))
        hi = moves[fcs > med]
        lo = moves[fcs <= med]
        if len(hi) > 0 and len(lo) > 0:
            supp_val = float(np.mean(hi) - np.mean(lo))
    supp_passed = None if supp_val is None else bool(supp_val > 0)

    if ncase < 30:
        status = "not observable"
        decided = f"Fewer than 30 independent cases over all coins and windows ({ncase})."
    elif tval is not None and mean_move > 0 and tval >= 2 and supp_passed:
        status = "confirmed"
        decided = "The main measure is positive with t >= 2 and the supporting check is above 0."
    elif tval is not None and mean_move < 0 and tval <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check is at or below 0 (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_move,
            "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual move of cases with forecast above median minus at or below",
            "value": supp_val,
            "passed": supp_passed,
        },
        "counts": {"independent cases": ncase, "active bars": int(active_total)},
        "decided_by": decided,
        "reading": reading,
    }
