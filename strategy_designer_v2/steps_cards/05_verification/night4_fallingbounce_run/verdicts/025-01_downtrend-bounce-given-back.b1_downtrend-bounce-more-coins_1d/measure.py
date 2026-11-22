import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.bounce.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # 90-day fall: recomputed from prices inside the window where possible, else the detector's regime
            ret90 = close / close.shift(90) - 1.0
            regime_fall = df["regime"].astype(str) == "mean_reversion"
            fall = np.where(ret90.notna(), ret90 < 0, regime_fall)
            # one-day rise: the raw vol-scaled 1-day return, else the price return
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            r1 = close / close.shift(1) - 1.0
            rise_val = raw.where(raw.notna(), r1)
            rise = (rise_val > 0).fillna(False).to_numpy()
            active = (fc != 0).to_numpy()
            situ = np.asarray(fall, dtype=bool) & rise & (fc < 0).to_numpy()
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The 90-day fall is recomputed as close[t]/close[t-90]-1 inside the window where 90 prior bars exist "
               "and taken from regime == 'mean_reversion' elsewhere, the rise is the bounce component's raw value > 0; "
               "a short bet is a fall of the forecast of at least 2 points from its least-short level on the short side "
               "since the last bet (from 0 after flat or long), the case of a grid cell is its first bet with a full "
               "5-bar return inside the window, and the forecast's size is its absolute value.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars on a one-day rise in a coin "
                           "with a negative 90-day return, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    moves = []
    sizes = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            n = len(df)
            ref = 0.0
            used_cells = set()
            for t in range(n):
                if f[t] >= 0:
                    ref = 0.0
                    continue
                mag = -f[t]
                is_bet = (mag - ref) >= BAND - 1e-12
                if is_bet:
                    ref = mag
                else:
                    ref = min(ref, mag)
                    continue
                cell = t // H
                if cell in used_cells:
                    continue
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                used_cells.add(cell)
                ret = c[t + H] / c[t] - 1.0
                moves.append(-(ret - drift))
                sizes.append(abs(f[t]))

    n_cases = len(moves)
    moves = np.array(moves, dtype=float)
    sizes = np.array(sizes, dtype=float)

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(moves, ddof=1))
        if sd > 0:
            t_stat = float(mean_move / (sd / np.sqrt(n_cases)))
    corr = None
    if n_cases >= 3 and np.std(sizes) > 0 and np.std(moves) > 0:
        corr = float(stats.pearsonr(sizes, moves)[0])

    main = {
        "name": "mean unusual 5-bar move in the short direction after short bets",
        "value": mean_move,
        "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2",
    }
    supp = {
        "name": "Pearson correlation of forecast size with the unusual short move",
        "value": corr,
        "passed": (corr > 0) if corr is not None else None,
    }
    counts = {"cases over all coins and windows": n_cases}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 cases over all coins and windows, the plan's minimum."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no spread in the moves), so neither rule is met."
    elif mean_move > 0 and t_stat >= 2:
        if corr is not None and corr > 0:
            status = "confirmed"
            decided = "The mean unusual short move is positive with t >= 2 and the correlation is above 0."
        else:
            status = "inconclusive"
            decided = "The mean unusual short move is positive with t >= 2 but the correlation is 0 or below."
    elif mean_move < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual short move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
