import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    THRESH = -10.0
    MIN_CASES = 30
    RAW_COL = "debug_info.components.rsi_high.last_history_value"
    SCALING = 0.4

    # ---------- 1. Situation check: RSI(14) above 50, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            if RAW_COL not in df.columns or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            ok = fc.notna() & raw.notna()
            active = ok & (fc != 0)
            rsi = 50.0 - raw / SCALING
            situation = rsi > 50.0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "pooled excess forward 5-bar return after forecast <= -10 (vs coin-window mean)"
    threshold_txt = ("confirm: excess < 0 with t <= -2 and negative in at least 2 of 3 coins; "
                     "reject: excess > 0 with t >= +2; minimum 30 non-overlapping extreme cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a short position only while RSI(14) is above 50, "
                           "but fewer than 90% of the bars with a non-zero forecast are short bars with RSI above 50"
                           if n_active > 0 else
                           "The record has no active bars, so the config does not trade the plan's situation."),
            "reading": "Situation taken as RSI(14) > 50 with forecast < 0, RSI recovered as 50 - raw / 0.4.",
        }

    # ---------- 2. Criterion ----------
    pooled = []
    per_coin = {}
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            valid_fwd = np.isfinite(fwd)
            if not valid_fwd.any():
                continue
            baseline = float(np.mean(fwd[valid_fwd]))
            grid = np.arange(0, n, H)
            for i in grid:
                if np.isfinite(fc[i]) and fc[i] <= THRESH and np.isfinite(fwd[i]):
                    ex = fwd[i] - baseline
                    coin_vals.append(ex)
                    pooled.append(ex)
        per_coin[coin] = coin_vals

    pooled = np.asarray(pooled, dtype=float)
    n_cases = int(len(pooled))
    mean_ex = float(np.mean(pooled)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(pooled, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))
    n_coins = int(len(per_coin))
    coin_ok = n_neg_coins >= 2

    counts = {
        "pooled non-overlapping extreme cases": n_cases,
        "coins with negative excess": n_neg_coins,
        "coins in record": n_coins,
    }
    for c, v in per_coin.items():
        counts[f"extreme cases {c}"] = int(len(v))

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping extreme cases pooled, below the plan's minimum of 30."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2 and coin_ok:
        status = "confirmed"
        decided = "Pooled excess return is negative with t <= -2 and negative in at least 2 coins (confirm rule)."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided = "Pooled excess return is positive with t >= +2 (reject rule: continuation, not reversal)."
    else:
        status = "inconclusive"
        if t_stat is not None and t_stat <= -2 and not coin_ok:
            decided = "t <= -2 but the excess is negative in fewer than 2 coins, so neither confirm nor reject holds."
        else:
            decided = "t lies strictly between -2 and +2 (inconclusive rule)."

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
            "name": "number of coins with negative mean excess return (need >= 2)",
            "value": n_neg_coins,
            "passed": bool(coin_ok),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Extreme cases are grid bars (positions 0,5,10,... per window) with forecast <= -10 and a "
                    "defined in-window 5-bar forward return, the baseline is the mean forward 5-bar return over "
                    "all bars of that coin-window that have one, and with BNB absent the 'at least 2 of the 3 coins' "
                    "rule is applied literally as at least 2 negative coins among those present."),
    }
