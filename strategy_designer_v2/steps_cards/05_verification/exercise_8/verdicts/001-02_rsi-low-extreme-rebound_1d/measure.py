import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    VAL = "debug_info.components.rsi_low.last_history_value"

    # ---------- 1. Situation check: RSI below 50 (value > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", VAL]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            n_agree += int(((d[VAL] > 0) & (d["forecast"] > 0) & act).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled mean 5-bar excess return (vs window hold average) after top-quintile forecast bars"
    thr_words = ("confirm if t >= 2 and supporting check holds; reject if t <= -2; "
                 "inconclusive otherwise or if < 30 pooled top-quintile cases or < 8 per coin")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is RSI below 50 held long, but fewer than 90% of the "
                           "bars with a non-zero forecast are long bars with RSI below 50."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    pooled_top = []
    per_coin_top_n = {}
    coin_diffs = {}

    for coin, wins in bars.items():
        # top-quintile cut-off over this coin's non-zero forecasts, all windows
        nz = []
        for w, df in wins.items():
            f = df["forecast"].dropna()
            nz.append(f[f != 0].values)
        nz = np.concatenate(nz) if len(nz) else np.array([])
        if len(nz) == 0:
            per_coin_top_n[coin] = 0
            coin_diffs[coin] = None
            continue
        cut = np.quantile(nz, 0.8)

        top_ex, neu_ex = [], []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            base = fwd.dropna().mean()
            if not np.isfinite(base):
                continue
            excess = fwd - base
            grid = np.arange(0, len(df), H)
            g = pd.DataFrame({"f": df["forecast"].values[grid], "ex": excess.values[grid]}).dropna()
            top_ex.extend(g.loc[(g["f"] != 0) & (g["f"] >= cut), "ex"].tolist())
            neu_ex.extend(g.loc[g["f"] == 0, "ex"].tolist())

        per_coin_top_n[coin] = len(top_ex)
        pooled_top.extend(top_ex)
        if len(top_ex) > 0 and len(neu_ex) > 0:
            coin_diffs[coin] = float(np.mean(top_ex) - np.mean(neu_ex))
        else:
            coin_diffs[coin] = None

    pooled = np.array(pooled_top, dtype=float)
    n_pooled = int(len(pooled))
    mean_ex = float(pooled.mean()) if n_pooled > 0 else None
    if n_pooled > 1 and pooled.std(ddof=1) > 0:
        t = float(pooled.mean() / (pooled.std(ddof=1) / np.sqrt(n_pooled)))
    else:
        t = None

    n_pos = sum(1 for v in coin_diffs.values() if v is not None and v > 0)
    support_ok = bool(n_pos >= 2)

    counts = {"pooled non-overlapping top-quintile cases": n_pooled}
    for c, n in per_coin_top_n.items():
        counts[f"top-quintile cases {c}"] = int(n)
    counts["coins with positive top-minus-neutral excess"] = int(n_pos)

    enough = n_pooled >= 30 and all(n >= 8 for n in per_coin_top_n.values()) and len(per_coin_top_n) > 0

    if not enough or t is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 pooled non-overlapping top-quintile cases or fewer than 8 for some coin."
    elif t >= 2 and support_ok:
        status = "confirmed"
        decided = "Confirm: pooled mean excess after top-quintile positions has t >= 2 and the supporting check holds."
    elif t <= -2:
        status = "rejected"
        decided = "Reject: pooled mean excess after top-quintile positions has t <= -2."
    else:
        status = "inconclusive"
        decided = ("Inconclusive: t lies between -2 and 2, or t >= 2 but the supporting check "
                   "(positive in at least 2 coins) fails.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": thr_words,
        },
        "supporting_check": {
            "name": "coins with top-quintile minus neutral excess > 0 (need >= 2)",
            "value": float(n_pos),
            "passed": support_ok,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Top quintile is forecast >= the 80th percentile of each coin's non-zero forecasts over all "
                    "its windows, the hold baseline is the mean of all 5-bar forward returns in the same window, "
                    "and with only the coins present the supporting check still requires at least 2 positive coins."),
    }
