import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    coin_top = {}
    coin_neu = {}
    pos_f, pos_r = [], []

    for coin in sorted(bars.keys()):
        frames = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            d = df[["close", "forecast"]].copy().reset_index(drop=True)
            d["fwd"] = d["close"].shift(-H) / d["close"] - 1.0
            d["grid"] = (np.arange(len(d)) % H) == 0
            frames.append(d)
        if not frames:
            continue
        allc = pd.concat(frames, ignore_index=True)

        # Top-quintile cutoff over all of this coin's positive forecasts (every window, every row).
        pos_all = allc["forecast"].dropna()
        pos_all = pos_all[pos_all > 0]
        cut = float(np.quantile(pos_all.values, 0.8)) if len(pos_all) > 0 else np.inf

        g = allc[allc["grid"]].dropna(subset=["forecast", "fwd"])
        top = g[(g["forecast"] > 0) & (g["forecast"] >= cut)]["fwd"].values
        neu = g[g["forecast"] == 0]["fwd"].values
        coin_top[coin] = top
        coin_neu[coin] = neu

        pp = g[g["forecast"] > 0]
        pos_f.extend(pp["forecast"].tolist())
        pos_r.extend(pp["fwd"].tolist())

    coins = list(coin_top.keys())

    def _arr(d):
        vals = [d[c] for c in coins if len(d[c])]
        return np.concatenate(vals) if vals else np.array([])

    all_top = _arr(coin_top)
    all_neu = _arr(coin_neu)

    diff, tstat = None, None
    if len(all_top) > 0 and len(all_neu) > 0:
        diff = float(np.mean(all_top) - np.mean(all_neu))
        if len(all_top) >= 2 and len(all_neu) >= 2:
            t = stats.ttest_ind(all_top, all_neu, equal_var=False).statistic
            tstat = float(t) if np.isfinite(t) else None

    coin_diff = {}
    for c in coins:
        if len(coin_top[c]) > 0 and len(coin_neu[c]) > 0:
            coin_diff[c] = float(np.mean(coin_top[c]) - np.mean(coin_neu[c]))
        else:
            coin_diff[c] = None
    n_pos_coins = sum(1 for v in coin_diff.values() if v is not None and v > 0)
    n_nonpos_coins = sum(1 for v in coin_diff.values() if v is not None and v <= 0)

    rho = None
    if len(pos_f) >= 3:
        r = stats.spearmanr(pos_f, pos_r).correlation
        rho = float(r) if np.isfinite(r) else None
    supp_passed = None if rho is None else bool(rho > 0)

    counts = {"pooled non-overlapping top-quintile cases": int(len(all_top)),
              "pooled non-overlapping neutral cases": int(len(all_neu))}
    for c in coins:
        counts[f"top-quintile cases {c}"] = int(len(coin_top[c]))
        counts[f"neutral cases {c}"] = int(len(coin_neu[c]))
    counts["coins with positive excess return"] = int(n_pos_coins)
    counts["coins with non-positive excess return"] = int(n_nonpos_coins)
    counts["coins in record"] = int(len(coins))

    min_coin = min((len(coin_top[c]) for c in coins), default=0)
    if len(all_top) < 30 or min_coin < 8 or len(coins) == 0:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 pooled non-overlapping top-quintile cases or fewer than 8 for at least one coin."
    elif diff is None:
        status = "inconclusive"
        decided = "Inconclusive: the excess return could not be computed (no neutral samples)."
    elif diff > 0 and tstat is not None and tstat >= 2 and n_pos_coins >= 2:
        status = "confirmed"
        decided = "Confirmed: pooled excess return above 0 with Welch t of at least 2 and positive in at least 2 coins."
    elif diff <= 0 and n_nonpos_coins >= 2:
        status = "rejected"
        decided = "Rejected: pooled excess return at or below 0 and non-positive in at least 2 coins."
    else:
        status = "inconclusive"
        decided = "Inconclusive: positive excess return with t below 2, or coins disagree beyond the confirm/reject rules."

    return {
        "status": status,
        "main_measure": {
            "name": "top-quintile minus neutral mean forward 5-bar return",
            "value": diff,
            "statistic": None if tstat is None else {"name": "Welch t", "value": tstat},
            "threshold": "excess return above 0 with t of at least 2, positive in at least 2 of the 3 coins",
        },
        "supporting_check": {
            "name": "Spearman rank correlation forecast vs forward 5-bar return (positive forecasts)",
            "value": rho,
            "passed": supp_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Top quintile is set per coin as forecast at or above the 80th percentile of that coin's positive forecasts over all its rows and windows; the forward 5-bar returns are taken on the per-window grid 0,5,10,... (as is the supporting correlation); and because only "
                    + str(len(coins)) + " of the plan's 3 coins are in the record, the 'at least 2 coins' rules are applied to the coins present."),
    }
