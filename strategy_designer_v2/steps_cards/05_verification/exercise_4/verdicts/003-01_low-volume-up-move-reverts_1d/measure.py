import numpy as np
import pandas as pd


def measure(bars):
    pos_col = "postRebalance_current_allocation"
    case_pos = []
    case_excess = []
    n_qualifying = 0

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            next_ret = close.shift(-1) / close - 1.0  # inside this window only
            mu = next_ret.dropna().mean()  # unconditional mean next-bar return in this window
            if not np.isfinite(mu):
                continue
            regime = df["regime"].astype(str)
            pos = pd.to_numeric(df[pos_col], errors="coerce")
            mask = (regime == "mean_reversion") & next_ret.notna() & pos.notna()
            for i in np.where(mask.values)[0]:
                case_pos.append(float(pos.iloc[i]))
                case_excess.append(float(next_ret.iloc[i] - mu))
                n_qualifying += 1

    case_pos = np.array(case_pos, dtype=float)
    case_excess = np.array(case_excess, dtype=float)

    # Position-weighted, drift-adjusted next-bar return of the position (short gains when price falls).
    weighted = case_pos * case_excess
    n = len(weighted)
    mean_val = float(np.mean(weighted)) if n > 0 else None
    t_val = None
    if n >= 2:
        sd = float(np.std(weighted, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n)))
        else:
            t_val = 0.0 if mean_val == 0 else float(np.sign(mean_val) * np.inf)

    # Supporting check: thirds by |position|, mean next-bar drop vs unconditional mean.
    sup_value = None
    sup_passed = None
    n_large = n_small = 0
    if n >= 3:
        order = np.argsort(np.abs(case_pos), kind="stable")
        thirds = np.array_split(order, 3)
        small, large = thirds[0], thirds[-1]
        n_small, n_large = len(small), len(large)
        if n_small > 0 and n_large > 0:
            drop_small = float(np.mean(-case_excess[small]))
            drop_large = float(np.mean(-case_excess[large]))
            sup_value = drop_large - drop_small
            sup_passed = bool(drop_large > drop_small)

    if n_qualifying < 60 or mean_val is None or t_val is None:
        status = "inconclusive"
        decided_by = "Fewer than 60 qualifying bars across all windows (or no computable t-stat), which the plan calls inconclusive."
    elif mean_val > 0 and t_val >= 2.0 and sup_passed:
        status = "confirmed"
        decided_by = "The drift-adjusted, position-weighted next-bar return of the short is above 0 with t >= 2.0 and the largest third reverts more than the smallest third."
    elif mean_val <= 0 and t_val <= 0:
        status = "rejected"
        decided_by = "The short earns 0 or less after the drift adjustment with a t-stat of 0 or below."
    else:
        status = "inconclusive"
        if mean_val > 0 and t_val >= 2.0:
            decided_by = "The mean is confirmed but the largest third does not revert more than the smallest third, which the plan calls inconclusive."
        else:
            decided_by = "The drift-adjusted result is not confirmed (t-stat between 0 and 2) nor rejected, which the plan calls inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "drift-adjusted position-weighted next-bar return after thin-volume up bars",
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": "above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject",
        },
        "supporting_check": {
            "name": "largest-third minus smallest-third mean drift-adjusted next-bar drop, by |position|",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {
            "qualifying bars": int(n_qualifying),
            "largest third": int(n_large),
            "smallest third": int(n_small),
        },
        "decided_by": decided_by,
        "reading": (
            "Qualifying bars are rows with regime 'mean_reversion' that have a next close in the same window. "
            "The position is postRebalance_current_allocation, the position actually held. "
            "Each case is position x (next-bar return minus that window's unconditional mean next-bar return), pooled over all windows. "
            "Thirds are a stable sort on |position| split with array_split."
        ),
    }
