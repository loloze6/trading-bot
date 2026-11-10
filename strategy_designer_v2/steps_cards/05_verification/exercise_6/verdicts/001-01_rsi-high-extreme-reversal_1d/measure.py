import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    EXTREME = -10.0
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
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0  # inside this window only

            # Supporting check: all bars with forecast < 0 and a valid 5-bar forward return
            m = (fc < 0) & fwd.notna() & fc.notna()
            sup_size.extend(np.abs(fc[m]).tolist())
            sup_ret.extend(fwd[m].tolist())

            # Non-overlapping grid: positions 0, H, 2H, ... from the window's first row
            grid = np.arange(0, len(df), H)
            g_fwd = fwd.iloc[grid]
            g_fc = fc.iloc[grid]
            valid = g_fwd.notna()
            if valid.sum() == 0:
                continue
            drift = float(g_fwd[valid].mean())
            ext = valid & g_fc.notna() & (g_fc <= EXTREME)
            ex = (g_fwd[ext] - drift).tolist()
            coin_vals.extend(ex)
        per_coin_excess[coin] = coin_vals
        pooled_excess.extend(coin_vals)

    n_pooled = len(pooled_excess)
    per_coin_n = {c: len(v) for c, v in per_coin_excess.items()}
    per_coin_mean = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin_excess.items()}
    n_neg = sum(1 for c, mu in per_coin_mean.items() if mu is not None and mu < 0)

    mean_ex = float(np.mean(pooled_excess)) if n_pooled > 0 else None
    t_stat = None
    if n_pooled >= 2:
        sd = float(np.std(pooled_excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_pooled)))

    # Supporting check
    rho = None
    passed = None
    if len(sup_size) >= 3 and np.nanstd(sup_size) > 0 and np.nanstd(sup_ret) > 0:
        r = stats.spearmanr(sup_size, sup_ret).correlation
        if r is not None and np.isfinite(r):
            rho = float(r)
            passed = bool(rho < 0)

    enough = (n_pooled >= MIN_POOLED) and len(per_coin_n) > 0 and all(
        n >= MIN_PER_COIN for n in per_coin_n.values())

    if not enough or mean_ex is None or t_stat is None:
        status = "inconclusive"
        decided_by = ("Fewer than 30 pooled non-overlapping extreme blocks or fewer than 8 in a coin "
                      "(or no usable t), so the result is inconclusive.")
    elif mean_ex < 0 and t_stat <= -2 and n_neg >= MIN_NEG_COINS:
        status = "confirmed"
        decided_by = ("Pooled excess forward return after extreme bars is negative with t <= -2 and "
                      "negative in at least 2 coins.")
    elif mean_ex >= 0:
        status = "rejected"
        decided_by = "Pooled excess forward return after extreme bars is >= 0."
    elif n_neg < MIN_NEG_COINS and t_stat > -1:
        status = "rejected"
        decided_by = "Excess return is negative in fewer than 2 coins with t > -1."
    else:
        status = "inconclusive"
        if t_stat <= -2:
            decided_by = "Significant negative pooled result but the coins are split (fewer than 2 negative)."
        else:
            decided_by = "Negative pooled excess return with -2 < t <= -1 (or split coins without t > -1)."

    counts = {"pooled non-overlapping extreme blocks": int(n_pooled),
              "coins with negative excess return": int(n_neg)}
    for c, n in per_coin_n.items():
        counts[f"extreme blocks {c}"] = int(n)

    return {
        "status": status,
        "main_measure": {
            "name": "pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus own window drift",
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": "confirm if negative with t <= -2 and negative in >= 2 of the coins; reject if >= 0 or negative in < 2 coins with t > -1",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| vs next 5-bar return, bars with forecast < 0 (should be negative)",
            "value": rho,
            "passed": passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Extreme blocks are grid bars at positions 0,5,10,... of each window with forecast <= -10, drift is the mean "
                    "5-bar forward return over that same grid in the window, t is the ordinary t of the pooled excess mean, the "
                    "'2 of 3 coins' rule and the 8-per-coin minimum are applied to the coins present in the record (BTCUSD, ETHUSD), "
                    "and the supporting rank correlation uses all bars with forecast < 0 (not only the grid)."),
    }
