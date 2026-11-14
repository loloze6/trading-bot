import numpy as np
import pandas as pd


def measure(bars):
    POS = "postRebalance_current_allocation"
    cases = []  # (pos, adj_ret)

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # same window only; last row NaN
            mu = nxt.dropna().mean()  # unconditional mean next-bar return in this window
            if not np.isfinite(mu):
                continue
            pos = pd.to_numeric(d[POS], errors="coerce")
            reg = d["regime"].astype(str)
            mask = (reg == "mean_reversion") & nxt.notna() & pos.notna()
            for i in np.where(mask.values)[0]:
                cases.append((float(pos.iloc[i]), float(nxt.iloc[i] - mu)))

    n = len(cases)
    counts = {"qualifying bars": n}

    value = None
    tstat = None
    sup_value = None
    sup_passed = None

    if n > 0:
        p = np.array([c[0] for c in cases])
        a = np.array([c[1] for c in cases])
        gain = p * a  # drift-adjusted position gain per case (positive = short earned)
        wsum = np.abs(p).sum()
        if wsum > 0:
            value = float(gain.sum() / wsum)
        if n >= 2:
            sd = gain.std(ddof=1)
            if sd > 0:
                tstat = float(gain.mean() / (sd / np.sqrt(n)))
            elif gain.mean() == 0:
                tstat = 0.0

        k = n // 3
        if k >= 1:
            order = np.argsort(np.abs(p), kind="stable")
            small = a[order[:k]]
            large = a[order[-k:]]
            drop_small = -float(small.mean())
            drop_large = -float(large.mean())
            sup_value = drop_large - drop_small
            sup_passed = bool(sup_value > 0)

    if n < 60:
        status = "inconclusive"
        decided = "Fewer than 60 qualifying bars across all windows is inconclusive."
    elif value is None or tstat is None:
        status = "inconclusive"
        decided = "The drift-adjusted position-weighted return or its t-stat could not be computed, so the result is inconclusive."
    elif value > 0 and tstat >= 2.0 and sup_passed:
        status = "confirmed"
        decided = "The drift-adjusted position-weighted next-bar return of the short is above 0 with t >= 2.0 and the largest third reverts more than the smallest third."
    elif value <= 0 and tstat <= 0:
        status = "rejected"
        decided = "The short earns 0 or less after the drift adjustment, with a t-stat of 0 or below."
    elif value > 0 and tstat >= 2.0:
        status = "inconclusive"
        decided = "A confirmed mean without the size ordering is inconclusive."
    else:
        status = "inconclusive"
        decided = "A positive drift-adjusted result with a t-stat between 0 and 2 (or mixed signs) is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "drift-adjusted position-weighted next-bar return of the short after thin up bars",
            "value": value,
            "statistic": None if tstat is None else {"name": "t of the mean of drift-adjusted position gains", "value": tstat},
            "threshold": "above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject",
        },
        "supporting_check": None if sup_value is None else {
            "name": "mean next-bar drop vs unconditional mean, largest third minus smallest third by |position|",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are bars labelled regime 'mean_reversion' with a next bar in the same window, the position is postRebalance_current_allocation (zero positions kept as cases), the main value is sum(pos x (r - window mean)) / sum(|pos|) so a short gains when r falls below the mean, its t-stat is the ordinary t of the per-case gains pos x (r - mean), and thirds are the n//3 cases with smallest and largest |position|.",
    }
