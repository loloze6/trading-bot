import numpy as np
import pandas as pd


def measure(bars):
    alloc_col = "postRebalance_current_allocation"
    vals, weights, adj = [], [], []
    n_qual = 0
    n_windows = 0

    for coin, wins in bars.items():
        for wname, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            uncond = nxt.dropna()
            if len(uncond) == 0:
                continue
            mu = float(uncond.mean())
            n_windows += 1
            alloc = pd.to_numeric(d[alloc_col], errors="coerce")
            reg = d["regime"]
            mask = (reg == "mean_reversion") & nxt.notna() & alloc.notna()
            for i in np.where(mask.values)[0]:
                a = float(alloc.iloc[i])
                r_adj = float(nxt.iloc[i]) - mu
                w = abs(a)
                vals.append(-r_adj)   # short's drift-adjusted gain per unit of position
                weights.append(w)
                adj.append(r_adj)
                n_qual += 1

    vals = np.array(vals, dtype=float)
    weights = np.array(weights, dtype=float)
    adj = np.array(adj, dtype=float)

    wmean, tstat = None, None
    if n_qual > 0 and weights.sum() > 0:
        wmean = float(np.sum(vals * weights) / np.sum(weights))
        prod = vals * weights
        if n_qual > 1:
            sd = float(np.std(prod, ddof=1))
            if sd > 0:
                tstat = float(np.mean(prod) / (sd / np.sqrt(n_qual)))

    # Supporting check: thirds by |position|
    sup_val, sup_pass = None, None
    if n_qual >= 3:
        order = np.argsort(weights, kind="mergesort")
        thirds = np.array_split(order, 3)
        small, large = thirds[0], thirds[-1]
        if len(small) > 0 and len(large) > 0:
            drop_large = float(np.mean(-adj[large]))
            drop_small = float(np.mean(-adj[small]))
            sup_val = drop_large - drop_small
            sup_pass = bool(sup_val > 0)

    if n_qual < 60:
        status = "inconclusive"
        decided = f"Fewer than 60 qualifying bars across all windows ({n_qual}), which the plan calls inconclusive."
    elif wmean is None or tstat is None:
        status = "inconclusive"
        decided = "The drift-adjusted position-weighted return or its t-stat could not be computed, so the result is inconclusive."
    elif wmean > 0 and tstat >= 2.0 and sup_pass:
        status = "confirmed"
        decided = "The drift-adjusted position-weighted short return is above 0 with t >= 2.0 and the largest third reverts more than the smallest third."
    elif wmean <= 0 and tstat <= 0:
        status = "rejected"
        decided = "The short earns 0 or less after the drift adjustment with a t-stat of 0 or below."
    elif wmean > 0 and tstat >= 2.0:
        status = "inconclusive"
        decided = "The mean is confirmed but the largest third does not revert more than the smallest third, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The drift-adjusted result has a t-stat between 0 and 2 (or mixed signs), which the plan calls inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "drift-adjusted |position|-weighted next-bar short return after thin up bars",
            "value": wmean,
            "statistic": {"name": "t of the mean of |position| x drift-adjusted short return",
                          "value": tstat} if tstat is not None else None,
            "threshold": "above 0 with t-stat >= 2.0 to confirm; at or below 0 with t-stat <= 0 to reject",
        },
        "supporting_check": {
            "name": "mean drift-adjusted next-bar drop, largest third minus smallest third by |position|",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"qualifying bars": int(n_qual), "windows": int(n_windows)},
        "decided_by": decided,
        "reading": "Qualifying bars are rows labelled regime 'mean_reversion' with a next bar in the same window, weighted by |postRebalance_current_allocation| (zero-position bars included with zero weight); the short's gain is minus (next-bar return minus the window's mean next-bar return over all bars), the t-stat is the ordinary t of the per-case products |position| x that gain, and thirds come from an ascending sort by |position| split with array_split.",
    }
