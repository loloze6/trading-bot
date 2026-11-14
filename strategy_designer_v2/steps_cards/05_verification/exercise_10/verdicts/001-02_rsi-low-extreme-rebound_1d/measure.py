import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_low.last_history_value"
    THRESH_TEXT = ("confirm if pooled t >= 2 and the supporting check holds; reject if pooled t <= -2; "
                   "otherwise inconclusive; at least 30 pooled non-overlapping top-quintile cases and at least 8 per coin")
    MAIN_NAME = "pooled mean 5-bar excess return (vs coin's window hold average) after top-quintile forecast bars"
    SUPPORT_NAME = "coins where top-quintile excess minus neutral excess > 0 (need >= 2)"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            # situation: RSI below 50  <=> raw (50 - RSI) * 0.4 > 0 ; expected side: long
            ok = act & (d[RAW] > 0) & (d["forecast"] > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": MAIN_NAME, "value": None, "statistic": None, "threshold": THRESH_TEXT},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have RSI below 50 with a long forecast, so the config's "
                           "positions do not follow the plan's situation (RSI low, long side)."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    pooled_top = []
    per_coin_top = {}
    per_coin_neutral = {}
    for coin, wins in bars.items():
        # top quintile threshold of the coin's non-zero forecasts, over all its windows
        fc_all = []
        for w, df in wins.items():
            f = df["forecast"].dropna()
            fc_all.append(f[f != 0].values)
        fc_all = np.concatenate(fc_all) if fc_all else np.array([])
        top_list, neu_list = [], []
        if len(fc_all) == 0:
            per_coin_top[coin] = top_list
            per_coin_neutral[coin] = neu_list
            continue
        q80 = float(np.quantile(fc_all, 0.8))
        for w, df in wins.items():
            close = df["close"].values.astype(float)
            fc = df["forecast"].values.astype(float)
            n = len(df)
            grid = np.arange(0, n, H)
            grid = grid[grid + H < n]
            rets, fcs = [], []
            for i in grid:
                c0, c1 = close[i], close[i + H]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                rets.append(c1 / c0 - 1.0)
                fcs.append(fc[i])
            if not rets:
                continue
            rets = np.array(rets)
            fcs = np.array(fcs)
            base = float(np.mean(rets))  # hold baseline: mean 5-bar return on the window's grid
            exc = rets - base
            valid = ~np.isnan(fcs)
            top_mask = valid & (fcs != 0) & (fcs >= q80)
            neu_mask = valid & (fcs == 0)
            top_list.extend(exc[top_mask].tolist())
            neu_list.extend(exc[neu_mask].tolist())
        per_coin_top[coin] = top_list
        per_coin_neutral[coin] = neu_list
        pooled_top.extend(top_list)

    pooled_top = np.array(pooled_top, dtype=float)
    n_pooled = int(len(pooled_top))
    counts = {"pooled top-quintile cases": n_pooled}
    for coin in per_coin_top:
        counts[f"top-quintile cases {coin}"] = int(len(per_coin_top[coin]))

    mean_exc = float(np.mean(pooled_top)) if n_pooled > 0 else None
    t = None
    if n_pooled > 1:
        sd = float(np.std(pooled_top, ddof=1))
        if sd > 0:
            t = float(mean_exc / (sd / np.sqrt(n_pooled)))

    # supporting check
    n_pos = 0
    any_diff = False
    for coin in per_coin_top:
        a, b = per_coin_top[coin], per_coin_neutral[coin]
        if len(a) > 0 and len(b) > 0:
            any_diff = True
            if np.mean(a) - np.mean(b) > 0:
                n_pos += 1
    support_passed = bool(n_pos >= 2) if any_diff else None
    supporting = {"name": SUPPORT_NAME, "value": float(n_pos) if any_diff else None, "passed": support_passed}

    reading = ("The top quintile is the coin's non-zero forecasts at or above their 80th percentile over all its windows; "
               "the hold baseline is the mean 5-bar return over the window's non-overlapping grid; the per-coin minimum "
               "of 8 and the '2 of 3 coins' rule are applied to the coins present in the record (BTC, ETH), so both must be positive.")

    statistic = {"name": "t of the mean", "value": t} if t is not None else None
    main = {"name": MAIN_NAME, "value": mean_exc, "statistic": statistic, "threshold": THRESH_TEXT}

    min_coin = min([len(v) for v in per_coin_top.values()]) if per_coin_top else 0
    if n_pooled < 30 or min_coin < 8 or t is None:
        if n_pooled < 30:
            why = f"Only {n_pooled} pooled non-overlapping top-quintile cases, fewer than the plan's minimum of 30."
        elif min_coin < 8:
            why = f"A coin has only {min_coin} top-quintile cases, fewer than the plan's minimum of 8 per coin."
        else:
            why = "The t-statistic could not be computed (zero variance)."
        return {"status": "not observable",
                "situation_check": {"agreement": agreement, "passed": True},
                "main_measure": main, "supporting_check": supporting,
                "counts": counts, "decided_by": why, "reading": reading}

    if t >= 2 and support_passed:
        status = "confirmed"
        why = f"Pooled t = {t:.2f} >= 2 and top-minus-neutral excess is positive in {n_pos} coins, meeting the confirm rule."
    elif t <= -2:
        status = "rejected"
        why = f"Pooled t = {t:.2f} <= -2: price keeps falling after low RSI, meeting the reject rule."
    else:
        status = "inconclusive"
        if t >= 2:
            why = f"Pooled t = {t:.2f} >= 2 but the supporting check fails ({n_pos} coins positive), so neither confirm nor reject holds."
        else:
            why = f"Pooled t = {t:.2f} lies between -2 and 2, the plan's inconclusive rule."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main, "supporting_check": supporting,
            "counts": counts, "decided_by": why, "reading": reading}
