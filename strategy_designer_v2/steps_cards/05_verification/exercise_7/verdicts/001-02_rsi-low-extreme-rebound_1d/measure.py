import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5

    def find_col(df, suffix):
        cols = [c for c in df.columns if c.startswith("debug_info.components.") and c.endswith(suffix)]
        return cols[0] if cols else None

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            col = find_col(df, ".last_history_value")
            if col is None:
                continue
            sub = df[["forecast", col]].dropna()
            f = sub["forecast"].astype(float).values
            v = sub[col].astype(float).values
            active = f != 0
            # Raw value > 0 means RSI below 50. The expected side is long.
            situation = v > 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation (RSI-14 below 50, long only) does not hold, on the long side, "
                           "on at least 90% of the bars where the config's forecast is non-zero."),
            "reading": "none",
        }

    # ---------- 2. Top-quintile threshold (pooled over all positive forecasts) ----------
    pos_all = []
    for coin in bars:
        for w in bars[coin]:
            f = bars[coin][w]["forecast"].astype(float)
            pos_all.append(f[f > 0].dropna().values)
    pos_all = np.concatenate(pos_all) if pos_all else np.array([])
    q80 = float(np.quantile(pos_all, 0.8)) if pos_all.size > 0 else np.inf

    # ---------- Non-overlapping samples ----------
    recs = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and np.isfinite(fc[i])):
                    continue
                if close[i] == 0:
                    continue
                recs.append((coin, w, fc[i], close[i + H] / close[i] - 1.0))
    s = pd.DataFrame(recs, columns=["coin", "window", "forecast", "ret"])

    top = s[(s["forecast"] > 0) & (s["forecast"] >= q80)]
    flat = s[s["forecast"] == 0]

    def excess(t, z):
        if len(t) == 0 or len(z) == 0:
            return None
        return float(t["ret"].mean() - z["ret"].mean())

    pooled = excess(top, flat)
    tstat = None
    if len(top) >= 2 and len(flat) >= 2:
        r = stats.ttest_ind(top["ret"].values, flat["ret"].values, equal_var=False)
        tstat = float(r.statistic) if np.isfinite(r.statistic) else None

    coins = sorted(bars.keys())
    per_coin = {}
    per_coin_n = {}
    for c in coins:
        per_coin[c] = excess(top[top["coin"] == c], flat[flat["coin"] == c])
        per_coin_n[c] = int((top["coin"] == c).sum())
    n_pos_coins = sum(1 for c in coins if per_coin[c] is not None and per_coin[c] > 0)
    n_nonpos_coins = sum(1 for c in coins if per_coin[c] is not None and per_coin[c] <= 0)

    # ---------- Supporting check ----------
    pos = s[s["forecast"] > 0]
    rho = None
    sc_passed = None
    if len(pos) >= 3 and pos["forecast"].nunique() > 1 and pos["ret"].nunique() > 1:
        rr = stats.spearmanr(pos["forecast"].values, pos["ret"].values)
        rho = float(rr.correlation) if np.isfinite(rr.correlation) else None
        sc_passed = (rho > 0) if rho is not None else None

    counts = {"pooled non-overlapping top-quintile cases": int(len(top)),
              "non-overlapping flat cases": int(len(flat)),
              "coins with positive excess": int(n_pos_coins),
              "coins with non-positive excess": int(n_nonpos_coins)}
    for c in coins:
        counts[f"top-quintile cases {c}"] = per_coin_n[c]

    # ---------- Decision ----------
    min_coin = min(per_coin_n.values()) if per_coin_n else 0
    if len(top) < 30 or min_coin < 8 or pooled is None:
        status = "inconclusive"
        decided = ("Inconclusive: fewer than 30 pooled non-overlapping top-quintile cases, "
                   "or fewer than 8 for at least one coin.")
    elif pooled > 0 and tstat is not None and tstat >= 2 and n_pos_coins >= 2:
        status = "confirmed"
        decided = ("Confirm: the pooled excess return is above 0, its Welch t is at least 2, "
                   "and it is positive in at least 2 coins.")
    elif pooled <= 0 and n_nonpos_coins >= 2:
        status = "rejected"
        decided = "Reject: the pooled excess return is at or below 0, and it is non-positive in at least 2 coins."
    else:
        status = "inconclusive"
        decided = ("Inconclusive: the excess return is positive with a t below 2, "
                   "or the coins disagree beyond the confirm and reject rules.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "top-quintile forecast fwd 5-bar return minus flat-bar fwd 5-bar return",
            "value": pooled,
            "statistic": {"name": "Welch t", "value": tstat} if tstat is not None else None,
            "threshold": "excess above 0 with t >= 2 and positive in at least 2 of the coins",
        },
        "supporting_check": {"name": "Spearman rank correlation of forecast vs fwd 5-bar return on positive-forecast bars",
                             "value": rho, "passed": sc_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The top quintile is the forecast at or above the 80th percentile of all positive forecasts, "
                    "pooled over coins and windows; samples (also for the Spearman check) are the bars at positions "
                    "0, 5, 10, ... of each window; and since only BTC and ETH ran, 'at least 2 of the 3 coins' "
                    "and the 8-per-coin minimum are applied to the coins present."),
    }
