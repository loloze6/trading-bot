import numpy as np
import pandas as pd


def measure(bars):
    POS = "postRebalance_current_allocation"
    gains = []      # per case: position x (next-bar return - window's unconditional mean)
    abs_pos = []    # per case: |position|
    adj_rets = []   # per case: next-bar return - window's unconditional mean

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) < 2:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            # Next-bar return, inside this window only.
            nxt = close.shift(-1) / close - 1.0
            uncond = nxt.dropna()
            if len(uncond) == 0:
                continue
            uncond_mean = float(uncond.mean())

            pos = pd.to_numeric(df[POS], errors="coerce")
            regime = df["regime"].astype(str)
            # A case is a thin-volume up bar, which the strategy labels mean_reversion.
            is_case = (regime == "mean_reversion") & nxt.notna() & pos.notna()
            for i in np.where(is_case.values)[0]:
                r_adj = float(nxt.iloc[i]) - uncond_mean
                p = float(pos.iloc[i])
                gains.append(p * r_adj)
                abs_pos.append(abs(p))
                adj_rets.append(r_adj)

    gains = np.asarray(gains, dtype=float)
    abs_pos = np.asarray(abs_pos, dtype=float)
    adj_rets = np.asarray(adj_rets, dtype=float)
    n = int(len(gains))

    mean_gain = float(np.mean(gains)) if n > 0 else None
    t_stat = None
    if n > 1:
        sd = float(np.std(gains, ddof=1))
        if sd > 0:
            t_stat = mean_gain / (sd / np.sqrt(n))
        elif mean_gain is not None:
            t_stat = 0.0 if mean_gain == 0 else float(np.sign(mean_gain) * np.inf)

    # Supporting check: thirds by |position|, mean next-bar drop vs the unconditional mean.
    support_value = None
    support_passed = None
    if n >= 3:
        order = np.argsort(abs_pos, kind="mergesort")
        thirds = np.array_split(order, 3)
        small_drop = float(-np.mean(adj_rets[thirds[0]]))
        large_drop = float(-np.mean(adj_rets[thirds[-1]]))
        support_value = large_drop - small_drop
        support_passed = bool(large_drop > small_drop)

    if n < 60:
        status = "inconclusive"
        decided_by = (f"Inconclusive rule: only {n} qualifying thin-volume up bars across all windows, "
                      "fewer than the 60 required.")
    elif mean_gain is None or t_stat is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the t-stat could not be computed."
    elif mean_gain > 0 and t_stat >= 2.0 and support_passed:
        status = "confirmed"
        decided_by = ("Confirm rule: the drift-adjusted, position-weighted next-bar return of the short is above 0 "
                      "with a t-stat of at least 2.0, and the largest third reverts more than the smallest third.")
    elif mean_gain <= 0 and t_stat <= 0:
        status = "rejected"
        decided_by = ("Reject rule: the short earns 0 or less after the drift adjustment, "
                      "with a t-stat of 0 or below.")
    elif mean_gain > 0 and t_stat >= 2.0:
        status = "inconclusive"
        decided_by = ("Inconclusive rule: the drift-adjusted mean is confirmed (t >= 2) "
                      "but the largest third does not revert more than the smallest third.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive rule: the drift-adjusted result has a t-stat between 0 and 2 "
                      "and is neither confirmed nor rejected.")

    return {
        "status": status,
        "main_measure": {
            "name": "drift-adjusted, position-weighted next-bar return of the short (mean per case)",
            "value": mean_gain,
            "threshold": "above 0 with t-stat >= 2.0 to confirm; <= 0 with t-stat <= 0 to reject",
            "t_stat": None if t_stat is None else float(t_stat),
        },
        "supporting_check": {
            "name": "largest-third minus smallest-third (by |position|) mean drift-adjusted next-bar drop",
            "value": support_value,
            "passed": support_passed,
        },
        "cases": n,
        "decided_by": decided_by,
        "reading": ("A case is a bar labelled regime 'mean_reversion' with a next bar in the same window. Its value is "
                    "postRebalance_current_allocation x (next-bar return minus that window's unconditional mean "
                    "next-bar return), and cases with a zero position count with value 0. The t-stat is the mean over "
                    "its standard error, pooled over all windows. Thirds come from a stable sort by |position|."),
    }
