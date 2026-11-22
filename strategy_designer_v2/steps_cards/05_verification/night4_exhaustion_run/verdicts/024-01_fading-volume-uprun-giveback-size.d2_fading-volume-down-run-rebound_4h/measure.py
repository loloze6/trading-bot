import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MAX_BARS = 180

    def down_streak_fade(close, volume):
        # Situation from prices: bar t closed down, inside an unbroken down streak
        # (capped at MAX_BARS bars), with volume declining across the streak's bars
        # (least-squares slope of volume over the down bars < 0; needs >= 2 bars).
        n = len(close)
        sit = np.zeros(n, dtype=bool)
        streak = 0
        for t in range(n):
            if t > 0 and np.isfinite(close[t]) and np.isfinite(close[t - 1]) and close[t] < close[t - 1]:
                streak += 1
            else:
                streak = 0
            L = min(streak, MAX_BARS)
            if L >= 2:
                v = volume[t - L + 1:t + 1]
                if np.all(np.isfinite(v)):
                    x = np.arange(L, dtype=float)
                    xm = x - x.mean()
                    slope = float(np.sum(xm * (v - v.mean())) / np.sum(xm * xm))
                    sit[t] = slope < 0
        return sit

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            vol = df["volume"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            sit = down_streak_fade(close, vol)
            col = "debug_info.components.streak_loss.last_history_value"
            if col in df.columns:
                raw = df[col].astype(float).values
                # where the raw streak loss is recorded it must show a loss (> 0)
                raw_ok = np.where(np.isfinite(raw), raw > 0, True)
            else:
                raw_ok = np.ones(len(df), dtype=bool)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & sit & raw_ok & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "confirm: mean > 0 with t >= 2 and size check difference > 0; reject: mean < 0 with t <= -2; fewer than 30 cases: not observable"
    reading = ("The situation is rebuilt as bar t closing below bar t-1 inside an unbroken down streak (capped at 180 bars) "
               "whose down bars' volumes have a negative least-squares slope (at least 2 bars), with the recorded raw streak loss > 0 where present; "
               "a case is the first bet (long forecast rise of >= 2 points from its lowest level since the last bet, from 0 after flat) in each 18-bar grid cell of a window, "
               "the drift is the coin's mean 18-bar return on the grid of all its windows, and cases at exactly the median forecast are left out of the size check.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 18-bar move per case", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": None},
            "decided_by": ("Fewer than 90% of the active forecast bars are long bars of a running down streak with fading volume "
                           "(agreement %.3f), so the config does not do what the plan's Fidelity says." % agreement),
            "reading": reading,
        }

    # ---------- criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        grid_rets = []
        per_window = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # bets
            low = 0.0
            bets = np.zeros(n, dtype=bool)
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bets[t] = True
                    low = f
                else:
                    low = min(low, f)
            seen = set()
            for t in np.where(bets)[0]:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H < n:
                    r = close[t + H] / close[t] - 1.0
                    if np.isfinite(r):
                        per_window.append((r, fc[t]))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, f in per_window:
            case_moves.append(r - drift)
            case_fc.append(f)

    moves = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean = float(moves.mean()) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(moves.std(ddof=1))
        t_stat = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    n_above = n_below = 0
    t_diff = None
    if n_cases > 0:
        med = float(np.median(fcs))
        above = moves[fcs > med]
        below = moves[fcs < med]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above > 0 and n_below > 0:
            diff = float(above.mean() - below.mean())
            if n_above >= 2 and n_below >= 2:
                tt = stats.ttest_ind(above, below, equal_var=False)
                t_diff = float(tt.statistic) if np.isfinite(tt.statistic) else None
    check_passed = (diff > 0) if diff is not None else None

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 cases in total (%d), the plan's minimum count, so the data could not show the idea." % n_cases
    elif mean is not None and t_stat is not None and mean > 0 and t_stat >= 2 and check_passed is True:
        status = "confirmed"
        decided = "The mean unusual move is > 0 with t >= 2 and the above-minus-below-median difference is > 0 (confirm rule)."
    elif mean is not None and t_stat is not None and mean < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is < 0 with t <= -2 (reject rule)."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the size check (above minus below median > 0) does not pass (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or cannot be computed), so neither the confirm nor the reject rule is met (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean unusual 18-bar move per case (return minus coin's normal 18-bar drift)",
                         "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
                         "threshold": threshold_txt},
        "supporting_check": {"name": "mean unusual move above minus below median case forecast",
                             "value": diff, "passed": check_passed},
        "counts": {"cases": n_cases, "cases above median": n_above, "cases below median": n_below,
                   "active bars": n_active},
        "decided_by": decided,
        "reading": reading,
    }
