import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    EXT = -10.0
    MIN_POOLED = 30
    MIN_PER_COIN = 8
    MIN_NEG_COINS = 2

    pooled_excess = []
    per_coin_excess = {}
    sup_size, sup_ret = [], []

    for coin in sorted(bars.keys()):
        coin_vals = []
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # supporting check: all bars with forecast < 0 inside the window
            m_sup = np.isfinite(fc) & (fc < 0) & np.isfinite(fwd)
            sup_size.extend(np.abs(fc[m_sup]).tolist())
            sup_ret.extend(fwd[m_sup].tolist())

            # non-overlapping grid: positions 0, H, 2H, ... from the window's first row
            grid = np.arange(0, n, H)
            g_fwd = fwd[grid]
            g_fc = fc[grid]
            valid = np.isfinite(g_fwd)
            if valid.sum() == 0:
                continue
            drift = float(np.mean(g_fwd[valid]))
            ext = valid & np.isfinite(g_fc) & (g_fc <= EXT)
            ex = (g_fwd[ext] - drift).tolist()
            coin_vals.extend(ex)
        per_coin_excess[coin] = coin_vals
        pooled_excess.extend(coin_vals)

    pooled = np.array(pooled_excess, dtype=float)
    n_pooled = int(len(pooled))
    mean_ex = float(np.mean(pooled)) if n_pooled > 0 else None
    t_val = None
    if n_pooled >= 2:
        sd = float(np.std(pooled, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_pooled)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin_excess.items()}
    coin_counts = {c: len(v) for c, v in per_coin_excess.items()}
    neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))

    # supporting check
    rho = None
    passed = None
    if len(sup_size) >= 3:
        r, _ = stats.spearmanr(sup_size, sup_ret)
        if r is not None and np.isfinite(r):
            rho = float(r)
            passed = bool(rho < 0)

    counts = {"pooled non-overlapping extreme blocks": n_pooled}
    for c, k in coin_counts.items():
        counts["extreme blocks " + c] = int(k)
    counts["coins with negative excess return"] = neg_coins

    enough = n_pooled >= MIN_POOLED and len(coin_counts) > 0 and all(
        k >= MIN_PER_COIN for k in coin_counts.values()
    )

    if not enough or mean_ex is None or t_val is None:
        status = "inconclusive"
        decided_by = ("Fewer than 30 pooled non-overlapping extreme blocks or fewer than 8 per coin "
                      "(or no usable t), so the result is inconclusive.")
    elif mean_ex >= 0:
        status = "rejected"
        decided_by = "The pooled excess forward return after extreme bars is >= 0, which meets the reject rule."
    elif neg_coins < MIN_NEG_COINS and t_val > -1:
        status = "rejected"
        decided_by = "The excess return is negative in fewer than 2 coins with t > -1, which meets the reject rule."
    elif t_val <= -2 and neg_coins >= MIN_NEG_COINS:
        status = "confirmed"
        decided_by = ("The pooled excess forward return after extreme bars is negative with t <= -2 and "
                      "negative in at least 2 coins, which meets the confirm rule.")
    else:
        status = "inconclusive"
        if t_val <= -2:
            decided_by = "A significant negative pooled result with the coins split, which is inconclusive."
        else:
            decided_by = "A negative pooled excess return with -2 < t <= -1 (or otherwise between rules), which is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "pooled 5-bar excess forward return after extreme bars (forecast <= -10) minus coin-window drift",
            "value": mean_ex,
            "statistic": ({"name": "one-sample t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": "confirm if negative with t <= -2 and negative in at least 2 coins; reject if >= 0 or negative in fewer than 2 coins with t > -1",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| with next 5-bar return over bars with forecast < 0",
            "value": rho,
            "passed": passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Drift is each window's mean 5-bar forward return over the same non-overlapping grid (positions 0,5,10,... "
                    "from the window's first row), the 'at least 2 of the 3 coins' and 'at least 8 per coin' rules are applied "
                    "to the coins present in the record (BTCUSD, ETHUSD; BNB is absent) with the threshold of 2 kept, and the "
                    "supporting check uses all in-window bars with forecast < 0 and is reported but does not enter the decision."),
    }
