import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_N = 30

    # Top-20% cut-off of the non-zero forecast values, pooled over every bar in the record
    all_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").dropna()
            all_fc.append(fc[fc != 0].values)
    nz = np.concatenate(all_fc) if all_fc else np.array([])
    thr = float(np.quantile(nz, 0.8)) if len(nz) > 0 else np.nan

    ext_all, neu_all = [], []
    per_coin = {}
    support_total = 0.0
    support_any = False
    support_per_coin = {}

    for coin, wins in bars.items():
        ext_c, neu_c = [], []
        strat_sum = 0.0
        coin_ret_sum = 0.0
        alloc_vals = []
        has_support = False
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            n = len(df)

            # Non-overlapping 5-bar grid: positions 0, 5, 10, ... with t+5 inside the window
            for t in range(0, n - H, H):
                c0, c1, f = close[t], close[t + H], fc[t]
                if np.isnan(c0) or np.isnan(c1) or np.isnan(f) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                if not np.isnan(thr) and f != 0 and f >= thr:
                    ext_c.append(r)
                elif f < 1:
                    neu_c.append(r)

            # Supporting check: per-bar gains before costs, inside this window only
            for t in range(n - 1):
                a, c0, c1 = alloc[t], close[t], close[t + 1]
                if np.isnan(a) or np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                r1 = c1 / c0 - 1.0
                strat_sum += a * r1
                coin_ret_sum += r1
                alloc_vals.append(a)
                has_support = True

        ext_all += ext_c
        neu_all += neu_c
        d = (np.mean(ext_c) - np.mean(neu_c)) if (len(ext_c) > 0 and len(neu_c) > 0) else None
        per_coin[coin] = {"diff": d, "n_extreme": len(ext_c), "n_neutral": len(neu_c)}

        if has_support:
            avg_exp = float(np.mean(alloc_vals))
            excess = strat_sum - avg_exp * coin_ret_sum
            support_per_coin[coin] = excess
            support_total += excess
            support_any = True

    n_ext, n_neu = len(ext_all), len(neu_all)
    diff, tval = None, None
    if n_ext > 0 and n_neu > 0:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False)
        tval = float(tt.statistic) if np.isfinite(tt.statistic) else None

    coins_positive = sum(1 for v in per_coin.values() if v["diff"] is not None and v["diff"] > 0)
    support_val = float(support_total) if support_any else None
    support_pass = (support_val > 0) if support_val is not None else None

    if n_ext < MIN_N or n_neu < MIN_N or tval is None:
        status = "inconclusive"
        decided = (f"Inconclusive: fewer than 30 non-overlapping extreme cases ({n_ext}) "
                   f"or neutral cases ({n_neu}) pooled, or no t-statistic could be computed.")
    elif tval <= -2:
        status = "rejected"
        decided = f"Rejected: the pooled t ({tval:.2f}) is -2 or below, pointing to reversal."
    elif tval <= 0:
        status = "rejected"
        decided = f"Rejected: the pooled extreme-minus-neutral difference is zero or negative (t = {tval:.2f} <= 0)."
    elif tval >= 2 and coins_positive >= 2 and support_pass:
        status = "confirmed"
        decided = (f"Confirmed: the difference is positive with t = {tval:.2f} >= 2, positive in "
                   f"{coins_positive} coins (>= 2), and the pooled supporting excess is positive.")
    elif tval >= 2:
        status = "inconclusive"
        decided = (f"Inconclusive: t = {tval:.2f} >= 2 but the remaining confirm conditions fail "
                   f"(coins positive = {coins_positive}, supporting excess positive = {support_pass}), "
                   f"and the reject rule (t <= 0) is not met.")
    else:
        status = "inconclusive"
        decided = f"Inconclusive: t = {tval:.2f} lies between 0 and 2."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 5-bar forward return, extreme minus neutral bars, pooled",
            "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": "positive with t >= 2 confirms (with >= 2 of 3 coins positive and positive pooled support); t <= 0 rejects",
        },
        "supporting_check": {
            "name": "strategy return minus exposure-scaled buy-and-hold, summed over coins",
            "value": support_val,
            "passed": support_pass,
        },
        "counts": {
            "non-overlapping extreme cases": int(n_ext),
            "neutral cases": int(n_neu),
            "coins with positive difference": int(coins_positive),
            "coins": int(len(per_coin)),
        },
        "decided_by": decided,
        "reading": (
            "Extreme bars are those whose forecast is at or above the 80th percentile of all non-zero forecasts "
            "pooled over every bar of every coin and window, and neutral bars are those whose forecast is below 1, "
            "both taken on the 0,5,10,... grid of each window. With only the coins present in the record, the rule "
            "'positive in at least 2 of the 3 coins' is applied as at least 2 positive coins. The supporting excess "
            "is computed per coin as the sum of per-bar gains (allocation x next-bar return) minus the mean allocation "
            "times the sum of the coin's per-bar returns, all inside each window, and these per-coin excesses are "
            "summed to give the pooled value."
        ),
    }
