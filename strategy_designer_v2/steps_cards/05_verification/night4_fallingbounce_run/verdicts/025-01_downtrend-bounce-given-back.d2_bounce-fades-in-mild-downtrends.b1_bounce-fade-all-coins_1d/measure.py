import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    BC = "debug_info.components.bounce.last_history_value"
    FC = "debug_info.components.fall90.last_history_value"

    def wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return str(w)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=wkey):
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            day_ret = np.full(len(df), np.nan)
            if len(df) > 1:
                day_ret[1:] = close[1:] / close[:-1] - 1.0
            if FC in df.columns:
                f90 = pd.to_numeric(df[FC], errors="coerce").values
            else:
                f90 = np.full(len(df), np.nan)
            if BC in df.columns:
                bnc = pd.to_numeric(df[BC], errors="coerce").values
            else:
                bnc = np.full(len(df), np.nan)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            for i in range(len(df)):
                if fc[i] == 0 or not np.isfinite(fc[i]):
                    continue
                n_active += 1
                # regime: 90-day return below 0
                if np.isfinite(f90[i]):
                    in_regime = f90[i] < 0
                else:
                    in_regime = regime[i] == "mean_reversion"
                # a one-day rise (graded, any positive vol-scaled return)
                if np.isfinite(bnc[i]):
                    rise = bnc[i] > 0
                else:
                    rise = np.isfinite(day_ret[i]) and day_ret[i] > 0
                if in_regime and rise and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean short-direction unusual 5-day move over short-bet cases"
    main_thr = "mean > 0 with t >= 2 confirms (with slope t >= 2); t <= -2 rejects"
    sup_name = "slope t of unusual move on fall90 raw 90-day return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": "Fewer than 90% of the active (non-zero forecast) bars are short bets on an up day in a coin whose 90-day return is below 0, as the plan's Fidelity requires.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    moves = []
    f90_cases = []
    for coin in sorted(bars):
        wins = sorted(bars[coin], key=wkey)
        # normal drift: mean of non-overlapping 5-bar returns over all windows
        grid_rets = []
        dfs = {}
        for w in wins:
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            dfs[w] = df
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w in wins:
            df = dfs[w]
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            f90 = pd.to_numeric(df[FC], errors="coerce").values if FC in df.columns else np.full(len(df), np.nan)
            ref = 0.0  # lowest short magnitude since last bet
            used_cells = set()
            for i in range(len(df)):
                f = fc[i]
                if not (f < 0):
                    ref = 0.0
                    continue
                mag = -f
                bet = (mag - ref) >= BAND - 1e-12
                if bet:
                    ref = mag
                else:
                    ref = min(ref, mag)
                    continue
                cell = i // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                moves.append(-(r - drift))
                f90_cases.append(f90[i])

    moves = np.asarray(moves, dtype=float)
    f90_cases = np.asarray(f90_cases, dtype=float)
    n = int(len(moves))

    mean = float(np.mean(moves)) if n > 0 else None
    t_main = None
    if n > 1:
        sd = float(np.std(moves, ddof=1))
        t_main = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    ok = np.isfinite(f90_cases) & np.isfinite(moves)
    n_reg = int(ok.sum())
    slope = None
    t_slope = None
    if n_reg > 2 and np.std(f90_cases[ok]) > 0:
        lr = stats.linregress(f90_cases[ok], moves[ok])
        slope = float(lr.slope)
        if lr.stderr and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    counts = {"cases": n, "cases with fall90 recorded": n_reg}
    reading = ("A case is the first bar in each non-overlapping 5-bar grid cell of a window where the forecast falls at "
               "least 2 points below its least-negative level since the last short bet (from 0 after flat), its move is "
               "-(close[t+5]/close[t]-1 - the coin's mean grid 5-bar return over all windows), the slope's t is the OLS "
               "slope over its standard error on fall90's raw last_history_value, and the plan's 30-case minimum is "
               "reported as not observable.")

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases across all coins and windows, below the plan's minimum of 30."
        sup_passed = None if t_slope is None else bool(t_slope >= 2)
    else:
        sup_passed = None if t_slope is None else bool(t_slope >= 2)
        if (t_main is not None and t_main <= -2) or (t_slope is not None and t_slope <= -2):
            status = "rejected"
            decided = "Reject rule met: the main measure's t is <= -2 or the slope's t is <= -2."
        elif (mean is not None and mean > 0 and t_main is not None and t_main >= 2
              and t_slope is not None and t_slope >= 2):
            status = "confirmed"
            decided = "Confirm rule met: mean unusual short move positive with t >= 2 and slope t >= 2."
        else:
            status = "inconclusive"
            decided = "Neither rule met: the main t or the slope t lies between -2 and 2 (or the confirm's other part fails)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if t_main is None else {"name": "t of the mean", "value": t_main},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": t_slope, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
