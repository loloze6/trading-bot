import numpy as np
import pandas as pd


def measure(bars):
    pos_col = "postRebalance_current_allocation"
    case_vals = []   # position-weighted, drift-adjusted next-bar return of the held position
    case_abs = []    # |position| for the size thirds
    case_drop = []   # drift-adjusted next-bar drop: -(r - mu)
    n_windows = 0

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if df is None or len(df) < 2:
                continue
            n_windows += 1
            close = df["close"].astype(float)
            r_next = close.shift(-1) / close - 1.0  # inside this window only
            mu = r_next.dropna().mean()             # unconditional mean next-bar return, this window
            if not np.isfinite(mu):
                continue
            thin_up = df["regime"].astype(str) == "mean_reversion"
            pos = pd.to_numeric(df[pos_col], errors="coerce")
            mask = thin_up & r_next.notna() & pos.notna()
            for i in np.where(mask.values)[0]:
                p = float(pos.iloc[i])
                adj = float(r_next.iloc[i]) - mu
                case_vals.append(p * adj)
                case_abs.append(abs(p))
                case_drop.append(-adj)

    n = len(case_vals)
    vals = np.array(case_vals, dtype=float)

    mean_val = float(vals.mean()) if n > 0 else None
    t_val = None
    if n > 1:
        sd = vals.std(ddof=1)
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n)))

    # Supporting check: thirds by |position|
    sup_value = None
    sup_passed = None
    if n >= 3:
        order = np.argsort(np.array(case_abs), kind="mergesort")
        thirds = np.array_split(order, 3)
        drops = np.array(case_drop, dtype=float)
        small = drops[thirds[0]]
        large = drops[thirds[2]]
        if len(small) > 0 and len(large) > 0:
            sup_value = float(large.mean() - small.mean())
            sup_passed = bool(sup_value > 0)

    if n < 60:
        status = "inconclusive"
        decided = "Fewer than 60 qualifying thin-volume up bars across all windows, so the result is inconclusive."
    elif mean_val is None or t_val is None:
        status = "inconclusive"
        decided = "The t-stat could not be computed (no dispersion), so the rule cannot be applied and the result is inconclusive."
    elif mean_val > 0 and t_val >= 2.0 and sup_passed is True:
        status = "confirmed"
        decided = "The drift-adjusted, position-weighted short return is above 0 with t >= 2.0 and the largest |position| third reverts more than the smallest third."
    elif mean_val <= 0 and t_val <= 0:
        status = "rejected"
        decided = "The short earns 0 or less after the drift adjustment with a t-stat of 0 or below."
    elif mean_val > 0 and t_val >= 2.0:
        status = "inconclusive"
        decided = "The mean is confirmed (positive, t >= 2.0) but the largest third does not revert more than the smallest third."
    else:
        status = "inconclusive"
        decided = "The drift-adjusted short return is positive with a t-stat between 0 and 2 (or otherwise meets neither confirm nor reject)."

    return {
        "status": status,
        "main_measure": {
            "name": "drift-adjusted position-weighted next-bar return of the short after thin up bars",
            "value": mean_val,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": "above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject",
        },
        "supporting_check": {
            "name": "largest minus smallest |position| third, mean drift-adjusted next-bar drop",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {
            "qualifying bars": int(n),
            "windows": int(n_windows),
        },
        "decided_by": decided,
        "reading": (
            "Cases are all bars with regime 'mean_reversion' (thin up bars) having a next bar in the same window, each case's "
            "value is postRebalance_current_allocation x (next-bar return minus the window's unconditional mean next-bar return) "
            "averaged over pooled cases with the ordinary t of the mean, and thirds are formed by a stable sort on "
            "|postRebalance_current_allocation| split into three near-equal groups."
        ),
    }
