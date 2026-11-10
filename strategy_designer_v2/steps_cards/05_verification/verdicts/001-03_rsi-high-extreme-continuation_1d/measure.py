import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    VAL = "debug_info.components.rsi_high.last_history_value"
    SCALE = 0.4

    # ---------- 1. Situation check: RSI above 50 (graded long), expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            v = pd.to_numeric(df[VAL], errors="coerce")
            ok = f.notna() & v.notna()
            active = ok & (f != 0)
            rsi = 50.0 - v / SCALE
            agree = active & (rsi > 50.0) & (f > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "extreme minus neutral forward 5-bar return", "value": None,
                             "statistic": None,
                             "threshold": "positive with Welch t >= 2 to confirm; negative with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a long position only while RSI(14) is above 50, but fewer than 90% "
                           "of the bars with a non-zero forecast have RSI above 50 with a positive forecast "
                           "(the config standardises the RSI value against its own 60-bar history, so the long "
                           "side follows RSI relative to its recent mean rather than RSI above 50)."),
            "reading": "Situation taken as RSI = 50 - value/0.4 strictly above 50 with forecast > 0.",
        }

    # ---------- 2. Extreme threshold: top 20% of positive forecasts, pooled ----------
    pos = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            pos.append(f[f > 0].dropna().values)
    pos = np.concatenate(pos) if pos else np.array([])
    q80 = float(np.quantile(pos, 0.80)) if len(pos) > 0 else np.inf

    ext_all, neu_all = [], []
    per_coin = {}
    sup_vals = {}
    for coin, wins in bars.items():
        ext_c, neu_c = [], []
        strat_sum, hold_sum = 0.0, 0.0
        n_sup = 0
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            v = pd.to_numeric(df[VAL], errors="coerce").values
            a = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            n = len(df)
            # non-overlapping grid
            for i in range(0, n - H, H):
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(f[i]) and f[i] > 0 and f[i] >= q80:
                    ext_c.append(r)
                if np.isfinite(v[i]) and abs(v[i]) <= 4.0:
                    neu_c.append(r)
            # supporting check: bars with non-zero forecast
            for i in range(n - 1):
                if not (np.isfinite(f[i]) and f[i] != 0):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + 1]) and np.isfinite(a[i]) and c[i] != 0):
                    continue
                r1 = c[i + 1] / c[i] - 1.0
                strat_sum += a[i] * r1
                hold_sum += r1
                n_sup += 1
        ext_all += ext_c
        neu_all += neu_c
        d = (np.mean(ext_c) - np.mean(neu_c)) if (len(ext_c) > 0 and len(neu_c) > 0) else None
        per_coin[coin] = None if d is None else float(d)
        sup_vals[coin] = float(strat_sum - hold_sum) if n_sup > 0 else None

    n_ext, n_neu = len(ext_all), len(neu_all)
    if n_ext >= 2 and n_neu >= 2:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
        t = float(stats.ttest_ind(ext_all, neu_all, equal_var=False).statistic)
    else:
        diff = float(np.mean(ext_all) - np.mean(neu_all)) if (n_ext and n_neu) else None
        t = None

    coins_pos = sum(1 for d in per_coin.values() if d is not None and d > 0)
    coins_neg = sum(1 for d in per_coin.values() if d is not None and d < 0)
    sup_pos = sum(1 for s in sup_vals.values() if s is not None and s > 0)
    sup_passed = bool(sup_pos >= 2)

    enough = n_ext >= 30 and n_neu >= 30
    if not enough:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 non-overlapping extreme cases or fewer than 30 neutral cases in the pool."
    elif t is None or diff is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic cannot be computed."
    elif diff > 0 and t >= 2 and coins_pos >= 2:
        status = "confirmed"
        decided = "Confirm: the extreme-minus-neutral difference is positive with t >= 2 and positive in at least 2 coins."
    elif diff < 0 and t <= -2 and coins_neg >= 2:
        status = "rejected"
        decided = "Reject: the difference is negative with t <= -2, high RSI followed by weaker moves than neutral bars."
    elif -2 < t < 2:
        status = "inconclusive"
        decided = "Inconclusive: t lies between -2 and 2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the result is supported in only one coin."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "extreme minus neutral forward 5-bar return, pooled, before costs",
            "value": diff,
            "statistic": None if t is None else {"name": "Welch t", "value": t},
            "threshold": "positive with t >= 2 and positive in at least 2 of 3 coins to confirm; negative with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "strategy minus buy-and-hold return on non-zero-forecast bars, coins positive",
            "value": float(sup_pos),
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping extreme cases": int(n_ext),
            "neutral cases": int(n_neu),
            "coins with positive difference": int(coins_pos),
            "coins with negative difference": int(coins_neg),
            "coins in record": int(len(per_coin)),
        },
        "decided_by": decided,
        "reading": ("Extreme bars are grid bars whose forecast is at or above the 80th percentile of all positive "
                    "forecasts pooled over coins and windows, neutral bars are grid bars with |component value| <= 4, "
                    "'at least 2 of the 3 coins' is applied as at least 2 of the coins present (the same count "
                    "of 2 negative coins is required for a rejection to be supported in more than one coin), and the "
                    "supporting check sums per-bar strategy and coin returns over each coin's non-zero-forecast bars."),
    }
