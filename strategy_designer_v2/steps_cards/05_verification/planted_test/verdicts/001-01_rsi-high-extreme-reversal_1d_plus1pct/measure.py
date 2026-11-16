import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP = "debug_info.components.rsi_high.last_history_value"
    SCALE = 0.4
    THRESH_FC = -10.0
    MIN_CASES = 30
    MIN_NEG_COINS = 2

    # ---------- 1. Situation check: short while RSI(14) > 50 ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[COMP], errors="coerce") if COMP in df.columns else pd.Series(np.nan, index=df.index)
            rsi = 50.0 - raw / SCALE
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & rsi.notna() & (rsi > 50.0) & (fc < 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled excess forward 5-bar return after forecast <= -10 vs holding baseline"
    threshold_words = ("confirm if pooled excess < 0 with t <= -2 and negative in >= 2 of 3 coins; "
                       "reject if pooled excess > 0 with t >= +2; inconclusive otherwise or if < 30 cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a short position only while RSI(14) is above 50, but fewer than 90% "
                           "of the bars with a non-zero forecast are short bars with RSI above 50."),
            "reading": "RSI is recovered as 50 - last_history_value / 0.4 and the situation is RSI > 50 with forecast < 0.",
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
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            base_vals = fwd.dropna()
            if len(base_vals) == 0:
                continue
            baseline = float(base_vals.mean())
            grid = np.arange(len(df)) % H == 0
            sel = grid & fc.notna().values & (fc.values <= THRESH_FC) & fwd.notna().values
            ex = (fwd.values[sel] - baseline).tolist()
            coin_vals.extend(ex)
            pooled.extend(ex)
        per_coin[coin] = coin_vals

    pooled = np.asarray(pooled, dtype=float)
    n = int(len(pooled))
    mean_ex = float(pooled.mean()) if n > 0 else None
    t_stat = None
    if n >= 2:
        sd = float(pooled.std(ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for v in coin_means.values() if v is not None and v < 0))
    coins_present = int(len(per_coin))
    support_passed = bool(n_neg_coins >= MIN_NEG_COINS)

    if n < MIN_CASES:
        status = "inconclusive"
        decided = f"Fewer than 30 non-overlapping extreme cases pooled ({n}), so the plan's inconclusive rule applies."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (zero dispersion), so no confirm or reject rule is met."
    elif mean_ex < 0 and t_stat <= -2 and support_passed:
        status = "confirmed"
        decided = "The pooled excess forward return is negative with t <= -2 and negative in at least 2 coins, meeting the confirm rule."
    elif mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided = "The pooled excess forward return is positive with t >= +2, meeting the reject rule (continuation, not reversal)."
    elif -2 < t_stat < 2:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and +2, meeting the inconclusive rule."
    else:
        status = "inconclusive"
        decided = ("The pooled excess is negative with t <= -2 but negative in fewer than 2 coins, so neither confirm "
                   "nor reject is met.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold_words,
        },
        "supporting_check": {
            "name": "number of coins with negative mean excess forward return (need >= 2)",
            "value": n_neg_coins,
            "passed": support_passed,
        },
        "counts": {
            "non-overlapping extreme cases pooled": n,
            "coins with negative excess": n_neg_coins,
            "coins present": coins_present,
        },
        "decided_by": decided,
        "reading": ("The baseline is the mean forward 5-bar return over all bars of each coin and window, the extreme cases are "
                    "grid bars at positions 0,5,10,... with forecast <= -10, the t is the ordinary t of the pooled mean, and "
                    "'at least 2 of the 3 coins' is applied as at least 2 negative coins among the coins present, with a "
                    "negative t <= -2 lacking that coin support treated as inconclusive."),
    }
