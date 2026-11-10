import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_low.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def wilder_rsi(close, period=14):
        d = close.diff()
        up = d.clip(lower=0.0)
        dn = (-d).clip(lower=0.0)
        au = up.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        ad = dn.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        rs = au / ad
        rsi = 100.0 - 100.0 / (1.0 + rs)
        rsi = rsi.where(ad != 0, 100.0)
        rsi = rsi.where(au.notna() & ad.notna())
        return rsi

    ext_all, neu_all = [], []
    per_coin = {}
    sup_diffs = {}

    for coin in sorted(bars.keys()):
        ext_c, neu_c = [], []
        strat_growth = 1.0
        bench_growth = 1.0
        gains_r, allocs = [], []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0 or "close" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True) if RAW in df.columns else pd.Series(np.nan, index=close.index)
            rsi = wilder_rsi(close)
            fwd = close.shift(-H) / close - 1.0
            for t in range(0, len(df), H):
                r = fwd.iloc[t]
                if not np.isfinite(r):
                    continue
                rv = raw.iloc[t]
                if np.isfinite(rv) and rv >= 8:
                    ext_c.append(float(r))
                rs_ = rsi.iloc[t]
                if np.isfinite(rs_) and 40 <= rs_ <= 60:
                    neu_c.append(float(r))
            # supporting check data (per bar, within window)
            if ALLOC in df.columns:
                a = pd.to_numeric(df[ALLOC], errors="coerce").reset_index(drop=True)
                r1 = close.shift(-1) / close - 1.0
                m = a.notna() & r1.notna()
                for av, rv1 in zip(a[m].values, r1[m].values):
                    allocs.append(float(av))
                    gains_r.append(float(rv1))
        ext_all.extend(ext_c)
        neu_all.extend(neu_c)
        diff_c = (np.mean(ext_c) - np.mean(neu_c)) if (len(ext_c) > 0 and len(neu_c) > 0) else None
        per_coin[coin] = {"n_ext": len(ext_c), "n_neu": len(neu_c), "diff": diff_c}
        if len(allocs) > 0:
            allocs_a = np.array(allocs)
            r_a = np.array(gains_r)
            avg = allocs_a.mean()
            strat = np.prod(1.0 + allocs_a * r_a) - 1.0
            bench = np.prod(1.0 + avg * r_a) - 1.0
            sup_diffs[coin] = float(strat - bench)

    n_ext = len(ext_all)
    n_neu = len(neu_all)
    diff = None
    tval = None
    if n_ext >= 2 and n_neu >= 2:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False)
        tval = float(tt.statistic) if np.isfinite(tt.statistic) else None
    elif n_ext >= 1 and n_neu >= 1:
        diff = float(np.mean(ext_all) - np.mean(neu_all))

    coin_diffs = [v["diff"] for v in per_coin.values()]
    n_neg = sum(1 for d in coin_diffs if d is not None and d < 0)
    n_pos = sum(1 for d in coin_diffs if d is not None and d > 0)
    min_coin_ext = min([v["n_ext"] for v in per_coin.values()]) if per_coin else 0

    counts = {"pooled non-overlapping extreme cases": n_ext,
              "pooled non-overlapping neutral cases": n_neu,
              "coins": len(per_coin),
              "coins with negative difference": n_neg}
    for c, v in per_coin.items():
        counts[f"{c} non-overlapping extreme cases"] = v["n_ext"]

    if n_ext < 30 or min_coin_ext < 8 or len(per_coin) == 0 or diff is None:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for a coin, is inconclusive whatever the sign."
    elif diff >= 0:
        status = "rejected"
        decided = "Pooled extreme-minus-neutral 5-bar return is >= 0 (no continuation)."
    elif tval is not None and tval <= -2 and n_neg >= 2 and n_pos == 0:
        status = "confirmed"
        decided = "Pooled extreme-minus-neutral 5-bar return is below 0 with t <= -2 and negative in at least 2 coins."
    elif n_pos > 0:
        status = "inconclusive"
        decided = "Negative pooled difference but coins disagree in sign."
    else:
        status = "inconclusive"
        decided = "Negative pooled difference with t between -2 and 0 (or not enough negative coins)."

    if sup_diffs:
        sup_val = float(np.mean(list(sup_diffs.values())))
        sup_pass = bool(all(v > 0 for v in sup_diffs.values()))
    else:
        sup_val, sup_pass = None, None

    return {
        "status": status,
        "main_measure": {
            "name": "pooled 5-bar forward return, extreme (raw>=8) minus neutral (RSI 40-60) bars",
            "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": "below 0 with t <= -2 and negative in at least 2 of the 3 coins to confirm; >= 0 rejects",
        },
        "supporting_check": {
            "name": "mean per-coin cumulative strategy return minus same-average-size constant short (passed if > 0 for every coin)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Extreme bars use the recorded raw component >= 8 and neutral bars use Wilder RSI(14) recomputed from each window's closes (40 <= RSI <= 60, rows without enough history skipped), both on the 0,5,10,... grid per window; with only the coins present, 'at least 2 of the 3 coins' is applied literally as at least 2 negative coins with none positive, minimum counts are checked first, then a non-negative pooled difference rejects; the supporting check compounds per-bar gains within windows per coin against a constant position equal to the coin's mean allocation.",
    }
