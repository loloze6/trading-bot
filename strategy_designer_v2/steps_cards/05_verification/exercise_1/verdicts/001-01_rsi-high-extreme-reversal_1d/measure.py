import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    EXTREME = -10.0
    MIN_POOLED = 30
    MIN_PER_COIN = 8
    NEED_NEG_COINS = 2

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

            # 5-bar forward return inside this window only
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # the coin's own drift in this window: mean of all valid 5-bar forward returns
            valid_fwd = fwd[np.isfinite(fwd)]
            if valid_fwd.size == 0:
                continue
            drift = float(np.mean(valid_fwd))

            # non-overlapping 5-bar blocks on a fixed grid from the window's first bar
            for start in range(0, n - H, H):
                f = fc[start]
                r = fwd[start]
                if not (np.isfinite(f) and np.isfinite(r)):
                    continue
                if f <= EXTREME:
                    ex = r - drift
                    coin_vals.append(ex)
                    pooled_excess.append(ex)

            # supporting check: all bars with forecast < 0 and a valid 5-bar forward return
            mask = np.isfinite(fc) & np.isfinite(fwd) & (fc < 0)
            sup_size.extend(np.abs(fc[mask]).tolist())
            sup_ret.extend(fwd[mask].tolist())
        per_coin_excess[coin] = coin_vals

    pooled = np.array(pooled_excess, dtype=float)
    n_pooled = int(pooled.size)
    mean_ex = float(np.mean(pooled)) if n_pooled > 0 else None
    t_stat = None
    if n_pooled >= 2:
        sd = float(np.std(pooled, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_pooled)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin_excess.items()}
    coin_counts = {c: len(v) for c, v in per_coin_excess.items()}
    neg_coins = sum(1 for m in coin_means.values() if m is not None and m < 0)

    # supporting check
    rho = None
    passed = None
    if len(sup_size) >= 3:
        r_, _ = stats.spearmanr(sup_size, sup_ret)
        if r_ is not None and np.isfinite(r_):
            rho = float(r_)
            passed = bool(rho < 0)

    enough = (
        n_pooled >= MIN_POOLED
        and len(coin_counts) > 0
        and all(c >= MIN_PER_COIN for c in coin_counts.values())
    )

    if not enough or mean_ex is None or t_stat is None:
        status = "inconclusive"
        decided_by = (
            f"Fewer than {MIN_POOLED} pooled non-overlapping extreme blocks or fewer than "
            f"{MIN_PER_COIN} in some coin (pooled {n_pooled}, per coin {coin_counts}), so the result is inconclusive."
        )
    elif mean_ex >= 0:
        status = "rejected"
        decided_by = "The pooled excess forward return after extreme bars is >= 0, which meets the reject rule."
    elif t_stat <= -2 and neg_coins >= NEED_NEG_COINS:
        status = "confirmed"
        decided_by = (
            f"The pooled excess return is negative with t <= -2 and negative in {neg_coins} coins (at least 2), "
            "which meets the confirm rule."
        )
    elif neg_coins < NEED_NEG_COINS and t_stat > -1:
        status = "rejected"
        decided_by = (
            f"The pooled excess return is negative in fewer than 2 coins ({neg_coins}) with t > -1, "
            "which meets the reject rule."
        )
    else:
        status = "inconclusive"
        if t_stat <= -2:
            decided_by = (
                f"The pooled result is significant (t <= -2) but the coins are split ({neg_coins} negative), "
                "which meets the inconclusive rule."
            )
        else:
            decided_by = (
                "The pooled excess return is negative with -2 < t <= -1 (or otherwise between the confirm and "
                "reject rules), which meets the inconclusive rule."
            )

    return {
        "status": status,
        "main_measure": {
            "name": "pooled excess 5-bar forward return after extreme bars (forecast <= -10), minus coin-window drift",
            "value": mean_ex,
            "threshold": "negative with t <= -2 to confirm; >= 0 rejects; -2 < t <= -1 is inconclusive",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| with next 5-bar return, forecast < 0",
            "value": rho,
            "passed": passed,
        },
        "cases": n_pooled,
        "decided_by": decided_by + f" (t = {t_stat}, per-coin mean excess = {coin_means}, per-coin blocks = {coin_counts})",
        "reading": (
            "Non-overlapping blocks are a fixed 5-bar grid from each window's first bar, and a block counts as "
            "extreme when its start bar has forecast <= -10. Drift is the mean of all valid 5-bar forward returns "
            "in that coin-window. t is the one-sample t of the pooled block excess returns. 'At least 2 of the 3 "
            "coins' and the 8-per-coin minimum are applied to the coins present in the record. The supporting "
            "check uses every bar with forecast < 0 and a valid 5-bar forward return, pooled across coins and windows."
        ),
    }
