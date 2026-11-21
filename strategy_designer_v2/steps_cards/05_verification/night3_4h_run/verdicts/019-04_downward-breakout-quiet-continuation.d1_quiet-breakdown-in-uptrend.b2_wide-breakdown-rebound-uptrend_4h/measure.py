import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18          # horizon in bars
    BAND = 2.0      # bet band in forecast points
    BRK_P = 12      # prior-low lookback
    MOM_P = 180     # momentum lookback
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            prior_low = low.shift(1).rolling(BRK_P, min_periods=BRK_P).min()
            mom = close / close.shift(MOM_P) - 1.0
            determinable = prior_low.notna() & mom.notna() & close.notna()
            situ = (close < prior_low) & (mom > 0)
            active = fc.notna() & (fc != 0) & determinable
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("The situation is recomputed from prices as close below the minimum low of the 12 prior bars and "
               "close/close 180 bars earlier minus 1 above 0, inside each window, leaving out active bars without "
               "180 bars of in-window history; a case is the first long bet (forecast rise of at least 2 points from "
               "its lowest level since the last bet, from 0 after a flat) in each 18-bar grid cell of each window, "
               "with cases pooled over all coins and each coin's drift the mean of its non-overlapping 18-bar grid "
               "returns over all its windows; fewer than 30 cases is reported as not observable.")

    main_name = "mean 18-bar excess return over coin drift of long bets"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars where the close is below the prior 12-bar low "
                           "with a positive 180-bar return and a long forecast, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess_all = []
    fc_all = []
    for coin, wins in bars.items():
        # coin's normal drift: mean of non-overlapping 18-bar grid returns over all windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append((close, fc))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc in prepared:
            n = len(close)
            # bet detection on the long side
            bets = np.zeros(n, dtype=bool)
            base = 0.0
            prev = 0.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f):
                    f = 0.0
                if f > 0:
                    if prev <= 0:
                        base = 0.0
                    if f - base >= BAND:
                        bets[i] = True
                        base = f
                    else:
                        base = min(base, f)
                else:
                    base = 0.0
                prev = f
            # one case per grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bets[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r) or not np.isfinite(fc[t]):
                    continue
                excess_all.append(r - drift)
                fc_all.append(fc[t])

    ex = np.asarray(excess_all, dtype=float)
    fa = np.asarray(fc_all, dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_cases)))
    rho = None
    if n_cases > 2 and np.std(fa) > 0 and np.std(ex) > 0:
        rho_v, _ = stats.spearmanr(fa, ex)
        if np.isfinite(rho_v):
            rho = float(rho_v)
    support_pass = None if rho is None else bool(rho > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 30."
    elif t_val is not None and mean_ex > 0 and t_val >= 2:
        if support_pass:
            status = "confirmed"
            decided = "Mean excess return positive with t >= 2 over at least 30 cases and width Spearman correlation above 0."
        else:
            status = "inconclusive"
            decided = "Confirm-level t but the width Spearman correlation is not above 0."
    elif t_val is not None and mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Spearman(forecast width, excess return) > 0",
            "value": rho,
            "passed": support_pass,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
