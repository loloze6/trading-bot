import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    rows = []
    # Pool the forecast's positive values over all bars to set the top-quintile cut-off.
    all_pos = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            all_pos.extend(f[np.isfinite(f) & (f > 0)].tolist())
    all_pos = np.asarray(all_pos, dtype=float)
    q80 = float(np.quantile(all_pos, 0.8)) if all_pos.size > 0 else np.nan

    # Non-overlapping grid: positions 0, 5, 10, ... of each window, forward 5-bar return inside the window.
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and np.isfinite(f[t]) and c[t] != 0):
                    continue
                rows.append((coin, w, f[t], c[t + H] / c[t] - 1.0))

    samp = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    coins = sorted(bars.keys())

    if np.isfinite(q80) and len(samp) > 0:
        top = samp[(samp["forecast"] > 0) & (samp["forecast"] >= q80)]
    else:
        top = samp.iloc[0:0]
    zero = samp[samp["forecast"] == 0]

    def diff_t(a, b):
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        if len(a) == 0 or len(b) == 0:
            return None, None
        d = float(a.mean() - b.mean())
        t = None
        if len(a) >= 2 and len(b) >= 2:
            res = stats.ttest_ind(a, b, equal_var=False)
            if np.isfinite(res.statistic):
                t = float(res.statistic)
        return d, t

    value, tstat = diff_t(top["ret"], zero["ret"])

    per_coin = {}
    per_coin_counts = {}
    for coin in coins:
        tc = top[top["coin"] == coin]["ret"]
        zc = zero[zero["coin"] == coin]["ret"]
        d, _ = diff_t(tc, zc)
        per_coin[coin] = d
        per_coin_counts[coin] = int(len(tc))

    n_pos_coins = sum(1 for d in per_coin.values() if d is not None and d > 0)
    n_nonpos_coins = sum(1 for d in per_coin.values() if d is not None and d <= 0)

    # Supporting check: Spearman on positive-forecast non-overlapping samples.
    pos = samp[samp["forecast"] > 0]
    rho = None
    passed = None
    if len(pos) >= 3 and pos["forecast"].nunique() > 1 and pos["ret"].nunique() > 1:
        r = stats.spearmanr(pos["forecast"], pos["ret"]).correlation
        if np.isfinite(r):
            rho = float(r)
            passed = bool(rho > 0)

    n_top = int(len(top))
    min_coin = min(per_coin_counts.values()) if per_coin_counts else 0

    if n_top < 30 or min_coin < 8 or value is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 30 pooled non-overlapping top-quintile cases or fewer than 8 for "
                      "some coin (or no measurable excess return).")
    elif value > 0 and tstat is not None and tstat >= 2 and n_pos_coins >= 2:
        status = "confirmed"
        decided_by = ("Confirm: pooled excess return above 0 with Welch t of at least 2 and positive in at least "
                      "2 coins.")
    elif value <= 0 and n_nonpos_coins >= 2:
        status = "rejected"
        decided_by = "Reject: pooled excess return at or below 0 and non-positive in at least 2 coins."
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: positive excess return with t below 2, or coins disagree beyond the "
                      "confirm/reject rules.")

    counts = {"pooled non-overlapping top-quintile cases": n_top}
    for coin in coins:
        counts[f"top-quintile cases {coin}"] = per_coin_counts[coin]
    counts["neutral (forecast 0) cases"] = int(len(zero))
    counts["coins with positive excess return"] = int(n_pos_coins)
    counts["coins with non-positive excess return"] = int(n_nonpos_coins)
    counts["coins in record"] = len(coins)

    return {
        "status": status,
        "main_measure": {
            "name": "forward 5-bar return, top-quintile forecast minus zero-forecast bars",
            "value": value,
            "statistic": {"name": "Welch t", "value": tstat} if tstat is not None else None,
            "threshold": "excess above 0 with t >= 2 and positive in at least 2 of the 3 coins",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of forecast vs forward 5-bar return on positive-forecast bars",
            "value": rho,
            "passed": passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The top quintile is cut at the 80th percentile of all positive forecasts pooled across coins "
                    "and windows, the supporting check uses the same non-overlapping grid, and with only "
                    f"{len(coins)} coins in the record the 'at least 2 of the 3 coins' rules are applied to the "
                    "coins present."),
    }
