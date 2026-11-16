import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 12
    RAW = "debug_info.components.rsi_high.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            # RSI = 50 - raw/0.4 > 50  <=> raw < 0 ; expected side short <=> forecast < 0
            ok = act & (d[RAW] < 0) & (d["forecast"] < 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean forward 12-bar log excess return after top-decile |forecast| bars",
                             "value": None, "statistic": None,
                             "threshold": "confirm: negative with t <= -2 and negative in >= 2 coins; reject: positive with t >= +2"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation (RSI above 50, short side) holds on fewer than 90% of the bars "
                           "where the config's forecast is active, so the config does not implement the planned situation."),
            "reading": "Situation taken as raw RSI-pullback value < 0 (RSI > 50) with forecast < 0 on bars with forecast != 0.",
        }

    # ---------- 2. build per-bar records ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                with np.errstate(divide="ignore", invalid="ignore"):
                    fwd[: n - H] = np.log(close[H:] / close[: n - H])
            fwd[~np.isfinite(fwd)] = np.nan
            drift = np.nanmean(fwd) if np.isfinite(fwd).any() else np.nan
            pos = np.arange(n)
            rows.append(pd.DataFrame({
                "coin": coin, "window": w,
                "absf": d["forecast"].astype(float).abs().values,
                "fwd": fwd,
                "excess": fwd - drift,
                "grid": (pos % H) == 0,
            }))
    all_df = pd.concat(rows, ignore_index=True)
    all_df = all_df.dropna(subset=["absf", "excess"])

    # top decile of |forecast| over all pooled bars (and non-zero)
    q90 = float(np.quantile(all_df["absf"].values, 0.9)) if len(all_df) else np.nan
    all_df["extreme"] = (all_df["absf"] >= q90) & (all_df["absf"] > 0)

    ext = all_df[all_df["extreme"] & all_df["grid"]]
    x = ext["excess"].values
    n_pool = int(len(x))
    if n_pool >= 2 and np.std(x, ddof=1) > 0:
        mean_ex = float(np.mean(x))
        t_val = float(mean_ex / (np.std(x, ddof=1) / np.sqrt(n_pool)))
    else:
        mean_ex = float(np.mean(x)) if n_pool else None
        t_val = None

    coins = sorted(bars.keys())
    per_coin_n = {}
    per_coin_mean = {}
    for c in coins:
        xc = ext.loc[ext["coin"] == c, "excess"].values
        per_coin_n[c] = int(len(xc))
        per_coin_mean[c] = float(np.mean(xc)) if len(xc) else np.nan
    coins_neg = int(sum(1 for c in coins if np.isfinite(per_coin_mean[c]) and per_coin_mean[c] < 0))

    # ---------- 3. supporting check ----------
    nz = all_df[all_df["absf"] > 0]
    sup_value = None
    sup_passed = None
    if len(nz) >= 5:
        edges = np.quantile(nz["absf"].values, [0.2, 0.4, 0.6, 0.8])
        grp = np.where(all_df["absf"].values == 0, 0,
                       1 + np.searchsorted(edges, all_df["absf"].values, side="left"))
        grp = np.clip(grp, 0, 5)
        all_df["grp"] = grp
        g = all_df[all_df["grid"]]

        def group_means(sub):
            return [float(sub.loc[sub["grp"] == k, "excess"].mean()) if (sub["grp"] == k).any() else np.nan
                    for k in range(6)]

        pm = group_means(g)
        if all(np.isfinite(pm)):
            steady = all(pm[k + 1] < pm[k] for k in range(5))
            rho = float(stats.spearmanr(np.arange(6), pm).correlation)
            sup_value = rho
            coin_neg_slope = 0
            for c in coins:
                cm = group_means(g[g["coin"] == c])
                if all(np.isfinite(cm)):
                    r = stats.spearmanr(np.arange(6), cm).correlation
                    if np.isfinite(r) and r < 0:
                        coin_neg_slope += 1
            sup_passed = bool(steady and coin_neg_slope >= 2)

    # ---------- 4. decision ----------
    enough = (n_pool >= 100) and all(per_coin_n[c] >= 30 for c in coins)
    if not enough or t_val is None:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme episodes per coin or fewer than 100 pooled, so the test is inconclusive whatever the t."
    elif mean_ex < 0 and t_val <= -2 and coins_neg >= 2:
        status = "confirmed"
        decided = "The pooled excess return after extreme bars is negative with t <= -2 and negative in at least 2 coins."
    elif mean_ex > 0 and t_val >= 2:
        status = "rejected"
        decided = "The pooled excess return after extreme bars is positive with t >= +2 (continuation rather than give-back)."
    elif t_val <= -2:
        status = "inconclusive"
        decided = "Pooled t <= -2 but fewer than 2 coins agree in sign."
    else:
        status = "inconclusive"
        decided = "The pooled t lies between -2 and +2."

    counts = {"pooled non-overlapping extreme episodes": n_pool}
    for c in coins:
        counts[f"non-overlapping extreme episodes {c}"] = per_coin_n[c]
    counts["coins with negative excess"] = coins_neg
    counts["coins in record"] = len(coins)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean forward 12-bar log excess return after top-decile |forecast| bars",
            "value": mean_ex,
            "statistic": {"name": "t of the mean on non-overlapping 12-bar blocks", "value": t_val} if t_val is not None else None,
            "threshold": "confirm: negative with t <= -2 and negative in >= 2 coins; reject: positive with t >= +2; else inconclusive; needs >= 30 episodes per coin and >= 100 pooled",
        },
        "supporting_check": {
            "name": "excess return falls steadily from zero-forecast group through |forecast| quintiles (Spearman rho), same sign in >= 2 coins",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Top decile is the pooled 90th percentile of |forecast| over all bars of all coins and windows (non-zero only), "
                    "excess is each bar's forward 12-bar log return minus its coin-window mean over all bars, sampled on the 0,12,24,... grid "
                    "with the ordinary t of the mean; with only 2 coins in the record, 'at least 2 of 3 coins' is read as both coins, and "
                    "'fall steadily' as strictly decreasing pooled means over neutral then quintiles 1-5, with a negative per-coin Spearman slope in at least 2 coins."),
    }
