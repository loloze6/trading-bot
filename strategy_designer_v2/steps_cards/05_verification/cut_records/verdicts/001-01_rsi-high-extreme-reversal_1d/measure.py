import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP = "debug_info.components.rsi_high.last_history_value"
    SCALE = 0.4

    # ---------- 1. Situation check: RSI(14) above 50, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or COMP not in df.columns:
                continue
            sub = df[["forecast", COMP]].dropna()
            active = sub[sub["forecast"] != 0]
            if len(active) == 0:
                continue
            rsi = 50.0 - active[COMP].astype(float) / SCALE
            ok = (rsi > 50.0) & (active["forecast"] < 0)
            n_active += int(len(active))
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (
                "No active bars in the record, so the short-while-RSI-above-50 situation cannot be matched."
                if agreement is None else
                "Fewer than 90% of the bars with a non-zero forecast are short bars with RSI(14) above 50, "
                "so the config does not do what the plan's Fidelity describes."
            ),
            "reading": "Situation taken as RSI(14) > 50 (component raw value < 0) with a negative forecast.",
        }

    # ---------- 2. Criterion ----------
    pooled = []
    per_coin = {}
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0  # inside this window only
            baseline = fwd.dropna()
            if len(baseline) == 0:
                continue
            base_mean = float(baseline.mean())
            grid = np.arange(0, len(d), H)
            fc = d["forecast"].astype(float)
            for i in grid:
                f = fc.iloc[i]
                r = fwd.iloc[i]
                if pd.isna(f) or pd.isna(r):
                    continue
                if f <= -10:
                    ex = float(r) - base_mean
                    pooled.append(ex)
                    coin_vals.append(ex)
        per_coin[coin] = coin_vals

    n = len(pooled)
    mean_ex = float(np.mean(pooled)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(pooled, ddof=1))
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(n)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for v in coin_means.values() if v is not None and v < 0))
    support_pass = n_neg_coins >= 2

    reading = ("Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10 and a defined "
               "5-bar forward return, the baseline is the mean 5-bar forward return over all bars of that coin and "
               "window with a defined forward return, t is the ordinary t of the pooled mean, and the 'at least 2 of "
               "the 3 coins' rule is applied literally to the coins present, so with fewer than 2 negative coins it "
               "cannot be met.")

    main = {
        "name": "pooled excess forward 5-bar return after forecast <= -10",
        "value": mean_ex,
        "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
        "threshold": "confirm if negative with t <= -2 (and negative in >= 2 of 3 coins); reject if positive with t >= +2",
    }
    supporting = {
        "name": "number of coins with negative excess return",
        "value": n_neg_coins,
        "passed": bool(support_pass),
    }
    counts = {"non-overlapping extreme cases pooled": int(n),
              "coins with extreme cases": int(sum(1 for v in per_coin.values() if len(v) > 0))}

    if n < 30 or t is None:
        status = "not observable"
        decided = (f"Only {n} non-overlapping extreme cases pooled, below the plan's minimum of 30."
                   if n < 30 else "The t-statistic could not be computed (zero dispersion).")
    elif mean_ex < 0 and t <= -2 and support_pass:
        status = "confirmed"
        decided = "Pooled excess return negative with t <= -2 and negative in at least 2 coins (confirm rule)."
    elif mean_ex > 0 and t >= 2:
        status = "rejected"
        decided = "Pooled excess return positive with t >= +2 (reject rule: continuation, not reversal)."
    else:
        status = "inconclusive"
        if -2 < t < 2:
            decided = "t lies strictly between -2 and +2 (inconclusive rule)."
        else:
            decided = ("t <= -2 but the excess return is negative in fewer than 2 of the 3 coins, "
                       "so neither the confirm nor the reject rule is met.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
