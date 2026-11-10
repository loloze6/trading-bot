import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    adj_gain = []   # alloc * (r_next - mu_window): positive means the short earned after drift adjustment
    abs_pos = []    # |position| for the size split
    adj_ret = []    # r_next - mu_window

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) < 2:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            r_next = close.shift(-1) / close - 1.0
            mu = r_next.dropna().mean()
            if not np.isfinite(mu):
                continue
            regime = df["regime"].astype(str)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            mask = (regime == "mean_reversion") & r_next.notna() & alloc.notna()
            for i in np.where(mask.values)[0]:
                a = float(alloc.iloc[i])
                rr = float(r_next.iloc[i]) - mu
                adj_gain.append(a * rr)
                abs_pos.append(abs(a))
                adj_ret.append(rr)

    adj_gain = np.asarray(adj_gain, dtype=float)
    abs_pos = np.asarray(abs_pos, dtype=float)
    adj_ret = np.asarray(adj_ret, dtype=float)
    n = int(len(adj_gain))

    mean_val = float(np.mean(adj_gain)) if n > 0 else None
    t_stat = None
    if n >= 2:
        sd = np.std(adj_gain, ddof=1)
        if sd > 0:
            t_stat = float(mean_val / (sd / np.sqrt(n)))
        else:
            t_stat = 0.0 if mean_val == 0 else float(np.sign(mean_val) * np.inf)

    # Supporting check: thirds by |position|
    sup_val = None
    sup_pass = None
    if n >= 3:
        order = np.argsort(abs_pos, kind="mergesort")
        parts = np.array_split(order, 3)
        small_mean = float(np.mean(adj_ret[parts[0]]))
        large_mean = float(np.mean(adj_ret[parts[-1]]))
        # drop measured as negative adjusted return; positive value means largest third falls more
        sup_val = small_mean - large_mean
        sup_pass = bool(large_mean < small_mean)

    if n < 60 or mean_val is None or t_stat is None:
        status = "inconclusive"
        decided_by = "Fewer than 60 qualifying thin up bars across all windows is inconclusive."
    elif mean_val > 0 and t_stat >= 2.0 and sup_pass:
        status = "confirmed"
        decided_by = ("The drift-adjusted, position-weighted next-bar return of the short is above 0 with t >= 2.0 "
                      "and the largest third reverts more than the smallest third.")
    elif mean_val <= 0 and t_stat <= 0:
        status = "rejected"
        decided_by = ("The short earns 0 or less after the drift adjustment with a t-stat of 0 or below.")
    else:
        status = "inconclusive"
        if mean_val > 0 and t_stat >= 2.0:
            decided_by = "A confirmed mean without the size ordering is inconclusive."
        else:
            decided_by = "A drift-adjusted result with a t-stat between 0 and 2 (or mixed sign) is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "drift-adjusted position-weighted next-bar return of the short (t-stat)",
            "value": t_stat if t_stat is None or np.isfinite(t_stat) else float(np.sign(t_stat) * 1e9),
            "threshold": "mean above 0 with t-stat >= 2.0 to confirm; mean <= 0 with t-stat <= 0 to reject; at least 60 cases",
        },
        "supporting_check": {
            "name": "largest-third minus smallest-third next-bar drop vs unconditional mean (by |position|)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "cases": n,
        "decided_by": decided_by,
        "reading": ("Thin up bars are rows labelled regime 'mean_reversion'; each case's value is "
                    "postRebalance_current_allocation x (next-bar return minus the window's mean next-bar return), "
                    "pooled across all windows, with the main value reported as the t-stat of these values "
                    f"(mean {mean_val}); thirds are split by sorted |position| with numpy array_split."),
    }
