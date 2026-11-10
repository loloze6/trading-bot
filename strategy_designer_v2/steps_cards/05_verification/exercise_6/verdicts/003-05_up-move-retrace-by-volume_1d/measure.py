import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    thin_shares, heavy_shares = [], []
    sup = {"trending": {"strat": 0.0, "hold": 0.0, "n": 0},
           "mean_reversion": {"strat": 0.0, "hold": 0.0, "n": 0}}

    for coin, windows in bars.items():
        for w, df in windows.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            move = close / close.shift(1) - 1.0       # the bar's own one-bar return, inside the window
            nxt = close.shift(-1) / close - 1.0       # next bar's close-to-close return, inside the window
            regime = df["regime"].astype(str)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")

            for i in range(len(df)):
                r = regime.iloc[i]
                if r not in ("trending", "mean_reversion"):
                    continue
                m, n = move.iloc[i], nxt.iloc[i]
                # main measure: share kept or given back
                if pd.notna(m) and pd.notna(n) and m > 0:
                    share = n / m
                    if r == "mean_reversion":
                        thin_shares.append(share)
                    else:
                        heavy_shares.append(share)
                # supporting check: active bars only
                a = alloc.iloc[i]
                if pd.notna(a) and pd.notna(n) and a != 0:
                    sup[r]["strat"] += a * n
                    sup[r]["hold"] += n
                    sup[r]["n"] += 1

    n_thin, n_heavy = len(thin_shares), len(heavy_shares)
    thin_mean = float(np.mean(thin_shares)) if n_thin else None
    heavy_mean = float(np.mean(heavy_shares)) if n_heavy else None
    diff = (thin_mean - heavy_mean) if (thin_mean is not None and heavy_mean is not None) else None

    t_stat = None
    if n_thin >= 2 and n_heavy >= 2:
        t = stats.ttest_ind(thin_shares, heavy_shares, equal_var=False).statistic
        if np.isfinite(t):
            t_stat = float(t)

    # supporting check: strategy return minus holding BTC, summed over active bars, per part
    ex_heavy = (sup["trending"]["strat"] - sup["trending"]["hold"]) if sup["trending"]["n"] else None
    ex_thin = (sup["mean_reversion"]["strat"] - sup["mean_reversion"]["hold"]) if sup["mean_reversion"]["n"] else None
    if ex_heavy is None or ex_thin is None:
        sup_val, sup_pass = None, None
    else:
        sup_val = float(min(ex_heavy, ex_thin))
        sup_pass = bool(ex_heavy > 0 and ex_thin > 0)

    # decision
    if n_thin < 15 or n_heavy < 15:
        status = "inconclusive"
        decided = "Fewer than 15 thin cases or fewer than 15 heavy cases across the 6 windows, so the result is inconclusive."
    elif thin_mean >= heavy_mean:
        status = "rejected"
        decided = "The thin mean share is at or above the heavy mean share, so the idea is rejected."
    elif t_stat is None or t_stat > -2.0:
        status = "inconclusive"
        decided = "Thin is below heavy but the Welch t-stat magnitude is under 2.0, so the result is inconclusive."
    elif thin_mean < 0:
        status = "confirmed"
        decided = "The thin mean share is below the heavy mean share with a Welch t-stat of at least 2.0 in magnitude, and the thin mean share is below 0, so the idea is confirmed."
    else:
        status = "inconclusive"
        decided = "Thin is significantly below heavy but the thin mean share is not below 0; this meets neither the confirm nor the reject rule, so the result is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar share of move, thin minus heavy",
            "value": None if diff is None else float(diff),
            "statistic": None if t_stat is None else {"name": "Welch t (thin minus heavy)", "value": t_stat},
            "threshold": "thin mean share below heavy mean share with Welch t of at least 2.0 in magnitude, and thin mean share below 0",
        },
        "supporting_check": {
            "name": "strategy minus holding BTC on active bars, min of heavy-only and thin-only parts",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"thin cases": n_thin, "heavy cases": n_heavy},
        "decided_by": decided,
        "reading": "Heavy and thin cases are the bars labelled trending and mean_reversion. The move is the bar's own close-to-close return inside its window, and only moves above 0 are kept. The t-stat compares thin minus heavy, so a value of -2.0 or lower counts as at least 2.0. The case where thin is significantly below heavy but not below 0 matches no rule and is treated as inconclusive. The supporting check sums the strategy's gain minus BTC's return over active bars (allocation not 0), split by regime, and is reported but does not enter the decision.",
    }
