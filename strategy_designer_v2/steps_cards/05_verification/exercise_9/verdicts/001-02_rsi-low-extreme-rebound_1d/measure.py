import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_low.last_history_value"

    # ---------- 1. Situation check: RSI below 50 (raw > 0), expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            n_agree += int((act & (d[RAW] > 0) & (d["forecast"] > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars where RSI14 is below 50 "
                          "with a long forecast, so the config does not trade the plan's situation on its side.",
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    pooled_top = []
    per_coin_top = {}
    per_coin_zero = {}

    for coin, wins in bars.items():
        # top quintile threshold of this coin's non-zero forecasts, all its windows together
        fc_all = pd.concat([df["forecast"] for df in wins.values()]).dropna()
        nz = fc_all[fc_all != 0]
        thr = float(np.quantile(nz.values, 0.8)) if len(nz) > 0 else np.inf

        top_ex, zero_ex = [], []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            grid = np.arange(0, len(df), H)
            g = pd.DataFrame({"fc": df["forecast"].values[grid], "r": fwd.values[grid]}).dropna()
            if len(g) == 0:
                continue
            base = g["r"].mean()  # hold baseline: the window's average non-overlapping 5-bar return
            ex = g["r"] - base
            top_mask = (g["fc"] != 0) & (g["fc"] >= thr)
            zero_mask = g["fc"] == 0
            top_ex.extend(ex[top_mask].tolist())
            zero_ex.extend(ex[zero_mask].tolist())
        per_coin_top[coin] = top_ex
        per_coin_zero[coin] = zero_ex
        pooled_top.extend(top_ex)

    n_pooled = len(pooled_top)
    counts = {"pooled non-overlapping top-quintile cases": int(n_pooled)}
    for coin in per_coin_top:
        counts[f"{coin} top-quintile cases"] = int(len(per_coin_top[coin]))

    arr = np.asarray(pooled_top, dtype=float)
    mean_ex = float(arr.mean()) if n_pooled > 0 else None
    if n_pooled > 1 and arr.std(ddof=1) > 0:
        t = float(arr.mean() / (arr.std(ddof=1) / np.sqrt(n_pooled)))
    else:
        t = None

    # supporting check: top-quintile excess minus neutral excess > 0 in at least 2 coins
    n_pos = 0
    for coin in per_coin_top:
        a, b = per_coin_top[coin], per_coin_zero[coin]
        if len(a) > 0 and len(b) > 0 and (np.mean(a) - np.mean(b)) > 0:
            n_pos += 1
    support_ok = bool(n_pos >= 2)

    main = {
        "name": "pooled mean 5-bar excess return after top-quintile forecasts (vs window hold average)",
        "value": mean_ex,
        "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
        "threshold": "confirm if t >= 2 with the supporting check; reject if t <= -2",
    }
    supp = {
        "name": "coins where top-quintile excess minus neutral excess > 0 (need >= 2)",
        "value": int(n_pos),
        "passed": support_ok,
    }
    reading = ("Top quintile is the 80th percentile of each coin's non-zero forecasts across all its windows, the hold "
               "baseline is the mean non-overlapping 5-bar return of the same window, and with only BTC and ETH in the "
               "record the per-coin minimum applies to these two coins and the supporting check needs both of them positive.")

    low_coins = [c for c in per_coin_top if len(per_coin_top[c]) < 8]
    if n_pooled < 30 or low_coins or t is None:
        status = "not observable"
        if n_pooled < 30:
            decided = f"Only {n_pooled} pooled non-overlapping top-quintile cases, below the plan's minimum of 30."
        elif low_coins:
            decided = f"Fewer than 8 top-quintile cases for {', '.join(low_coins)}, below the plan's per-coin minimum."
        else:
            decided = "The t-statistic could not be computed (zero dispersion)."
    elif t >= 2 and support_ok:
        status = "confirmed"
        decided = "Pooled mean excess after top-quintile positions has t >= 2 and the supporting check holds."
    elif t <= -2:
        status = "rejected"
        decided = "Pooled mean excess after top-quintile positions has t <= -2: price keeps falling after low RSI."
    else:
        status = "inconclusive"
        if t >= 2:
            decided = "t >= 2 but the supporting check fails, so neither the confirm nor the reject rule is met."
        else:
            decided = "The pooled t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
