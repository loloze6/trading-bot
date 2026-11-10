import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_high.last_history_value"

    # ---------- 1. Situation check: short only while RSI(14) > 50 ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            active = d["forecast"] != 0
            raw = d.loc[active, RAW]
            fc = d.loc[active, "forecast"]
            # RSI = 50 - raw/0.4 ; RSI > 50  <=>  raw < 0
            rsi = 50.0 - raw / 0.4
            ok = (rsi > 50.0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a short position only while RSI(14) is above 50, "
                           "but fewer than 90% of the active forecast bars are short bars with RSI above 50."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    pooled = []
    per_coin = {}
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0  # within this window only
            baseline = fwd.dropna().mean()  # holding baseline: all bars of coin/window
            if not np.isfinite(baseline):
                continue
            grid = np.arange(0, len(df), H)
            sub = pd.DataFrame({"forecast": df["forecast"].iloc[grid].values,
                                "fwd": fwd.iloc[grid].values}).dropna()
            ext = sub[sub["forecast"] <= -10]
            ex = (ext["fwd"] - baseline).tolist()
            coin_vals.extend(ex)
            pooled.extend(ex)
        per_coin[coin] = coin_vals

    pooled = np.asarray(pooled, dtype=float)
    n = int(len(pooled))
    mean_ex = float(pooled.mean()) if n > 0 else None
    if n > 1:
        sd = pooled.std(ddof=1)
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        t = None

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))
    support_passed = n_neg_coins >= 2

    if n < 30 or t is None:
        status = "inconclusive"
        decided_by = "Fewer than 30 non-overlapping extreme cases pooled (or no t computable), so the plan calls it inconclusive."
    elif mean_ex < 0 and t <= -2 and support_passed:
        status = "confirmed"
        decided_by = "The pooled excess forward 5-bar return is negative with t <= -2 and negative in at least 2 coins, meeting the confirm rule."
    elif mean_ex > 0 and t >= 2:
        status = "rejected"
        decided_by = "The pooled excess forward 5-bar return is positive with t >= +2 (continuation), meeting the reject rule."
    elif -2 < t < 2:
        status = "inconclusive"
        decided_by = "The pooled t lies strictly between -2 and +2, meeting the inconclusive rule."
    else:
        status = "inconclusive"
        decided_by = ("The pooled t is <= -2 but fewer than 2 coins show a negative excess return, so the confirm rule "
                      "is not met and neither is the reject rule; the result is left inconclusive.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled excess forward 5-bar return after forecast <= -10 (vs holding baseline)",
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": "confirm if negative with t <= -2; reject if positive with t >= +2; at least 30 cases",
        },
        "supporting_check": {
            "name": "number of coins with negative mean excess return",
            "value": n_neg_coins,
            "passed": bool(support_passed),
        },
        "counts": {
            "non-overlapping extreme cases pooled": n,
            "coins": int(len(per_coin)),
            "coins with negative excess": n_neg_coins,
        },
        "decided_by": decided_by,
        "reading": ("The holding baseline is the mean forward 5-bar return over all bars of each coin and window (not only grid bars), "
                    "extreme cases are grid bars at positions 0,5,10,... with forecast <= -10, and 'at least 2 of the 3 coins' is applied "
                    "literally as at least 2 coins negative, which with only BTC and ETH in the record means both."),
    }
