import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_high.last_history_value"

    # ---------- 1. Situation check: short while RSI(14) > 50 (raw value < 0) ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            active = d["forecast"] != 0
            n_active += int(active.sum())
            raw = d[RAW].astype(float)
            rsi = 50.0 - raw / 0.4
            agree = active & (rsi > 50.0) & (d["forecast"] < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a short position only while RSI(14) is above 50, "
                           "but fewer than 90% of the bars with a non-zero forecast are short bars with RSI above 50."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    pooled = []
    per_coin = {}
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            fwd_s = pd.Series(fwd)
            base = fwd_s.dropna()
            if len(base) == 0:
                continue
            baseline = float(base.mean())
            fc = d["forecast"].astype(float)
            grid = np.zeros(n, dtype=bool)
            grid[::H] = True
            sel = grid & (fc <= -10).values & ~np.isnan(fwd)
            ex = fwd[sel] - baseline
            coin_vals.extend(ex.tolist())
            pooled.extend(ex.tolist())
        per_coin[coin] = coin_vals

    pooled = np.asarray(pooled, dtype=float)
    n_cases = int(len(pooled))
    mean_ex = float(pooled.mean()) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(pooled.std(ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))
    coin_ok = n_neg_coins >= 2

    if n_cases < 30 or t_stat is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 non-overlapping extreme cases pooled (or no t-statistic could be computed)."
    elif mean_ex < 0 and t_stat <= -2 and coin_ok:
        status = "confirmed"
        decided = ("Confirm: the pooled excess forward 5-bar return is negative with t <= -2 "
                   "and negative in at least 2 coins.")
    elif mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided = "Reject: the pooled excess forward 5-bar return is positive with t >= +2 (continuation)."
    elif -2 < t_stat < 2:
        status = "inconclusive"
        decided = "Inconclusive: the pooled t is strictly between -2 and +2."
    else:
        status = "inconclusive"
        decided = ("Inconclusive: t <= -2 on a negative pooled excess return, but fewer than 2 coins show "
                   "a negative excess return, so the confirm rule is not met.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled excess forward 5-bar return after forecast <= -10 vs holding baseline",
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": "confirm if negative with t <= -2 (and negative in >= 2 coins); reject if positive with t >= +2; minimum 30 cases",
        },
        "supporting_check": {
            "name": "number of coins with negative excess return",
            "value": n_neg_coins,
            "passed": bool(coin_ok),
        },
        "counts": {
            "non-overlapping extreme cases pooled": n_cases,
            "coins with negative excess return": n_neg_coins,
            "coins in record": int(len(per_coin)),
        },
        "decided_by": decided,
        "reading": ("Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10, the baseline "
                    "is the mean forward 5-bar return over all bars of that coin and window with a forward return, the "
                    "t is the ordinary t of the pooled mean, and the 'at least 2 of the 3 coins' rule is applied as at "
                    "least 2 negative coins among those present in the record."),
    }
