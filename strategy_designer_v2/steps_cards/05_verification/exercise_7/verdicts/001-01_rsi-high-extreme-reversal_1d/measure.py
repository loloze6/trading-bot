import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    VAL = "debug_info.components.rsi_high.last_history_value"

    # ---------- 1. Situation check: RSI above 50 (raw value (50-RSI)*0.4 < 0), short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", VAL]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            ok = active & (d[VAL] < 0) & (d["forecast"] < 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9

    main_name = "pooled excess 5-bar forward return after extreme bars (forecast <= -10) minus coin's window drift"
    threshold_txt = ("confirm: pooled excess < 0 with t <= -2 and negative in >= 2 coins; "
                     "reject: pooled excess >= 0, or negative in < 2 coins with t > -1; "
                     "min 30 pooled non-overlapping extreme blocks and 8 per coin")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short positions taken while the 14-bar RSI is above 50 "
                           "(raw component value below 0), so the forecast does not do what the plan's situation states."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    pooled = []
    per_coin = {}
    sup_x, sup_y = [], []
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            fc = df["forecast"].astype(float).values

            # supporting: all bars with forecast < 0 and valid forward return
            m = (fc < 0) & np.isfinite(fwd) & np.isfinite(fc)
            sup_x.extend(np.abs(fc[m]).tolist())
            sup_y.extend(fwd[m].tolist())

            # non-overlapping grid: positions 0, 5, 10, ...
            grid = np.arange(0, n, H)
            g_ret = fwd[grid]
            g_fc = fc[grid]
            valid = np.isfinite(g_ret)
            if valid.sum() == 0:
                continue
            drift = float(np.mean(g_ret[valid]))
            ext = valid & np.isfinite(g_fc) & (g_fc <= -10)
            ex = (g_ret[ext] - drift).tolist()
            coin_vals.extend(ex)
        per_coin[coin] = coin_vals
        pooled.extend(coin_vals)

    pooled = np.array(pooled, dtype=float)
    n_pooled = int(len(pooled))
    mean_ex = float(np.mean(pooled)) if n_pooled > 0 else None
    t_val = None
    if n_pooled > 1:
        sd = float(np.std(pooled, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n_pooled)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for v in coin_means.values() if v is not None and v < 0))

    rho = None
    if len(sup_x) >= 3:
        r, _ = stats.spearmanr(sup_x, sup_y)
        if np.isfinite(r):
            rho = float(r)
    sup_pass = None if rho is None else bool(rho < 0)

    counts = {"pooled_non_overlapping_extreme_blocks": n_pooled}
    for c, v in per_coin.items():
        counts[f"extreme_blocks_{c}"] = int(len(v))
    counts["coins_with_negative_excess"] = n_neg_coins

    enough = n_pooled >= 30 and all(len(v) >= 8 for v in per_coin.values()) and len(per_coin) > 0

    if not enough or mean_ex is None or t_val is None:
        status = "inconclusive"
        decided = "Fewer than 30 pooled non-overlapping extreme blocks or fewer than 8 in some coin, so the result is inconclusive."
    elif mean_ex < 0 and t_val <= -2 and n_neg_coins >= 2:
        status = "confirmed"
        decided = "The pooled excess return after extreme bars is negative with t <= -2 and negative in at least 2 coins."
    elif mean_ex >= 0:
        status = "rejected"
        decided = "The pooled excess return after extreme bars is >= 0."
    elif n_neg_coins < 2 and t_val > -1:
        status = "rejected"
        decided = "The excess return is negative in fewer than 2 coins with t > -1."
    elif mean_ex < 0 and -2 < t_val <= -1:
        status = "inconclusive"
        decided = "The pooled excess return is negative with -2 < t <= -1."
    elif mean_ex < 0 and t_val <= -2:
        status = "inconclusive"
        decided = "The pooled result is significant but the coins are split (fewer than 2 coins negative)."
    else:
        status = "inconclusive"
        decided = "The numbers meet neither the confirm nor the reject rule, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |forecast| with next 5-bar return, bars with forecast < 0",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's drift is the mean 5-bar forward return over the same non-overlapping grid (positions 0, 5, 10, ...) "
                    "of each window, the per-coin sign is the mean excess over that coin's extreme blocks, the 'at least 2 of the 3 coins' "
                    "rule is applied as at least 2 negative coins among the coins present, and the supporting correlation uses all bars "
                    "with forecast < 0."),
    }
