import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_low.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def wilder_rsi(close, period=14):
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)
        ag = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
        al = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
        rs = ag / al
        rsi = 100 - 100 / (1 + rs)
        rsi = rsi.where(al != 0, 100.0)
        rsi = rsi.where(ag.notna() & al.notna())
        return rsi

    ext_all, neu_all = [], []
    per_coin = {}
    support = {}

    for coin in sorted(bars.keys()):
        ext_c, neu_c = [], []
        strat_rets, coin_rets, allocs = [], [], []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float)
            n = len(df)
            fwd = close.shift(-H) / close - 1
            rsi = wilder_rsi(close)
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            for i in range(0, n, H):
                r = fwd.iloc[i]
                if pd.isna(r):
                    continue
                rv = raw.iloc[i]
                if pd.notna(rv) and rv >= 8:
                    ext_c.append(float(r))
                ri = rsi.iloc[i]
                if pd.notna(ri) and 40 <= ri <= 60:
                    neu_c.append(float(r))
            # supporting-check data
            r1 = close.shift(-1) / close - 1
            a = df[ALLOC].astype(float) if ALLOC in df.columns else pd.Series(np.nan, index=df.index)
            m = r1.notna() & a.notna()
            strat_rets.extend((a[m] * r1[m]).tolist())
            coin_rets.extend(r1[m].tolist())
            allocs.extend(a[m].tolist())
        ext_all.extend(ext_c)
        neu_all.extend(neu_c)
        diff_c = (np.mean(ext_c) - np.mean(neu_c)) if (len(ext_c) > 0 and len(neu_c) > 0) else None
        per_coin[coin] = {"n_extreme": len(ext_c), "n_neutral": len(neu_c), "diff": diff_c}
        if len(strat_rets) > 0:
            avg = float(np.mean(allocs))
            strat_cum = float(np.prod(1 + np.array(strat_rets)) - 1)
            bench_cum = float(np.prod(1 + avg * np.array(coin_rets)) - 1)
            support[coin] = strat_cum - bench_cum
        else:
            support[coin] = None

    n_ext = len(ext_all)
    n_neu = len(neu_all)
    if n_ext > 0 and n_neu > 0:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
    else:
        diff = None
    t = None
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False).statistic
        if np.isfinite(tt):
            t = float(tt)

    n_coins = len(per_coin)
    neg_coins = sum(1 for c in per_coin.values() if c["diff"] is not None and c["diff"] < 0)
    pos_coins = sum(1 for c in per_coin.values() if c["diff"] is not None and c["diff"] >= 0)
    min_coin_ext = min([c["n_extreme"] for c in per_coin.values()]) if per_coin else 0

    if n_ext < 30 or min_coin_ext < 8 or diff is None:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for some coin, is inconclusive whatever the sign."
    elif diff >= 0:
        status = "rejected"
        decided = "Pooled extreme-minus-neutral 5-bar return is >= 0 (reject)."
    elif t is not None and t <= -2 and neg_coins >= 2:
        status = "confirmed"
        decided = "Pooled extreme-minus-neutral 5-bar return is below 0 with t <= -2 and negative in at least 2 coins (confirm)."
    else:
        status = "inconclusive"
        if pos_coins > 0 and neg_coins > 0:
            decided = "Coins disagree in sign of the extreme-minus-neutral difference (inconclusive)."
        else:
            decided = "Negative pooled difference with t between -2 and 0, or not negative in at least 2 coins (inconclusive)."

    sup_vals = [v for v in support.values() if v is not None]
    sup_value = float(np.mean(sup_vals)) if sup_vals else None
    sup_passed = (all(v > 0 for v in sup_vals) if sup_vals else None)

    counts = {"pooled non-overlapping extreme cases": n_ext,
              "pooled non-overlapping neutral cases": n_neu,
              "coins": n_coins,
              "coins with negative difference": neg_coins}
    for coin, c in per_coin.items():
        counts["extreme cases " + coin] = c["n_extreme"]

    return {
        "status": status,
        "main_measure": {
            "name": "pooled 5-bar forward return, extreme (raw>=8) minus neutral (RSI 40-60) bars",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
            "threshold": "below 0 with t <= -2 and negative in at least 2 of the coins confirms; >= 0 rejects",
        },
        "supporting_check": {
            "name": "mean over coins of strategy cumulative return minus same-average-size constant position",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Neutral RSI is Wilder RSI(14) recomputed from each window's closes only (first bars without RSI left out), "
                    "extremes use the recorded raw component >= 8, both on the 0,5,10,... grid per window; with only 2 coins present "
                    "'at least 2 of the 3 coins' requires both coins negative; the supporting check compounds per-bar gains over all "
                    "windows against a constant position equal to the coin's mean allocation and passes if positive for every coin."),
    }
