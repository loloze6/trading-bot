import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_high.last_history_value"
    THRESH_FC = -10.0
    MIN_CASES = 30

    # ---------- 1. Situation check: RSI(14) above 50 (raw value < 0), side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # RSI = 50 - raw/0.4 > 50  <=>  raw < 0 ; expected side: short (forecast < 0)
            agree = active & raw.notna() & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "pooled excess forward 5-bar return after forecast <= -10 (non-overlapping), vs coin/window holding mean"
    threshold_txt = "confirm: excess < 0 with t <= -2 and negative in >= 2 coins; reject: excess > 0 with t >= +2; else or < 30 cases inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
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
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid = np.isfinite(fwd)
            if not valid.any():
                continue
            baseline = float(np.mean(fwd[valid]))
            grid = np.arange(0, n, H)
            for i in grid:
                if np.isfinite(fwd[i]) and np.isfinite(fc[i]) and fc[i] <= THRESH_FC:
                    ex = fwd[i] - baseline
                    pooled.append(ex)
                    coin_vals.append(ex)
        per_coin[coin] = coin_vals

    pooled = np.array(pooled, dtype=float)
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
    support_passed = n_neg_coins >= 2

    if n_cases < MIN_CASES:
        status = "inconclusive"
        decided = f"Fewer than {MIN_CASES} non-overlapping extreme cases pooled ({n_cases}), so the plan's inconclusive rule applies."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (zero dispersion), so it is not beyond +/-2 and the result is inconclusive."
    elif mean_ex < 0 and t_stat <= -2 and support_passed:
        status = "confirmed"
        decided = "The pooled excess forward return is negative with t <= -2 and negative in at least 2 coins, meeting the confirm rule."
    elif mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided = "The pooled excess forward return is positive with t >= +2 (continuation), meeting the reject rule."
    elif -2 < t_stat < 2:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and +2, meeting the inconclusive rule."
    else:
        status = "inconclusive"
        decided = ("The pooled excess is negative with t <= -2 but fewer than 2 coins show a negative excess, "
                   "so the confirm rule is not fully met and neither is the reject rule.")

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
            "name": "number of coins with negative mean excess return",
            "value": n_neg_coins,
            "passed": bool(support_passed),
        },
        "counts": {
            "non-overlapping extreme cases pooled": n_cases,
            "coins with negative excess": n_neg_coins,
            "coins in record": n_coins,
        },
        "decided_by": decided,
        "reading": ("Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10 and a defined 5-bar "
                    "forward return, the holding baseline is the mean forward 5-bar return over all bars of that coin and window, "
                    "the per-coin sign is that of the coin's mean excess over its cases, and since only the coins present can be "
                    "counted, 'at least 2 of the 3 coins' is applied as at least 2 coins with negative excess among those in the record."),
    }
