import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    COMP = "debug_info.components.rsi_low.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def wilder_rsi(close, period=14):
        delta = close.diff()
        gain = delta.clip(lower=0.0)
        loss = (-delta).clip(lower=0.0)
        ag = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        al = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        rs = ag / al
        rsi = 100.0 - 100.0 / (1.0 + rs)
        rsi = rsi.where(al != 0, 100.0)
        rsi[ag.isna() | al.isna()] = np.nan
        return rsi

    ext_all, neu_all = [], []
    per_coin = {}
    support = {}

    for coin in sorted(bars.keys()):
        ext_c, neu_c = [], []
        strat_gains, bench_r, allocs = [], [], []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if "close" not in df.columns or len(df) == 0:
                continue
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            rsi = wilder_rsi(close)
            comp = df[COMP].astype(float) if COMP in df.columns else pd.Series(np.nan, index=df.index)

            for i in range(0, len(df), H):
                r = fwd.iloc[i]
                if pd.isna(r):
                    continue
                c = comp.iloc[i]
                is_ext = (not pd.isna(c)) and c >= 8.0
                if is_ext:
                    ext_c.append(r)
                    continue
                rv = rsi.iloc[i]
                if (not pd.isna(rv)) and 40.0 <= rv <= 60.0:
                    neu_c.append(r)

            # supporting check data (per-bar, within window)
            r1 = close.shift(-1) / close - 1.0
            if ALLOC in df.columns:
                a = df[ALLOC].astype(float)
                ok = (~a.isna()) & (~r1.isna())
                strat_gains.extend((a[ok] * r1[ok]).tolist())
                bench_r.extend(r1[ok].tolist())
                allocs.extend(a[ok].tolist())

        ext_all.extend(ext_c)
        neu_all.extend(neu_c)
        diff_c = (float(np.mean(ext_c)) - float(np.mean(neu_c))) if (len(ext_c) > 0 and len(neu_c) > 0) else None
        per_coin[coin] = {"n_extreme": len(ext_c), "n_neutral": len(neu_c), "diff": diff_c}

        if len(allocs) > 0:
            avg_size = float(np.mean(np.abs(allocs)))
            strat_cum = float(np.prod(1.0 + np.array(strat_gains)) - 1.0)
            bench_cum = float(np.prod(1.0 - avg_size * np.array(bench_r)) - 1.0)
            support[coin] = strat_cum - bench_cum

    n_ext = len(ext_all)
    n_neu = len(neu_all)
    if n_ext > 0 and n_neu > 0:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
    else:
        diff = None
    t = None
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    n_coins = len(per_coin)
    neg_coins = sum(1 for v in per_coin.values() if v["diff"] is not None and v["diff"] < 0)
    pos_coins = sum(1 for v in per_coin.values() if v["diff"] is not None and v["diff"] > 0)
    min_coin_ext = min([v["n_extreme"] for v in per_coin.values()]) if per_coin else 0

    if n_ext < 30 or min_coin_ext < 8 or n_coins == 0:
        status = "inconclusive"
        decided = "Fewer than 30 pooled non-overlapping extreme cases or fewer than 8 for some coin, which is inconclusive whatever the sign."
    elif diff is None:
        status = "inconclusive"
        decided = "The pooled extreme-minus-neutral difference cannot be computed (an empty group), so the result is inconclusive."
    elif diff >= 0:
        status = "rejected"
        decided = "Pooled extreme-minus-neutral 5-bar return is >= 0, which meets the reject rule."
    elif t is not None and t <= -2 and neg_coins >= 2:
        status = "confirmed"
        decided = "Pooled extreme-minus-neutral 5-bar return is below 0 with t <= -2 and negative in at least 2 coins, which meets the confirm rule."
    else:
        status = "inconclusive"
        decided = "Negative pooled difference but t is above -2 or coins disagree in sign / fewer than 2 coins negative, which is inconclusive."

    sup_val = float(np.mean(list(support.values()))) if support else None
    sup_pass = (all(v > 0 for v in support.values())) if support else None

    counts = {"non-overlapping extreme cases pooled": n_ext,
              "non-overlapping neutral cases pooled": n_neu,
              "coins with negative difference": neg_coins,
              "coins with positive difference": pos_coins,
              "coins in record": n_coins}
    for coin, v in per_coin.items():
        counts["extreme cases " + coin] = v["n_extreme"]
        counts["neutral cases " + coin] = v["n_neutral"]
        if v["diff"] is not None:
            counts["difference " + coin] = v["diff"]
    for coin, v in support.items():
        counts["strategy minus same-size short " + coin] = v

    return {
        "status": status,
        "main_measure": {
            "name": "pooled 5-bar forward return, extreme (component>=8) minus neutral (RSI 40-60)",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
            "threshold": "confirm if below 0 with t <= -2 and negative in at least 2 of the 3 coins; reject if >= 0",
        },
        "supporting_check": {
            "name": "mean per-coin cumulative strategy return minus same-average-size short hold (passed if positive for every coin)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Extreme bars use the recorded component >= 8 while neutral bars use Wilder RSI(14) recomputed from each window's closes "
                    "(40 <= RSI <= 60, extreme bars excluded), both sampled on the 0,5,10,... grid per window; with only 2 coins in the record "
                    "'negative in at least 2 of the 3 coins' requires both to be negative; the supporting check compounds per-bar gains within "
                    "windows against a short of the mean absolute allocation and passes only if positive for every coin."),
    }
