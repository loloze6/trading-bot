import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    LHV = "debug_info.components.bounce.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0 or "forecast" not in df:
                continue
            close = df["close"].astype(float)
            f = df["forecast"].astype(float)
            # 90-bar return from prices where the window holds 90 bars of history,
            # else the detector's decision (its only rule is r90 < 0)
            r90 = close / close.shift(90) - 1.0
            reg_mr = (df["regime"].astype(str) == "mean_reversion") if "regime" in df else pd.Series(False, index=df.index)
            falling = pd.Series(np.where(r90.notna(), r90 < 0, reg_mr), index=df.index).astype(bool)
            # one-day rise: raw vol-scaled return > 0, else the day's price return > 0
            if LHV in df:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            dayret = close / close.shift(1) - 1.0
            rise = pd.Series(np.where(raw.notna(), raw > 0, dayret > 0), index=df.index).astype(bool)
            active = f.notna() & (f != 0)
            ok = active & falling & rise & (f < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 1.0
    passed = agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean short-direction unusual 5-bar move of the short cases",
                             "value": None, "statistic": None,
                             "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": n_active},
            "decided_by": (f"Only {agreement:.1%} of the active bars are short forecasts on bars with a negative "
                           f"90-day return and a one-day rise, below the 90 % the plan's situation requires."),
            "reading": "The 90-day return is recomputed from the window's closes where 90 bars of history exist and taken from the regime column elsewhere; a rise is a positive raw bounce value (or a positive day's return where it is not recorded).",
        }

    # ---------- 2. drift per coin: mean non-overlapping 5-bar return over all windows ----------
    drift = {}
    for coin in bars:
        rets = []
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases: short bets of >= 2 points, once per 5-bar grid cell ----------
    moves = []
    absf = []
    for coin in sorted(bars):
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            ref = 0.0
            seen_cells = set()
            for i in range(len(f)):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    ref = 0.0
                    continue
                m = -fi
                if m - ref >= BAND:
                    ref = m
                    cell = i // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if i + H < len(c) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 \
                            and np.isfinite(drift[coin]):
                        r = c[i + H] / c[i] - 1.0
                        moves.append(-(r - drift[coin]))
                        absf.append(abs(fi))
                else:
                    ref = min(ref, m)

    moves = np.array(moves, dtype=float)
    absf = np.array(absf, dtype=float)
    n = int(len(moves))

    mean_move = float(moves.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = moves.std(ddof=1)
        t = float(mean_move / (sd / np.sqrt(n))) if sd > 0 else None

    diff = None
    n_large = n_small = 0
    if n > 1:
        med = np.median(absf)
        large = moves[absf > med]
        small = moves[absf <= med]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            diff = float(large.mean() - small.mean())
    sup_passed = (diff > 0) if diff is not None else None

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases across all coins and windows, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (no spread), so neither rule is met."
    elif t >= 2 and mean_move > 0:
        if sup_passed:
            status = "confirmed"
            decided = "The mean short-direction unusual move is positive with t >= 2 and the larger-forecast half shows a larger unusual move than the smaller half."
        else:
            status = "inconclusive"
            decided = "A confirming t >= 2 whose larger-forecast half does not exceed its smaller half is inconclusive."
    elif t <= -2 and mean_move < 0:
        status = "rejected"
        decided = "The mean short-direction unusual move is negative with t <= -2: the coins rose more than their drift after these bounces."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-direction unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean short-direction unusual 5-bar move of the short cases",
            "value": mean_move,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects; between is inconclusive",
        },
        "supporting_check": {
            "name": "larger-|forecast| half minus smaller half, mean unusual move",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {"cases": n, "larger half": n_large, "smaller half": n_small},
        "decided_by": decided,
        "reading": ("A case is the first short bet (a fall of the forecast of at least 2 points from its lowest short "
                    "level since the last bet, from 0 after a flat) in each 5-bar cell counted from each window's first "
                    "row, cases without 5 bars left in the window are dropped, the drift is the coin's mean "
                    "non-overlapping 5-bar return over all its windows, the larger half is |forecast| above the median "
                    "(ties at the median go to the smaller half), and fewer than 30 cases is reported as not observable."),
    }
