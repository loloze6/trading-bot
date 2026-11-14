import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    EXTREME = -10.0
    MIN_POOLED = 30
    MIN_PER_COIN = 8

    pooled_excess = []
    per_coin_excess = {}
    sup_size = []
    sup_ret = []

    for coin in sorted(bars.keys()):
        coin_vals = []
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # Non-overlapping grid: positions 0, H, 2H, ... with a full 5-bar forward return in the window
            grid = [i for i in range(0, n, H) if i + H < n]
            fwd = []
            fcs = []
            for i in grid:
                c0, c1 = close[i], close[i + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    fwd.append(c1 / c0 - 1.0)
                else:
                    fwd.append(np.nan)
                fcs.append(fc[i])
            fwd = np.array(fwd, dtype=float)
            fcs = np.array(fcs, dtype=float)

            valid_ret = np.isfinite(fwd)
            if valid_ret.sum() == 0:
                continue
            drift = float(np.mean(fwd[valid_ret]))

            ext = valid_ret & np.isfinite(fcs) & (fcs <= EXTREME)
            ex = (fwd[ext] - drift).tolist()
            coin_vals.extend(ex)
            pooled_excess.extend(ex)

            neg = valid_ret & np.isfinite(fcs) & (fcs < 0)
            sup_size.extend(np.abs(fcs[neg]).tolist())
            sup_ret.extend(fwd[neg].tolist())
        per_coin_excess[coin] = coin_vals

    pooled = np.array(pooled_excess, dtype=float)
    n_pooled = int(len(pooled))
    mean_ex = float(np.mean(pooled)) if n_pooled > 0 else None
    t_stat = None
    if n_pooled >= 2:
        sd = float(np.std(pooled, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_pooled)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin_excess.items()}
    coin_counts = {c: int(len(v)) for c, v in per_coin_excess.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))

    # Supporting check
    rho = None
    passed = None
    if len(sup_size) >= 3:
        r = stats.spearmanr(sup_size, sup_ret).correlation
        if r is not None and np.isfinite(r):
            rho = float(r)
            passed = bool(rho < 0)

    counts = {"pooled non-overlapping extreme blocks": n_pooled}
    for c in sorted(coin_counts):
        counts[f"extreme blocks {c}"] = coin_counts[c]
    counts["coins with negative excess return"] = n_neg_coins
    counts["coins in record"] = len(per_coin_excess)

    enough = (n_pooled >= MIN_POOLED and len(coin_counts) > 0
              and all(v >= MIN_PER_COIN for v in coin_counts.values()))

    if not enough:
        status = "inconclusive"
        decided_by = ("Fewer than 30 pooled non-overlapping extreme blocks or fewer than 8 in some coin, "
                      "so the plan's minimum counts make the result inconclusive.")
    elif mean_ex is None or t_stat is None:
        status = "inconclusive"
        decided_by = "The pooled excess return or its t-statistic could not be computed, so the result is inconclusive."
    elif mean_ex >= 0:
        status = "rejected"
        decided_by = "The pooled excess forward return after extreme bars is >= 0, which meets the reject rule."
    elif t_stat <= -2 and n_neg_coins >= 2:
        status = "confirmed"
        decided_by = ("The pooled excess forward return after extreme bars is negative with t <= -2 and negative "
                      "in at least 2 coins, which meets the confirm rule.")
    elif n_neg_coins < 2 and t_stat > -1:
        status = "rejected"
        decided_by = ("The pooled excess return is negative in fewer than 2 coins with t > -1, "
                      "which meets the reject rule.")
    else:
        status = "inconclusive"
        if t_stat <= -2:
            decided_by = ("The pooled excess return is significant (t <= -2) but negative in fewer than 2 coins, "
                          "so the coins are split and the result is inconclusive.")
        else:
            decided_by = ("The pooled excess return is negative with -2 < t <= -1 (or weak with coins split), "
                          "which meets the inconclusive rule.")

    reading = ("Extreme bars are non-overlapping grid bars (positions 0,5,10,... per window with a full 5-bar return "
               "inside the window) with forecast <= -10, each coin's drift is the mean 5-bar forward return over that "
               "window's grid bars, pooled t is the ordinary t of the mean excess, the supporting Spearman correlation "
               "uses the same grid bars with forecast < 0, and the 'at least 2 of 3 coins' rule and per-coin minimum "
               "apply to the coins present in the record (BTCUSD, ETHUSD; BNB did not run).")

    return {
        "status": status,
        "main_measure": {
            "name": "pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus own-window drift",
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": ("confirm if negative with t <= -2 and negative in at least 2 coins; reject if >= 0 or "
                          "negative in fewer than 2 coins with t > -1; at least 30 pooled and 8 per coin blocks"),
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| with next 5-bar return over forecast < 0 bars (should be negative)",
            "value": rho,
            "passed": passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
