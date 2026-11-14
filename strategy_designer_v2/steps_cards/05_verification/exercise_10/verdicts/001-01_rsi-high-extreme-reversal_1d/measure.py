import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    EXTREME = -10.0
    MIN_CASES = 30
    RAW = "debug_info.components.rsi_high.last_history_value"

    def _num(x):
        if x is None:
            return None
        x = float(x)
        return None if not np.isfinite(x) else x

    # ---------- 1. situation check ----------
    # Fidelity: situation = RSI above 50 (graded high readings); outcome = fall -> short.
    # RSI = 50 - raw/0.4, so RSI > 50 <=> raw < 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            f = sub["forecast"].astype(float).values
            raw = sub[RAW].astype(float).values
            rsi = 50.0 - raw / 0.4
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & (rsi > 50.0) & (f < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "pooled excess forward 5-bar return after forecast <= -10 (minus same coin/window mean forward 5-bar return), non-overlapping"
    threshold = "confirm: negative with t <= -2 and negative in at least 2 of the 3 coins; reject: positive with t >= +2; inconclusive otherwise or fewer than 30 pooled cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _num(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars with RSI above 50, so the config's forecast "
                           "does not trade the plan's situation (short while RSI is high)."
                           if n_active > 0 else
                           "The record holds no active (non-zero forecast) bars, so the config never trades the plan's situation."),
            "reading": "Situation taken as RSI(14) > 50 (raw value < 0) on the short side, per the Fidelity lines.",
        }

    # ---------- 2. criterion ----------
    pooled = []
    per_coin = {}
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            fc = d["forecast"].astype(float)
            valid_fwd = fwd.notna() & np.isfinite(fwd)
            if valid_fwd.sum() == 0:
                continue
            baseline = float(fwd[valid_fwd].mean())
            pos = np.arange(len(d))
            grid = (pos % H) == 0
            sel = grid & valid_fwd.values & fc.notna().values & (fc.values <= EXTREME)
            ex = (fwd.values[sel] - baseline).tolist()
            coin_vals.extend(ex)
            pooled.extend(ex)
        per_coin[coin] = coin_vals

    n = len(pooled)
    arr = np.asarray(pooled, dtype=float)
    mean = float(arr.mean()) if n > 0 else None
    if n > 1:
        sd = float(arr.std(ddof=1))
        t = mean / (sd / np.sqrt(n)) if sd > 0 else None
    else:
        t = None

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))
    n_coins = len(per_coin)
    support_passed = n_neg_coins >= 2

    counts = {
        "non-overlapping extreme cases pooled": int(n),
        "coins with negative excess return": n_neg_coins,
        "coins in record": int(n_coins),
    }
    for c, v in per_coin.items():
        counts[f"extreme cases {c}"] = int(len(v))

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} non-overlapping extreme cases pooled, below the plan's minimum of 30."
    elif mean is not None and t is not None and mean < 0 and t <= -2 and support_passed:
        status = "confirmed"
        decided = "Pooled excess forward return is negative with t <= -2 and negative in at least 2 coins (confirm rule)."
    elif mean is not None and t is not None and mean > 0 and t >= 2:
        status = "rejected"
        decided = "Pooled excess forward return is positive with t >= +2 (reject rule: continuation, not reversal)."
    else:
        status = "inconclusive"
        if t is not None and t <= -2 and not support_passed:
            decided = "t <= -2 but the excess return is negative in fewer than 2 coins, so neither confirm nor reject is met (inconclusive)."
        else:
            decided = "t lies strictly between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": _num(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": _num(mean),
            "statistic": ({"name": "t of the mean", "value": _num(t)} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "sign of excess return per coin (negative in at least 2 coins)",
            "value": float(n_neg_coins),
            "passed": bool(support_passed),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10 and a 5-bar forward "
                    "return inside the window, the baseline is the mean 5-bar forward return over all bars of that coin and "
                    "window that have one, the t is the ordinary t of the pooled mean, and 'at least 2 of the 3 coins' is "
                    "applied literally as at least 2 coins with negative mean excess return among the coins present."),
    }
