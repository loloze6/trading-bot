import numpy as np
import pandas as pd


def measure(bars):
    H = 12
    VAL = "debug_info.components.rsi_high.last_history_value"
    SCALE = 0.4
    THRESH_WORDS = ("confirm: pooled excess < 0 with t <= -2 and negative in >= 2 coins; "
                    "reject: pooled excess > 0 with t >= +2; needs >= 30 non-overlapping "
                    "extreme episodes per coin and >= 100 pooled")

    def _f(x):
        return None if x is None or not np.isfinite(x) else float(x)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["_coin"] = coin
            d["_win"] = w
            d["_pos"] = np.arange(len(d))
            c = d["close"].astype(float).values
            fwd = np.full(len(d), np.nan)
            if len(d) > H:
                fwd[:-H] = np.log(c[H:] / c[:-H])
            d["_fwd"] = fwd
            fc = d["forecast"].astype(float)
            raw = d[VAL].astype(float) if VAL in d.columns else pd.Series(np.nan, index=d.index)
            rsi = 50.0 - raw / SCALE
            act = fc.notna() & (fc != 0)
            n_active += int(act.sum())
            # Situation: RSI above 50; expected side: short
            n_agree += int((act & (rsi > 50) & (fc < 0)).sum())
            drift = np.nanmean(fwd) if np.isfinite(fwd).any() else np.nan
            d["_ex"] = d["_fwd"] - drift
            frames.append(d)

    agreement = n_agree / n_active if n_active > 0 else 0.0
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean fwd 12-bar log return after top-decile |forecast| minus drift",
                             "value": None, "statistic": None, "threshold": THRESH_WORDS},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short positions taken while RSI is above 50, "
                           "so the config does not implement the plan's situation and side."),
            "reading": "Situation taken as RSI > 50 (raw component value < 0) with a negative forecast.",
        }

    allb = pd.concat(frames, ignore_index=True)
    allb["_abs"] = allb["forecast"].astype(float).abs()

    # ---------- 2. main measure ----------
    valid_f = allb["_abs"].dropna()
    q90 = float(np.quantile(valid_f.values, 0.9)) if len(valid_f) else np.nan
    extreme = (allb["_abs"] >= q90) & (allb["_abs"] > 0)
    grid = (allb["_pos"] % H == 0)
    ext_grid = allb[extreme & grid & allb["_ex"].notna()]

    x = ext_grid["_ex"].values.astype(float)
    n_pool = len(x)
    mean_pool = float(np.mean(x)) if n_pool > 0 else np.nan
    t_pool = (mean_pool / (np.std(x, ddof=1) / np.sqrt(n_pool))
              if n_pool > 1 and np.std(x, ddof=1) > 0 else np.nan)

    coins = list(bars.keys())
    per_coin_n = {}
    per_coin_mean = {}
    for coin in coins:
        xc = ext_grid.loc[ext_grid["_coin"] == coin, "_ex"].values
        per_coin_n[coin] = int(len(xc))
        per_coin_mean[coin] = float(np.mean(xc)) if len(xc) else np.nan
    coins_neg = sum(1 for c in coins if np.isfinite(per_coin_mean[c]) and per_coin_mean[c] < 0)

    # ---------- 3. supporting check ----------
    sup = allb[allb["_ex"].notna() & allb["_abs"].notna()].copy()
    sup_value = None
    sup_pass = None
    nz = sup[sup["_abs"] > 0]
    if len(nz) >= 5:
        try:
            sup.loc[nz.index, "_grp"] = pd.qcut(nz["_abs"], 5, labels=False, duplicates="drop") + 1
        except ValueError:
            sup.loc[nz.index, "_grp"] = np.nan
        sup.loc[sup["_abs"] == 0, "_grp"] = 0
        g = sup.dropna(subset=["_grp"]).groupby("_grp")["_ex"].mean().sort_index()
        if len(g) >= 2:
            steady = bool(np.all(np.diff(g.values) < 0))
            top = g.index.max()
            sign_coins = 0
            for coin in coins:
                sc = sup[(sup["_coin"] == coin) & (sup["_grp"] == top)]["_ex"]
                if len(sc) and sc.mean() < 0:
                    sign_coins += 1
            sup_value = float(g.loc[top] - g.loc[g.index.min()])
            sup_pass = bool(steady and sign_coins >= 2)

    # ---------- 4. decision ----------
    enough = n_pool >= 100 and all(per_coin_n[c] >= 30 for c in coins)
    if not enough:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme episodes in some coin or fewer than 100 pooled, so the test is inconclusive whatever the t."
    elif np.isfinite(t_pool) and t_pool <= -2 and mean_pool < 0 and coins_neg >= 2:
        status = "confirmed"
        decided = "The pooled excess return after extreme bars is negative with t <= -2 and negative in at least 2 coins."
    elif np.isfinite(t_pool) and t_pool >= 2 and mean_pool > 0:
        status = "rejected"
        decided = "The pooled excess return after extreme bars is positive with t >= +2 (continuation rather than give-back)."
    elif np.isfinite(t_pool) and t_pool <= -2:
        status = "inconclusive"
        decided = "Pooled t <= -2 but fewer than 2 coins agree in sign."
    else:
        status = "inconclusive"
        decided = "Pooled t lies between -2 and +2."

    counts = {"pooled non-overlapping extreme episodes": int(n_pool),
              "coins with negative excess": int(coins_neg)}
    for c in coins:
        counts[f"non-overlapping extreme episodes {c}"] = per_coin_n[c]

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean fwd 12-bar log return after top-decile |forecast| minus drift",
                         "value": _f(mean_pool),
                         "statistic": {"name": "t of the mean on non-overlapping 12-bar blocks",
                                       "value": _f(t_pool)} if np.isfinite(t_pool) else None,
                         "threshold": THRESH_WORDS},
        "supporting_check": {"name": "excess return falls across |forecast| quintiles (top minus neutral)",
                             "value": sup_value, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Top decile is |forecast| >= its 90th percentile over all pooled bars (nonzero only), the drift "
                    "is the mean forward 12-bar log return of all bars of the same coin and window, extreme "
                    "episodes are extreme bars on the 0,12,24,... grid of each window, the supporting check uses "
                    "all bars with zero-forecast bars as group 0 and needs a strictly falling mean plus a negative "
                    "top-quintile excess in at least 2 coins, and with only the coins present the rule "
                    "'at least 2 of 3 coins' is applied as at least 2 coins."),
    }
