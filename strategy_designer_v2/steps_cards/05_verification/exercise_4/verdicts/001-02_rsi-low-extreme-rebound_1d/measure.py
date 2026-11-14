import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_POOLED = 30
    MIN_PER_COIN = 8
    T_MIN = 2.0
    EPS = 1e-12

    # Collect every bar's forecast and its 5-bar forward return (inside its window only).
    # Mark the non-overlapping grid: positions 0, 5, 10, ... of each window.
    rows = []
    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            for i in range(n):
                rows.append({
                    "coin": coin,
                    "window": window,
                    "pos": i,
                    "forecast": fc[i],
                    "fwd": fwd[i],
                    "grid": (i % H == 0),
                })
    data = pd.DataFrame(rows, columns=["coin", "window", "pos", "forecast", "fwd", "grid"])
    coins = sorted(bars.keys())

    # Top-quintile cut-off: the 80th percentile of all positive forecast values,
    # pooled across coins and windows.
    pos_fc = data.loc[data["forecast"] > EPS, "forecast"].dropna()
    q80 = float(np.quantile(pos_fc.to_numpy(), 0.8)) if len(pos_fc) > 0 else np.nan

    # The samples: grid bars that have both a forecast and a forward return.
    samp = data[data["grid"] & data["forecast"].notna() & data["fwd"].notna()].copy()
    if np.isfinite(q80):
        is_top = (samp["forecast"] > EPS) & (samp["forecast"] >= q80)
    else:
        is_top = pd.Series(False, index=samp.index)
    is_zero = samp["forecast"].abs() <= EPS
    top = samp[is_top]
    neu = samp[is_zero]

    # Main measure: pooled excess return (top quintile minus neutral) and Welch t.
    excess = None
    t_stat = None
    if len(top) >= 1 and len(neu) >= 1:
        excess = float(top["fwd"].mean() - neu["fwd"].mean())
    if len(top) >= 2 and len(neu) >= 2:
        t = stats.ttest_ind(top["fwd"].to_numpy(), neu["fwd"].to_numpy(), equal_var=False).statistic
        t_stat = float(t) if np.isfinite(t) else None

    # Excess return for each coin.
    per_coin = {}
    top_counts = {}
    for c in coins:
        tc = top[top["coin"] == c]["fwd"]
        nc = neu[neu["coin"] == c]["fwd"]
        top_counts[c] = int(len(tc))
        if len(tc) >= 1 and len(nc) >= 1:
            per_coin[c] = float(tc.mean() - nc.mean())
        else:
            per_coin[c] = None
    n_pos_coins = sum(1 for v in per_coin.values() if v is not None and v > 0)
    n_nonpos_coins = sum(1 for v in per_coin.values() if v is not None and v <= 0)

    # Supporting check: Spearman correlation between the forecast and the forward return,
    # on grid bars with a positive forecast.
    pos_samp = samp[samp["forecast"] > EPS]
    rho = None
    passed = None
    if len(pos_samp) >= 3:
        r = stats.spearmanr(pos_samp["forecast"].to_numpy(), pos_samp["fwd"].to_numpy()).correlation
        if r is not None and np.isfinite(r):
            rho = float(r)
            passed = bool(rho > 0)

    n_top_pooled = int(len(top))
    counts = {"non-overlapping top-quintile cases pooled": n_top_pooled}
    for c in coins:
        counts[f"top-quintile cases {c}"] = top_counts[c]
    counts["non-overlapping neutral cases pooled"] = int(len(neu))
    counts["coins with positive excess"] = int(n_pos_coins)
    counts["coins with non-positive excess"] = int(n_nonpos_coins)
    counts["coins in record"] = int(len(coins))

    # Apply the plan's rule.
    too_few = (n_top_pooled < MIN_POOLED) or any(top_counts[c] < MIN_PER_COIN for c in coins)
    if too_few:
        status = "inconclusive"
        decided = (f"Inconclusive: fewer than {MIN_POOLED} pooled non-overlapping top-quintile cases "
                   f"or fewer than {MIN_PER_COIN} for at least one coin.")
    elif excess is None:
        status = "inconclusive"
        decided = "Inconclusive: the excess return cannot be computed because a group has no samples."
    elif excess > 0 and t_stat is not None and t_stat >= T_MIN and n_pos_coins >= 2:
        status = "confirmed"
        decided = ("Confirmed: the pooled excess return is above 0 with Welch t >= 2 "
                   "and is positive in at least 2 coins.")
    elif excess <= 0 and n_nonpos_coins >= 2:
        status = "rejected"
        decided = ("Rejected: the pooled excess return is at or below 0 "
                   "and is non-positive in at least 2 coins.")
    elif excess > 0 and (t_stat is None or t_stat < T_MIN):
        status = "inconclusive"
        decided = "Inconclusive: the excess return is positive but its t-statistic is below 2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the coins disagree beyond the confirm and reject rules."

    return {
        "status": status,
        "main_measure": {
            "name": "pooled fwd 5-bar return, top-quintile forecast minus zero forecast",
            "value": excess,
            "statistic": {"name": "Welch t", "value": t_stat} if t_stat is not None else None,
            "threshold": "excess > 0 with t >= 2 and positive in at least 2 of 3 coins to confirm; "
                         "excess <= 0 and non-positive in at least 2 coins to reject",
        },
        "supporting_check": {
            "name": "Spearman rank corr of forecast vs fwd 5-bar return (positive forecasts)",
            "value": rho,
            "passed": passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The top-quintile cut-off is the 80th percentile of all positive forecasts, pooled across "
                    "coins and windows (bars at or above it count); samples are the grid bars 0, 5, 10, ... of "
                    "each window; the Spearman check uses the same grid; and since only "
                    f"{len(coins)} coins are in the record, the 'at least 2 of the 3 coins' counts are applied "
                    "literally to the coins present."),
    }
