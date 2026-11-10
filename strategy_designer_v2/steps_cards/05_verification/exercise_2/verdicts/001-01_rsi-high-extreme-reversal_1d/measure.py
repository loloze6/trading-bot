import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    EXTREME = -10.0
    MIN_POOLED = 30
    MIN_PER_COIN = 8
    MIN_NEG_COINS = 2

    pooled = []
    per_coin = {}
    sup_f = []
    sup_r = []

    for coin in sorted(bars.keys()):
        coin_ex = []
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid = np.isfinite(fwd)
            if not valid.any():
                continue
            drift = float(np.mean(fwd[valid]))

            # non-overlapping extreme blocks: take an extreme bar, then skip the next H-1 bars
            t = 0
            while t < n:
                if np.isfinite(fc[t]) and fc[t] <= EXTREME and np.isfinite(fwd[t]):
                    coin_ex.append(fwd[t] - drift)
                    t += H
                else:
                    t += 1

            # supporting check data: all bars with forecast < 0 and a valid forward return
            m = np.isfinite(fc) & (fc < 0) & valid
            sup_f.extend(np.abs(fc[m]).tolist())
            sup_r.extend(fwd[m].tolist())
        per_coin[coin] = coin_ex
        pooled.extend(coin_ex)

    pooled = np.array(pooled, dtype=float)
    n_pooled = int(len(pooled))
    mean_ex = float(np.mean(pooled)) if n_pooled > 0 else None
    t_stat = None
    if n_pooled > 1:
        sd = float(np.std(pooled, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_pooled)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    coin_counts = {c: len(v) for c, v in per_coin.items()}
    neg_coins = sum(1 for v in coin_means.values() if v is not None and v < 0)

    # supporting check
    rho = None
    passed = None
    if len(sup_f) >= 3 and np.std(sup_f) > 0 and np.std(sup_r) > 0:
        r, _ = stats.spearmanr(sup_f, sup_r)
        if np.isfinite(r):
            rho = float(r)
            passed = bool(rho < 0)

    enough = (n_pooled >= MIN_POOLED and len(per_coin) > 0
              and all(cnt >= MIN_PER_COIN for cnt in coin_counts.values()))

    if not enough or mean_ex is None or t_stat is None:
        status = "inconclusive"
        decided_by = ("Fewer than 30 pooled non-overlapping extreme blocks or fewer than 8 in some coin "
                      f"(pooled {n_pooled}, per coin {coin_counts}), so the result is inconclusive.")
    elif mean_ex < 0 and t_stat <= -2 and neg_coins >= MIN_NEG_COINS:
        status = "confirmed"
        decided_by = (f"Pooled excess return is negative with t = {t_stat:.2f} <= -2 and negative in "
                      f"{neg_coins} coins (>= 2), meeting the confirm rule.")
    elif mean_ex >= 0:
        status = "rejected"
        decided_by = "Pooled excess forward return after extreme bars is >= 0, meeting the reject rule."
    elif neg_coins < MIN_NEG_COINS and t_stat > -1:
        status = "rejected"
        decided_by = (f"Excess return is negative in only {neg_coins} coins (< 2) with t = {t_stat:.2f} > -1, "
                      "meeting the reject rule.")
    elif -2 < t_stat <= -1:
        status = "inconclusive"
        decided_by = (f"Pooled excess return is negative with -2 < t = {t_stat:.2f} <= -1, "
                      "meeting the inconclusive rule.")
    elif t_stat <= -2 and neg_coins < MIN_NEG_COINS:
        status = "inconclusive"
        decided_by = (f"Pooled result is significant (t = {t_stat:.2f}) but the coins are split "
                      f"({neg_coins} negative), meeting the inconclusive rule.")
    else:
        status = "inconclusive"
        decided_by = (f"Pooled excess return is negative but t = {t_stat:.2f} > -1 with {neg_coins} negative coins; "
                      "neither confirm nor reject is met, so inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus own window drift",
            "value": mean_ex,
            "threshold": "negative with t <= -2 and negative in at least 2 coins to confirm; >= 0 rejects",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| vs next 5-bar return over bars with forecast < 0 (should be negative)",
            "value": rho,
            "passed": passed,
        },
        "cases": n_pooled,
        "decided_by": decided_by,
        "reading": ("Only BTC and ETH are in the record, so 'at least 2 of the 3 coins' is read as at least 2 of the "
                    "coins present, which here means both, and the minimum of 8 blocks applies to each coin present; "
                    "non-overlapping blocks are taken greedily in time order within each window, keeping an extreme "
                    "bar and skipping the next 4 bars; drift is the mean 5-bar forward return over all bars in that "
                    "coin-window; t is the one-sample t of the pooled block excesses; the supporting check uses all "
                    "bars with forecast < 0 pooled across coins and windows and does not enter the decision."),
    }
