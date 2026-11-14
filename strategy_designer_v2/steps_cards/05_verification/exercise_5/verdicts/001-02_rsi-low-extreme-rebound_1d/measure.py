import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(n):
                fwd = np.nan
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                    fwd = close[i + H] / close[i] - 1.0
                rows.append({"coin": coin, "window": w, "pos": i, "forecast": fc[i],
                             "fwd": fwd, "grid": (i % H == 0)})
    data = pd.DataFrame(rows, columns=["coin", "window", "pos", "forecast", "fwd", "grid"])

    coins = sorted(bars.keys())
    n_coins = len(coins)

    # Top-quintile cut-off over all positive forecasts pooled across coins and windows
    pos_fc = data.loc[data["forecast"].notna() & (data["forecast"] > 0), "forecast"].values
    cutoff = float(np.quantile(pos_fc, 0.8)) if len(pos_fc) > 0 else np.nan

    valid = data[data["grid"] & data["forecast"].notna() & data["fwd"].notna()]
    top = valid[(valid["forecast"] > 0) & (valid["forecast"] >= cutoff)] if np.isfinite(cutoff) else valid.iloc[0:0]
    zero = valid[valid["forecast"] == 0]

    def diff_t(a, b):
        a = np.asarray(a, float)
        b = np.asarray(b, float)
        if len(a) < 1 or len(b) < 1:
            return None, None
        diff = float(a.mean() - b.mean())
        t = None
        if len(a) >= 2 and len(b) >= 2:
            tt = stats.ttest_ind(a, b, equal_var=False).statistic
            if np.isfinite(tt):
                t = float(tt)
        return diff, t

    excess, tstat = diff_t(top["fwd"].values, zero["fwd"].values)

    per_coin = {}
    per_coin_counts = {}
    for c in coins:
        d_c, _ = diff_t(top.loc[top["coin"] == c, "fwd"].values, zero.loc[zero["coin"] == c, "fwd"].values)
        per_coin[c] = d_c
        per_coin_counts[c] = int((top["coin"] == c).sum())

    n_pos_coins = sum(1 for c in coins if per_coin[c] is not None and per_coin[c] > 0)
    n_nonpos_coins = sum(1 for c in coins if per_coin[c] is not None and per_coin[c] <= 0)

    # Supporting check: Spearman on positive-forecast bars of the same non-overlapping grid
    posv = valid[valid["forecast"] > 0]
    rho = None
    passed = None
    if len(posv) >= 3 and posv["forecast"].nunique() > 1 and posv["fwd"].nunique() > 1:
        r = stats.spearmanr(posv["forecast"].values, posv["fwd"].values).correlation
        if np.isfinite(r):
            rho = float(r)
            passed = bool(rho > 0)

    n_top = int(len(top))
    min_coin = min(per_coin_counts.values()) if per_coin_counts else 0

    if n_top < 30 or min_coin < 8 or excess is None:
        status = "inconclusive"
        decided = ("Inconclusive: fewer than 30 pooled non-overlapping top-quintile cases or fewer than 8 for at least one coin "
                   f"(pooled {n_top}, smallest coin {min_coin}).")
    elif excess > 0 and tstat is not None and tstat >= 2 and n_pos_coins >= 2:
        status = "confirmed"
        decided = "Confirm: pooled excess return above 0 with Welch t of at least 2 and positive in at least 2 coins."
    elif excess <= 0 and n_nonpos_coins >= 2:
        status = "rejected"
        decided = "Reject: pooled excess return at or below 0 and non-positive in at least 2 coins."
    else:
        status = "inconclusive"
        if excess > 0 and (tstat is None or tstat < 2):
            decided = "Inconclusive: positive pooled excess return with a t-statistic below 2."
        else:
            decided = "Inconclusive: coins disagree beyond the confirm/reject rules."

    counts = {"non-overlapping top-quintile cases pooled": n_top,
              "non-overlapping zero-forecast cases pooled": int(len(zero)),
              "coins": n_coins,
              "coins with positive excess": n_pos_coins,
              "coins with non-positive excess": n_nonpos_coins}
    for c in coins:
        counts[f"non-overlapping top-quintile cases {c}"] = per_coin_counts[c]

    return {
        "status": status,
        "main_measure": {
            "name": "Top-quintile minus zero-forecast mean forward 5-bar return (non-overlapping, pooled)",
            "value": excess,
            "statistic": ({"name": "Welch t", "value": tstat} if tstat is not None else None),
            "threshold": "excess > 0 with t >= 2 and positive in at least 2 of the coins to confirm; <= 0 and non-positive in at least 2 coins to reject",
        },
        "supporting_check": {"name": "Spearman rank correlation of forecast vs forward 5-bar return on positive-forecast bars",
                             "value": rho, "passed": passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The top-quintile cut-off is the 80th percentile of all positive forecasts pooled across coins and windows, "
                    "both groups and the Spearman check use the bars at positions 0,5,10,... of each window, and since only "
                    f"{n_coins} coins are in the record the 'at least 2 of the 3 coins' rules are applied as at least 2 of the coins present "
                    "and the per-coin minimum of 8 to each coin present."),
    }
