import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    COMP = "debug_info.components.rsi_low.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def rsi_wilder(close, period=14):
        delta = close.diff()
        gain = delta.clip(lower=0.0)
        loss = (-delta).clip(lower=0.0)
        avg_g = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        avg_l = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        rs = avg_g / avg_l
        rsi = 100.0 - 100.0 / (1.0 + rs)
        rsi = rsi.where(avg_l != 0, 100.0)
        rsi = rsi.where(avg_g.notna() & avg_l.notna())
        return rsi

    pooled_ext, pooled_neu = [], []
    per_coin = {}
    support = {}

    for coin in sorted(bars.keys()):
        c_ext, c_neu = [], []
        strat_sum = 0.0
        alloc_all = []
        ret_rows = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            comp = pd.to_numeric(df[COMP], errors="coerce").astype(float) if COMP in df else pd.Series(np.nan, index=df.index)
            rsi = rsi_wilder(close)
            fwd = close.shift(-H) / close - 1.0
            n = len(df)
            for i in range(0, n, H):
                r = fwd.iloc[i]
                if not np.isfinite(r):
                    continue
                cv = comp.iloc[i]
                if np.isfinite(cv) and cv >= 8:
                    c_ext.append(r)
                rv = rsi.iloc[i]
                if np.isfinite(rv) and 40.0 <= rv <= 60.0:
                    c_neu.append(r)
            # supporting check data
            alloc = pd.to_numeric(df[ALLOC], errors="coerce").astype(float) if ALLOC in df else pd.Series(np.nan, index=df.index)
            r1 = close.shift(-1) / close - 1.0
            for i in range(n):
                a, rr = alloc.iloc[i], r1.iloc[i]
                if np.isfinite(a):
                    alloc_all.append(a)
                if np.isfinite(a) and np.isfinite(rr):
                    strat_sum += a * rr
                    ret_rows.append(rr)
        pooled_ext.extend(c_ext)
        pooled_neu.extend(c_neu)
        diff = (np.mean(c_ext) - np.mean(c_neu)) if (len(c_ext) > 0 and len(c_neu) > 0) else None
        per_coin[coin] = {"n_extreme": len(c_ext), "n_neutral": len(c_neu),
                          "diff": float(diff) if diff is not None else None}
        if len(alloc_all) > 0 and len(ret_rows) > 0:
            avg_size = float(np.mean(np.abs(alloc_all)))
            bench = -avg_size * float(np.sum(ret_rows))
            support[coin] = float(strat_sum - bench)
        else:
            support[coin] = None

    n_ext = len(pooled_ext)
    n_neu = len(pooled_neu)
    diff = None
    tval = None
    if n_ext > 0 and n_neu > 0:
        diff = float(np.mean(pooled_ext) - np.mean(pooled_neu))
    if n_ext >= 2 and n_neu >= 2:
        t = stats.ttest_ind(pooled_ext, pooled_neu, equal_var=False).statistic
        tval = float(t) if np.isfinite(t) else None

    n_neg_coins = sum(1 for c in per_coin.values() if c["diff"] is not None and c["diff"] < 0)
    signs = [np.sign(c["diff"]) for c in per_coin.values() if c["diff"] is not None]
    min_coin_ext = min([c["n_extreme"] for c in per_coin.values()]) if per_coin else 0

    if n_ext < 30 or min_coin_ext < 8 or len(per_coin) == 0:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme cases pooled or fewer than 8 for some coin, which is inconclusive whatever the sign."
    elif diff is None:
        status = "inconclusive"
        decided = "The pooled extreme-minus-neutral difference could not be computed (no neutral cases), so the result is inconclusive."
    elif diff >= 0:
        status = "rejected"
        if tval is not None and tval >= 2:
            decided = "Pooled extreme-minus-neutral 5-bar return is positive with t >= 2 (reversal instead of continuation): rejected."
        else:
            decided = "Pooled extreme-minus-neutral 5-bar return is >= 0: rejected."
    elif tval is not None and tval <= -2 and n_neg_coins >= 2:
        status = "confirmed"
        decided = "Pooled extreme-minus-neutral 5-bar return is below 0 with t <= -2 and negative in at least 2 coins: confirmed."
    else:
        status = "inconclusive"
        if tval is None or tval > -2:
            decided = "Negative pooled difference with t between -2 and 0 (or t not computable): inconclusive."
        else:
            decided = "Negative pooled difference with t <= -2 but fewer than 2 coins negative (coins disagree in sign): inconclusive."

    sup_vals = [v for v in support.values() if v is not None]
    sup_value = float(np.sum(sup_vals)) if sup_vals else None
    sup_passed = (all(v > 0 for v in sup_vals) if sup_vals and len(sup_vals) == len(support) else None)

    counts = {"non-overlapping extreme cases pooled": int(n_ext),
              "non-overlapping neutral cases pooled": int(n_neu),
              "coins with negative difference": int(n_neg_coins),
              "coins in record": int(len(per_coin))}
    for coin, c in per_coin.items():
        counts["extreme cases " + coin] = int(c["n_extreme"])
        counts["neutral cases " + coin] = int(c["n_neutral"])

    return {
        "status": status,
        "main_measure": {
            "name": "pooled extreme-minus-neutral 5-bar forward return",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": tval} if tval is not None else None),
            "threshold": "confirm if below 0 with t <= -2 and negative in at least 2 coins; reject if >= 0; at least 30 extreme cases pooled and 8 per coin",
        },
        "supporting_check": {
            "name": "strategy cumulative return minus same-average-size short hold, summed over coins",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Extreme bars are those with raw component >= 8 and neutral bars are those with Wilder RSI(14) "
                    "recomputed from each window's own closes between 40 and 60 inclusive (the first 14 bars of each window, "
                    "with no RSI, are left out of the neutral group); both use the 0,5,10,... grid per window. "
                    "Since only 2 coins are in the record, 'negative in at least 2 of the 3 coins' is applied literally "
                    "as at least 2 coins negative. The supporting check uses summed per-bar gains, "
                    "with the benchmark being a short of the coin's mean absolute allocation, "
                    "and it passes only if every coin is above zero."),
    }
