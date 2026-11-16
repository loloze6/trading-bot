import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    THR = -10.0
    MIN_CASES = 30
    COMP = "debug_info.components.rsi_high.last_history_value"
    SCALING = 0.4

    # ---------- 1. Situation check: RSI(14) above 50, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            if "forecast" not in df.columns or COMP not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[COMP], errors="coerce")
            rsi = 50.0 - raw / SCALING
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & rsi.notna() & (rsi > 50.0) & (fc < 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled excess forward 5-bar return after forecast <= -10 (vs coin/window mean 5-bar return)"
    thr_words = ("confirm if pooled excess < 0 with t <= -2 and negative in >= 2 of 3 coins; "
                 "reject if pooled excess > 0 with t >= +2; inconclusive otherwise or if < 30 cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("The plan's situation is a short position only while RSI(14) is above 50, but fewer than 90% "
                           "of the bars with a non-zero forecast are short bars with RSI above 50."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    excess_by_coin = {}
    for coin, wins in bars.items():
        coin_ex = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            valid = np.isfinite(fwd)
            if not valid.any():
                continue
            baseline = float(np.mean(fwd[valid]))
            grid = np.zeros(n, dtype=bool)
            grid[::H] = True
            sel = grid & valid & np.isfinite(fc) & (fc <= THR)
            ex = fwd[sel] - baseline
            coin_ex.extend(ex.tolist())
        excess_by_coin[coin] = coin_ex
        excess_all.extend(coin_ex)

    excess_all = np.asarray(excess_all, dtype=float)
    n_cases = int(len(excess_all))
    mean_ex = float(np.mean(excess_all)) if n_cases > 0 else None
    if n_cases >= 2:
        sd = float(np.std(excess_all, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else float("nan")
    else:
        t = float("nan")

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in excess_by_coin.items()}
    n_neg_coins = int(sum(1 for v in coin_means.values() if v is not None and v < 0))
    coins_ok = n_neg_coins >= 2

    if n_cases < MIN_CASES:
        status = "inconclusive"
        decided = f"Fewer than 30 non-overlapping extreme cases pooled ({n_cases}), so the plan rules inconclusive."
    elif not np.isfinite(t):
        status = "inconclusive"
        decided = "The t-statistic is undefined, so neither the confirm nor the reject rule is met: inconclusive."
    elif mean_ex < 0 and t <= -2 and coins_ok:
        status = "confirmed"
        decided = ("The pooled excess forward return is negative with t <= -2 and is negative in at least 2 coins, "
                   "meeting the confirm rule.")
    elif mean_ex > 0 and t >= 2:
        status = "rejected"
        decided = "The pooled excess forward return is positive with t >= +2 (continuation), meeting the reject rule."
    elif -2 < t < 2:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and +2, so the plan rules inconclusive."
    else:
        status = "inconclusive"
        decided = ("The pooled excess is negative with t <= -2 but negative in fewer than 2 coins, so the confirm rule "
                   "is not fully met and the reject rule is not met: inconclusive.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": (t if np.isfinite(t) else None)},
            "threshold": thr_words,
        },
        "supporting_check": {
            "name": "number of coins with negative mean excess return (need >= 2)",
            "value": n_neg_coins,
            "passed": bool(coins_ok),
        },
        "counts": {
            "non-overlapping extreme cases pooled": n_cases,
            "coins in record": int(len(excess_by_coin)),
            "coins with negative excess": n_neg_coins,
        },
        "decided_by": decided,
        "reading": ("Extreme cases are grid bars (positions 0,5,10,... of each window) with forecast <= -10, the holding "
                    "baseline is the mean 5-bar forward return over all bars of that coin and window that have one, and "
                    "with only the coins present in the record the coin rule still requires at least 2 coins negative."),
    }
