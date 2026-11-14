import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    THR = -10.0
    MIN_CASES = 30
    comp_col = "debug_info.components.rsi_high.last_history_value"
    scaling = 0.4

    # ---------- 1. Situation check: RSI(14) above 50 -> short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or comp_col not in df.columns:
                continue
            d = df[["forecast", comp_col]].dropna()
            fc = d["forecast"].astype(float).values
            raw = d[comp_col].astype(float).values
            rsi = 50.0 - raw / scaling
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & (rsi > 50.0) & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "pooled excess forward 5-bar return after forecast <= -10 (minus holding baseline)"
    threshold_txt = ("confirm: negative with t <= -2 and negative in >= 2 of 3 coins; "
                     "reject: positive with t >= +2; min 30 non-overlapping cases")
    reading = ("Holding baseline is the mean forward 5-bar return over all bars of the coin's window with a valid "
               "forward return (overlapping), extreme cases are the non-overlapping grid bars (positions 0,5,10,... "
               "of each window) with forecast <= -10, t is the ordinary t of the pooled mean, and a coin absent from "
               "the record or without cases counts as not negative among the plan's 3 coins.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are bars with RSI(14) above 50 carrying a short forecast, "
                           "so the config does not trade the plan's situation (high RSI, short side)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    pooled = []
    per_coin = {}
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid_fwd = fwd[~np.isnan(fwd)]
            if len(valid_fwd) == 0:
                continue
            base = float(np.mean(valid_fwd))
            for i in range(0, n, H):
                if np.isnan(fwd[i]) or np.isnan(fc[i]):
                    continue
                if fc[i] <= THR:
                    ex = fwd[i] - base
                    pooled.append(ex)
                    coin_vals.append(ex)
        per_coin[coin] = coin_vals

    pooled = np.array(pooled, dtype=float)
    n_cases = int(len(pooled))
    mean_ex = float(pooled.mean()) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(pooled.std(ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))
    support_passed = bool(n_neg_coins >= 2)

    counts = {
        "non-overlapping extreme cases pooled": n_cases,
        "coins with negative excess return": n_neg_coins,
        "coins in record": int(len(bars)),
    }

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = (f"Only {n_cases} non-overlapping extreme cases pooled, below the plan's minimum of 30.")
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2 and support_passed:
        status = "confirmed"
        decided = ("Pooled excess forward return is negative with t <= -2 and negative in at least 2 of the 3 coins.")
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided = "Pooled excess forward return is positive with t >= +2 (continuation, not reversal)."
    else:
        status = "inconclusive"
        if t_stat is not None and t_stat <= -2 and not support_passed:
            decided = ("t <= -2 but the excess return is negative in fewer than 2 of the 3 coins, so neither "
                       "the confirm nor the reject rule is met.")
        else:
            decided = "t lies strictly between -2 and +2, meeting the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "number of coins (of 3) with negative mean excess return",
            "value": n_neg_coins,
            "passed": support_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
