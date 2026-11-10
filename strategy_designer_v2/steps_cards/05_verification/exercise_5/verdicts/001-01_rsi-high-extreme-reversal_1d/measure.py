import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    THRESH = -10.0
    MIN_POOLED = 30
    MIN_PER_COIN = 8
    MIN_NEG_COINS = 2

    pooled_excess = []
    per_coin_excess = {}
    sup_size = []
    sup_ret = []

    for coin, windows in bars.items():
        coin_vals = []
        for win, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # supporting check: all bars with forecast < 0 and a valid forward return
            m_sup = (fc < 0) & np.isfinite(fwd) & np.isfinite(fc)
            sup_size.extend(np.abs(fc[m_sup]).tolist())
            sup_ret.extend(fwd[m_sup].tolist())

            # non-overlapping grid: positions 0, H, 2H, ...
            grid = np.arange(0, n, H)
            g_fwd = fwd[grid]
            g_fc = fc[grid]
            valid = np.isfinite(g_fwd)
            if valid.sum() == 0:
                continue
            drift = float(np.mean(g_fwd[valid]))
            ext = valid & np.isfinite(g_fc) & (g_fc <= THRESH)
            ex = (g_fwd[ext] - drift).tolist()
            coin_vals.extend(ex)
            pooled_excess.extend(ex)
        per_coin_excess[coin] = coin_vals

    pooled = np.array(pooled_excess, dtype=float)
    n_pooled = int(len(pooled))
    mean_ex = float(pooled.mean()) if n_pooled > 0 else None
    t_val = None
    if n_pooled >= 2:
        sd = float(pooled.std(ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_pooled)))

    coin_counts = {c: len(v) for c, v in per_coin_excess.items()}
    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin_excess.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))

    # supporting check
    sup_val = None
    sup_pass = None
    if len(sup_size) >= 3 and np.std(sup_size) > 0 and np.std(sup_ret) > 0:
        rho, _ = stats.spearmanr(sup_size, sup_ret)
        if np.isfinite(rho):
            sup_val = float(rho)
            sup_pass = bool(rho < 0)

    counts = {"pooled non-overlapping extreme blocks": n_pooled}
    for c, k in coin_counts.items():
        counts[f"extreme blocks {c}"] = int(k)
    counts["coins with negative excess return"] = n_neg_coins
    counts["coins in record"] = int(len(per_coin_excess))

    enough = n_pooled >= MIN_POOLED and len(coin_counts) > 0 and all(
        k >= MIN_PER_COIN for k in coin_counts.values()
    )

    if not enough or mean_ex is None or t_val is None:
        status = "inconclusive"
        decided = ("Fewer than 30 pooled non-overlapping extreme blocks or fewer than 8 in some coin "
                   "(or no usable t), so the result is inconclusive.")
    elif mean_ex < 0 and t_val <= -2 and n_neg_coins >= MIN_NEG_COINS:
        status = "confirmed"
        decided = ("Pooled excess forward return after extreme bars is negative with t <= -2 and "
                   "negative in at least 2 coins.")
    elif mean_ex >= 0:
        status = "rejected"
        decided = "Pooled excess forward return after extreme bars is >= 0."
    elif n_neg_coins < MIN_NEG_COINS and t_val > -1:
        status = "rejected"
        decided = "Excess return is negative in fewer than 2 coins with t > -1."
    elif -2 < t_val <= -1:
        status = "inconclusive"
        decided = "Negative pooled excess return with -2 < t <= -1."
    elif t_val <= -2:
        status = "inconclusive"
        decided = "Significant pooled negative result but the coins are split (fewer than 2 negative)."
    else:
        status = "inconclusive"
        decided = ("Negative pooled excess return with t > -1 but negative in at least 2 coins, "
                   "which meets neither confirm nor reject, so inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus coin-window drift",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": "negative with t <= -2 and negative in at least 2 of the 3 coins",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| with next 5-bar return, forecast < 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Drift is the mean 5-bar forward return over the same non-overlapping grid (positions 0,5,10,... "
                    "per window) as the extreme blocks, the per-coin minimum of 8 and the 'at least 2 coins negative' "
                    "rule are applied to the coins present in the record (BNB is absent), and the supporting check uses "
                    "all bars with forecast < 0 pooled across coins and windows."),
    }
