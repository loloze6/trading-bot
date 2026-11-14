import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    thin_shares, heavy_shares = [], []
    sup = {"trending": [], "mean_reversion": []}

    for coin, windows in bars.items():
        for w, df in windows.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            move = close / close.shift(1) - 1.0          # the bar's own one-bar move, inside the window
            nxt = close.shift(-1) / close - 1.0          # next bar's close-to-close return, inside the window
            regime = df["regime"].astype(str)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")

            for i in range(len(df)):
                r = regime.iat[i]
                if r not in ("trending", "mean_reversion"):
                    continue
                m, n = move.iat[i], nxt.iat[i]
                if np.isfinite(m) and np.isfinite(n) and m > 0:
                    share = n / m
                    if r == "mean_reversion":
                        thin_shares.append(share)
                    else:
                        heavy_shares.append(share)
                a = alloc.iat[i]
                if np.isfinite(a) and np.isfinite(n) and a != 0:
                    sup[r].append(a * n - n)  # strategy gain before costs minus holding BTC

    n_thin, n_heavy = len(thin_shares), len(heavy_shares)
    thin_mean = float(np.mean(thin_shares)) if n_thin else None
    heavy_mean = float(np.mean(heavy_shares)) if n_heavy else None
    diff = (thin_mean - heavy_mean) if (thin_mean is not None and heavy_mean is not None) else None

    t_val = None
    if n_thin >= 2 and n_heavy >= 2:
        t = stats.ttest_ind(thin_shares, heavy_shares, equal_var=False).statistic
        t_val = float(t) if np.isfinite(t) else None

    heavy_ex = float(np.mean(sup["trending"])) if sup["trending"] else None
    thin_ex = float(np.mean(sup["mean_reversion"])) if sup["mean_reversion"] else None
    if heavy_ex is None or thin_ex is None:
        sup_val, sup_pass = (heavy_ex if thin_ex is None else thin_ex), None
    else:
        sup_val = min(heavy_ex, thin_ex)
        sup_pass = bool(heavy_ex > 0 and thin_ex > 0)

    if n_thin < 15 or n_heavy < 15:
        status = "inconclusive"
        decided = "Fewer than 15 thin cases or fewer than 15 heavy cases across the windows, so the result is inconclusive."
    elif thin_mean >= heavy_mean:
        status = "rejected"
        decided = "The thin mean share is at or above the heavy mean share, which meets the reject rule."
    elif t_val is None or -t_val < 2.0:
        status = "inconclusive"
        decided = "Thin mean share is below heavy but the Welch t-stat is under 2.0, so the result is inconclusive."
    elif thin_mean >= 0:
        status = "rejected"
        decided = "Thin is significantly below heavy but the thin mean share is at or above 0, so no part of the rise is given back (reject rule)."
    else:
        status = "confirmed"
        decided = "Thin mean share is below heavy with Welch t of at least 2.0 and is below 0, which meets the confirm rule."

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar return / move return, thin minus heavy",
            "value": diff,
            "statistic": ({"name": "Welch t (thin minus heavy)", "value": t_val} if t_val is not None else None),
            "threshold": "thin mean share below heavy with Welch t of at least 2.0 in magnitude, and thin mean share below 0",
        },
        "supporting_check": {
            "name": "min over heavy-only and thin-only parts of mean active-bar gain before costs minus BTC return",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "thin cases": n_thin,
            "heavy cases": n_heavy,
            "thin mean share": thin_mean,
            "heavy mean share": heavy_mean,
            "heavy-only active bars": len(sup["trending"]),
            "thin-only active bars": len(sup["mean_reversion"]),
            "heavy-only mean excess": heavy_ex,
            "thin-only mean excess": thin_ex,
        },
        "decided_by": decided,
        "reading": "Bars are classified by the recorded regime label (mean_reversion = thin, trending = heavy). The move is close[t]/close[t-1]-1 within the window, so each window's first row and any non-positive moves are dropped. The Welch t is taken as thin minus heavy and needs to be at or below -2.0. If thin is significantly below heavy but thin is at or above 0, the plan's second reject clause applies. The supporting check compares the per-bar allocation gain minus the BTC return on bars with a non-zero position in each regime.",
    }
